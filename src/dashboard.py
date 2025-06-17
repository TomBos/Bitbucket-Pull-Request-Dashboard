#!/usr/bin/env python

from request_controller import requestController as rc
from cache_manager import cacheManager as cm
from dotenv import load_dotenv

import os
import json
import sys
import time
import datetime

keys = ["API_KEY", "API_USER", "ORGANIZATION", "PROJECT"]

load_dotenv() 

for key in keys:
    if not os.getenv(key): 
        raise ValueError(f"Missing required environment variable {key}")

org = os.getenv("ORGANIZATION")
project = os.getenv("PROJECT")
user = os.getenv("API_USER")
api_key = os.getenv("API_KEY")

file_path =  "cache/pr_overview.json"
can_recache = True

if os.path.exists(file_path):
    mod_time = os.path.getmtime(file_path) 
    can_recache = mod_time < (time.time() - 3600) 

if can_recache:
    req = rc(user,api_key)
    endpoint = req.build_url(["repositories",org,project,"pullrequests"])
    res = req.get(endpoint)

    cache = cm()
    cache.save_json_cache(res,file_path)

    pull_requests = res["values"]
    for pr in pull_requests:
        endpoint = req.build_url(["repositories",org,project,"pullrequests",pr["id"]])
        res = req.get(endpoint)
        if not res["draft"]:
            file_path = f"cache/{pr["id"]}.pr.json"
            cache.save_json_cache(res,file_path)


data = None
with open("cache/6888.pr.json", "r") as f:
    data = json.load(f)


author = data["author"]["display_name"]
participants = data["participants"]
approved_count = 0

print(f"Autor: {author}")

for participant in participants:
    if participant["user"]["display_name"] != author:
        if participant["approved"]:
            approved_count += 1
        print(f"Participant: {participant["user"]["display_name"]}")

print(f"Approved: {approved_count}")

sys.exit(0)

"""
def load_pull_requests():
    cache_file = "pullrequests.json"
    
    # Check if cache file exists
    if not os.path.exists(cache_file):
        print("Cache file not found, fetching pull requests...")
        if cache_master_file() != 1:
            raise RuntimeError("Failed to fetch pull requests")
    
    # Load and return the cached data
    try:
        with open(cache_file, "r") as f:
            # print("Loading data from cache...")
            return json.load(f)
    except (IOError, json.JSONDecodeError) as e:
        print(f"Error loading cache: {e}")
        # Attempt to refresh cache if corrupted
        print("Attempting to refresh cache...")
        if cache_master_file() != 1:
            raise RuntimeError("Failed to refresh pull requests cache")
        with open(cache_file, "r") as f:
            return json.load(f)
        
def get_single_pull_request(pullrequest_id):
    if not os.path.exists(f"{pullrequest_id}.pr.json"):
        print(f"Fetching pr {pullrequest_id} ...")
    
    
    return
"""

# Load pull requests data
# pull_requests_data = load_pull_requests()
# print(f"Successfully loaded {len(pull_requests_data)} pull requests from cache")
# print(f"Found {len(pull_requests_data)} pull requests:")
# y = json.dumps(pull_requests_data[1])
# print(y)

# List of what i need:
# id
# title
# state
# draft
# author
# updated_on
# created_on


# using ID's then fetch each PR into file if it is not already cached and it havent been 1h since last upload
# for pr in pull_requests_data:
#       get_single_pull_request(pr["id"])



sys.exit(1)

for pr in pull_requests_data:
    print(f"- #{pr['id']}: {pr['title']} (state: {pr['state']})")

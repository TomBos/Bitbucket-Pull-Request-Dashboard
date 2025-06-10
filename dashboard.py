#!/usr/bin/env python

from dotenv import load_dotenv

import os
import requests
import json
import sys

def cache_pull_requests():
    try:
        load_dotenv()
        auth_v2 = os.getenv("API_KEY")
        user = os.getenv("API_USER")
        organization = os.getenv("ORGANIZATION")
        project = os.getenv("PROJECT")

        if not all([auth_v2, user, organization, project]):
            raise ValueError("Missing required environment variables")

        base_url = "https://api.bitbucket.org/2.0"
        endpoint = f"{base_url}/repositories/{organization}/{project}/pullrequests"

        response = requests.get(
            endpoint,
            auth=(user, auth_v2),
            headers={"Accept": "application/json"},
            params={"pagelen": 50}
        )

        response.raise_for_status()
        parsed_response = response.json()
        data = parsed_response["values"]

        with open("pullrequests.json", "w") as f:
            json.dump(data, f, indent=2)

        print("Saved to pullrequests.json")
        return 1

    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")
        return 0
    except (ValueError, IOError, json.JSONDecodeError) as e:
        print(f"Processing error: {e}")
        return 0

def load_pull_requests():
    """Load pull requests from cache or fetch if cache doesn't exist"""
    cache_file = "pullrequests.json"
    
    # Check if cache file exists
    if not os.path.exists(cache_file):
        print("Cache file not found, fetching pull requests...")
        if cache_pull_requests() != 1:
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
        if cache_pull_requests() != 1:
            raise RuntimeError("Failed to refresh pull requests cache")
        with open(cache_file, "r") as f:
            return json.load(f)
        
def get_single_pull_request(pullrequest_id):
    if not os.path.exists(f"{pullrequest_id}.pr.json"):
        print(f"Fetching pr {pullrequest_id} ...")
    
    
    return

# Load pull requests data
pull_requests_data = load_pull_requests()
# print(f"Successfully loaded {len(pull_requests_data)} pull requests from cache")
# print(f"Found {len(pull_requests_data)} pull requests:")
y = json.dumps(pull_requests_data[1])
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
for pr in pull_requests_data:
    get_single_pull_request(pr["id"])



sys.exit(1)

for pr in pull_requests_data:
    print(f"- #{pr['id']}: {pr['title']} (state: {pr['state']})")

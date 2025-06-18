#!/usr/bin/env python

from http.server import BaseHTTPRequestHandler, HTTPServer

from request_controller import RequestController
from cache_manager import CacheManager
from dotenv import load_dotenv

import json
import os
import sys
import time
import datetime

APPROVAL_THRESHOLD = 2
CACHE_DIR = "cache/"
CACHE_TTL = 3600

def load_env_vars(required_keys):
    load_dotenv()
    env = {}
    for key in required_keys:
        value = os.getenv(key)
        if not value:
            raise ValueError(f"Missing required environment variable {key}")
        env[key] = value
    return env

config = load_env_vars(["API_KEY", "API_USER", "ORGANIZATION", "PROJECT"])

class ServerController(BaseHTTPRequestHandler):
    def _set_headers(self, status=200, content_type="application/json"):
        self.send_response(status)
        self.send_header("Content-type", content_type)
        self.end_headers()

    def do_GET(self):
        if self.path == "/reload-cache":
            pr_overview_path = os.path.join(CACHE_DIR, "pr_overview.json")
            
            try:
                mod_time = os.path.getmtime(pr_overview_path)
                cache_expired = (time.time() - mod_time) > CACHE_TTL
            except FileNotFoundError:
                cache_expired = True

            if not cache_expired:
                return
            
            cache = CacheManager()
            cache.clear_pr_cache(CACHE_DIR) 
    
            req = RequestController(config["API_USER"], config["API_KEY"])
            base_endpoint = req.build_url([
                "repositories",
                config["ORGANIZATION"],
                config["PROJECT"],
                "pullrequests"
            ]) 
            
            try:
                overview_response = req.get(base_endpoint)
            except Exception as e:
                print(f"Failed to fetch pull requests overview: {e}")
                return

            cache.save_cache(overview_response, pr_overview_path)
            pull_requests = overview_response.get("values", [])
            for pr in pull_requests:
                if pr.get("draft"):
                    continue

                pr_id = pr.get("id")
                pr_endpoint =  base_endpoint + str(pr_id)

                try:
                    pr_details = req.get(pr_endpoint)
                except Exception as e:
                    print(f"Failed to fetch PR {pr_id}: {e}")
                    continue

                if not cache.has_enough_approvals(pr_details, APPROVAL_THRESHOLD):
                    pr_cache_path = os.path.join(CACHE_DIR, f"{pr_id}.pr.json")
                    cache.save_cache(pr_details, pr_cache_path)




        if self.path == "/server-content":
           return 




def run(server_class=HTTPServer, handler_class=ServerController, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Server running on port {port}")
    httpd.serve_forever()


run()

"""
cache = cm()
data = cache.load_cache(f"{CACHE_DIR}/6882.pr.json")
data.pop("links", None)
if "summary" in data and isinstance(data["summary"], dict):
    html_content = data["summary"].get("html")
    data["summary"] = {"html": html_content} if html_content else {}

if "participants" in data and isinstance(data["participants"], list):
    data["participants"] = [
        {
            "display_name": p.get("user", {}).get("display_name"),
            "approved": p.get("approved"),
            "avatar": p.get("user", {}).get("links", {}).get("avatar", {}).get("href", "")
        }
        for p in data["participants"]
    ]

if "reviewers" in data and isinstance(data["reviewers"], list):
    data["reviewers"] = [
        {
            "display_name": r.get("display_name",{}),
            "avatar": r.get("links", {}).get("avatar", {}).get("href", "") 
        }
        for r in data["reviewers"]
    ]

data.pop("destination", None)
data.pop("source", None)
data.pop("reason", None)
data.pop("type", None)
data.pop("rendered", None)
data.pop("state", None)
data.pop("draft", None)
data.pop("merge_commit", None)
data.pop("closed_by", None)
data.pop("close_source_branch", None)
data["author"] = data["author"]["display_name"]


cache.save_json_cache(data,f"{CACHE_DIR}/Testing.pr.json")


print(json.dumps(data, indent=4))
"""



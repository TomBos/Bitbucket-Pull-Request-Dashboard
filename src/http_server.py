#!/usr/bin/env python

from http.server import BaseHTTPRequestHandler, HTTPServer

from request_controller import requestController as rc
from cache_manager import cacheManager as cm
from dotenv import load_dotenv

import json
import os
import sys
import time
import datetime

APPROVAL_THRESHOLD = 2

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
CACHE_DIR = "cache/"

class ServerController(BaseHTTPRequestHandler):
    def _set_headers(self, status=200, content_type="application/json"):
        self.send_response(status)
        self.send_header("Content-type", content_type)
        self.end_headers()

    def do_GET(self):
        if self.path == "/reload-cache":
            file_path =  f"{CACHE_DIR}/pr_overview.json"
            can_recache = True
            
            if os.path.exists(file_path):
                mod_time = os.path.getmtime(file_path) 
                can_recache = mod_time < (time.time() - 3600) 

            if can_recache:
                cache = cm() 
                cache.clear_old_pull_requests(CACHE_DIR) 
    
                req = rc(config["API_USER"],config["API_KEY"])
                endpoint = req.build_url(["repositories",config["ORGANIZATION"],config["PROJECT"],"pullrequests"])
                res = req.get(endpoint)

                cache.save_json_cache(res,file_path)

                pull_requests = res["values"]
                for pr in pull_requests:
                    endpoint = req.build_url(["repositories",config["ORGANIZATION"],config["PROJECT"],"pullrequests",pr["id"]])
                    res = req.get(endpoint)
                    if not res["draft"]:
                        if not cache.passes_reviews(res, APPROVAL_THRESHOLD): 
                            file_path = f"{CACHE_DIR}/{pr["id"]}.pr.json"
                            cache.save_json_cache(res,file_path)




def run(server_class=HTTPServer, handler_class=ServerController, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Server running on port {port}")
    httpd.serve_forever()


run()
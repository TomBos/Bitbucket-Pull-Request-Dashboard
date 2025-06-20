#!/usr/bin/env python

from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Union, Dict, Any, Optional
from dotenv import load_dotenv
from urllib.parse import unquote

from request_controller import RequestController
from cache_manager import CacheManager

import mimetypes
import json
import os
import sys
import time
import datetime
import glob

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CACHE_DIR = os.path.join(BASE_DIR, "cache")
PUBLIC = os.path.join(BASE_DIR, "public")

APPROVAL_THRESHOLD = 2
CACHE_TTL = 3600

def load_env_vars(*required_keys: str):
    load_dotenv()
    env = {}
    for key in required_keys:
        value = os.getenv(key)
        if not value:
            raise ValueError(f"Missing required environment variable {key}")
        env[key] = value
    return env

config = load_env_vars("API_KEY", "API_USER", "ORGANIZATION", "PROJECT")


class ServerController(BaseHTTPRequestHandler):
    
    def _send_response(self, response_object: Union[str, bytes], encode: bool = True, status: int = 200, content_type: str = "application/json") -> None:
        self.send_response(status)
        self.send_header("Content-type", content_type)
        self.end_headers()
        if encode:
            if isinstance(response_object, str):
                response_object = response_object.encode()
        self.wfile.write(response_object)

    def do_GET(self):
        if self.path in ["/", "/index", "/index.html", "/index.php"]:
            file_path = os.path.join(PUBLIC, "index.html")
            try:
                with open(file_path, "rb") as f:
                    html_content = f.read()
                    return self._send_response(html_content, False, 200, "text/html")
            except FileNotFoundError:
                return self.send_error(404)
        
        if self.path.startswith("/assets/"):
            relative_path = unquote(self.path.lstrip('/'))
            file_path = os.path.join(PUBLIC, relative_path)
            try:
                with open(file_path, "rb") as f:
                    content = f.read()
                    content_type = mimetypes.guess_type(file_path)[0] or "application/octet-stream"
                    return self._send_response(content, content_type=content_type)
            except FileNotFoundError:
                return self.send_error(404)

        return self.send_error(404)

    def do_POST(self):
        if self.path == "/reload-cache":
            pr_overview_path = os.path.join(CACHE_DIR, "pr_overview.json")
            
            try:
                mod_time = os.path.getmtime(pr_overview_path)
                cache_expired = (time.time() - mod_time) > CACHE_TTL
            except FileNotFoundError:
                cache_expired = True

            if not cache_expired:
                response_json = json.dumps({"message": "cache has been updated within last hour"}) + "\n"
                return self._send_response(response_json)
 
            cache = CacheManager()
            cache.clear_pr_cache(CACHE_DIR) 
    
            req = RequestController(config["API_USER"], config["API_KEY"])
            base_endpoint = req.build_url("repositories",config["ORGANIZATION"],config["PROJECT"],"pullrequests")
            
            try:
                overview_response = req.get(base_endpoint)
                if not overview_response:
                    response = json.dumps({"message": "Bitbucket API returned empty object"}) + "\n"
                    return self._send_response(response, 500)
            except Exception as e:
                response = json.dumps({"message": f"{e}"}) + "\n"
                return self._send_response(response, 500)

            cache.save_cache(overview_response, pr_overview_path)
            pull_requests = overview_response.get("values", [])
            for pr in pull_requests:
                if pr.get("draft"):
                    continue

                pr_id = pr.get("id")
                pr_endpoint = req.build_url("repositories",config["ORGANIZATION"],config["PROJECT"],"pullrequests", str(pr_id))
                
                try:
                    pr_details = req.get(pr_endpoint)
                except Exception as e:
                    response = json.dumps({"message": f"Failed to fetch PR {pr_id}: {e}"}) + "\n"
                    return self._send_response(response, 500)

                if not cache.has_enough_approvals(pr_details, APPROVAL_THRESHOLD):
                    parsed_data = cache.trim_cache_object(pr_details)
                    pr_cache_path = os.path.join(CACHE_DIR, f"{pr_id}.pr.json")
                    cache.save_cache(parsed_data, pr_cache_path)


        if self.path == "/tea":
            response = json.dumps({"error": "I'm a teapot 🫖 - I cannot brew coffee"}) + "\n"
            return self._send_response(response)


        if self.path == "/serve-content":
            response_object = []
            for file in glob.glob(os.path.join(CACHE_DIR, "*.json")):
                cache = CacheManager()
                data = cache.load_cache(file)
                response_object.append(data)
            response_json = json.dumps(response_object) + "\n"

            return self._send_response(response_json)

        error_message = json.dumps({"error": "endpoint doesnt exist"}) + "\n"
        return self._send_response(error_message,500)



def run(server_class=HTTPServer, handler_class=ServerController, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Server running on port {port}")
    httpd.serve_forever()


run()
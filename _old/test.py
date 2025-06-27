#!/usr/bin/env python

"""
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

SERVER_HOST = "0.0.0.0"
SERVER_PORT = 8000


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
        if self.path == "/serve-content":
            response_object = []
            for file in glob.glob(os.path.join(CACHE_DIR, "*.pr.json")):
                cache = CacheManager()
                data = cache.load_cache(file)
                response_object.append(data)
            response_json = json.dumps(response_object) + "\n"
            return self._send_response(response_json)

        return self.send_error(404)

    def do_POST(self):
        if self.path == "/reload-cache":
            pr_id = "6899"
            req = RequestController(config["API_USER"], config["API_KEY"])
            pr_endpoint = req.build_url("repositories",config["ORGANIZATION"],config["PROJECT"],"pullrequests", pr_id)
            cache = CacheManager()
            
            try:
                pr_details = req.get(pr_endpoint)
            except Exception as e:
                response = json.dumps({"message": f"Failed to fetch PR {pr_id}: {e}"}) + "\n"
                return self._send_response(response, 500)
                
            if not cache.has_enough_approvals(pr_details, APPROVAL_THRESHOLD):
                pr_cache_path = os.path.join(CACHE_DIR, f"{pr_id}.pr.json")
                cache.save_cache(pr_details, pr_cache_path)

            success_message = json.dumps({"message": "cache successfully reloaded"}) + "\n"
            return self._send_response(success_message)

        error_message = json.dumps({"error": "endpoint doesnt exist"}) + "\n"
        return self._send_response(error_message,500)



def run(server_class=HTTPServer, handler_class=ServerController, host='127.0.0.1', port=8000):
    server_address = (host,port)
    httpd = server_class(server_address, handler_class)
    print(f"Server running on: http://{host}:{port}")
    httpd.serve_forever()


run(host=SERVER_HOST, port=SERVER_PORT)

"""


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

cache = CacheManager()
pr_details = cache.load_cache(os.path.join(CACHE_DIR, "6899.pr.json"))
obj = cache.trim_cache_object(pr_details)
print(json.dumps(obj, indent=4))
sys.exit(0)
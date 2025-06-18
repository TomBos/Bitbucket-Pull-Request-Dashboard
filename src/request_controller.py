#!/usr/bin/env python

import requests
import json

class RequestController:
    def __init__(self, username, api_key):
        self.username = username
        self.api_key = api_key
        pass

    def build_url(self, params = []):
        endpoint = "https://api.bitbucket.org/2.0" 
        for param in params:
            endpoint += f"/{param}"
        return endpoint


    def get(self, endpoint):
        try: 
            response = requests.get(
                endpoint,
                auth=(self.username, self.api_key),
                headers={"Accept": "application/json"},
                params={"pagelen": 50}
            )
        
            response.raise_for_status()

        except requests.exceptions.RequestException as e:
            print(f"API request failed: {e}")
            return {}
        except (ValueError, IOError, json.JSONDecodeError) as e:
            print(f"Processing error: {e}")
            return {}        

        return response.json()



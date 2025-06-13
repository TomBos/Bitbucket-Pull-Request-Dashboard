#!/usr/bin/env python

import requests
import json

class requestController:
    def __init__(self, username, api_key):
        self.username = username
        self.api_key = api_key
        pass


    def call_endpoint(self, endpoint):
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



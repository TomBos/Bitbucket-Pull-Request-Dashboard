#!/usr/bin/env python

import requests
import json
import typing

class RequestController:
    def __init__(self, username, api_key):
        self.username = username
        self.api_key = api_key
        pass

    def build_url(self, *params: str) -> str:
        base = "https://api.bitbucket.org/2.0"
        parts = [base]

        for param in params:
            clean_part = param.strip("/")
            parts.append(clean_part)

        url = "/".join(parts)
        return url


    def get(self, endpoint: str) -> dict:
        try:
            response = requests.get(
                endpoint,
                auth=(self.username, self.api_key),
                headers={"Accept": "application/json"},
                params={"pagelen": 50}
            )
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            print(f"API request failed: {e}")
        except (ValueError, IOError, json.JSONDecodeError) as e:
            print(f"Processing error: {e}")

        return {}



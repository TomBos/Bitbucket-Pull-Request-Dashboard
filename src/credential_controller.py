#!/usr/bin/env python

import os
from dotenv import load_dotenv

class credentialController:
    def __init__(self):
        load_dotenv() 
        self.API_KEY = os.getenv("API_KEY")
        self.USER = os.getenv("API_USER") 
        self.ORGANIZATION = os.getenv("ORGANIZATION")
        self.PROJECT = os.getenv("PROJECT") 
        pass

    def get_var_value(self, key):
        return getattr(self, key, None)




#!/usr/bin/env python

import os
import json

class cacheManager():
    def __init__(self):
        pass

    def save_json_cache(self, data, file_path):
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        



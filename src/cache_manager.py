#!/usr/bin/env python

import os
import json
import datetime
import time
class cacheManager():
    def __init__(self):
        pass

    def save_json_cache(self, data):
        file_path =  "pr_overview.json" 
        mod_time = os.path.getmtime(file_path) 
        can_recache = mod_time < (time.time() - 3600) 
        if can_recache:
            with open(file_path, 'w') as f:
                json.dump(data, f)
            return True
        else:
            return False

        



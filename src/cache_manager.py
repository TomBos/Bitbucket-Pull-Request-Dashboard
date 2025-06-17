#!/usr/bin/env python

import os
import json
import glob

class cacheManager():
    def __init__(self):
        pass

    def save_json_cache(self, data, file_path):
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def remove_cached_file(self, file_path):
        if os.path.exists(file_path): 
            os.remove(file_path)

    def load_cache(self, file_path):
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                return json.load(f)

    def clear_old_pull_requests(self, dir_path):
        if os.path.isdir(dir_path):
            for file in glob.glob(os.path.join(dir_path, "*.json")):
                self.remove_cached_file(file)

    def passes_reviews(self, pr_data, approval_threshold):
        author = pr_data["author"]["display_name"]
        participants = pr_data["participants"]
        approved_count = 0

        for participant in participants:
            if participant["user"]["display_name"] != author:
                if participant["approved"]:
                    approved_count += 1

        if approved_count >= approval_threshold:
            return 1
        else:
            return 0


    # Delete Later ?
    """
    def test(self):
        for file in glob.glob(os.path.join("cache/", "*.pr.json")):
            pr_data = self.load_cache(file)
            author = pr_data["author"]["display_name"]
            participants = pr_data["participants"]
            approved_count = 0

            for participant in participants:
                if participant["user"]["display_name"] != author:
                    if participant["approved"]:
                        approved_count += 1

            print(f"PR: {pr_data["title"]} has {approved_count} approves")
    """




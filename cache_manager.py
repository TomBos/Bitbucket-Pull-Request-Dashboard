#!/usr/bin/env python

import os
import glob
import json
from typing import Any, Dict, Optional

class CacheManager:
    def save_cache(self, data: Any, file_path: str) -> None:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def delete_cache(self, file_path: str) -> None:
        try:
            os.remove(file_path)
        except FileNotFoundError:
            pass

    def load_cache(self, file_path: str) -> Optional[Any]:
        if os.path.isfile(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None

    def clear_pr_cache(self, dir_path: str) -> None:
        if os.path.isdir(dir_path):
            for file in glob.glob(os.path.join(dir_path, "*.json")):
                self.delete_cache(file)

    def has_enough_approvals(self, pr_data: dict, approval_threshold: int) -> bool:
        author = pr_data["author"]["display_name"]
        participants = pr_data.get("participants", [])
        approved_count = sum(
            1 for p in participants 
            if p["user"]["display_name"] != author and p.get("approved")
        )
        return approved_count >= approval_threshold


    def trim_cache_object(self, data: Dict[str, Any]) -> Dict[str, Any]:
        if isinstance(data.get("summary"), dict):
            html_content = data["summary"].get("html")
            data["summary"] = {"html": html_content} if html_content else {}

        if isinstance(data.get("participants"), list):
            data["participants"] = [
                {
                    "display_name": p.get("user", {}).get("display_name"),
                    "approved": p.get("approved"),
                    "avatar": p.get("user", {}).get("links", {}).get("avatar", {}).get("href", "")
                }
                for p in data["participants"]
            ]

        if isinstance(data.get("reviewers"), list):
            data["reviewers"] = [
                {
                    "display_name": r.get("display_name", {}),
                    "avatar": r.get("links", {}).get("avatar", {}).get("href", "")
                }
                for r in data["reviewers"]
            ]

        for key in [
            "destination", "source", "reason", "type", "rendered", "links",
            "state", "draft", "merge_commit", "closed_by", "close_source_branch"
        ]: data.pop(key, None)

        data["author"] = data["author"]["display_name"]
        return data






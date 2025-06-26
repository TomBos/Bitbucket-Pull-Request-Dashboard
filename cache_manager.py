#!/usr/bin/env python

import os
import glob
import json
from typing import Any, Dict, List, Optional

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
        keys_to_remove = [
            "destination", "source", "reason", "type", "rendered", "links",
            "state", "draft", "merge_commit", "closed_by", "close_source_branch"
        ]

        for key in keys_to_remove: 
            data.pop(key, None)

        summary = self.normalize_summary(data["summary"])
        participants = self.normalize_participants(data["participants"]) 
        
        """
        reviewers = self.normalize_reviewers(data)
        """
        
        author = data.get("author")
        if isinstance(author, dict):
            display_name = author.get("display_name")
        else:
            display_name = author

        """
        reviewers_dict = {r["display_name"]: r for r in reviewers if r["display_name"]}
        
        filtered_participants = []
        for p in participants:
            name = p["display_name"]
            if name in reviewers_dict:
                reviewers_dict[name]["approved"] = p.get("approved", False)
            else:
                filtered_participants.append(p)
        """

        # data["participants"] = participants
        # data["reviewers"] = reviewers


        data["summary"] = summary
        data["participants"] = participants

        return data

    def normalize_participants(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        participants = []
        for p in data:
            user = p.get("user", {})
            display_name = user.get("display_name")
            approved = p.get("approved")
            avatar = ""

            links = user.get("links")
            if links:
                avatar_dict = links.get("avatar")
                if avatar_dict:
                    avatar = avatar_dict.get("href", "")

            if display_name:
                participants.append({
                    "display_name": display_name,
                    "approved": approved,
                    "avatar": avatar,
                })

        return participants

    def normalize_reviewers(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        reviewers = []
        for r in data.get("reviewers", []):
            display_name = r.get("display_name")
            avatar = ""

            links = r.get("links")
            if links:
                avatar_dict = links.get("avatar")
                if avatar_dict:
                    avatar = avatar_dict.get("href", "")

            if display_name:
                reviewers.append({
                    "display_name": display_name,
                    "avatar": avatar,
                })

        return reviewers

    def normalize_summary(self, data: dict) -> dict:
        if isinstance(data, dict):
            return data.get("html")
        return {}





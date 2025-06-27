#!/usr/bin/env python

import os
import glob
import json
from typing import Any, Dict, List, Tuple, Optional

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
        author = self.normalize_author(data["author"], participants)
        reviewers = self.normalize_reviewers(data["reviewers"])
        [filtred_participants, filtred_reviewers] = self.deduplicate_participants(participants, reviewers)

        data["author"] = author
        data["summary"] = summary
        data["participants"] = filtred_participants
        data["reviewers"] = filtred_reviewers

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
        for r in data:
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


    def normalize_summary(self, data: Dict[str, Any]) -> dict:
        if isinstance(data, dict):
            return data.get("html")
        return {}


    def normalize_author(self, author_dict: Dict[str, Any], participant_dict: List[Dict[str, Any]]) -> dict:
        author_name = author_dict.get("display_name")
        for participant in participant_dict:
            if participant.get("display_name") == author_name:
                return participant
        raise ValueError(f"Author '{author_name}' not found in participants")


    
    def deduplicate_participants(self, participant_list: List[Dict[str, Any]], reviewers_list: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        deduped_participants = []
        deduped_reviewers = []

        for p in participant_list:
            found = False
            for r in reviewers_list:
                if r.get("display_name") == p.get("display_name"):
                    found = True
                    break

            if found:
                already_in_reviewers = False
                for r in deduped_reviewers:
                    if r.get("display_name") == p.get("display_name"):
                        already_in_reviewers = True
                        break
                if not already_in_reviewers:
                    deduped_reviewers.append(p)
            else:
                deduped_participants.append(p)

        return deduped_participants, deduped_reviewers



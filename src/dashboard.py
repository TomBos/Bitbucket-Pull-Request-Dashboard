#!/usr/bin/env python

"""
def load_pull_requests():
    cache_file = "pullrequests.json"
    
    # Check if cache file exists
    if not os.path.exists(cache_file):
        print("Cache file not found, fetching pull requests...")
        if cache_master_file() != 1:
            raise RuntimeError("Failed to fetch pull requests")
    
    # Load and return the cached data
    try:
        with open(cache_file, "r") as f:
            # print("Loading data from cache...")
            return json.load(f)
    except (IOError, json.JSONDecodeError) as e:
        print(f"Error loading cache: {e}")
        # Attempt to refresh cache if corrupted
        print("Attempting to refresh cache...")
        if cache_master_file() != 1:
            raise RuntimeError("Failed to refresh pull requests cache")
        with open(cache_file, "r") as f:
            return json.load(f)
        
def get_single_pull_request(pullrequest_id):
    if not os.path.exists(f"{pullrequest_id}.pr.json"):
        print(f"Fetching pr {pullrequest_id} ...")
    
    
    return
"""

# Load pull requests data
# pull_requests_data = load_pull_requests()
# print(f"Successfully loaded {len(pull_requests_data)} pull requests from cache")
# print(f"Found {len(pull_requests_data)} pull requests:")
# y = json.dumps(pull_requests_data[1])
# print(y)

# List of what i need:
# id
# title
# state
# draft
# author
# updated_on
# created_on


# using ID's then fetch each PR into file if it is not already cached and it havent been 1h since last upload
# for pr in pull_requests_data:
#       get_single_pull_request(pr["id"])



sys.exit(1)

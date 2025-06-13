import requests
import json
import os
from typing import Any, Dict, List, Optional
from datetime import datetime, timedelta, timezone

BASE_URL = "https://api.spacexdata.com/v4"
CACHE_DIR = ".cache"
CACHE_TTL = timedelta(hours=6)

class SpaceXAPIClient:
    def __init__(self):
        os.makedirs(CACHE_DIR, exist_ok=True)

    def _get(self, endpoint: str) -> Any:
        cache_file = os.path.join(CACHE_DIR, endpoint.strip("/").replace("/", "_") + ".json")
        now = datetime.now(timezone.utc)
        # Try to load from cache
        if os.path.exists(cache_file):
            try:
                with open(cache_file, "r") as f:
                    data = json.load(f)
                ts = datetime.fromtimestamp(os.path.getmtime(cache_file), timezone.utc)
                if now - ts < CACHE_TTL:
                    return data
            except Exception:
                pass  # Ignore cache errors, fetch fresh
        # Fetch from API
        url = BASE_URL + endpoint
        try:
            resp = requests.get(url, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            with open(cache_file, "w") as f:
                json.dump(data, f)
            return data
        except Exception as e:
            # On error, try to return stale cache if available
            if os.path.exists(cache_file):
                try:
                    with open(cache_file, "r") as f:
                        return json.load(f)
                except Exception:
                    pass
            raise RuntimeError(f"Failed to fetch {endpoint}: {e}")

    def get_launches(self) -> List[Dict[str, Any]]:
        return self._get("/launches")

    def get_rockets(self) -> List[Dict[str, Any]]:
        return self._get("/rockets")

    def get_launchpads(self) -> List[Dict[str, Any]]:
        return self._get("/launchpads") 
from typing import List, Optional
from datetime import datetime
from .models import Launch

def parse_date(date_str: str) -> datetime:
    return datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%fZ")

def filter_launches(
    launches: List[Launch],
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    rocket_ids: Optional[List[str]] = None,
    launchpad_ids: Optional[List[str]] = None,
    success: Optional[bool] = None,
) -> List[Launch]:
    result = []
    for launch in launches:
        dt = parse_date(launch.date_utc)
        if start_date and dt < start_date:
            continue
        if end_date and dt > end_date:
            continue
        if rocket_ids and launch.rocket not in rocket_ids:
            continue
        if launchpad_ids and launch.launchpad not in launchpad_ids:
            continue
        if success is not None and launch.success != success:
            continue
        result.append(launch)
    return result 
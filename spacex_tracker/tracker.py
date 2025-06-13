from typing import List, Dict
from collections import defaultdict, Counter
from .models import Launch, Rocket, Launchpad
from .utils import parse_date
from datetime import datetime

def success_rates_by_rocket(launches: List[Launch], rockets: List[Rocket]) -> Dict[str, float]:
    rocket_success = defaultdict(lambda: [0, 0])  # [successes, total]
    for launch in launches:
        if launch.success is not None:
            rocket_success[launch.rocket][1] += 1
            if launch.success:
                rocket_success[launch.rocket][0] += 1
    rates = {}
    for rocket in rockets:
        successes, total = rocket_success[rocket.id]
        rates[rocket.name] = successes / total if total else 0.0
    return rates

def launches_per_site(launches: List[Launch], launchpads: List[Launchpad]) -> Dict[str, int]:
    site_counts = Counter(launch.launchpad for launch in launches)
    site_names = {pad.id: pad.name for pad in launchpads}
    return {site_names.get(site_id, site_id): count for site_id, count in site_counts.items()}

def launch_frequency(launches: List[Launch]) -> Dict[str, Dict[str, int]]:
    monthly = Counter()
    yearly = Counter()
    for launch in launches:
        dt = parse_date(launch.date_utc)
        monthly[dt.strftime('%Y-%m')] += 1
        yearly[dt.strftime('%Y')] += 1
    return {"monthly": dict(monthly), "yearly": dict(yearly)} 
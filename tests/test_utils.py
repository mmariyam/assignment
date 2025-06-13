from spacex_tracker.utils import parse_date, filter_launches
from spacex_tracker.models import Launch
from datetime import datetime

def test_parse_date():
    date_str = "2020-01-01T12:34:56.789Z"
    dt = parse_date(date_str)
    assert dt.year == 2020 and dt.month == 1 and dt.day == 1

def test_filter_launches():
    launches = [
        Launch(id="1", name="A", date_utc="2020-01-01T00:00:00.000Z", rocket="r1", launchpad="lp1", success=True),
        Launch(id="2", name="B", date_utc="2021-01-01T00:00:00.000Z", rocket="r2", launchpad="lp2", success=False),
    ]
    start = datetime(2020, 6, 1)
    filtered = filter_launches(launches, start_date=start)
    assert len(filtered) == 1
    assert filtered[0].id == "2" 
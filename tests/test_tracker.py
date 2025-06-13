from spacex_tracker.tracker import success_rates_by_rocket, launches_per_site, launch_frequency
from spacex_tracker.models import Launch, Rocket, Launchpad

def test_success_rates_by_rocket():
    launches = [
        Launch(id="1", name="A", date_utc="2020-01-01T00:00:00.000Z", rocket="r1", launchpad="lp1", success=True),
        Launch(id="2", name="B", date_utc="2020-01-02T00:00:00.000Z", rocket="r1", launchpad="lp1", success=False),
        Launch(id="3", name="C", date_utc="2020-01-03T00:00:00.000Z", rocket="r2", launchpad="lp2", success=True),
    ]
    rockets = [Rocket(id="r1", name="Falcon 9"), Rocket(id="r2", name="Falcon Heavy")]
    rates = success_rates_by_rocket(launches, rockets)
    assert rates["Falcon 9"] == 0.5
    assert rates["Falcon Heavy"] == 1.0

def test_launches_per_site():
    launches = [
        Launch(id="1", name="A", date_utc="2020-01-01T00:00:00.000Z", rocket="r1", launchpad="lp1", success=True),
        Launch(id="2", name="B", date_utc="2020-01-02T00:00:00.000Z", rocket="r1", launchpad="lp1", success=False),
        Launch(id="3", name="C", date_utc="2020-01-03T00:00:00.000Z", rocket="r2", launchpad="lp2", success=True),
    ]
    launchpads = [Launchpad(id="lp1", name="Pad 1", locality=None), Launchpad(id="lp2", name="Pad 2", locality=None)]
    counts = launches_per_site(launches, launchpads)
    assert counts["Pad 1"] == 2
    assert counts["Pad 2"] == 1

def test_launch_frequency():
    launches = [
        Launch(id="1", name="A", date_utc="2020-01-01T00:00:00.000Z", rocket="r1", launchpad="lp1", success=True),
        Launch(id="2", name="B", date_utc="2020-01-15T00:00:00.000Z", rocket="r1", launchpad="lp1", success=False),
        Launch(id="3", name="C", date_utc="2021-01-03T00:00:00.000Z", rocket="r2", launchpad="lp2", success=True),
    ]
    freq = launch_frequency(launches)
    assert freq["monthly"]["2020-01"] == 2
    assert freq["monthly"]["2021-01"] == 1
    assert freq["yearly"]["2020"] == 2
    assert freq["yearly"]["2021"] == 1 
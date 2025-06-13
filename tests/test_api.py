import pytest
from unittest.mock import patch, MagicMock
import tempfile
from spacex_tracker.api import SpaceXAPIClient

@patch('spacex_tracker.api.CACHE_DIR', tempfile.mkdtemp())
@patch('requests.get')
def test_get_launches(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = [{"id": "1", "name": "Test Launch", "date_utc": "2020-01-01T00:00:00.000Z", "rocket": "r1", "launchpad": "lp1", "success": True}]
    client = SpaceXAPIClient()
    launches = client.get_launches()
    assert isinstance(launches, list)
    assert launches[0]["name"] == "Test Launch" 
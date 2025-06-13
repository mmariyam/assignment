# SpaceX Launch Tracker

A Python application to track and analyze SpaceX launches using the public SpaceX API v4.

## Features
- Fetch and cache SpaceX launch, rocket, and launchpad data
- List and filter launches (by date, rocket, site, success)
- Generate statistics (success rates, launches per site, frequency)
- Command-line interface
- Unit tested and type hinted

## Setup
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage
```bash
python -m spacex_tracker.cli
```

## Testing
```bash
pytest
```

## API Reference
- https://api.spacexdata.com/v4/launches
- https://api.spacexdata.com/v4/rockets
- https://api.spacexdata.com/v4/launchpads 
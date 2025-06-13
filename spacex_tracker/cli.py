import argparse
from rich.console import Console
from rich.table import Table
from datetime import datetime
from .api import SpaceXAPIClient
from .models import Launch, Rocket, Launchpad
from .utils import filter_launches, parse_date
from .tracker import success_rates_by_rocket, launches_per_site, launch_frequency

def main():
    parser = argparse.ArgumentParser(description="SpaceX Launch Tracker")
    parser.add_argument('--list', action='store_true', help='List launches')
    parser.add_argument('--stats', action='store_true', help='Show statistics')
    parser.add_argument('--start', type=str, help='Start date (YYYY-MM-DD)')
    parser.add_argument('--end', type=str, help='End date (YYYY-MM-DD)')
    parser.add_argument('--rocket', type=str, help='Rocket name')
    parser.add_argument('--site', type=str, help='Launch site name')
    parser.add_argument('--success', type=str, choices=['true','false'], help='Success only (true/false)')
    parser.add_argument('--export', type=str, help='Export to CSV file')
    args = parser.parse_args()

    client = SpaceXAPIClient()
    launches_raw = client.get_launches()
    rockets_raw = client.get_rockets()
    launchpads_raw = client.get_launchpads()

    rockets = [Rocket.from_api(r) for r in rockets_raw]
    launchpads = [Launchpad.from_api(p) for p in launchpads_raw]
    launches = [Launch.from_api(l) for l in launches_raw]

    # Filtering
    start_date = parse_date(args.start+"T00:00:00.000Z") if args.start else None
    end_date = parse_date(args.end+"T23:59:59.999Z") if args.end else None
    rocket_ids = [r.id for r in rockets if r.name.lower() == args.rocket.lower()] if args.rocket else None
    launchpad_ids = [p.id for p in launchpads if p.name.lower() == args.site.lower()] if args.site else None
    success = {'true': True, 'false': False}.get(args.success) if args.success else None
    filtered = filter_launches(launches, start_date, end_date, rocket_ids, launchpad_ids, success)

    console = Console()

    if args.list:
        table = Table(title="SpaceX Launches")
        table.add_column("Date")
        table.add_column("Name")
        table.add_column("Rocket")
        table.add_column("Site")
        table.add_column("Success")
        for l in filtered:
            rocket_name = next((r.name for r in rockets if r.id == l.rocket), l.rocket)
            site_name = next((p.name for p in launchpads if p.id == l.launchpad), l.launchpad)
            table.add_row(l.date_utc[:10], l.name, rocket_name, site_name, str(l.success))
        console.print(table)

    if args.stats:
        console.print("[bold]Success Rates by Rocket:[/bold]")
        rates = success_rates_by_rocket(filtered, rockets)
        for rocket, rate in rates.items():
            console.print(f"{rocket}: {rate:.2%}")
        console.print("\n[bold]Launches per Site:[/bold]")
        site_counts = launches_per_site(filtered, launchpads)
        for site, count in site_counts.items():
            console.print(f"{site}: {count}")
        console.print("\n[bold]Launch Frequency:[/bold]")
        freq = launch_frequency(filtered)
        console.print("Monthly:", freq['monthly'])
        console.print("Yearly:", freq['yearly'])
    
    if args.export:
        import pandas as pd
        data = []
        for l in filtered:
            rocket_name = next((r.name for r in rockets if r.id == l.rocket), l.rocket)
            site_name = next((p.name for p in launchpads if p.id == l.launchpad), l.launchpad)
            data.append({
                'Date': l.date_utc[:10],
                'Name': l.name,
                'Rocket': rocket_name,
                'Site': site_name,
                'Success': l.success
            })
        df = pd.DataFrame(data)
        df.to_csv(args.export, index=False)
        console.print(f"[green]Exported {len(data)} launches to {args.export}[/green]")

if __name__ == "__main__":
    main() 
import requests
from bs4 import BeautifulSoup
import argparse
import json
from datetime import datetime, timedelta
from rich.console import Console

console = Console()

BASE_URL = "https://services.ecourts.gov.in/ecourtindia_v6/"

def fetch_case_details(cnr=None, case_type=None, case_no=None, year=None):
    try:
        session = requests.Session()
        if cnr:
            url = f"{BASE_URL}?p=casestatus&cnr={cnr}"
        else:
            url = f"{BASE_URL}?p=casestatus&ctype={case_type}&cno={case_no}&cyear={year}"

        response = session.get(url, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        return soup
    except Exception as e:
        console.print(f"[red]Error fetching case details:[/red] {e}")
        return None

def check_listing(soup, date_to_check):
    listings = soup.find_all("tr")
    results = []

    for row in listings:
        if date_to_check in row.text:
            serial = row.find("td", {"class": "srno"})
            court = row.find("td", {"class": "court_name"})
            results.append({
                "serial": serial.text.strip() if serial else "N/A",
                "court_name": court.text.strip() if court else "N/A"
            })

    return results

def save_json(data, filename):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    console.print(f"[green]Saved results to {filename}[/green]")

def main():
    parser = argparse.ArgumentParser(description="eCourts Case Scraper")
    parser.add_argument("--cnr", help="Enter CNR number")
    parser.add_argument("--case_type", help="Enter case type (e.g., CR, WP)")
    parser.add_argument("--case_no", help="Enter case number")
    parser.add_argument("--year", help="Enter case year")
    parser.add_argument("--today", action="store_true", help="Check today's listing")
    parser.add_argument("--tomorrow", action="store_true", help="Check tomorrow's listing")
    parser.add_argument("--causelist", action="store_true", help="Download today's cause list")

    args = parser.parse_args()

    date_today = datetime.now().strftime("%d-%m-%Y")
    date_tomorrow = (datetime.now() + timedelta(days=1)).strftime("%d-%m-%Y")

    soup = fetch_case_details(args.cnr, args.case_type, args.case_no, args.year)
    if not soup:
        return

    if args.today:
        results = check_listing(soup, date_today)
        save_json(results, "today_listing.json")
    elif args.tomorrow:
        results = check_listing(soup, date_tomorrow)
        save_json(results, "tomorrow_listing.json")

    elif args.causelist:
        console.print("[yellow]Downloading today's cause list...[/yellow]")
        # TODO: Add function to fetch cause list PDF

if __name__ == "__main__":
    main()

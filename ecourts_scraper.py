import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from rich.console import Console
from time import sleep

console = Console()

BASE_URL = "https://services.ecourts.gov.in/ecourtindia_v6/"
OUTPUT_DIR = "cause_lists"

def get_states():
    """Fetch available states from eCourts"""
    url = BASE_URL + "?p=caselist/index/"
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, "html.parser")
    states = {opt.text.strip(): opt["value"] for opt in soup.select("#sess_state_code option") if opt["value"]}
    return states

def get_districts(state_code):
    """Fetch district courts for a given state"""
    url = f"{BASE_URL}?p=caselist/getDistrict&state_code={state_code}"
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, "html.parser")
    return {opt.text.strip(): opt["value"] for opt in soup.find_all("option") if opt["value"]}

def download_cause_list(state_name, dist_name, dist_code, date_str):
    """Download the cause list PDF for a given district"""
    try:
        url = f"{BASE_URL}?p=caselist/getCauseList&dist_code={dist_code}&date={date_str}"
        r = requests.get(url, timeout=15)
        if r.headers.get("content-type", "").lower().startswith("application/pdf"):
            folder = os.path.join(OUTPUT_DIR, state_name, dist_name)
            os.makedirs(folder, exist_ok=True)
            file_path = os.path.join(folder, f"{date_str}.pdf")
            with open(file_path, "wb") as f:
                f.write(r.content)
            console.print(f"[green]Saved {file_path}[/green]")
        else:
            console.print(f"[yellow]No cause list found for {dist_name} ({state_name})[/yellow]")
    except Exception as e:
        console.print(f"[red]Error downloading for {dist_name}: {e}[/red]")

def main():
    today_str = datetime.now().strftime("%d-%m-%Y")
    console.print(f"[cyan]Fetching cause lists for {today_str}...[/cyan]")

    states = get_states()
    for state_name, state_code in states.items():
        console.print(f"\n[bold blue]State:[/bold blue] {state_name}")
        districts = get_districts(state_code)

        for dist_name, dist_code in districts.items():
            download_cause_list(state_name, dist_name, dist_code, today_str)
            sleep(0.5)  # be gentle to the server

    console.print("\n[bold green]All available cause lists downloaded![/bold green]")

if __name__ == "__main__":
    main()

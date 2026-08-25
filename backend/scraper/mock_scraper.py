import argparse
import os
import re
from datetime import datetime, timezone

import requests

API_URL = os.getenv("API_URL", "http://localhost:8000/api/delays")

SAMPLE_PAYLOADS = [
    "Western UP: signal issue between Dadar - Bandra; trains delayed by 18 minutes. Major disruption.",
    "Central DN: technical snag affecting Dadar - Kurla stretch; 27 min delay. Severe disruption.",
    "Harbour UP: points failure between Wadala Road - Kurla causing 9 minutes delay. Minor disruption.",
    "Western DN: overhead wire fluctuation affecting Andheri - Borivali services by 12 minutes. Major disruption.",
    "Central UP: track congestion between Ghatkopar - Vikhroli; trains running 6 minutes late. Minor disruption.",
    "Harbour DN: heavy rainfall impact between Panvel - Vashi; services delayed by 22 minutes. Severe disruption.",
]


def parse_update(text: str) -> dict:
    match = re.search(
        r"(?P<line>Western|Central|Harbour) (?P<direction>UP|DN): .*?"
        r"(?:between |affecting )(?P<stretch>[A-Za-z ]+ - [A-Za-z ]+).*?"
        r"(?P<delay>\d+) ?(?:min|minutes)",
        text,
        re.IGNORECASE,
    )
    if not match:
        raise ValueError(f"Could not parse railway update: {text}")

    delay = int(match.group("delay"))
    priority = "Severe" if delay >= 20 else "Major" if delay >= 10 else "Minor"
    stretch = match.group("stretch").strip()
    return {
        "line": match.group("line").title(),
        "direction": match.group("direction").upper(),
        "station": stretch.split(" - ")[0].strip(),
        "affected_stretch": stretch,
        "delay_minutes": delay,
        "priority": priority,
        "announcement_text": text,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }


def post_mock_incidents(count: int) -> None:
    for index in range(count):
        incident = parse_update(SAMPLE_PAYLOADS[index % len(SAMPLE_PAYLOADS)])
        response = requests.post(API_URL, json=incident, timeout=10)
        if response.ok:
            created = response.json()
            print(
                f"[{datetime.now().isoformat(timespec='seconds')}] created "
                f"#{created['id']} {created['line']} {created['direction']} "
                f"{created['delay_minutes']}m at {created['station']}"
            )
        else:
            print(
                f"Failed to post incident ({response.status_code}): {response.text}",
            )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate and post mock Mumbai local delay announcements.",
    )
    parser.add_argument("--count", type=int, default=5, help="Number of incidents to post")
    args = parser.parse_args()
    post_mock_incidents(args.count)


if __name__ == "__main__":
    main()

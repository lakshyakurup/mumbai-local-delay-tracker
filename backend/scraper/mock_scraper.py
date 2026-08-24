import argparse
import random
from datetime import datetime

import requests

API_URL = "http://localhost:8000/api/delays"

LINES = ["Central", "Western", "Harbour"]
DIRECTIONS = ["UP", "DN"]

LINE_SEGMENTS = {
    "Central": [
        ("Dadar", "Kurla"),
        ("Kurla", "Thane"),
        ("Ghatkopar", "Vikhroli"),
        ("Byculla", "Dadar"),
    ],
    "Western": [
        ("Andheri", "Bandra"),
        ("Borivali", "Andheri"),
        ("Dadar", "Mumbai Central"),
        ("Virar", "Nalasopara"),
    ],
    "Harbour": [
        ("Wadala Road", "Kurla"),
        ("Panvel", "Vashi"),
        ("Govandi", "Mankhurd"),
        ("Chembur", "Tilak Nagar"),
    ],
}

REASONS = [
    "signal issue",
    "technical snag",
    "overhead wire fluctuation",
    "track congestion",
    "points failure",
    "heavy rainfall impact",
]


def generate_mock_incident() -> dict:
    line = random.choice(LINES)
    direction = random.choice(DIRECTIONS)
    start_station, end_station = random.choice(LINE_SEGMENTS[line])
    delay_minutes = random.randint(3, 35)
    reason = random.choice(REASONS)

    station = random.choice([start_station, end_station])
    announcement_text = (
        f"{reason.capitalize()} between {start_station} and {end_station} causing "
        f"{delay_minutes} min delay on {line} Line {direction}."
    )

    return {
        "line": line,
        "direction": direction,
        "station": station,
        "delay_minutes": delay_minutes,
        "announcement_text": announcement_text,
    }


def post_mock_incidents(count: int) -> None:
    for _ in range(count):
        incident = generate_mock_incident()
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

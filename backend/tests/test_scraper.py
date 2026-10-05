from backend.services.scraper import parse_status_payload, parse_status_text, severity_for_delay


def test_parse_payload_filters_unknown_lines_and_invalid_delays():
    updates = parse_status_payload({"updates": [{"line": "Central", "station": "Dadar", "delay_minutes": 12}, {"line": "metro", "station": "X", "delay_minutes": 3}, {"line": "Western", "station": "", "delay_minutes": 4}]})
    assert len(updates) == 1
    assert updates[0].line == "central"
    assert updates[0].delay_minutes == 12


def test_parse_text_and_severity():
    updates = parse_status_text("Western - Bandra 14 min")
    assert updates[0].station == "Bandra"
    assert severity_for_delay(0) == "normal"
    assert severity_for_delay(25) == "severe"

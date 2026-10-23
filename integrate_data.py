#!/usr/bin/env python3
"""Integrate nursery CSV, JSON, and XML sources into a normalized CSV."""
import csv, json, xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "source-data"
OUT = ROOT / "integrated-data" / "integrated_dataset.csv"
FIELDS = [
    "timestamp", "event_type", "room_number", "person_id", "person_type",
    "access_status", "room_temperature_f", "door_status", "heart_rate_bpm",
    "breathing_rate_per_min", "patient_temperature_f", "source_file",
    "source_record_number", "data_quality_notes"
]

def main():
    records = []
    with (SRC / "batch101.csv").open(newline="", encoding="utf-8-sig") as f:
        for i, r in enumerate(csv.DictReader(f), 1):
            room = (r.get("Room") or "").strip()
            notes = ""
            if room.startswith("103") and len(room) == 5:
                notes = f"Room normalized from source code {room} to {room[2:]} by removing leading '10' to align with room sensor identifiers."
                room = room[2:]
            role = (r.get("PersonType") or "").strip()
            if role == "Patien":
                role = "Patient"
                notes = (notes + " " if notes else "") + "PersonType corrected from 'Patien' to 'Patient' (obvious truncated label)."
            dt = datetime.strptime(f"{r['Date']} {r['Time']}", "%m/%d/%Y %I:%M %p")
            records.append({
                "timestamp": dt.strftime("%Y-%m-%d %H:%M:%S"), "event_type": "access_event",
                "room_number": room, "person_id": (r.get("PersonID") or "").strip(),
                "person_type": role, "access_status": (r.get("Access") or "").strip(),
                "room_temperature_f": "", "door_status": "", "heart_rate_bpm": "",
                "breathing_rate_per_min": "", "patient_temperature_f": "",
                "source_file": "batch101.csv", "source_record_number": i, "data_quality_notes": notes
            })
    with (SRC / "stream101.json").open(encoding="utf-8") as f:
        readings = json.load(f).get("Readings", [])
    for i, r in enumerate(readings, 1):
        dt = datetime.strptime(r["dateTime"], "%m/%d/%Y %I:%M %p")
        records.append({
            "timestamp": dt.strftime("%Y-%m-%d %H:%M:%S"), "event_type": "room_environment",
            "room_number": str(r.get("roomNumber", "")), "person_id": "", "person_type": "",
            "access_status": "", "room_temperature_f": r.get("roomTempF", ""),
            "door_status": r.get("doorStatus", ""), "heart_rate_bpm": "",
            "breathing_rate_per_min": "", "patient_temperature_f": "",
            "source_file": "stream101.json", "source_record_number": i, "data_quality_notes": ""
        })
    root = ET.parse(SRC / "feed101.xml").getroot()
    for i, r in enumerate(root.findall(".//reading"), 1):
        dt = datetime.strptime(f"{r.findtext('date')} {r.findtext('time')}", "%Y-%m-%d %H:%M")
        records.append({
            "timestamp": dt.strftime("%Y-%m-%d %H:%M:%S"), "event_type": "patient_vitals",
            "room_number": "", "person_id": (r.findtext("patientId") or "").strip(),
            "person_type": "Patient", "access_status": "", "room_temperature_f": "",
            "door_status": "", "heart_rate_bpm": (r.findtext("heartRate") or "").strip(),
            "breathing_rate_per_min": (r.findtext("breathingRate") or "").strip(),
            "patient_temperature_f": (r.findtext("temperature") or "").strip(),
            "source_file": "feed101.xml", "source_record_number": i,
            "data_quality_notes": "Patient vital-sign record; room number not provided in XML source."
        })
    records.sort(key=lambda r: (r["timestamp"], r["event_type"], r["source_file"], int(r["source_record_number"])))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(records)
    print(f"Wrote {len(records)} records to {OUT}")

if __name__ == "__main__":
    main()

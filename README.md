# IoT Data Integration: Nursery Scenario

## Project overview
This repository documents and integrates three IoT data sources from a nursery scenario: access events, room environment readings, and patient vital-sign readings.

## Repository structure
- `source-data/` — original CSV, JSON, and XML files, preserved for traceability.
- `integrated-data/integrated_dataset.csv` — unified dataset with one row per source record.
- `documentation/data_dictionary.md` — field definitions, types, units, and handling notes.
- `documentation/report.md` — integration method, summary statistics, data-quality decisions, and limitations.
- `scripts/integrate_data.py` — reproducible script to regenerate the integrated CSV from the source files.

## Source files
| File | Format | Contents |
|---|---|---|
| `batch101.csv` | CSV | Time-stamped room access events and person roles |
| `stream101.json` | JSON | Room temperature and door status readings |
| `feed101.xml` | XML | Patient heart rate, breathing rate, and temperature readings |

## Integration approach
The three sources represent different kinds of events and do not provide a complete shared key. Rather than force an unreliable join, each record is appended to a common table and labeled with `event_type` and `source_file`. Timestamps are normalized to `YYYY-MM-DD HH:MM:SS`. Room identifiers from the CSV are normalized to match the JSON room IDs; this and the `Patien` to `Patient` label correction are documented in `data_quality_notes`. Repeated access records are retained unless the source proves they are accidental duplicates.

## Reproduce
Run the integration script from the repository root with Python 3:
```bash
python scripts/integrate_data.py
```
The script expects the three files in `source-data/` and writes `integrated-data/integrated_dataset.csv`.

## Documentation
See `documentation/data_dictionary.md` for the schema and `documentation/report.md` for the report and descriptive results.

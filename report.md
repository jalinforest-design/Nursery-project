# Data Pipeline Integration Report

## 1. Purpose
This project integrates three nursery IoT data sources into a single, documented dataset: room access events (CSV), room environmental readings (JSON), and patient vital-sign readings (XML).

## 2. Source files and formats
- `source-data/batch101.csv`: access events with time, date, room code, person ID, person type, and access field.
- `source-data/stream101.json`: room temperature and door status readings.
- `source-data/feed101.xml`: patient ID, heart rate, breathing rate, and patient temperature readings.

## 3. Integration method
The files describe different event types and do not share a complete common key. The integrated dataset therefore uses a **union / append approach**, not a forced one-to-one join. Each source record becomes one row with a common timestamp, event type, shared identifiers where available, source-specific measurements, source filename, and source record number. Fields not present in a source are left blank rather than filled with invented values.

Timestamps were normalized to `YYYY-MM-DD HH:MM:SS` (24-hour time). Room codes in the CSV follow a consistent pattern (`10305`, `10334`, `10337`, `10345`) corresponding to JSON room identifiers (`305`, `334`, `337`, `345`); the integrated dataset removes the leading `10` from those CSV room codes and records the transformation in `data_quality_notes`. The CSV typo `Patien` was standardized to `Patient`, with the correction documented in the notes. Repeated access records were retained because the source alone does not establish that they are erroneous duplicates.

## 4. Results and summary
- CSV access events: 43
- JSON room environment readings: 36
- XML patient vital records: 196
- Total integrated records: 275
- Integrated time range: 2026-03-11 17:00:00 through 2026-03-11 21:00:00
- Room temperature readings ranged from 70.4 °F to 72.5 °F (mean 71.55 °F).
- Door status counts: {'closed': 27, 'open': 9}.
- Patient heart-rate readings ranged from 129 to 192 bpm (mean 143.14 bpm).
- Patient breathing-rate readings ranged from 36 to 73 breaths/min (mean 44.96).
- Patient temperature readings ranged from 98.0 °F to 99.2 °F (mean 98.52 °F).

These are descriptive summaries of the provided dataset, not clinical interpretations or diagnoses.

## 5. Data quality and limitations
1. The CSV `Access` column contains `n/a`; the source does not indicate whether each event was granted or denied.
2. The CSV includes repeated entries for patient `P1002` at 6:09 PM. They were preserved, not deduplicated, because no unique event ID is provided to prove they are accidental duplicates.
3. The source CSV contains the label `Patien`, which was corrected to `Patient` in the integrated data and documented.
4. The room-code normalization is based on the consistent mapping pattern across the provided records. The original source file is preserved unchanged.
5. XML patient readings do not contain a room number, so the integrated dataset does not infer one.
6. The files have different sampling intervals: room readings occur every 30 minutes, while XML patient readings are recorded more frequently. Exact timestamp equality should not be treated as proof that unrelated records describe the same physical event.

## 6. Output
The integrated CSV is `integrated-data/integrated_dataset.csv`. Field definitions are in `documentation/data_dictionary.md`. Original source files are retained in `source-data/`.

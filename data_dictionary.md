# Data Dictionary

The integrated dataset uses one row per source record. Blank fields mean that a field was not supplied by that source; they are not zero values.

| Field | Type / unit | Source | Definition / handling |
|---|---|---|---|
| timestamp | ISO-style datetime string (YYYY-MM-DD HH:MM:SS) | All sources | Event or measurement time normalized to 24-hour time. |
| event_type | Categorical string | Generated | access_event, room_environment, or patient_vitals. |
| room_number | String | CSV and JSON | Room identifier normalized to match room-sensor numbering. Blank for XML records because XML does not include room. |
| person_id | String | CSV and XML | Person identifier from access log or patient identifier from XML. |
| person_type | String | CSV and XML | Role label, e.g., Parent, Nurse, Doctor, Patient. Blank when not applicable. |
| access_status | String | CSV | Original access field; n/a means the source did not provide an access decision. |
| room_temperature_f | Decimal °F | JSON | Room environmental temperature in Fahrenheit. |
| door_status | Categorical string | JSON | Door status reported by room sensor: open or closed. |
| heart_rate_bpm | Integer beats/min | XML | Heart rate value as reported by patient sensor. |
| breathing_rate_per_min | Integer breaths/min | XML | Breathing rate value as reported by patient sensor. |
| patient_temperature_f | Decimal °F | XML | Patient temperature in Fahrenheit, distinct from room temperature. |
| source_file | String | Generated | Source file from which the row originated. |
| source_record_number | Integer | Generated | 1-based record number within its source file, used for traceability. |
| data_quality_notes | String | Generated | Notes for normalization, correction, or limitations; blank if none. |

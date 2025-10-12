# Functional Requirements

## FR1 — Overcrowded Vehicle Detection
The system shall detect **overcrowded public transport vehicles** (e.g., buses, Suzuki pickups, chingchis) using real-time CCTV camera feeds.

## FR2 — Violation Data Capture
The system shall capture and send the following parameters for each detected violation to the admin dashboard:
- Snapshot of the violation
- Timestamp of detection
- GPS location (or camera location)
- Detected vehicle’s number plate (if visible)

## FR3 - Voilation Data Storage
The system shall store all detected overcrowded vehicle violation data in a persistent database, including:
- Snapshot of the violation
- Timestamp of detection
- GPS or camera location
- Vehicle number plate (if visible)

## FR4 — Violation Management
The admin shall be able to **view** all overcrowded vehicle violations on the dashboard.

## FR5 - Search Voilation
The admin shall be able to **Search** all overcrowded vechicle voilations on the dashboard.

## FR6 — Violation Filtering
The admin shall be able to **filter** recorded violations by:
- Date/time range  
- Location  
- Vehicle Number Plate

## FR7 — Violation Deletion
The admin shall be able to **delete** specific overcrowded vehicle violation records from the dashboard.

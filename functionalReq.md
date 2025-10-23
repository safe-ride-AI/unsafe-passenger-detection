# Functional Requirements

## FR1 — Real-Time Camera Feed Acquisition
The system shall capture and stream **real-time video feeds** from fixed surveillance cameras for continuous monitoring of vehicles.

---

## FR2 — Overcrowded Vehicle Detection
The system shall detect **overcrowded public transport vehicles** using real-time CCTV camera feeds.

---

## FR3 — Person Detection and Counting
The system shall:
- Detect **all persons** outside of the vehicle (e.g., standing passengers on sides, roof passengers).  
- **Count the total number of detected persons** for vehicle.

---

## FR4 — Vehicle Type Detection (Triggered After Overcrowding)
For vehicles marked as overcrowded, the system shall determine the **type of vehicle**, such as:
- Bus  
- Suzuki pickup  
- Chingchi  


---

## FR5 — Number Plate Detection and Recognition
After identifying the overcrowded vehicle and its type, the system shall:
- Detect the **vehicle’s number plate region**.  
- Extract the **vehicle registration number**.

---

## FR6 — Violation Data Capture
For each detected overcrowding violation, the system shall capture:
- Snapshot of the overcrowded vehicle  
- Timestamp of detection  
- GPS or camera location  
- Total person count  
- Vehicle type  
- Vehicle number plate (if visible)

---

## FR7 — Violation Data Transmission
The system shall securely **transmit all violation data** to the central **admin dashboard**.

---

## FR8 — Violation Data Storage
The system shall store all detected violations in a **persistent database**, including all associated metadata (snapshot, timestamp, person count, location, vehicle type and number plate).

---

## FR9 — Admin Dashboard
The system shall provide an admin dashboard that allows authorized personnel to:
- View all recorded violations  
- Display snapshots, timestamps, person counts, vehicle type, and location  

---

## FR10 — Search Functionality
The admin shall be able to **search violations** based on:
- Vehicle number plate  

---

## FR11 — Filter Functionality
The admin shall be able to **filter violations** based on:
- Location  
- Date/time range  
- Vehicle type

---

## FR12 — View Violation Details
The admin shall be able to **view detailed information** of a specific violation, including all metadata and snapshot.

---

## FR13 — Delete Violation Records
The admin shall be able to **delete** violation records from the database via the dashboard.

---

## FR14 — User Authentication
The system shall require **login credentials** for admin access to the dashboard.

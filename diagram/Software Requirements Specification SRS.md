# Software Requirements Specification (SRS)  
**System:** Unsafe Passenger Vehicle Detection and Violation Management System  

**Version:** 1.0  
**Date:** 2025-10-01  
**Author:** Mustafa 

---

## 1. Introduction  

### 1.1 Purpose  
The purpose of this system is to **monitor vehicles in real-time**, detect unsafe passenger conditions, capture violation data, and provide an admin interface to manage violations efficiently. The system helps **enforce traffic safety regulations** and provides data for analysis and reporting.  

### 1.2 Scope  
The system will:  
- Capture real-time video feeds from surveillance cameras.  
- Detect vehicle types and assess safety of passenger load.  
- Count persons outside the vehicle.  
- Identify and record unsafe passenger vehicles.  
- Store violation data in a persistent database.  
- Provide an admin dashboard for viewing, searching, filtering, and deleting violations.  

**System Modules:**  
1. **Camera Detection Module:** Handles real-time video feed, vehicle detection, person detection, unsafe passenger detection, and number plate recognition.  
2. **Backend Module:** Stores and manages violation data and interacts with the database.  
3. **Admin Dashboard Module:** Provides UI for authorized personnel to view and manage violations.  

### 1.3 Definitions, Acronyms, and Abbreviations  
- **Unsafe Vehicle:** A vehicle classified as unsafe based on passenger Standing outside or Sitting/Standing on roofTops.  
- **FR:** Functional Requirement  

---

## 2. Overall Description  

### 2.1 System Perspective  
The system interacts with:  
- **Surveillance Cameras:** Provide video feeds of vehicles.  
- **Database:** Stores violation records and associated metadata.  
- **Admin Dashboard:** Allows authorized access to violation data.  

### 2.2 System Functions  
The system functions are aligned with the functional requirements (FRs) and include:  
- Real-time vehicle monitoring  
- Unsafe passenger vehicle detection  
- Person detection and counting  
- Vehicle type detection  
- Number plate detection and recognition  
- Violation data capture, transmission, and storage  
- Admin dashboard operations: view, search, filter, detail, delete  


### 2.3 Operating Environment  
- **Frontend:** admin dashboard  
- **Backend:** Server application with database connectivity  
- **Camera:** Fixed surveillance cameras  

### 2.4 Design and Implementation Constraints  
- Real-time detection must operate with minimal latency.  
- Database must ensure persistent storage and secure access.  
- Admin access requires authentication.  

---

## 3. Functional Requirements  

### FR1 — Real-Time Camera Feed Acquisition  
The system shall capture and stream **real-time video feeds** from fixed surveillance cameras for continuous monitoring of vehicles.  

### FR2 — Vehicle Type Detection  
For each detected vehicle, the system shall determine the **type of vehicle**, such as:  
- Bus  
- Suzuki pickup  
- Chingchi  

### FR3 — Unsafe Passenger Vehicle Detection  
The system shall determine whether a detected vehicle is **Unsafe** or **Safe** based on the passenger load and other safety criteria.  

### FR4 — Person Detection and Counting  
The system shall:  
- Detect **persons outside of the vehicle** (standing passengers or rooftop passengers).  
- **Count total persons** for each vehicle.  
**Note:** Person count is estimated due to camera resolution and occlusion.  

### FR5 — Number Plate Detection and Recognition  
For unsafe vehicles:  
- Detect the **vehicle’s number plate region**.  
- Extract the **vehicle registration number**.  

### FR6 — Violation Data Capture  
For each detected unsafe vehicle violation, the system shall capture:  
- Snapshot of the vehicle  
- Timestamp of detection  
- GPS or camera location  
- Total person count  
- Vehicle type  
- Vehicle number plate (if visible)  

### FR7 — Violation Data Transmission  
The system shall securely **transmit all violation data** to the backend module.  

### FR8 — Violation Data Storage  
The system shall store all detected violations in a **persistent database**, including all metadata (snapshot, timestamp, person count, location, vehicle type, number plate).  

### FR9 — Admin Dashboard  
The system shall provide an admin dashboard for authorized personnel to:  
- View all recorded violations  
- Display snapshots, timestamps, person counts, vehicle type, and location  

### FR10 — Search Functionality  
The admin shall be able to **search violations** based on vehicle number plate.  

### FR11 — Filter Functionality  
The admin shall be able to **filter violations** based on:  
- Location  
- Date/time range  
- Vehicle type  

### FR12 — View Violation Details  
The admin shall be able to **view detailed information** of a specific violation, including all metadata and snapshot.  

### FR13 — Delete Violation Records  
The admin shall be able to **delete violation records** from the database via the dashboard.  

### FR14 — User Authentication  
The system shall require **login credentials** for admin access to the dashboard.  

---

## 4. Non-Functional Requirements  

- **Performance:** System must process video frames in near real-time .  
- **Security:** All data transmissions must be encrypted; admin access must be authenticated.  
- **Reliability:** System must ensure 99% uptime for monitoring critical areas.  
- **Scalability:** System should handle multiple cameras simultaneously.  
- **Maintainability:** Modular architecture to allow updates to detection algorithms.  

---

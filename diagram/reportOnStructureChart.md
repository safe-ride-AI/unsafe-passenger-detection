# Structure Chart Report

## Overview
The **Structure Chart** for the *Overcrowded Vehicle Detection System* represents the modular design of the system, showing how the overall process is divided into smaller, manageable functional components. The chart follows a **top-down hierarchical approach**, beginning with the main system and breaking it into three major subsystems: **Detection Module**, **Backend (API)**, and **Admin Dashboard**.

---

## Main Modules and Their Submodules

### 1. Detection Module
This module is responsible for identifying overcrowded public transport vehicles through real-time CCTV feeds.

**Submodules:**
- **Vehicle Detection:** Detects overcrowding in vehicles using AI or computer vision algorithms.  
- **Capture Violation:** Captures the violation snapshot, timestamp, GPS location, and number plate (if visible).  
- **Send Violation:** Sends all captured violation data to the backend for storage and further processing.

---

### 2. Backend (API)
This module manages communication between the detection system, the database, and the admin interface.

**Submodules:**
- **Store Violation:** Stores detected violations in a persistent database.  
- **Retrieve Violations:** Fetches stored violation records for the admin dashboard.  
- **Delete Violation:** Removes specific violation records when requested by the admin.

---

### 3. Admin Dashboard
This module provides a graphical interface for system administrators to view and manage violations.

**Submodules:**
- **View Violations:** Displays all recorded violations on the dashboard.  
- **Filter/Search Violations:** Allows filtering and searching of violations by date, time, location, or vehicle number plate.  
- **Delete Violation:** Enables deletion of specific violation records from the dashboard.

---

## Control Hierarchy and Flow
The top-level act as a System Name, **Overcrowded Vehicle Detection System**.
- It invokes the **Detection Module** for real-time monitoring and violation detection.  
- The **Detection Module** communicates detected data to the **Backend (API)**.  
- The **Admin Dashboard** interacts with the backend to display, filter, or delete stored violations.

Lines in the structure chart represent **control relationships**, not data flow. Each connection shows a **calling relationship** where a parent module activates its child modules to perform specific functions.

---

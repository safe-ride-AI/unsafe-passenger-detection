# System Design Phase

## 1. Selected Design

The proposed system follows a **Three-Tier Layered Architecture**.  
This design divides the system into **Presentation**, **Application**, and **Data** layers.  
It ensures scalability, modularity, and maintainability, allowing each layer to operate and be updated independently.

---

## 2. Layered Architecture Overview

### **1️ Presentation Layer**
**Component:** Admin Dashboard  
- Acts as the user interface for system administrators.  
- Allows admins to view, filter, and delete overcrowding violation records.  
- Communicates with the backend server.  

---

### **2️ Application Layer**
**Components:** Detection Module and Backend Server  

**Detection Module**
- Uses computer vision to detect overcrowded vehicles.  
- Captures image snapshots and metadata (timestamp, location, vehicle ID).  
- Sends the data to the backend server through an API.

**Backend Server**
- Receives data from the detection module.  
- Stores violation records into the database.  
- Provides APIs for the Admin Dashboard.  
- Acts as the intermediary between the frontend and database.

---

### **3️ Data Layer**
**Component:** Database  
- Stores all violation data including images, timestamps, locations, and detection details.  
- Supports data retrieval, searching, and deletion through the backend.  
- Example technologies: MongoDB, MySQL, or Firebase Firestore.  

---

## 3. System Architecture Diagram

[ Admin Dashboard ] ← Presentation Layer
        |
        v
[ Backend Server ] ←→ [ Detection Module ] ← Application Layer
        |
        v
[ Database ] ← Data Layer



---

## 4. Justification for Selected Design

| Design Aspect | Reason |
|----------------|---------|
| **Scalability** | Each layer can be upgraded or scaled independently. |
| **Modularity** | Separation of concerns improves maintainability. |
| **Security** | The backend acts as a secure mediator between frontend and database. |
| **Maintainability** | Code changes in one layer don’t affect others. |

---

## 5. Summary

The **Three-Tier Layered Architecture** was selected because it best fits the project’s functional requirements — real-time overcrowded vehicle detection, data storage, and user-friendly dashboard management. This architecture ensures a robust, maintainable, and scalable system.

---

## 6. Technology Stack

| Component | Technology Used |
|------------|----------------|
| **Detection Module** | Python, YOLOv8 |
| **Backend Server** | Python |
| **Database** | MongoDB |
| **Admin Dashboard** | Flutte (Dart) |


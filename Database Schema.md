# MongoDB Database Schema

This document describes the MongoDB collections for storing traffic violations and admin credentials.

---

## 1. Violations Collection

**Collection Name:** `violations`

Each document stores information about a traffic violation:

```json
{
  "_id": ObjectId("..."),      // MongoDB unique ID
  "violation_id": "V12345",    // Unique violation identifier
  "camera_id": "C456",         // ID of the camera that captured the violation
  "vehicle_plate": "ABC-1234", // Vehicle plate number
  "vehicle_type": "Car",       // Type of vehicle
  "person_count": 2,           // Number of people in the vehicle
  "location": {
    "latitude": 37.7749,
    "longitude": -122.4194
  },
  "timestamp": ISODate("2025-10-25T14:30:00Z")  // Violation date & time
}

--

## 2. Admin Collection

**Collection Name:** `admin_credentials`

Each document stores information about admin Credentials:

```json
{
  "_id": ObjectId("..."),      // MongoDB unique ID
  "username": "admin1",
  "password_hash": "$2b$12$hashhere", // Store only hashed passwords
  "role": "admin",
  "created_at": ISODate("2025-10-25T14:30:00Z"),
  "JWT_token" "3fsdf3asdf3fasdfwfsfw3f4"
}

# 🧾 Test Plan Document

## 1. Test Plan ID
**TP-OVD-01**

---

## 2. Introduction
This document outlines the testing strategy, objectives, scope, resources, schedule, and deliverables for the **Overcrowded Vehicle Detection System**.  
The system uses **real-time CCTV feeds** to detect overcrowded public transport vehicles and provides an **admin dashboard** for monitoring, filtering, and managing detected violations.

---

## 3. Objectives
- Verify that the system accurately detects overcrowded vehicles in real time.  
- Ensure that violation data (snapshot, timestamp, location, and number plate) is correctly captured, stored, and displayed.  
- Validate that the admin dashboard provides reliable search, filter, and deletion functionality.  

---

## 4. Scope of Testing

### In Scope
- Real-time video processing for overcrowding detection.  
- Violation data capturing and transmission.  
- Database storage and retrieval of violation records.  
- Admin dashboard UI testing (view, search, filter, delete).  

### Out of Scope
- CCTV hardware testing or camera installation.  
- External network latency issues.  

---

## 5. Features to be Tested

| ID | Functional Requirement | Feature Description |
|----|------------------------|---------------------|
| FR1 | Overcrowded Vehicle Detection | Detect overcrowding in CCTV video feed. |
| FR2 | Violation Data Capture | Capture snapshot, timestamp, GPS, and number plate for each violation. |
| FR3 | Violation Data Storage | Store all violation details in the database. |
| FR4 | Violation Management | Display all violations on the admin dashboard. |
| FR5 | Search Violation | Enable admin to search violations by keywords (plate, location, etc.). |
| FR6 | Violation Filtering | Filter violations by date/time, location, or number plate. |
| FR7 | Violation Deletion | Delete violation records from the admin dashboard. |


---

## 6. Test Approach

### Test Levels
The testing will be carried out in multiple levels to ensure quality and stability:
1. **Unit Testing** – Developers will verify individual modules such as detection, database interaction, and dashboard components.
2. **Integration Testing** – The interaction between AI detection, data storage, and dashboard display will be tested.
3. **System Testing** – End-to-end testing to validate the complete workflow (from detection to admin view).
4. **Acceptance Testing** – Final verification by stakeholders to confirm the system meets user expectations.


### Test Techniques

The following test techniques will be applied to ensure effective and comprehensive testing:

| Technique | Purpose | Example in System |
|------------|----------|-------------------|
| **Black Box Testing** | Validate system behavior without internal knowledge | Test detection results for different video inputs |
| **White Box Testing** | Verify internal logic and flow of modules | Check AI model decision logic and database connections |
| **Gray Box Testing** | Combine knowledge of system internals with external testing | Test detection thresholds based on known crowd limits |
| **Equivalence Partitioning** | Reduce test cases by grouping similar input types | Low, medium, and high crowd levels |
| **Boundary Value Analysis** | Identify edge-case failures | Crowd sizes at 9, 10, and 11 persons |
| **Error Guessing** | Find likely problem areas using experience | Blurred number plates, poor lighting |
| **Exploratory Testing** | Discover unexpected behaviors | Randomly test various live or recorded feeds |


### Testing Types

| Type | Purpose |
|------|----------|
| **Functional Testing** | To verify system features match requirements (FR1–FR7). |
| **Integration Testing** | To test interaction between detection module, database, and dashboard. |
| **System Testing** | To test the complete end-to-end workflow. |
| **UI/UX Testing** | To check admin dashboard usability and responsiveness. |
| **Performance Testing** | To ensure system handles continuous video streams and multiple violations. |
| **Regression Testing** | To ensure new updates don’t break existing functionality. |

---

## 7. Test Environment

| Component | Details |
|------------|----------|
| **Frontend** | dashboard (Flutter) |
| **Backend** | Python |
| **Database** | MongoDB|
| **Detection Module** | AI/ML model for overcrowding detection using CCTV feed |
| **Test Devices** | Laptop|
| **Network** | Stable internet connection with CCTV stream simulation |

---

## 8. Test Data Requirements
- Sample CCTV video clips with varying crowd densities.  
- Test images with visible and partially visible number plates.  
- Sample GPS/camera locations.  
- Sample admin dashboard. 

---

## 9. Entry Criteria
- All functional modules implemented and unit tested.  
- Test environment set up and stable.  
- Required test data prepared.  

---

## 10. Exit Criteria
- All **critical** and **high-priority** defects resolved.  
- 80% of test cases executed successfully.  
- All features verified against functional requirements.  

---

## 11. Roles and Responsibilities

| Role | Responsibility |
|-------|----------------|
| **QA Engineer** | Design and execute test cases, report bugs. |
| **Developer** | Fix reported issues and retest. |
| **Test Lead** | Manage testing schedule and review results. |
| **Project Manager** | Approve test completion and sign-off. |

---

## 12. Test Deliverables
- Test Plan (this document)  
- Test Cases Document  
- Bug/Defect Report  
- Test Execution Report  
- Final Test Summary Report  

---

## 13. Risk and Mitigation

| Risk | Impact | Mitigation |
|-------|---------|-------------|
| AI model false positives/negatives | High | Fine-tune detection threshold, use better dataset |
| Database storage failure | High | Use backup and replication |
| Slow dashboard loading | Medium | Optimize queries and pagination |
| Missing GPS data | Low | Use default camera location |
| Number plate not detected or blurred | Medium | Apply image enhancement and OCR fallback models |

---

## 14. Test Schedule

| Phase | Duration | Responsible |
|--------|-----------|--------------|
| Test Planning | Oct 13–Oct 15 | QA Lead |
| Test Case Design | Oct 15–Oct 17 | QA Engineer |
| Environment Setup | Oct 17–Oct 18 | DevOps |
| Test Execution | Oct 18–Oct 25 | QA Team |
| Bug Fixing & Retesting | Oct 25–Oct 28 | Dev + QA |
| Test Closure | Oct 29 | Project Manager |

---

## 15. Test Case Summary (High-Level)

| ID | Test Scenario | Expected Result |
|----|----------------|-----------------|
| TC1 | Detect overcrowded vehicle from live feed | System flags overcrowded vehicle correctly. |
| TC2 | Capture and send violation data to backend | All fields (snapshot, timestamp, GPS, plate) sent. |
| TC3 | Store violation data in database | Data appears correctly in database. |
| TC4 | Display violations in dashboard | Violations list loads correctly. |
| TC5 | Search violation | Search returns correct results. |
| TC6 | Filter by date/location/plate | Filter works as expected. |
| TC7 | Delete a violation record | Record removed successfully. |

---

## 16. Approval

| Name | Role | Signature | Date |
|-------|------|------------|------|
| **Mustafa** | QA Engineer |  |  |
| **Fazale-Basit** | Project Manager |  |  |

---

# Software Development Plan (SDP)

## 1. Introduction
The **Overcrowded Vehicle Detection System** is designed to automatically identify overcrowded public transport vehicles (such as buses, chingchis, and pickups) using CCTV camera feeds and AI-based detection.  
Detected violations will be stored in a database and displayed on an admin dashboard for review.  
This Software Development Plan defines the approach, tools, team roles, and processes that will guide the system’s development and maintenance.

---

## 2. Project Organization

The project team consists of three members who collectively handle development, testing, and deployment tasks. Their roles and responsibilities are defined below:

| Member | Role | Responsibility |
|---------|------|----------------|
| **Hamza** | **AI & System Integration Developer** | Leads development of the AI detection model for overcrowded vehicles, integrates it with backend services, and ensures smooth data flow to the dashboard. |
| **Abdullah Amir** | **Backend & Database Developer** | Implements backend, manages database operations, and develops APIs for data retrieval and storage. |
| **Mustafa** | **Frontend & Dashboard Developer (UI/UX)** | Designs and develops the Flutter-based admin dashboard, ensuring features like viewing, searching, filtering, and deleting violation records work effectively. |

> *Each member also contributes to testing and documentation during their respective modules.*

| Role | Responsibility |
|------|-----------------|
| **Project Manager** | Plans, monitors, and manages the overall project. |
| **Developers** | Build and integrate system modules (AI, backend, dashboard). |
| **QA/Testers** | Create and execute test cases to ensure system quality. |
| **UI/UX Designer** | Designs an intuitive and responsive admin dashboard. |
| **DevOps Engineer** | Manages deployment, environment setup, and updates. |

---

## 3. Development Process
The project will follow the **Iterative Development Model**, where each cycle involves analysis, design, development, and testing.  
This allows continuous feedback, early error detection, and flexible feature improvement.

### Key Iterations

| Iteration | Functional Requirements (FRs) Covered | Description |
|------------|----------------------------------------|-------------|
| **Iteration 1** | FR1 | Develop and test AI module for overcrowded vehicle detection. |
| **Iteration 2** | FR2, FR3 | Implement violation data capture and database storage. |
| **Iteration 3** | FR4, FR5, FR6, FR7 | Develop admin dashboard for viewing, searching, filtering, and deleting violation data. |
| **Iteration 4** | All FRs | Perform full system integration, testing, and performance optimization. |


---

## 4. Tools and Technologies
The tools and technologies used to build, test, and deploy the system are listed below:

| Category | Tools / Technologies |
|-----------|----------------------|
| **Frontend** | Flutter (Dart) |
| **Backend** | Python |
| **Database** | MongoDB |
| **AI / ML** | Python, YOLO |
| **Version Control** | Git, GitHub |

---

## 5. Work Breakdown Structure (WBS)
The project is divided into smaller, manageable modules for efficient development and tracking.

1. **AI Detection Module** – Detect overcrowded vehicles from video feeds.  
2. **Database Integration** – Store violation details in Firestore.  
3. **Dashboard Development** – Display, filter, and manage violation records.  
4. **Testing and Deployment** – Conduct testing, fix bugs, and deploy system.

---

## 6. Schedule and Milestones
The estimated timeline for major development phases is as follows:

| Phase | Start | End | Responsible |
|--------|--------|------|--------------|
| Requirement Analysis | Oct 13 | Oct 15 | Project Lead |
| Design Phase | Oct 16 | Oct 20 | UI/UX Team |
| Development Phase | Oct 21 | Nov 10 | Dev Team |
| Testing & QA | Nov 11 | Nov 20 | QA Team |
| Deployment | Nov 21 | Nov 25 | DevOps |
| Maintenance | Ongoing | — | Support Team |

---

## 7. Resource Requirements
### Hardware
- Developer workstations or laptops  
- GPU-enabled system for AI model testing  
- Access to CCTV video feeds for model validation  

### Software
- Flutter SDK and Android Studio  
- Firebase Console access  
- Python environment


---

## 8. Risk and Mitigation

| Risk | Impact | Mitigation |
|-------|---------|-------------|
| AI model false positives/negatives | High | Fine-tune detection threshold, use better dataset |
| Database storage failure | High | Use backup and replication |
| Slow dashboard loading | Medium | Optimize queries and pagination |
| Missing GPS data | Low | Use default camera location |
| Number plate not detected or blurred | Medium | Apply image enhancement and OCR fallback models |

---

## 9. Quality Assurance Plan
Ensures the system meets performance and functionality standards through:
- Code reviews before merges  
- Unit and integration testing after each iteration  
- Continuous integration with GitHub Actions  
- Reference to a detailed **Test Plan Document** for full QA coverage  

---

## 10. Configuration Management
Defines how code, versions, and changes are tracked throughout development.

- **Version Control:** Git (GitHub repository)  
- **Branching Strategy:**  
  - `main` → Stable production code  
  - `develop` → Ongoing development  
  - `feature/*` → Individual module work  
  - `se`  → Software Engineering work
- **Change Tracking:** GitHub Issues and Pull Requests  

---

## 11. Delivery and Maintenance
Describes how the system will be delivered and maintained after deployment.

### Delivery
- Source code and documentation shared via GitHub  
- Deployment on (not decided yet)

### Maintenance
- Regular updates for AI model improvement  
- backups of database  
- Ongoing bug fixes and feature enhancements  

---


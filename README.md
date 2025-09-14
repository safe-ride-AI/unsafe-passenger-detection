# SafeRide AI  
**Image-based Real-Time Passenger Vehicle Overloading Detection using Deep Learning**

---

## Overview

**SafeRide AI** is an end-to-end computer vision system designed to detect unsafe passenger practices in public transport vehicles, such as passengers hanging outside or sitting on rooftops of buses, chingchis, rickshaws, and Suzuki pickups.  

This system uses roadside CCTV camera feeds to:
- Detect public transport vehicles
- Identify overloaded or unsafe passenger behaviors
- Capture violation evidence (image, time, location)
- Log violations to a server and display them on a dashboard

---

## Motivation

In many developing regions across South Asia and Africa, public transport vehicles are often dangerously overloaded. Passengers frequently hang outside or ride on rooftops, leading to severe accidents and fatalities.

Current monitoring is **manual, inconsistent, and not scalable**.  
This project aims to **automate traffic enforcement** using AI.

> According to the WHO, 1.3 million people die annually in road crashes, and overloading is a major contributor in developing countries.

---

## System Workflow

```mermaid
flowchart LR
  A[Traffic Camera (Law Enforcement)] --> B[Frame Capture]
  B --> C[Deep Learning Pipeline]
  C --> C1[Vehicle Detection]
  C1 --> C2[Overloading Classification]
  C2 --> D{Is Overloaded?}
  D -- Yes --> E[Capture Evidence (image, time, location)]
  E --> F[Transmit to Server / Log DB]
  F --> G[Dashboard / Violation Reports]
  D -- No --> H[Continue Monitoring]

---

## Project Structure
safe-ride-AI/
│── data/             # Collected traffic videos & frames
│── labels/           # YOLO annotations
│── src/               # Source code
│   ├── preprocess.py
│   ├── train.py
│   ├── detect.py
│── notebooks/         # Experiments and model training notebooks
│── results/            # Sample outputs & model results
│── docs/                # Reports, presentations
│── requirements.txt     # Dependencies
│── README.md             # Project overview

---

## Dataset Plan

Build a custom dataset of public transport vehicles:
Buses
Suzuki pickups
Chingchis

  Collect at least 1000 images per class
  Capture various lighting, weather, and angles
  Annotate using CVAT / LabelImg in YOLO format
---

## Tech Stack

  YOLOv8 / YOLOv9 – object detection
  OpenCV – video/frame processing
  Python 3.10+
  FastAPI / Flask – backend for model + API
  Flutter – dashboard front end
  CVAT / LabelImg / Roboflow – dataset annotation

---

## Project Goals
**FYP-1 (Fall 2025)**
  Data collection and preprocessing
  Image annotation (YOLO format)
  Train initial baseline model
**FYP-2 (Spring 2026)**
  Improve model accuracy and speed
  Real-time detection integration
  Build dashboard and backend
  Deploy and test full system

---

## Project Timeline

| Phase                      | Duration                 |
| -------------------------- | ------------------------ |
| FYP-1: Sep 2025 – Dec 2025 | Data + Model Development |
| FYP-2: Jan 2026 – May 2026 | Integration + Deployment |

---

## Expected Outcomes

  Detect overloaded vehicles in real time from roadside cameras
  Automatic logging of violations (image, time, location)
  Interactive dashboard for law enforcement
  Help reduce road accidents and support smart city initiatives

---

## License
This project is developed for academic purposes under the FAST-NUCES Final Year Project 2025–26.



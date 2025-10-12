# SafeRide AI

**Image-based Real-Time Passenger Vehicle Overcrowded Detection using Deep Learning**

-----

## Overview

**SafeRide AI** is an end-to-end computer vision system designed to detect unsafe passenger practices in public transport vehicles, such as passengers hanging outside or sitting on rooftops of buses, chingchis, rickshaws, and Suzuki pickups.

This system uses roadside CCTV camera feeds to:

  - Detect public transport vehicles.
  - Identify overcrowded or unsafe passenger behaviors.
  - Capture violation evidence (number plate, image, time, location).
  - Estimate the number of unsafe passengers (hanging + on roof).
  - Log violations to a server and display them on a dashboard.

## Motivation

In many developing regions across South Asia and Africa, public transport is often dangerously overcrowded, leading to severe accidents and fatalities. Current monitoring is **manual, inconsistent, and not scalable**. This project aims to **automate traffic enforcement** using AI to create safer roads and support smart city initiatives.

-----

## Tech Stack

  - **Object Detection:** YOLOv8 / YOLOv9
  - **Core Library:** Python 3.10+
  - **Video Processing:** OpenCV
  - **Backend & API:** FastAPI / Flask
  - **Frontend:** Flutter
  - **Annotation:** CVAT / LabelImg / Roboflow

-----

## Project Structure

```
safe-ride-AI/
├── data/         # Collected traffic videos & frames
├── labels/       # YOLO annotations
├── src/          # Source code
│   ├── preprocess.py
│   ├── train.py
│   └── detect.py
├── notebooks/    # Experiments and model training notebooks
├── results/      # Sample outputs & model results
├── docs/         # Reports, presentations
├── requirements.txt
└── README.md
```

-----

## Dataset Plan

The project involves building a custom dataset of public transport vehicles common in the target regions.

  - **Classes:** Bus, Suzuki Pickup, Chingchi.
  - **Target Size:** At least 1000 annotated images per class.
  - **Diversity:** Images will be captured in various lighting, weather, and camera angle conditions to ensure model robustness.
  - **Format:** Annotations will be in YOLO format.

-----

## Project Goals & Timeline

The project is divided into two academic semesters, each with clear objectives.

### FYP-1 (Fall 2025)

  - [ ] Data collection and preprocessing
  - [ ] Image annotation (YOLO format)
  - [ ] Train initial baseline model

### FYP-2 (Spring 2026)

  - [ ] Improve model accuracy and speed
  - [ ] Real-time detection integration
  - [ ] Build dashboard and backend API
  - [ ] Deploy and test the complete end-to-end system

| Phase                       | Duration                  | Focus                    |
| --------------------------- | ------------------------- | ------------------------ |
| **FYP-1** | Sep 2025 – Dec 2025       | Data + Model Development |
| **FYP-2** | Jan 2026 – May 2026       | Integration + Deployment |

-----

## Expected Outcomes

  - A system to **detect overloaded vehicles in real-time** from roadside cameras.
  - **Automatic logging of violations** with evidence (image, time, location).
  - An **interactive dashboard** for law enforcement agencies.
  - A solution that helps **reduce road accidents** and supports smart city infrastructure.

-----
## License

This project is licensed under the MIT License, see the LICENSE file for details.
This project is also developed for academic purposes under the FAST-NUCES Final Year Project 2025–26.

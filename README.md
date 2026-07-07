# RoadScan — Road Damage Detection System

A full-stack road damage detection system using YOLOv8 fine-tuned on the RDD2022 India dataset. Upload a road image to detect and classify surface damage by type and severity in real time.

**Live Demo:** [your-vercel-url]

---

## Problem Statement

Indian municipalities lack scalable tools to identify and prioritize road repairs. Manual surveys are slow and inconsistent. This system automates damage detection from dashcam or smartphone images — any image can feed into a reporting pipeline without requiring human inspection.

## Architecture

```
React/TypeScript Frontend (Vercel)
↓ multipart/form-data
FastAPI Backend (Render)
↓
YOLOv8s fine-tuned on RDD2022 India
↓
Annotated image + structured JSON report
```
---

## Features

- Detects 5 damage classes: Longitudinal Crack, Transverse Crack, Alligator Crack, Pothole, White Line Blur
- Severity classification (Severe / Moderate / Minor) based on bounding box geometry and confidence
- Returns annotated image with color-coded bounding boxes + structured detection report
- Model loaded once on server startup via singleton pattern — no per-request overhead

## Tech Stack

**Backend:** Python, FastAPI, YOLOv8 (Ultralytics), OpenCV, Docker
**Frontend:** React, TypeScript, Vite, Axios
**ML:** YOLOv8s fine-tuned on RDD2022 India subset (5,368 labeled images, 30 epochs, Google Colab T4 GPU)
**Deploy:** Render (backend), Vercel (frontend)

## Model Performance

| Class | mAP50 |
|---|---|
| Alligator Crack | 0.598 |
| Pothole | 0.471 |
| White Line Blur | 0.405 |
| Longitudinal Crack | 0.329 |
| Transverse Crack | 0.162 |
| **Overall** | **0.393** |

## Known Limitations

- **Domain shift:** Trained on dry paved roads. Performance degrades on unpaved or waterlogged roads — water-filled potholes create specular reflections that mask depth cues the model relies on.
- **Class imbalance:** Transverse crack has only 50 training samples, leading to underdetection.
- **Next iteration:** Augmented training data with wet/muddy road conditions and more balanced class distribution would meaningfully improve generalization.

## Local Setup

```bash
# Backend
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
# Place best.pt in backend/weights/
python -m uvicorn app.main:app --reload

# Frontend
cd frontend
npm install
npm run dev
```

## Training

See `notebooks/train_yolo.ipynb` for the full fine-tuning pipeline on Google Colab using the RDD2022 India subset.

## Dataset

[Road Damage Dataset 2022 (RDD2022)](https://github.com/sekilab/RoadDamageDetector) — India subset, 5,368 labeled images across 5 damage categories.
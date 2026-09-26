# CivicLens

**Report road hazards. Help your community stay safe.**

CivicLens lets citizens report road hazards -potholes, damaged signage, flooding, broken streetlights — by simply snapping a photo. An ML model automatically classifies each hazard's category and severity, so reports are triaged and prioritized without waiting on manual review. Local admins then track and resolve issues through a dedicated dashboard.

#DEMO VIDEO
https://youtu.be/9nKBa-5cjbk
---

## Table of contents

- [Features](#features)
- [How it works](#how-it-works)
- [Tech stack](#tech-stack)
- [Project structure](#project-structure)
- [Note on the dataset](#note-on-the-dataset)


---

## Features

## Features

| Feature | Description |
|---|---|
| **Photo-based reporting** | Users capture or upload an image of a hazard directly from their phone or browser |
| **Automatic geotagging** | Reports are tagged with the reporter's location via the browser's Geolocation API |
| **ML-powered triage** | An object detection model classifies each report by category (pothole, flooding, damaged signage, etc.) and severity (low / medium / high / critical) |
| **Priority-driven feed** | The homepage surfaces the highest-severity, most-upvoted reports first, with no manual sorting needed |
| **Community upvoting** | Users upvote existing reports to signal how widespread or urgent an issue is |
| **Status tracking** | Reports move through a lifecycle: `pending` → `in review` → `resolved`, updated by admins |
| **Admin dashboard** | Authorized admins review flagged reports, verify ML predictions, and mark issues resolved |
| **Nearby incident map** | Users can view a map of reports near their current location |
| **Intelligent incident aggregation** *(Planned)* | New reports are compared with existing unresolved incidents by GPS location and category. Matching reports are linked to the original incident instead of creating duplicates, so statistics reflect distinct problems rather than raw report counts |
| **ML-based duplicate detection** *(Planned)* | A similarity model learns visual similarity between images and estimates how likely two reports show the same incident. It is combined with GPS distance and detected category, so look-alike issues in different places are not merged |
| **Spatial clustering** *(Planned)* | Distinct incidents are grouped by geographic proximity into clusters |
| **Hotspot scoring** *(Planned)* | Each cluster is scored on incident count, severity, community engagement and recent change over a time window, highlighting both established and emerging problem areas |
---

## How it works

1. A logged-in user takes or uploads a photo of a road hazard.
2. The browser captures the user's coordinates via geolocation.
3. The image is sent to the backend, where an ML model predicts the hazard's **category** and **severity**.
4. The report is stored with status `pending` and immediately appears on the public feed, sorted by severity.
5. An admin reviews the report — confirming or correcting the ML prediction if needed — and updates its status once resolved.

---

## Tech stack

- **Backend** — Flask (Python)
- **Frontend** — Jinja2 templates, HTML/CSS, JavaScript
- **ML model** — image classification / object detection for hazard category and severity, see `data/` for training data structure, annotations, and conversion scripts
- **Database** — SQLite

---

## Project structure

```
CivicLense/
├── Backend/              # Flask application, routes, models
├── data/                 # Training dataset, annotations, and conversion scripts (excluded — see below)
├── static/               # CSS, JS, uploaded report images
├── templates/            # Jinja2 HTML templates
└── README.md
```


## Note on the dataset

> The training dataset (`data.zip`, ~2000 images) and processed data folders (`data/images`, `data/yolo_dataset`, etc.) are excluded from this repository due to GitHub's file size limits.
>
> The dataset structure, annotation format, and conversion scripts (`COCO-conversion-script.py`, `YOLO-conversion-script.py`, `split_dataset.py`) are documented in `data/` and available on request.

---




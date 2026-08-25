# CivicLens

**Report road hazards. Help your community stay safe.**

CivicLens lets citizens report road hazards -potholes, damaged signage, flooding, broken streetlights — by simply snapping a photo. An ML model automatically classifies each hazard's category and severity, so reports are triaged and prioritized without waiting on manual review. Local admins then track and resolve issues through a dedicated dashboard.

---

## Table of contents

- [Features](#features)
- [How it works](#how-it-works)
- [Tech stack](#tech-stack)
- [Project structure](#project-structure)
- [Note on the dataset](#note-on-the-dataset)
- [Roadmap](#roadmap)

---

## Features

| Feature | Description |
|---|---|
| **Photo-based reporting** | Users capture or upload an image of a hazard directly from their phone or browser |
| **Automatic geotagging** | Reports are tagged with the reporter's location via the browser's Geolocation API |
| **ML-powered triage** | An object detection model classifies each report by category (pothole, flooding, damaged signage, etc.) and severity (low / medium / high / critical) |
| **Priority-driven feed** | The homepage surfaces the highest-severity, most-upvoted reports first — no manual sorting needed |
| **Community upvoting** | Users upvote existing reports to signal how widespread or urgent an issue is |
| **Status tracking** | Reports move through a lifecycle: `pending` → `in review` → `resolved`, updated by admins |
| **Admin dashboard** | Authorized admins review flagged reports, verify ML predictions, and mark issues resolved |
| **Nearby incident map** | Users can view a map of reports near their current location |

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

## Roadmap

- [ ] Duplicate/cluster detection for reports near the same location
- [ ] Admin analytics dashboard (hazard trends by area, category, and time)
- [ ] Confidence scores shown alongside ML predictions for admin review

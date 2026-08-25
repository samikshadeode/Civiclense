CivicLens
Report road hazards. Help your community stay safe.
CivicLens lets citizens report road hazards - potholes, damaged signage, flooding, broken streetlights - by simply snapping a photo.
An ML model automatically classifies the hazard's category and severity, so reports are triaged and prioritized without waiting on manual review. Local admins can then track and resolve issues through a dedicated dashboard.

Features
1.Photo-based reporting — users capture or upload an image of a hazard directly from their phone or browser
2.Automatic geotagging — reports are tagged with the reporter's location using the browser's Geolocation API
3.ML-powered triage — an object detection model classifies each report by category (e.g. pothole, flooding, damaged signage) and severity (low / medium / high / critical), removing the need for manual sorting
4.Priority-driven feed — the homepage surfaces the highest-severity, most-upvoted reports first, so the most urgent hazards get visibility without human intervention
5.Community upvoting — users can upvote existing reports to signal how widespread or urgent an issue is
6.Status tracking — every report moves through a lifecycle: pending → in review → resolved, updated by admins
7.Admin dashboard — authorized admins review flagged reports, verify ML predictions, and mark issues as resolved
8.Nearby incident map — users can view a map of reports near their current location


How it works
A logged-in user takes or uploads a photo of a road hazard.
The browser captures the user's coordinates via geolocation.
The image is sent to the backend, where an ML model predicts the hazard's category and severity.
The report is stored with status pending and immediately becomes visible on the public feed, sorted by severity.
An admin reviews the report — confirming or correcting the ML prediction if needed — and updates its status once resolved.

Tech stack
Backend: Flask (Python)
Frontend: Jinja2 templates, HTML/CSS, JavaScript
ML model: image classification/object detection for hazard category and severity (see data/ for training data structure, annotations, and conversion scripts)
Database: (add your DB here, e.g. SQLite / PostgreSQL)

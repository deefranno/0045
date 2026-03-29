# Product Image Finder

A local-first Debian Linux desktop app for finding, reviewing, and downloading
product images in bulk.

---

## Phase 1 – UI Scaffold

This phase establishes the base project structure, application window, and
navigation shell.  No database, scraping, or import logic is included yet.

---

## Requirements

- Debian Linux (tested on Debian 12 / Ubuntu 22.04+)
- Python 3.11 or later
- A virtual environment (recommended)

---

## Quick Start

```bash
# 1. Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
python3 app.py
```

If PySide6 fails to find Qt platform plugins on a minimal Debian install,
install the system dependency:

```bash
sudo apt install libxcb-cursor0
```

---

## Project Structure

```
product_image_finder/
├── app.py                  # Entry point
├── requirements.txt
├── README.md
│
├── core/                   # Non-UI logic (config, database, processing)
│   ├── __init__.py
│   └── config.py           # App-wide constants
│
├── ui/                     # All PySide6 UI code
│   ├── __init__.py
│   ├── theme.py            # Global Qt stylesheet
│   ├── main_window.py      # MainWindow – header + sidebar + stack
│   ├── sidebar.py          # Left navigation sidebar
│   └── views/              # One file per section
│       ├── __init__.py
│       ├── base_view.py    # Shared view scaffold (subclassed by each view)
│       ├── dashboard.py
│       ├── import_products.py
│       ├── search_queue.py
│       ├── review_images.py
│       ├── exports.py
│       └── settings.py
│
└── data/                   # Local SQLite DB and downloaded images (Phase 2+)
    └── .gitkeep
```

---

## Phases

| Phase | Description                                    | Status      |
|-------|------------------------------------------------|-------------|
| 1     | Project scaffold + navigation shell            | ✓ Complete  |
| 2     | SQLite data model + product import (TXT/CSV)   | Upcoming    |
| 3     | Name cleaning + search query generation        | Upcoming    |
| 4     | Playwright image search + candidate storage    | Upcoming    |
| 5     | Image review UI (approve / reject)             | Upcoming    |
| 6     | Image download + export (CSV / JSON)           | Upcoming    |

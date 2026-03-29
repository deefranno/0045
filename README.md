# Product Image Finder

A local-first Debian Linux desktop app for finding, reviewing, and downloading
product images in bulk.

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

## Import Formats

### Plain text (.txt)

One product name per line. Blank lines are ignored.

```
Widget Pro 500ml Blue
Gadget XL v2
Accessory Kit Standard
```

### CSV (.csv)

Standard comma-separated file with a header row. Any column can be selected
as the product name column inside the app.

```csv
sku,product_name,category
SKU001,Widget Pro 500ml Blue,Electronics
SKU002,Gadget XL v2,Accessories
SKU003,Accessory Kit Standard,Accessories
```

**Notes:**
- Files exported from Excel are supported (UTF-8 BOM and latin-1 are handled automatically)
- The column picker appears after selecting a CSV — choose whichever column holds the name
- Blank cells in the selected column are skipped automatically

### Paste

Switch to the **Paste Text** tab and type or paste names directly — one per line.

---

## Duplicate Handling

When loading a preview, each product name is checked against the database:

| Status      | Meaning                                          |
|-------------|--------------------------------------------------|
| **New**     | Not in the database — will be imported           |
| **In DB**   | Already exists as a product                      |
| **Batch dup.** | Appeared more than once in the same import   |

Choose **Skip** (default) to import only new names, or **Import anyway** to
create additional rows for names already in the database.

---

## Project Structure

```
product_image_finder/
├── app.py                      # Entry point
├── requirements.txt
├── README.md
│
├── core/
│   ├── __init__.py
│   ├── config.py               # App-wide constants and paths
│   ├── models.py               # Product + CandidateImage dataclasses
│   ├── database.py             # DatabaseManager (schema DDL, connection)
│   ├── repository.py           # ProductRepository (all SQL)
│   └── importer.py             # File/paste parsing, preview row building
│
├── ui/
│   ├── __init__.py
│   ├── theme.py                # Global Qt stylesheet
│   ├── main_window.py          # MainWindow – header + sidebar + stack
│   ├── sidebar.py              # Left navigation sidebar
│   └── views/
│       ├── __init__.py
│       ├── base_view.py        # Placeholder scaffold for unimplemented views
│       ├── dashboard.py        # Live stat cards
│       ├── import_products.py  # Full import workflow
│       ├── search_queue.py
│       ├── review_images.py
│       ├── exports.py
│       └── settings.py
│
└── data/
    └── products.db             # Created automatically on first run (not committed)
```

---

## Phases

| Phase | Description                                    | Status      |
|-------|------------------------------------------------|-------------|
| 1     | Project scaffold + navigation shell            | ✓ Complete  |
| 2     | SQLite data model + Dashboard counts           | ✓ Complete  |
| 3     | Product import from TXT / CSV / paste          | ✓ Complete  |
| 4     | Name cleaning + search query generation        | Upcoming    |
| 5     | Playwright image search + candidate storage    | Upcoming    |
| 6     | Image review UI (approve / reject)             | Upcoming    |
| 7     | Image download + export (CSV / JSON)           | Upcoming    |

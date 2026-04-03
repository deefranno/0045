# Product Image Matcher Pro

Product Image Matcher Pro is a desktop application designed for supermarket inventory management. It automates the process of finding, matching, and ranking product images from multiple online sources based on messy, abbreviated product names.

## System Requirements
- Debian 12 / Debian Trixie (or compatible Linux distribution)
- Python 3.11+ (Python 3.12/3.13 supported)
- Pip and Python Venv
- Playwright Chromium dependencies

## Installation
From a clean Debian terminal, run:
```bash
sudo apt update
sudo apt install python3 python3-venv python3-pip
./run.sh
```
*Note: `run.sh` will automatically install Python dependencies and Playwright browsers.*

## How to Use
1. **Import**: Upload a CSV file containing product names or paste names manually. Map the columns for name, SKU, and brand.
2. **Dashboard/Results**: (Work in progress) Future updates will show processing metrics.
3. **Process**: Products are automatically normalised (abbreviations expanded, sizes extracted), searched across tiers of websites, and scored.
4. **Review**: Manually review matches with low confidence scores. Accept, reject, or select a different image.
5. **Export**: Export the final matches to a WooCommerce-compatible CSV with UTF-8 BOM encoding.

## Configuration
Configuration files are located in the `config/` directory:
- `app_config.json`: App-level settings, whitelists, and blacklists.
- `abbreviations.json`: Maps abbreviations like "P/BOIL" to "parboiled".
- `brands.json`: List of brands for detection.
- `synonyms.json`: Maps terms like "CHOC" to "chocolate".
- `sources.json`: Defines search URLs and tiers (1-6).

## Troubleshooting
1. **Playwright Errors**: If the scraper fails, ensure Playwright dependencies are installed using `playwright install-deps`.
2. **Database Locked**: Close any other application accessing `data/app_database.sqlite`.
3. **Empty Results**: Check `config/sources.json` to ensure URLs are correct and domains are not blacklisted.
4. **Encoding Issues**: Ensure input CSVs are UTF-8 or Latin-1.
5. **UI Lag**: Thumbnail loading and searching are offloaded to background threads, but ensure you have a stable internet connection.

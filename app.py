import sys
import os
from PySide6.QtWidgets import QApplication
from utils.logger import setup_logging, logger
from core.config_loader import load_all_configs
from core.database import initialize_database
from ui.main_window import MainWindow

def main():
    # Initial setup
    setup_logging()
    logger.info("Starting Product Image Matcher Pro")

    # Init database
    try:
        initialize_database()
    except Exception as e:
        logger.critical(f"Failed to initialize database: {e}")
        sys.exit(1)

    # Load config
    try:
        configs = load_all_configs()
    except Exception as e:
        logger.critical(f"Failed to load configurations: {e}")
        sys.exit(1)

    # Launch GUI
    app = QApplication(sys.argv)

    window = MainWindow(configs)
    window.show()

    logger.info("Application launched.")
    sys.exit(app.exec())

if __name__ == "__main__":
    main()

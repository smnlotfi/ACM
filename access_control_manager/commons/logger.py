# logger.py
import logging
from logging.handlers import RotatingFileHandler
import os

# Set up the logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create a log folder if it doesn't exist
log_folder = 'logs'
if not os.path.exists(log_folder):
    os.makedirs(log_folder)

# Set up a rotating file handler to keep the log file from growing too large
log_file_path = os.path.join(log_folder, 'app.log')
handler = RotatingFileHandler(log_file_path, maxBytes=1024 * 1024, backupCount=5)
handler.setLevel(logging.DEBUG)

# Create a formatter and add it to the handler
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(handler)

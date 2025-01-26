import logging
from logging.handlers import RotatingFileHandler
import os

# Define the logger
logger = logging.getLogger('autogen_trace_logger')
logger.setLevel(logging.INFO)  # Set the log level to INFO for production

# Create a file handler with log rotation
log_file = os.path.join('logs', 'autogen_trace.log')
file_handler = RotatingFileHandler(log_file, maxBytes=1024*1024*5, backupCount=5)  # 5 MB per file, 5 files

# Create a console handler
console_handler = logging.StreamHandler()

# Define a formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Set the formatter for the handlers
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add the handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# Example usage
logger.info("This is an info message")
logger.error("This is an error message")
import logging

# Create a logger with the name of the current module
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create a file handler and set the level to DEBUG
file_handler = logging.FileHandler('logs/authentication.log')
file_handler.setLevel(logging.DEBUG)

# Create a rotating file handler that writes to a separate log file
rotating_file_handler = logging.handlers.RotatingFileHandler(
    'logs/etrade.log', maxBytes=10485760, backupCount=3
)
rotating_file_handler.setLevel(logging.DEBUG)

# Create a console handler and set the level to INFO
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Create a formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add the handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

import logging
import os
from datetime import datetime

log_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
os.makedirs(log_folder, exist_ok=True)
log_file = os.path.join(log_folder, f'{datetime.now().date().__str__()}app.log')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename=log_file,
    filemode='a'
)
logger = logging.getLogger(__name__)

print(f"Logging to {log_file}")
logger.info("Logger initialized.")
logger.info(f"Log file: {log_file}")

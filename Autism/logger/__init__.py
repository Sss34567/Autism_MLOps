import logging
import os
import sys
from datetime import datetime
from pathlib import Path

LOG_DIR = "logs"
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

try:
    log_dir_path = PROJECT_ROOT / LOG_DIR
    log_dir_path.mkdir(parents=True, exist_ok=True)
except OSError:
    log_dir_path = Path("/tmp") / LOG_DIR
    log_dir_path.mkdir(parents=True, exist_ok=True)

logs_path = os.path.join(log_dir_path, LOG_FILE)

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(logs_path),
        logging.StreamHandler(sys.stdout),  # يظهر في Azure Log stream
    ],
)

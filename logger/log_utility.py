import logging
import os
from datetime import datetime


def setup_logger(log_file: str = "finance_app.log") -> logging.Logger:
    log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
    os.makedirs(log_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_file_path = os.path.join(log_dir, f"{log_file.split('.')[0]}_{timestamp}.log")

    logger = logging.getLogger("ag_std_mcp_agent")
    logger.setLevel(logging.DEBUG)

    # Prevents duplicate handlers
    if not logger.handlers:
        file_handler = logging.FileHandler(log_file_path)
        file_handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger

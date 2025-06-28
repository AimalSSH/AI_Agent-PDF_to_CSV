import logging
from logging.handlers import RotatingFileHandler
import yaml
from pathlib import Path

def setup_logging():
    config_path = Path(__file__).parent.parent / "config" / "logging_config.yaml"
    
    with open(config_path) as f:
        config = yaml.safe_load(f)
    
    logger = logging.getLogger("PDF_AI_Processor")
    logger.setLevel(config["level"])
    file_handler = RotatingFileHandler(
        "pdf_processor.log",
        maxBytes=1_000_000,
        backupCount=3,
        encoding='utf-8'
    )
    
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    file_handler = RotatingFileHandler(
        config["log_file"],
        maxBytes=config["max_bytes"],
        backupCount=config["backup_count"]
    )
    file_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    return logger

logger = setup_logging()
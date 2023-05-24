import os
import json
import logging
from dotenv import load_dotenv
import pytesseract
import openai

load_dotenv()

def load_config():
    """Load configuration from JSON file"""
    try:
        logging.info("Loading configuration from config.json")
        with open('config.json') as config_file:
            config = json.load(config_file)
        logging.info("Successfully loaded configuration")
        return config
    except (FileNotFoundError, IOError) as e:
        logging.error(f"Error reading config file: {e}")
        return None
    except json.JSONDecodeError as e:
        logging.error(f"Error parsing config file: {e}")
        return None

def set_config():
    """Load configuration and set environment variables"""
    load_dotenv()
    config = load_config()
    if config is None:
        return None

    logging.info("Setting environment variables and configuration parameters")
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    openai.api_key = os.getenv("OPENAI_API_KEY")
    pytesseract.pytesseract.tesseract_cmd = os.getenv("TESSERACT_CMD")
    return config

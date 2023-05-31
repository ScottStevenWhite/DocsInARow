import os
import logging
from dotenv import load_dotenv
import pytesseract
import openai


def set_config():
    """Load configuration and set environment variables"""
    load_dotenv()

    logging.info("Loading environment variables and configuration parameters")

    # Validate and set environment variables
    try:
        openai_api_key = os.getenv("OPENAI_API_KEY")
        google_application_credentials = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        tesseract_cmd = os.getenv("TESSERACT_CMD")

        if not openai_api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")

        if not google_application_credentials:
            raise ValueError(
                "GOOGLE_APPLICATION_CREDENTIALS environment variable not set"
            )

        if not tesseract_cmd:
            raise ValueError("TESSERACT_CMD environment variable not set")

        # Set pytesseract command
        pytesseract.pytesseract.tesseract_cmd = tesseract_cmd
        # Set openai api key
        openai.api_key = openai_api_key
        # Set Google application credentials
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = google_application_credentials

        config = {
            "openai_api_key": openai_api_key,
            "google_application_credentials": google_application_credentials,
            "tesseract_cmd": tesseract_cmd,
        }

        logging.info(
            "Environment variables and configuration parameters set successfully"
        )

        return config

    except ValueError as e:
        logging.error(e)
        return None

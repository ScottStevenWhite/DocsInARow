from dotenv import load_dotenv
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from src import text_processing


# Set up constants for use in tests
load_dotenv()

TEST_API_KEY = os.getenv("OPENAI_API_KEY")
TEST_IMAGE_PATH = os.path.join(".", "test_images", "test_image.jpg")


def test_extract_text():
    result = text_processing.extract_text(TEST_IMAGE_PATH)
    assert isinstance(result, str), "The function should return a string"


def test_detect_labels():
    result = text_processing.detect_labels(TEST_IMAGE_PATH)
    assert isinstance(result, list), "The function should return a list"


def test_correct_text():
    incorrect_text = "Thsi is a tset string. It cnotains typos."
    result = text_processing.correct_text(incorrect_text, TEST_API_KEY)
    assert isinstance(result, str), "The function should return a string"


def test_categorize_document():
    text = "This is a test string"
    result = text_processing.categorize_document(text, TEST_API_KEY)
    assert isinstance(result, str), "The function should return a string"


def test_generate_filename():
    text = "This is a test string"
    result = text_processing.generate_filename(text, TEST_API_KEY)
    assert isinstance(result, str), "The function should return a string"
    assert result.endswith(".jpg"), "The filename should end with .jpg"


def test_has_more_than_25_words():
    text_under_25 = "This is a test string"
    text_over_25 = "This is a test string " * 6
    assert not text_processing.has_more_than_25_words(
        text_under_25
    ), "Function should return False if less than 25 words"
    assert text_processing.has_more_than_25_words(
        text_over_25
    ), "Function should return True if more than 25 words"

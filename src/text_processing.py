import openai
import textwrap
import pytesseract
import re
from google.cloud import vision
import logging
from PIL import Image


def extract_text(image_path):
    """Extract text from image using Pytesseract"""
    try:
        return pytesseract.image_to_string(Image.open(image_path))
    except Exception as e:
        logging.error(f"Error extracting text from image {image_path}: {e}")
        return ""


def detect_labels(image_path):
    """Detect labels in the image using Google Vision"""
    try:
        client = vision.ImageAnnotatorClient()
        with open(image_path, "rb") as image_file:
            content = image_file.read()
        image = vision.Image(content=content)
        response = client.label_detection(image=image)
        return [label.description for label in response.label_annotations]
    except Exception as e:
        logging.error(f"Error detecting labels in image {image_path}: {e}")
        return []


def openai_completion(engine, prompt, temperature, max_tokens):
    """A helper function to perform OpenAI completions"""
    try:
        response = openai.Completion.create(
            engine=engine, prompt=prompt, temperature=temperature, max_tokens=max_tokens
        )
        return response.choices[0].text.strip()
    except Exception as e:
        logging.error(f"Error performing OpenAI completion: {e}")
        return ""


def correct_text(incorrect_text):
    """Correct text using OpenAI"""
    corrected_text = ""
    text_chunks = textwrap.wrap(incorrect_text, 2000)
    for chunk in text_chunks:
        prompt = (
            "Correct the following text and output only the corrected text with nothing else added: "
            + chunk
        )
        corrected_text += openai_completion("text-davinci-003", prompt, 0.5, 2000)
    return corrected_text


def categorize_document(text):
    """Categorize text using OpenAI"""
    prompt = f"The snippet is from a document. Please look at the snippet and output a one or two word category. Only output the category and nothing else. Snippet: {text[:2048]}"
    return openai_completion("text-davinci-003", prompt, 0.3, 250)


def generate_filename(text):
    """Generate a meaningful filename using OpenAI"""
    prompt = f"The following is a document snippet: {text[:2048]}. Please generate a meaningful filename for this document. It may be anywhere between one to five words, but words must be separated via underscores and all files should end with .jpg For example 2023_W2.jpg: "
    output = openai_completion("text-davinci-003", prompt, 0.3, 100)

    # Clean up the output
    filename = re.search(r"\b[\w_]+\.jpg\b", output)

    if filename is not None:
        # Extract the match
        filename = filename.group()
    else:
        # If no match, return a default filename
        filename = "default_filename.jpg"

    return filename


def has_more_than_25_words(string):
    """Check if string has more than 25 words"""
    return len(string.split()) > 25

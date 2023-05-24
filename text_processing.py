import os
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
    except (FileNotFoundError, IOError) as e:
        logging.error(f"Error reading image: {e}")
        return ""
    except pytesseract.TesseractError as e:
        logging.error(f"Error extracting text: {e}")
        return ""

def detect_labels(image_path):
    """Detect labels in the image using Google Vision"""
    client = vision.ImageAnnotatorClient()
    with open(image_path, 'rb') as image_file:
        content = image_file.read()
    image = vision.Image(content=content)
    response = client.label_detection(image=image)
    return [label.description for label in response.label_annotations]

def correct_text(incorrect_text, api_key):
    """Correct text using OpenAI"""
    openai.api_key = api_key
    corrected_text = ''
    text_chunks = textwrap.wrap(incorrect_text, 2000)
    for chunk in text_chunks:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt="Correct the following text and output only the corrected text with nothing else added: " + chunk,
            temperature=0.5,
            max_tokens=2000
        )
        corrected_text += response.choices[0].text.strip()
    return corrected_text

def categorize_document(text, api_key):
    """Categorize text using OpenAI"""
    openai.api_key = api_key
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"The snippet is from a document. Please look at the snippet and output a one or two word category. Only output the category and nothing else. Snippet: {text[:2048]}",
        temperature=0.3,
        max_tokens=250
    )
    return response.choices[0].text.strip()

def generate_filename(text, api_key):
    """Generate a meaningful filename using OpenAI"""
    openai.api_key = api_key
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"The following is a document snippet: {text[:2048]}. Please generate a meaningful filename for this document. It may be anywhere between one to five words, but words must be seperated via underscores and all files should end with .jpg For example 2023_W2.jpg: ",
        temperature=0.3,
        max_tokens=100
    )

    # Clean up the output
    output = response.choices[0].text.strip()

    # Search for the filename pattern in the output
    filename = re.search(r'\b[\w_]+\.jpg\b', output)

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

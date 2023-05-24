import os
import shutil
from datetime import datetime
from PIL import Image
import pytesseract
import openai
import json
import textwrap
import piexif
from google.cloud import vision
import logging
import argparse
import re
from dotenv import load_dotenv

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

def get_image_files(pictures_dir):
    """Get image files from the specified directory"""
    try:
        logging.info(f"Getting image files from {pictures_dir}")
        img_files = []
        for file in os.listdir(pictures_dir):
            if file.startswith("img"):
                img_files.append(os.path.join(pictures_dir, file))
        logging.info(f"Found {len(img_files)} image files")
        return img_files
    except FileNotFoundError as e:
        logging.error(f"Error reading directory: {e}")
        return []

def add_text_to_metadata(image_path, text):
    """Add text to the image metadata"""
    im = Image.open(image_path)
    if "exif" in im.info:
        exif_dict = piexif.load(im.info["exif"])
    else:
        exif_dict = {"0th": {}, "Exif": {}, "GPS": {}, "1st": {}}

    exif_dict["Exif"][piexif.ExifIFD.UserComment] = json.dumps(text).encode()
    exif_bytes = piexif.dump(exif_dict)
    im.save(image_path, exif=exif_bytes)

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

def move_file_to_date_dir(filename, base_dir='E:\\Documents\\by-year'):
    """Move file to date-specific directory in Documents"""
    
    # Get current date
    now = datetime.now()

    # Format date as Year/Month
    date_dir = os.path.join(base_dir, now.strftime('%Y\\%B'))

    # Create directory if it doesn't exist
    if not os.path.exists(date_dir):
        os.makedirs(date_dir)

    # Move the file to the new directory
    shutil.move(filename, date_dir)

    print(f"Moved {filename} to {date_dir}")


def has_more_than_25_words(string):
    """Check if string has more than 25 words"""
    return len(string.split()) > 25

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

def process_image_file(img_file, api_key, pictures_dir):
    """Process individual image file"""
    logging.info(f"Processing {img_file}")
    try:
        text = extract_text(img_file)
        if has_more_than_25_words(text):
            corrected_text = correct_text(text, api_key)
            print("------------------ Text after correction ------------------")
            print(corrected_text)
            add_text_to_metadata(img_file, corrected_text)
            print("------------------ Category ------------------")
            print(categorize_document(corrected_text, api_key))

            # Generate filename and rename the file
            new_filename = generate_filename(corrected_text, api_key)
            os.rename(img_file, os.path.join(pictures_dir, new_filename))
            print(f"Renamed {img_file} to {new_filename}")

            # Move the file to the appropriate date directory in Documents
            new_path = os.path.join(pictures_dir, new_filename)
            move_file_to_date_dir(new_path)

        else:
            print("Google Vision")
            labels = detect_labels(img_file)
            print(labels)
    except Exception as e:
        logging.error(f"Error processing {img_file}: {e}")

def main(skip_prompt=False):
    logging.info("Starting program")
    logging.basicConfig(level=logging.INFO)
    config = set_config()
    if config is None:
        return
    pictures_dir = config["pictures_dir"]
    img_files = get_image_files(pictures_dir)
    if not img_files:
        return
    for img_file in img_files:
        process_image_file(img_file, config["openai_api_key"], pictures_dir)
        # Ask user to continue or quit
        if not skip_prompt:
            user_input = input("Do you want to continue to the next image? (Y/N): ")
            if user_input.lower() != 'y':
                break
    logging.info("Finished processing all images")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='This is an image processing script that uses OpenAI and Google Vision to extract and correct text from images.')
    parser.add_argument("--skip_prompt", action='store_true', help="If set, the script will not prompt the user after processing each image.")
    args = parser.parse_args()
    main(skip_prompt=args.skip_prompt)

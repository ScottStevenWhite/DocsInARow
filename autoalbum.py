import os
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

def load_config():
    """Load configuration from JSON file"""
    with open('config.json') as config_file:
        return json.load(config_file)

def get_image_files(pictures_dir):
    """Get image files from the specified directory"""
    img_files = []
    for file in os.listdir(pictures_dir):
        if file.startswith("img"):
            img_files.append(os.path.join(pictures_dir, file))
    return img_files

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
    return pytesseract.image_to_string(Image.open(image_path))

def detect_labels(image_path):
    """Detect labels in the image using Google Vision"""
    client = vision.ImageAnnotatorClient()
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

def main(skip_prompt=False):
    logging.basicConfig(level=logging.INFO)
    config = load_config()

    # Set environment variables and configuration parameters
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = config["google_application_credentials"]
    openai.api_key = config["openai_api_key"]
    pytesseract.pytesseract.tesseract_cmd = config["tesseract_cmd"]
    pictures_dir = config["pictures_dir"]

    img_files = get_image_files(pictures_dir)

    for img_file in img_files:
        logging.info(f"Processing {img_file}")
        try:
            text = extract_text(img_file)
            if has_more_than_25_words(text):
                corrected_text = correct_text(text, openai.api_key)
                print("------------------ Text after correction ------------------")
                print(corrected_text)
                add_text_to_metadata(img_file, corrected_text)
                print("------------------ Category ------------------")
                print(categorize_document(corrected_text, openai.api_key))

                # Generate filename and rename the file
                new_filename = generate_filename(corrected_text, openai.api_key)
                os.rename(img_file, os.path.join(pictures_dir, new_filename))
                print(f"Renamed {img_file} to {new_filename}")

            else:
                print("Google Vision")
                labels = detect_labels(img_file)
                print (labels)

            # Ask user to continue or quit
            if not skip_prompt:
                user_input = input("Do you want to continue to the next image? (Y/N): ")
                if user_input.lower() != 'y':
                    break
        except Exception as e:
            logging.error(f"Error processing {img_file}: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--skip_prompt", action='store_true', help="Skip the user prompt after each image")
    args = parser.parse_args()
    main(skip_prompt=args.skip_prompt)

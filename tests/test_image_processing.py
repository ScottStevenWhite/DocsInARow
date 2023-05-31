import os
import json
from PIL import Image
import piexif
from datetime import datetime
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from src import image_processing

# Mock image file paths for testing
TEST_IMAGE_DIR = "test_images"
TEST_IMAGE_PATHS = [
    os.path.join(TEST_IMAGE_DIR, "test_image.jpg"),
]


def test_add_text_to_metadata(tmpdir):
    # Create a temporary image file for testing
    image_path = str(tmpdir.join("test_image.jpg"))
    Image.new("RGB", (100, 100), color="red").save(image_path)

    # Call the add_text_to_metadata function with the temporary image file
    text = "Test text"
    image_processing.add_text_to_metadata(image_path, text)

    # Open the modified image and extract the user comment from the metadata
    im = Image.open(image_path)
    exif_dict = piexif.load(im.info["exif"])
    user_comment = json.loads(exif_dict["Exif"][piexif.ExifIFD.UserComment].decode())

    # Check if the user comment matches the expected text
    assert user_comment == text

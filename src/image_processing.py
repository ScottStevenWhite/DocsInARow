import os
import json
import logging
from PIL import Image
import piexif

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


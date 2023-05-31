import json
import logging
import os

import piexif
from google.cloud import documentai_v1beta3 as documentai
from PIL import Image


def parse_form(project_id="YOUR_PROJECT_ID", file_path="path_to_your_file.pdf"):
    client = documentai.DocumentUnderstandingServiceClient()

    # Read the file into memory
    with open(file_path, "rb") as f:
        content = f.read()

    # mime_type can be application/pdf, image/tiff, and image/gif, or application/json
    input_config = documentai.types.InputConfig(
        content=content, mime_type="application/pdf"
    )

    # Improve form parsing results by providing key-value pair hints.
    # For each key hint, key is text that is likely to appear in the
    # document as a form field name (i.e. "DOB").
    # Value types are optional, but can be one or more of:
    # ADDRESS, LOCATION, ORGANIZATION, PERSON, PHONE_NUMBER, ID,
    # NUMBER, EMAIL, PRICE, TERMS, DATE, NAME
    key_value_pair_hints = [
        documentai.types.KeyValuePairHint(
            key="Emergency Contact", value_types=["NAME"]
        ),
        documentai.types.KeyValuePairHint(key="Referred By"),
    ]

    # Setting enabled=True enables form extraction
    form_extraction_params = documentai.types.FormExtractionParams(
        enabled=True, key_value_pair_hints=key_value_pair_hints
    )

    # Location can be 'us' or 'eu'
    parent = "projects/{}/locations/us".format(project_id)
    request = documentai.types.ProcessDocumentRequest(
        parent=parent,
        input_config=input_config,
        form_extraction_params=form_extraction_params,
    )

    document = client.process_document(request=request)

    def _get_text(el):
        """Doc AI identifies form fields by their offsets
        in document text. This function converts offsets
        to text snippets.
        """
        response = ""
        # If a text segment spans several lines, it will
        # be stored in different text segments.
        for segment in el.text_anchor.text_segments:
            start_index = segment.start_index
            end_index = segment.end_index
            response += document.text[start_index:end_index]
        return response

    for page in document.pages:
        print("Page number: {}".format(page.page_number))
        for form_field in page.form_fields:
            print(
                "Field Name: {}\tConfidence: {}".format(
                    _get_text(form_field.field_name), form_field.field_name.confidence
                )
            )
            print(
                "Field Value: {}\tConfidence: {}".format(
                    _get_text(form_field.field_value), form_field.field_value.confidence
                )
            )


def get_image_files(pictures_dir):
    """Get image files from the specified directory"""
    try:
        logging.info(f"Getting image files from {pictures_dir}")
        img_files = []
        for file in os.listdir(pictures_dir):
            # Temporarily, during early development, only process images that start with 'img'
            if file.lower().startswith("img") and file.lower().endswith(
                (".png", ".jpg", ".jpeg")
            ):
                img_files.append(os.path.join(pictures_dir, file))
        logging.info(f"Found {len(img_files)} image files")
        return img_files
    except FileNotFoundError as e:
        logging.error(f"Error reading directory: {e}")
        return []


def add_text_to_metadata(image_path, text):
    """Add text to the image metadata"""
    try:
        im = Image.open(image_path)
        if "exif" in im.info:
            exif_dict = piexif.load(im.info["exif"])
        else:
            exif_dict = {"0th": {}, "Exif": {}, "GPS": {}, "1st": {}}

        exif_dict["Exif"][piexif.ExifIFD.UserComment] = json.dumps(text).encode()
        exif_bytes = piexif.dump(exif_dict)
        im.save(image_path, exif=exif_bytes)
        logging.info(f"Added text to metadata of image: {image_path}")
    except Exception as e:
        logging.error(f"Error opening/processing image {image_path}: {e}")

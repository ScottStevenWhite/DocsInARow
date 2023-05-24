import os
import logging
import argparse
from config import set_config
from image_processing import get_image_files, add_text_to_metadata, move_file_to_date_dir
from text_processing import extract_text, has_more_than_25_words, correct_text, categorize_document, generate_filename, detect_labels

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

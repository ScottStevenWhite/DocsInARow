# AutoAlbum: A Document and Image Categorization Tool

AutoAlbum is a Python application for scanning and analyzing images or documents. The tool is designed to read and interpret the text contained in scanned documents and categorize the document type using the GPT-3 model provided by OpenAI. For images, it uses Google Vision to detect labels and categories. 

## Features

1. Text extraction from images using Optical Character Recognition (OCR) with Tesseract.
2. Text correction and formatting using OpenAI's GPT-3 model.
3. Document categorization using GPT-3.
4. Label detection in images using Google Vision.
5. Image metadata editing to include corrected text.

## Setup

1. Clone the repository or download the Python script.

2. Install necessary dependencies with pip:

    ```bash
    pip install PIL pytesseract openai google-cloud-vision textwrap piexif
    ```

3. Make sure to set up Tesseract-OCR on your system and update the path in the script:

    ```python
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    ```

4. Replace the OpenAI API key and Google Cloud Vision API key with your own in the script:

    ```python
    openai.api_key = 'your-openai-api-key'
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "your-google-cloud-vision-key.json"
    ```

5. Place your images in the `Pictures` directory, or change the `pictures_dir` variable to your preferred directory:

    ```python
    pictures_dir = "E:\\Pictures"
    ```

## Usage

Run the Python script. The script will go through each image in the directory. 

For each image:

- If the image contains more than 25 words, it's considered a document. The script extracts the text, corrects it using GPT-3, and prints out the corrected text. It also categorizes the document using GPT-3 and adds the corrected text to the image's metadata.
- If the image contains less than 25 words, it's considered a picture. The script uses Google Vision to detect labels and prints them out.

After each image, the script asks whether you want to continue to the next image. You can type 'Y' to continue or 'N' to stop the script.

## Notes

The tool uses the OpenAI's text-davinci-003 model, which has a maximum context length of 4096 tokens. This limit includes both the prompt text and the completion, so ensure your text to correct and categorize fits within this limit.

Please also be aware of the usage costs associated with the OpenAI API and Google Cloud Vision API.

## Contribution

Contributions are welcome! Please feel free to submit a Pull Request or open an Issue.

## License

AutoAlbum is open-source software licensed under the MIT license.

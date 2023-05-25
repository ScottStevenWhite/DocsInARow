from setuptools import setup, find_packages

setup(
    name="YourPackageName",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "openai",
        "Pillow",
        "pytesseract",
        "python-dotenv",
        "google-cloud-vision",
        "piexif",
        # add any other packages your project depends on
    ],
)

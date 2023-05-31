from datetime import datetime
import shutil
import ctypes
from ctypes import wintypes, windll
import os
import logging
from pathlib import Path


def get_windows_folder(CSIDL_FOLDER):
    SHGFP_TYPE_CURRENT = 0  # Get current path, not default path

    path = ctypes.create_unicode_buffer(wintypes.MAX_PATH)
    if windll.shell32.SHGetFolderPathW(
        None, CSIDL_FOLDER, None, SHGFP_TYPE_CURRENT, path
    ):
        raise RuntimeError(
            f"Unable to retrieve the folder path for CSIDL {CSIDL_FOLDER}"
        )

    return path.value


def get_windows_documents_folder():
    CSIDL_PERSONAL = 5  # My Documents
    return get_windows_folder(CSIDL_PERSONAL)


def get_windows_pictures_folder():
    CSIDL_MYPICTURES = 39  # My Pictures
    return get_windows_folder(CSIDL_MYPICTURES)


def move_file_to_date_dir(filename, base_dir=None):
    """Move file to date-specific directory in Documents"""

    # Get current date
    now = datetime.now()

    # Set default base directory depending on OS
    if base_dir is None:
        if os.name == "nt":
            # This is a Windows system
            base_dir = Path(get_windows_documents_folder(), "by-year")
        else:
            # This is a non-Windows system (Mac or Linux)
            base_dir = Path.home() / "Documents" / "by-year"

    # Create base directory (including 'by-year') if it doesn't exist
    base_dir.mkdir(parents=True, exist_ok=True)

    # Format date as Year/Month
    date_dir = base_dir / now.strftime("%Y/%B")

    # Create date directory if it doesn't exist
    date_dir.mkdir(parents=True, exist_ok=True)

    # Move the file to the new directory
    shutil.move(filename, date_dir)

    logging.info(f"Moved {filename} to {date_dir}")

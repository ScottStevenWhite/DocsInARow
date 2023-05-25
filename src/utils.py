from datetime import datetime
import shutil
import ctypes
from ctypes import wintypes, windll
import os

def get_windows_documents_folder():
    CSIDL_PERSONAL = 5       # My Documents
    SHGFP_TYPE_CURRENT = 0   # Get current path, not default path

    path = ctypes.create_unicode_buffer(wintypes.MAX_PATH)
    if windll.shell32.SHGetFolderPathW(None, CSIDL_PERSONAL, None, SHGFP_TYPE_CURRENT, path):
        raise RuntimeError("Unable to retrieve the documents folder path.")

    return path.value

def get_windows_pictures_folder():
    CSIDL_MYPICTURES = 39    # My Pictures
    SHGFP_TYPE_CURRENT = 0   # Get current path, not default path

    path = ctypes.create_unicode_buffer(wintypes.MAX_PATH)
    if windll.shell32.SHGetFolderPathW(None, CSIDL_MYPICTURES, None, SHGFP_TYPE_CURRENT, path):
        raise RuntimeError("Unable to retrieve the pictures folder path.")

    return path.value


def move_file_to_date_dir(filename, base_dir=None):
    """Move file to date-specific directory in Documents"""
    
    # Get current date
    now = datetime.now()

    # Set default base directory depending on OS
    if base_dir is None:
        if os.name == 'nt':
            # This is a Windows system
            base_dir = get_windows_documents_folder() + '\\by-year'
        else:
            # This is a non-Windows system (Mac or Linux)
            base_dir = os.path.expanduser('~/Documents/by-year')

    # Create base directory (including 'by-year') if it doesn't exist
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)

    # Format date as Year/Month
    date_dir = os.path.join(base_dir, now.strftime('%Y/%B'))

    # Create date directory if it doesn't exist
    if not os.path.exists(date_dir):
        os.makedirs(date_dir)

    # Move the file to the new directory
    shutil.move(filename, date_dir)

    print(f"Moved {filename} to {date_dir}")



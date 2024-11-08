import os
import shutil
import sys
from datetime import datetime

from PIL import Image
from PIL.ExifTags import TAGS


def get_date_from_exif(path):
    try:
        image = Image.open(path)
        info = image._getexif()
        if info:
            for tag, value in info.items():
                decoded = TAGS.get(tag, tag)
                if decoded == "DateTimeOriginal":
                    return datetime.strptime(value, "%Y:%m:%d %H:%M:%S")
    except Exception as e:
        print(f"Error getting date from EXIF data of {path}: {e}")
    return None


def get_date_from_filename(filename):
    try:
        # Extract the date part from the filename
        date_str = filename.split("_")[1]
        # Convert the date string to a datetime object
        return datetime.strptime(date_str, "%Y%m%d")
    except Exception as e:
        print(f"Error getting date from {filename}: {e}")
    return None


def organize_files(src_folder, dest_folder):
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)

    for root, dirs, files in os.walk(src_folder):
        for file in files:
            if file.lower().endswith((".jpg", ".jpeg", ".mp4")):
                src_path = os.path.join(root, file)
                date_taken = (
                    get_date_from_exif(src_path)
                    if file.lower().endswith((".jpg", ".jpeg"))
                    else None
                )
                if not date_taken:
                    date_taken = get_date_from_filename(file)
                date_folder = (
                    date_taken.strftime("%Y-%m-%d") if date_taken else "unknown_date"
                )

                dest_path = os.path.join(dest_folder, date_folder)
                if not os.path.exists(dest_path):
                    os.makedirs(dest_path)

                shutil.copy2(src_path, dest_path)
                print(f"Copied {src_path} to {dest_path}")


# Check if source and destination folder paths are provided as arguments
if len(sys.argv) == 3:
    src_folder = sys.argv[1]
    dest_folder = sys.argv[2]
else:
    # Prompt the user for source and destination folder paths
    src_folder = input("Enter the source folder path: ")
    dest_folder = input("Enter the destination folder path: ")

organize_files(src_folder, dest_folder)

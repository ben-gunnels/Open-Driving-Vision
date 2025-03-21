import zipfile
import os

def extract_zip(zip_path: str="masks_and_images.zip", extract_dir: str="dataset"):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)

    print("Extraction complete!")
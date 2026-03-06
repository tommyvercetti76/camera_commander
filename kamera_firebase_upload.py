"""
upload_kameras.py

A modular, scalable Python script to upload camera and lens JSON data to Google Firestore.

FUNCTIONALITY:
- Uploads camera and lens specifications into Firestore under the collection "Kameras".
- Supports multiple camera manufacturers (Canon, Nikon, etc.).
- Automatically creates or updates Firestore documents and fields.

REQUIREMENTS:
- firebase-admin SDK installed (`pip install firebase-admin`).
- Firebase service account JSON file for authentication (`firebase_sa.json`).
- JSON files structured appropriately for cameras and lenses.

USAGE:
- Adjust paths to your JSON and service account files in the CONFIGURATION section.
- Run via terminal with: `python3 upload_kameras.py`
"""

import json
import os
import firebase_admin
from firebase_admin import credentials, firestore


# ==== CONFIGURATION ====
SERVICE_ACCOUNT_FILE = '/Users/Rohan/Desktop/camera_project/kaaykostore-sa.json'
COLLECTION_NAME = 'Kameras'

# Dictionary containing manufacturer-specific JSON file paths.
MANUFACTURERS = {
    "sony": {
        "cameras_file": "/Users/Rohan/Desktop/camera_project/sony_cameras.json",
        "lenses_file": "/Users/Rohan/Desktop/camera_project/sony_lenses.json"
    },
    "canon": {
        "cameras_file": "/Users/Rohan/Desktop/camera_project/canon_cameras.json",
        "lenses_file": "/Users/Rohan/Desktop/camera_project/canon_lenses.json"
    }
    # Additional manufacturers (e.g., Nikon) can be added here.
}


# ==== FIREBASE INITIALIZATION ====
def init_firebase():
    if not firebase_admin._apps:
        cred = credentials.Certificate(SERVICE_ACCOUNT_FILE)
        firebase_admin.initialize_app(cred)
    return firestore.client()


# ==== HELPER FUNCTION: LOAD JSON ====
def load_json_safely(filepath, key_name):
    """
    Load JSON file and return data safely.

    Parameters:
        filepath (str): Path to the JSON file.
        key_name (str): Key to extract data from JSON if it's a dictionary.

    Returns:
        list: Parsed JSON data as a list.

    Raises:
        ValueError: If JSON format is incorrect or key is missing.
    """
    with open(filepath, 'r') as file:
        data = json.load(file)
        if isinstance(data, list):
            return data
        elif isinstance(data, dict) and key_name in data:
            return data[key_name]
        else:
            raise ValueError(
                f"Invalid format in '{filepath}'. Expecting a list or dictionary with key '{key_name}'.")


# ==== DATA UPLOAD FUNCTION ====
def upload_manufacturer_data(db, brand, camera_path, lens_path):
    """
    Upload cameras and lenses data for a given manufacturer to Firestore.

    Parameters:
        db (firestore.Client): Initialized Firestore client.
        brand (str): Manufacturer brand name (e.g., "canon").
        camera_path (str): File path to cameras JSON.
        lens_path (str): File path to lenses JSON.

    Returns:
        None
    """
    print(f"Uploading data for brand: {brand.upper()}...")

    # Validate file existence
    if not os.path.exists(camera_path) or not os.path.exists(lens_path):
        print(f"Missing JSON files for {brand}. Please verify file paths.")
        return

    try:
        # Load JSON data
        cameras = load_json_safely(camera_path, "cameras")
        lenses = load_json_safely(lens_path, "lenses")

        # Firestore document reference
        doc_ref = db.collection(COLLECTION_NAME).document(brand.lower())

        # Upload or update document
        doc_ref.set({
            "cameras": cameras,
            "lenses": lenses
        })

        print(f"Successfully uploaded {brand} data to Firestore.")
    except Exception as e:
        print(f"Error uploading data for {brand}: {e}")


# ==== MAIN ENTRYPOINT ====
def main():
    """Main entrypoint: initializes Firebase and uploads manufacturer data."""
    db = init_firebase()
    print("Connected to Firebase Firestore.")

    for brand, paths in MANUFACTURERS.items():
        upload_manufacturer_data(db, brand, paths['cameras_file'], paths['lenses_file'])

    print("Data upload process completed for all manufacturers.")


# Run script
if __name__ == '__main__':
    main()

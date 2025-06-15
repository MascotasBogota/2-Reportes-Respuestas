# src/services/image_service.py

import os
from src.controllers.upload_images_controller import validate_file, process_and_save_image

def handle_image_upload(file, user_id):
    is_valid, error = validate_file(file)
    if not is_valid:
        return False, error

    success, result = process_and_save_image(file, user_id)
    return success, os.path.basename(result)

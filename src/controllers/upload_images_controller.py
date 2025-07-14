# src/controllers/upload_images_controller.py

import os, uuid, logging, io
from PIL import Image
from werkzeug.utils import secure_filename
from supabase import create_client
from config import Config

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
MAX_IMAGE_SIZE = (800, 800)

# Initialize Supabase client
supabase = create_client(Config.SUPABASE_URL, Config.SUPABASE_KEY)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def validate_file(file):
    if not file:
        return False, "No se seleccionó ningún archivo"
    if file.filename == '':
        return False, "Nombre de archivo vacío"
    if not allowed_file(file.filename):
        return False, "Tipo de archivo no permitido"
    file.seek(0, os.SEEK_END)
    if file.tell() > MAX_FILE_SIZE:
        return False, "Archivo muy grande (máx 5MB)"
    file.seek(0)
    return True, None

def process_and_save_image(file, user_id):
    try:
        ext = file.filename.rsplit('.', 1)[1].lower()
        filename = secure_filename(f"{user_id}_{uuid.uuid4().hex[:8]}.{ext}")
        
        image = Image.open(file)

        # Convertir a RGB si es necesario
        if image.mode in ('RGBA', 'LA', 'P'):
            background = Image.new('RGB', image.size, (255, 255, 255))
            if image.mode == 'P':
                image = image.convert('RGBA')
            background.paste(image, mask=image.split()[-1] if image.mode == 'RGBA' else None)
            image = background

        # Redimensionar si es demasiado grande
        if image.size[0] > MAX_IMAGE_SIZE[0] or image.size[1] > MAX_IMAGE_SIZE[1]:
            image.thumbnail(MAX_IMAGE_SIZE, Image.Resampling.LANCZOS)

        # Guardar como JPEG en un buffer en memoria
        buffer = io.BytesIO()
        image.save(buffer, 'JPEG', quality=85, optimize=True)
        buffer.seek(0)

        # Subir la imagen a Supabase Storage
        storage_path = f"reports/{filename}"
        result = supabase.storage.from_(Config.SUPABASE_BUCKET).upload(
            storage_path,
            buffer.read(),
            {
                "content-type": "image/jpeg",
                "x-upsert": "true"  # Usar upsert para evitar conflictos
            }
        )
        
        # Obtener la URL pública de la imagen
        public_url = supabase.storage.from_(Config.SUPABASE_BUCKET).get_public_url(storage_path)
        
        return True, public_url

    except Exception as e:
        logging.error(f"Error subiendo imagen a Supabase: {e}")
        return False, f"Error interno al procesar la imagen {e}"

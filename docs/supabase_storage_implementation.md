# Migración a Supabase Storage

## Implementación de Supabase para almacenamiento de imágenes

Esta guía describe la implementación de Supabase Storage para el almacenamiento
de imágenes en la aplicación PatitasBog.

### Características

- Almacenamiento en la nube de Supabase
- URLs públicas para acceder a las imágenes
- Procesamiento de imágenes antes de la subida (redimensionamiento, conversión
  de formato)
- Validación de tipos de archivos y tamaño

### Configuración

Las variables de entorno necesarias para la conexión con Supabase son:

```
SUPABASE_URL=https://wyuefggkaclfafqumzyc.supabase.co
SUPABASE_KEY=sb_secret_3oZTk9WHnOfsWoTklU6sbw_NDxO7SsX
SUPABASE_BUCKET=petimages
```

Estas variables están configuradas por defecto en el archivo `config.py` pero
pueden ser sobrescritas mediante variables de entorno.

### API Endpoints

#### POST /api/images/upload

Este endpoint permite subir imágenes al almacenamiento de Supabase.

**Solicitud:**

- Método: POST
- Encabezados: Authorization: Bearer {token}
- Formulario: image (archivo)

**Respuesta exitosa:**

```json
{
  "success": true,
  "imageUrl": "https://wyuefggkaclfafqumzyc.supabase.co/storage/v1/object/public/petimages/reports/userid_abcdef12.jpg"
}
```

**Respuesta de error:**

```json
{
  "success": false,
  "error": "Mensaje de error"
}
```

### Manejo de imágenes existentes

Para migrar imágenes existentes en el almacenamiento local a Supabase Storage,
se recomienda usar el script `migrate_images_to_supabase.py` en la raíz del
proyecto.

### Requisitos

La implementación requiere la instalación de la biblioteca `supabase` de Python,
que se ha agregado al archivo `requirements.txt`.

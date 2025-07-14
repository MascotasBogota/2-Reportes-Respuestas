# Migración a Firebase Storage

Este documento explica la migración del sistema de almacenamiento de imágenes
desde almacenamiento local a Firebase Storage.

## Cambios realizados

1. Se agregó Firebase Admin SDK para gestionar la subida de imágenes
2. Se modificó el servicio de imágenes para utilizar Firebase Storage
3. Se eliminó la ruta de visualización local de imágenes
4. Las URLs de imágenes ahora son URLs completas de Firebase Storage
5. Se creó un script de migración para mover las imágenes existentes

## Instrucciones de configuración

### 1. Instalar las dependencias

```bash
pip install -r requirements.txt
```

### 2. Verificar el archivo .env

Asegúrate de que tu archivo `.env` contenga las siguientes variables:

```
FIREBASE_CREDENTIALS_PATH=patitasbog-storage-firebase-adminsdk-fbsvc-94d0507917.json
FIREBASE_STORAGE_BUCKET=patitasbog-storage.appspot.com
```

### 3. Migrar imágenes existentes (si aplica)

Para migrar las imágenes existentes del almacenamiento local a Firebase Storage,
sigue estos pasos:

1. Ejecutar el script en modo de prueba:
   ```bash
   python migrate_images.py --dry-run
   ```
2. Si todo parece correcto, ejecutar la migración real:
   ```bash
   python migrate_images.py
   ```

## Notas importantes

- Las imágenes ahora se almacenan en Firebase Storage en la siguiente
  estructura: `images/{user_id}/{unique_id}.{extension}`
- Las URLs devueltas por la API son URLs públicas completas que apuntan
  directamente a Firebase Storage

- Los endpoints de la API no han cambiado:

  - `POST /images/upload`: Subir una imagen (ahora a Firebase Storage)
  - El endpoint `GET /images/view/<filename>` ya no existe porque Firebase
    proporciona URLs públicas

- El campo `image` en las respuestas de la API ahora se llama `image_url` para
  mayor claridad

## Seguridad

- Las credenciales de Firebase se almacenan en un archivo JSON en la raíz del
  proyecto
- Este archivo NO debe subirse a repositorios públicos (está incluido en
  .gitignore)
- Las imágenes en Firebase Storage son públicas, pero con URLs impredecibles

## Soporte y solución de problemas

Si encuentras algún problema con la subida de imágenes o con Firebase Storage:

1. Verifica que Firebase esté correctamente inicializado en la aplicación
2. Comprueba que las credenciales de Firebase sean válidas
3. Verifica que el bucket de Firebase Storage exista y esté correctamente
   configurado
4. Revisa los logs del servidor para mensajes de error específicos

## Documentación adicional

- [Firebase Admin SDK para Python](https://firebase.google.com/docs/admin/setup)
- [Firebase Storage](https://firebase.google.com/docs/storage)

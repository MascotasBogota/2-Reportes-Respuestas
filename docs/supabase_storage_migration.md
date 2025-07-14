# Migración a Supabase Storage

Este documento explica la migración del sistema de almacenamiento de imágenes
desde almacenamiento local a Supabase Storage.

## Cambios realizados

1. Se agregó la librería Supabase para gestionar la subida de imágenes
2. Se modificó el servicio de imágenes para utilizar Supabase Storage
3. Se eliminó la ruta de visualización local de imágenes
4. Las URLs de imágenes ahora son URLs completas de Supabase Storage
5. Se creó un script de migración para mover las imágenes existentes

## Instrucciones de configuración

### 1. Instalar las dependencias

```bash
pip install -r requirements.txt
```

### 2. Verificar el archivo .env

Asegúrate de que tu archivo `.env` contenga las siguientes variables:

```
SUPABASE_URL=https://wyuefggkaclfafqumzyc.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Ind5dWVmZ2drYWNsZmFmcXVtenljIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTI1MjgxMTQsImV4cCI6MjA2ODEwNDExNH0.uYPVtc0ETbfRyfo54p2AXCMhSJr2E8pz_VUn3BpcmSY
SUPABASE_BUCKET=petimages
```

### 3. Migrar imágenes existentes (si aplica)

Para migrar las imágenes existentes del almacenamiento local a Supabase Storage,
sigue estos pasos:

1. Ejecutar el script en modo de prueba:
   ```bash
   python migrate_images_to_supabase.py --dry-run
   ```
2. Si todo parece correcto, ejecutar la migración real:
   ```bash
   python migrate_images_to_supabase.py
   ```

## Notas importantes

- Las imágenes ahora se almacenan en Supabase Storage en la siguiente
  estructura: `{user_id}/{unique_id}.{extension}`
- Las URLs devueltas por la API son URLs públicas completas que apuntan
  directamente a Supabase Storage

- Los endpoints de la API no han cambiado:

  - `POST /images/upload`: Subir una imagen (ahora a Supabase Storage)
  - El endpoint `GET /images/view/<filename>` ya no existe porque Supabase
    proporciona URLs públicas

- El campo `image_url` en las respuestas de la API contiene la URL pública de
  Supabase

## Seguridad

- La clave API de Supabase que usamos es la clave anónima (pública), pero las
  políticas de Supabase controlan quién puede subir/leer archivos
- Es recomendable revisar y configurar las políticas de acceso en Supabase
  Storage para limitar el acceso si es necesario
- Las imágenes en Supabase Storage son públicas, pero con URLs que incluyen
  identificadores únicos

## Configuración de Supabase

Para que el almacenamiento funcione correctamente, asegúrate de que el bucket
"petimages" esté configurado en Supabase con las políticas de acceso adecuadas:

1. Inicia sesión en [Supabase](https://app.supabase.com)
2. Selecciona tu proyecto
3. Ve a "Storage" en el menú lateral
4. Verifica que existe el bucket "petimages"
5. Ve a la pestaña "Policies" y asegúrate de que existan políticas para:
   - Permitir subida de archivos a usuarios autenticados
   - Permitir lectura pública de archivos

Aquí hay un ejemplo de políticas SQL que puedes aplicar:

```sql
-- Permitir subida de archivos a usuarios autenticados
CREATE POLICY "Allow authenticated uploads"
ON storage.objects
FOR INSERT
TO authenticated
WITH CHECK (true);

-- Permitir lectura pública de archivos
CREATE POLICY "Allow public read"
ON storage.objects
FOR SELECT
TO public
USING (true);
```

## Soporte y solución de problemas

Si encuentras algún problema con la subida de imágenes o con Supabase Storage:

1. Verifica que las credenciales de Supabase sean válidas
2. Comprueba que el bucket "petimages" exista en Supabase
3. Asegúrate de que las políticas de acceso estén correctamente configuradas
4. Revisa los logs del servidor para mensajes de error específicos

### Errores comunes

1. **403 Forbidden**: Revisa las políticas de acceso en Supabase
2. **404 Not Found**: Verifica que el bucket exista
3. **413 Payload Too Large**: La imagen es demasiado grande (el límite es 5MB)

## Documentación adicional

- [Documentación de Supabase Storage](https://supabase.com/docs/guides/storage)
- [Políticas de acceso en Supabase](https://supabase.com/docs/guides/storage/security/access-control)
- [Límites de Supabase](https://supabase.com/docs/guides/platform/limits)

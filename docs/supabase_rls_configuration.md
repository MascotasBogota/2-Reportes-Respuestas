# Configuración de Políticas de Seguridad en Supabase Storage

Este documento explica cómo configurar correctamente las políticas de seguridad
a nivel de fila (RLS) en Supabase Storage para permitir la carga de imágenes
desde la API de PatitasBog.

## Problema: Error 403 al subir imágenes

Si al subir imágenes a Supabase Storage recibes el siguiente error:

```
Error subiendo imagen a Supabase: {'statusCode': 403, 'error': Unauthorized, 'message': new row violates row-level security policy}
```

Significa que las políticas de seguridad (RLS) en Supabase están bloqueando la
operación de carga.

## Solución: Configurar políticas de seguridad adecuadas

### Opción 1: Configurar el bucket para acceso público (más simple)

1. Inicia sesión en tu [Dashboard de Supabase](https://app.supabase.com)
2. Selecciona tu proyecto
3. Ve a "Storage" en el menú lateral
4. Selecciona el bucket "petimages"
5. Ve a la pestaña "Policies"
6. Haz clic en "New Policy"
7. Selecciona "Create a policy from scratch"
8. Configura la política:
   - Policy name: `allow_public_uploads`
   - For bucket: `petimages`
   - Operations allowed: `INSERT, UPDATE, DELETE` (seleccionar las tres)
   - Policy definition: `true` (para permitir todas las operaciones)
9. Guarda la política

### Opción 2: Usar un token de servicio para la autenticación (más seguro)

En lugar de usar la clave secreta directamente, puedes crear un token de
servicio con permisos específicos:

1. En el Dashboard de Supabase, ve a "Settings" > "API"
2. En "Service Keys", crea una nueva clave con permisos para Storage
3. Actualiza la configuración de la aplicación para usar este token

```python
# En config.py
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY", "tu_service_key")
```

```python
# En upload_images_controller.py
from supabase import Client, create_client
from config import Config

# Usa el token de servicio en lugar de la clave secreta
supabase = create_client(Config.SUPABASE_URL, Config.SUPABASE_SERVICE_KEY)
```

### Opción 3: Configurar una política RLS específica para la API

Si quieres un control más granular, puedes configurar una política que permita
cargas solo desde tu aplicación:

1. En la sección de políticas del bucket, crea una nueva política
2. Configura la siguiente regla SQL para la operación INSERT:

```sql
(role() = 'authenticated') OR
(request.header('apikey') = '<tu_clave_anon>' AND
 request.method = 'POST')
```

Esto permitirá cargas solo desde usuarios autenticados o desde tu API cuando se
use la clave anónima correcta.

## Verificar la configuración

Después de configurar las políticas, intenta subir imágenes nuevamente. Si
sigues teniendo problemas:

1. Verifica los logs de Supabase para obtener más detalles sobre el error
2. Asegúrate de que la estructura de carpetas en el bucket coincida con la ruta
   que estás usando (`reports/`)
3. Verifica que estás usando la clave correcta y que tiene los permisos
   adecuados

Si configuraste correctamente las políticas, las operaciones de carga deberían
funcionar sin errores.

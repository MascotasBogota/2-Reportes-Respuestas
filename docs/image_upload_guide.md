# Guía para subir imágenes a la API

Esta guía explica cómo subir imágenes a través de la API de PatitasBog
utilizando el sistema de almacenamiento de Firebase Storage.

## Endpoint de subida

```
POST /images/upload
```

## Requisitos

- Autenticación mediante JWT (Bearer Token)
- La imagen debe enviarse como un archivo (multipart/form-data)
- Formatos permitidos: JPG, PNG, GIF
- Tamaño máximo: 5MB

## Cómo subir imágenes

### Usando Postman

1. **Configurar la solicitud**:

   - Método: POST
   - URL: `http://tu-servidor/images/upload`

2. **Configurar la autenticación**:

   - Tipo: Bearer Token
   - Token: `tu_jwt_token` (sin "Bearer " al principio, Postman lo añade
     automáticamente)

3. **Configurar el cuerpo de la petición**:

   - Selecciona: "form-data"
   - Añade un campo clave-valor:
     - Clave: `image`
     - Valor: Selecciona "File" y elige la imagen desde tu sistema de archivos

   ![Postman Form-Data](https://i.imgur.com/example1.png)

4. **Envía la solicitud**

   - Haz clic en "Send" para enviar la solicitud

5. **Respuesta exitosa**:
   ```json
   {
     "success": true,
     "image_url": "https://storage.googleapis.com/patitasbog-storage.appspot.com/images/user123/abc123def456.jpg"
   }
   ```

### Usando cURL

```bash
curl -X POST "http://tu-servidor/images/upload" \
  -H "Authorization: Bearer tu_jwt_token" \
  -F "image=@/ruta/a/tu/imagen.jpg"
```

### Usando Swagger UI

1. Accede a la documentación Swagger en `http://tu-servidor/`
2. Navega hasta el endpoint `/images/upload`
3. Haz clic en el botón "Try it out"
4. En el campo Authorize, ingresa tu token JWT con el formato "Bearer
   tu_jwt_token"
5. Sube tu imagen usando el selector de archivos para el parámetro `image`
6. Haz clic en "Execute"

## Usando la URL de la imagen

Una vez que hayas subido la imagen con éxito, recibirás una URL completa que
apunta directamente a la imagen en Firebase Storage. Esta URL es pública y se
puede utilizar directamente en:

- Navegadores web
- Etiquetas HTML `<img>`
- Aplicaciones móviles
- Cualquier otro cliente que pueda mostrar imágenes desde URLs

Ejemplo:

```html
<img
  src="https://storage.googleapis.com/patitasbog-storage.appspot.com/images/user123/abc123def456.jpg"
  alt="Imagen de mascota" />
```

## Consideraciones adicionales

- Las imágenes se optimizan automáticamente antes de subirse (tamaño y
  compresión)
- Si necesitas reemplazar una imagen, simplemente sube una nueva; no hay forma
  de sobrescribir la anterior
- Firebase Storage tiene límites de almacenamiento y transferencia; asegúrate de
  no excederlos para evitar cargos adicionales

## Solución de problemas comunes

1. **Error 400: "No se envió ningún archivo"**

   - Verifica que estás enviando la imagen con la clave `image`
   - Asegúrate de que el formulario sea `multipart/form-data`

2. **Error 401: "Token inválido"**

   - Tu token JWT ha expirado o es inválido
   - Asegúrate de incluir "Bearer " antes del token (a menos que uses Postman en
     modo Bearer Token)

3. **Error "Tipo de archivo no permitido"**

   - Solo se permiten archivos JPG, PNG y GIF
   - Verifica la extensión y el tipo MIME del archivo

4. **Error "Archivo muy grande"**
   - El límite es de 5MB
   - Reduce el tamaño de la imagen antes de subirla

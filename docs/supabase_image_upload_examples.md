# Ejemplos de código para subir imágenes a Supabase Storage

Este documento contiene ejemplos de código para subir imágenes a la API de
PatitasBog desde diferentes plataformas y lenguajes.

> **Actualización**: La API ahora utiliza Supabase Storage para almacenar las
> imágenes y devuelve URLs públicas directamente.

## JavaScript (Fetch API)

```javascript
// Función para subir una imagen usando Fetch API
async function uploadImage(imageFile, authToken) {
  // Crear un FormData y añadir la imagen
  const formData = new FormData();
  formData.append("image", imageFile);

  try {
    // Hacer la petición
    const response = await fetch("http://tu-servidor/images/upload", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${authToken}`,
      },
      body: formData,
    });

    // Procesar la respuesta
    const data = await response.json();
    if (response.ok) {
      console.log("Imagen subida con éxito. URL:", data.image_url);
      return data.image_url;
    } else {
      console.error("Error al subir la imagen:", data.error);
      throw new Error(data.error);
    }
  } catch (error) {
    console.error("Error en la petición:", error);
    throw error;
  }
}

// Ejemplo de uso:
// En un formulario HTML con un input de tipo "file" con id "imageInput"
document
  .getElementById("uploadForm")
  .addEventListener("submit", async (event) => {
    event.preventDefault();

    const imageFile = document.getElementById("imageInput").files[0];
    const authToken = "tu_jwt_token"; // Obtenido durante el login

    try {
      const imageUrl = await uploadImage(imageFile, authToken);
      // Hacer algo con la URL de la imagen
      document.getElementById("imagePreview").src = imageUrl;
    } catch (error) {
      alert("Error al subir la imagen: " + error.message);
    }
  });
```

## Python (Requests)

```python
import requests

def upload_image(image_file_path, auth_token, api_url='http://tu-servidor/images/upload'):
    """
    Sube una imagen a la API de PatitasBog

    Args:
        image_file_path (str): Ruta al archivo de imagen
        auth_token (str): Token JWT para autenticación
        api_url (str): URL del endpoint de subida de imágenes

    Returns:
        str: URL de la imagen subida
    """
    headers = {
        'Authorization': f'Bearer {auth_token}'
    }

    with open(image_file_path, 'rb') as image_file:
        files = {'image': image_file}
        response = requests.post(api_url, headers=headers, files=files)

    if response.status_code == 200:
        data = response.json()
        print(f"Imagen subida con éxito. URL: {data['image_url']}")
        return data['image_url']
    else:
        try:
            error_msg = response.json().get('error', 'Error desconocido')
        except:
            error_msg = f"HTTP Error {response.status_code}"

        print(f"Error al subir la imagen: {error_msg}")
        raise Exception(error_msg)

# Ejemplo de uso:
try:
    image_url = upload_image(
        image_file_path='ruta/a/tu/imagen.jpg',
        auth_token='tu_jwt_token'
    )
    # Hacer algo con la URL de la imagen
except Exception as e:
    print(f"No se pudo subir la imagen: {e}")
```

## React / React Native

```jsx
import React, { useState } from "react";
import { Button, Image, View, Text, StyleSheet, Alert } from "react-native";
import * as ImagePicker from "expo-image-picker";

export default function ImageUploader({ authToken }) {
  const [image, setImage] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [uploadedImageUrl, setUploadedImageUrl] = useState(null);

  const pickImage = async () => {
    // Solicitar permiso para acceder a la galería
    const permissionResult =
      await ImagePicker.requestMediaLibraryPermissionsAsync();

    if (permissionResult.granted === false) {
      Alert.alert("Se requiere permiso para acceder a la galería");
      return;
    }

    const result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.Images,
      allowsEditing: true,
      aspect: [4, 3],
      quality: 0.8,
    });

    if (!result.cancelled && result.assets && result.assets[0]) {
      setImage(result.assets[0].uri);
    }
  };

  const uploadImage = async () => {
    if (!image) {
      Alert.alert("Por favor selecciona una imagen primero");
      return;
    }

    setUploading(true);

    try {
      // Crear FormData
      const formData = new FormData();

      // Añadir la imagen
      formData.append("image", {
        uri: image,
        type: "image/jpeg", // O el tipo correspondiente
        name: "upload.jpg",
      });

      // Realizar la petición
      const response = await fetch("http://tu-servidor/images/upload", {
        method: "POST",
        headers: {
          Authorization: `Bearer ${authToken}`,
          "Content-Type": "multipart/form-data",
        },
        body: formData,
      });

      const data = await response.json();

      if (response.ok) {
        setUploadedImageUrl(data.image_url);
        Alert.alert("Éxito", "Imagen subida correctamente");
      } else {
        Alert.alert("Error", data.error || "Error al subir la imagen");
      }
    } catch (error) {
      Alert.alert(
        "Error",
        error.message || "Error al conectar con el servidor"
      );
      console.error(error);
    } finally {
      setUploading(false);
    }
  };

  return (
    <View style={styles.container}>
      <Button title="Seleccionar Imagen" onPress={pickImage} />

      {image && (
        <View style={styles.imageContainer}>
          <Image source={{ uri: image }} style={styles.image} />
          <Button
            title={uploading ? "Subiendo..." : "Subir Imagen"}
            onPress={uploadImage}
            disabled={uploading}
          />
        </View>
      )}

      {uploadedImageUrl && (
        <View style={styles.resultContainer}>
          <Text style={styles.successText}>Imagen subida con éxito:</Text>
          <Image
            source={{ uri: uploadedImageUrl }}
            style={styles.resultImage}
          />
          <Text selectable>{uploadedImageUrl}</Text>
        </View>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    alignItems: "center",
  },
  imageContainer: {
    marginTop: 20,
    alignItems: "center",
  },
  image: {
    width: 300,
    height: 300,
    marginBottom: 10,
  },
  resultContainer: {
    marginTop: 20,
    alignItems: "center",
  },
  resultImage: {
    width: 150,
    height: 150,
    marginVertical: 10,
  },
  successText: {
    color: "green",
    fontSize: 16,
    fontWeight: "bold",
  },
});
```

## Angular (TypeScript)

```typescript
import { Component } from "@angular/core";
import { HttpClient, HttpHeaders } from "@angular/common/http";

@Component({
  selector: "app-image-uploader",
  template: `
    <div class="uploader">
      <h2>Subir Imagen</h2>

      <input type="file" (change)="onFileSelected($event)" accept="image/*" />

      <div *ngIf="selectedFile" class="preview">
        <img [src]="previewUrl" alt="Vista previa" />
        <button (click)="onUpload()" [disabled]="uploading">
          {{ uploading ? "Subiendo..." : "Subir Imagen" }}
        </button>
      </div>

      <div *ngIf="uploadedImageUrl" class="result">
        <h3>Imagen subida con éxito!</h3>
        <img [src]="uploadedImageUrl" alt="Imagen subida" />
        <p>URL: {{ uploadedImageUrl }}</p>
      </div>

      <div *ngIf="errorMessage" class="error">
        {{ errorMessage }}
      </div>
    </div>
  `,
  styles: [
    `
      .uploader {
        max-width: 500px;
        margin: 0 auto;
      }
      .preview {
        margin: 20px 0;
      }
      .preview img {
        max-width: 100%;
        max-height: 300px;
      }
      .result {
        margin-top: 20px;
        padding: 10px;
        background: #f0f0f0;
      }
      .result img {
        max-width: 200px;
        max-height: 200px;
      }
      .error {
        color: red;
        margin-top: 10px;
      }
    `,
  ],
})
export class ImageUploaderComponent {
  selectedFile: File | null = null;
  previewUrl: string | null = null;
  uploading = false;
  uploadedImageUrl: string | null = null;
  errorMessage: string | null = null;

  constructor(private http: HttpClient) {}

  onFileSelected(event: Event): void {
    const input = event.target as HTMLInputElement;

    if (input.files && input.files.length > 0) {
      this.selectedFile = input.files[0];

      // Crear una vista previa
      const reader = new FileReader();
      reader.onload = () => {
        this.previewUrl = reader.result as string;
      };
      reader.readAsDataURL(this.selectedFile);

      // Limpiar mensajes anteriores
      this.errorMessage = null;
      this.uploadedImageUrl = null;
    }
  }

  onUpload(): void {
    if (!this.selectedFile) {
      this.errorMessage = "Por favor selecciona una imagen primero";
      return;
    }

    this.uploading = true;
    this.errorMessage = null;

    // Crear FormData
    const formData = new FormData();
    formData.append("image", this.selectedFile);

    // Obtener el token de autenticación (esto dependerá de tu implementación)
    const authToken = "tu_jwt_token"; // Ejemplo

    // Configurar las cabeceras
    const headers = new HttpHeaders({
      Authorization: `Bearer ${authToken}`,
    });

    // Realizar la solicitud
    this.http
      .post<any>("http://tu-servidor/images/upload", formData, { headers })
      .subscribe({
        next: (response) => {
          this.uploadedImageUrl = response.image_url;
          this.uploading = false;
        },
        error: (error) => {
          this.errorMessage = error.error?.error || "Error al subir la imagen";
          this.uploading = false;
        },
      });
  }
}
```

## Implementación del Servidor (Python)

Esta sección muestra la implementación del servidor con Supabase Storage:

```python
# Ejemplo simplificado de la implementación del servidor
import io, uuid
from PIL import Image
from supabase import create_client
from config import Config

# Inicializar cliente de Supabase
supabase = create_client(Config.SUPABASE_URL, Config.SUPABASE_KEY)

def process_and_save_image(file, user_id):
    """
    Procesa y guarda una imagen en Supabase Storage

    Args:
        file: Archivo de imagen (objeto FileStorage de Flask)
        user_id: ID del usuario que sube la imagen

    Returns:
        tuple: (success, result) donde result es la URL pública o un mensaje de error
    """
    try:
        # Generar nombre único para el archivo
        ext = file.filename.rsplit('.', 1)[1].lower()
        filename = f"{user_id}_{uuid.uuid4().hex[:8]}.{ext}"

        # Procesar imagen con PIL
        image = Image.open(file)

        # Convertir a RGB si es necesario
        if image.mode in ('RGBA', 'LA', 'P'):
            background = Image.new('RGB', image.size, (255, 255, 255))
            if image.mode == 'P':
                image = image.convert('RGBA')
            background.paste(image, mask=image.split()[-1] if image.mode == 'RGBA' else None)
            image = background

        # Guardar como JPEG en un buffer en memoria
        buffer = io.BytesIO()
        image.save(buffer, 'JPEG', quality=85, optimize=True)
        buffer.seek(0)

        # Subir a Supabase Storage
        storage_path = f"reports/{filename}"
        supabase.storage.from_(Config.SUPABASE_BUCKET).upload(
            storage_path,
            buffer.read(),
            {"content-type": "image/jpeg"}
        )

        # Obtener URL pública
        public_url = supabase.storage.from_(Config.SUPABASE_BUCKET).get_public_url(storage_path)
        return True, public_url

    except Exception as e:
        return False, f"Error al procesar la imagen: {str(e)}"
```

### Respuesta del API

La respuesta del endpoint de subida de imágenes ahora incluye la URL pública
completa:

```json
{
  "success": true,
  "imageUrl": "https://wyuefggkaclfafqumzyc.supabase.co/storage/v1/object/public/petimages/reports/user123_abcdef12.jpg"
}
```

# Ejemplos de código para subir imágenes a la API

Este documento contiene ejemplos de código para subir imágenes a la API de
PatitasBog desde diferentes plataformas y lenguajes.

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

## React Native

```javascript
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

## Swift (iOS)

```swift
import UIKit

class ImageUploadService {

    static let shared = ImageUploadService()
    private let apiUrl = "http://tu-servidor/images/upload"

    func uploadImage(image: UIImage, authToken: String, completion: @escaping (Result<String, Error>) -> Void) {
        // Convertir la imagen a datos
        guard let imageData = image.jpegData(compressionQuality: 0.7) else {
            completion(.failure(NSError(domain: "ImageUploader", code: 0, userInfo: [NSLocalizedDescriptionKey: "No se pudo convertir la imagen"])))
            return
        }

        // Crear la URL
        guard let url = URL(string: apiUrl) else {
            completion(.failure(NSError(domain: "ImageUploader", code: 0, userInfo: [NSLocalizedDescriptionKey: "URL inválida"])))
            return
        }

        // Crear la solicitud
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("Bearer \(authToken)", forHTTPHeaderField: "Authorization")

        // Crear un límite único para multipart/form-data
        let boundary = UUID().uuidString
        request.setValue("multipart/form-data; boundary=\(boundary)", forHTTPHeaderField: "Content-Type")

        // Crear el cuerpo multipart
        var body = Data()

        // Añadir la imagen al cuerpo
        body.append("--\(boundary)\r\n".data(using: .utf8)!)
        body.append("Content-Disposition: form-data; name=\"image\"; filename=\"image.jpg\"\r\n".data(using: .utf8)!)
        body.append("Content-Type: image/jpeg\r\n\r\n".data(using: .utf8)!)
        body.append(imageData)
        body.append("\r\n".data(using: .utf8)!)
        body.append("--\(boundary)--\r\n".data(using: .utf8)!)

        // Asignar el cuerpo a la solicitud
        request.httpBody = body

        // Crear la tarea de la sesión
        let task = URLSession.shared.dataTask(with: request) { data, response, error in
            if let error = error {
                DispatchQueue.main.async {
                    completion(.failure(error))
                }
                return
            }

            guard let data = data else {
                DispatchQueue.main.async {
                    completion(.failure(NSError(domain: "ImageUploader", code: 0, userInfo: [NSLocalizedDescriptionKey: "No se recibieron datos"])))
                }
                return
            }

            // Decodificar la respuesta
            do {
                if let json = try JSONSerialization.jsonObject(with: data) as? [String: Any],
                   let success = json["success"] as? Bool,
                   success,
                   let imageUrl = json["image_url"] as? String {
                    DispatchQueue.main.async {
                        completion(.success(imageUrl))
                    }
                } else {
                    let errorMessage = try JSONSerialization.jsonObject(with: data) as? [String: Any]
                    let message = (errorMessage?["error"] as? String) ?? "Error desconocido"
                    DispatchQueue.main.async {
                        completion(.failure(NSError(domain: "ImageUploader", code: 0, userInfo: [NSLocalizedDescriptionKey: message])))
                    }
                }
            } catch {
                DispatchQueue.main.async {
                    completion(.failure(error))
                }
            }
        }

        // Iniciar la tarea
        task.resume()
    }
}

// Ejemplo de uso:
class ImageUploadViewController: UIViewController, UIImagePickerControllerDelegate, UINavigationControllerDelegate {

    @IBOutlet weak var imageView: UIImageView!
    @IBOutlet weak var uploadButton: UIButton!
    @IBOutlet weak var activityIndicator: UIActivityIndicatorView!

    override func viewDidLoad() {
        super.viewDidLoad()
        activityIndicator.isHidden = true
    }

    @IBAction func pickImage(_ sender: Any) {
        let picker = UIImagePickerController()
        picker.delegate = self
        picker.sourceType = .photoLibrary
        picker.allowsEditing = true
        present(picker, animated: true)
    }

    @IBAction func uploadImage(_ sender: Any) {
        guard let image = imageView.image else {
            showAlert(message: "Por favor selecciona una imagen primero")
            return
        }

        // Mostrar indicador de carga
        activityIndicator.isHidden = false
        activityIndicator.startAnimating()
        uploadButton.isEnabled = false

        // Ejemplo de token (en una app real obtendrías esto de tu sistema de autenticación)
        let authToken = "tu_jwt_token"

        // Subir la imagen
        ImageUploadService.shared.uploadImage(image: image, authToken: authToken) { [weak self] result in
            guard let self = self else { return }

            // Ocultar indicador de carga
            self.activityIndicator.stopAnimating()
            self.activityIndicator.isHidden = true
            self.uploadButton.isEnabled = true

            switch result {
            case .success(let imageUrl):
                self.showAlert(message: "Imagen subida con éxito")
                print("URL de la imagen: \(imageUrl)")

            case .failure(let error):
                self.showAlert(message: "Error: \(error.localizedDescription)")
            }
        }
    }

    func imagePickerController(_ picker: UIImagePickerController, didFinishPickingMediaWithInfo info: [UIImagePickerController.InfoKey : Any]) {
        if let editedImage = info[.editedImage] as? UIImage {
            imageView.image = editedImage
        } else if let originalImage = info[.originalImage] as? UIImage {
            imageView.image = originalImage
        }

        dismiss(animated: true)
    }

    func showAlert(message: String) {
        let alert = UIAlertController(title: nil, message: message, preferredStyle: .alert)
        alert.addAction(UIAlertAction(title: "OK", style: .default))
        present(alert, animated: true)
    }
}
```

Estos ejemplos pueden servir como guía para implementar la subida de imágenes en
diferentes plataformas y lenguajes. Asegúrate de adaptar las URLs y los métodos
de autenticación según las necesidades específicas de tu aplicación.

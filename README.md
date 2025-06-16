# 🐾 Módulo 2: Reportes y Respuestas – API de PatitasBog

Este módulo proporciona los endpoints necesarios para crear, consultar y gestionar reportes de mascotas perdidas, así como registrar interacciones (respuestas de avistamiento o hallazgo) por parte de la comunidad. Forma parte del sistema **PatitasBog**, una plataforma colaborativa para ayudar a reunir mascotas con sus familias.

---

## Tabla de contenidos

- [Objetivo del módulo](#objetivo-del-módulo)
- [Requisitos Previos](#requisitos-previos)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Setup](#setup-del-entorno)
- [Documentación de Endpoints](#endpoints-principales-y-contratos)

---

## Requisitos Previos

- Python 3.9+
- MongoDB Atlas (cluster creado)
- pip

---

## 🧠 Objetivo del Módulo

El módulo está dividido en dos submódulos:

* **2.1 Reportes de mascotas perdidas**: Permite a usuarios registrar y gestionar reportes de mascotas extraviadas.
* **2.2 Interacción y comunicación en reportes**: Facilita la colaboración entre usuarios a través de respuestas con información relevante (avistamientos o hallazgos), además de permitir filtros por tipo de mascota y geolocalización.

---

## 📁 Estructura del Proyecto

El diseño sigue el patrón **SOFEA** (Services-Oriented Front-End Architecture):

```
src/
🔺 controllers/     # Lógica que conecta rutas con servicios
🔺 models/          # Esquemas de MongoDB (Report, Response)
🔺 routes/          # Endpoints REST (Flask-RESTx)
🔺 services/        # Lógica de negocio
🔺 utils/           # Autenticación, serialización, validaciones
tests/
🔺 TBD
uploads/
🔺 report_images/   # Ruta para guardar imagenes localmente (solución temporal) 
app.py
config.py
docker-compose.yml
Dockerfile
README.md
requirements.txt
```

---

## 🚀 Setup del Entorno

### 1. Clonar repositorio

```bash
git clone https://github.com/MascotasBogota/2-Reportes-Respuestas.git
cd 2-Reportes-Respuestas
```

### 2. Crear y activar entorno virtual

```bash
python -m venv venv
.\venv\Scripts\activate   # Windows
```

⚠️ Cambia el intérprete de VSCode a `.venv/Scripts/python.exe`.

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar archivo `.env`

Crea un archivo `.env` con la siguiente estructura:

```
FLASK_APP=app.py
FLASK_ENV=development
MONGO_URI=mongodb+srv://<user>:<pass>@reportes-respuestas.mongodb.net
JWT_PUBLIC_KEY="-----BEGIN PUBLIC KEY-----\nMIIBI...\n-----END PUBLIC KEY-----"
DEV_MODE=True
```

### 5. Ejecutar la app

```bash
python app.py
```

---

## 🐋 Uso con Docker

Si prefieres contenedores:

```bash
docker compose up
```

> Esto evita problemas de dependencias cruzadas entre equipos.

---

## 🔐 Autenticación

La mayoría de endpoints requieren un token JWT.

* En **producción**, el token JWT lo almacena y es usado por el front-end tras el login.
* Para **pruebas** o desarrollo, puedes obtener un token usando la API de login de otro equipo (consultar documentación compartida por el equipo de Autenticación).

Incluye el token en las peticiones usando el encabezado:

```http
Authorization: Bearer <token>
```

---

## 📌 Endpoints Principales y Contratos

La siguiente sección contiene la documentación completa de todos los endpoints del módulo 2, incluyendo descripción, parámetros, ejemplos de request y posibles respuestas.

## 📊 Documentación Swagger
Esta API también cuenta con una documentación interactiva generada automáticamente gracias a Flask-RESTX. Puedes acceder a ella ejecutando la app y visitando:

```bash
http://localhost:5050/
```

Desde ahí puedes:

* Ver todos los endpoints disponibles

* Probar llamadas a la API

* Revisar parámetros, estructuras y posibles errores

* Compartir fácilmente con nuevos miembros del equipo

---

## 📄 Documentación de Endpoints (Contratos)

Esto es una guía y es importante notar que las respuestas y código de errores pueden ser vistos en la documentación Swagger.

### 3.1 Reportes de mascotas perdidas

#### 3.1.1 Listar reportes

* **Ruta:** `GET /reports/public`
* **Descripción:** Devuelve reportes filtrados por tipo o ubicación.
* **Parámetros URL:** `type`, `lat`, `lng`, `radius`

**Response 200 OK:**

```json
{
  "reports": [
    {
      "id": "...",
      "type": "perro",
      "description": "...",
      "location": { "type": "Point", "coordinates": [-74.08, 4.6] },
      "images": ["https://..."],
      "status": "open",
      "created_at": "..."
    }
  ]
}
```

**Errores:** `400`, `500`

---

#### 3.1.2 Crear nuevo reporte

* **Ruta:** `POST /reports`
* **Headers:** `Authorization: Bearer <token>`
* **Body:**

```json
{
  "type": "perro",
  "description": "...",
  "location": { "type": "Point", "coordinates": [-74.08, 4.6] },
  "images": ["data:image/jpeg;base64,..."]
}
```

**Response 201 Created:** objeto con `id`, `status`, `created_at`, etc.

**Errores:** `400`, `401`, `500`

---

#### 3.1.3 Obtener detalle de un reporte

* **Ruta:** `GET /reports/{report_id}`
* **Response 200 OK:** datos del reporte y respuestas relacionadas.
* **Errores:** `404`, `500`

---

#### 3.1.4 Actualizar reporte

* **Ruta:** `PUT /reports/public/{report_id}`
* **Headers:** `Authorization: Bearer <token>`
* **Body:** campos editables + `images_to_add`, `images_to_remove`

**Response 200 OK:** datos actualizados
**Errores:** `401`, `500`

---

#### 3.1.5 Eliminar reporte

* **Ruta:** `DELETE /reports/{report_id}`
* **Headers:** `Authorization: Bearer <token>`

**Response 204 OK:** reporte eliminado

**Errores:** `401`, `500`

---

#### 3.1.6 Cerrar reporte

* **Ruta:** `POST /reports/{report_id}/close`
* **Headers:** `Authorization: Bearer <token>`

**Response 200 OK:**

```json
{ "id": "...", "status": "closed", "closed_at": "..." }
```

**Errores:** `401`, `500`

---

### 3.2 Respuestas en reportes

#### 3.2.1 Listar respuestas

* **Ruta:** `GET /responses/{report_id}/allResponses`
* **Response 200 OK:**

```json
{
  "report_id": "...",
  "responses": [
    { "id": "...", "type": "avistamiento", "comment": "..." }
  ]
}
```

**Errores:** `404`, `500`

---

#### 3.2.2 Obtener detalle de una respuesta

* **Ruta:** `POST /responses/{report_id}/{response_id}`
* **Response 200 OK:**

```json
{
  "type": "avistamiento",
  "comment": "...",
  "location": { "type": "Point", "coordinates": [-74.03, 4.67] }
}
```

**Response 200 OK:**

**Errores:**  `404`, `500`

---

#### 3.2.3 Crear respuesta

* **Ruta:** `POST /responses/{report_id}`
* **Headers:** `Authorization: Bearer <token>`
* **Body:**

```json
{
  "type": "avistamiento",
  "comment": "...",
  "location": { "type": "Point", "coordinates": [-74.03, 4.67] }
}
```

**Response 201 Created:** objeto `response`

**Errores:** `400`, `401`, `403`, `404`, `500`

---

#### 3.2.4 Actualizar respuesta

* **Ruta:** `POST /responses/{report_id}/{response_id}/put`
* **Headers:** `Authorization: Bearer <token>`
* **Body:**

```json
{
  "type": "avistamiento",
  "comment": "...",
  "location": { "type": "Point", "coordinates": [-74.03, 4.67] }
}
```

**Response 201 Created:** objeto `response`

**Errores:** `400`, `401`, `403`, `404`, `500`

---

#### 3.2.5 Eliminar respuesta

* **Ruta:** `POST /responses/{report_id}/{response_id}/delete`
* **Headers:** `Authorization: Bearer <token>`

**Response 201 Created:** objeto `response`

**Errores:** `400`, `401`, `403`, `404`, `500`

---

### 3.3 Filtro de reportes

#### 3.3.1 GET /reports/filter

* Igual a `/reports` pero requiere al menos un parámetro de filtro.
* **Errores:** `400` si no hay filtros, `500` error interno

---

### 3.4 Imágenes

#### 3.4.1 Subir imagen

* **Ruta:** `POST /images/upload`
* **Headers:** `Authorization: Bearer <token>`

**Response 200 OK:** 

**Errores:** `400`, `401`, `403`, `404`, `500`

---
#### 3.4.2 Obtener imagen 

* **Ruta:** `POST /images/view/{filename}`
* **Headers:** `Authorization: Bearer <token>`
* **Body:**

```json
{
  "filename": "filename.jpg"
}
```

**Response 200 OK:** 

**Errores:** `400`, `401`, `403`, `404`, `500`

---

### 3.3 Filtro de reportes

#### 3.3.1 GET /reports/filter

* Igual a `/reports` pero requiere al menos un parámetro de filtro.
* **Errores:** `400` si no hay filtros, `500` error interno

---


✅ Este documento incluye todos los contratos y ejemplos actualizados a junio de 2025. Puedes usar esta guía como referencia técnica integral para desarrollar, mantener o extender el módulo 2 del sistema PatitasBog.

¿Dudas o sugerencias? Contacta al equipo de backend 😺

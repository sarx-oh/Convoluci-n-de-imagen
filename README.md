# Convolución-de-imagen
# Procesamiento de Imágenes y OCR con Google Books API

Este proyecto toma imágenes de libros, extrae el texto de la portada usando OCR (Reconocimiento Óptico de Caracteres) con pytesseract, y busca información del libro en Google Books API.

---

##  **Flujo del programa**
1. Descarga una imagen desde una URL.
2. Convierte la imagen a escala de grises y mejora su legibilidad.
3. Aplica filtros y umbralización para mejorar el OCR.
4.  Extrae el texto de la imagen con pytesseract.
5. Busca el libro en Google Books usando el texto extraído.
6. Muestra un enlace de compra o más información sobre el libro.

---
##  **Explicación de funciones**

### 🔹 `download_image(url)`
Descarga una imagen desde una URL y la convierte en un formato procesable por OpenCV.

-  Realiza una petición HTTP para obtener la imagen.
-  Verifica que el contenido sea una imagen.
-  Convierte la imagen a un formato compatible con OpenCV (cv2).

---

### 🔹 `process_image(image)`
Prepara la imagen para el OCR.

-  Convierte la imagen a escala de grises.
-  Mejora el contraste usando CLAHE (mejor distribución del brillo).
-  Reduce el ruido con un filtro bilateral.
-  Binariza la imagen con umbral automatico de Otsu para mejorar la detección de texto.

---

### 🔹 `show_image(image, title="Imagen")`
Muestra una imagen usando Matplotlib.

-  Se usa solo para visualizar los resultados antes del OCR.

---

### 🔹 `extract_text(image_url)`
Extrae el texto de la imagen.

-  Descarga la imagen con download_image(url).
-  Procesa la imagen con process_image(image).
-  Ejecuta OCR .
-  Filtra los caracteres permitidos (letras, números y algunos signos).
-  Devuelve el texto extraído o un mensaje de error.

---

### 🔹 `get_purchase_link(book_title)`
Busca un libro en Google Books API.

-  Realiza una búsqueda con el título extraído.
-  Devuelve el enlace a la página del libro si está disponible.
-  Maneja errores si no se encuentra el libro o hay problemas con la API.

---

### 🔹 `is_valid_image_url(url)`
Verifica si una URL es válida y contiene una imagen.

-  Devuelve True si la URL apunta a una imagen.
-  Devuelve False si la URL no es válida o no contiene una imagen.

---

### 🔹 `main()`
Ejecuta el flujo completo para varias imágenes.

-  Define una lista de URLs de imágenes de libros.
-  Recorre sobre cada URL:
  - Verifica si es una imagen válida.
  - Procesa la imagen y extrae el texto.
  - Busca el libro en Google Books.
  - Imprime el enlace de compra o información del libro.
---

## **Requisitos**
Antes de ejecutar el código, instala las dependencias necesarias; además se recomienda el uso de Google Colab:

```bash
pip install requests pillow numpy opencv-python pytesseract matplotlib



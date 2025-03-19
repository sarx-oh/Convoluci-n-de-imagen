
# Importar bibliotecas
import cv2
import pytesseract
import numpy as np
import requests
from io import BytesIO
from PIL import Image
from google.colab.patches import cv2_imshow  # Para mostrar imágenes en Colab

# Configurar pytesseract (ruta al ejecutable Tesseract)
pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'

def download_image(url):
    """Descarga una imagen desde una URL y la convierte a formato OpenCV."""
    try:
        response = requests.get(url, timeout=5)  # Máximo 5 segundos de espera
        response.raise_for_status()  # Verifica errores HTTP
        image = Image.open(BytesIO(response.content))
        return cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    except requests.exceptions.Timeout:
        print("Error: La solicitud excedió el tiempo de espera.")
    except requests.exceptions.RequestException as e:
        print(f"Error al descargar la imagen: {e}")
    return None

def process_image(image):
    """Preprocesa la imagen para resaltar el texto y desenfocar el fondo."""
    # Convertir a escala de grises
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detección de bordes para encontrar áreas de texto
    edges = cv2.Canny(gray, 50, 150)

    # Dilatar los bordes para unir áreas cercanas
    kernel = np.ones((3, 3), np.uint8)
    dilated = cv2.dilate(edges, kernel, iterations=2)

    # Encontrar contornos de las áreas de texto
    contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Crear una máscara para las áreas de texto
    mask = np.zeros_like(gray)
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(mask, (x, y), (x + w, y + h), (255), -1)

    # Desenfocar toda la imagen
    blurred_image = cv2.GaussianBlur(image, (25, 25), 0)

    # Combinar la imagen desenfocada con las áreas de texto nítidas
    result = np.where(mask[..., None] == 255, image, blurred_image)

    return result

def extract_text(image_url):
    """Extrae el texto de una imagen usando OCR."""
    image = download_image(image_url)
    if image is None:
        return "No se pudo procesar la imagen."

    processed_image = process_image(image)

    # Configuración avanzada para mejorar OCR
    custom_config = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(processed_image, config=custom_config, lang='eng')

    return text.strip()  # Eliminar espacios en blanco innecesarios

# Ejecutar el código
if __name__ == "__main__":
    # Prueba con diferentes portadas
    image_urls = [
        "https://www.planetadelibros.com.mx/usuaris/libros/fotos/383/m_libros/portada_orgullo-y-prejuicio_jane-austen_202308011307.jpg",
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT_esq8obGbU3busaB8YJ6BR4hygxV8VhYgiQ&s",  # Agregar más URLs de portadas aquí
    ]

    for url in image_urls:
        print(f"Procesando imagen: {url}")
        extracted_text = extract_text(url)
        print("Texto extraído:")
        print(extracted_text)

        # Mostrar la imagen procesada en Colab
        image = download_image(url)
        processed_image = process_image(image)
        cv2_imshow(processed_image)  # Usar cv2_imshow en lugar de cv2.imshow
        print("\n" + "="*50 + "\n")
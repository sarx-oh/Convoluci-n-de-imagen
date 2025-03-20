
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
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        image = Image.open(BytesIO(response.content))
        return cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    except requests.exceptions.Timeout:
        print("Error: La solicitud excedió el tiempo de espera.")
    except requests.exceptions.RequestException as e:
        print(f"Error al descargar la imagen: {e}")
    return None

def process_image(image):
    """Preprocesa la imagen para mejorar la precisión del OCR."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Convertir a escala de grises

    # Mejorar el contraste con ecualización de histograma
    clahe = cv2.createCLAHE(clipLimit=5.0, tileGridSize=(8, 8))
    gray = clahe.apply(gray)

    # Reducir ruido con un filtro bilateral
    denoised = cv2.bilateralFilter(gray, 9, 75, 75)

    # Usar umbral adaptativo o binarización de Otsu según el caso
    _, thresh = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    return thresh

def extract_text(image_url):
    """Extrae el texto de una imagen usando OCR mejorado."""
    image = download_image(image_url)
    if image is None:
        return "No se pudo procesar la imagen."

    processed_image = process_image(image)

    # Configuración avanzada de Tesseract
    custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789,.!?() "'
    text = pytesseract.image_to_string(processed_image, config=custom_config, lang='eng')

    return text.strip()

def get_purchase_link(book_title):
    """Busca un enlace de compra para el libro basado en su título."""
    # Se integra una API de comercio electrónico (por ejemplo, Amazon, Google Books, etc.)
    # en este caso se busca en Google Books.
    base_url = "https://www.googleapis.com/books/v1/volumes"
    params = {
        "q": book_title,  # Título del libro
        "maxResults": 1,  # Solo un resultado
    }
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        if data.get("items"):
            # Obtener el enlace de compra checa si está disponible o no
            purchase_link = data["items"][0]["volumeInfo"].get("infoLink", "No disponible")
            return purchase_link
        else:
            return "No se encontró el libro."
    except requests.exceptions.RequestException as e:
        return f"Error al buscar el libro: {e}"

# ejecutar el código
if __name__ == "__main__":
    image_urls = [
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT_esq8obGbU3busaB8YJ6BR4hygxV8VhYgiQ&s",
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS_HHeiT15U_9PDR0FhgS_riO6zha67cN7DHw&s", 
        "https://www.elbazardelibro.com.mx/imagenes/9786071/978607141537.JPG"

    ]

    for url in image_urls:
        print(f"Procesando imagen: {url}")
        extracted_text = extract_text(url)
        print("Texto extraído:")
        print(extracted_text)

        # Enlace de compra basado en el texto extraído
        purchase_link = get_purchase_link(extracted_text)
        print("Enlace de compra:")
        print(purchase_link)

        # Mostrar imagen ya procesada
        image = download_image(url)
        processed_image = process_image(image)
        cv2_imshow(processed_image)  # Usar cv2_imshow en Colab
        print("\n" + "="*50 + "\n")
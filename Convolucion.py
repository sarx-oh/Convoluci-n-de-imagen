import cv2
import pytesseract
import numpy as np
import requests
from io import BytesIO
from PIL import Image


#Descarga una imagen y la convierte a OpenCv
def download_image(url):
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

#Mejora la extracción de texto
def process_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Reducción de ruido con desenfoque
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Umbral adaptativo para mejorar contraste
    thresh = cv2.adaptiveThreshold(
        blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
    )

    # Aplicar un cierre morfológico para mejorar segmentación
    kernel = np.ones((3, 3), np.uint8)
    processed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

    return processed

#Extrae el texto usando OCR
def extract_text(image_url):
    image = download_image(image_url)
    if image is None:
        return "No se pudo procesar la imagen."

    processed_image = process_image(image)

    # Configuración avanzada para mejorar OCR
    custom_config = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(processed_image, config=custom_config, lang='eng')

    return text.strip()  # Eliminar espacios en blanco innecesarios


if __name__ == "__main__":
    image_url = (
        "https://images.cdn2.buscalibre.com/fit-in/360x360/c8/fc/c8fc51c9d0213acbfb24c0ac3cbd7c66.jpg"
    )  # Usa otra imagen si la original no funciona
    extracted_text = extract_text(image_url)

    print("Texto extraído:")
    print(extracted_text)

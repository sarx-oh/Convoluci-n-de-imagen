import requests
from PIL import Image
from io import BytesIO
import cv2
import numpy as np
import pytesseract
import matplotlib.pyplot as plt


# Función que valida si el URL contiene una imagen
def is_valid_image_url(url):
    try:
        # Se pide el HEAD para obtener los encabezados para después usar content-type
        response = requests.head(url, timeout=5)
        content_type = response.headers.get("Content-Type", "")

        if "image" not in content_type:
            print(f" La URL {url} no parece ser una imagen. Tipo: {content_type}")
            return False
        return True
    except requests.exceptions.RequestException as e:
        print(f" No se pudo verificar la URL {url}: {e}")
        return False


# Función para descargar una imagen
def download_image(url):
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()

        if not response.content:
            print(f"Error: La URL {url} no devolvió contenido válido.")
            return None

        image = Image.open(BytesIO(response.content))
        # La convierte en cv2 para facilitar el procesamiento
        return cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    # Se agregan para las posibles excepciones
    except requests.exceptions.Timeout:
        print(f"Error: La solicitud a {url} excedió el tiempo de espera.")
    except requests.exceptions.RequestException as e:
        print(f"Error al descargar la imagen {url}: {e}")
    except Exception as e:
        print(f"Error inesperado con la imagen {url}: {e}")

    return None


# Función para procesar la imagen
def process_image(image):
    if image is None:
        print("Error: La imagen es None y no se puede procesar.")
        return None

    # Convierte la imagen a escala de grises
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Mejora el contraste
    clahe = cv2.createCLAHE(clipLimit=5.0, tileGridSize=(8, 8))
    gray = clahe.apply(gray)
    # Reduce el ruido
    denoised = cv2.bilateralFilter(gray, 9, 75, 75)
    # Aplica umbralización
    _, thresh = cv2.threshold(
        denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )

    return thresh

# Función para mostrar la imagen
def show_image(image, title="Imagen"):
    plt.figure(figsize=(8, 6))
    plt.imshow(image, cmap='gray')
    plt.title(title)
    plt.axis("off")
    plt.show()


# Función para extraer el texto de la imagen
def extract_text(image_url):
    image = download_image(image_url)
    if image is None:
        return "No se pudo procesar la imagen."

    processed_image = process_image(image)
    if processed_image is None:
        return "Error en el procesamiento de la imagen."

    show_image(processed_image, "Imagen Procesada")

    # Ejecuta OCR usando OEM 3, PSM 6, lista blanca de caracteres
    custom_config = (
        r'--oem 3 --psm 6 -c tessedit_char_whitelist="'
        r'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789,.!?() "'
    )
    text = pytesseract.image_to_string(processed_image, config=custom_config, lang='eng')

    return text.strip()

# Función para obtener un enlace de compra usando la API de Google Books
def get_purchase_link(book_title):
    base_url = "https://www.googleapis.com/books/v1/volumes"
    params = {"q": book_title, "maxResults": 1}
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()

        if data.get("items"):
            return data["items"][0]["volumeInfo"].get("infoLink", "No disponible")
        return "No se encontró el libro."
    except requests.exceptions.RequestException as e:
        return f"Error al buscar el libro: {e}"

if __name__ == "__main__":
    image_urls = [
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT_esq8obGbU3busaB8YJ6BR4hygxV8VhYgiQ&s",
        "https://elratondebiblioteca.com/wp-content/uploads/2024/02/464-1c51bb26-0c83-4093-8824-5bb07679130d.jpg",
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS_HHeiT15U_9PDR0FhgS_riO6zha67cN7DHw&s",
        "https://images.cdn2.buscalibre.com/fit-in/360x360/03/05/03056fc1f0f830b81b7f92a74b5ce27e.jpg",
        "https://image.isu.pub/161205231810-a6826fe780ef64bf5bd3a99eb2792947/jpg/page_1_thumb_large.jpg"
    ]

    for url in image_urls:
        if not is_valid_image_url(url):
            print(f"Saltando URL no válida: {url}")
            continue

        print(f"Procesando imagen: {url}")
        extracted_text = extract_text(url)
        print("Texto extraído:")
        print(extracted_text)

        purchase_link = get_purchase_link(extracted_text)
        print("Enlace de compra:")
        print(purchase_link)
        print("\n" + "=" * 50 + "\n")

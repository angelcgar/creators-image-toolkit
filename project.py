from PIL import Image, ImageDraw, ImageFont
import sys
import os

def main():
    # 1. Obtener ruta de la imagen desde sys.argv
    # 2. Llamar a tus funciones
    # 3. Guardar el resultado
    ...

def validate_image(path):
    if not os.path.exists(path):
        raise FileNotFoundError("Archivo no encontrado")
    # Lógica para verificar extensión...
    return True

def apply_watermark(img_path, text="By GastoPro"):
    # Lógica con Pillow para escribir texto en la imagen
    ...
    return "watermarked_image.png"

def resize_for_social(img_path, platform="youtube"):
    # Lógica para cambiar el tamaño
    sizes = {"youtube": (1280, 720), "instagram": (1080, 1080)}
    ...
    return "resized_image.png"

if __name__ == "__main__":
    main()
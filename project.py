"""
Creators Image Toolkit - A CLI utility for digital creators to process images.

This module provides functionality to add watermarks and resize images
for different social media platforms (YouTube, Instagram).
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Literal

from PIL import Image, ImageDraw, ImageFont
#from PIL.UnidentifiedImageError import UnidentifiedImageError
from PIL import Image, UnidentifiedImageError


VALID_EXTENSIONS: tuple[str, ...] = (".png", ".jpg", ".jpeg")
PLATFORM_SIZES: dict[str, tuple[int, int]] = {
    "youtube": (1280, 720),
    "instagram": (1080, 1350),
}
PlatformType = Literal["youtube", "instagram"]


def main() -> None:
    """
    Main entry point for the CLI application.

    Parses command-line arguments, validates the input file,
    applies watermark, resizes for the target platform, and saves the output.
    """
    parser = argparse.ArgumentParser(
        description="Process images for social media platforms with watermarks.",
        prog="project",
    )
    parser.add_argument(
        "input",
        type=str,
        help="Path to the source image file.",
    )
    parser.add_argument(
        "--platform",
        type=str,
        choices=["youtube", "instagram"],
        default="youtube",
        help="Target platform for resizing (default: youtube).",
    )
    parser.add_argument(
        "--text",
        type=str,
        default="ArtPro",
        help="Watermark text to apply (default: ArtPro).",
    )

    args = parser.parse_args()

    try:
        validated_path = validate_file(args.input)
        image = Image.open(validated_path).convert("RGBA")

        watermarked_image = apply_watermark(image, args.text)
        resized_image = resize_for_platform(watermarked_image, args.platform)

        output_filename = f"{validated_path.stem}_{args.platform}_final.png"
        resized_image.save(output_filename)
        print(f"Image saved as: {output_filename}")

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except UnidentifiedImageError:
        print(f"Error: Cannot identify image file '{args.input}'.", file=sys.stderr)
        sys.exit(1)
    except OSError as e:
        print(f"Error: Failed to process image - {e}", file=sys.stderr)
        sys.exit(1)


def validate_file(path: str) -> Path:
    """
    Validate that the file exists and has a supported image extension.

    Args:
        path: The file path to validate.

    Returns:
        A Path object representing the validated file path.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file extension is not supported.
    """
    file_path = Path(path)

    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    if file_path.suffix.lower() not in VALID_EXTENSIONS:
        raise ValueError(
            f"Invalid file extension '{file_path.suffix}'. "
            f"Allowed: {', '.join(VALID_EXTENSIONS)}"
        )

    return file_path


def apply_watermark(image: Image.Image, text: str) -> Image.Image:
    """
    Mejora: Usa fuentes de sistema en Linux y dibuja un borde para que se vea
    en fondos claros y oscuros.
    """
    overlay = Image.new("RGBA", image.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(overlay)

    # Proporción del 5% del ancho de la imagen
    font_size = max(24, image.width // 20)
    
    # Intentar cargar una fuente común en Arch Linux (DejaVu o Liberation)
    font = None
    fonts_to_try = [
        "/usr/share/fonts/TTF/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/liberation/LiberationSans-Bold.ttf",
        "arial.ttf"
    ]
    
    for f in fonts_to_try:
        try:
            font = ImageFont.truetype(f, font_size)
            break
        except OSError:
            continue
            
    if not font:
        font = ImageFont.load_default()

    # Calcular posición con padding relativo
    padding = image.width // 50
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = image.width - text_width - padding
    y = image.height - text_height - padding

    # Dibujar un pequeño borde negro para que resalte
    draw.text((x+2, y+2), text, font=font, fill=(0, 0, 0, 150))
    # Dibujar el texto blanco principal
    draw.text((x, y), text, font=font, fill=(255, 255, 255, 200))

    return Image.alpha_composite(image, overlay)

def resize_for_platform(image: Image.Image, platform: PlatformType) -> Image.Image:
    """
    Mejora: Ajusta la imagen al tamaño exacto de la plataforma.
    Si la relación de aspecto no coincide, añade un fondo negro (letterboxing).
    """
    target_width, target_height = PLATFORM_SIZES[platform]
    
    # Crear un lienzo negro del tamaño exacto de la plataforma
    canvas = Image.new("RGBA", (target_width, target_height), (0, 0, 0, 255))
    
    # Redimensionar manteniendo aspecto (Thumbnailing)
    img_copy = image.copy()
    img_copy.thumbnail((target_width, target_height), Image.Resampling.LANCZOS)
    
    # Centrar la imagen en el lienzo
    offset = (
        (target_width - img_copy.width) // 2,
        (target_height - img_copy.height) // 2
    )
    
    canvas.paste(img_copy, offset, img_copy if img_copy.mode == 'RGBA' else None)
    return canvas

if __name__ == "__main__":
    main()
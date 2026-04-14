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
    "youtube": (1920, 1080),
    "instagram": (1080, 1350),
    "square": (1080, 1080),
    "tiktok": (1080, 1920),
}
PlatformType = Literal["youtube", "instagram", "square", "tiktok"]


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
        choices=["youtube", "instagram", "square", "tiktok"],
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
    Apply a semi-transparent watermark with drop shadow to the bottom-right corner.

    Font size is calculated as 5% of the SHORTER side to prevent oversized text
    on vertical images.

    Args:
        image: The source PIL Image object (must be in RGBA mode).
        text: The watermark text to apply.

    Returns:
        A new PIL Image object with the watermark applied.
    """
    overlay = Image.new("RGBA", image.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(overlay)

    shorter_side = min(image.width, image.height)
    font_size = max(24, shorter_side // 20)

    font = None
    fonts_to_try = [
        "/usr/share/fonts/TTF/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/liberation/LiberationSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "arial.ttf",
    ]

    for font_path in fonts_to_try:
        try:
            font = ImageFont.truetype(font_path, font_size)
            break
        except OSError:
            continue

    if not font:
        font = ImageFont.load_default()

    padding = shorter_side // 40
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    x = image.width - text_width - padding
    y = image.height - text_height - padding

    shadow_offset = max(2, font_size // 18)
    draw.text((x + shadow_offset, y + shadow_offset), text, font=font, fill=(0, 0, 0, 150))
    draw.text((x, y), text, font=font, fill=(255, 255, 255, 200))

    return Image.alpha_composite(image, overlay)

def resize_for_platform(image: Image.Image, platform: PlatformType) -> Image.Image:
    """
    Resize an image using Fit & Fill logic for a specific platform.

    Creates a black canvas of the exact target size, scales the source image
    to fit within the target dimensions (maintaining aspect ratio, no cropping),
    and centers it on the canvas (letterboxing/pillarboxing as needed).

    Args:
        image: The source PIL Image object.
        platform: The target platform ('youtube', 'instagram', 'square', 'tiktok').

    Returns:
        A new PIL Image object with exact platform dimensions.
    """
    target_width, target_height = PLATFORM_SIZES[platform]

    canvas = Image.new("RGBA", (target_width, target_height), (0, 0, 0, 255))

    scale_factor = min(target_width / image.width, target_height / image.height)
    new_width = int(image.width * scale_factor)
    new_height = int(image.height * scale_factor)

    resized_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)

    offset_x = (target_width - new_width) // 2
    offset_y = (target_height - new_height) // 2

    canvas.paste(resized_image, (offset_x, offset_y), resized_image if resized_image.mode == "RGBA" else None)
    return canvas

if __name__ == "__main__":
    main()
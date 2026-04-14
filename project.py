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
    Apply a semi-transparent watermark text to the bottom-right corner of an image.

    The font size is calculated relative to the image width (approximately 3%).
    The watermark uses 50% transparency (alpha=128).

    Args:
        image: The source PIL Image object (must be in RGBA mode).
        text: The watermark text to apply.

    Returns:
        A new PIL Image object with the watermark applied.
    """
    overlay = Image.new("RGBA", image.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(overlay)

    font_size = max(16, image.width // 30)
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except OSError:
        font = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    padding = 20
    x_position = image.width - text_width - padding
    y_position = image.height - text_height - padding

    draw.text(
        (x_position, y_position),
        text,
        font=font,
        fill=(255, 255, 255, 128),
    )

    return Image.alpha_composite(image, overlay)


def resize_for_platform(image: Image.Image, platform: PlatformType) -> Image.Image:
    """
    Resize an image for a specific social media platform while maintaining aspect ratio.

    The image is scaled to fit within the target dimensions without cropping,
    preserving the original aspect ratio.

    Args:
        image: The source PIL Image object.
        platform: The target platform ('youtube' or 'instagram').

    Returns:
        A new PIL Image object resized for the specified platform.
    """
    target_width, target_height = PLATFORM_SIZES[platform]

    image_ratio = image.width / image.height
    target_ratio = target_width / target_height

    if image_ratio > target_ratio:
        new_width = target_width
        new_height = int(target_width / image_ratio)
    else:
        new_height = target_height
        new_width = int(target_height * image_ratio)

    return image.resize((new_width, new_height), Image.Resampling.LANCZOS)


if __name__ == "__main__":
    main()
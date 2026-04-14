from PIL import Image, ImageDraw, ImageFont
import sys
import os


VALID_EXTENSIONS = (".png", ".jpg", ".jpeg")
PLATFORM_SIZES = {
    "youtube": (1280, 720),
    "instagram": (1080, 1350),
}


def main():
    if len(sys.argv) < 3:
        sys.exit("Usage: python project.py <image_path> <platform>")

    image_path = sys.argv[1]
    platform = sys.argv[2].lower()

    if platform not in PLATFORM_SIZES:
        sys.exit(f"Invalid platform. Choose from: {', '.join(PLATFORM_SIZES.keys())}")

    validated_path = validate_file(image_path)

    watermark_text = input("Enter watermark text (default: ArtPro): ").strip()
    if not watermark_text:
        watermark_text = "ArtPro"

    watermarked_img = apply_watermark(validated_path, watermark_text)
    resized_img = resize_for_platform(watermarked_img, platform)

    base_name = os.path.splitext(os.path.basename(validated_path))[0]
    output_filename = f"{base_name}_{platform}_final.png"
    resized_img.save(output_filename)
    print(f"Image saved as: {output_filename}")


def validate_file(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")

    _, ext = os.path.splitext(path)
    if ext.lower() not in VALID_EXTENSIONS:
        raise ValueError(f"Invalid file extension. Allowed: {', '.join(VALID_EXTENSIONS)}")

    return path


def apply_watermark(img_path, text):
    img = Image.open(img_path).convert("RGBA")

    overlay = Image.new("RGBA", img.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(overlay)

    try:
        font = ImageFont.truetype("arial.ttf", 36)
    except OSError:
        font = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    padding = 20
    x = img.width - text_width - padding
    y = img.height - text_height - padding

    draw.text((x, y), text, font=font, fill=(255, 255, 255, 128))

    watermarked = Image.alpha_composite(img, overlay)
    return watermarked


def resize_for_platform(img, platform="youtube"):
    if isinstance(img, str):
        img = Image.open(img).convert("RGBA")

    target_width, target_height = PLATFORM_SIZES[platform]

    img_ratio = img.width / img.height
    target_ratio = target_width / target_height

    if img_ratio > target_ratio:
        new_width = target_width
        new_height = int(target_width / img_ratio)
    else:
        new_height = target_height
        new_width = int(target_height * img_ratio)

    resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
    return resized


if __name__ == "__main__":
    main()
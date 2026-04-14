# Creators Image Toolkit

#### Video Demo:

#### Description: 

The Creators Image Toolkit is a specialized Command Line Interface (CLI) tool designed for digital artists and content creators who need to streamline their post-production workflow. As a digital illustrator myself, I often found the process of manually watermarking and resizing artworks for different social media platforms to be tedious and prone to human error. This project solves that problem by providing a robust, automated solution written in Python.

The core purpose of this software is to take a high-resolution source image (such as an export from Ibis Paint X or Procreate) and automatically generate multiple versions optimized for platforms like Instagram, YouTube, TikTok, and Square formats. Beyond simple resizing, the toolkit ensures that every exported image maintains its professional branding through a dynamically scaled watermark.

### Features and Functionality

The toolkit offers several key features that distinguish it from basic image converters:

1. **Smart Resizing (Fit & Fill):** Unlike standard tools that might stretch or crop an image, this toolkit uses a "canvas-based" approach. It creates a background of the exact required dimensions (e.g., 1080x1350 for Instagram) and centers the artwork, adding black bars (letterboxing) if the aspect ratios do not match.

2. **Dynamic Watermarking:** The tool calculates the optimal font size based on the image's dimensions. It also adds a subtle drop shadow to the text, ensuring the watermark is legible regardless of whether the artwork has a light or dark background.

3. **Broad Platform Support:** It includes presets for modern social media standards, including vertical formats for TikTok/Reels and high-definition landscapes for YouTube.

### Project Structure and Files

- `project.py`: This is the heart of the application. It utilizes the `argparse` library to provide a clean CLI experience. It handles the logic for opening images with the **Pillow (PIL)** library, orchestrates the transformation process, and manages error handling for unsupported file types or missing assets.

- `test_project.py`: A comprehensive suite of 13 tests using `pytest`. These tests ensure the reliability of the validation logic, verify that the resizing math produces the exact pixel dimensions required, and confirm that the watermark process preserves the image's color mode and transparency.

- `requirements.txt`: Lists the essential external dependencies, specifically `Pillow` for image processing and `pytest` for the testing framework.

### Design Choices

During development, I made several critical design decisions:

- **Why Argparse?** I chose `argparse` over simple `sys.argv` to provide a professional user experience, including automatic help messages and strict type validation for command-line inputs

- **The Watermark Logic**: I initially considered a fixed font size, but realized it would be invisible on 4K renders and massive on small thumbnails. Implementing a percentage-based scaling (5% of the shorter side) ensured consistency across all resolutions.

- **Linux Compatibility**: Since I develop on **Arch Linux**, I implemented a font-searching logic that looks for common system fonts like *DejaVu Sans* or *Liberation Sans*, falling back to the default PIL font only if necessary. This makes the tool "plug-and-play" for Linux users.

- **RGBA vs RGB**: I decided to convert all images to RGBA during processing. This allows for semi-transparent watermarks and ensures that transparency in the original artwork is preserved throughout the resizing process.

### Conclusion

This project represents a bridge between my two passions: digital art and software development. It is not just an academic exercise but a tool I intend to use for my own creative portfolio. By automating these repetitive tasks, the **Creators Image Toolkit** allows artists to spend less time on technical exports and more time on the creative process.
"""
Test suite for project.py - Creators Image Toolkit.

Tests cover validate_file, apply_watermark, and resize_for_platform functions.
"""

import pytest
from pathlib import Path
from PIL import Image

from project import validate_file, apply_watermark, resize_for_platform


class TestValidateFile:
    """Tests for the validate_file function."""

    def test_validate_file_not_found(self) -> None:
        """Should raise FileNotFoundError for non-existent file."""
        with pytest.raises(FileNotFoundError):
            validate_file("non_existent_image.png")

    def test_validate_file_invalid_extension(self, tmp_path: Path) -> None:
        """Should raise ValueError for invalid file extension."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("dummy content")

        with pytest.raises(ValueError):
            validate_file(str(test_file))

    def test_validate_file_valid_png(self, tmp_path: Path) -> None:
        """Should return Path for valid .png file."""
        test_file = tmp_path / "test.png"
        test_file.write_bytes(b"dummy")

        result = validate_file(str(test_file))
        assert isinstance(result, Path)
        assert result.suffix == ".png"

    def test_validate_file_valid_jpg(self, tmp_path: Path) -> None:
        """Should return Path for valid .jpg file."""
        test_file = tmp_path / "test.jpg"
        test_file.write_bytes(b"dummy")

        result = validate_file(str(test_file))
        assert isinstance(result, Path)
        assert result.suffix == ".jpg"


class TestResizeForPlatform:
    """Tests for the resize_for_platform function."""

    @pytest.fixture
    def dummy_image(self) -> Image.Image:
        """Create a dummy RGBA image for testing."""
        return Image.new("RGBA", (800, 600), (255, 0, 0, 255))

    def test_resize_for_youtube(self, dummy_image: Image.Image) -> None:
        """Should resize to 1920x1080 for YouTube."""
        result = resize_for_platform(dummy_image, "youtube")

        assert result.width == 1920
        assert result.height == 1080

    def test_resize_for_tiktok(self, dummy_image: Image.Image) -> None:
        """Should resize to 1080x1920 for TikTok."""
        result = resize_for_platform(dummy_image, "tiktok")

        assert result.width == 1080
        assert result.height == 1920

    def test_resize_for_instagram(self, dummy_image: Image.Image) -> None:
        """Should resize to 1080x1350 for Instagram."""
        result = resize_for_platform(dummy_image, "instagram")

        assert result.width == 1080
        assert result.height == 1350

    def test_resize_for_square(self, dummy_image: Image.Image) -> None:
        """Should resize to 1080x1080 for square format."""
        result = resize_for_platform(dummy_image, "square")

        assert result.width == 1080
        assert result.height == 1080

    def test_resize_returns_rgba(self, dummy_image: Image.Image) -> None:
        """Should return an RGBA image."""
        result = resize_for_platform(dummy_image, "youtube")

        assert result.mode == "RGBA"


class TestApplyWatermark:
    """Tests for the apply_watermark function."""

    @pytest.fixture
    def dummy_image(self) -> Image.Image:
        """Create a dummy RGBA image for testing."""
        return Image.new("RGBA", (1000, 800), (100, 150, 200, 255))

    def test_apply_watermark_returns_image(self, dummy_image: Image.Image) -> None:
        """Should return a PIL Image object."""
        result = apply_watermark(dummy_image, "TestWatermark")

        assert isinstance(result, Image.Image)

    def test_apply_watermark_preserves_dimensions(self, dummy_image: Image.Image) -> None:
        """Should preserve the original image dimensions."""
        result = apply_watermark(dummy_image, "TestWatermark")

        assert result.width == dummy_image.width
        assert result.height == dummy_image.height

    def test_apply_watermark_preserves_mode(self, dummy_image: Image.Image) -> None:
        """Should preserve RGBA mode."""
        result = apply_watermark(dummy_image, "TestWatermark")

        assert result.mode == "RGBA"

    def test_apply_watermark_with_empty_text(self, dummy_image: Image.Image) -> None:
        """Should handle empty watermark text."""
        result = apply_watermark(dummy_image, "")

        assert isinstance(result, Image.Image)
        assert result.size == dummy_image.size

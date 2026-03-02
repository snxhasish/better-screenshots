"""Output saver - save images to files."""

import os
from datetime import datetime
from pathlib import Path
from typing import Optional

from PIL import Image


class ImageSaver:
    """Save processed images to files."""

    @staticmethod
    def generate_filename(
        directory: str,
        pattern: str,
        format: str,
    ) -> Path:
        """Generate filename from pattern."""
        directory = os.path.expanduser(directory)
        Path(directory).mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime(pattern)
        filename = f"{timestamp}.{format}"

        return Path(directory) / filename

    @staticmethod
    def save_image(
        image: Image.Image,
        output_path: Path,
        format: str = "PNG",
        quality: int = 90,
        compression: int = 6,
    ) -> Path:
        """Save image to file."""
        output_path.parent.mkdir(parents=True, exist_ok=True)

        save_kwargs = {}

        if format.upper() in ("JPEG", "JPG"):
            save_kwargs["quality"] = quality
            save_kwargs["optimize"] = True
            if image.mode == "RGBA":
                image = image.convert("RGB")
        elif format.upper() == "PNG":
            save_kwargs["compress_level"] = compression

        image.save(str(output_path), format=format.upper(), **save_kwargs)

        return output_path

    @staticmethod
    def get_next_filename(
        directory: str,
        pattern: str,
        format: str,
    ) -> Path:
        """Get next available filename."""
        directory = os.path.expanduser(directory)
        Path(directory).mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime(pattern)
        base_path = Path(directory) / f"{timestamp}.{format}"

        if not base_path.exists():
            return base_path

        counter = 1
        while True:
            new_path = Path(directory) / f"{timestamp}_{counter}.{format}"
            if not new_path.exists():
                return new_path
            counter += 1

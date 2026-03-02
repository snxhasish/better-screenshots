"""Clipboard functionality for copying images."""

import subprocess
from pathlib import Path
from typing import Optional

from PIL import Image


class Clipboard:
    """Copy images to clipboard."""

    @staticmethod
    def is_wayland() -> bool:
        """Check if running on Wayland."""
        return "WAYLAND_DISPLAY" in __import__("os").environ

    @staticmethod
    def is_x11() -> bool:
        """Check if running on X11."""
        return "DISPLAY" in __import__("os").environ

    def copy_image(self, image_path: Path) -> bool:
        """Copy image to clipboard."""
        if self.is_wayland():
            return self._copy_wayland(image_path)
        elif self.is_x11():
            return self._copy_x11(image_path)
        return False

    def _copy_wayland(self, image_path: Path) -> bool:
        """Copy image to clipboard on Wayland."""
        try:
            subprocess.run(
                ["wl-copy", "--type", "image/png"],
                input=image_path.read_bytes(),
                check=True,
            )
            return True
        except (subprocess.SubprocessError, FileNotFoundError):
            return self._copy_x11(image_path)

    def _copy_x11(self, image_path: Path) -> bool:
        """Copy image to clipboard on X11."""
        try:
            subprocess.run(
                ["xclip", "-selection", "clipboard", "-t", "image/png", "-i", str(image_path)],
                check=True,
            )
            return True
        except (subprocess.SubprocessError, FileNotFoundError):
            return False

    def copy_text(self, text: str) -> bool:
        """Copy text to clipboard."""
        if self.is_wayland():
            return self._copy_text_wayland(text)
        elif self.is_x11():
            return self._copy_text_x11(text)
        return False

    def _copy_text_wayland(self, text: str) -> bool:
        """Copy text to clipboard on Wayland."""
        try:
            subprocess.run(
                ["wl-copy"],
                input=text.encode(),
                check=True,
            )
            return True
        except (subprocess.SubprocessError, FileNotFoundError):
            return False

    def _copy_text_x11(self, text: str) -> bool:
        """Copy text to clipboard on X11."""
        try:
            subprocess.run(
                ["xclip", "-selection", "clipboard"],
                input=text.encode(),
                check=True,
            )
            return True
        except (subprocess.SubprocessError, FileNotFoundError):
            return False

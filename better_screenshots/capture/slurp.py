"""Slurp integration for region selection."""

import subprocess
from pathlib import Path
from typing import Optional


class SlurpSelector:
    """Region selection using slurp."""

    @staticmethod
    def is_available() -> bool:
        """Check if slurp is available."""
        try:
            subprocess.run(
                ["slurp", "--version"],
                capture_output=True,
                check=True,
            )
            return True
        except (subprocess.SubprocessError, FileNotFoundError):
            return False

    def select_region(self) -> Optional[str]:
        """Select a region interactively."""
        try:
            result = subprocess.run(
                ["slurp"],
                capture_output=True,
                check=True,
                text=True,
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError:
            return None

    def select_region_with_options(
        self,
        format: str = "geo",
        color: Optional[str] = None,
        border_size: Optional[int] = None,
    ) -> Optional[str]:
        """Select region with custom options."""
        cmd = ["slurp", "-f", format]

        if color:
            cmd.extend(["-c", color])
        if border_size:
            cmd.extend(["-w", str(border_size)])

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                check=True,
                text=True,
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError:
            return None

    def parse_geometry(self, geometry: str) -> dict:
        """Parse slurp geometry string."""
        parts = geometry.split("x")
        if len(parts) != 2:
            return {}

        width, height = parts
        coords = height.split("+")

        return {
            "width": int(coords[0]),
            "height": int(coords[1]) if len(coords) > 1 else 0,
            "x": int(coords[2]) if len(coords) > 2 else 0,
            "y": int(coords[3]) if len(coords) > 3 else 0,
        }

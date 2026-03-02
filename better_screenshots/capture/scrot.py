"""Scrot integration for X11 screenshot capture."""

import subprocess
from pathlib import Path
from typing import Optional


class ScrotCapture:
    """Screenshot capture using scrot."""

    @staticmethod
    def is_available() -> bool:
        """Check if scrot is available."""
        try:
            subprocess.run(
                ["scrot", "--version"],
                capture_output=True,
                check=True,
            )
            return True
        except (subprocess.SubprocessError, FileNotFoundError):
            return False

    def capture_fullscreen(
        self,
        output_path: Optional[Path] = None,
    ) -> Path:
        """Capture full screen."""
        cmd = ["scrot"]

        if output_path:
            cmd.append(str(output_path))
        else:
            import tempfile
            cmd.append(str(Path(tempfile.gettempdir()) / "screenshot.png"))

        subprocess.run(cmd, check=True)
        return Path(cmd[-1])

    def capture_window(
        self,
        output_path: Optional[Path] = None,
        select: bool = True,
    ) -> Path:
        """Capture window (optionally with selection)."""
        cmd = ["scrot"]

        if select:
            cmd.append("--select")

        if output_path:
            cmd.append(str(output_path))
        else:
            import tempfile
            cmd.append(str(Path(tempfile.gettempdir()) / "screenshot.png"))

        subprocess.run(cmd, check=True)
        return Path(cmd[-1])

    def capture_region(
        self,
        output_path: Optional[Path] = None,
    ) -> Path:
        """Capture selected region."""
        cmd = ["scrot", "--select"]

        if output_path:
            cmd.append(str(output_path))
        else:
            import tempfile
            cmd.append(str(Path(tempfile.gettempdir()) / "screenshot.png"))

        subprocess.run(cmd, check=True)
        return Path(cmd[-1])

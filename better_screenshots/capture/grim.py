"""Grim integration for Wayland screenshot capture."""

import shutil
import subprocess
from pathlib import Path
from typing import Optional


class GrimCapture:
    """Screenshot capture using grim."""

    @staticmethod
    def is_available() -> bool:
        """Check if grim is available."""
        return shutil.which("grim") is not None

    def capture_fullscreen(
        self,
        output_path: Optional[Path] = None,
        monitor: Optional[str] = None,
    ) -> Path:
        """Capture full screen."""
        cmd = ["grim"]

        if monitor:
            cmd.extend(["-o", monitor])

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
        window_id: Optional[str] = None,
    ) -> Path:
        """Capture specific window."""
        cmd = ["grim"]

        if window_id:
            cmd.extend(["-w", window_id])
        else:
            cmd.append("-w")

        if output_path:
            cmd.append(str(output_path))
        else:
            import tempfile
            cmd.append(str(Path(tempfile.gettempdir()) / "screenshot.png"))

        subprocess.run(cmd, check=True)
        return Path(cmd[-1])

    def capture_region(
        self,
        geometry: str,
        output_path: Optional[Path] = None,
    ) -> Path:
        """Capture region with specified geometry."""
        cmd = ["grim", "-g", geometry]

        if output_path:
            cmd.append(str(output_path))
        else:
            import tempfile
            cmd.append(str(Path(tempfile.gettempdir()) / "screenshot.png"))

        subprocess.run(cmd, check=True)
        return Path(cmd[-1])

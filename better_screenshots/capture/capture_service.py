"""Screenshot capture service - unified interface for grim/scrot."""

import subprocess
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from .grim import GrimCapture
from .scrot import ScrotCapture
from .slurp import SlurpSelector


@dataclass
class CaptureResult:
    """Result of a screenshot capture."""
    image_path: Path
    geometry: Optional[dict] = None


class CaptureService:
    """Unified capture service for screenshots."""

    def __init__(self):
        self.grim = GrimCapture()
        self.scrot = ScrotCapture()
        self.slurp = SlurpSelector()

    def detect_backend(self) -> str:
        """Detect available screenshot backend."""
        if self.grim.is_available():
            return "grim"
        elif self.scrot.is_available():
            return "scrot"
        return "none"

    def is_available(self) -> bool:
        """Check if any capture backend is available."""
        return self.detect_backend() != "none"

    def capture(
        self,
        mode: str = "region",
        delay: int = 0,
        output_path: Optional[Path] = None,
    ) -> CaptureResult:
        """Capture screenshot based on mode."""
        if delay > 0:
            time.sleep(delay)

        backend = self.detect_backend()

        if mode == "fullscreen":
            return self._capture_fullscreen(backend, output_path)
        elif mode == "window":
            return self._capture_window(backend, output_path)
        elif mode == "region":
            return self._capture_region(backend, output_path)
        else:
            return self._capture_region(backend, output_path)

    def _capture_fullscreen(
        self,
        backend: str,
        output_path: Optional[Path] = None,
    ) -> CaptureResult:
        """Capture full screen."""
        if not output_path:
            output_path = Path(tempfile.gettempdir()) / "screenshot.png"

        if backend == "grim":
            path = self.grim.capture_fullscreen(output_path)
        elif backend == "scrot":
            path = self.scrot.capture_fullscreen(output_path)
        else:
            raise RuntimeError("No screenshot backend available")

        return CaptureResult(image_path=path)

    def _capture_window(
        self,
        backend: str,
        output_path: Optional[Path] = None,
    ) -> CaptureResult:
        """Capture window."""
        if not output_path:
            output_path = Path(tempfile.gettempdir()) / "screenshot.png"

        if backend == "grim":
            path = self.grim.capture_window(output_path)
        elif backend == "scrot":
            path = self.scrot.capture_window(output_path)
        else:
            raise RuntimeError("No screenshot backend available")

        return CaptureResult(image_path=path)

    def _capture_region(
        self,
        backend: str,
        output_path: Optional[Path] = None,
    ) -> CaptureResult:
        """Capture region."""
        if not output_path:
            output_path = Path(tempfile.gettempdir()) / "screenshot.png"

        if backend == "grim":
            return self._capture_region_wayland(output_path)
        elif backend == "scrot":
            return self._capture_region_x11(output_path)
        else:
            raise RuntimeError("No screenshot backend available")

    def _capture_region_wayland(
        self,
        output_path: Path,
    ) -> CaptureResult:
        """Capture region on Wayland using slurp + grim."""
        geometry = self.slurp.select_region()

        if not geometry:
            raise RuntimeError("No region selected")

        parsed = self.slurp.parse_geometry(geometry)
        path = self.grim.capture_region(geometry, output_path)

        return CaptureResult(image_path=path, geometry=parsed)

    def _capture_region_x11(
        self,
        output_path: Path,
    ) -> CaptureResult:
        """Capture region on X11 using scrot."""
        path = self.scrot.capture_region(output_path)
        return CaptureResult(image_path=path)

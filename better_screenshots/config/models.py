"""Config data classes."""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class CaptureConfig:
    """Capture settings."""
    default_format: str = "png"
    save_directory: str = "~/Pictures/Screenshots"
    naming_pattern: str = "screenshot_%Y%m%d_%H%M%S"
    default_mode: str = "region"
    delay_seconds: int = 0


@dataclass
class BackgroundGradient:
    """Gradient background settings."""
    enabled: bool = True
    start_color: str = "#ff5858"
    end_color: str = "#ffc8c8"
    direction: str = "horizontal"


@dataclass
class BackgroundImage:
    """Image background settings."""
    enabled: bool = False
    path: str = ""
    fit: str = "cover"
    opacity: float = 1.0


@dataclass
class BackgroundConfig:
    """Background settings."""
    default_type: str = "gradient"
    default_color: str = "#1a1a2e"
    padding: int = 32
    shadow_enabled: bool = True
    shadow_blur: int = 20
    shadow_offset_x: int = 0
    shadow_offset_y: int = 10
    shadow_color: str = "#000000"
    frame_enabled: bool = True
    frame_width: int = 0
    frame_color: str = "#ffffff"
    frame_radius: int = 16
    background_radius: int = 16
    gradient: BackgroundGradient = field(default_factory=BackgroundGradient)
    image: BackgroundImage = field(default_factory=BackgroundImage)


@dataclass
class OutputConfig:
    """Output settings."""
    jpeg_quality: int = 90
    png_compression: int = 6
    copy_to_clipboard: bool = True
    show_save_dialog: bool = False


@dataclass
class CloudSelfHosted:
    """Self-hosted cloud settings."""
    api_url: str = ""
    api_key: str = ""


@dataclass
class CloudThirdParty:
    """Third-party cloud settings."""
    service: str = "imgur"
    api_key: str = ""


@dataclass
class CloudAdvanced:
    """Cloud advanced settings."""
    auto_upload: bool = False
    copy_link_to_clipboard: bool = True
    delete_after_days: int = 30


@dataclass
class CloudConfig:
    """Cloud hosting settings."""
    enabled: bool = False
    provider: str = "self_hosted"
    self_hosted: CloudSelfHosted = field(default_factory=CloudSelfHosted)
    third_party: CloudThirdParty = field(default_factory=CloudThirdParty)
    advanced: CloudAdvanced = field(default_factory=CloudAdvanced)


@dataclass
class Preset:
    """Preset template."""
    name: str
    width: int = 1080
    height: int = 1080
    background_type: str = "solid"
    background_color: str = "#1a1a2e"
    gradient_start: str = "#1a1a2e"
    gradient_end: str = "#16213e"
    padding: int = 32


@dataclass
class Config:
    """Main configuration."""
    capture: CaptureConfig = field(default_factory=CaptureConfig)
    background: BackgroundConfig = field(default_factory=BackgroundConfig)
    output: OutputConfig = field(default_factory=OutputConfig)
    cloud: CloudConfig = field(default_factory=CloudConfig)
    presets: list[Preset] = field(default_factory=list)

    @classmethod
    def default_presets(cls) -> list[Preset]:
        """Return default presets."""
        return [
            Preset(
                name="Instagram Post",
                width=1080,
                height=1080,
                background_type="solid",
                background_color="#1a1a2e",
                padding=40,
            ),
            Preset(
                name="Twitter Image",
                width=1200,
                height=675,
                background_type="gradient",
                gradient_start="#1a1a2e",
                gradient_end="#16213e",
                padding=32,
            ),
        ]

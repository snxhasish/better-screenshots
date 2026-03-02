"""Config manager - load, save, and watch config files."""

import json
from pathlib import Path
from typing import Optional

import toml
import yaml

from .models import (
    BackgroundConfig,
    BackgroundGradient,
    BackgroundImage,
    CaptureConfig,
    CloudAdvanced,
    CloudConfig,
    CloudSelfHosted,
    CloudThirdParty,
    Config,
    OutputConfig,
    Preset,
)
from .parser import ConfigParser


class ConfigManager:
    """Manage configuration loading and saving."""

    CONFIG_DIR = Path.home() / ".config" / "better-screenshots"
    CONFIG_FILES = ["config.toml", "config.json", "config.yaml"]

    def __init__(self):
        self.config: Optional[Config] = None
        self.config_path: Optional[Path] = None

    def get_config_dir(self) -> Path:
        """Get config directory, create if not exists."""
        self.CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        return self.CONFIG_DIR

    def find_config_file(self) -> Optional[Path]:
        """Find the first existing config file."""
        config_dir = self.get_config_dir()
        for filename in self.CONFIG_FILES:
            path = config_dir / filename
            if path.exists():
                return path
        return None

    def load_config(self) -> Config:
        """Load config from file or create default."""
        config_file = self.find_config_file()

        if config_file:
            self.config_path = config_file
            data = ConfigParser.parse_file(config_file)
            self.config = self._parse_config_data(data)
        else:
            self.config = self._create_default_config()
            self.config_path = self.get_config_dir() / "config.toml"

        return self.config

    def _parse_config_data(self, data: dict) -> Config:
        """Parse raw config data into Config object."""
        capture_data = data.get("capture", {})
        capture = CaptureConfig(
            default_format=capture_data.get("default_format", "png"),
            save_directory=capture_data.get("save_directory", "~/Pictures/Screenshots"),
            naming_pattern=capture_data.get("naming_pattern", "screenshot_%Y%m%d_%H%M%S"),
            default_mode=capture_data.get("default_mode", "region"),
            delay_seconds=capture_data.get("delay_seconds", 0),
        )

        bg_data = data.get("background", {})
        gradient_data = bg_data.get("gradient", {})
        gradient = BackgroundGradient(
            enabled=gradient_data.get("enabled", False),
            start_color=gradient_data.get("start_color", "#1a1a2e"),
            end_color=gradient_data.get("end_color", "#16213e"),
            direction=gradient_data.get("direction", "vertical"),
        )
        image_data = bg_data.get("image", {})
        image = BackgroundImage(
            enabled=image_data.get("enabled", False),
            path=image_data.get("path", ""),
            fit=image_data.get("fit", "cover"),
            opacity=image_data.get("opacity", 1.0),
        )
        background = BackgroundConfig(
            default_type=bg_data.get("default_type", "solid"),
            default_color=bg_data.get("default_color", "#1a1a2e"),
            padding=bg_data.get("padding", 32),
            shadow_enabled=bg_data.get("shadow_enabled", True),
            shadow_blur=bg_data.get("shadow_blur", 20),
            shadow_offset_x=bg_data.get("shadow_offset_x", 0),
            shadow_offset_y=bg_data.get("shadow_offset_y", 10),
            shadow_color=bg_data.get("shadow_color", "#000000"),
            frame_enabled=bg_data.get("frame_enabled", False),
            frame_width=bg_data.get("frame_width", 0),
            frame_color=bg_data.get("frame_color", "#ffffff"),
            frame_radius=bg_data.get("frame_radius", 0),
            gradient=gradient,
            image=image,
        )

        output_data = data.get("output", {})
        output = OutputConfig(
            jpeg_quality=output_data.get("jpeg_quality", 90),
            png_compression=output_data.get("png_compression", 6),
            copy_to_clipboard=output_data.get("copy_to_clipboard", True),
            show_save_dialog=output_data.get("show_save_dialog", False),
        )

        cloud_data = data.get("cloud", {})
        self_hosted_data = cloud_data.get("self_hosted", {})
        self_hosted = CloudSelfHosted(
            api_url=self_hosted_data.get("api_url", ""),
            api_key=self_hosted_data.get("api_key", ""),
        )
        third_party_data = cloud_data.get("third_party", {})
        third_party = CloudThirdParty(
            service=third_party_data.get("service", "imgur"),
            api_key=third_party_data.get("api_key", ""),
        )
        advanced_data = cloud_data.get("advanced", {})
        advanced = CloudAdvanced(
            auto_upload=advanced_data.get("auto_upload", False),
            copy_link_to_clipboard=advanced_data.get("copy_link_to_clipboard", True),
            delete_after_days=advanced_data.get("delete_after_days", 30),
        )
        cloud = CloudConfig(
            enabled=cloud_data.get("enabled", False),
            provider=cloud_data.get("provider", "self_hosted"),
            self_hosted=self_hosted,
            third_party=third_party,
            advanced=advanced,
        )

        presets = []
        for preset_data in data.get("presets", []):
            presets.append(Preset(
                name=preset_data.get("name", "Custom"),
                width=preset_data.get("width", 1080),
                height=preset_data.get("height", 1080),
                background_type=preset_data.get("background_type", "solid"),
                background_color=preset_data.get("background_color", "#1a1a2e"),
                gradient_start=preset_data.get("gradient_start", "#1a1a2e"),
                gradient_end=preset_data.get("gradient_end", "#16213e"),
                padding=preset_data.get("padding", 32),
            ))

        if not presets:
            presets = Config.default_presets()

        return Config(
            capture=capture,
            background=background,
            output=output,
            cloud=cloud,
            presets=presets,
        )

    def _create_default_config(self) -> Config:
        """Create default configuration."""
        return Config(presets=Config.default_presets())

    def save_config(self, config: Optional[Config] = None) -> None:
        """Save config to file."""
        if config:
            self.config = config

        if not self.config:
            self.config = self._create_default_config()

        config_path = self.config_path or self.get_config_dir() / "config.toml"
        data = self._config_to_dict(self.config)

        if config_path.suffix == ".toml":
            content = toml.dumps(data)
        elif config_path.suffix == ".json":
            import json
            content = json.dumps(data, indent=2)
        else:
            content = yaml.dump(data)

        with open(config_path, "w", encoding="utf-8") as f:
            f.write(content)

    def _config_to_dict(self, config: Config) -> dict:
        """Convert Config object to dictionary."""
        return {
            "capture": {
                "default_format": config.capture.default_format,
                "save_directory": config.capture.save_directory,
                "naming_pattern": config.capture.naming_pattern,
                "default_mode": config.capture.default_mode,
                "delay_seconds": config.capture.delay_seconds,
            },
            "background": {
                "default_type": config.background.default_type,
                "default_color": config.background.default_color,
                "padding": config.background.padding,
                "shadow_enabled": config.background.shadow_enabled,
                "shadow_blur": config.background.shadow_blur,
                "shadow_offset_x": config.background.shadow_offset_x,
                "shadow_offset_y": config.background.shadow_offset_y,
                "shadow_color": config.background.shadow_color,
                "frame_enabled": config.background.frame_enabled,
                "frame_width": config.background.frame_width,
                "frame_color": config.background.frame_color,
                "frame_radius": config.background.frame_radius,
                "gradient": {
                    "enabled": config.background.gradient.enabled,
                    "start_color": config.background.gradient.start_color,
                    "end_color": config.background.gradient.end_color,
                    "direction": config.background.gradient.direction,
                },
                "image": {
                    "enabled": config.background.image.enabled,
                    "path": config.background.image.path,
                    "fit": config.background.image.fit,
                    "opacity": config.background.image.opacity,
                },
            },
            "output": {
                "jpeg_quality": config.output.jpeg_quality,
                "png_compression": config.output.png_compression,
                "copy_to_clipboard": config.output.copy_to_clipboard,
                "show_save_dialog": config.output.show_save_dialog,
            },
            "cloud": {
                "enabled": config.cloud.enabled,
                "provider": config.cloud.provider,
                "self_hosted": {
                    "api_url": config.cloud.self_hosted.api_url,
                    "api_key": config.cloud.self_hosted.api_key,
                },
                "third_party": {
                    "service": config.cloud.third_party.service,
                    "api_key": config.cloud.third_party.api_key,
                },
                "advanced": {
                    "auto_upload": config.cloud.advanced.auto_upload,
                    "copy_link_to_clipboard": config.cloud.advanced.copy_link_to_clipboard,
                    "delete_after_days": config.cloud.advanced.delete_after_days,
                },
            },
            "presets": [
                {
                    "name": p.name,
                    "width": p.width,
                    "height": p.height,
                    "background_type": p.background_type,
                    "background_color": p.background_color,
                    "gradient_start": p.gradient_start,
                    "gradient_end": p.gradient_end,
                    "padding": p.padding,
                }
                for p in config.presets
            ],
        }

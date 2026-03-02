"""Config parser for TOML/JSON/YAML files."""

import json
from pathlib import Path
from typing import Any, Optional

import toml
import yaml


class ConfigParser:
    """Parse config files in multiple formats."""

    @staticmethod
    def parse_toml(content: str) -> dict[str, Any]:
        """Parse TOML content."""
        return toml.loads(content)

    @staticmethod
    def parse_json(content: str) -> dict[str, Any]:
        """Parse JSON content."""
        return json.loads(content)

    @staticmethod
    def parse_yaml(content: str) -> dict[str, Any]:
        """Parse YAML content."""
        return yaml.safe_load(content)

    @staticmethod
    def detect_format(file_path: Path) -> Optional[str]:
        """Detect config file format from extension."""
        ext = file_path.suffix.lower()
        if ext == ".toml":
            return "toml"
        elif ext == ".json":
            return "json"
        elif ext in (".yaml", ".yml"):
            return "yaml"
        return None

    @staticmethod
    def parse_file(file_path: Path) -> dict[str, Any]:
        """Parse config file based on extension."""
        format_type = ConfigParser.detect_format(file_path)
        if not format_type:
            raise ValueError(f"Unsupported config format: {file_path.suffix}")

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        if format_type == "toml":
            return ConfigParser.parse_toml(content)
        elif format_type == "json":
            return ConfigParser.parse_json(content)
        elif format_type == "yaml":
            return ConfigParser.parse_yaml(content)

        raise ValueError(f"Unsupported config format: {format_type}")

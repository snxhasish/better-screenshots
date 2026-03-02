"""Imgur cloud provider."""

from pathlib import Path
from typing import Optional


class ImgurProvider:
    """Imgur cloud provider."""

    def __init__(self, api_key: str):
        self.api_key = api_key

    def upload(self, image_path: Path) -> Optional[str]:
        """Upload to Imgur."""
        import requests

        try:
            with open(image_path, "rb") as f:
                files = {"image": f}
                headers = {"Authorization": f"Client-ID {self.api_key}"}
                response = requests.post(
                    "https://api.imgur.com/3/image",
                    files=files,
                    headers=headers,
                    timeout=30,
                )

            if response.status_code == 200:
                data = response.json()
                return data.get("data", {}).get("link")

        except Exception:
            pass

        return None

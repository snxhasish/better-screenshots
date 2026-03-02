"""Cloud upload service."""

from pathlib import Path
from typing import Optional


class UploadService:
    """Upload screenshots to cloud services."""

    def __init__(self, config):
        self.config = config
        self.enabled = config.cloud.enabled

    def upload(self, image_path: Path) -> Optional[str]:
        """Upload image to configured cloud service."""
        if not self.enabled:
            return None

        provider = self.config.cloud.provider

        if provider == "self_hosted":
            return self._upload_self_hosted(image_path)
        elif provider == "imgur":
            return self._upload_imgur(image_path)
        elif provider == "cloudinary":
            return self._upload_cloudinary(image_path)
        elif provider == "s3":
            return self._upload_s3(image_path)

        return None

    def _upload_self_hosted(self, image_path: Path) -> Optional[str]:
        """Upload to self-hosted server."""
        import requests

        api_url = self.config.cloud.self_hosted.api_url
        api_key = self.config.cloud.self_hosted.api_key

        if not api_url or not api_key:
            return None

        try:
            with open(image_path, "rb") as f:
                files = {"file": f}
                headers = {"Authorization": f"Bearer {api_key}"}
                response = requests.post(
                    f"{api_url}/upload",
                    files=files,
                    headers=headers,
                    timeout=30,
                )

            if response.status_code == 200:
                data = response.json()
                return f"{api_url}/s/{data.get('code', '')}"

        except Exception:
            pass

        return None

    def _upload_imgur(self, image_path: Path) -> Optional[str]:
        """Upload to Imgur."""
        import requests

        api_key = self.config.cloud.third_party.api_key

        if not api_key:
            return None

        try:
            with open(image_path, "rb") as f:
                files = {"image": f}
                headers = {"Authorization": f"Client-ID {api_key}"}
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

    def _upload_cloudinary(self, image_path: Path) -> Optional[str]:
        """Upload to Cloudinary."""
        return None

    def _upload_s3(self, image_path: Path) -> Optional[str]:
        """Upload to S3."""
        return None

"""Self-hosted cloud provider."""

from pathlib import Path
from typing import Optional


class SelfHostedProvider:
    """Self-hosted cloud provider."""

    def __init__(self, api_url: str, api_key: str):
        self.api_url = api_url
        self.api_key = api_key

    def upload(self, image_path: Path) -> Optional[str]:
        """Upload to self-hosted server."""
        import requests

        try:
            with open(image_path, "rb") as f:
                files = {"file": f}
                headers = {"Authorization": f"Bearer {self.api_key}"}
                response = requests.post(
                    f"{self.api_url}/upload",
                    files=files,
                    headers=headers,
                    timeout=30,
                )

            if response.status_code == 200:
                data = response.json()
                return f"{self.api_url}/s/{data.get('code', '')}"

        except Exception:
            pass

        return None

    def get_links(self) -> list:
        """Get list of uploaded links."""
        import requests

        try:
            headers = {"Authorization": f"Bearer {self.api_key}"}
            response = requests.get(
                f"{self.api_url}/links",
                headers=headers,
                timeout=10,
            )

            if response.status_code == 200:
                return response.json().get("links", [])

        except Exception:
            pass

        return []

    def delete_link(self, code: str) -> bool:
        """Delete a link."""
        import requests

        try:
            headers = {"Authorization": f"Bearer {self.api_key}"}
            response = requests.delete(
                f"{self.api_url}/links/{code}",
                headers=headers,
                timeout=10,
            )

            return response.status_code == 200

        except Exception:
            pass

        return False

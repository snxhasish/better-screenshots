"""Background renderer - creates solid, gradient, and image backgrounds."""

from io import BytesIO
from pathlib import Path
from typing import Optional

from PIL import Image


class BackgroundRenderer:
    """Render different types of backgrounds."""

    @staticmethod
    def hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
        """Convert hex color to RGB tuple."""
        hex_color = hex_color.lstrip("#")
        return (int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16))

    def render_solid(
        self,
        width: int,
        height: int,
        color: str,
    ) -> Image.Image:
        """Render solid color background."""
        rgb = self.hex_to_rgb(color)
        return Image.new("RGBA", (width, height), rgb + (255,))

    def render_gradient(
        self,
        width: int,
        height: int,
        start_color: str,
        end_color: str,
        direction: str = "vertical",
    ) -> Image.Image:
        """Render gradient background."""
        start_rgb = self.hex_to_rgb(start_color)
        end_rgb = self.hex_to_rgb(end_color)

        gradient = Image.new("RGBA", (width, height))
        pixels = gradient.load()

        for y in range(height):
            ratio = y / height if direction == "vertical" else 0
            if direction == "horizontal":
                ratio = 0
            elif direction == "diagonal":
                ratio = (y / height + 0) / 2

            r = int(start_rgb[0] + (end_rgb[0] - start_rgb[0]) * ratio)
            g = int(start_rgb[1] + (end_rgb[1] - start_rgb[1]) * ratio)
            b = int(start_rgb[2] + (end_rgb[2] - start_rgb[2]) * ratio)

            for x in range(width):
                if direction == "horizontal":
                    ratio = x / width
                    r = int(start_rgb[0] + (end_rgb[0] - start_rgb[0]) * ratio)
                    g = int(start_rgb[1] + (end_rgb[1] - start_rgb[1]) * ratio)
                    b = int(start_rgb[2] + (end_rgb[2] - start_rgb[2]) * ratio)
                elif direction == "diagonal":
                    ratio = (y / height + x / width) / 2
                    r = int(start_rgb[0] + (end_rgb[0] - start_rgb[0]) * ratio)
                    g = int(start_rgb[1] + (end_rgb[1] - start_rgb[1]) * ratio)
                    b = int(start_rgb[2] + (end_rgb[2] - start_rgb[2]) * ratio)

                pixels[x, y] = (r, g, b, 255)

        return gradient

    def render_image(
        self,
        width: int,
        height: int,
        image_path: str,
        fit: str = "cover",
        opacity: float = 1.0,
    ) -> Image.Image:
        """Render image background."""
        bg = Image.new("RGBA", (width, height), (0, 0, 0, 0))

        img = Image.open(image_path).convert("RGBA")

        if fit == "cover":
            img = self._cover_resize(img, width, height)
        elif fit == "contain":
            img = self._contain_resize(img, width, height)
        elif fit == "stretch":
            img = img.resize((width, height), Image.LANCZOS)

        if opacity < 1.0:
            img = Image.new("RGBA", img.size)
            alpha = int(255 * opacity)
            for x in range(img.width):
                for y in range(img.height):
                    r, g, b, a = img.getpixel((x, y))
                    img.putpixel((x, y), (r, g, b, a))

        paste_x = (width - img.width) // 2
        paste_y = (height - img.height) // 2
        bg.paste(img, (paste_x, paste_y), img)

        return bg

    def _cover_resize(self, img: Image.Image, width: int, height: int) -> Image.Image:
        """Resize image to cover dimensions."""
        img_ratio = img.width / img.height
        target_ratio = width / height

        if img_ratio > target_ratio:
            new_height = height
            new_width = int(height * img_ratio)
        else:
            new_width = width
            new_height = int(width / img_ratio)

        img = img.resize((new_width, new_height), Image.LANCZOS)

        left = (new_width - width) // 2
        top = (new_height - height) // 2
        img = img.crop((left, top, left + width, top + height))

        return img

    def _contain_resize(self, img: Image.Image, width: int, height: int) -> Image.Image:
        """Resize image to fit within dimensions."""
        img_ratio = img.width / img.height
        target_ratio = width / height

        if img_ratio > target_ratio:
            new_width = width
            new_height = int(width / img_ratio)
        else:
            new_height = height
            new_width = int(height * img_ratio)

        img = img.resize((new_width, new_height), Image.LANCZOS)
        return img

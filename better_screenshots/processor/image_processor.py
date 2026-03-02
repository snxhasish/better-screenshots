"""Image processor - applies background, shadow, padding to screenshots."""

from pathlib import Path
from typing import Optional

from PIL import Image, ImageDraw, ImageFilter

from ..config.models import BackgroundConfig, Preset
from .background import BackgroundRenderer


class ImageProcessor:
    """Process screenshots with background and effects."""

    def __init__(self):
        self.bg_renderer = BackgroundRenderer()

    def process_screenshot(
        self,
        image_path: Path,
        background: BackgroundConfig,
        preset: Optional[Preset] = None,
    ) -> Image.Image:
        """Process screenshot with background and effects."""
        screenshot = Image.open(image_path).convert("RGBA")

        target_width = preset.width if preset else screenshot.width + background.padding * 2
        target_height = preset.height if preset else screenshot.height + background.padding * 2

        background_image = self._create_background(
            target_width,
            target_height,
            background,
            preset,
        )

        processed = self._composite_screenshot(
            background_image,
            screenshot,
            background,
            preset,
        )

        if background.frame_enabled and background.frame_width > 0:
            processed = self._add_frame(processed, background)

        return processed

    def _create_background(
        self,
        width: int,
        height: int,
        background: BackgroundConfig,
        preset: Optional[Preset] = None,
    ) -> Image.Image:
        """Create background based on config."""
        bg_type = preset.background_type if preset else background.default_type
        bg_color = preset.background_color if preset else background.default_color

        if bg_type == "solid":
            return self.bg_renderer.render_solid(width, height, bg_color)
        elif bg_type == "gradient":
            if preset:
                start = preset.gradient_start
                end = preset.gradient_end
            else:
                start = background.gradient.start_color
                end = background.gradient.end_color
            direction = background.gradient.direction
            return self.bg_renderer.render_gradient(width, height, start, end, direction)
        elif bg_type == "image":
            return self.bg_renderer.render_image(
                width,
                height,
                background.image.path,
                background.image.fit,
                background.image.opacity,
            )
        else:
            return self.bg_renderer.render_solid(width, height, bg_color)

    def _composite_screenshot(
        self,
        background: Image.Image,
        screenshot: Image.Image,
        background_config: BackgroundConfig,
        preset: Optional[Preset],
    ) -> Image.Image:
        """Composite screenshot onto background with shadow and padding."""
        padding = preset.padding if preset else background_config.padding

        if background_config.shadow_enabled:
            screenshot = self._add_shadow(screenshot, background_config)

        paste_x = padding + background_config.shadow_offset_x
        paste_y = padding + background_config.shadow_offset_y

        result = background.copy()
        result.paste(screenshot, (paste_x, paste_y), screenshot)

        return result

    def _add_shadow(
        self,
        image: Image.Image,
        config: BackgroundConfig,
    ) -> Image.Image:
        """Add shadow to image."""
        shadow_color = self.bg_renderer.hex_to_rgb(config.shadow_color)

        shadow = Image.new("RGBA", image.size, (0, 0, 0, 0))
        shadow_draw = ImageDraw.Draw(shadow)
        shadow_draw.rectangle(
            [(0, 0), (image.width - 1, image.height - 1)],
            fill=(*shadow_color, 180),
        )

        shadow = shadow.filter(ImageFilter.GaussianBlur(config.shadow_blur))

        offset_x = config.shadow_offset_x
        offset_y = config.shadow_offset_y

        result = Image.new("RGBA", (
            image.width + abs(offset_x) + config.shadow_blur * 2,
            image.height + abs(offset_y) + config.shadow_blur * 2,
        ), (0, 0, 0, 0))

        result.paste(shadow, (max(0, -offset_x) + config.shadow_blur, max(0, -offset_y) + config.shadow_blur), shadow)
        result.paste(image, (config.shadow_blur, config.shadow_blur), image)

        return result

    def _add_frame(
        self,
        image: Image.Image,
        config: BackgroundConfig,
    ) -> Image.Image:
        """Add frame/border around image."""
        frame_width = config.frame_width
        frame_color = self.bg_renderer.hex_to_rgb(config.frame_color)

        new_width = image.width + frame_width * 2
        new_height = image.height + frame_width * 2

        result = Image.new("RGBA", (new_width, new_height), frame_color + (255,))

        if config.frame_radius > 0:
            mask = Image.new("L", (new_width, new_height), 0)
            mask_draw = ImageDraw.Draw(mask)
            mask_draw.rounded_rectangle(
                [(0, 0), (new_width - 1, new_height - 1)],
                radius=config.frame_radius,
                fill=255,
            )
            result.putalpha(mask)

        result.paste(image, (frame_width, frame_width), image)

        return result

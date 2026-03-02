"""CLI commands using click."""

import sys
from pathlib import Path
from typing import Optional

import click

from ..capture.capture_service import CaptureService
from ..config.manager import ConfigManager
from ..output.clipboard import Clipboard
from ..output.saver import ImageSaver
from ..processor.image_processor import ImageProcessor


@click.group()
@click.version_option(version="0.1.0")
def cli():
    """Better Screenshots - Screenshot tool with background customization."""
    pass


@cli.command()
@click.option(
    "--mode",
    type=click.Choice(["fullscreen", "window", "region"], case_sensitive=False),
    default=None,
    help="Capture mode",
)
@click.option(
    "--format",
    "output_format",
    type=click.Choice(["png", "jpg", "jpeg", "webp"], case_sensitive=False),
    default=None,
    help="Output format",
)
@click.option(
    "--delay",
    type=int,
    default=None,
    help="Delay in seconds before capture",
)
@click.option(
    "--preset",
    type=str,
    default=None,
    help="Preset name to use",
)
@click.option(
    "--clipboard-only",
    is_flag=True,
    help="Only copy to clipboard, don't save",
)
@click.option(
    "--upload",
    is_flag=True,
    help="Upload to cloud after capture",
)
@click.option(
    "--output",
    type=click.Path(path_type=Path),
    default=None,
    help="Output file path",
)
def capture(
    mode: Optional[str],
    output_format: Optional[str],
    delay: Optional[int],
    preset: Optional[str],
    clipboard_only: bool,
    upload: bool,
    output: Optional[Path],
):
    """Capture a screenshot."""
    config_manager = ConfigManager()
    config = config_manager.load_config()

    capture_service = CaptureService()

    if not capture_service.is_available():
        click.echo("Error: No screenshot backend available (grim or scrot)", err=True)
        sys.exit(1)

    mode = mode or config.capture.default_mode
    delay = delay if delay is not None else config.capture.delay_seconds
    output_format = output_format or config.capture.default_format

    try:
        click.echo(f"Capturing screenshot in {mode} mode...")
        result = capture_service.capture(mode=mode, delay=delay)

        click.echo("Processing image...")
        processor = ImageProcessor()

        selected_preset = None
        if preset:
            for p in config.presets:
                if p.name.lower() == preset.lower():
                    selected_preset = p
                    break
            if not selected_preset:
                click.echo(f"Warning: Preset '{preset}' not found, using default", err=True)

        processed_image = processor.process_screenshot(
            result.image_path,
            config.background,
            selected_preset,
        )

        if clipboard_only:
            click.echo("Copying to clipboard...")
            temp_path = Path("/tmp/better-screenshots-temp.png")
            saver = ImageSaver()
            saver.save_image(processed_image, temp_path, "PNG")

            clipboard = Clipboard()
            if clipboard.copy_image(temp_path):
                click.echo("Copied to clipboard!")
            else:
                click.echo("Failed to copy to clipboard", err=True)

            temp_path.unlink(missing_ok=True)
        else:
            if output:
                save_path = output
            else:
                saver = ImageSaver()
                save_path = saver.get_next_filename(
                    config.capture.save_directory,
                    config.capture.naming_pattern,
                    output_format,
                )

            click.echo(f"Saving to {save_path}...")
            saver = ImageSaver()
            saver.save_image(processed_image, save_path, output_format, config.output.jpeg_quality)
            click.echo(f"Saved to {save_path}")

            if config.output.copy_to_clipboard:
                click.echo("Copying to clipboard...")
                clipboard = Clipboard()
                clipboard.copy_image(save_path)

        if upload or config.cloud.advanced.auto_upload:
            click.echo("Uploading to cloud...")
            click.echo("Cloud upload not yet implemented")

        click.echo("Done!")

    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command()
def presets():
    """List available presets."""
    config_manager = ConfigManager()
    config = config_manager.load_config()

    click.echo("Available presets:")
    for preset in config.presets:
        click.echo(f"  - {preset.name} ({preset.width}x{preset.height})")


@cli.command()
def config_path():
    """Show config file path."""
    config_manager = ConfigManager()
    config_manager.load_config()

    if config_manager.config_path:
        click.echo(str(config_manager.config_path))
    else:
        click.echo("No config file found")


@cli.command()
def init_config():
    """Create default config file."""
    config_manager = ConfigManager()
    config_manager.load_config()
    config_manager.save_config()

    click.echo(f"Config created at {config_manager.config_path}")


if __name__ == "__main__":
    cli()

"""CLI entry point for better-screenshots."""

import sys
from .cli.commands import cli


def main():
    """Main entry point."""
    sys.exit(cli())


if __name__ == "__main__":
    main()

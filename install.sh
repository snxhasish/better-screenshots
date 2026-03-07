#!/bin/bash

set -e

VERSION="0.1.0"
INSTALL_DIR="${HOME}/.local/bin"
REPO="snhsish/better-screenshots"

echo "Installing better-screenshots v${VERSION}..."

# Detect platform
if [[ "$(uname -m)" == "aarch64" || "$(uname -m)" == "arm64" ]]; then
    PLATFORM="linux-aarch64"
else
    PLATFORM="linux-x86_64"
fi

# Create install directory
mkdir -p "$INSTALL_DIR"

# Download the binary
echo "Downloading better-screenshots for ${PLATFORM}..."
curl -sSL "https://github.com/${REPO}/releases/latest/download/better-screenshots-${PLATFORM}" -o "${INSTALL_DIR}/better-screenshots"
chmod +x "${INSTALL_DIR}/better-screenshots"

# Check dependencies
echo "Checking dependencies..."

# Check for grim
if ! command -v grim &> /dev/null; then
    echo "Warning: grim not found. Install via your package manager:"
    echo "  - Arch: sudo pacman -S grim"
    echo "  - Debian/Ubuntu: sudo apt install grim"
    echo "  - Fedora: sudo dnf install grim"
fi

# Check for slurp
if ! command -v slurp &> /dev/null; then
    echo "Warning: slurp not found. Install via your package manager:"
    echo "  - Arch: sudo pacman -S slurp"
    echo "  - Debian/Ubuntu: sudo apt install slurp"
    echo "  - Fedora: sudo dnf install slurp"
fi

# Check for wl-copy
if ! command -v wl-copy &> /dev/null; then
    echo "Warning: wl-copy not found (optional, for clipboard). Install via:"
    echo "  - Arch: sudo pacman -S wl-clipboard"
    echo "  - Debian/Ubuntu: sudo apt install wl-clipboard"
fi

echo ""
echo "Installation complete!"
echo "Add ${INSTALL_DIR} to your PATH if not already added."
echo "Run 'better-screenshots --help' to get started."

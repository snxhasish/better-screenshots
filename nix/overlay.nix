# Overlay for better-screenshots
#
# Add to your NixOS configuration:
#   nixpkgs.overlays = [ (import ./better-screenshots/nix/overlay.nix) ];
#
# Or in flake-based NixOS:
#   inputs.better-screenshots.url = "github:snxhasish/better-screenshots";
#   inputs.better-screenshots.overlays.default = final: prev: {
#     better-screenshots = final.callPackage ./better-screenshots/nix/default.nix {};
#   };

final: prev:
{
  better-screenshots = final.callPackage ./default.nix {
    grim = final.grim;
    slurp = final.slurp;
    wl-clipboard = final.wl-clipboard;
  };
}

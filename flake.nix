{
  description = "Better Screenshots - CLI screenshot tool for Linux with background customization";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; };
        python = pkgs.python3;

        better-screenshots = pkgs.python3Packages.buildPythonPackage {
          pname = "better-screenshots";
          version = "0.1.0";
          format = "pyproject";

          src = pkgs.fetchFromGitHub {
            owner = "snxhasish";
            repo = "better-screenshots";
            rev = "main";
            hash = "sha256-AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=";
          };

          dependencies = with pkgs.python3Packages; [
            click
            pillow
            toml
            pyyaml
            requests
          ];

          nativeCheckInputs = with pkgs; [
            grim
            slurp
            wl-clipboard
          ];

          postInstall = ''
            wrapProgram $out/bin/better-screenshots \
              --prefix PATH : "${pkgs.lib.makeBinPath [
                pkgs.grim
                pkgs.slurp
                pkgs.wl-clipboard
              ]}"
          '';

          meta = with pkgs.lib; {
            description = "CLI screenshot tool for Linux with background customization";
            homepage = "https://github.com/snxhasish/better-screenshots";
            license = licenses.mit;
            maintainers = [ ];
            platforms = platforms.linux;
          };
        };
      in
      {
        packages.default = better-screenshots;
        apps.default = flake-utils.lib.mkApp {
          drv = better-screenshots;
        };
        devShells.default = pkgs.mkShell {
          buildInputs = with pkgs; [
            python
            grim
            slurp
            wl-clipboard
          ];
        };
      }
    );
}

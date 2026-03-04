{ lib, python3, fetchFromGitHub, grim, slurp, wl-clipboard, ... }:

python3.pkgs.buildPythonPackage {
  pname = "better-screenshots";
  version = "0.1.0";

  src = fetchFromGitHub {
    owner = "snxhasish";
    repo = "better-screenshots";
    rev = "main";
    hash = "sha256-AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=";
  };

  format = "pyproject";

  dependencies = with python3.pkgs; [
    python3.pkgs.click
    python3.pkgs.pillow
    python3.pkgs.toml
    python3.pkgs.pyyaml
    python3.pkgs.requests
  ];

  postInstall = ''
    wrapProgram $out/bin/better-screenshots \
      --prefix PATH : "${lib.makeBinPath [ grim slurp wl-clipboard ]}"
  '';

  meta = with lib; {
    description = "CLI screenshot tool for Linux with background customization";
    homepage = "https://github.com/snxhasish/better-screenshots";
    license = licenses.mit;
    platforms = platforms.linux;
  };
}

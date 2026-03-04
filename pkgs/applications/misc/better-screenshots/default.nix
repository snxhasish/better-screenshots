{ lib, python3, fetchFromGitHub, grim, slurp, wl-clipboard, click, pillow, toml, pyyaml, requests }:

python3.pkgs.buildPythonPackage {
  pname = "better-screenshots";
  version = "0.1.0";

  src = fetchFromGitHub {
    owner = "snxhasish";
    repo = "better-screenshots";
    rev = "v${version}";
    hash = "sha256-AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=";
  };

  format = "pyproject";

  dependencies = [
    click
    pillow
    toml
    pyyaml
    requests
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
    maintainers = [ ];
  };
}

{ config, lib, pkgs, ... }:

with lib;

let
  cfg = config.programs.better-screenshots;
in
{
  options.programs.better-screenshots = {
    enable = mkEnableOption "Better Screenshots - CLI screenshot tool";

    package = mkOption {
      type = types.package;
      default = pkgs.better-screenshots;
      description = "The better-screenshots package to use.";
    };

    settings = mkOption {
      type = types.attrsOf types.anything;
      default = { };
      example = {
        capture = {
          default_mode = "region";
          default_format = "png";
        };
        background = {
          default_type = "gradient";
          gradient = {
            start_color = "#ff5858";
            end_color = "#ffc8c8";
            direction = "horizontal";
          };
        };
      };
      description = "Configuration for better-screenshots. See https://github.com/snxhasish/better-screenshots#configuration";
    };
  };

  config = mkIf cfg.enable {
    environment.systemPackages = [ cfg.package ];

    # Create config directory and write config if settings are provided
    systemd.tmpfiles.rules = mkIf (cfg.settings != { }) [
      "d ${config.xdg.configHome}/better-screenshots 0755 ${config.users.users.${config.users.forceUser ? "root" : "root"}.name} ${config.users.groups ? { }.wheel.name or ""} - -"
    ];

    environment.etc."better-screenshots/config.toml".text = mkIf (cfg.settings != { }) (
      let
        toToml = value:
          if builtins.isBool value then
            (if value then "true" else "false")
          else if builtins.isString value then
            ''"${value}"''
          else if builtins.isInt value then
            toString value
          else if builtins.isList value then
            "[" + builtins.concatMapStringsSep ", " toToml value + "]"
          else if builtins.isAttrs value then
            builtins.concatStringsSep "\n" (
              builtins.mapAttrsToList (name: val: "${name} = ${toToml val}") value
            )
          else
            builtins.toJSON value;
      in
      builtins.concatStringsSep "\n" (
        builtins.mapAttrsToList (section: values: 
          "[${section}]\n" + builtins.concatStringsSep "\n" (
            builtins.mapAttrsToList (key: value: "${key} = ${toToml value}") values
          )
        ) cfg.settings
      )
    );
  };

  meta.maintainers = [ ];
}

{
  description = "CodeVM agent environment";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

  outputs = { self, nixpkgs }:
    let
      system = "aarch64-linux";
      lib = nixpkgs.lib;
      pkgs = import nixpkgs {
        inherit system;
        config.allowUnfreePredicate = p: builtins.elem (lib.getName p) [ "claude-code" ];
      };
    in {
      packages.${system}.default = pkgs.buildEnv {
        name = "codevm-env";
        paths = import ./packages.nix pkgs;
      };
    };
}

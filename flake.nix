{
  description = "Logs of AI agents playing Dominion, and the runner that records them";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = {
    self,
    nixpkgs,
    flake-utils,
  }:
    flake-utils.lib.eachDefaultSystem (system: let
      pkgs = nixpkgs.legacyPackages.${system};
    in {
      packages.default = pkgs.writeShellApplication {
        name = "dominion-play";
        runtimeInputs = [pkgs.python3 pkgs.git];
        text = ''exec python3 ${./scripts/play.py} "$@"'';
      };

      devShells.default = pkgs.mkShell {
        packages = with pkgs; [just alejandra python3 ruff git];
      };

      formatter = pkgs.alejandra;
    });
}

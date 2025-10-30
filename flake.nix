{
  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";

  outputs = { self, nixpkgs }:
    let
      supportedSystems = [ "x86_64-linux" "x86_64-darwin" "aarch64-linux" "aarch64-darwin" ];
      forAllSystems = nixpkgs.lib.genAttrs supportedSystems;
      pkgs = forAllSystems (system: nixpkgs.legacyPackages.${system});
    in
    {
      devShells = forAllSystems (system:
        let
          python = pkgs.${system}.python3;
          pythonEnv = python.withPackages (ps: with ps; [
            pyopengl
            pyopengl-accelerate
            numpy
          ]);
        in {
          default = pkgs.${system}.mkShell {
            packages = with pkgs.${system}; [
              pythonEnv
              poetry
              freeglut
              libGL
              libGLU
              xorg.libX11
              xorg.libXext
            ];

            shellHook = ''
              export LD_LIBRARY_PATH=${pkgs.${system}.lib.makeLibraryPath [
                pkgs.${system}.freeglut
                pkgs.${system}.libGL
                pkgs.${system}.libGLU
                pkgs.${system}.xorg.libX11
                pkgs.${system}.xorg.libXext
              ]}:$LD_LIBRARY_PATH
              export PYOPENGL_PLATFORM=glx
            '';
          };
        }
      );
    };
}

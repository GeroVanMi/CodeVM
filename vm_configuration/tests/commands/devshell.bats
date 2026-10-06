#!/usr/bin/env bats
# The Nix dev shell (devShells.default in nix/flake.nix) for native npm builds.

load ../helpers

# Built and loaded like a node-gyp addon: compiled against gd, then
# required by the Nix node from the profile.
@test "dev shell builds a node addon that links gd" {
  run in_vm 'cd "$(mktemp -d)" && printf "#include <node_api.h>\n#include <gd.h>\nNAPI_MODULE_INIT() { gdImageDestroy(gdImageCreate(1, 1)); return exports; }\n" > a.c && timeout 300 nix develop --no-write-lock-file /opt/codevm/nix -c sh -c "gcc -shared -fPIC -I\$(dirname \$(readlink -f \$(command -v node)))/../include/node a.c -o a.node \$(pkg-config --cflags --libs gdlib)" && timeout 10 node -e "require(\"./a.node\")"'
  [ "$status" -eq 0 ]
}

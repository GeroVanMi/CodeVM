#!/usr/bin/env bash
# Non-nix package installs. Idempotent, runs as `agent`.
set -euo pipefail

# codegraph — move to packages.nix once in nixpkgs
if ! command -v codegraph >/dev/null 2>&1; then
  curl -fsSL https://raw.githubusercontent.com/colbymchenry/codegraph/main/install.sh | sh
else
  echo "codegraph: already installed, skipping"
fi

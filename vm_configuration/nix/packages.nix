# Each group has a matching tests/commands/<group>.bats.
pkgs: with pkgs; [
  # agents
  claude-code pi-coding-agent
  # vcs
  git gh worktrunk
  # cli
  ripgrep fd jq curl zoxide unzip
  # containers (podman itself is apt, see lima/codevm.yaml)
  docker-compose
  # editor
  neovim
  # languages (setuptools provides distutils for node-gyp < 10)
  nodejs pnpm (python3.withPackages (ps: [ ps.setuptools ]))
  # native build deps, mirroring apt's pkg-config + libgd-dev (gd.dev has headers/.pc)
  pkg-config gd gd.dev
]

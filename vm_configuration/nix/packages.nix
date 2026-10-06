# Each group has a matching tests/commands/<group>.bats.
pkgs: with pkgs; [
  # agents
  claude-code pi-coding-agent
  # vcs
  git gh worktrunk
  # cli
  ripgrep fd jq bat eza curl zoxide unzip rclone
  # containers (podman itself is apt, see lima/codevm.yaml)
  docker-compose
  # editor
  neovim
  # languages (setuptools provides distutils for node-gyp < 10)
  nodejs pnpm (python3.withPackages (ps: [ ps.setuptools ]))
  # native build deps, mirroring apt's pkg-config
  pkg-config
]

# Each group has a matching tests/commands/<group>.bats.
pkgs: with pkgs; [
  # agents
  claude-code pi-coding-agent
  # vcs
  git gh
  # cli
  ripgrep fd jq curl zoxide unzip
  # editor
  neovim
  # languages
  nodejs python3 gcc
]

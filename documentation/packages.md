# Packages

## Nix packages

Packages available to the `agent` user inside the VM are declared in
[`nix/packages.nix`](../nix/packages.nix), a list of Nix package names grouped by comments. Each group has a matching
file of checks in `tests/commands/` (see [testing](testing.md)).
The current list is claude-code, pi-coding-agent, git, gh, ripgrep, fd, jq,
curl, neovim, nodejs, python3, zoxide, unzip, and gcc.

To add or remove a package, edit `nix/packages.nix` on the host and run
`codevm sync` (see [usage](usage.md#sync)). Sync resets the `agent` user's Nix
profile to exactly the declared list, so any package installed ad hoc with
`nix profile add` inside the VM is removed on the next sync.

Only claude-code is allowed to be an unfree package; any other unfree package
added to the list fails to build.

## Extra, non-Nix packages

[`extra-packages.sh`](../extra-packages.sh) installs tools that are not
available through Nix. It runs as the `agent` user during sync, after the Nix
profile is applied. Each entry checks whether the tool is already installed
before running its installer, so re-running the script is a no-op for anything
already present.

The current entry installs codegraph to `~/.local/bin` using its own install
script. It is marked in the script for a move to `packages.nix` once it is
available in Nix's package repository, nixpkgs.

## Bumping the Nix lock file

[`nix/flake.lock`](../nix/flake.lock) pins the exact versions of packages
resolved by [`nix/flake.nix`](../nix/flake.nix). Sync never updates an existing
lock file; it only generates one if none exists yet.

Bumping the lock to pick up newer package versions is currently a manual step:
run `nix flake update` against a writable copy of `nix/` inside the VM, then
copy the resulting `flake.lock` back to the host. A future `codevm update`
subcommand could automate this, but it does not exist yet.

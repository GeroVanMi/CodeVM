# Packages

## Nix packages

Packages available to the `agent` user inside the VM are declared in
[`nix/packages.nix`](../nix/packages.nix), a list of Nix package names grouped
by comments. Each group has a matching file of checks in `tests/commands/` (see
[testing](testing.md)). The current list is claude-code, pi-coding-agent, git,
gh, worktrunk, ripgrep, fd, jq, curl, neovim, nodejs, python3, zoxide, rclone, and
unzip. python3 includes setuptools, which provides the `distutils` module that
node-gyp versions before 10 need.

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

## System packages

Podman is installed with apt, not Nix, together with its rootless helpers uidmap
and passt. The `agent` user runs podman rootless, without sudo.

`podman compose` runs docker-compose, which is installed with Nix from
`packages.nix`. Unlike podman, docker-compose is only a client, so it doesn't
need apt's file paths. It talks to podman through the rootless podman API
socket, a systemd user unit for `agent`. The provision script and `codevm sync`
enable it.

The C toolchain is also installed with apt: build-essential (gcc, make)
and pkg-config. Use it for C programs built and run outside node.
Native npm modules need the [Nix dev shell](#nix-dev-shell) instead.

The provision script in
[`lima/codevm.yaml`](../vm_configuration/lima/codevm.yaml) installs these
packages when the VM is created, and `codevm sync` installs any that are
missing. Sync also enables lingering for `agent`, which keeps its systemd user
instance running. Checks for these packages live in
`tests/commands/system.bats`.

To add another C library, add its `-dev` package to the apt lists in both the
provision script and `bin/codevm`.

## Nix dev shell

Native npm modules must link C libraries from Nix, because node comes from Nix
and cannot load libraries from `/usr/lib`. The dev shell in
[`nix/flake.nix`](../vm_configuration/nix/flake.nix) provides Nix's gcc
and pkg-config. Run native installs inside it:

```bash
nix develop /opt/codevm/nix -c npm ci
```

A plain `npm ci` still builds, against the apt libraries, but the module then
fails to load. Sync registers the dev shell as a garbage collection root, so the
libraries that built modules link to stay installed. To add a C library, add it
to `buildInputs` in the dev shell. Checks live in
`tests/commands/devshell.bats`.

## Bumping the Nix lock file

[`nix/flake.lock`](../nix/flake.lock) pins the exact versions of packages
resolved by [`nix/flake.nix`](../nix/flake.nix). Sync never updates an existing
lock file; it only generates one if none exists yet.

Bumping the lock to pick up newer package versions is currently a manual step:
run `nix flake update` against a writable copy of `nix/` inside the VM, then
copy the resulting `flake.lock` back to the host. A future `codevm update`
subcommand could automate this, but it does not exist yet.

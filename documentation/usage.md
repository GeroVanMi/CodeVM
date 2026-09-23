# Usage

## Subcommands

The `codevm` command supports the following subcommands.

### codevm (no argument)

Creates the VM if it does not exist, running a full sync as part of creation.
Starts the VM if it is stopped. Opens a shell inside the VM as the `agent` user,
in `~/projects`.

### sync

Pushes the repository's configuration into the running VM and applies it: Nix
packages, the firewall rules, the shell configuration, and the git identity from
[`config.env`](../config.env). See [packages](packages.md) for what a sync
changes about the installed package set. Sync does not enter a shell; it exits
once the VM is up to date.

### destroy

Deletes the VM. Before deleting, if the VM is running, `codevm` checks every git
repository under `~/projects` for uncommitted changes or commits that have not
been pushed to a remote. Any such repository is listed as dirty, because its
contents will be lost.

Regardless of whether dirty repositories were found, `codevm` then asks you to
confirm by typing `codevm` exactly. Any other input, including an empty line,
aborts the destroy and leaves the VM in place.

### rebuild

Runs destroy, then recreates the VM from scratch and syncs it. The same
dirty-repository check and typed confirmation from destroy apply.

## Unknown subcommands

Any argument other than `sync`, `destroy`, or `rebuild` prints usage information
and exits with status 2.

## Troubleshooting

### Warp hangs on shell entry

Entering the VM (`codevm` with no argument) drops into a shell via
`sudo -u agent -H`. On Ubuntu, sudo's default `use_pty` setting relays terminal
I/O through an extra pseudo-terminal it allocates for the command. This extra
relay layer can break Warp's terminal integration, which negotiates a handshake
with the shell on startup: Warp may hang for over a minute and stop responding
to Ctrl-C, requiring the tab or window to be closed.

`bin/codevm` works around this with a scoped sudoers rule,
`/etc/sudoers.d/90-codevm-agent-nopty`, that disables `use_pty` only for
commands targeting the `agent` user:

```
Defaults>agent !use_pty
```

This rule is installed by both the `lima/codevm.yaml` provision script and
`codevm sync`, so it is present on a fresh VM and restored if ever removed. It
does not affect `use_pty` for any other sudo use on the VM. If a future change
to the shell-entry command reintroduces a similar hang in another terminal
emulator, suspect the same mechanism: an intermediary pseudo-terminal
interfering with that terminal's own handshake or escape-sequence handling.

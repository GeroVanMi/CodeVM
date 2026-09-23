# Installation

## Prerequisites

CodeVM runs on macOS with the Lima virtual machine tool. You need:

- macOS on Apple silicon (arm64).
- Lima 2.2.0 or later, installed via Homebrew: `brew install lima`.
- Nix is not required on the host. Nix runs only inside the VM.

## Add codevm to your PATH

`bin/codevm` is the command that creates, starts, and enters the VM. Add it to
your shell's PATH by adding a line like this to your own `~/.zshrc`:

```sh
export PATH="PATH/TO/CodeVM/bin:$PATH"
```

Replace the path with wherever you cloned this repository. This project does not
edit your `~/.zshrc` for you; add the line yourself and open a new shell or run
`source ~/.zshrc`.

## First run

Run:

```sh
codevm
```

On the first run, this creates the `codevm` Lima VM from
[`lima/codevm.yaml`](../lima/codevm.yaml), then runs a sync that installs the
Nix environment, the firewall, and the shell configuration inside the VM. See
[usage](usage.md#sync) for what sync does. Once the sync finishes, `codevm`
drops you into a shell inside the VM, logged in as the `agent` user in
`~/projects`.

On later runs, `codevm` starts the VM if it is stopped and opens the same shell;
it does not sync again automatically. Run `codevm sync` to push further changes.

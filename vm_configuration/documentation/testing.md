# Testing

Tests run on the host against a disposable Test VM named `codevm-test`, built
from the working tree. They never touch the `codevm` VM that agents work in.

## Prerequisites

- [Lima](https://lima-vm.io), which provides `limactl`.
- [bats-core](https://github.com/bats-core/bats-core), installed with
  `brew install bats-core`.

## Running the tests

`bin/codevm-test` takes one optional argument:

- `fast` (default): creates `codevm-test` if it is missing, syncs the working
  tree into it with `codevm sync`, then runs every Command Check.
- `full`: deletes `codevm-test`, then creates, syncs, and checks it from
  scratch. Run this before committing changes to `lima/codevm.yaml` or
  `bin/codevm`.
- `stop`: stops `codevm-test` to free host resources.

The script refuses to run if `limactl` or `bats` is missing, or if the VM name
resolves to `codevm`. A run can regenerate `nix/flake.lock` if it is missing.

## Command Checks

A Command Check is a command that must succeed when run as the `agent` user
inside a freshly synced Test VM. Checks live in `tests/commands/`, one file per
group in [`nix/packages.nix`](../nix/packages.nix), plus `extras.bats` for
[`extra-packages.sh`](../extra-packages.sh). Every package has at least one
check.

Each check uses the `in_vm` helper from `tests/helpers.bash`, which runs its
argument as `agent` in a login shell:

```bash
@test "ripgrep" {
  run in_vm 'timeout 10 rg --version'
  [ "$status" -eq 0 ]
}
```

Every check bounds its own run time, usually with `timeout`, so a hanging
command fails instead of stalling the suite.

## Fixing a missing or broken command

1. Add a check for the command and run `bin/codevm-test` to see it fail.
2. Change the configuration until the check passes.

## VM name override

`bin/codevm` reads the VM name from `CODEVM_NAME` (default `codevm`). Setting
`CODEVM_DESTROY_YES=1` skips the destroy confirmation, but only when the name
is not `codevm`.

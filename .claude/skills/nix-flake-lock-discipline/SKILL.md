---
name: nix-flake-lock-discipline
description: How to add packages, update the Nix profile, or handle nix/flake.lock in this repo without accidentally bumping pinned dependency versions or breaking reproducibility. Use this whenever editing nix/packages.nix, nix/flake.nix, running any nix profile or nix flake command against the codevm VM, or when flake.lock is missing, out of date, or needs regenerating — even if the user just says something like "add ripgrep to the packages" or "the VM's tools are out of date", not only when they mention flake.lock by name.
---

# Keeping nix/flake.lock stable and intentional

`nix/flake.lock` pins the exact `nixpkgs` revision (and anything else the flake depends on) that every package version resolves against. Losing control of when it changes means the VM's tool versions can drift silently between one `codevm sync` and the next, defeating the whole point of declaring them in Nix.

## The rule: sync never bumps an existing lock

`codevm sync` must only regenerate `flake.lock` when it doesn't exist yet — never as a side effect of installing packages or resetting drift. If the host already has `nix/flake.lock`, a sync run copies it into the VM and uses it as-is; it does not run `nix flake update` or anything that could silently move the pin. If you're adding a new sync step, check whether it could implicitly write a lock file and add `--no-write-lock-file` (or equivalent) if so.

## Generating the lock the first time

`nix flake lock` needs a writable directory, but `/opt/codevm/nix` on the VM is intentionally root-owned and read-only to `agent`. The pattern:

1. As `agent`, copy the flake to a scratch writable location (e.g. `/tmp/...`), `chmod -R u+w` it.
2. Run `nix flake lock` there.
3. Copy the resulting `flake.lock` back to the **host** repo (`limactl copy`), so it's the one source of truth and gets committed.
4. Install that same lock file into `/opt/codevm/nix/flake.lock` (root-owned, 0644) so the applied config matches the repo.

## Resetting profile drift without touching the lock

To bring `agent`'s Nix profile back to exactly what's declared (undoing any ad hoc `nix profile add` the agent ran):

```
nix profile remove --regex '.*'
nix profile add --no-write-lock-file /opt/codevm/nix#default
```

`--regex '.*'` removes every profile entry and works across old and new Nix versions — the newer `--all` flag doesn't exist everywhere. `--no-write-lock-file` on the add is what stops this reset from silently rewriting the lock if it happens to resolve slightly differently.

## Adding a package

Edit `nix/packages.nix` (a plain list passed to `pkgs.buildEnv`), then `codevm sync`. Don't hand-add it via `nix profile add` on the live VM — that's exactly the kind of drift the reset step above is designed to undo on the next sync.

## Deliberately bumping the lock

There's no `codevm update` command yet (see `documentation/packages.md`) — bumping `nixpkgs` to pick up newer package versions is currently a manual step: run `nix flake update` in a writable copy inside the VM, then copy the new `flake.lock` back to the host and commit it. Treat this as a distinct, deliberate action, not something that happens as a byproduct of an unrelated sync.

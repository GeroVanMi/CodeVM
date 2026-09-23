---
name: safe-sudoers-edit
description: How to safely change sudo permissions or Defaults settings (e.g. use_pty, NOPASSWD, requiretty) on the codevm VM or any Linux host in this repo, without risking a syntax error that locks out sudo entirely. Use this whenever a task involves editing /etc/sudoers, adding a file under /etc/sudoers.d/, granting or restricting sudo access for a user, or troubleshooting sudo-related behavior — even if the user just says something like "give agent passwordless access to X" or "stop sudo from doing Y", not only when they say "sudoers" outright.
---

# Editing sudoers safely

A syntax error in `/etc/sudoers` breaks sudo for everyone on the box, including the person trying to fix it. Root shells and console access aside, this can be a genuinely bad afternoon. The tooling exists to make this near-impossible to get wrong — always use it.

## The procedure

1. **Never edit `/etc/sudoers` or files under `/etc/sudoers.d/` directly.** Write the new content to a temp file first (`mktemp`).
2. **Validate before installing.** Run `visudo -cf <tempfile>`. Only proceed if it exits 0.
3. **Install with the right ownership and permissions.** `install -m 0440 -o root -g root <tempfile> /etc/sudoers.d/<name>`. Sudoers files ignore anything not exactly 0440 and root-owned, so getting this wrong silently no-ops the change rather than erroring.
4. **Prefer a new drop-in file over editing an existing one.** `/etc/sudoers.d/` is read in lexical order after the main file; a small, purpose-named file (e.g. `90-codevm-agent-nopty`) is easier to reason about and revert than a diff buried in a large sudoers file.

## Scope narrowly

Sudoers `Defaults` settings exist for a reason (`use_pty` isolates the command's terminal, `requiretty` blocks non-interactive privilege escalation, etc.). When a setting needs relaxing for one specific case, scope it as tightly as the syntax allows instead of disabling it globally:

- `Defaults>targetuser !setting` applies only when the command's target user (via `sudo -u`) matches.
- `Defaults:invokinguser !setting` applies only when the invoking user matches.
- `Defaults!commandalias !setting` applies only to a specific command.

Example — the fix that unblocked Warp terminal's handshake through `sudo -u agent`, where the default pty-relay behavior was interfering with an interactive terminal protocol:

```
# codevm-managed: no pty relay for commands run as agent (Warp)
Defaults>agent !use_pty
```

This leaves `use_pty` intact for every other sudo invocation on the box. A blanket `Defaults !use_pty` would have "worked" too, but it throws away a security control for cases that never needed the exception.

## In this repo specifically

`bin/codevm sync` already contains a working example of this whole pattern (temp file → `visudo -cf` → `install -m 0440`) — read that function before writing a new one from scratch. If the change should survive a VM rebuild, it needs to live in the `lima/codevm.yaml` provision script (idempotent, since that script reruns on every boot) as well as in `sync`.

# HANDOVER — CodeVM build plan

One Lima VM (`codevm`) that isolates coding agents. The host enters it with `codevm`. Packages are declared with Nix. All decisions below are **settled with the user**, so don't re-open them. Items under "Open points" are yours to resolve, and you must report what you chose.

## Context / facts (verified 2026-09-23)

- Host: macOS, arm64, zsh. `limactl` 2.2.0 via Homebrew. **No Nix on host.**
- Repo `/Users/gero/Gists/CodeVM`: empty, branch `main`, no commits.
- Existing Lima VM `agents` (vz, running). It **gets replaced**, but see M0.
- Commit, push or edit host dotfiles **only if the user asks**.

## Settled decisions

| # | Decision |
|---|---|
| VM | One VM, name `codevm`, Lima `vmType: vz`, arm64, **Ubuntu 26.04.1 LTS** cloud image, 6 CPU / 12GiB / 100GiB |
| Mounts | `mounts: []`. **Zero** host mounts. Code moves only via git clone/pull/push |
| Users | Lima default user = admin (sudo). Agents run as `agent`: bash login shell, **no sudo**, workdir `~/projects` |
| Net | Outbound internet open. Drop RFC1918, link-local, CGNAT, host gw `192.168.5.2`. Allow DNS `192.168.5.3:53`. Inbound SSH forwarding must keep working. Empty allowlist section for later |
| Creds | VM-only and manual (docs checklist): VM-generated SSH key, fine-grained GH token via `gh auth login`. No `ssh.forwardAgent`, no env passthrough. No secrets in the repo |
| Nix | Ubuntu + Nix via Determinate installer (flakes on). `nix/flake.nix` → one `buildEnv`. `nix/packages.nix` = plain list. `flake.lock` pins. Installed into **`agent`'s** profile |
| Unfree | `allowUnfreePredicate` allows only `claude-code` |
| Packages | `claude-code pi-coding-agent git gh ripgrep fd jq curl neovim nodejs python3 zoxide` |
| Non-nix | `extra-packages.sh`, idempotent, runs as `agent`. Currently: codegraph via `curl -fsSL https://raw.githubusercontent.com/colbymchenry/codegraph/main/install.sh \| sh`. Each entry has a comment: "move to packages.nix once in nixpkgs" |
| Ad hoc | `agent` may run `nix profile add` / `nix shell`. `codevm sync` resets the profile to declared state |
| Config push | Host pushes: `limactl copy` the repo parts into the VM, then apply via `limactl shell`. Agent must NOT be able to edit the applied config |
| Shell | Repo `home/bashrc.d/codevm.sh` holds zoxide init, then the Warp DCS line **last**. Sync installs it. `~/.bashrc` ends with exactly one managed source line. Content above it stays user-owned |
| Git id | `config.env` in repo (`GIT_USER_NAME`, `GIT_USER_EMAIL`). Sync sets `git config --global` for `agent`. Values: `Gerome Meyer` / `gerome.meyer@pm.me` |
| CLI | `bin/codevm` (bash). `codevm` = create-if-missing (+ first sync) → start-if-stopped → shell as `agent` in `~/projects`. `codevm sync`, `codevm destroy`, `codevm rebuild` |
| Safety | `destroy`/`rebuild`: list repos in `~/projects` with uncommitted changes or unpushed commits, then require typing `codevm` exactly |
| Docs | `README.md` = short purpose + links. Details live in `documentation/*.md`. PATH/alias line is documented only; do **not** edit `~/.zshrc` |

## Target layout

```
README.md
HANDOVER.md                 # this file; delete or keep per user
config.env                  # GIT_USER_NAME / GIT_USER_EMAIL
bin/codevm
lima/codevm.yaml
firewall/codevm.nft
nix/flake.nix
nix/packages.nix
nix/flake.lock              # generated in VM, copied back to host
extra-packages.sh
home/bashrc.d/codevm.sh
documentation/{installation,usage,packages,security,credentials}.md
```

In-VM paths: applied config lives in `/opt/codevm/` (root-owned, 0755, agent read-only). Staging dir is `/tmp/codevm-sync/`.

## Technical spec

### `lima/codevm.yaml`
- `vmType: vz`, `arch: aarch64`, `cpus: 6`, `memory: 12GiB`, `disk: 100GiB`, `mounts: []`, `ssh.forwardAgent: false`, `containerd: {system: false, user: false}`.
- Image: Ubuntu 26.04.1 arm64 cloud image. First check `limactl create --list-templates` for an `ubuntu-26.04` template and, if one exists, copy its `images:` block. Otherwise use `https://cloud-images.ubuntu.com/releases/26.04/release/ubuntu-26.04-server-cloudimg-arm64.img` and pin the `digest` from that dir's `SHA256SUMS`. **Never invent a digest.**
- `provision:` `mode: system` script. It runs on **every boot**, so it must be idempotent:
  1. `apt-get install -y nftables git curl` if missing.
  2. `id agent || useradd -m -s /bin/bash agent`. Don't add it to `sudo`/`admin`. `install -d -o agent -g agent /home/agent/projects`.
  3. Install Nix if `/nix` is missing: `curl -fsSL https://install.determinate.systems/nix | sh -s -- install --no-confirm`. Before using it, check which installer flags are current (upstream vs Determinate Nix both work). Multi-user daemon.
  4. Firewall: if `/opt/codevm/firewall/codevm.nft` exists, install it as `/etc/nftables.conf` (or include it), then `systemctl enable --now nftables`.
- Leave port forwarding at Lima defaults (guest ports → host 127.0.0.1). Mention this in `security.md`.

### `firewall/codevm.nft`
```
table inet codevm { chain output { type filter hook output priority 0; policy accept;
  oif lo accept
  ct state established,related accept      # REQUIRED: SSH replies go to the gw 192.168.5.2
  # --- allowlist (extend here) ---
  ip daddr 192.168.5.3 udp dport 53 accept
  ip daddr 192.168.5.3 tcp dport 53 accept
  meta l4proto ipv6-icmp accept            # NDP
  ip daddr { 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16, 169.254.0.0/16, 100.64.0.0/10 } drop
  ip6 daddr { fc00::/7, fe80::/10 } drop
}}
```
- Start with `flush table inet codevm` (or delete + recreate the table) so re-applying is idempotent.
- **Verify the actual gw and DNS IPs under vz** (`ip route`, `resolvectl status`). If they differ from `.2`/`.3`, adapt the rules and tell the user.

### `nix/flake.nix`
- Input: `nixpkgs` = `github:NixOS/nixpkgs/nixos-unstable` (claude-code moves fast). System `aarch64-linux`.
- `pkgs = import nixpkgs { inherit system; config.allowUnfreePredicate = p: builtins.elem (lib.getName p) [ "claude-code" ]; };`
- `packages.aarch64-linux.default = pkgs.buildEnv { name = "codevm-env"; paths = import ./packages.nix pkgs; };`
- `packages.nix`: `pkgs: with pkgs; [ claude-code pi-coding-agent git gh ripgrep fd jq curl neovim nodejs python3 zoxide ]`

### `home/bashrc.d/codevm.sh`
- Prepend `~/.local/bin` to PATH (codegraph).
- `eval "$(zoxide init bash)"`
- Last line: `printf '\eP$f{"hook": "SourcedRcFileForWarp", "value": { "shell": "bash"}}\x9c'`. Guard it with `[[ $- == *i* ]]`.
- Managed line in `~/.bashrc`: `[ -f ~/.bashrc.d/codevm.sh ] && . ~/.bashrc.d/codevm.sh # codevm-managed`. Sync deletes every line containing `# codevm-managed` and appends one fresh line, so it's always last and never duplicated.

### `codevm sync` (host side), in order
1. Ensure the VM is running.
2. `limactl copy -r` nix/, firewall/, home/, extra-packages.sh, config.env → `codevm:/tmp/codevm-sync/`.
3. As the Lima user with sudo: `rsync`/`cp` into `/opt/codevm/`, `chown -R root:root`, dirs 0755 / files 0644, `extra-packages.sh` 0755.
4. Firewall: `nft -f /opt/codevm/firewall/codevm.nft`, install it as the persistent config, `systemctl enable nftables`.
5. As `agent` (`sudo -iu agent`):
   - Reset the profile: remove all entries (`nix profile remove --all` or the regex form, whichever the installed Nix supports), then `nix profile add /opt/codevm/nix#default`.
   - `nix flake lock` needs a writable dir, so on the first run create `flake.lock` in a writable copy and then `limactl copy` it **back** to the host `nix/flake.lock`. Sync must never silently bump an existing lock.
6. As `agent`: run `/opt/codevm/extra-packages.sh`. Each entry skips when `command -v` finds the tool.
7. As `agent`: install `~/.bashrc.d/codevm.sh`, fix up the managed line, `git config --global user.name/user.email` from `config.env`.

### `bin/codevm`
- `set -euo pipefail`. Repo dir = resolved script dir `/..` (symlink-safe). `VM=codevm`.
- Status: `limactl list --format '{{.Status}}' "$VM" 2>/dev/null`. Empty → create: `limactl start --name="$VM" --tty=false "$REPO/lima/codevm.yaml"`, then `sync`. `Stopped` → `limactl start "$VM"`.
- Enter: `exec limactl shell --workdir / "$VM" sudo -iu agent bash -lc 'cd ~/projects && exec bash -l'`. `--workdir /` is needed because the host cwd doesn't exist in the guest. Ubuntu's `.profile` sources `.bashrc`, so the Warp hook fires.
- `destroy`: if running, list dirty repos as `agent`. For each `~/projects/*/.git`: `git status --porcelain` non-empty, or `git log --branches --not --remotes --oneline` non-empty. Then `read` a confirmation that must equal `codevm`, then `limactl delete -f "$VM"`.
- `rebuild` = `destroy` + create path.
- Unknown subcommand → usage, exit 2.

## Milestones (each one has a verification gate: all checks must pass before moving on)

### M0 — retire `agents`
- `limactl shell agents` → find git repos under the Lima user's home and `/home/*`, and report dirty or unpushed ones. Lima `agents` may mount host `~`, so **ignore anything under `/Users`**.
- **Ask the user before** `limactl delete agents`, because it's irreversible.
- ✅ `limactl list` doesn't show `agents` (only after user approval).

### M1 — VM boots per spec
- Write `lima/codevm.yaml` (provision steps 1–3 only, no firewall yet). `limactl validate lima/codevm.yaml`. `limactl start --name=codevm --tty=false lima/codevm.yaml`.
- ✅ `/etc/os-release` shows 26.04.1. `nproc`=6. `free -g` ≈12. `df -h /` ≈100G.
- ✅ No host mounts: `mount | grep -Ei 'virtiofs|9p|sshfs|/Users'` is empty, and `ls /Users` fails.
- ✅ Reboot (`limactl stop codevm && limactl start codevm`), then the provision re-run has no errors (`/var/log/cloud-init-output.log`, `limactl` output).

### M2 — `agent` user
- ✅ `id agent` isn't in `sudo`/`admin`. `sudo -iu agent sudo -n true` fails. `~agent/projects` is owned by agent.
- ✅ `sudo -iu agent nix --version` works, and `nix flake --help` works (flakes enabled).

### M3 — firewall
- Add `firewall/`, the provision step 4, and the firewall part of sync.
- ✅ As `agent`: `curl -sSfI https://github.com` OK, `getent hosts github.com` OK.
- ✅ Host `python3 -m http.server 8765 --bind 0.0.0.0` → guest `curl -m5 http://192.168.5.2:8765` **fails**, `curl -m5 http://<host LAN IP>:8765` **fails**, `curl -m5 http://<LAN router IP>` **fails**. Kill the server afterwards.
- ✅ `limactl shell codevm true` still works (SSH replies pass).
- ✅ After a VM restart, `sudo nft list table inet codevm` is present. As `agent`, `nft list ruleset` is denied.

### M4 — Nix env
- Write the flake, packages.nix and sync steps 1–5.
- ✅ As `agent`, `command -v claude pi git gh rg fd jq curl nvim node python3 zoxide` all resolve under `/nix/store` or `~/.nix-profile`. `claude --version` and `pi --version` run.
- ✅ Unfree scope: adding an unrelated unfree pkg to a scratch copy fails evaluation.
- ✅ Drift reset: as `agent` `nix profile add nixpkgs#hello`, then `codevm sync`, then `hello` is gone.
- ✅ Host `nix/flake.lock` exists. A second sync leaves it byte-identical (`git diff --exit-code nix/flake.lock` after committing, or compare `shasum`).
- ✅ As `agent`, `touch /opt/codevm/nix/x` fails.

### M5 — extras
- ✅ As `agent`, `codegraph --version` (or the tool's equivalent) runs. A second sync skips it (no download in the output).

### M6 — shell
- ✅ `tail -1 ~agent/.bashrc` is the managed line. After 2 syncs, `grep -c codevm-managed` = 1.
- ✅ `sudo -iu agent bash -ic 'type z'` works. `sudo -iu agent bash -ic true | od -c | grep 'P  \$  f'` shows the DCS sequence. The last line of `codevm.sh` is the printf.
- ✅ `sudo -iu agent git config --global user.email` = `gerome.meyer@pm.me`.
- The user checks Warp auto-warpify manually. Ask them.

### M7 — CLI
- ✅ `limactl stop codevm; echo 'pwd; whoami; exit' | bin/codevm` prints `/home/agent/projects` and `agent`, and the VM ends up Running.
- ✅ Dirty-repo guard: as `agent`, `git init ~/projects/t && touch ~/projects/t/f`. Then `echo wrong | bin/codevm destroy` aborts, lists `t`, and the VM still exists.
- ✅ `bin/codevm bogus` → exit 2 with usage. `shellcheck bin/codevm extra-packages.sh` is clean (install it on the host via brew only if the user agrees; otherwise skip and say so).

### M8 — docs
- Load the `write-documentation` skill first. `README.md` links each `documentation/*.md`:
  - `installation`: prereqs, the PATH/alias line for `~/.zshrc`, first `codevm`
  - `usage`: subcommands
  - `packages`: edit packages.nix → sync, extras, bumping the lock
  - `security`: threat model, no mounts, the `agent`/admin split, firewall + how to extend the allowlist, port-forward note
  - `credentials`: checklist for ssh-keygen in the VM, GitHub key, fine-grained token + `gh auth login`
- ✅ Every relative link resolves (`grep -o '([^)]*\.md)'`, then check each exists). Commands in the docs match the actual CLI.

### M9 — clean-room E2E
- ✅ `echo codevm | bin/codevm destroy`, then `bin/codevm` from scratch → all M1–M6 checks pass again with no manual steps.
- Report the results to the user. Don't commit unless asked.

## Open points: resolve, then report your choices
1. Ubuntu 26.04 image source (template vs pinned URL + digest).
2. Actual vz gateway/DNS IPs if they're not `.2`/`.3`.
3. Determinate installer flavor and flags. The `nix profile remove` all-entries syntax for that Nix version.
4. Lock bumping: sync never bumps. Propose `codevm update` (`nix flake update` in VM + copy the lock back) to the user rather than adding it silently.
5. codegraph's install location and binary name. Make sure it's on `agent`'s PATH.

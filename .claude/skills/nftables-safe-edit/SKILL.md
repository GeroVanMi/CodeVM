---
name: nftables-safe-edit
description: How to safely edit, test, and apply nftables firewall rules for the codevm VM. Use this whenever changing firewall/codevm.nft, adding or adjusting an outbound allowlist entry, debugging why a network connection is unexpectedly blocked or unexpectedly allowed, or making the ruleset persist across a reboot — even if the user just says something like "let the VM reach this host" or "why can't the agent hit this API", not only when they mention nftables by name.
---

# Editing the codevm firewall safely

`firewall/codevm.nft` is a default-allow-outbound ruleset that blocks RFC1918/link-local/CGNAT ranges and the host gateway subnet, with an explicit allowlist for DNS and anything else that needs poking through. Two things matter most when touching it: the ruleset must stay idempotent to reapply, and a bad rule should never leave you unable to reach the VM to fix it.

## Before applying: syntax-check

`nft -c -f firewall/codevm.nft` validates the syntax without touching the live ruleset. Always run this before `nft -f` for real, whether testing locally or from within `codevm sync`.

## Idempotent reapply

The ruleset starts with `flush table inet codevm` (or an equivalent delete-and-recreate) precisely so that reapplying it — after an edit, on every `sync`, or on every VM boot via the `lima/codevm.yaml` provision script — doesn't stack duplicate rules. Any new rule file should keep this pattern: define the table skeleton, flush it, then add rules, rather than appending to whatever might already be loaded.

## Making a rule change stick

Applying a ruleset with `nft -f` only affects the running kernel state; it does not survive a reboot on its own. To persist it:

```
sudo install -m 0644 -o root -g root firewall/codevm.nft /etc/nftables.conf
sudo systemctl enable nftables
sudo systemctl restart nftables   # not `enable --now` — nftables is a oneshot unit that's
                                   # typically already active, and --now won't re-apply a
                                   # changed ruleset to an already-active service
```

## Testing a block or allow change

Don't trust a rule until you've watched it actually block or allow traffic. The pattern used throughout this repo's own verification:

1. On the host: `python3 -m http.server 8765 --bind 0.0.0.0` (background it, and remember to kill it afterward — it's a real listener on your LAN).
2. From inside the guest, as `agent`: `curl -m5 http://<host-ip>:8765` should time out if the rule is meant to block host/LAN reachability, or succeed if it's meant to allow it.
3. For an allowlist addition (e.g. a new external host or port), confirm the *opposite*: that the specific allowed destination now works while everything else you didn't intend to open is still blocked.
4. Confirm `limactl shell codevm true` (or any SSH-based access) still works after the change — `ct state established,related accept` needs to stay intact or you lose remote access to the VM entirely.

## Finding the real gateway/DNS IPs

Don't assume Lima's usual `192.168.5.2`/`192.168.5.3` split. Under vz on this host, gateway and DNS turned out to be the *same* IP (`192.168.5.2`). Verify with `ip route` and `resolvectl status` (or `/etc/resolv.conf`) inside the guest before writing IP-specific rules, and note in a comment if they diverge from the usual assumption.

After applying, run `bin/codevm-test`.

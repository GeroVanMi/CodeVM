# Security

## Threat model

CodeVM isolates coding agents, such as claude-code and pi-coding-agent, from the
host machine. Agents run inside a Lima virtual machine, so a compromised or
misbehaving agent cannot read or modify files on the host, and its network
access is restricted by an egress firewall.

## No host mounts

The VM has zero host mounts, configured as `mounts: []` in
[`lima/codevm.yaml`](../lima/codevm.yaml). Code enters or leaves the VM only
through git clone, pull, and push. An agent running inside the VM cannot read or
write any file on the host filesystem.

## User privilege split

The VM has two users. The Lima admin user has sudo access and is used only to
apply configuration during sync. Coding agents run as the `agent` user, which
has no sudo access and works out of `~/projects`. Configuration applied by sync
lives in `/opt/codevm/`, owned by root with read-only access for `agent`, so an
agent cannot modify the firewall rules, Nix packages, or other applied
configuration from inside its own session.

## Firewall

The egress firewall, defined in [`firewall/codevm.nft`](../firewall/codevm.nft),
applies to outbound traffic from the VM. It allows outbound traffic by default,
but drops destinations in the private IPv4 ranges (RFC1918), link-local
addresses, and the Carrier Grade NAT range, as well as their IPv6 equivalents.
This blocks an agent from reaching the host's LAN or other private network
devices, since the host gateway itself falls in one of these blocked ranges. DNS
lookups still work because the firewall explicitly allows traffic to the gateway
address, 192.168.5.2, which also serves DNS in this Lima vz setup.

To allow additional destinations, add rules to the allowlist section marked in
`firewall/codevm.nft`, above the block rules, then run `codevm sync` to apply
the change.

## Port forwarding

Lima's default port forwarding applies: ports opened by services inside the VM
are forwarded to `127.0.0.1` on the host only. Nothing on the host's LAN, or any
other machine, can reach a VM service through a forwarded port.

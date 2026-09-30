# CodeVM

CodeVM isolates coding agents inside a Lima virtual machine, keeping them off
the host filesystem and behind an egress firewall.

## Documentation

- [Installation](documentation/installation.md): prerequisites and the first
  `codevm` run.
- [Usage](documentation/usage.md): the `codevm` subcommands.
- [Packages](documentation/packages.md): editing the Nix package list and
  applying changes.
- [Security](documentation/security.md): the isolation model and the firewall.
- [Testing](documentation/testing.md): running the Command Checks against the
  Test VM.
- [Credentials](documentation/credentials.md): setting up SSH and GitHub access
  inside the VM.

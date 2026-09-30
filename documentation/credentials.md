# Credentials

CodeVM stores no secrets in this repository and passes no credentials from the
host into the VM. There is no SSH agent forwarding and no environment variable
passthrough. Set up credentials manually, once, inside the VM.

## Checklist

- [ ] Generate an SSH key inside the VM with `ssh-keygen`.
- [ ] Add the resulting public key to your GitHub account.
- [ ] Create a fine-grained personal access token on GitHub, scoped to the
      repositories the agent needs.
- [ ] Run `gh auth login` inside the VM and authenticate with that token.

Run these steps from a `codevm` shell (see
[installation](installation.md#first-run)). Because the VM has no host mounts,
an SSH key or token generated on the host cannot be copied in; it must be
created inside the VM itself.

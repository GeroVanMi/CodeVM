# Shared helpers for Command Checks. Loaded with `load ../helpers`.

VM="${CODEVM_NAME:-codevm-test}"

# in_vm '<cmd>': run <cmd> as agent in a login shell on the Test VM.
# Wrap slow commands in `timeout N` inside <cmd> so every check is bounded.
in_vm() {
  limactl shell --workdir / "$VM" sudo -u agent -H bash -lc "$1"
}

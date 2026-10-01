#!/usr/bin/env bash
# Host-side: copy every sources/corpus/<ID>/clean.md into the CodeVM checkout.
# The VM has no host mounts and corpus/ is gitignored, so git does not carry it.
# Usage: scripts/push_corpus_to_vm.sh [VM_REPO_PATH]   (default ~/projects/CodeVM, as user agent)
set -euo pipefail
VM="${CODEVM_NAME:-codevm}"
DEST="${1:-projects/CodeVM}"   # relative to /home/agent
HERE="$(cd "$(dirname "$0")/.." && pwd)"
TAR="$(mktemp -t corpus).tgz"
(cd "$HERE/sources" && tar -czf "$TAR" corpus/*/clean.md)
limactl copy "$TAR" "$VM:/tmp/corpus-clean.tgz"
limactl shell --workdir / "$VM" sudo -u agent -H bash -lc \
  "mkdir -p ~/$DEST/isolation_research/sources && tar -xzf /tmp/corpus-clean.tgz -C ~/$DEST/isolation_research/sources && ls ~/$DEST/isolation_research/sources/corpus | wc -l"
limactl shell --workdir / "$VM" rm -f /tmp/corpus-clean.tgz
rm -f "$TAR"

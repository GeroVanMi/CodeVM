# Agent instructions

- Tests run on the host only, never inside the VM.
- Run `bin/codevm-test` after every change.
- Run `bin/codevm-test full` before committing changes to `lima/codevm.yaml` or `bin/codevm`.
- When fixing a missing or broken command, add a failing check in `tests/commands/` first.
- Run `bin/codevm-test stop` when finished.

See [documentation/testing.md](documentation/testing.md).

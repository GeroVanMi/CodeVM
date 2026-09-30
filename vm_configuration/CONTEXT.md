# CodeVM

## Language

**Test VM**:
A disposable VM built from the working tree, used only for testing, never the one agents work in.
_Avoid_: staging VM, scratch VM

**Command Check**:
A command that must succeed when run as the agent user inside a freshly synced **Test VM**.
_Avoid_: smoke test, package test

**Fast tier**:
Re-syncing the existing **Test VM** from the working tree, then running every **Command Check**.

**Full tier**:
Recreating the **Test VM** from scratch, then running every **Command Check**.

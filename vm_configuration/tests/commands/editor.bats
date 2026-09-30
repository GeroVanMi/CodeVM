#!/usr/bin/env bats

load ../helpers

@test "neovim" {
  run in_vm 'timeout 20 nvim --headless +qa'
  [ "$status" -eq 0 ]
}

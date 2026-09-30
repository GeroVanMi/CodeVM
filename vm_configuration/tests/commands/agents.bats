#!/usr/bin/env bats

load ../helpers

@test "claude-code" {
  run in_vm 'timeout 30 claude --version'
  [ "$status" -eq 0 ]
}

@test "pi-coding-agent" {
  run in_vm 'timeout 30 pi --version'
  [ "$status" -eq 0 ]
}

#!/usr/bin/env bats

load ../helpers

@test "codegraph" {
  run in_vm 'timeout 30 codegraph --version'
  [ "$status" -eq 0 ]
}

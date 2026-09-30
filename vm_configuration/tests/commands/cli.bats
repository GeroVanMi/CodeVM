#!/usr/bin/env bats

load ../helpers

@test "ripgrep" {
  run in_vm 'timeout 10 rg --version'
  [ "$status" -eq 0 ]
}

@test "fd" {
  run in_vm 'timeout 10 fd --version'
  [ "$status" -eq 0 ]
}

@test "jq" {
  run in_vm 'echo "{\"a\":1}" | timeout 10 jq -e .a'
  [ "$status" -eq 0 ]
}

@test "curl" {
  run in_vm 'timeout 10 curl --version'
  [ "$status" -eq 0 ]
}

@test "zoxide" {
  run in_vm 'timeout 10 zoxide --version'
  [ "$status" -eq 0 ]
}

@test "unzip" {
  run in_vm 'timeout 10 unzip -v'
  [ "$status" -eq 0 ]
}

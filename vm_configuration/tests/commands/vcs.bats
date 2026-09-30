#!/usr/bin/env bats

load ../helpers

@test "git" {
  run in_vm 'timeout 10 git --version'
  [ "$status" -eq 0 ]
}

@test "gh" {
  run in_vm 'timeout 10 gh --version'
  [ "$status" -eq 0 ]
}

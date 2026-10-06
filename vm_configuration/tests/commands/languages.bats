#!/usr/bin/env bats

load ../helpers

@test "nodejs" {
  run in_vm 'timeout 10 node -e "process.exit(0)"'
  [ "$status" -eq 0 ]
}

@test "python3" {
  run in_vm 'timeout 10 python3 -c pass'
  [ "$status" -eq 0 ]
}

@test "python3 distutils (node-gyp < 10)" {
  run in_vm 'timeout 10 python3 -c "import distutils"'
  [ "$status" -eq 0 ]
}

@test "pnpm" {
  run in_vm 'timeout 10 pnpm --version'
  [ "$status" -eq 0 ]
}

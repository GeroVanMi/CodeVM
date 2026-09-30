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

@test "gcc" {
  run in_vm 'cd "$(mktemp -d)" && echo "int main(void){return 0;}" > t.c && timeout 60 gcc t.c -o t && ./t'
  [ "$status" -eq 0 ]
}

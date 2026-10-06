#!/usr/bin/env bats
# Packages installed with apt by the provision script in lima/codevm.yaml
# (podman, the C toolchain and C libraries), plus podman compose.

load ../helpers

@test "podman rootless user namespace" {
  run in_vm 'timeout 30 podman unshare true'
  [ "$status" -eq 0 ]
}

@test "podman systemd cgroup manager" {
  run in_vm 'timeout 30 podman info --format "{{.Host.CgroupManager}}"'
  [ "$status" -eq 0 ]
  [ "$output" = systemd ]
}

@test "podman compose uses docker-compose" {
  run in_vm 'timeout 30 podman compose version'
  [ "$status" -eq 0 ]
  [[ "$output" == *"Docker Compose"* ]]
}

@test "podman compose runs a service" {
  run in_vm 'cd "$(mktemp -d)" && printf "services:\n  t:\n    image: docker.io/library/alpine\n    command: \"true\"\n" > compose.yaml && timeout 120 podman compose run --rm t; s=$?; podman compose down >/dev/null 2>&1; exit $s'
  [ "$status" -eq 0 ]
}

@test "gcc" {
  run in_vm 'cd "$(mktemp -d)" && echo "int main(void){return 0;}" > t.c && timeout 60 gcc t.c -o t && ./t'
  [ "$status" -eq 0 ]
}

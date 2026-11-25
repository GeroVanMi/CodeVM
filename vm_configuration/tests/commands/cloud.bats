load ../helpers

@test "exoscale-cli" {
  run in_vm 'timeout 30 exo version'
  [ "$status" -eq 0 ]
}

@test "opentofu" {
  run in_vm 'timeout 30 tofu version'
  [ "$status" -eq 0 ]
}

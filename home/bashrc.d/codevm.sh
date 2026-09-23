export PATH="$HOME/.local/bin:$PATH"

eval "$(zoxide init bash)"

[[ $- == *i* ]] && printf '\eP$f{"hook": "SourcedRcFileForWarp", "value": { "shell": "bash"}}\x9c'

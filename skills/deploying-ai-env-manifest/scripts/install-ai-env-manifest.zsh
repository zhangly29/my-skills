#!/usr/bin/env zsh
set -eo pipefail

export PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:${PATH:-}"

ai_dir="${AI_ENV_DIR:-$HOME/.ai}"
bin_dir="${AI_ENV_BIN_DIR:-$HOME/.local/bin}"
manifest="$ai_dir/env.json"
refresh="$ai_dir/refresh-env.zsh"
check="$bin_dir/ai-env-check"
shell_path="$(command -v zsh 2>/dev/null || printf '/bin/sh')"

mkdir -p "$ai_dir" "$bin_dir"

cat > "$refresh" <<'SCRIPT'
#!/usr/bin/env zsh
set -eo pipefail

export PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:${PATH:-}"
[[ -r "$HOME/.zshrc" ]] && source "$HOME/.zshrc"

json_escape() {
  /usr/bin/python3 -c 'import json,sys; print(json.dumps(sys.stdin.read().rstrip("\n")))'
}

cmd_path() {
  command -v "$1" 2>/dev/null || true
}

cmd_version() {
  local cmd="$1"
  local out
  out=$(eval "$cmd" 2>&1 | /usr/bin/sed -n '1p' || true)
  printf '%s' "$out"
}

cmd_json() {
  local name="$1"
  local version_cmd="$2"
  local cmdpath version
  cmdpath=$(cmd_path "$name")
  version=$(cmd_version "$version_cmd")
  if [[ -z "$cmdpath" ]]; then
    printf '"%s":{"path":null,"version":null}' "$name"
  else
    printf '"%s":{"path":%s,"version":%s}' "$name" "$(printf '%s' "$cmdpath" | json_escape)" "$(printf '%s' "$version" | json_escape)"
  fi
}

out="$HOME/.ai/env.json"
tmp="${out}.tmp"

cat > "$tmp" <<EOF
{"schema":"ai-env.v1","shell":$(printf '%s' "$(command -v zsh 2>/dev/null || printf /bin/sh)" | json_escape),"policy":{"on_missing_env":"source ~/.zshrc","then":"install_dependency_if_still_missing"},"commands":{$(cmd_json node 'node -v'),$(cmd_json npm 'npm -v'),$(cmd_json npx 'npx --version'),$(cmd_json corepack 'corepack --version'),$(cmd_json pnpm 'pnpm --version'),$(cmd_json codex 'codex --version'),$(cmd_json java 'java -version'),$(cmd_json javac 'javac -version'),$(cmd_json mvn 'mvn -version'),$(cmd_json gradle 'gradle -version')},"tools":{$(cmd_json python3 'python3 --version'),$(cmd_json uv 'uv --version'),$(cmd_json uvx 'uvx --version'),$(cmd_json git 'git --version'),$(cmd_json rg 'rg --version'),$(cmd_json fd 'fd --version'),$(cmd_json jq 'jq --version'),$(cmd_json curl 'curl --version'),$(cmd_json wget 'wget --version'),$(cmd_json brew 'brew --version'),$(cmd_json claude 'claude --version'),$(cmd_json opencode 'opencode --version'),$(cmd_json kimi 'kimi --version'),$(cmd_json eza 'eza --version'),$(cmd_json bat 'bat --version'),$(cmd_json fzf 'fzf --version'),$(cmd_json zoxide 'zoxide --version')},"paths":{"home":$(printf '%s' "$HOME" | json_escape),"codex_home":$(printf '%s' "${CODEX_HOME:-$HOME/.codex}" | json_escape),"workspace_root":$(printf '%s' "${PWD:-}" | json_escape)}}
EOF

/usr/bin/python3 -m json.tool "$tmp" >/dev/null
command mv -f "$tmp" "$out"
rm -f "$tmp"
printf '%s\n' "$out"
SCRIPT

cat > "$check" <<'SCRIPT'
#!/usr/bin/env zsh
set -eo pipefail

export PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:${PATH:-}"
[[ -r "$HOME/.zshrc" ]] && source "$HOME/.zshrc"

show() {
  local name="$1"
  local version_cmd="$2"
  local cmdpath version
  cmdpath=$(command -v "$name" 2>/dev/null || true)
  if [[ -z "$cmdpath" ]]; then
    printf '%-9s missing\n' "$name"
    return
  fi
  version=$(eval "$version_cmd" 2>&1 | /usr/bin/sed -n '1p' || true)
  printf '%-9s %s %s\n' "$name:" "$cmdpath" "$version"
}

printf 'shell:   %s\n' "$(command -v zsh 2>/dev/null || printf /bin/sh)"
show node 'node -v'
show npm 'npm -v'
show npx 'npx --version'
show corepack 'corepack --version'
show pnpm 'pnpm --version'
show codex 'codex --version'
show java 'java -version'
show javac 'javac -version'
show mvn 'mvn -version'
show gradle 'gradle -version'
printf '\n'
show python3 'python3 --version'
show uv 'uv --version'
show uvx 'uvx --version'
show git 'git --version'
show rg 'rg --version'
show fd 'fd --version'
show jq 'jq --version'
show curl 'curl --version'
show wget 'wget --version'
show brew 'brew --version'
show claude 'claude --version'
show opencode 'opencode --version'
show kimi 'kimi --version'
show eza 'eza --version'
show bat 'bat --version'
show fzf 'fzf --version'
show zoxide 'zoxide --version'
printf 'manifest: %s\n' "$HOME/.ai/env.json"
SCRIPT

chmod +x "$refresh" "$check"
"$refresh" >/dev/null
printf 'installed: %s\n' "$manifest"
printf 'installed: %s\n' "$refresh"
printf 'installed: %s\n' "$check"
printf 'shell: %s\n' "$shell_path"

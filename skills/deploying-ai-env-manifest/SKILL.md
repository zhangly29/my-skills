---
name: deploying-ai-env-manifest
description: Use when setting up, repairing, or porting a compact AI-readable environment manifest, live environment check command, or shell/tool detection workflow for Codex or other AI coding agents.
---

# Deploying AI Env Manifest

## Purpose

Install a compact environment awareness workflow any AI coding agent can use:

- Static manifest: `$HOME/.ai/env.json`
- Refresh script: `$HOME/.ai/refresh-env.zsh`
- Live check command: `$HOME/.local/bin/ai-env-check`
- Agent instruction: read manifest first, run live check when current paths matter

## Use When

- A model needs reliable knowledge of local shells, runtimes, package managers, or CLI tools.
- Environment docs are stale, too verbose, or stored in ambiguous `.env` files.
- Commands differ between human terminals and AI tool calls.
- Porting this workflow to another machine, WSL distro, or coding-agent setup.

## Deployment

1. Prefer zsh when available. Use bash only if zsh is absent.
2. Run the bundled installer:

```bash
zsh /path/to/skill/scripts/install-ai-env-manifest.zsh
```

3. Verify:

```bash
ai-env-check
python3 -m json.tool "$HOME/.ai/env.json" >/dev/null
```

4. Add or update agent instructions:

```text
Read $HOME/.ai/env.json when a task depends on local tools/runtimes.
Run ai-env-check when current paths or versions matter.
If a tool is missing: source ~/.zshrc -> retry -> still missing -> install dependency.
After tool/runtime changes, run $HOME/.ai/refresh-env.zsh.
```

## Manifest Shape

Keep it small and machine-oriented:

```json
{
  "schema": "ai-env.v1",
  "shell": "/usr/bin/zsh",
  "policy": {"on_missing_env": "source ~/.zshrc", "then": "install_dependency_if_still_missing"},
  "commands": {},
  "tools": {},
  "paths": {}
}
```

Use `commands` for core runtimes and critical CLIs: `node`, `pnpm`, `codex`, `java`, `mvn`.
Use `tools` for helper CLIs: `uv`, `rg`, `fd`, `jq`, `git`, `brew`, `claude`, `opencode`, etc.

## Maintenance Rules

- Do not use `$HOME/.env` for this workflow; it is ambiguous with dotenv conventions.
- Do not hand-maintain long prose in the manifest.
- Refresh after installing/removing runtimes or CLI tools.
- If a refresh fails, do not overwrite a good manifest with null values; fix the refresh script and retry.


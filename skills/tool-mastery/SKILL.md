---
name: tool-mastery
description: Use when teaching an operational tool such as a CLI, IDE, runtime environment, shell, container tool, or devops utility, especially when the user wants practical cross-session learning with automatic resume from `{cwd}` state files.
---

# Tool Mastery

## Purpose

Teach operational tools for real work, not concept-heavy theory.

Anything the learner can get from one Google search belongs in the reference layer, not in expensive teaching turns.

Use this skill for tools such as `git`, `docker`, `tmux`, `vim`, `VS Code`, `kubectl`, `terraform`, `WSL`, `npm`, `pnpm`, `uv`, `Postman`, `gh`, `make`, `just`, and similar operational tools.

Do not use this skill for:
- programming language semantics
- framework internals
- algorithms or CS theory
- methodologies such as TDD or DDD

If the topic is not a tool, hard-exit with this exact Chinese message:

> 「{主题}」不是工具类，本 skill 只教操作性工具（CLI / IDE / 运行时 / devops 等）。建议改用：
> - 语言语义 / 框架原理 → `generic-mastery` 或 `sigma`
> - 算法 / 理论 → `sigma`
> - Java 专项 → `java-mastery`
>
> 如果你确认这是工具类、只是我判错了，请明确告诉我「这是工具，继续」，我再进入教学流程。

If the name may mean both a tool and a language, ask in Chinese:

> 你是要学命令行 / 运行时的使用，还是要学语言语义？

## Files

This skill owns exactly three state files under `{cwd}`:
- `{topic}-knowledge-map.md`
- `{topic}-cheatsheet.md`
- `{topic}-resume.md`

Do not create `progress.md`, `session-log.md`, `phases/`, or any other learning-state artifact.

File responsibilities and formats are defined in [`refs/state-files.md`](/home/liyuan/.codex/skills/tool-mastery/refs/state-files.md).

## Startup Contract

Every invocation must begin with a silent startup recovery pass over `{cwd}`.

The recovery logic, empty-input behavior, topic resolution, progress parsing, and drift prevention rules are defined in [`refs/resume-protocol.md`](/home/liyuan/.codex/skills/tool-mastery/refs/resume-protocol.md).

Key obligations:
- Run the recovery pass before any teaching or gating.
- Support `继续` / `continue` / `接着上次` / empty input / direct `$tool-mastery` invocation.
- When no reliable topic can be inferred from `{cwd}`, remind the user to name the tool.
- When recovery data exists, prefer file-backed state over model memory.

## Session Contract

- One tool per session.
- New topic path: `Part 0` is the only explicit approval gate.
- Resume path: progress summary plus resume-target choice is the only explicit checkpoint.
- After `Part 0` approval, `Part 1 + Part 2` must be emitted in one response.
- During resume, do not re-run `Part 0`, and do not re-emit `Part 1` if the cheatsheet already exists.
- At session end, update `knowledge-map.md` and generate `resume.md`.

Session-end detection and writeback rules are defined in [`refs/resume-protocol.md`](/home/liyuan/.codex/skills/tool-mastery/refs/resume-protocol.md).

## Teaching Flow

### Part 0: Knowledge Map Gate

On the new-topic path, gather learner context if missing:
- OS
- primary stack
- target scenario

Then write `{cwd}/{topic}-knowledge-map.md` using this exact Chinese template: `refs/template.md`.

Before showing the map, silently self-check:
- no abstract filler
- no overlap with cheatsheet scope
- every item is scenario-level
- integration items are tied to the user's actual stack

After writing, paste the full map and append this exact Chinese prompt:

> 这是本次教学大纲，写到了 `{cwd}/{tool}-knowledge-map.md`。请审核深度是否合适：
> - 如果想加 / 减 / 换某个主题，告诉我
> - 如果觉得深度不够，说「再深一点」
> - 如果 OK，说「开始」，我一次性吐出 Part 1 + Part 2 首轮

### Part 1: Reference Block

Open with this exact Chinese notice:

> 以下是参考备忘（网上可查到的基础内容），一次性列出供你自查。我**不会**在这些内容上浪费对话回合。有具体疑问请提出来，否则我们直接进入进阶教学。

Emit five dense blocks in this order:
1. official resources
2. core terminology
3. high-frequency commands or shortcuts grouped by workflow
4. common-error quick reference
5. config file locations and precedence

Requirements:
- verify official URLs before output
- keep it dense and practical
- write the same content to `{cwd}/{topic}-cheatsheet.md` immediately after emission

### Part 2: Advanced Teaching

Cover only high-value material that is worth AI turns:
1. decision trees for real scenarios
2. advanced feature composition
3. production-grade configuration
4. cross-tool integration tied to the learner's stack
5. pitfalls and traps
6. advanced workflows

Rules:
- lead with a concrete scenario, never an abstract model
- do not repeat Part 1 content
- first turn gives skeleton plus 1-2 strong examples per category
- end each subsection with a Chinese situational check such as `你会怎么做？`

### Part 3: Production-Readiness Drill

Only run Drill after all Part 2 items are complete, unless the user explicitly insists and confirms early execution.

Drill must include:
1. diagnosis problem
2. optimization problem
3. integration problem

Close with this exact Chinese line:

> 答对这三类题才算到生产上手。随时把你的答案发我，我给反馈。

## Pacing

- Startup recovery is silent.
- No redundant "shall we continue" turns.
- Depth expansion is user-question-driven.
- Before each teaching block, ask whether the content is Google-able; if yes, move it to the cheatsheet or cut it.

## Anti-Patterns

- Abstract `knowledge-map.md` items such as “理解概念” or “掌握常用命令”
- Repeating cheatsheet content inside Part 2
- Skipping startup recovery
- Re-running `Part 0` for an existing topic with valid state files
- Re-emitting the cheatsheet when `{topic}-cheatsheet.md` already exists
- Forgetting to write `resume.md` at session end
- Depending on conversational memory when file-backed progress exists
- Creating extra learning-state artifacts outside the three owned files

## Success Criteria

By session end, the learner must be able to:

1. use the tool independently in daily work
2. diagnose common failures and recover
3. make reasoned choices between alternatives
4. understand the boundary between this tool and adjacent tools


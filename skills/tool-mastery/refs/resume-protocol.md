# Tool Mastery Resume Protocol

## Goal

Recover the correct topic and verified progress from `{cwd}` with minimal user effort and minimal drift.

## Startup Scan

Run this silently at the start of every invocation, before any gate or teaching output.

### Step 1: Discover files

Scan `{cwd}` for:
- `*-knowledge-map.md`
- `*-cheatsheet.md`
- `*-resume.md`

Build a topic inventory by slug.

Also detect whether the current invocation is one of these low-information resume forms:
- `继续`
- `continue`
- `接着上次`
- `继续学`
- `明天继续`
- direct `$tool-mastery` invocation with no topic
- empty input

### Step 2: Resolve topic

Resolve the topic in this order:
1. explicit tool named in the current user message
2. explicit tool alias normalized to a canonical slug
3. exactly one recoverable topic found in `{cwd}`
4. candidate topic inferred from scanning other `*.md` files in `{cwd}` when the user gave low-information input

Alias normalization should cover common forms such as:
- `vscode`, `vs-code`, `code` -> `visual-studio-code`
- `idea` -> `intellij-idea`
- `k8s` -> `kubernetes`
- `gh` -> `github-cli`

### Step 3: Empty-input fallback

If the user provides empty input or only invokes `$tool-mastery`:
- scan all top-level `*.md` files in `{cwd}`
- look for topic candidates from existing `knowledge-map`, `resume`, `cheatsheet`, or clearly named tool-learning documents
- if exactly one reliable topic is found, resume it automatically
- if multiple plausible topics are found, list them in Chinese and ask which one to continue
- if none are reliable, remind the user in Chinese to name the tool topic

Required reminder when no topic can be inferred:

> 我没有在当前目录里识别到可恢复的学习主题。请直接告诉我要继续学哪个工具，例如 `继续学 git`、`教我 docker`。

## Path Selection

After topic resolution:
- if `{cwd}/{topic}-knowledge-map.md` exists, take the resume path
- otherwise take the new-topic path

Cheatsheet handling:
- if `{cwd}/{topic}-cheatsheet.md` exists, do not re-emit `Part 1`
- if missing, generate it when `Part 1` is first emitted, or silently backfill it during resume if needed

## Resume Path

When `{cwd}/{topic}-knowledge-map.md` exists:
- skip Gate 0 and `Part 0`
- do not ask the user to re-describe prior progress
- reconstruct progress from files

### Step 1: Read progress from files

Read in this order:
1. `{cwd}/{topic}-resume.md`
2. `{cwd}/{topic}-knowledge-map.md`
3. `{cwd}/{topic}-cheatsheet.md` if present

Use `resume.md` for:
- last verified stop point
- suggested next step
- last learner-context snapshot
- drill status snapshot

Use `knowledge-map.md` for:
- authoritative checkbox counts by subsection
- detecting stale or contradictory `resume.md`

### Step 2: Reconcile drift

If `resume.md` and `knowledge-map.md` disagree:
- trust the checkbox state in `knowledge-map.md`
- keep only the `resume.md` fields still supported by the map
- refresh `resume.md` at the next session-end writeback

If the user now states a different OS, stack, or target scenario:
- ask one short Chinese question to confirm whether to update the learner context
- if confirmed, update the context block and any stack-bound items, especially `2.4`

### Step 3: Progress summary output

Emit one compact Chinese progress summary that includes:
- map path
- subsection progress counts
- whether cheatsheet exists
- recommended resume point

If `resume.md` exists, include its suggested next step. If not, derive the suggestion from the first `[~]` item, otherwise the first `[ ]` item.

Wait for the user to pick a target before teaching.

### Step 4: Teaching during resume

Teach only the selected item or items.

Rules:
- scenario first
- no Part 1 repetition
- end with a verification anchor
- do not jump to Drill until all `Part 2` items are `[x]`, unless the user explicitly insists

## Session-End Detection

Treat these as session-end signals when they clearly mean “stop teaching and save state”:
- `结束教学`
- `stop`
- `明天继续`
- `下次继续`
- `先到这里`
- `今天先这样`

When one of these appears:
1. stop advancing teaching content
2. update `knowledge-map.md` checkbox state
3. write or refresh `{cwd}/{topic}-resume.md`
4. reply with a compact Chinese wrap-up plus where the next session should resume

## Resume Writeback

At session end, `resume.md` must include:
- topic
- last updated timestamp
- learner-context snapshot
- completed / partial / not-started breakdown
- last session stop point
- suggested next step
- drill status
- relevant file paths

Write only verified progress. Never promote partially discussed material to completed.

## Anti-Drift Rules

- Prefer file-backed state over conversational memory.
- Do not assume “继续” means “continue the last thing I remember”; resolve from `{cwd}`.
- Do not guess a topic when multiple plausible topics exist.
- Do not summarize progress from impressionistic memory if files are missing or contradictory.
- If recovery confidence is low, say so briefly and ask for the topic.

## Pressure Scenarios

The protocol must behave correctly for at least these scenarios:

### Scenario 1: Plain continue

User says only `继续`.

Expected behavior:
- scan `{cwd}`
- resolve the topic from existing files
- summarize verified progress
- propose the next item

### Scenario 2: Empty invocation

User invokes `$tool-mastery` with no content.

Expected behavior:
- scan `*.md` under `{cwd}`
- recover exactly one reliable topic if possible
- otherwise ask the user to name the topic

### Scenario 3: End session

User says `明天继续` or `结束教学`.

Expected behavior:
- stop teaching
- update map checkboxes
- generate `resume.md`
- provide a compact handoff summary


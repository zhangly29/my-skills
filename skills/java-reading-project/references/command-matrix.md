# Command Matrix

## Mission

Define command routing, command safety, progress status transitions, mode behavior, failure priority, active-project preflight, and explicit active-project abandonment handling for Java Reading Project.

This file is the single source of truth for command control flow. `progress-contract.md` owns state shape and write mechanics; this file owns when commands may read, write, stop, or transition state.

## Required References By Command

| Command | Required references | Conditional references |
|---|---|---|
| `jr ask <node-id>` | `adaptive-difficulty.md`, `progress-contract.md`, `node-assessment.md`, `evidence-rules.md`, `command-matrix.md` | `generator.md` only for corpus map/index field meanings |
| `jr start <node-id> --s|--m|--b [--auto] [--follow|--micro-follow]` | `generator.md`, `builder.md`, `progress-contract.md`, `teaching-slices.md`, `node-assessment.md`, `learning-experience.md`, `code-annotation.md`, `adaptive-difficulty.md`, `evidence-rules.md`, `command-matrix.md` | `code-follow.md` only when `build_mode` is `follow` or `micro-follow`; `extends-node.md` only when node is unmapped |
| `jr progress <node-id>` | `progress-contract.md`, `node-assessment.md`, `adaptive-difficulty.md`, `evidence-rules.md`, `command-matrix.md` | none |
| `jr extend-node <node-id>` | `extends-node.md`, `command-matrix.md` | corpus docs and validation tools as required by `extends-node.md` |
| `jr status` | `progress-contract.md`, `command-matrix.md` | active project artifacts when present |
| `jr weak` | `progress-contract.md`, `node-assessment.md`, `adaptive-difficulty.md`, `evidence-rules.md`, `command-matrix.md` | none |
| `jr pause` | `progress-contract.md`, `command-matrix.md` | none |
| `jr resume` | `builder.md`, `progress-contract.md`, `teaching-slices.md`, `learning-experience.md`, `adaptive-difficulty.md`, `command-matrix.md`, `evidence-rules.md` | `code-follow.md` when active project build mode is `follow` or `micro-follow` |

## Read And Write Surfaces

| Command | May read | May write |
|---|---|---|
| `jr ask` | `java-catalog.md`, training map, recommendation index, progress files, adaptive data | `adaptive-training-data.yaml`, `progress-state.yaml`, `progress.md` |
| `jr start` before recommendation approval | catalog, corpus map/index/coverage/ledger, progress files, adaptive data | progress files only after no active incomplete project is found |
| `jr start` after recommendation approval | approved corpus resources, progress files, project root | project artifacts, project source, `progress-state.yaml`, `progress.md` |
| `jr progress` | catalog, training map, progress files, coverage, ledger, project logs when present | none |
| `jr extend-node` before approval | catalog and corpus metadata | none |
| `jr extend-node` after approval | catalog and corpus metadata | authored corpus resources through extension protocol, regenerated corpus indexes through tools |
| `jr status` | progress files, active project artifacts when present | progress files only for explicit legacy migration or summary regeneration |
| `jr weak` | progress files and adaptive summary | progress files only for explicit legacy migration or summary regeneration |
| `jr pause` | progress files | `progress-state.yaml`, `progress.md` |
| `jr resume` before confirmation | progress files and active project artifacts | progress files only for explicit legacy migration or summary regeneration |
| `jr resume` after confirmation | active project artifacts, progress files | active project artifacts and progress files required to continue the current incomplete slice |

Never write generated corpus files by hand. Use corpus tools when generated files must be rebuilt.

## Progress Status Transitions

Allowed statuses:

```text
idle
generating_recommendation
selected
building
assessment_pending
paused
completed
```

Allowed transitions:

```text
idle -> generating_recommendation
generating_recommendation -> selected
selected -> building
building -> assessment_pending
assessment_pending -> completed
completed -> idle
selected|building|assessment_pending -> paused
paused -> selected|building|assessment_pending
selected|building|assessment_pending|paused -> idle only after explicit abandon confirmation
```

Rules:

- `jr start` may begin only from `idle` or after an active-project preflight proves no active incomplete project exists.
- `jr pause` may set `paused` only for `selected`, `building`, or `assessment_pending` with `progress.current_project`.
- `jr resume` may continue `selected`, `building`, `assessment_pending`, or `paused` when `progress.current_project` is set.
- `completed` means the project has finished build/demo and required final progress merge. After final summary, the workspace may return to `idle` as a housekeeping transition, but completed project history, weakpoints, equipment, adaptive summary, and evidence must be preserved.
- Do not clear an active project by starting a new recommendation.

## Teaching And Build Mode Matrix

`teaching_mode` controls confirmation rhythm. `build_mode` controls code visibility.

| Combination | Behavior |
|---|---|
| `guided + normal` | Show Slice Gate, wait for fresh confirmation, apply slice, show Slice Completion, wait before next gate. |
| `guided + follow` | Show Slice Gate, wait for fresh confirmation, show meaningful Code Follow Blocks, wait before applying each block, apply block, show applied summary, show Slice Completion. |
| `guided + micro-follow` | Same as `guided + follow`, but Code Follow Blocks are smaller while preserving responsibility boundaries. |
| `auto + normal` | Do not wait for confirmations, but still output every Slice Gate, implementation summary, Slice Completion, reading focus, and `TEACHING_LOG.md` update. |
| `auto + follow` | Show Code Follow Blocks for visibility, then apply without confirmation unless the user interrupts or asks a question. |
| `auto + micro-follow` | Show smaller Code Follow Blocks for visibility, then apply without confirmation unless the user interrupts or asks a question. |

In `guided` mode, a reply after Slice Completion can open the next Slice Gate, but it does not authorize implementing that next slice. The next Slice Gate still needs fresh confirmation.

Natural confirmations include:

```text
继续
ok
开始
go
没问题
下一个
行
可以
嗯
```

## `jr start` Active-Project Preflight

Before `jr start` writes any file:

1. Resolve `{progress_state}` and `{progress_summary}`.
2. Read `{progress_state}` if it exists.
3. If `{progress_state}` is missing and `{progress_summary}` contains legacy YAML, parse the legacy YAML read-only.
4. If parsed state has `progress.status` in `selected`, `building`, `assessment_pending`, or `paused` and `progress.current_project` is set, stop immediately.
5. Do not update progress files, corpus files, generated indexes, or project files.
6. Reply:

```text
检测到还有未完成的阅读项目：`{current_project}`，当前状态是 `{status}`。
请先使用 `jr resume` 继续；如果确实要放弃当前项目，需要明确告诉我如何处理。
```

Only after this preflight proves no active incomplete project exists may `jr start` initialize progress state, write migrated legacy state, or generate a recommendation.

## Failure Priority

When multiple errors relevant to the current command exist, stop at the highest-priority error that can be determined safely. Do not block progress-only commands such as `jr status`, `jr weak`, `jr pause`, or `jr resume` on catalog, training-map, recommendation-index, or corpus-derived errors unless that command explicitly needs those files for the requested output.

1. `java-catalog.md` missing or unreadable.
2. `progress-state.yaml` exists but is invalid or cannot be safely parsed.
3. legacy `progress.md` state exists but cannot be safely parsed.
4. active incomplete project exists.
5. requested node does not exist in `java-catalog.md`.
6. requested node is missing from `catalog-training-map.yaml`.
7. required corpus index or derived file is missing, stale, or inconsistent.
8. no recommendation candidate is usable.
9. builder compile/demo verification fails.
10. progress write fails.

Recovery rules:

- Do not guess a damaged progress state.
- Do not overwrite damaged progress files unless the user explicitly approves a repair/reset plan.
- Do not hand-edit generated corpus files under `_derived`.
- If writing `progress-state.yaml` fails, do not regenerate `progress.md`.
- If generated corpus files are stale or missing, use validation and index tools rather than manual edits.

## Explicit Active Project Abandonment

There is no separate `jr abandon` command in V2.1. If the user explicitly asks to abandon the active project, use this safety flow:

1. Summarize active project name, node, status, current milestone, current slice, project directory, and paused timestamp when present.
2. Ask for explicit second confirmation.
3. Before confirmation, write nothing.
4. After confirmation, set progress fields to idle values and regenerate `progress.md`.
5. Preserve project directory, source files, `TEACHING_LOG.md`, corpus resources, and generated indexes.

Use this confirmation:

```text
你确认要放弃当前阅读项目 `{current_project}` 吗？
我会只重置 workspace 级 progress 状态，不删除项目目录或学习记录。
```

Idle progress fields after confirmed abandonment:

```yaml
progress:
  current_node: null
  current_project: null
  current_size: null
  current_milestone: null
  current_slice: null
  current_entry_mode: null
  current_investigation_focus: null
  current_adaptive_level: null
  current_adaptive_controls: null
  teaching_mode: "guided"
  build_mode: "normal"
  current_follow_block: null
  status: "idle"
  paused_at: null
  pause_reason: null
```

Do not delete completed project history, weakpoints, equipment, adaptive summary, or next project bias during abandonment unless the user explicitly requests a full reset and approves a separate reset plan.

## Corpus Schema And Generated Files

When corpus schema or generated index maintenance details matter, read the existing corpus resources:

```text
java-reading-corpus/_schemas/
java-reading-corpus/AGENT_GUIDE.md
java-reading-corpus/USER_GUIDE.md
java-reading-corpus/tools/validate-corpus.py
java-reading-corpus/tools/build-index.py
java-reading-corpus/tools/check-coverage.py
```

Generated files must come from tools:

```text
java-reading-corpus/_derived/recommendation-index.yaml
java-reading-corpus/_derived/coverage-matrix.yaml
java-reading-corpus/_derived/validation-ledger.yaml
```

Do not hand-edit generated files.

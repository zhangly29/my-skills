# Runtime Control

## Mission

Define command routing, runtime load paths, read/write surfaces, progress state shape, state writes, legacy migration, status transitions, failure priority, pause/resume, and active-project abandonment for Java Reading Project.

This file is the single source of truth for command control flow and workspace progress state. Domain evidence is owned by `evidence-policy.md`; project generation is owned by `start-project.md`; project construction is owned by `build-project.md`; mastery reporting is owned by `assessment-progress.md`.

**Owned topics**: per-command runtime load paths, read/write surfaces, progress state shape overview (`progress-state.yaml` + `progress.md`), state-write rules, legacy migration, allowed status transitions, active-state preflight, teaching/build/entry mode matrix, **natural confirmation keywords**, pause/resume, abandonment safety flow, failure priority, **"do not copy `TEACHING_LOG.md` into workspace progress files"**, **"do not hand-edit generated `_derived` files"**, validator entry-points.

**Cross-references**: what counts as evidence → `evidence-policy.md`; detailed progress data shapes + `progress_update` field set → `progress-shapes.md`; recommendation shape → `start-project.md`; Slice / Code Follow templates → `build-project.md`; adaptive controls semantics → `adaptive-difficulty.md`; mastery reporting → `assessment-progress.md`.

## Runtime Load Paths

| Command | Required runtime packets | Conditional packets |
|---|---|---|
| `jr ask <node-id>` | `runtime-control.md`, `adaptive-difficulty.md`, `evidence-policy.md` | `progress-shapes.md` when refreshing `adaptive_summary` |
| `jr start <node-id> --s|--m|--b [--auto] [--follow|--micro-follow]` | `runtime-control.md`, `start-project.md`, `evidence-policy.md`, `adaptive-difficulty.md` | `build-project.md` after recommendation approval; `progress-shapes.md` when assembling/merging `progress_update` |
| `jr resume` | `runtime-control.md`, `build-project.md`, `evidence-policy.md`, `adaptive-difficulty.md` | `progress-shapes.md` when assembling/merging `progress_update` |
| `jr progress <node-id>` | `runtime-control.md`, `assessment-progress.md`, `evidence-policy.md`, `adaptive-difficulty.md` | active project logs when present; `progress-shapes.md` to interpret `completed_projects`/`weakpoints` fields |
| `jr weak` | `runtime-control.md`, `assessment-progress.md`, `evidence-policy.md`, `adaptive-difficulty.md` | `progress-shapes.md` to interpret `weakpoints`/`next_project_bias` fields |
| `jr status` | `runtime-control.md` | active project artifacts when present |
| `jr pause` | `runtime-control.md` | none |
| `jr extend-node <node-id>` | `runtime-control.md`, `start-project.md` | corpus docs and validation tools named by `start-project.md` |

Load only the packets needed for the current command phase. For `jr start`, do not load `build-project.md` until the recommendation is approved, and do not load `progress-shapes.md` until you are assembling the final `progress_update`.

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

## Workspace Progress Files

| Variable | Path | Role |
|---|---|---|
| `{progress_state}` | `{workspace}/progress-state.yaml` | Machine-readable source of truth. Read and write this for all workflow decisions. |
| `{progress_summary}` | `{workspace}/progress.md` | Human-readable summary regenerated from `{progress_state}`. Do not parse it as authoritative state except during explicit legacy migration. |

If both files are missing, create `{progress_state}` first:

```yaml
version: 2
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

completed_projects: []
weakpoints: []
node_mastery: {}
equipment_unlocked: []
adaptive_summary: {}
next_project_bias: {}
```

Then create `{progress_summary}` from the state:

```markdown
# Java Reading Project Progress

> Source of truth: `progress-state.yaml`. This file is a human-readable summary.

## Current

- status: `idle`
- current_node: -
- current_project: -
- current_size: -
- current_milestone: -
- current_slice: -
- current_entry_mode: -
- current_investigation_focus: -
- current_adaptive_level: -
- current_adaptive_controls: -
- teaching_mode: `guided`
- build_mode: `normal`
- current_follow_block: -
- paused_at: -
- pause_reason: -

## Completed Projects

None.

## Recent Weakpoints

None.

## Equipment Unlocked

None.

## Adaptive Difficulty

None.

## Next Project Bias

None.
```

If `{progress_state}` exists and `{progress_summary}` is missing or stale, regenerate `{progress_summary}` from `{progress_state}`. Do not reverse-merge data from `{progress_summary}` into `{progress_state}` except during explicit legacy migration.

## State Write Rules

For every workflow state change:

1. Read `{progress_state}`.
2. Apply the smallest required state change.
3. Write `{progress_state}`.
4. Regenerate `{progress_summary}` from the saved state.

Prefer a structured YAML parser when available. Do not patch YAML by matching unrelated prose in `{progress_summary}`.

If the state write fails, do not update `{progress_summary}`. The summary must never be newer than the source-of-truth state.

## Legacy Migration

Older workspaces may store full YAML state inside `{progress_summary}`. When `{progress_state}` is missing and `{progress_summary}` exists:

1. Look for a fenced `yaml` block containing `progress:`.
2. If found, parse that YAML and write it to `{progress_state}` with `version: 2`.
3. Regenerate `{progress_summary}` as a human-readable summary.
4. Continue from `{progress_state}`.

For `jr start`, perform a read-only legacy YAML parse before active-project preflight can pass. If that read-only parse reveals an active incomplete project, stop before writing `{progress_state}` or regenerating `{progress_summary}`.

If legacy YAML cannot be parsed, do not guess. Tell the user that progress state needs manual repair and show the expected `{progress_state}` path.

Never copy full `TEACHING_LOG.md` content into either progress file.

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
idle -> selected
generating_recommendation -> selected
generating_recommendation -> idle
selected -> building
building -> assessment_pending
assessment_pending -> completed
completed -> idle
selected|building|assessment_pending -> paused
paused -> selected|building|assessment_pending
selected|building|assessment_pending|paused -> idle only after explicit abandon confirmation
```

Rules:

- `generating_recommendation` is a transient label only. Because `jr start` writes nothing to `{progress_state}` before the user approves the recommendation, the **persisted** happy path is `idle -> selected`. Do not write `generating_recommendation` to disk just to satisfy the table; both `idle -> selected` (persisted) and `idle -> generating_recommendation` (if a future flow ever stages it) are allowed.
- `generating_recommendation -> idle` covers a recommendation that is rejected or abandoned before any state write.
- `jr start` may begin only from `idle` or after active-project preflight proves no active incomplete project exists.
- `jr pause` may set `paused` only for `selected`, `building`, or `assessment_pending` with `progress.current_project`.
- `jr resume` may continue `selected`, `building`, `assessment_pending`, or `paused` when `progress.current_project` is set.
- `completed` means the project has finished build/demo and required final progress merge. After final summary, the workspace may return to `idle` as a housekeeping transition, but completed project history, weakpoints, equipment, adaptive summary, and evidence must be preserved.
- Do not clear an active project by starting a new recommendation.

## Active State Rules

An active incomplete project exists when:

```text
progress.status in selected|building|assessment_pending|paused
and progress.current_project is set
```

`jr start` must treat this as a hard stop before any state write or project generation. It may read progress files to detect the condition, but it must not modify progress files, corpus files, generated indexes, or project files. The only normal continuation command for this condition is `jr resume`.

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

## Active Project Fields

When a project is approved, set:

```yaml
progress.current_node: node_id
progress.current_project: approved project_name
progress.current_size: size
progress.current_entry_mode: incident-first|design-document
progress.current_investigation_focus: null
progress.current_adaptive_level: supportive|standard|stretch
progress.current_adaptive_controls:
  explanation_density: more|standard|shorter
  clue_exposure: conclusion-first|balanced|clue-first
  jdk8_bridge: more|standard|brief
  equipment_callback: direct|hinted|challenge
  assessment_followup_depth: scaffolded|standard|deeper
progress.teaching_mode: guided|auto
progress.build_mode: normal|follow|micro-follow
progress.current_follow_block: null
progress.status: selected
progress.paused_at: null
progress.pause_reason: null
```

After showing the incident packet, if the learner identifies a useful first investigation focus, set:

```yaml
progress.current_investigation_focus: "short focus, such as SIGNATURE_INVALID retry or lost cause"
```

This field biases explanation and callbacks only. It must not reorder Teaching Slices.

When builder starts the first Teaching Slice:

```yaml
progress.status: building
progress.current_milestone: active milestone
progress.current_slice: active slice id/title
progress.current_follow_block: null
```

When builder starts a Code Follow Block:

```yaml
progress.current_follow_block: active block id/title
```

Write this before showing or applying the block. Clear `current_follow_block` when the Teaching Slice is complete.

After build/demo succeeds but before post-project assessment is completed, set:

```yaml
progress.status: assessment_pending
```

Keep project context set so `jr resume` can continue into assessment. Do not append the final completed project entry or record a mastery judgment until assessment is completed or explicitly skipped.

At completion, merge `progress_update` into `{progress_state}`, set `progress.status: completed`, append one `completed_projects` entry, merge weakpoints and equipment, update adaptive summary, store `next_project_bias`, and clear active project fields unless the user explicitly wants visible context. Regenerate `{progress_summary}` after the state write succeeds.

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

## Pause And Resume

`jr pause` preserves current node, project, size, milestone, slice, entry mode, investigation focus, adaptive level, adaptive controls, teaching mode, build mode, and current follow block. It sets `progress.status: paused`, `progress.paused_at` to current date/time, and `progress.pause_reason: user_requested`, then refreshes `{progress_summary}`.

`jr pause` may write only `{progress_state}` and regenerated `{progress_summary}`. It must not create a new active project and must not modify project code, project learning artifacts, corpus files, or generated corpus indexes. If no active incomplete project exists, report that there is nothing to pause and do not write files.

`jr resume` is valid for active incomplete states:

```text
selected
building
assessment_pending
paused
```

If `status` is `selected`, resume from the first planned Teaching Slice. If `status` is `building` or `paused`, resume from `current_slice` or the next incomplete slice according to `TEACHING_LOG.md`. If `status` is `assessment_pending`, resume into the post-project assessment and do not regenerate or rewrite completed slices.

`jr resume` first reads the progress bookmark and project artifacts, then presents a resume-point summary and waits for confirmation before editing files. The summary includes current project, milestone, selected resume slice or assessment state, current follow block if any, latest reading checkpoint, user-initiated question if any, and `paused_at` when present.

Resume reads:

- `{progress_state}`
- active project `PLAN.md`
- `TASKS.md`
- `TEACHING_LOG.md`
- `READING_GUIDE.md` if present
- `REVIEW.md` if present

Resume input to builder:

```yaml
resume_input:
  root: "/abs/path/project-name"
  current_milestone: "Milestone 2"
  current_slice: "slice-2-parse-boundary"
  current_entry_mode: "incident-first"
  current_investigation_focus: "why invalid signature was retried"
  current_adaptive_level: "standard"
  current_adaptive_controls:
    explanation_density: "standard"
    clue_exposure: "balanced"
    jdk8_bridge: "standard"
    equipment_callback: "hinted"
    assessment_followup_depth: "standard"
  teaching_mode: "guided|auto"
  build_mode: "normal|follow|micro-follow"
  current_follow_block: "block-2-parse-record|null"
  metadata_sources:
    - "PLAN.md"
    - "TASKS.md"
    - "TEACHING_LOG.md"
    - "READING_GUIDE.md"
    - "REVIEW.md"
```

Builder resumes from the current incomplete Teaching Slice and current follow block when present, or from the next incomplete slice if the current one is already complete. Do not recreate completed slices or overwrite existing teaching-log evidence.

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

There is no separate `jr abandon` command in v2.3. If the user explicitly asks to abandon the active project, use this safety flow:

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

## Progress Data Shapes

The `progress-state.yaml` data shapes (`completed_projects`, `weakpoints`, `equipment_unlocked`, `adaptive_summary`, `next_project_bias`), the anti-repetition fingerprints, and the builder `progress_update` required field set now live in `progress-shapes.md`. Load that packet only when assembling, merging, or validating progress data. `scripts/_schemas.py` is the enforced source of truth, exercised via `uv run python java-reading-project/scripts/validate-progress.py` (`--state`, `--all`, `--progress-update -`, `--policy`, `--check-transition`).

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

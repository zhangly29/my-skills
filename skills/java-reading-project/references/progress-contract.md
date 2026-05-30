# Progress Contract

## Workspace Progress Files

Progress has two files:

| Variable | Path | Role |
|---|---|---|
| `{progress_state}` | `{workspace}/progress-state.yaml` | Machine-readable source of truth. Read and write this for all workflow decisions. |
| `{progress_summary}` | `{workspace}/progress.md` | Human-readable summary regenerated from `{progress_state}`. Do not parse it as authoritative state. |

Command routing, allowed command transitions, active-project preflight, explicit abandonment, and failure priority are owned by `command-matrix.md`. This file owns state shape, initialization, legacy migration mechanics, state writes, and summary regeneration.

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

If `{progress_state}` exists and `{progress_summary}` is missing or stale, regenerate `{progress_summary}` from `{progress_state}`. Do not reverse-merge data from `{progress_summary}` into `{progress_state}` except during the explicit legacy migration below.

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

For `jr start`, `command-matrix.md` requires a read-only legacy YAML parse before active-project preflight can pass. If that read-only parse reveals an active incomplete project, stop before writing `{progress_state}` or regenerating `{progress_summary}`.

If legacy YAML cannot be parsed, do not guess. Tell the user that progress state needs manual repair and show the expected `{progress_state}` path.

Never copy full `TEACHING_LOG.md` content into either progress file.

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

Allowed command transitions are defined in `command-matrix.md`. Do not infer command permission from the status list alone.

## Data Shapes

`completed_projects` entries use this shape:

```yaml
completed_projects:
  - node_id: "1.1"
    project_name: "order-import-preflight"
    size: "s"
    entry_mode: "incident-first|design-document"
    investigation_focus: "first symptom or code/log clue the learner wanted to inspect"
    adaptive_level: "supportive|standard|stretch"
    adaptive_controls:
      explanation_density: "more|standard|shorter"
      clue_exposure: "conclusion-first|balanced|clue-first"
      jdk8_bridge: "more|standard|brief"
      equipment_callback: "direct|hinted|challenge"
      assessment_followup_depth: "scaffolded|standard|deeper"
    build_mode: "follow"
    training_mode: "single"
    boundary_id: "B-lang-parse"
    seed_id: "supplier-product-import"
    cross_id: null
    project_type: "CLI 文件处理器"
    enterprise_slice: "电商订单导入前的本地预检模块"
    entry_fallback_reason: null
    domain: "订单导入"
    io_shape: "CSV-like text file -> preflight report"
    artifact_shape: "runnable Maven CLI jar"
    core_flow: "read file -> parse row -> validate business rules -> render report"
    primary_training: []
    secondary_training: []
    background_only: []
    primary_data_structures: []
    interaction_model: "single-run CLI"
    mastery_signal: "..."
    out_of_scope: []
    concepts_covered: []
    user_questions_summary: []
    weakpoints_found: []
    teaching_slices_summary: []
    equipment_unlocked:
      - name: "Exhaustive Switch 反问"
        source_slice: "slice-1-taxonomy"
        use_sentence: "如果这里改成 switch，新增 status 时编译器会不会提醒我们漏判？"
        transfer_contexts:
          - "HTTP status code client"
          - "message event dispatch"
        code_evidence:
          - "src/main/java/.../PaymentGatewayTaxonomyService.java"
    equipment_used:
      count: 0
      examples: []
    fm_exposed: []
    fm_resolved: []
    transfer_evidence:
      count: 0
      examples: []
    build_passed: true
    demo_passed: true
    teaching_questions:
      answered: 0
      unanswered: 0
    assessment:
      status: "pending|partial|completed|skipped"
      main_flow_reconstruction: "pending|weak|adequate|strong"
      boundary_ownership: "pending|weak|adequate|strong"
      failure_classification: "pending|weak|adequate|strong"
      bad_design_diagnosis: "pending|weak|adequate|strong"
      transfer_check: "pending|weak|adequate|strong"
      evidence_summary: []
    mastery_review: {}
```

Use these fields as project fingerprints for anti-repetition:

- `domain`
- `io_shape`
- `artifact_shape`
- `core_flow`
- `primary_data_structures`
- `interaction_model`

`weakpoints` entries use this shape:

```yaml
weakpoints:
  - node_id: "1.1"
    fm_id: "FM-P-01"
    boundary_id: "B-lang-parse"
    status: "open"
    concept: "异常边界"
    issue: "混淆 parse failure 和 validation failure"
    evidence: "用户在 post-project assessment 中认为字段为空属于 parse exception"
    evidence_refs:
      - project: "order-import-preflight"
        file: "TEACHING_LOG.md"
        slice: "parse"
    source_project: "order-import-preflight"
    last_seen: "2026-05-21"
```

Merge weakpoints by `node_id + fm_id + boundary_id` when `fm_id` is available. Legacy weakpoints without `fm_id` may still merge by `node_id + concept + issue`, but new corpus-backed projects must provide `fm_id`.

`next_project_bias` is keyed by node id:

```yaml
next_project_bias:
  "1.1":
    prefer:
      - "对象状态变化"
    avoid:
      - "再次做文件导入预检"
```

`node_mastery` is an optional cache for `jr progress <node-id>` summaries. It is not more authoritative than completed projects and weakpoints.

```yaml
node_mastery:
  "1.1":
    last_assessed: "2026-05-21"
    estimated_percent: 62
    status: "learning"
    covered_boundaries:
      - "B-lang-parse"
    missing_boundaries:
      - "B-lang-exception"
    unresolved_core_fm:
      - "FM-P-01"
    recommended_next:
      command: "jr start 1.1 --s"
      reason: "需要补 B-lang-exception 和 open FM。"
```

When starting a node, read only the matching node id plus any global weakpoints explicitly marked as cross-node.

`equipment_unlocked` is a lightweight global list of reusable review/debug/design tools:

```yaml
equipment_unlocked:
  - name: "Cause Chain 保留检查"
    node_id: "1.1"
    source_project: "payment-gateway-errors-core"
    source_slice: "slice-2-cause"
    use_sentence: "这里 wrap 异常时有没有把原始 cause 带出去？没有的话 on-call 怎么定位 SDK 还是业务失败？"
    transfer_contexts:
      - "third-party SDK client"
      - "file parser"
      - "message consumer"
    unlocked_at: "2026-05-26"
    last_used_at: null
    use_count: 0
```

Rules:

- Equipment is not a score, badge, or mastery claim.
- Store concise equipment data only; do not store full slice narrative.
- Merge by `name + node_id`; update transfer contexts if a later project sharpens them.
- `equipment_used` and `transfer_evidence` require explicit learner use or explanation. Showing an equipment callback is not evidence.

`adaptive_summary` is a lightweight cache derived from `{adaptive_training_data}` and completed project assessment evidence:

```yaml
adaptive_summary:
  "1.1":
    updated_at: "2026-05-26T21:30:00+08:00"
    source: "ask-data|assessment|weakpoints|mixed"
    sample_count: 12
    confidence: "low|medium|high"
    current_level: "supportive|standard|stretch"
    hardest_boundaries:
      - "B-lang-exception"
    strongest_boundaries:
      - "B-lang-basic-oop"
    hardest_fm:
      - "FM-lost-cause"
    preferred_controls:
      explanation_density: "more|standard|shorter"
      clue_exposure: "conclusion-first|balanced|clue-first"
      jdk8_bridge: "more|standard|brief"
      equipment_callback: "direct|hinted|challenge"
      assessment_followup_depth: "scaffolded|standard|deeper"
```

Rules:

- `adaptive_summary` is not mastery, score, or grade.
- Detailed ask samples live only in `{adaptive_training_data}`.
- Ask data alone may set `supportive` or `standard`; do not set `stretch` without assessment evidence or explicit transfer evidence.
- Open core FM weakpoints can lower `current_level` to `supportive`.

`jr ask <node-id>` must update `adaptive_summary.{node_id}` immediately after successfully writing `{adaptive_training_data}`. `jr start` reads this summary in the same session; do not wait for a project completion before refreshing it.

## Active State Rules

An active incomplete project exists when:

```text
progress.status in selected|building|assessment_pending|paused
and progress.current_project is set
```

`jr start` must treat this as a hard stop before any state write or project generation. It may read `{progress_state}` to detect the condition, but it must not modify `{progress_state}`, `{progress_summary}`, corpus files, generated indexes, or project files. The only normal continuation command for this condition is `jr resume`.

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

Write this to `{progress_state}` and refresh `{progress_summary}`.

After showing the incident packet, if the learner identifies a useful first investigation focus, set:

```yaml
progress.current_investigation_focus: "short focus, such as SIGNATURE_INVALID retry or lost cause"
```

This field biases explanation and callbacks only. It must not reorder V2-MVP Teaching Slices.

When builder starts the first Teaching Slice:

```yaml
progress.status: building
progress.current_milestone: active milestone
progress.current_slice: active slice id/title
progress.current_follow_block: null
```

Write this to `{progress_state}` and refresh `{progress_summary}`.

When builder starts a Code Follow Block:

```yaml
progress.current_follow_block: active block id/title
```

Write this to `{progress_state}` and refresh `{progress_summary}` before showing or applying the block.

When the active Teaching Slice is complete, clear:

```yaml
progress.current_follow_block: null
```

`jr pause` preserves current node, project, size, milestone, slice, entry mode, investigation focus, adaptive level, adaptive controls, teaching mode, build mode, and current follow block in `{progress_state}`, sets `progress.status: paused`, sets `progress.paused_at` to the current date/time, sets `progress.pause_reason: user_requested`, then refreshes `{progress_summary}`.

`jr pause` may write only `{progress_state}` and regenerated `{progress_summary}`. It must not create a new active project and must not modify project code, project learning artifacts, corpus files, or generated corpus indexes. If no active incomplete project exists, report that there is nothing to pause and do not write files.

`jr resume` is valid for active incomplete states:

```text
selected
building
assessment_pending
paused
```

If `status` is `selected`, resume from the first planned Teaching Slice. If `status` is `building` or `paused`, resume from `current_slice` or the next incomplete slice according to `TEACHING_LOG.md`. If `status` is `assessment_pending`, resume into the post-project assessment and do not regenerate or rewrite completed slices.

`jr resume` is the only command that continues an active incomplete project. It must not create a new recommendation or replace the active project.

`jr resume` must first read the progress bookmark and project artifacts, then present a resume-point summary and wait for user confirmation before editing files. The summary must include current project, milestone, selected resume slice or assessment state, current follow block if any, latest reading checkpoint, user-initiated question if any, and `paused_at` when present.

If `progress.current_slice` is already complete in `TEACHING_LOG.md`, resume from the next incomplete Teaching Slice. Do not recreate completed slices, overwrite existing `TEACHING_LOG.md` evidence, duplicate already completed explanations, or rewrite completed project artifacts except for narrowly scoped changes needed by the next incomplete slice.

After build/demo succeeds but before post-project assessment is completed, set:

```yaml
progress.status: assessment_pending
```

Keep `progress.current_project`, `current_node`, `current_size`, and project context set so `jr resume` can continue into assessment. Do not append the final completed project entry or write a precise mastery percentage until assessment is completed or explicitly skipped.

If the user explicitly skips assessment, the project may be marked completed with `assessment.status: skipped`, but `mastery_review` must say evidence is limited and node mastery must not use a precise percentage.

At completion, merge `progress_update` into `{progress_state}`, set `progress.status: completed`, append one `completed_projects` entry, merge `weakpoints_found`, store `next_project_bias` under the current `node_id`, and clear `current_project`, `current_milestone`, `current_slice`, and `current_follow_block` unless the user explicitly wants visible context. Regenerate `{progress_summary}` after the state write succeeds.

At completion, also merge `progress_update.equipment_unlocked` into top-level `equipment_unlocked`, update equipment use counters only from explicit `equipment_used.examples`, update `adaptive_summary` from ask data plus assessment/weakpoint evidence, and clear `current_entry_mode`, `current_investigation_focus`, `current_adaptive_level`, and `current_adaptive_controls` unless preserving visible context was explicitly requested.

## Progress Update Required Fields

Builder final `progress_update` must include:

- `node_id`
- `project_name`
- `size`
- `entry_mode`
- `entry_fallback_reason`
- `investigation_focus`
- `adaptive_level`
- `adaptive_controls`
- `build_mode`
- `training_mode`
- `boundary_id`
- `seed_id`
- `cross_id`
- `project_type`
- `enterprise_slice`
- `domain`
- `io_shape`
- `artifact_shape`
- `core_flow`
- `primary_training`
- `secondary_training`
- `background_only`
- `primary_data_structures`
- `interaction_model`
- `mastery_signal`
- `out_of_scope`
- `concepts_covered`
- `user_questions_summary`
- `weakpoints_found`
- `teaching_slices_summary`
- `equipment_unlocked`
- `equipment_used`
- `fm_exposed`
- `fm_resolved`
- `transfer_evidence`
- `build_passed`
- `demo_passed`
- `teaching_questions`
- `assessment`
- `mastery_review`
- `next_project_bias`

Store `teaching_slices_summary` inside the completed project entry in `{progress_state}`, but do not copy full `TEACHING_LOG.md` content into workspace-level progress files.

Weakpoints must come from user questions, incorrect design judgment, inability to explain, or explicit user reflection. Do not infer weakpoints only because a topic is expected to be difficult.

Equipment use must come from explicit learner transfer or explanation. Do not infer it from reading, confirmation, or AI-authored callbacks.

Adaptive level and controls must describe delivery style only. Do not store them as mastery evidence.

## Resume Contract

For `jr resume`, read:

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

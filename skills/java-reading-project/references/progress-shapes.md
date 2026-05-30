# Progress Shapes

## Mission

Define the machine-checked data shapes for workspace progress: `completed_projects`,
`weakpoints`, `equipment_unlocked`, `adaptive_summary`, `next_project_bias`, and the
builder's final `progress_update`. These are **cold** definitions — load this packet
only when assembling, merging, or validating progress data, not for routing or
read-only reporting.

`scripts/_schemas.py` is the enforced source of truth for every field set and enum
here; this file is the human-readable mirror. Command routing, status transitions,
read/write surfaces, and state-write rules live in `runtime-control.md`.

**Owned topics**: `progress-state.yaml` data shapes (`completed_projects`,
`weakpoints`, `equipment_unlocked`, `adaptive_summary`, `next_project_bias`),
anti-repetition fingerprints, builder `progress_update` required field set, the
"do not copy `TEACHING_LOG.md` into progress files" application rule for
`teaching_slices_summary`.

**Cross-references**: routing / transitions / state-write rules / legacy migration →
`runtime-control.md`; what counts as evidence behind these fields →
`evidence-policy.md`; how `progress_update` is assembled at delivery →
`build-project.md §Progress Update`; adaptive control semantics →
`adaptive-difficulty.md`.

## Validator Entry Points

The shapes below are machine-checked by `python java-reading-project/scripts/validate-progress.py`:

- `--state <progress-state.yaml>` validates the top-level `version`/`progress`/`completed_projects`/`weakpoints`/`node_mastery`/`equipment_unlocked`/`adaptive_summary`/`next_project_bias` shapes.
- `--all <workspace-dir>` auto-discovers `progress-state.yaml` and `adaptive-training-data.yaml`.
- `--check-transition FROM:TO` verifies a single status transition against `runtime-control.md §Progress Status Transitions`.
- `--policy` runs cross-shape checks (assessment subitem consistency, equipment consistency, no duplicate active project, no `stretch` without assessment).
- `--progress-update -` (stdin) validates an assembled `progress_update` before merge.

## `completed_projects` Entry

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
    equipment_unlocked: []
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

## `weakpoints` Entry

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

Weakpoints must come from user questions, incorrect design judgment, inability to explain, or explicit user reflection. Do not infer weakpoints only because a topic is expected to be difficult.

## `equipment_unlocked`

A lightweight global list of reusable review/debug/design tools:

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

Equipment is not a score, badge, or mastery claim. Store concise equipment data only; do not store full slice narrative. Merge by `name + node_id`; update transfer contexts if a later project sharpens them. Equipment *use* must come from explicit learner transfer or explanation — do not infer it from reading, confirmation, or AI-authored callbacks (`evidence-policy.md §Equipment Evidence`).

## `adaptive_summary`

A lightweight cache derived from `{adaptive_training_data}` and completed project assessment evidence:

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

Detailed ask samples live only in `{adaptive_training_data}`. Ask data alone may set `supportive` or `standard`; do not set `stretch` without assessment evidence or explicit transfer evidence. Adaptive level and controls describe delivery style only — do not store them as mastery evidence.

## `next_project_bias`

Keyed by node id:

```yaml
next_project_bias:
  "1.1":
    prefer:
      - "对象状态变化"
    avoid:
      - "再次做文件导入预检"
```

## Builder `progress_update` Required Fields

Validate the assembled object before merge:

```bash
cat /tmp/progress_update.yaml | python java-reading-project/scripts/validate-progress.py --progress-update -
```

The builder's final `progress_update` must carry **every field shown in the `completed_projects` entry shape above** (`node_id` … `mastery_review`), **plus** `next_project_bias`. The validator's `PROGRESS_UPDATE_REQUIRED_FIELDS` in `scripts/_schemas.py` is the enforced, exhaustive list — run `--progress-update -` rather than maintaining a parallel checklist here.

Store `teaching_slices_summary` inside the completed project entry in `{progress_state}`. Detailed per-slice narrative stays in the project's `TEACHING_LOG.md` and is not copied into workspace-level progress files (see `runtime-control.md §Legacy Migration` for the canonical rule).

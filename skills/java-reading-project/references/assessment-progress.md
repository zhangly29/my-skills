# Assessment Progress

## Mission

Assess one catalog node using `catalog-training-map.yaml`, corpus coverage, completed projects, Teaching Slice evidence, post-project assessment evidence, adaptive difficulty, and FM weakpoints.

This runtime packet powers internal `jr start <node-id>` decisions and user-facing `jr progress <node-id>` / `jr weak` reports.

Evidence validity follows `evidence-policy.md`. Runtime state shape and progress writes follow `runtime-control.md`. Adaptive profile interpretation follows `adaptive-difficulty.md`.

**Owned topics**: `jr progress` / `jr weak` / `jr status` report format and rules, node mastery status values (`learning` / `reading_completed_assessment_pending` / `needs_drill` / `ready_for_mix` / `mastered`), conservative mastery estimate dimensions, dimension scoring rubric (boundary coverage, weakpoint health, project practice, user interaction evidence, transfer evidence), how to phrase confidence-limited reports, mastery anti-patterns.

**Cross-references**: what makes any of those evidence sources count → `evidence-policy.md` (this file scores evidence only after the policy admits it); progress data shapes consumed by these reports → `runtime-control.md`; adaptive profile semantics → `adaptive-difficulty.md`.

## Inputs

```yaml
node_assessment_input:
  node_id: "1.1"
  training_map: "java-reading-corpus/_shared/catalog-training-map.yaml"
  progress_state: "progress-state.yaml"
  recommendation_index: "java-reading-corpus/_derived/recommendation-index.yaml"
  coverage_matrix: "java-reading-corpus/_derived/coverage-matrix.yaml"
  validation_ledger: "java-reading-corpus/_derived/validation-ledger.yaml"
  project_logs:
    - "supplier-product-import-core/TEACHING_LOG.md"
    - "supplier-product-import-core/REVIEW.md"
  equipment_unlocked:
    - name: "Cause Chain 保留检查"
      node_id: "1.1"
      use_count: 1
  adaptive_summary:
    "1.1":
      confidence: "medium"
      current_level: "standard"
      hardest_boundaries: ["B-lang-exception"]
```

## Status Values

- `learning`: required evidence is incomplete.
- `reading_completed_assessment_pending`: required project reading/build evidence exists, but post-project assessment evidence is missing or incomplete.
- `needs_drill`: unresolved core FM weakpoints should be remediated before more breadth.
- `ready_for_mix`: required single-boundary coverage is met and no blocking FM remains.
- `mastered`: mastery policy is satisfied with recent project evidence and transfer evidence.

## Conservative Mastery Estimate

The mastery estimate is not an exam score and not an objective ability grade. It is a conservative routing heuristic for choosing the next reading project and explaining evidence gaps.

Mastery is reported **qualitatively only** — a status value plus per-dimension rubric. Never produce a precise percentage, even with assessment evidence and even when asked (`evidence-policy.md §Mastery Is Qualitative`).

If post-project assessment is missing:

- report `assessment: pending`;
- use status `reading_completed_assessment_pending` when project coverage exists;
- do not claim mastery;
- give the qualitative status, never a number or numeric range;
- explain that reading/build completion is not mastery evidence.

Base the qualitative judgment on these evidence dimensions; score each one `weak` / `adequate` / `strong`, and never collapse them into a single number:

| Dimension | Strong signal | Weak signal |
|---|---|---|
| Boundary coverage | Required corpus boundaries appear in completed runnable projects. | Required boundaries are missing or only seen as background topics. |
| Weakpoint health | No open core FM weakpoint blocks the next step. | Open core FM weakpoints remain unresolved or recently repeated. |
| Project practice | Completed projects are runnable, demoable, and mapped to the node. | Project evidence is missing, stale, repetitive, or assessment-pending. |
| User interaction evidence | Assessment answers, explanations, corrections, or revealing questions show understanding. | Evidence is mostly confirmation, passive reading, or AI-authored explanation. |
| Transfer evidence | The learner applies the boundary or equipment outside the original slice context. | Transfer exists only as an AI-provided example. |

Always use qualitative language such as `evidence-limited`, `learning`, `needs_drill`, `ready_for_mix`, or `mastered`. If the user explicitly asks for a percentage, explain that this skill reports mastery as a routing heuristic (status + dimension rubric), not as a score, and give that instead of a number.

## Dimension Details

### Boundary Coverage

Use `mastery_policy.senior_ready_requires.required_boundaries`.

A required boundary counts as covered when a completed project has the same `boundary_id`, `build_passed: true`, and `demo_passed: true`. This is project coverage evidence only — see `evidence-policy.md §Build And Demo Boundary` for what it does not prove.

### Weakpoint Health

Open core FM weakpoints lower confidence and usually bias the next recommendation toward a drill project.

Core FM means the FM appears in `weakpoint_routing` or in a required boundary.

### Project Practice

Project practice shows the learner has gone through a complete runnable case. For why build/demo success is not understanding evidence, see `evidence-policy.md §Build And Demo Boundary`.

### User Interaction Evidence

Use post-project assessment answers across:

- main-flow reconstruction;
- boundary ownership;
- failure classification;
- bad-design diagnosis;
- transfer check.

Also count AI correction followed by improved explanation or explicit transfer evidence when recorded in project artifacts.

Use `evidence-policy.md` to decide whether confirmations, user questions, equipment, ask data, reading completion, build/demo success, or transfer examples count as evidence. This packet only scores evidence after it is valid under that policy.

### Transfer Evidence

Transfer evidence requires explicit learner application or explanation. Reading an AI-provided transfer example does not count.

## `jr progress <node-id>` Report Format

```markdown
# <node-id> <node-title> Progress

总体判断：`evidence-limited|learning|needs_drill|ready_for_mix|mastered`（evidence-based 路由启发式，不是考试分数，不给精确百分比）
状态：`learning|reading_completed_assessment_pending|needs_drill|ready_for_mix|mastered`
assessment：`pending|completed|partial`

## 证据摘要

## Boundary 掌握

## Concept 掌握

## 用户问答证据

## 项目实践证据

## Equipment 迁移证据

## Adaptive 难度画像

## Weakpoints

## 判断

## 推荐下一步
```

Rules:

- Missing logs reduce confidence; say evidence is limited.
- Prefer recommending a single-boundary drill for open core FM weakpoints.
- If mastered, recommend the next nodes from `mastery_policy.if_mastered.recommend_next_nodes`.
- Do not call the estimate a grade, exam result, rank, or ability label.

## `jr weak`

Summarize:

- node-specific weakpoints;
- global recurring weakpoints;
- adaptive hard spots when present;
- unresolved FM IDs;
- evidence refs from `TEACHING_LOG.md` or `REVIEW.md`;
- how weakpoints bias future project generation.

Weakpoints must come from user questions, incorrect design judgment, inability to explain, incorrect assessment answers, AI correction followed by learner confusion, or explicit user reflection. Do not infer weakpoints only because a topic is expected to be difficult.

## `jr status`

When active project state exists, report:

- current node/project/size/status;
- milestone/slice/follow block;
- teaching mode/build mode;
- entry mode and investigation focus;
- adaptive level/profile if present;
- latest reading checkpoint from active project artifacts;
- recent weakpoints;
- recently unlocked equipment;
- recommended next command.

Do not call generator or builder from status.

## Anti-Patterns

- Presenting the conservative estimate as an objective test score.
- Producing any precise mastery percentage or numeric range; mastery is qualitative only (`evidence-policy.md §Mastery Is Qualitative`).
- Inferring mastery from build/demo success.
- Inferring weakpoints from ask data alone.
- Hiding missing evidence behind confident language.
- Recommending breadth when open core FM weakpoints need a drill.

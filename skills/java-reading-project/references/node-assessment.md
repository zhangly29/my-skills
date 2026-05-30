# Node Assessment Reference

## Mission

Assess one catalog node using `catalog-training-map.yaml`, corpus coverage, completed projects, Teaching Slice evidence, and FM weakpoints.

This reference powers internal `jr start <node-id>` decisions and the user-facing `jr progress <node-id>` report.

## Evidence Policy Source

For mastery, transfer, equipment, ask-data, passive-reading, build/demo, and precise-percentage evidence rules, follow `evidence-rules.md`. This file may describe local evidence recording or reporting mechanics, but it must not redefine what counts as mastery evidence.

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

## Evidence-Based Percentage

The percentage is an evidence-based estimate, not an exam score. Eligibility for precise percentages follows `evidence-rules.md`: only produce a precise percentage after at least one completed post-project assessment for the node or equivalent explicit transfer evidence.

If post-project assessment is missing:

- report `assessment: pending`
- use status `reading_completed_assessment_pending` when project coverage exists
- do not claim mastery
- either omit the percentage or present a broad confidence-limited range
- explain that reading/build completion is not mastery evidence

Use this first-version weighting:

```text
boundary coverage: 35%
weakpoint health: 25%
project practice: 20%
user interaction evidence: 15%
transfer evidence: 5%
```

### Boundary Coverage

Use `mastery_policy.senior_ready_requires.required_boundaries`.

Score:

```text
35 * completed_required_boundaries / required_boundary_count
```

A required boundary counts as completed when a completed project has the same `boundary_id`, `build_passed: true`, and `demo_passed: true`.

### Weakpoint Health

Start with 25 points.

For weakpoints under the node:

- subtract 8 for each `open` core FM;
- subtract 4 for each `improving` core FM;
- subtract 0 for `resolved`;
- floor at 0.

Core FM means the FM appears in `weakpoint_routing` or in a required boundary.

### Project Practice

Score up to 20:

- 10 if at least one completed project exists for the node;
- 5 if all counted projects have `build_passed: true`;
- 5 if all counted projects have `demo_passed: true`.

### User Interaction Evidence

Score up to 15:

- 10 points from post-project assessment answers across main-flow reconstruction, boundary ownership, failure classification, bad-design diagnosis, and transfer check.
- plus 5 if at least one project records AI correction followed by improved explanation or transfer evidence.

Use `evidence-rules.md` to decide whether confirmations, user questions, equipment, ask data, reading completion, build/demo success, or transfer examples count as evidence. This section only scores evidence after it is valid under that policy.

### Transfer Evidence

Score 5 if the node has at least `transfer_evidence_min` transfer evidence examples.

## Report Format

```markdown
# <node-id> <node-title> Progress

总体掌握度：<percent or evidence-limited range>（evidence-based estimate，不是考试分数）
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

## Rules

- Follow `evidence-rules.md` for evidence validity.
- Missing logs reduce confidence; say evidence is limited.
- Prefer recommending a single-boundary drill for open core FM weakpoints.
- If mastered, recommend the next nodes from `mastery_policy.if_mastered.recommend_next_nodes`.

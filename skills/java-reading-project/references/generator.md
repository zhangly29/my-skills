# Generator Reference

## Mission

Recommend exactly one corpus-backed, incident-first Java reading project for a selected mapped catalog node.

Use `catalog-training-map.yaml` to understand the node, `progress-state.yaml` to diagnose evidence, and `_derived/recommendation-index.yaml` to choose a single seed or mix scenario. Do not invent project shapes from catalog prose when a corpus-backed candidate exists.

Recommendation wording must follow `evidence-rules.md`: candidate ranking, incident interest, equipment callbacks, and adaptive difficulty are not mastery evidence by themselves.

## Evidence Policy Source

For mastery, transfer, equipment, ask-data, passive-reading, build/demo, and precise-percentage evidence rules, follow `evidence-rules.md`. This file may describe local evidence recording or reporting mechanics, but it must not redefine what counts as mastery evidence.

## Input

```yaml
generation_input:
  workspace: "/abs/path"
  catalog_text: "/abs/path/java-catalog.md"
  corpus: "/abs/path/java-reading-corpus"
  training_map: "/abs/path/java-reading-corpus/_shared/catalog-training-map.yaml"
  recommendation_index: "/abs/path/java-reading-corpus/_derived/recommendation-index.yaml"
  coverage_matrix: "/abs/path/java-reading-corpus/_derived/coverage-matrix.yaml"
  progress_state: "/abs/path/progress-state.yaml"
  progress_summary: "/abs/path/progress.md"
  adaptive_training_data: "/abs/path/adaptive-training-data.yaml"
  node_id: "1.1"
  node_title: "Java 核心语法与面向对象"
  size: "s|m|b"
  teaching_mode: "guided|auto"
  node_map: {}
  node_assessment: {}
  adaptive_profile: {}
  user_adjustment: null
  entry_mode: "incident-first"
```

`teaching_mode` does not change project selection. It only tells the generator whether the builder will pause between Teaching Slices (`guided`) or continue without confirmation (`auto`).

`entry_mode` defaults to `incident-first` in V2-MVP. Use `design-document` only as the fallback when the selected corpus candidate cannot support a credible incident packet. Keep Teaching Slice order stable regardless of the learner's first question.

## Size Semantics

- `s`: one main backend capability unit, one clear flow, usually 1-2 milestones, 3-6 Teaching Slices, reading target 30-60 minutes.
- `m`: 2-4 related capability units, 2-4 milestones, clear package layering, reading target 1-3 hours.
- `b`: 4-8 business flows, 4-6 milestones, multiple packages or bounded contexts, still strictly bounded.

## Training Focus

- A project should be driven by 1-2 primary training points.
- Do not average-cover every catalog concept.
- Familiar or advanced concepts may appear as background, but must not dominate.
- A recommended project must be decomposable into Teaching Slices.
- Each Teaching Slice should map to a capability boundary, not just a file list.
- Avoid project shapes that only make sense if implemented as one large batch.

## Learning Experience

Use `learning-experience.md` when presenting the recommendation. Add story, conflict, role, and curiosity fields to help the learner want to read the project, but do not change candidate ranking, corpus fingerprints, weakpoint routing, or mastery policy.

Experience fields must be grounded in the selected corpus candidate:

- `entry_mode`: `incident-first` by default, or `design-document` only when incident fallback rules require it.
- `incident_packet`: a concrete first artifact the learner sees before code, such as log lines, failed CLI output, alert text, customer ticket, exception trace, retry timeline, stale cache symptom, or bad report excerpt.
- `cold_open`: a concrete backend moment with production signal and cost.
- `role_assignment`: the learner's realistic role and decision responsibility.
- `story_hook`: a real backend case premise; prefer concrete `cold_open` over abstract thesis.
- `case_conflict`: the concrete engineering tension or failure risk.
- `antagonist_design`: a credible bad design or shortcut that exposes the selected FM.
- `role_lens`: 2-4 classes/components explained as system roles.
- `curiosity_trail`: 2-4 questions that make the project worth reading.
- `equipment_callback_candidate`: up to 3 existing equipment items from `progress-state.yaml` that could apply to this project, or `null`.
- `double_demo_plan`: whether this candidate can support `demo-naive` plus `demo`, and which FM the naive demo exposes.
- `adaptive_plan`: how the next project will adjust explanation density, clue exposure, JDK8 bridge notes, equipment callback directness, and assessment follow-up depth.

The `incident_packet` is the learner's first interaction point. It should invite one natural investigation question before the project enters code, but it must not become an assessment prompt or mastery evidence.

### Incident Packet Quality Gate

Before showing a recommendation, verify that the incident packet:

- uses concrete observable evidence from the selected corpus candidate
- has one visible production cost or debugging consequence
- points toward the selected capability boundary without explaining it away
- can be reproduced or approximated by `demo-naive`, `demo-incident`, bad output, or a documented scenario
- is realistic for the domain and not melodramatic

### Incident Fallback

If the selected corpus candidate does not provide forced failure scenarios, FM-backed incident traces, production-shaped failure logs, or enough FM detail to derive a credible incident:

1. Try to derive a concise incident packet from FM IDs and expected production risk.
2. If the incident would be fictional, melodramatic, or unsupported, set `entry_mode: design-document`.
3. In `incident_packet`, write `not_supported` plus the reason.
4. Add `corpus_todo`: a short note that the seed should gain an incident packet or forced failure scenario.
5. Do not invent fictional incidents.

`design-document` fallback starts from `PLAN.md` design intent and bad-design pressure, then still uses the same stable Teaching Slice order and adaptive controls.

## Corpus Candidate Ranking

For mapped nodes:

1. Prefer candidates whose `boundary_id` is in missing required boundaries.
2. Prefer candidates whose `exposes_fm` intersects unresolved core FM IDs.
3. Avoid candidates with completed `seed_id`, completed `cross_id`, or highly similar novelty fingerprint.
4. Keep `single` until `selection_policy.prefer_single_until` is satisfied.
5. Use `mix_candidates` only when `allow_mix_when` is satisfied or the user explicitly asks for mix and prerequisites are acceptable.
6. Prefer `validation_status: validated`, then `runnable`; do not recommend `deprecated`.
7. Prefer candidates that can show a credible incident packet and, for failure-boundary work, a real double demo.
8. Prefer candidates whose difficulty can be kept near the learner's target using the available adaptive controls.
9. Show one recommendation only.

Adaptive profile affects presentation and teaching controls, not corpus truth:

- It may prefer a candidate with a boundary that matches current training need and can be explained at `supportive|standard|stretch`.
- It may not hide required boundaries merely because the learner rated them hard.
- It may not recommend a mastered or repetitive candidate just because it would feel easier.

If the node is missing from `catalog-training-map.yaml`, do not recommend a project. Tell the controller to enter `extends_node`.

## Equipment Callback Matching

After selecting the candidate seed or cross scenario and before showing the recommendation:

1. Read `progress.equipment_unlocked`.
2. For each equipment item, compare its `transfer_contexts`, source boundary, source FM if present, use sentence, and code evidence against the candidate's:
   - `boundary_id`
   - exposed/resolved FM IDs
   - domain
   - io_shape
   - interaction_model
   - teaching slice candidates
3. A match exists when:
   - boundary IDs match or are closely related, or
   - FM IDs match or share the same failure family, or
   - a transfer context clearly maps to the new domain/IO/interaction shape.
4. Attach the top 3 strongest matches as `equipment_callback_candidate`.
5. If no genuine match exists, use `null`.

Do not force a callback just to reuse equipment. A false callback damages trust more than no callback.

## Anti-Repetition

Reject a recommendation if it shares more than two of these major fingerprints with any completed project under the same `node_id`:

- `domain`
- `io_shape`
- `artifact_shape`
- `core_flow`
- `primary_data_structures`
- `interaction_model`

Weakpoints affect concept weighting and scenario selection, but must not force reuse of the same project type.

Example:

```text
Weakpoint: parse vs validate boundary
Allowed new scenarios:
- command parsing vs business rule validation
- JSON config parsing vs domain validation
- HTTP request binding vs application validation
- inventory command parsing vs stock rule validation
```

## Recommendation Format

Output exactly one recommendation:

```markdown
## 推荐项目：<中文项目标题>

- **project-name**: `<kebab-case-name>`
- **source**: `corpus`
- **entry_mode**: `incident-first|design-document`
- **training_mode**: `single|mix`
- **boundary_id**: `<boundary id or null>`
- **seed_id**: `<seed id or null>`
- **cross_id**: `<cross id or null>`
- **validation_status**: `validated|runnable|draft`
- **load_packet**: `<required corpus files>`
- **size**: `s|m|b`
- **enterprise_slice**: `<compressed real backend module>`
- **incident_packet**:
- **corpus_todo**: `<null or missing incident packet note>`
- **cold_open**:
- **role_assignment**:
- **story_hook**:
- **case_conflict**:
- **antagonist_design**:
- **equipment_callback_candidate**: `<up to 3 existing equipment matches or null>`
- **double_demo_plan**: `<demo-naive/demo feasibility and exposed FM>`
- **adaptive_plan**:
  - current_level: `supportive|standard|stretch`
  - basis: `<ask data / assessment / weakpoints / default>`
  - controls: `<explanation_density, clue_exposure, jdk8_bridge, equipment_callback, assessment_followup_depth>`
- **role_lens**:
- **curiosity_trail**:
- **project_type**: `<type>`
- **domain**: `<domain>`
- **io_shape**: `<input -> output>`
- **artifact_shape**: `<runnable artifact>`
- **core_flow**: `<step -> step -> step>`
- **primary_training**: `<1-2 primary training points>`
- **secondary_training**: `<secondary concepts>`
- **background_only**: `<concepts that may appear but must not dominate>`
- **primary_data_structures**: `<List/Map/Queue/etc>`
- **interaction_model**: `<single-run CLI/API/interactive CLI/etc>`
- **teaching_slice_candidates**: `<3-6 capability-boundary slices>`
- **mastery_signal**：
- **node_assessment_summary**：
- **why_this_candidate**：
- **why_this_is_not_toy**：
- **out_of_scope**：
- **做什么**：
- **为什么适合当前节点**：
- **不重复说明**：
- **demo 信号**：
- **正反馈点**：
```

`mastery_signal` describes the intended learning target, not proof that the learner has mastered it.

Then ask:

```text
如果认可，回复 `开始`；如果方向不对，告诉我调整偏好，我会重新推荐 1 个更合适的项目。
```

## Quality Gate

Before showing the recommendation, check:

- runnable and demoable
- selected from `recommendation-index.yaml` using `catalog-training-map.yaml`, `progress-state.yaml`, and `node_assessment`
- anti-repetition against completed projects
- weakpoints addressed without repeating old shape
- existing equipment considered for callback without forcing repetition
- equipment callback matching scans `progress.equipment_unlocked` after candidate selection and attaches only genuine top-3 matches
- adaptive profile considered without changing mapped training need or Teaching Slice order
- selected size is realistic
- real backend capability unit, not a toy scenario
- teachable as 3-6 Teaching Slices, each with a capability boundary and reading checkpoint
- catalog node remains the deliberate-practice boundary through the mapped corpus resources
- includes `entry_mode`, concrete `incident_packet` when supported, concrete `cold_open`, realistic `role_assignment`, real backend `story_hook`, concrete `case_conflict`, credible `antagonist_design`, 2-4 `role_lens` items, and 2-4 `curiosity_trail` questions
- uses `design-document` fallback rather than inventing an unsupported incident
- `double_demo_plan` is honest: `supported` only when the selected FM can produce a credible naive/correct contrast; otherwise state why it is not supported
- `adaptive_plan` is present and conservative; it must default to `standard` when ask data and assessment evidence are missing
- learning-experience prose supports the selected corpus candidate without replacing technical fingerprints

## Anti-Patterns

- Do not show a three-project menu by default.
- Do not offer entry-mode choices in V2-MVP.
- Do not recommend from catalog prose when no mapped corpus-backed candidate exists.
- Do not recommend generic CRUD or superficial input-format rewrites.
- Do not use vague phrases like “练习集合和异常” without concrete class/method landing points.
- Do not promise tests as the main learning artifact.
- Do not generate fantasy/game-like projects unless explicitly requested.
- Do not use abstract textbook story hooks when a concrete production signal can be grounded in the candidate.
- Do not invent a melodramatic incident that the selected corpus candidate cannot support.
- Do not force `incident-first` when the corpus candidate cannot support a credible incident packet.
- Do not claim the learner's first question will reorder the project. In V2-MVP it may set emphasis only.
- Do not claim an equipment callback unless an existing equipment item is present in progress and genuinely applies to the selected boundary.
- Do not use adaptive difficulty to avoid hard required boundaries, repeat an easy project, or infer mastery from ask data.
- Do not propose slice candidates that are only file names.
- Do not use motivational filler instead of concrete backend conflict.
- Do not let narrative replace `boundary_id`, `seed_id`, `cross_id`, novelty fingerprints, or Teaching Slice candidates.

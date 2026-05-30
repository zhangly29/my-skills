# Start Project

## Mission

Recommend exactly one corpus-backed, incident-first Java reading project for a selected mapped catalog node, or safely route unmapped nodes through corpus extension.

Use `catalog-training-map.yaml` to understand the node, `progress-state.yaml` to diagnose evidence, and `_derived/recommendation-index.yaml` to choose a single seed or mix scenario. Do not invent project shapes from `java-catalog.md` prose when a corpus-backed candidate exists.

Runtime command safety follows `runtime-control.md`. Evidence validity follows `evidence-policy.md`. Adaptive controls come from `adaptive-difficulty.md`.

**Owned topics**: `jr start` generation input shape, size semantics, training focus rules, corpus candidate ranking, incident-first recommendation fields, incident packet quality gate, incident fallback to `design-document`, equipment callback matching, anti-repetition fingerprint, **recommendation data layer (YAML)** and learner display layer, recommendation quality gate, unmapped-node extension protocol (`map-only` / `seed-extension` / `boundary-extension`).

**Cross-references**: what evidence to read from progress → `evidence-policy.md`; how the recommendation is consumed as `approved_recommendation` → `build-project.md §Builder Input`; how adaptive level/controls are computed → `adaptive-difficulty.md`; status writes after approval → `runtime-control.md §Active Project Fields`.

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
  build_mode: "normal|follow|micro-follow"
  node_map: {}
  node_assessment: {}
  adaptive_profile: {}
  user_adjustment: null
  entry_mode: "incident-first"
```

`teaching_mode` does not change project selection. It only tells the builder whether to pause between Teaching Slices. `build_mode` controls code visibility after approval, not recommendation ranking.

`entry_mode` defaults to `incident-first`. Use `design-document` only when the selected corpus candidate cannot support a credible incident packet. The Teaching Slice order is fixed by the canonical seed slices (see `SKILL.md §Hard Boundaries`); the learner's first investigation focus may only set emphasis.

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

If the node is missing from `catalog-training-map.yaml`, do not recommend a project. Enter the extension flow below.

## Incident-First Recommendation

Experience fields must be grounded in the selected corpus candidate.

**Source gold-seed material first.** If the selected seed carries authored `incident_packet` and `demo_naive_vs_demo` fields (gold seeds — see `java-reading-corpus/_shared/node-authoring-standard.md`), the recommendation must be built **from them**, not improvised:

- the recommendation `incident_packet` is derived from the seed's `incident_packet` (`alert`/`symptom`/`logs`/`antagonist_code`/`blast_radius`) — reuse its real log lines and antagonist code rather than inventing new ones;
- `antagonist_design` is the seed's `incident_packet.antagonist_code`;
- `double_demo_plan` is populated from the seed's `demo_naive_vs_demo` (`naive`/`demo`/`contrast_signal`);
- per-slice `design_question` and `wrong_answer_implies` come from the seed's `depth_instantiations` slices verbatim — do not paraphrase or replace them.

Only synthesize these fields when the seed lacks them (legacy non-gold seeds). When synthesizing, keep the same density as a gold seed.

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

- uses concrete observable evidence from the selected corpus candidate;
- has one visible production cost or debugging consequence;
- points toward the selected capability boundary without explaining it away;
- can be reproduced or approximated by `demo-naive`, `demo-incident`, bad output, or a documented scenario;
- is realistic for the domain and not melodramatic.

### Incident Fallback

If the selected corpus candidate does not provide forced failure scenarios, FM-backed incident traces, production-shaped failure logs, or enough FM detail to derive a credible incident:

1. Try to derive a concise incident packet from FM IDs and expected production risk.
2. If the incident would be fictional, melodramatic, or unsupported, set `entry_mode: design-document`.
3. In `incident_packet`, write `not_supported` plus the reason.
4. Add `corpus_todo`: a short note that the seed should gain an incident packet or forced failure scenario.
5. Do not invent fictional incidents.

`design-document` fallback starts from `PLAN.md` design intent and bad-design pressure, then still uses the same stable Teaching Slice order and adaptive controls.

## Equipment Callback Matching

After selecting the candidate seed or cross scenario and before showing the recommendation:

1. Read `progress.equipment_unlocked`.
2. For each equipment item, compare its `transfer_contexts`, source boundary, source FM if present, use sentence, and code evidence against the candidate's:
   - `boundary_id`
   - exposed/resolved FM IDs
   - domain
   - `io_shape`
   - `interaction_model`
   - Teaching Slice candidates
3. A match exists when:
   - boundary IDs match or are closely related; or
   - FM IDs match or share the same failure family; or
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

Allowed remediation shapes for the same weakpoint should vary domain, input, flow, or interaction model. For example, a parse-vs-validate weakpoint can move from CSV import to command parsing, JSON config parsing, HTTP request binding, or inventory command parsing.

## Recommendation Format

Output exactly one recommendation. The recommendation has two layers:

1. **Data layer (YAML)** — the structured contract that, after approval, is consumed as `approved_recommendation` by `build-project.md §Builder Input`. The YAML shape below is the single source of truth.
2. **Learner display layer (Chinese markdown)** — a short narrative wrapper for the user. It must derive from the YAML fields, not redefine them.

### Data layer

```yaml
recommendation:
  source: "corpus"
  entry_mode: "incident-first|design-document"
  training_mode: "single|mix"
  boundary_id: "<boundary id or null>"
  seed_id: "<seed id or null>"
  cross_id: "<cross id or null>"
  validation_status: "validated|runnable|draft"
  load_packet:
    required:
      - "<corpus file path>"
      - "<corpus file path>"
  project_name: "<kebab-case-name>"
  size: "s|m|b"
  enterprise_slice: "<compressed real backend module, Chinese>"
  incident_packet:
    kind: "failed output|log|alert|ticket|exception trace|not_supported"
    artifact: "<concrete learner-facing evidence, or null when kind=not_supported>"
    investigation_prompt: "<first low-pressure inspection prompt, or null when kind=not_supported>"
  corpus_todo: "<null or short note when incident-first is not credible>"
  cold_open: "<2-4 concrete sentences, Chinese>"
  role_assignment: "<learner role, Chinese>"
  story_hook: "<real backend case premise, Chinese>"
  case_conflict: "<concrete engineering tension, Chinese>"
  antagonist_design: "<credible bad design that exposes selected FM, Chinese>"
  equipment_callback_candidate: ["<up to 3 existing equipment names>"]  # or null
  double_demo_plan:
    supported: true
    naive_command: "demo-naive"        # omit when supported=false
    correct_command: "demo"            # omit when supported=false
    exposed_fm: ["FM-..."]             # omit when supported=false
  adaptive_plan:
    current_level: "supportive|standard|stretch"
    basis: ["ask data", "assessment", "weakpoints", "default"]
    controls:
      explanation_density: "more|standard|shorter"
      clue_exposure: "conclusion-first|balanced|clue-first"
      jdk8_bridge: "more|standard|brief"
      equipment_callback: "direct|hinted|challenge"
      assessment_followup_depth: "scaffolded|standard|deeper"
  role_lens: ["<2-4 role-as-class items>"]
  curiosity_trail: ["<2-4 questions that make the project worth reading>"]
  project_type: "<type, Chinese>"
  domain: "<domain, Chinese>"
  io_shape: "<input -> output>"
  artifact_shape: "<runnable artifact, Chinese>"
  core_flow: "<step -> step -> step>"
  primary_training: ["<1-2 primary training points>"]
  secondary_training: ["<secondary concepts>"]
  background_only: ["<concepts that may appear but must not dominate>"]
  primary_data_structures: ["List|Map|Queue|..."]
  interaction_model: "<single-run CLI|API|interactive CLI|...>"
  teaching_slice_candidates: ["<3-6 capability-boundary slices>"]
  mastery_signal: "<intended learning target, Chinese>"
  out_of_scope: ["<concepts deliberately excluded>"]
```

Field rules:

- `incident_packet.kind = "not_supported"` requires `corpus_todo` to explain why and what the seed needs.
- `double_demo_plan.supported = false` means omit `naive_command`, `correct_command`, and `exposed_fm`.
- `adaptive_plan.basis` is an array; multiple sources may contribute. Use `["default"]` when no ask data, assessment, or weakpoints exist.
- `mastery_signal` describes the intended learning target, not proof that the learner has mastered it.

This YAML shape can be machine-checked by `python java-reading-project/scripts/validate-progress.py --recommendation -` (pass the YAML on stdin).

### Learner display layer

After the data layer is ready, render a short Chinese display block for the user:

```markdown
## 推荐项目：<中文项目标题>

- 项目: `<project_name>` · 规模 `<size>` · 入口 `<entry_mode>`
- 节点边界: `<boundary_id>` / 种子: `<seed_id>` / cross: `<cross_id or null>`
- 事故现场（incident_packet）:
- 你的身份（role_assignment）:
- 本章对手（antagonist_design）:
- 做什么:
- 为什么适合当前节点:
- 不重复说明（anti-repetition 依据）:
- demo 信号:
- 正反馈点:
- adaptive_plan: `<current_level>` / 控件简述
```

Then ask:

```text
如果认可，回复 `开始`；如果方向不对，告诉我调整偏好，我会重新推荐 1 个更合适的项目。
```

## Recommendation Quality Gate

Before showing the recommendation, check:

- runnable and demoable;
- selected from `recommendation-index.yaml` using `catalog-training-map.yaml`, `progress-state.yaml`, and node assessment;
- anti-repetition against completed projects;
- weakpoints addressed without repeating old shape;
- existing equipment considered for callback without forcing repetition;
- adaptive profile considered without changing mapped training need or Teaching Slice order;
- selected size is realistic;
- real backend capability unit, not a toy scenario;
- teachable as 3-6 Teaching Slices, each with a capability boundary and reading checkpoint;
- catalog node remains the deliberate-practice boundary through mapped corpus resources;
- includes concrete `incident_packet` when supported, concrete `cold_open`, realistic `role_assignment`, real backend `story_hook`, concrete `case_conflict`, credible `antagonist_design`, 2-4 `role_lens` items, and 2-4 `curiosity_trail` questions;
- uses `design-document` fallback rather than inventing an unsupported incident;
- `double_demo_plan` is honest;
- `adaptive_plan` is present and conservative, defaulting to `standard` when ask data and assessment evidence are missing;
- learner-facing prose supports the selected corpus candidate without replacing technical fingerprints.

Optionally machine-check the data layer:

```bash
cat /tmp/recommendation.yaml | python java-reading-project/scripts/validate-progress.py --recommendation -
```

## Unmapped Node Extension

Use this flow when:

- `jr start <node-id>` finds the node in `java-catalog.md` but not in `catalog-training-map.yaml`;
- `jr extend-node <node-id>` is invoked;
- mapped corpus resources cannot remediate unresolved FM weakpoints.

Do not generate a Java project directly from `java-catalog.md` prose.

This flow follows the **Node Authoring Standard** — a node is published only when it reaches *gold* quality (de-homogenized seeds, complete concept coverage, tiered depth, incident density), enforced by `tools/lint-quality.py`. Structural validity alone is not enough.

Required sources:

- `java-catalog.md`
- `java-reading-corpus/_shared/node-authoring-standard.md`
- `java-reading-corpus/_shared/catalog-training-map.yaml`
- `java-reading-corpus/corpus-index.yaml`
- `java-reading-corpus/_derived/recommendation-index.yaml`
- `java-reading-corpus/_derived/coverage-matrix.yaml`
- `java-reading-corpus/_shared/concept-atlas.yaml`
- `java-reading-corpus/_shared/failure-mode-codex.yaml`

Before writing or modifying corpus resources, show:

```text
节点 <node-id> 尚未结构化映射。
我需要先按 Node Authoring Standard 执行 extends_node：
1. 抽取训练意图，列出声明概念
2. 概念 → boundary → FM 映射，补齐无法训练的概念
3. 判断 map-only / seed-extension / boundary-extension
4. 按 gold 质量条写入 authored corpus resources（去同质、事故密度、分层深度）
5. 运行全套校验 + lint-quality 门禁

这会修改 corpus 文件。回复 `开始扩展` 后我再执行。
```

Wait for explicit user approval.

After approval, produce one of:

- `map-only`: add a node entry to `catalog-training-map.yaml` (only when concepts are already covered by gold boundaries);
- `seed-extension`: add or update gold seeds under existing boundaries, then publish the map entry;
- `boundary-extension`: add boundary, at least 3 de-homogenized seeds, required FM references with real detection signals, cross usage, then publish the map entry.

Each seed must satisfy the standard's Quality Bar (unique non-template `design_question`, specific `why_not_toy`, ≤2 shared fingerprint dims among siblings, tiered `m`/`b` with new slices, `incident_packet` + `demo_naive_vs_demo`).

Run after edits, in order:

```bash
source ~/.zshrc
.venv/bin/python java-reading-corpus/tools/validate-corpus.py
.venv/bin/python java-reading-corpus/tools/check-coverage.py
.venv/bin/python java-reading-corpus/tools/build-index.py
.venv/bin/python java-reading-corpus/tools/lint-quality.py --node <node-id>
```

If any check fails, fix authored files. Do not patch generated files to hide failures. Publish `quality_status: gold` only after `lint-quality.py` passes. Node `1.1` is the worked reference to emulate.

## Anti-Patterns

- Do not show a three-project menu by default.
- Do not offer entry-mode choices in v2.3.
- Do not recommend from catalog prose when no mapped corpus-backed candidate exists.
- Do not recommend generic CRUD or superficial input-format rewrites.
- Do not use vague phrases like "练习集合和异常" without concrete class/method landing points.
- Do not promise tests as the main learning artifact.
- Do not force equipment callbacks.
- Do not claim the learner's first question will reorder the project. It may set emphasis only.

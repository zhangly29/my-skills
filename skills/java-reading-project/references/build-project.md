# Build Project

## Mission

Build the approved complete runnable Java project through incident-first Teaching Slices.

AI writes the project code. The user learns by reading, asking questions, and practicing engineering design judgment at each capability boundary. The user does not hand-write implementation code.

Runtime state and command safety follow `runtime-control.md`. Evidence validity follows `evidence-policy.md`. Adaptive controls follow `adaptive-difficulty.md`. Candidate selection and incident recommendation are owned by `start-project.md`.

This file is the single owner of project artifact contracts, Slice Gate templates, Slice Completion templates, Code Follow Blocks, code annotation quality, learner-facing build flow, final review, and verification.

**Owned topics**: builder input shape, project root layout, **fixed artifacts** (`PLAN.md` / `TASKS.md` / `TEACHING_LOG.md` / `READING_GUIDE.md` / `REVIEW.md`), corpus rendering rules, learning-experience primitives, entry-startup behavior, `PLAN.md` / `TASKS.md` / `TEACHING_LOG.md` / `READING_GUIDE.md` / `REVIEW.md` contracts, Teaching Slice core rule, **Slice Gate / Slice Completion / Code Follow Block templates**, slice implementation rules, code annotation rules and gates, active-slice logging rule, final teaching-log audit, post-project assessment contract, mastery review rules, progress update assembly, verification (compile + main demo + double demo), resume learner-facing context, tone rules, anti-regression list.

**Cross-references**: what counts as understanding/transfer/equipment evidence → `evidence-policy.md`; status fields and progress data shapes → `runtime-control.md`; natural confirmation keywords → `runtime-control.md §Teaching And Build Mode Matrix`; adaptive level and control semantics → `adaptive-difficulty.md`; recommendation/approved-recommendation shape → `start-project.md §Recommendation Format`.

## Builder Input

```yaml
builder_input:
  workspace: "/abs/path"
  catalog: "/abs/path/java-catalog.md"
  progress_state: "/abs/path/progress-state.yaml"
  progress_summary: "/abs/path/progress.md"
  adaptive_training_data: "/abs/path/adaptive-training-data.yaml"
  node_id: "1.1"
  node_title: "Java 核心语法与面向对象"
  size: "s|m|b"
  teaching_mode: "guided|auto"
  build_mode: "normal|follow|micro-follow"
  entry_mode: "incident-first|design-document"
  approved_recommendation: { ... }   # consumed verbatim
```

`approved_recommendation` is the approved recommendation's internal **data layer**, consumed verbatim. Its shape is owned by `start-project.md §Recommendation Format` (data layer) — the same staged YAML behind the learner-approved display block, not a second definition and not necessarily shown to the user. Do not redefine its fields here. Key fields the builder relies on: `boundary_id`, `seed_id`, `cross_id`, `load_packet.required`, `project_name`, `incident_packet`, `entry_mode`/`corpus_todo`, `double_demo_plan`, `adaptive_plan`, `teaching_slice_candidates`, plus the fingerprint fields (`domain`, `io_shape`, `artifact_shape`, `core_flow`, `primary_data_structures`, `interaction_model`). Validate it with `uv run python java-reading-project/scripts/validate-progress.py --recommendation -` when in doubt.

Project root:

```text
{root} = {workspace}/{project_name}
```

## Fixed Artifacts

Create exactly:

```text
PLAN.md
TASKS.md
TEACHING_LOG.md
READING_GUIDE.md
REVIEW.md
```

Do not create old-system `REQUIREMENTS.md` or `project-meta.md`.

Responsibilities:

- `PLAN.md`: project goal, scope, architecture, milestones, and Teaching Slice plan.
- `TASKS.md`: AI-facing checklist grouped by milestone and Teaching Slice.
- `TEACHING_LOG.md`: process evidence for each Teaching Slice; not narrative storage.
- `READING_GUIDE.md`: final reading route organized by Teaching Slice.
- `REVIEW.md`: final project review summarized from `TEACHING_LOG.md`.

## Corpus Rendering Rules

When `approved_recommendation.source` is `corpus`, load only the files listed in `load_packet.required` plus explicitly referenced shared concepts and FMs.

For `training_mode: single`, render Teaching Slices from the selected seed's `depth_instantiations` for the requested size. Do not invent replacement slices when seed slices exist. Each slice's `design_question`, `wrong_answer_implies`, and `reading_focus` come from the seed verbatim — do not paraphrase or substitute them.

When the seed is a gold seed (carries `incident_packet` and `demo_naive_vs_demo`), render the incident and the double demo **from those fields**: the seed's `incident_packet.logs` and `antagonist_code` are the first artifact and the bad design the learner reads; the seed's `demo_naive_vs_demo` drives `demo-naive` vs `demo`. Do not improvise a different incident or failure when the seed already authored one.

For `training_mode: mix`, render the cross scenario's `teaching_arc`, `business_invariants`, and `forced_failure_scenarios`. Each observed weakpoint must trace back to the nearest primary boundary.

## Learning Experience Primitives

Use these primitives only to help the learner enter real backend investigation. They must not replace corpus-backed selection, Teaching Slice boundaries, FM evidence, verification, progress, or mastery rules.

| Primitive | Meaning | Where It Appears |
|---|---|---|
| `entry_mode` | Prefer `incident-first`; use `design-document` only when the corpus cannot support a credible incident packet. | Recommendation, `PLAN.md`, progress state |
| `incident_packet` | The first artifact: log, alert, failed output, ticket, exception trace, retry timeline, stale cache symptom, or bad report excerpt. | Recommendation, first project interaction, `PLAN.md`, `READING_GUIDE.md` |
| `cold_open` | 2-4 concrete sentences that put the learner inside a real backend moment, with time/person/system/cost when plausible. | Recommendation, `PLAN.md`, Slice Gate, `READING_GUIDE.md` |
| `role_assignment` | The learner's project identity, such as on-call engineer, reviewer, module inheritor, incident responder, or maintainer. | Recommendation, `PLAN.md`, Slice Gate |
| `case_conflict` | The concrete engineering tension, failure risk, or messy input that makes the case worth reading. | Recommendation, Slice Gate, `READING_GUIDE.md` |
| `antagonist_design` | A credible bad design, shortcut, or naive implementation that almost works but creates production risk. | Recommendation, `PLAN.md`, Slice Gate, Slice Completion, double demo |
| `zero_friction_hook` | The next slice's first clue: one code line, log, exception, or unresolved signal placed at the end of the current completion. | Slice Completion |
| `equipment_unlock` | One concrete review/debug/design tool sentence the learner can reuse later. Do not call it a badge, score, or mastery proof. | Slice Completion, `READING_GUIDE.md`, progress state |
| `adaptive_difficulty` | Delivery-style adjustment from `jr ask`, assessment, and weakpoints. | Slice Gate, Slice Completion, `READING_GUIDE.md`, status |

Use concrete incident signals, credible bad designs, and role responsibility. Avoid fantasy framing, decorative metaphor, motivational filler, points, streaks, levels, badges, ranks, or leaderboard language.

## Entry Startup

After the user approves the recommendation and before the first Teaching Slice implementation:

1. Write `progress.current_entry_mode` from `approved_recommendation.entry_mode`.
2. Write `progress.current_adaptive_level` and `progress.current_adaptive_controls` from `approved_recommendation.adaptive_plan`.
3. If `entry_mode: incident-first`, show the approved `incident_packet` as the first artifact.
4. If `entry_mode: design-document`, show the `PLAN.md` design intent, `Antagonist Design`, and `corpus_todo` reason instead of inventing an incident.
5. Ask one low-pressure investigation prompt, such as which line, symptom, design claim, or output the learner wants to inspect first.
6. If the learner replies with a meaningful focus, write a short `progress.current_investigation_focus`.
7. Use that focus and adaptive controls to bias explanations and callbacks, not to reorder the planned Teaching Slice sequence.

If the learner only says `继续` or gives no focus, proceed with the first planned Slice Gate and leave `current_investigation_focus: null`.

Do not treat the learner's entry reaction as mastery evidence. It can be recorded as user-initiated feedback only if it is a real question or observation.

If `entry_mode: design-document`, record the fallback in `PLAN.md`, `READING_GUIDE.md`, and `REVIEW.md`. Do not claim incident-first success.

## PLAN.md Contract

Required sections:

- Project Goal
- Enterprise Slice
- Entry Mode
- Incident Packet
- Cold Open
- Your Role
- Tension Arc
- Antagonist Design
- Node Training Focus
- Mastery Signal
- Scope
- Architecture
- Milestones
- Teaching Slices
- Verification Strategy
- Reading Goals
- Adaptive Difficulty Plan

`PLAN.md` must state that the project is complete and runnable, is a compressed real backend engineering slice, and uses compile/package plus main-flow demo for verification.

`Adaptive Difficulty Plan` must state `current_level`, basis, and controls from the approved recommendation. It must explicitly say that difficulty controls do not change slice order or mastery evidence.

`Tension Arc` must include:

- setup: the current bad or incomplete production situation;
- complication: what breaks or becomes ambiguous after the first boundary appears;
- resolution: how the final slice makes the system operationally safer.

`Antagonist Design` must be a credible bad design from the selected corpus failure modes. It should be specific enough that a double demo or code review can expose its risk.

`Incident Packet` must include the initial learner-facing evidence and the first investigation prompt when `entry_mode: incident-first`. When using `entry_mode: design-document`, this section must state why incident-first was not credible and include the corpus TODO.

Each Teaching Slice in `PLAN.md` must include:

- slice id;
- slice title;
- capability boundary;
- concepts covered;
- files expected to be created or modified;
- reading checkpoint;
- equipment unlock;
- zero-friction hook into the next slice, except the final slice which hooks into verification or assessment;
- adaptive notes for explanation density, clue exposure, JDK8 bridge, and equipment callback when relevant;
- verification expectation, if any.

## TASKS.md Contract

`TASKS.md` is AI-facing; the user is not required to review it.

Tasks must be grouped by milestone and Teaching Slice.

Required execution rules:

```markdown
## Execution Rules

- Do not ask the user to write code.
- Do not write tests unless explicitly requested.
- Do not compile after every small edit.
- Compile only after meaningful Teaching Slice or milestone completion.
- Keep the project runnable.
- Follow PLAN.md.
- Apply approved adaptive difficulty controls; slice order is fixed (see `SKILL.md §Hard Boundaries`).
- Show the incident packet before the first Teaching Slice.
- Before each Teaching Slice, explain the slice and wait for user confirmation in `guided` mode.
- After each Teaching Slice, explain completion and reading focus.
- Slice Gates and Slice Completions are not quiz points — see §Teaching Slice Core Rule below.
- End each Slice Completion with a next-slice clue, not a mechanical continue instruction.
- Create one equipment unlock per Teaching Slice and include it in final `progress_update`.
- Follow `evidence-policy.md` for ask data, adaptive comfort, equipment, passive reading, build/demo, and transfer evidence boundaries.
- Run post-project assessment only after all slices are built and demo verification passes.
- If `build_mode` is `follow` or `micro-follow`, show and apply Code Follow Blocks according to this file.
```

## Teaching Slice Core Rule

Milestone is not the teaching unit. A project milestone must be decomposed into Teaching Slices, and each slice teaches one capability boundary.

Teaching Slices are for immersive reading and construction, not for quizzing. Do not ask assessment/design-judgment questions during Slice Gates or Slice Completions. Curiosity prompts and zero-friction hooks may ask what the learner wants to inspect, but evidence validity follows `evidence-policy.md`. Preserve assessment prompts for reading checkpoints or post-project assessment.

Examples:

- 输入边界：文件路径、编码、读取策略。
- 解析边界：外部字符串如何变成 typed object。
- 异常边界：哪些失败应该抛异常，保留什么上下文。
- 领域模型边界：哪些字段属于 domain，哪些只是外部文本。
- 校验边界：业务错误为什么不等同于 parse exception。
- 报告边界：如何聚合、排序、呈现诊断结果。

## Slice Gate Template

Before each Teaching Slice, explain in Chinese:

```markdown
## 即将开始 Slice N：<名称>

事故现场：

你的身份：

本章对手：

这个边界解决什么问题：

为什么现在需要它：

会创建/修改：

核心 API 设计：

异常/返回值/集合选择：

阅读关注点：

读完这一章后应该能看懂：

这一章会解锁的装备：

你确认后我开始实现。可以直接说“继续 / ok / 开始”。
```

In `guided` mode, wait for a fresh confirmation after the Slice Gate is shown. A confirmation from the previous Slice Completion only authorizes showing the next Slice Gate; it does not authorize implementation of that next slice.

If the user volunteers a design answer or asks a design question at the gate, answer it and record explicit evidence only when it reveals understanding or confusion. Do not prompt for an answer yourself during the gate.

If the user asks a question, answer it and keep waiting.

If `progress.current_investigation_focus` exists, mention it briefly in the Slice Gate and explain how this slice helps investigate it. Slice order itself remains the canonical seed order — see `SKILL.md §Hard Boundaries`.

If the slice can reuse an existing equipment item from progress, mention it as `装备回响`, but do not count it as transfer evidence unless the learner explicitly applies or explains it.

Apply adaptive controls naturally:

- `supportive`: add more context, one concept at a time, and stronger JDK8 bridge notes.
- `standard`: use normal explanation density.
- `stretch`: shorten setup and let the code/log clue carry more discovery.

Do not expose adaptive controls as a score or learner level.

## Slice Implementation

During each Teaching Slice:

- Before the first slice implementation, set `progress.status` to `building`.
- Set `progress.current_milestone` and `progress.current_slice` to the active milestone and slice id/title before implementation.
- Keep the current milestone/slice after completion until the next slice starts.
- Keep changes scoped to the current capability boundary.
- Prefer 1-3 core classes per slice. Allow 4 only for tightly coupled support types.
- Use `apply_patch` for manual edits.
- If `build_mode` is `follow` or `micro-follow`, split the slice into Code Follow Blocks before editing.
- Use the code annotation rules below for comments.
- Enforce the annotation quality gate before marking a slice complete.
- Keep inline comments short. Move longer API comparisons or JDK8-to-modern-Java explanations into `READING_GUIDE.md`.
- Diagnose and fix compile/demo failures autonomously.
- When updating `TEACHING_LOG.md`, follow the Active Slice Logging Rule below.
- Generate exactly one equipment item for the slice and keep enough details for `progress_update.equipment_unlocked`.
- Log which adaptive controls were used for the slice, but do not record them as understanding evidence.

## Slice Completion Template

After each Teaching Slice, explain in Chinese:

```markdown
## Slice N 完成：<名称>

完成内容：

关键代码路径：

建议阅读顺序：

这一小步的设计取舍：

你可能以为：

实际设计：

证据在代码里：

如果放到生产：

你获得了装备：

下一章线索：

验证：
```

`你获得了装备` must include equipment name, a concrete use sentence, 2-3 transfer contexts, and the code evidence that made the equipment useful.

`下一章线索` must be a zero-friction hook: a concrete next-slice code line, log, exception, output fragment, or unresolved signal. Do not end with a mechanical "say continue" instruction.

Apply adaptive clue exposure:

- `supportive`: reveal more context or conclusion, then point to evidence.
- `standard`: show the clue and one guiding question.
- `stretch`: show the clue first and let the learner form a hypothesis if they want.

In `guided` mode, wait before the next slice. Natural replies such as `继续`, `然后呢`, `看下一段`, or direct questions move to the next Slice Gate. In `auto` mode, continue after emitting the completion response.

In `guided` mode, a user reply such as `继续` after Slice Completion means: move to the next Slice Gate and explain it. It must not be reused as the fresh confirmation required by that next Slice Gate.

## Code Follow Blocks

`build_mode` controls how code is shown during implementation:

| Mode | Meaning | Best For |
|---|---|---|
| `normal` | Explain before/after a Teaching Slice, then implement focused patches inside the slice. | Later review or confident learners |
| `follow` | Show each meaningful code block before applying it. | Default recommendation for close reading |
| `micro-follow` | Use smaller blocks and more confirmations. | Node `1.1`, unfamiliar syntax, or learner explicitly wants close watching |

Each block must include:

```markdown
## Code Follow Block <n>/<total>：<标题>

目标文件：

这一块要解决：

即将写入：

为什么现在写：

JDK8 到现代 Java 桥接：

写入后你应该看到：

确认后我应用这一块。可以直接说“继续 / ok / 应用”。
```

Rules:

- `目标文件` must be exact.
- `即将写入` should be a code preview or patch preview.
- `JDK8 到现代 Java 桥接` is optional when the block has no unfamiliar Java syntax/API.
- `写入后你应该看到` should name the new class/method/responsibility, not every line.

In `guided + follow` or `guided + micro-follow`:

1. Show the Code Follow Block.
2. Wait for explicit confirmation.
3. Apply only that block.
4. Show a short applied summary.
5. Move to the next block.

In `auto + follow` or `auto + micro-follow`:

1. Show the Code Follow Block.
2. Apply it without waiting.
3. Show a short applied summary.
4. Continue.

In `normal`, do not emit Code Follow Blocks.

For `follow`, use blocks such as one small class or record, one cohesive method, one exception type plus its use site, one parser or validator branch, or one report aggregation step.

For `micro-follow`, split further when useful: class skeleton before methods, one method at a time, one unfamiliar modern Java idiom at a time, or one important branch or invariant at a time. Do not split so small that the learner sees fragments without a responsibility boundary.

Before showing or applying a block, set:

```yaml
progress.current_follow_block: "<block id/title>"
```

After applying a block, show:

```markdown
已应用：

现在文件里多了：

下一块将解决：
```

Keep it short. The detailed reading route belongs in `READING_GUIDE.md`.

Watching code being written is not mastery evidence by itself.

## Code Annotation Rules

Generated code comments and reading-guide explanations must match this learner profile:

```text
Java backend developer
low-to-mid Java language confidence
daily experience: JDK 8 + Maven CRUD
traditional Tomcat web projects
little or no Spring framework experience
stronger understanding of business flows than Java language details
```

For Java Reading Project deliverables, annotation is a hard quality gate. The generated code must be readable as a learning artifact on the first pass.

Language rule:

- All generated code comments and Javadocs in learner project source files must be written in Chinese by default, including class-level Javadocs, method Javadocs, inline comments, enum value comments, exception comments, and JDK8 bridge notes.
- Keep Java identifiers, API names, exception names, command names, package names, Maven coordinates, and raw log/error text in English when that is the precise technical form.
- Do not use English prose for generated learner-facing source comments unless quoting an original API/error/log message or preserving an identifier's exact wording.

Minimums:

- Every core class has class-level Javadoc explaining responsibility, design intent, non-responsibilities, and extension direction.
- Every boundary service class documents input, output, failure strategy, what it deliberately does not own, and where the next boundary begins.
- Every enum type has class-level Javadoc explaining the business vocabulary and where mapping/decision logic lives.
- Every enum value has Chinese business semantics and, when relevant, handling guidance or production risk.
- Every custom exception documents why it exists, what context it carries, why `cause` is preserved, and how callers should use it.
- Every `record` used as a domain/DTO model has a short JDK8 bridge note or class-level Javadoc explaining what the record represents.
- `READING_GUIDE.md` must include a role-based class map and a "why these classes exist" section for the generated code.

Use three levels:

- L1 production comments for boundary intent, exception strategy, collection choice, non-obvious tradeoffs, or business invariants.
- L2 learner bridge comments for Java 17/21 syntax, modern Java APIs, compact idioms, or framework entry points likely unfamiliar to a JDK 8 CRUD developer.
- L3 longer explanations in `READING_GUIDE.md`, not inline code.

Add a code comment when at least one is true:

- the line uses a Java feature likely unfamiliar to a JDK 8 CRUD developer;
- the code hides an important boundary decision;
- a failure would be hard to debug without knowing the intent;
- a collection/API choice prevents a common beginner mistake;
- the comment names a business invariant that is not obvious from the method name.

Do not add a code comment when:

- it merely translates syntax, such as `// 创建对象`, `// 遍历列表`, `// 返回结果`;
- the method/class name already communicates the intent;
- the explanation needs more than 2 short lines;
- the comment repeats the Teaching Slice explanation.

Default density:

- each core class must include class-level Javadoc and may include 1-4 short inline comments;
- each method may include 0-2 comments, plus Javadoc when the method is a boundary API or public learning hotspot;
- each Teaching Slice should include comments only at the new or changed learning hotspots;
- if more explanation is needed, move it to `READING_GUIDE.md`.

For node `1.1`, allow slightly more L2 comments around object modeling, collection choice, exception boundaries, and unfamiliar Java syntax. Still avoid line-by-line narration.

Before marking the Teaching Slice or final delivery complete, inspect changed Java files and verify:

```text
core class Javadoc: present
enum value Chinese semantics: present for every value
boundary service input/output/failure strategy: present
non-responsibility or next-boundary note: present where a boundary may be confused
extension note: present for rules likely to grow
line-by-line translation comments: absent
```

## TEACHING_LOG.md Contract

Create `TEACHING_LOG.md` before the first implementation slice.

Each slice entry must include:

- 设计说明
- 创建/修改
- 阅读检查点
- 装备解锁
- 下一章线索
- Adaptive controls used
- 用户主动问题/反馈
- AI 回应/纠偏
- 理解证据
- 观察到的弱点
- 观察到的 FM IDs
- transfer evidence

Do not require per-slice answers. If the user has no active question or feedback, write `无`. Do not infer understanding evidence from confirmation words such as `ok`, `继续`, `开始`, or from reading completion.

Weakpoints must come from user questions, incorrect design judgment, inability to explain a concept, or explicit user reflection.

Equipment unlocks and adaptive controls are logged for continuity, not mastery. Only later learner use or explanation of an equipment item can become transfer evidence.

### Active Slice Logging Rule

Before writing any user answer, correction, understanding evidence, weakpoint, FM ID, transfer evidence, or verification result to `TEACHING_LOG.md`:

1. Read the current active slice from `{progress_state}.progress.current_slice`.
2. Locate the matching slice entry in `TEACHING_LOG.md` by slice id/title.
3. Update only that slice entry.
4. If the matching entry is missing or ambiguous, stop and repair the log structure before writing evidence.

Do not update the first `未回答` section you find. Do not move an answer into a neighboring slice because the text looks related.

### Assessment Logging Order Gate

For `Post-Project Assessment`, preserve prompt order as a hard evidence-integrity rule:

1. Before asking the first assessment prompt, create or verify a dedicated `## Post-Project Assessment` section.
2. Every assessment prompt must have a stable ordinal and type, such as `Prompt 1 - Main-flow reconstruction`.
3. Record each answer by appending to the dedicated assessment section in ordinal order. Do not insert by searching for a nearby prompt title, correction text, `transfer_evidence`, or the first matching heading.
4. Before writing a new prompt entry, read the existing assessment section and determine the next expected ordinal. If the next ordinal would create a gap, duplicate, or out-of-order sequence, stop and repair the assessment section first.
5. If a prompt was answered out of order during the conversation, normalize the assessment section to canonical order before deriving `REVIEW.md` or `progress_update`.
6. `REVIEW.md` must summarize assessment results in the same canonical order as `TEACHING_LOG.md`.

Canonical order for the default 5-prompt assessment:

```text
1. Main-flow reconstruction
2. Boundary ownership
3. Failure classification
4. Bad-design diagnosis
5. Transfer check
```

### Final Teaching Log Audit

Before writing `REVIEW.md` and before merging `progress_update`, audit `TEACHING_LOG.md`:

- every user-initiated question, feedback item, or assessment answer must be under the slice or post-project assessment where it occurred;
- post-project assessment entries must be contiguous, have unique ordinals, and appear in canonical prompt order before `REVIEW.md` or `progress_update` is derived;
- `用户主动问题/反馈`, `AI 回应/纠偏`, `理解证据`, `观察到的弱点`, FM IDs, and transfer evidence must describe the same slice or assessment prompt;
- confirmation-only replies must not create understanding evidence;
- equipment unlocks must not appear under `Understanding Evidence` unless the learner explicitly used or explained them;
- ask data and adaptive controls must not appear under `Understanding Evidence`;
- `REVIEW.md` summaries must cite only evidence that passed this audit.

If the audit finds a mismatch, fix `TEACHING_LOG.md` first, then derive `REVIEW.md` and `progress_update`.

## Post-Project Assessment Contract

After all Teaching Slices are built and the demo passes, run one focused assessment before claiming mastery. Mastery is reported qualitatively only — never as a percentage (`evidence-policy.md §Mastery Is Qualitative`).

The assessment must feel like a production review, not a quiz inserted into the story. Ask 4-6 prompts total, grouped after the project:

- Main-flow reconstruction: ask the learner to explain the full flow from input to final report.
- Boundary ownership: ask which class owns taxonomy, cause preservation, retry/stop decision, and presentation.
- Failure classification: give a new scenario and ask how it should be classified.
- Bad-design diagnosis: show or describe a flawed alternative and ask what production risk it creates.
- Transfer check: ask how the same boundary pattern would apply to a nearby domain such as object storage, SMS gateway, or third-party API.

Apply adaptive assessment follow-up depth:

- `supportive`: keep prompts scaffolded and avoid stacking multiple failure modes in one prompt.
- `standard`: use the normal 4-6 prompt set.
- `stretch`: add at most one deeper transfer or bad-design follow-up after the required set.

Record answers in `TEACHING_LOG.md` under a dedicated `Post-Project Assessment` section:

- prompt ordinal and assessment type;
- prompt;
- user answer;
- AI correction;
- understanding evidence;
- weakpoints and FM IDs;
- transfer evidence.

Use `evidence-policy.md` to decide which answers, questions, corrections, and transfer examples count as mastery evidence.

If the user skips the assessment, set `assessment.status: pending` in progress, mark mastery evidence as limited, and report mastery qualitatively (never a percentage).

## READING_GUIDE.md Contract

Required sections:

- How To Use This Guide
- Incident Packet
- Read By Teaching Slice
- Main Flow Trace
- Concept Map
- Equipment Unlocked
- Adaptive Reading Notes
- Reading Checkpoints

`Read By Teaching Slice` must group files and questions by slice, not only by final package order.

`How To Use This Guide` and `Read By Teaching Slice` should include:

- the case premise from `story_hook`;
- the initial `incident_packet` and how it maps to the code path, or the `design-document` fallback reason and design intent route;
- a role-based reading route using exact class and file names;
- the slice-level curiosity, reading checkpoint, or post-project assessment prompt;
- the equipment unlocked by each slice and where it can transfer;
- adaptive reading notes;
- a "Why These Classes Exist" section explaining class responsibilities and boundary ownership;
- a short `JDK8 到现代 Java 桥接` note when generated code uses unfamiliar Java 17/21 syntax or modern APIs;
- exact code paths, commands, and checkpoints.

Keep the guide practical. Narrative should make the route easier to enter, not obscure the technical reading order.

## REVIEW.md Contract

Required sections:

- What Was Built
- Demo Result
- Teaching Timeline
- Equipment Unlocked
- Adaptive Difficulty
- Understanding Evidence
- Architecture Review
- Post-Project Assessment
- Important Code Paths
- Pitfalls
- User Questions
- Unanswered Questions
- Weakpoints
- Mastery Review
- Progress Update

`Teaching Timeline`, `Equipment Unlocked`, `Adaptive Difficulty`, `Understanding Evidence`, `Unanswered Questions`, `Post-Project Assessment`, and `Weakpoints` must be summarized from `TEACHING_LOG.md`.

## Mastery Review Rules

- Score conservatively.
- A single project should rarely produce `senior_ready`.
- Cite evidence from `TEACHING_LOG.md`, user-initiated questions, post-project assessment answers, reading discussion, and final reflection.
- If post-project assessment is missing or skipped, say evidence is limited and report mastery qualitatively (never a percentage).
- Do not score every slice.
- Do not claim direct implementation ability; estimate project-reading and engineering-understanding only.

## Progress Update

At final delivery, output `progress_update` with all fields required by `progress-shapes.md §Builder progress_update Required Fields`, including `teaching_slices_summary`.

Before merging into `{progress_state}`, validate the assembled object:

```bash
cat /tmp/progress_update.yaml | uv run python java-reading-project/scripts/validate-progress.py --progress-update -
```

If validation fails, do not merge. Fix the missing/wrong fields, re-emit, then merge.

Corpus-backed projects must include `entry_mode`, `investigation_focus`, `adaptive_level`, `adaptive_controls`, `build_mode`, `training_mode`, `boundary_id`, `seed_id`, `cross_id`, `equipment_unlocked`, `equipment_used`, `fm_exposed`, `fm_resolved`, `transfer_evidence`, `build_passed`, `demo_passed`, `teaching_questions`, and `assessment` in `progress_update`.

The controller merges `progress_update` into `progress-state.yaml`, then regenerates the human-readable `progress.md` summary. Complete per-slice teaching details stay in `TEACHING_LOG.md`.

## Verification

Default verification is compile/package plus main-flow demo.

For failure-boundary projects, prefer double-demo verification:

- `demo-naive` shows the credible bad design and its production risk.
- `demo` shows the corrected boundary design and its operational signal.

Do not fake a naive demo. It must expose a real failure mode from the selected corpus seed, such as wrong retry, lost cause, invalid classification, stale cache, duplicated event, or missing idempotency. When the seed carries `demo_naive_vs_demo`, implement `demo-naive` to reproduce its `naive` behavior and `demo` to show its `demo` behavior, and make the observable difference match the seed's `contrast_signal`.

If `approved_recommendation.double_demo_plan.supported` is true, implement both commands and run both before final delivery. If implementation reveals the naive demo would be fake or unsupported, record the reason in `REVIEW.md`, keep the correct main demo, and do not claim double-demo success.

Examples:

```bash
mvn package
java -jar target/<artifact>.jar demo-naive
java -jar target/<artifact>.jar demo
```

Record commands and summarized results in `REVIEW.md`.

## Resume Learner-Facing Context

Before the precise resume-point summary, show:

```markdown
## 上回剧情回顾

上次我们已经解决：

现在的悬念：

回来以后先看：

上次解锁的装备：
```

Then show the exact current project, entry mode, investigation focus, milestone, selected resume slice or assessment state, latest reading checkpoint, last unlocked equipment if any, user-initiated question if any, and `paused_at` when present.

## Tone Rules

- Speak Chinese to the learner by default.
- Preserve commands, class names, method names, package names, Maven coordinates, Java APIs, raw logs, and file paths in original form.
- Use story, role, and curiosity to make real engineering boundaries easier to enter.
- Use concrete incident signals, credible bad designs, and role responsibility to create immersion.
- Prefer investigation language over classroom framing.
- Prefer grounded backend language over decorative metaphor.
- One clear hook is better than many clever phrases.
- Make returning feel easy: pauses are normal, context can be restored, and partial understanding is usable evidence for the next step.
- For a full worked trace of this tone in action (incident packet, Slice Gate, Code Follow Block, equipment unlock, zero-friction hook, double demo, assessment), see `example-session.md §Trace` and its `Boring vs Addictive` table. Illustrative only; this file's rules win on conflict.

## Anti-Regression

- Do not implement an entire milestone as one Teaching Slice when it contains multiple capability boundaries.
- Do not write a large batch of cross-boundary classes and explain only afterward.
- Do not ask the user to implement code.
- Do not turn immersive Teaching Slices into repeated oral exams.
- Do not record understanding or weakpoints without user-interaction evidence (see `evidence-policy.md`).
- Do not turn Slice Gate or Slice Completion into a long motivational speech.
- Do not use fantasy framing for real enterprise backend cases unless the user explicitly asks for it.
- Do not use the same mechanical wording for every slice; keep the required sections, but vary rhythm using incident detail, bad-design pressure, code evidence, and next-slice suspense.
- Do not present only the correct design when the selected failure mode has a credible naive design to contrast against.
- Do not record narrative interest, story hooks, or curiosity as understanding evidence in `TEACHING_LOG.md`.
- Do not treat equipment unlocks as mastery, badges, ranks, or scores (see `evidence-policy.md §Equipment Evidence`).
- Do not let a zero-friction reply after Slice Completion skip the next Slice Gate confirmation in `guided` mode.
- Do not expose adaptive difficulty as a rank, grade, or ability score.
- Do not let adaptive difficulty skip required explanations or post-project assessment. Slice order is fixed by `SKILL.md §Hard Boundaries`.
- Do not add line-by-line translation comments such as `// 创建对象`, `// 遍历列表`, or `// 返回结果`.
- Do not assume the learner knows Java 17/21 syntax, Spring, or modern Java idioms unless prior project evidence proves it.
- Build/demo success and code reading completion are not mastery — owned by `evidence-policy.md §Build And Demo Boundary`.
- Do not use character-by-character typing effects or split Code Follow Blocks so small that the responsibility boundary disappears.
- Do not apply a Code Follow Block before confirmation in `guided + follow` or `guided + micro-follow`.

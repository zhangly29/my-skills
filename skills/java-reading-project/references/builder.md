# Builder Reference

## Mission

Build the approved complete runnable Java project through incident-first Teaching Slices.

AI writes the project code. The user learns by reading, asking questions, and practicing engineering design judgment at each capability boundary. The user does not hand-write implementation code.

Builder state transitions and command safety follow `command-matrix.md`; learner evidence validity follows `evidence-rules.md`.

## Evidence Policy Source

For mastery, transfer, equipment, ask-data, passive-reading, build/demo, and precise-percentage evidence rules, follow `evidence-rules.md`. This file may describe local evidence recording or reporting mechanics, but it must not redefine what counts as mastery evidence.

## Input

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
  approved_recommendation:
    source: "corpus"
    entry_mode: "incident-first|design-document"
    training_mode: "single"
    boundary_id: "B-lang-exception"
    seed_id: "payment-gateway-errors"
    cross_id: null
    validation_status: "runnable"
    load_packet:
      required:
        - "boundaries/lang-runtime/B-lang-exception.yaml"
        - "scenarios/B-lang-exception/seed-payment-gateway-errors.yaml"
    project_name: "supplier-product-import-core"
    enterprise_slice: "external supplier data import boundary"
    incident_packet:
      kind: "failed output|log|alert|ticket|exception trace"
      artifact: "concrete learner-facing incident evidence"
      investigation_prompt: "first low-pressure inspection prompt"
    corpus_todo: null
    story_hook: "供应商脏数据入境检查站：外部商品数据进入系统前，先被翻译、校验和汇总成可诊断报告。"
    case_conflict: "如果 parse、validate、report 边界混在一起，脏数据会变成难排查的线上问题。"
    equipment_callback_candidate: null
    double_demo_plan:
      supported: true
      naive_command: "demo-naive"
      correct_command: "demo"
      exposed_fm: ["FM-..."]
    adaptive_plan:
      current_level: "supportive|standard|stretch"
      basis: ["ask data", "assessment", "weakpoints"]
      controls:
        explanation_density: "more|standard|shorter"
        clue_exposure: "conclusion-first|balanced|clue-first"
        jdk8_bridge: "more|standard|brief"
        equipment_callback: "direct|hinted|challenge"
        assessment_followup_depth: "scaffolded|standard|deeper"
    role_lens: ["Parser 像翻译官", "Validator 像质检员", "ImportReport 像结案报告"]
    curiosity_trail: ["为什么不直接边读文件边判断业务规则？", "哪些错误应该抛异常，哪些应该进入报告？"]
    project_type: "CLI/main demo"
    domain: "supplier product import"
    io_shape: "supplier product text file -> import report"
    artifact_shape: "runnable CLI application"
    core_flow: "read lines -> parse row -> validate fields -> validate business rules -> aggregate report"
    primary_training: ["异常边界", "面向对象建模"]
    secondary_training: ["集合选择", "IO/NIO"]
    background_only: ["泛型"]
    primary_data_structures: ["List", "Map"]
    interaction_model: "single-run CLI demo"
    teaching_slice_candidates: ["输入边界", "解析边界", "校验边界", "报告边界"]
    mastery_signal: "understand how external string input becomes typed, diagnosable backend data"
    out_of_scope: ["database", "Spring Boot", "Web API", "Excel", "async import"]
```

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

## Corpus Rendering Rules

When `approved_recommendation.source` is `corpus`, load only the files listed in `load_packet.required` plus explicitly referenced shared concepts and FMs.

For `training_mode: single`, render Teaching Slices from the selected seed's `depth_instantiations` for the requested size. Do not invent replacement slices when seed slices exist.

For `training_mode: mix`, render the cross scenario's `teaching_arc`, `business_invariants`, and `forced_failure_scenarios`. Each observed weakpoint must trace back to the nearest primary boundary.

Responsibilities:

- `PLAN.md`: project goal, scope, architecture, milestones, and Teaching Slice plan.
- `TASKS.md`: AI-facing checklist grouped by milestone and Teaching Slice.
- `TEACHING_LOG.md`: process evidence for each Teaching Slice; not narrative storage.
- `READING_GUIDE.md`: final reading route organized by Teaching Slice.
- `REVIEW.md`: final project review summarized from `TEACHING_LOG.md`.

## Language And Comment Rules

Learning artifact prose must be Simplified Chinese by default.

Keep these in English or original form:

- class, method, package, and variable names
- Maven coordinates, XML, commands, and paths
- Java API names
- raw logs, exception names, and compiler output
- ecosystem terms such as `Optional`, `Stream`, `ThreadLocal`, `Map`, `List`, `Set`

Use `code-annotation.md` to decide generated code comments for the learner profile: JDK 8 + Maven CRUD, traditional Tomcat web, limited Spring exposure, stronger business-flow understanding than Java language confidence.

Code comments should be Chinese by default and purposeful. Annotation is a mandatory delivery standard for reading projects, not optional polish. Use three levels:

- L1 production comments for boundary intent, exception strategy, collection choice, non-obvious tradeoffs, or business invariants.
- L2 learner bridge comments for Java 17/21 syntax, modern Java APIs, compact idioms, or framework entry points likely unfamiliar to a JDK 8 CRUD developer.
- L3 longer explanations in `READING_GUIDE.md`, not inline code.

Do not add comments that merely translate code, such as `// 创建一个列表`, `// 遍历数组`, or `// 返回结果`.

For node `1.1`, allow slightly more L2 comments around object modeling, collection choice, exception boundaries, and unfamiliar Java syntax. Still avoid line-by-line narration.

Mandatory annotation gate before final delivery:

- every core class has class-level Javadoc with responsibility, design intent, non-responsibilities, and extension direction
- every enum type explains the business vocabulary and every enum value has Chinese business semantics
- every boundary service documents input, output, failure strategy, next boundary, and what it deliberately does not own
- every custom exception documents carried context, `cause` preservation, and caller expectations
- `READING_GUIDE.md` contains a role-based class map and explains why the main classes exist

If this gate fails, fix comments before running final review or merging progress.

## Learning Experience Rules

Use `learning-experience.md` for learner-facing orientation and reading flow:

- V2-MVP prefers `entry_mode: incident-first`. Show the incident packet before code and before design-document orientation when supported. If the approved recommendation uses `entry_mode: design-document`, start from `PLAN.md` design intent and the credible bad-design pressure instead.
- Use `adaptive-difficulty.md` to apply the approved `adaptive_plan`. Difficulty controls may change explanation density and clue exposure, but not Teaching Slice order, code architecture, required explanations, or mastery policy.
- `PLAN.md` must include `Entry Mode`, `Incident Packet`, `Cold Open`, `Your Role`, `Tension Arc`, and `Antagonist Design` when the selected corpus candidate supports a realistic incident-shaped case.
- `READING_GUIDE.md` should carry most of the narrative reading experience: incident packet, case premise, role-based reading route, equipment list, exact code paths, and checkpoints.
- `TEACHING_LOG.md` remains evidence-oriented. Do not record story hooks, curiosity, or user enthusiasm as understanding evidence.
- `REVIEW.md` may include concise "what this case taught" language, but `Mastery Review` remains evidence-based.
- `progress-state.yaml` and `progress.md` must stay lightweight and must not store the full narrative. Store short entry mode, investigation focus, and equipment data only.

Experience language must support the engineering boundary. It must not replace corpus-backed slice rendering, FM evidence, verification, or conservative mastery judgment.

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

Do not treat the learner's entry reaction as mastery evidence. It can be recorded as `用户主动问题/反馈` only if it is a real question or observation.

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

- setup: the current bad or incomplete production situation
- complication: what breaks or becomes ambiguous after the first boundary appears
- resolution: how the final slice makes the system operationally safer

`Antagonist Design` must be a credible bad design from the selected corpus failure modes. It should be specific enough that a double demo or code review can expose its risk.

`Incident Packet` must include the initial learner-facing evidence and the first investigation prompt when `entry_mode: incident-first`. When using `entry_mode: design-document`, this section must state why incident-first was not credible and include the corpus TODO.

Each Teaching Slice in `PLAN.md` must include:

- slice id
- slice title
- capability boundary
- concepts covered
- files expected to be created or modified
- reading checkpoint
- equipment unlock
- zero-friction hook into the next slice, except the final slice which hooks into verification or assessment
- adaptive notes for explanation density, clue exposure, JDK8 bridge, and equipment callback when relevant
- verification expectation, if any

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
- Apply approved adaptive difficulty controls without changing Teaching Slice order.
- Show the incident packet before the first Teaching Slice.
- Before each Teaching Slice, explain the slice and wait for user confirmation in `guided` mode.
- After each Teaching Slice, explain completion and reading focus.
- Do not ask assessment/design-judgment questions during slice gates or completions.
- End each Slice Completion with a next-slice clue, not a mechanical continue instruction.
- Create one equipment unlock per Teaching Slice and include it in final `progress_update`.
- Follow `evidence-rules.md` for ask data, adaptive comfort, equipment, passive reading, build/demo, and transfer evidence boundaries.
- Run post-project assessment only after all slices are built and demo verification passes.
- If `build_mode` is `follow` or `micro-follow`, show and apply Code Follow Blocks according to `code-follow.md`.
```

## Code Follow Contract

When `build_mode` is `follow` or `micro-follow`, use `code-follow.md` during implementation:

- split each Teaching Slice into meaningful Code Follow Blocks before editing files
- show target file, intent, code or patch preview, why-now explanation, and JDK8 bridge note when relevant
- in `guided + follow`, wait for confirmation before applying each block
- in `auto + follow`, show each block and apply it without waiting
- update `progress.current_follow_block` before showing or applying each block
- clear `progress.current_follow_block` when the Teaching Slice is complete

`micro-follow` uses smaller blocks than `follow`, but still keeps responsibility boundaries. Do not use character-by-character or line-by-line spectacle.

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

### Final Teaching Log Audit

Before writing `REVIEW.md` and before merging `progress_update`, audit `TEACHING_LOG.md`:

- every user-initiated question, feedback item, or assessment answer must be under the slice or post-project assessment where it occurred
- `用户主动问题/反馈`, `AI 回应/纠偏`, `理解证据`, `观察到的弱点`, FM IDs, and transfer evidence must describe the same slice or assessment prompt
- confirmation-only replies must not create understanding evidence
- equipment unlocks must not appear under `Understanding Evidence` unless the learner explicitly used or explained them
- ask data and adaptive controls must not appear under `Understanding Evidence`
- `REVIEW.md` summaries must cite only evidence that passed this audit

If the audit finds a mismatch, fix `TEACHING_LOG.md` first, then derive `REVIEW.md` and `progress_update`.

## Post-Project Assessment Contract

After the project builds and the main-flow demo passes, create a `Post-Project Assessment` section in `TEACHING_LOG.md` and ask the learner one compact assessment set.

Required assessment areas:

- full main-flow reconstruction
- class responsibility and boundary ownership
- one new failure classification scenario
- one bad-design diagnosis
- one transfer scenario to a nearby backend domain

Record:

- prompt
- user answer
- AI correction
- understanding evidence
- weakpoints and FM IDs
- transfer evidence

If the user skips the assessment, set `assessment.status: pending` in progress, mark mastery evidence as limited, and do not write a precise mastery percentage.

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

- the case premise from `story_hook`
- the initial `incident_packet` and how it maps to the code path, or the `design-document` fallback reason and design intent route
- a role-based reading route using exact class and file names
- the slice-level curiosity, reading checkpoint, or post-project assessment prompt
- the equipment unlocked by each slice and where it can transfer
- adaptive reading notes: where extra bridge/context was added or where clue exposure was intentionally harder
- a "Why These Classes Exist" section explaining class responsibilities and boundary ownership
- a short `JDK8 到现代 Java 桥接` note when generated code uses unfamiliar Java 17/21 syntax or modern APIs
- exact code paths, commands, and checkpoints

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
- If post-project assessment is missing or skipped, say evidence is limited and do not write a precise mastery percentage.
- Do not score every slice.
- Do not claim direct implementation ability; estimate project-reading and engineering-understanding only.

## Progress Update

At final delivery, output `progress_update` with all fields required by `references/progress-contract.md`, including `teaching_slices_summary`.

Corpus-backed projects must include `entry_mode`, `investigation_focus`, `adaptive_level`, `adaptive_controls`, `build_mode`, `training_mode`, `boundary_id`, `seed_id`, `cross_id`, `equipment_unlocked`, `equipment_used`, `fm_exposed`, `fm_resolved`, `transfer_evidence`, `build_passed`, `demo_passed`, `teaching_questions`, and `assessment` in `progress_update`.

The controller merges `progress_update` into `progress-state.yaml`, then regenerates the human-readable `progress.md` summary. Complete per-slice teaching details stay in `TEACHING_LOG.md`.

## Verification

Default verification is compile/package plus main-flow demo.

For failure-boundary projects, prefer double-demo verification:

- `demo-naive` shows the credible bad design and its production risk.
- `demo` shows the corrected boundary design and its operational signal.

Do not fake a naive demo. It must expose a real failure mode from the selected corpus seed, such as wrong retry, lost cause, invalid classification, stale cache, duplicated event, or missing idempotency.

If `approved_recommendation.double_demo_plan.supported` is true, implement both commands and run both before final delivery. If implementation reveals the naive demo would be fake or unsupported, record the reason in `REVIEW.md`, keep the correct main demo, and do not claim double-demo success.

Examples:

```bash
mvn package
java -jar target/<artifact>.jar demo-naive
java -jar target/<artifact>.jar demo
```

Record commands and summarized results in `REVIEW.md`.

# Learning Experience Reference

## Mission

Make Java Reading Project feel like investigating a real backend incident, while preserving evidence-based Teaching Slices, corpus-backed recommendation, progress tracking, pause/resume, and conservative mastery judgment.

Use this reference only for learner-facing orientation, curiosity, reading flow, and return context. It must never replace the technical contract in `generator.md`, `builder.md`, `teaching-slices.md`, `progress-contract.md`, or `node-assessment.md`.

## Evidence Policy Source

For mastery, transfer, equipment, ask-data, passive-reading, build/demo, and precise-percentage evidence rules, follow `evidence-rules.md`. This file may describe local evidence recording or reporting mechanics, but it must not redefine what counts as mastery evidence.

## Non-Goals

- Do not add points, streaks, badges, ranks, leaderboards, or check-in pressure.
- Do not shame the learner for pauses, low energy, incomplete answers, or partial understanding.
- Do not say `你应该已经掌握`, `你落后了`, `打卡失败`, or similar pressure phrases.
- Do not turn real backend projects into fantasy/game scenarios unless the user explicitly requests that style.
- Do not claim understanding, mastery, or transfer evidence from narrative engagement; evidence validity follows `evidence-rules.md`.

Narrative is encouraged when it is grounded in a real backend incident, concrete role pressure, failure cost, and design tradeoff. Ban fantasy framing and motivational filler; do not ban realistic incident texture.

## Experience Primitives

Use these primitives when they help the learner enter the project:

| Primitive | Meaning | Where It Appears |
|---|---|---|
| `entry_mode` | V2-MVP prefers `incident-first`; `design-document` is allowed only when the corpus cannot support a credible incident packet. | Recommendation, `PLAN.md`, progress state |
| `incident_packet` | The first artifact: log, alert, failed output, ticket, exception trace, retry timeline, stale cache symptom, or bad report excerpt. | Recommendation, first project interaction, `PLAN.md`, `READING_GUIDE.md` |
| `cold_open` | 2-4 concrete sentences that put the learner inside a real backend moment, with time/person/system/cost when plausible. | Recommendation, `PLAN.md`, Slice Gate, `READING_GUIDE.md` |
| `role_assignment` | The learner's project identity, such as on-call engineer, reviewer, module inheritor, incident responder, or maintainer. | Recommendation, `PLAN.md`, Slice Gate |
| `story_hook` | A short real-backend case premise that names the business situation. Prefer a concrete `cold_open` over an abstract hook. | Recommendation, `PLAN.md`, `READING_GUIDE.md` |
| `case_conflict` | The concrete engineering tension, failure risk, or messy input that makes the case worth reading. | Recommendation, Slice Gate, `READING_GUIDE.md` |
| `antagonist_design` | A credible bad design, shortcut, or naive implementation that almost works but creates production risk. | Recommendation, `PLAN.md`, Slice Gate, Slice Completion, double demo |
| `tension_arc` | Project-level setup -> complication -> resolution showing how each slice changes the situation. | `PLAN.md`, `READING_GUIDE.md` |
| `role_lens` | 2-4 key classes/components explained as system roles. | Recommendation, Slice Completion, `READING_GUIDE.md` |
| `curiosity_trail` | 2-4 project-level questions that invite reading. | Recommendation, `READING_GUIDE.md` |
| `curiosity_question` | One slice-level question that makes the next boundary interesting. | Slice Gate |
| `aha_moment` | A contrast-driven "you might think X, but actual design is Y, because Z" moment grounded in code evidence. | Slice Completion, `REVIEW.md` |
| `production_relevance` | Why this judgment matters in production behavior, debugging, or maintainability. | Slice Completion, `READING_GUIDE.md`, `REVIEW.md` |
| `equipment_unlock` | One concrete review/debug/design tool sentence the learner can reuse later. Do not call it a badge, score, or mastery proof. | Slice Completion, `READING_GUIDE.md`, progress state |
| `zero_friction_hook` | The next slice's first clue: one code line, log, exception, or unresolved signal placed at the end of the current completion. | Slice Completion |
| `callback_from_last_project` | A weakpoint or misconception from progress state that reappears as a case tension in the new project. | Recommendation, `PLAN.md`, Slice Gate |
| `equipment_callback` | A prior equipment item that applies again in the new project; if the learner uses it, record transfer evidence. | Recommendation, Slice Gate, post-project assessment |
| `adaptive_difficulty` | Delivery-style adjustment from `jr ask`, assessment, and weakpoints; it changes explanation density, clue exposure, bridge notes, callback directness, and follow-up depth. | Recommendation, Slice Gate, Slice Completion, `READING_GUIDE.md`, status |
| `return_recap` | A friendly context restore after a pause or resume. | `jr resume` |

## Command Integration

### `jr start`

When showing a recommendation, include:

```markdown
- **entry_mode**: `incident-first|design-document`
- **incident_packet**:
- **cold_open**:
- **role_assignment**:
- **story_hook**:
- **case_conflict**:
- **antagonist_design**:
- **equipment_callback_candidate**:
- **double_demo_plan**:
- **adaptive_plan**:
- **role_lens**:
- **curiosity_trail**:
```

These fields must be based on the selected corpus candidate. They are learner-facing orientation only; they must not replace `boundary_id`, `seed_id`, `cross_id`, fingerprints, training focus, or Teaching Slice candidates.

`adaptive_plan` should be phrased as reading support, not as a learner grade:

```text
这次我会多给一点 JDK8 到现代 Java 的桥接，并把下一章线索露得更明确一点。
```

Do not say:

```text
你的等级是 supportive。
```

The first learner-facing interaction after approval should show `incident_packet` before code. Ask one low-pressure investigation prompt, such as:

```text
先看这段现场输出。你不用回答标准答案，只说你第一眼最想查哪一处。
```

Record the learner's response as `progress.current_investigation_focus` when it identifies a useful focus. This focus changes emphasis and callbacks, not Teaching Slice order.

If `entry_mode: design-document`, do not fake an incident. Start with the design intent and bad-design pressure:

```text
这个 corpus seed 还没有可信事故现场素材，所以这次先从设计意图切入：我们看它想防住哪种坏设计，以及代码怎样把边界立起来。
```

Record the fallback reason and corpus TODO in project artifacts.

`incident_packet` quality gate:

- include observable evidence, not only prose
- reveal a consequence or cost
- leave one unresolved question
- stay short enough to read before the learner commits to the project
- never imply that the learner's first reaction is mastery evidence

`cold_open` quality gate:

- use a concrete moment, not an abstract thesis
- include at least one observable production signal such as alarm, log, queue, timeout, customer ticket, retry storm, stale cache, bad report, or incident review
- include a consequence or cost
- stay realistic and concise

`role_assignment` quality gate:

- assign the learner a real backend role, such as `on-call`, `reviewer`, `module inheritor`, `incident responder`, or `maintainer`
- describe what decision the learner is responsible for
- do not call the learner a hero, player, warrior, or fantasy role

### Teaching Slice Gate

Add these sections before the technical boundary explanation:

```markdown
事故现场：

你的身份：

本章对手：

本章要解决：
```

`事故现场` should make the slice feel like a concrete production moment in 1-3 sentences.

`你的身份` should remind the learner of the role and local decision responsibility.

`本章对手` should name a credible bad design or shortcut for this slice.

`本章要解决` should state the exact capability boundary.

The curiosity question may still appear, but it should invite reading rather than force an answer, such as:

```text
为什么我们不在读取文件时直接判断所有业务规则，而要先把字符串变成 typed object？
```

The curiosity question should invite a design hypothesis. It should not feel like an exam.

If `progress.current_investigation_focus` exists, connect it to the slice in one sentence:

```text
你刚才盯住的是 `<focus>`；这一章先把它背后的边界补上。
```

Do not pretend the focus changed the slice order in V2-MVP.

If an existing equipment item applies, add a short `装备回响` line:

```text
装备回响：上次的 `<equipment>` 在这里能用，但这次先看它会不会失效。
```

If adaptive controls apply, fold them naturally into the explanation. Example:

```text
这里我会先把结论说出来，再带你回到代码证据；这个边界上次你标过偏难。
```

Do not announce a hidden ranking or ability level.

### Teaching Slice Completion

Add these sections after the design tradeoff:

```markdown
你可能以为：

实际设计：

证据在代码里：

如果放到生产：

你获得了装备：

下一章线索：
```

`你可能以为` names the tempting naive assumption or bad design.

`实际设计` names the correct boundary decision.

`证据在代码里` points to exact class/method/branch evidence.

`如果放到生产` connects that judgment to debugging, data correctness, cost, latency, maintainability, or failure recovery.

`你获得了装备` states one concrete capability the learner can now use in code review, debugging, or design discussion. It must include:

- equipment name
- one usable sentence the learner could paste or say in review/debug/design
- 2-3 transfer contexts
- why it is useful, grounded in this slice's code

`下一章线索` is the zero-friction hook. End on the next slice's first unresolved code/log/exception clue. Do not write a mechanical "say continue to proceed" line.

Keep both sections short. They should sharpen the learning moment, not become motivational speeches.

### Zero-Friction Continuation

At the end of each Slice Completion, place a concrete next-slice clue and stop there. Examples:

```text
下一章线索：

日志里还有一行没有解释：

    [16:00:12] pay-3471 attempt 1 gateway: TIMEOUT

这次问题不是网关返回了什么，而是：TIMEOUT 到底是谁抛出来的？
```

Rules:

- The hook points to the next planned Teaching Slice.
- The hook may ask a curiosity question, but it must not evaluate the learner.
- Natural replies such as `继续`, `然后呢`, `看下一段`, or a direct question move to the next Slice Gate.
- In `guided` mode, moving to the next Slice Gate is not permission to implement that slice; the Slice Gate still needs fresh confirmation.
- In `auto` mode, emit the hook briefly and continue.

### Equipment Rules

Equipment is a reusable engineering tool, not gamification.

Quality gate:

- one slice unlocks exactly one equipment item
- name it as a practical tool, such as `Exhaustive Switch 反问`, `Cause Chain 保留检查`, or `Non-retryable Failure 追问`
- include a use sentence suitable for review/debug/design
- include transfer contexts
- write it to progress through `progress_update.equipment_unlocked`
- evidence validity for equipment unlocks and equipment transfer follows `evidence-rules.md`

### `jr resume`

Before the precise resume-point summary, show:

```markdown
## 上回剧情回顾

上次我们已经解决：

现在的悬念：

回来以后先看：

上次解锁的装备：
```

Then show the exact current project, entry mode, investigation focus, milestone, selected resume slice or assessment state, latest reading checkpoint, last unlocked equipment if any, user-initiated question if any, and `paused_at` when present.

## Artifact Boundaries

- `PLAN.md`: must include `Entry Mode`, `Incident Packet`, `Cold Open`, `Your Role`, `Tension Arc`, and `Antagonist Design` for new V2-MVP reading projects. If `entry_mode: design-document`, `Incident Packet` states the fallback reason and corpus TODO instead of fake incident evidence.
- `TASKS.md`: stays AI-facing and should not become narrative-heavy.
- `TEACHING_LOG.md`: remains evidence-oriented. Do not record story hooks as understanding evidence.
- `READING_GUIDE.md`: should carry most of the narrative reading experience, including the incident packet, case premise, role-based reading route, equipment list, exact code paths, adaptive reading notes, and checkpoints.
- `REVIEW.md`: may include concise case-learning language, but `Mastery Review` remains evidence-based.
- `progress-state.yaml` and `progress.md`: stay lightweight. Store equipment names/use sentences and short investigation focus, not full narrative text.

## Tone Rules

- Speak Chinese to the learner by default.
- Preserve commands, class names, method names, package names, Maven coordinates, Java APIs, raw logs, and file paths in original form.
- Use story, role, and curiosity to make real engineering boundaries easier to enter.
- Use concrete incident signals, credible bad designs, and role responsibility to create immersion.
- Prefer investigation language over classroom framing.
- Prefer grounded backend language over decorative metaphor.
- One clear hook is better than many clever phrases.
- Make returning feel easy: pauses are normal, context can be restored, and partial understanding is usable evidence for the next step.

## Anti-Patterns

- Adding points, streaks, levels, badges, ranks, or leaderboard language.
- Calling equipment a reward, badge, rank, or proof of mastery.
- Calling adaptive difficulty a grade, rank, ability label, or proof of mastery.
- Turning every component into a metaphor until the actual class responsibility becomes fuzzy.
- Writing long motivational passages before every slice.
- Using fantasy framing for real enterprise backend scenarios.
- Using abstract textbook hooks when a concrete production moment can be stated.
- Showing only the correct design when a credible bad design would make the tradeoff visible.
- Creating a fake incident that cannot be reproduced, approximated, or explained by the selected corpus candidate.
- Ending Slice Completion with a mechanical confirmation line instead of a next-slice clue.
- Replacing corpus-backed selection, Teaching Slice boundaries, or FM evidence with narrative prose.
- Treating `story_hook`, curiosity, or user enthusiasm as proof of mastery.

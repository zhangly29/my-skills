# Teaching Slices

## Mission

Define Teaching Slice rhythm, slice gates, slice completion, post-project assessment placement, FM logging, and transfer-evidence recording for Java Reading Project builds.

## Evidence Policy Source

For mastery, transfer, equipment, ask-data, passive-reading, build/demo, and precise-percentage evidence rules, follow `evidence-rules.md`. This file may describe local evidence recording or reporting mechanics, but it must not redefine what counts as mastery evidence.

## Core Rule

Milestone is not the teaching unit. A project milestone must be decomposed into Teaching Slices, and each slice teaches one capability boundary.

Use `learning-experience.md` to make each slice easier to enter: incident evidence, story, curiosity, equipment, and adaptive difficulty controls should support the capability boundary, not replace API, exception, collection, verification, or evidence details.

Teaching Slices are for immersive reading and construction, not for quizzing. Do not ask assessment/design-judgment questions during Slice Gates or Slice Completions. Curiosity prompts and zero-friction hooks may ask what the learner wants to inspect, but evidence validity follows `evidence-rules.md`. Preserve assessment prompts as reading checkpoints or post-project assessment items.

Examples:

- 输入边界：文件路径、编码、读取策略。
- 解析边界：外部字符串如何变成 typed object。
- 异常边界：哪些失败应该抛异常，保留什么上下文。
- 领域模型边界：哪些字段属于 domain，哪些只是外部文本。
- 校验边界：业务错误为什么不等同于 parse exception。
- 报告边界：如何聚合、排序、呈现诊断结果。

## Teaching Modes

Default is `guided`.

For the authoritative `teaching_mode x build_mode` matrix, follow `command-matrix.md`.

- `guided`: stop before each Teaching Slice only for build confirmation and after each Teaching Slice for reading pause or user-initiated questions. Do not quiz the learner during the slice flow.
- `auto`: do not wait for confirmation, but still output every Teaching Slice story, boundary explanation, completion explanation, reading focus, and `TEACHING_LOG.md` update. Do not emit assessment questions during the build.

## Build Modes

Default is `normal`.

- `normal`: implement the Teaching Slice with focused patches after the Slice Gate confirmation.
- `follow`: use `code-follow.md` to show meaningful Code Follow Blocks before applying them.
- `micro-follow`: use smaller Code Follow Blocks for close reading, especially for node `1.1` or unfamiliar Java syntax.

`teaching_mode` controls confirmation rhythm. `build_mode` controls code visibility.

Accepted confirmations:

```text
继续
ok
开始
go
没问题
下一个
```

## Slice Gate

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

If `progress.current_investigation_focus` exists, mention it briefly in the Slice Gate and explain how this slice helps investigate it. Do not change the planned Teaching Slice order in V2-MVP.

If the slice can reuse an existing equipment item from progress, mention it as `装备回响`, but do not count it as transfer evidence unless the learner explicitly applies or explains it.

If `progress.current_adaptive_controls` exists, apply it to the Slice Gate:

- `supportive`: add more context, one concept at a time, and stronger JDK8 bridge notes.
- `standard`: use normal explanation density.
- `stretch`: shorten setup and let the code/log clue carry more of the discovery.

Do not expose adaptive controls as a score or learner level. Phrase changes naturally.

## Slice Implementation

During each Teaching Slice:

- Before the first slice implementation, set `progress.status` to `building`.
- Set `progress.current_milestone` and `progress.current_slice` to the active milestone and slice id/title before implementation.
- Keep the current milestone/slice after completion until the next slice starts.
- Keep changes scoped to the current capability boundary.
- Prefer 1-3 core classes per slice. Allow 4 only for tightly coupled support types.
- Use `apply_patch` for manual edits.
- If `build_mode` is `follow` or `micro-follow`, split the slice into Code Follow Blocks before editing. Follow `code-follow.md` for preview, confirmation, apply, and applied-summary behavior.
- Use `code-annotation.md` for comments. Add purposeful Chinese comments for boundary intent, exception strategy, collection choice, non-obvious tradeoffs, business invariants, and learner bridge points such as Java 17/21 syntax or modern APIs unfamiliar to a JDK 8 CRUD developer.
- Enforce the code annotation delivery gate before marking a slice complete: every core class added or changed by the slice has class-level Javadoc; every enum value has Chinese business semantics; every boundary service documents input, output, failure strategy, non-responsibilities, and extension notes where relevant.
- Keep inline comments short. Move longer API comparisons or JDK8-to-modern-Java explanations into `READING_GUIDE.md`.
- Diagnose and fix compile/demo failures autonomously.
- When updating `TEACHING_LOG.md`, follow `builder.md` Active Slice Logging Rule; never write evidence to a neighboring slice by text search alone.
- Generate exactly one equipment item for the slice and keep enough details for `progress_update.equipment_unlocked`.
- Log which adaptive controls were used for the slice, but do not record them as understanding evidence.

## Slice Completion

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

Before final delivery, run the `builder.md` Final Teaching Log Audit and fix any mismatch before deriving `REVIEW.md`, weakpoints, or `progress_update`.

## Post-Project Assessment

After all Teaching Slices are built and the demo passes, run one focused assessment before claiming mastery or writing a precise mastery percentage.

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

Record answers in `TEACHING_LOG.md` under a dedicated `Post-Project Assessment` section. Use `evidence-rules.md` to decide which answers, questions, corrections, and transfer examples count as mastery evidence.

## FM And Transfer Evidence

When a corpus seed or cross scenario provides `wrong_answer_implies` or `expected_fm`, Teaching Slice logs must preserve those FM IDs.

If the user answers a post-project assessment prompt incorrectly, or volunteers a design explanation that reveals confusion, map the correction to the relevant FM ID. If the user asks a question that reveals confusion, record the nearest FM ID only when evidence is explicit.

Transfer evidence means the user explains how the same boundary or concept applies to a different domain, input shape, or failure mode. Do not infer transfer evidence from project completion alone.

Equipment transfer evidence means the learner explicitly uses a previously unlocked equipment item in a new slice, project, or assessment answer. Do not infer equipment transfer from showing an equipment callback.

## Anti-Regression

- Do not implement an entire milestone as one Teaching Slice when it contains multiple capability boundaries.
- Do not write a large batch of cross-boundary classes and explain only afterward.
- Do not ask the user to implement code.
- Do not turn immersive Teaching Slices into repeated oral exams.
- Do not record understanding or weakpoints without user-interaction evidence.
- Do not turn Slice Gate or Slice Completion into a long motivational speech.
- Do not use fantasy framing for real enterprise backend cases unless the user explicitly asks for it.
- Do not use the same mechanical wording for every slice; keep the required sections, but vary rhythm using incident detail, bad-design pressure, code evidence, and next-slice suspense.
- Do not present only the correct design when the selected failure mode has a credible naive design to contrast against.
- Do not record narrative interest, story hooks, or curiosity as understanding evidence in `TEACHING_LOG.md`.
- Do not treat equipment unlocks as mastery, badges, ranks, or scores.
- Preserve the planned Teaching Slice sequence.
- Do not let a zero-friction reply after Slice Completion skip the next Slice Gate confirmation in `guided` mode.
- Do not expose adaptive difficulty as a rank, grade, or ability score.
- Do not let adaptive difficulty skip required explanations, post-project assessment, or Teaching Slice order.
- Do not add line-by-line translation comments such as `// 创建对象`, `// 遍历列表`, or `// 返回结果`.
- Do not assume the learner knows Java 17/21 syntax, Spring, or modern Java idioms unless prior project evidence proves it.
- Do not treat build/demo success or code reading completion as mastery.
- Do not use character-by-character typing effects or split Code Follow Blocks so small that the responsibility boundary disappears.
- Do not apply a Code Follow Block before confirmation in `guided + follow` or `guided + micro-follow`.

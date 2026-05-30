---
name: java-reading-project
description: "Use when the user runs any `jr ...` command (`jr start`, `jr resume`, `jr ask`, `jr progress`, `jr weak`, `jr status`, `jr pause`, `jr extend-node`) inside a Java reading-project workspace."
---

# Java Reading Project

**Version:** v2.3

## Mission

Run the Java Reading Project learning workflow from one entrypoint. The user learns by investigating incident-first, complete runnable Java projects built by AI, then practicing engineering design judgment after the project is runnable. The user does not hand-write implementation code.

Speak Chinese to the user by default. Keep commands, paths, class names, method names, package names, Maven coordinates, Java APIs, raw logs, and technical identifiers in original form.

## Runtime Packets

Load only the packet path needed for the current command phase. Detailed per-command load paths live in `runtime-control.md §Runtime Load Paths`; do not duplicate that table here.

| Packet | Owns (single source of truth) |
|---|---|
| `references/runtime-control.md` | command routing, runtime load paths, read/write surfaces, progress state overview, status transitions, failure priority, pause/resume, abandonment, generated-file safety, natural confirmation keywords |
| `references/progress-shapes.md` | `progress-state.yaml` data shapes (`completed_projects`/`weakpoints`/`equipment_unlocked`/`adaptive_summary`/`next_project_bias`), anti-repetition fingerprints, builder `progress_update` required field set |
| `references/evidence-policy.md` | mastery / transfer / equipment / ask-data / passive-reading / build-demo evidence rules, qualitative-only mastery reporting (no precise percentages) |
| `references/start-project.md` | `jr start` recommendation data layer, corpus-backed selection, incident fallback, anti-repetition, equipment callback matching, unmapped-node extension |
| `references/build-project.md` | approved project construction, Teaching Slice / Slice Gate / Slice Completion / Code Follow Block templates, code annotation, artifacts, verification, final review |
| `references/assessment-progress.md` | `jr progress`, `jr weak`, `jr status` reporting details, node mastery estimate, weakpoint interpretation |
| `references/adaptive-difficulty.md` | `jr ask`, perceived-difficulty data shape, adaptive profile, adaptive difficulty controls |

The validator `scripts/validate-progress.py` is the runtime source of truth for every data shape called out by these packets (see `--help`).

For a full worked `jr start` → build → demo → assessment trace showing the intended learner-facing feel, see `references/example-session.md`. It is an illustrative golden example to emulate when generating sessions, not a rule source — when it conflicts with a packet, the packet wins.

## Hard Boundaries

The five non-negotiable rules. Every other restriction lives in the owning packet — find it via the table above.

1. Do not ask the user to write implementation code.
2. Do not use the old `java-project-driven` / `pd` workflow.
3. Do not require tests as a learning artifact.
4. Do not bypass Teaching Slice explanations, even in `--auto`.
5. Keep the planned Teaching Slice order stable; adaptive behavior may change delivery style, never order.

For details on evidence policy, state writes, recommendation shape, slice templates, mastery reporting, and adaptive controls, follow the owning packet. `SKILL.md` must not redefine those rules.

## Paths

Resolve before use:

| Variable | Meaning | Resolution |
|---|---|---|
| `{workspace}` | Learning workspace root | Current working directory unless user explicitly provides another workspace |
| `{catalog_text}` | Human-readable Java catalog | `{workspace}/java-catalog.md` |
| `{corpus}` | Java reading corpus | `{workspace}/java-reading-corpus` |
| `{training_map}` | Catalog-to-corpus training map | `{corpus}/_shared/catalog-training-map.yaml` |
| `{recommendation_index}` | Generated recommendation index | `{corpus}/_derived/recommendation-index.yaml` |
| `{coverage_matrix}` | Generated coverage matrix | `{corpus}/_derived/coverage-matrix.yaml` |
| `{validation_ledger}` | Generated validation ledger | `{corpus}/_derived/validation-ledger.yaml` |
| `{node_extension_protocol}` | Corpus node authoring standard | `{corpus}/_shared/node-authoring-standard.md` |
| `{progress_state}` | Machine-readable progress state | `{workspace}/progress-state.yaml` |
| `{progress_summary}` | Human-readable progress summary | `{workspace}/progress.md` |
| `{adaptive_training_data}` | Perceived-difficulty ask data | `{workspace}/adaptive-training-data.yaml` |

When a command requires `{catalog_text}`, if `{catalog_text}` does not exist, stop that command and tell the user the workspace must contain `java-catalog.md`. Do not block progress-only commands on catalog availability unless the command explicitly needs catalog data for the requested output; follow `runtime-control.md` failure priority.

## Experience Contract

Every new reading project uses this restrained contract:

- `entry_mode`: prefer credible incident evidence grounded in the selected corpus candidate; fall back to design-document rather than inventing an unsupported incident.
- Stable Teaching Slice order: the learner's first curiosity can set `progress.current_investigation_focus` and affect emphasis, but it does not reorder implementation slices.
- Zero-friction continuation: each Slice Completion ends on the next slice's clue, not on a mechanical "say continue" instruction. In `guided` mode, a natural reply opens the next Slice Gate; implementation still requires the gate's fresh confirmation.
- Equipment unlock: every slice produces one reusable review/debug/design tool with a concrete use sentence and transfer contexts. Persist equipment in `{progress_state}`.
- Adaptive difficulty: use ask data, post-project assessment, and weakpoints to keep explanations slightly above the learner's current comfort level without changing project order or evidence rules.
- Double demo: failure-boundary projects should include `demo-naive` and `demo` when the selected FM can support a credible contrast.
- Post-project assessment remains the only required active assessment after the runnable project and demo are complete.

## Quick Reference

One-line index of every command. Full Execution Checklists live in `## Command Router` below.

| Command | Purpose | Writes state? |
|---|---|---|
| `jr ask <node-id>` | Collect perceived-difficulty ratings for adaptive delivery | yes — `{adaptive_training_data}` and `{progress_state}.adaptive_summary` |
| `jr start <node-id> [--s\|--m\|--b] [--auto] [--follow\|--micro-follow]` | Recommend and start one corpus-backed reading project | yes — only after user approves the recommendation |
| `jr resume` | Continue the active incomplete reading project | yes — only after user confirms the resume point |
| `jr pause` | Mark the active project as paused without losing context | yes — `{progress_state}.progress.status` only |
| `jr progress <node-id>` | Report node mastery and evidence state | no |
| `jr weak` | Report weakpoints, FM gaps, and next-project bias | no |
| `jr status` | Report current active context | no |
| `jr extend-node <node-id>` | Extend corpus for an unmapped catalog node | yes — only after user approves the extension plan |

Defaults: `size=--s`, `teaching_mode=guided`, `build_mode=normal`. Read-only commands never write progress files (except explicit legacy migration). Every state-writing command must complete its referenced preconditions before any write.

## Command Router

Each command below has an **Execution Checklist** — a numbered sequence the harness can follow step by step. Each step names the reference section that owns its rule. Steps marked with `[validator]` invoke `python java-reading-project/scripts/validate-progress.py`.

### `jr ask <node-id>`

Create or update perceived-difficulty ask data for one catalog node. This command does not start a project and does not assess mastery. Ask data is bounded by `evidence-policy.md §`jr ask` Boundary`.

**Execution Checklist:**

1. Resolve `{progress_state}`, `{progress_summary}`, `{adaptive_training_data}` (see `runtime-control.md §Workspace Progress Files`).
2. Verify `{catalog_text}` exists; otherwise stop with failure priority 1 (`runtime-control.md §Failure Priority`).
3. Read `{adaptive_training_data}`; classify session mode (`initial` / `follow_up` / `incremental`) per `adaptive-difficulty.md §Ask Session Modes`.
4. Build prompt candidates from corpus boundaries and FM groups (`adaptive-difficulty.md §Ask Prompt Sources`); pin `model_predicted_rating` before showing each prompt.
5. Ask each prompt; accept `1|2|3|easy|normal|hard|简单|正常|困难`; honor stop words (`停止|够了|pause|stop`).
6. Apply stop criteria (`adaptive-difficulty.md §Stop Criteria`); never push past the cap.
7. Write new samples and recompute the profile (`adaptive-difficulty.md §Profile Computation`).
8. Persist to `{adaptive_training_data}`, then refresh `{progress_state}.adaptive_summary.{node_id}` (`runtime-control.md §State Write Rules`).
9. [validator] `python java-reading-project/scripts/validate-progress.py --adaptive {adaptive_training_data}` — fail-loud if the new file does not validate.
10. Regenerate `{progress_summary}` from `{progress_state}` and report session mode, samples added, confidence band, hardest boundaries/FM, and next-project controls.

### `jr start <node-id> --s|--m|--b [--auto] [--follow|--micro-follow]`

Start a reading project only when no active incomplete project exists. Default size is `--s`; default teaching mode is `guided`; default build mode is `normal`. `--auto` maps to `teaching_mode: auto`; `--follow` maps to `build_mode: follow`; `--micro-follow` maps to `build_mode: micro-follow`.

**Execution Checklist:**

1. Resolve `{progress_state}`, `{progress_summary}`, `{catalog_text}` (`runtime-control.md §Workspace Progress Files`).
2. Read-only parse: load `{progress_state}` if present; otherwise read-only parse legacy YAML from `{progress_summary}` (`runtime-control.md §Legacy Migration`). **Write nothing yet.**
3. Active-project preflight: if `progress.status ∈ {selected|building|assessment_pending|paused}` and `progress.current_project` is set, stop immediately with the template in `runtime-control.md §Active State Rules`. Zero file writes.
4. Verify `{catalog_text}` exists and the node is in `catalog-training-map.yaml`. If unmapped, switch to `jr extend-node` flow (`start-project.md §Unmapped Node Extension`).
5. Compute adaptive level/controls (`adaptive-difficulty.md §Applying To `jr start``) and select **exactly one** corpus-backed candidate by ranking + anti-repetition + equipment-callback matching (`start-project.md §Corpus Candidate Ranking`).
6. Produce the recommendation as YAML (data layer) per `start-project.md §Recommendation Format` plus a short Chinese display block.
7. [validator] When the recommendation YAML is staged to a temp file before display, run `python java-reading-project/scripts/validate-progress.py --recommendation /tmp/rec.yaml` first and abort on failure.
8. Wait for user approval. Do not write progress files yet.
9. On approval: initialize `{progress_state}` if missing; set active project fields (`runtime-control.md §Active Project Fields`); set `progress.status: selected`; regenerate `{progress_summary}`.
10. Load `build-project.md`; show `incident_packet` or `design-document` fallback; capture optional `current_investigation_focus`.
11. For each Teaching Slice: emit Slice Gate → wait for fresh confirmation in `guided` mode → implement → emit Slice Completion (`build-project.md §Slice Gate Template`, `§Slice Completion Template`, `§Code Follow Blocks`).
12. After build/demo: set `progress.status: assessment_pending`; run post-project assessment (`build-project.md §Post-Project Assessment Contract`); assemble `progress_update`; [validator] `python java-reading-project/scripts/validate-progress.py --progress-update -` (stdin); merge into `{progress_state}` and regenerate `{progress_summary}`.

Initial acknowledgement (after step 1, before step 5):

```text
已识别节点：{node_id} {node_title}
项目规模：{size}
教学模式：{teaching_mode}
构建模式：{build_mode}
入口模式：优先 incident-first；corpus 不支持可信事故时使用 design-document fallback
工作区：{workspace}
我会基于 training map、progress evidence、已有装备、adaptive profile 和 recommendation index，只推荐 1 个最适合当前训练靶心、能从事故现场切入、并且能拆成 Teaching Slices 的 corpus-backed 可运行项目。
```

### `jr resume`

Continue an active incomplete project. Do not regenerate a recommendation, recreate completed slices, overwrite existing teaching evidence, or duplicate explanations already recorded as complete.

**Execution Checklist:**

1. Resolve `{progress_state}` and `{progress_summary}` (`runtime-control.md §Workspace Progress Files`).
2. Read `{progress_state}` (read-only legacy parse from `{progress_summary}` if missing). Refuse to write yet.
3. Verify `progress.status ∈ {selected|building|assessment_pending|paused}` and `progress.current_project` is set; otherwise report nothing to resume.
4. Read active project artifacts: `PLAN.md`, `TASKS.md`, `TEACHING_LOG.md`, optional `READING_GUIDE.md` / `REVIEW.md` (`runtime-control.md §Pause And Resume`).
5. Build `resume_input` YAML with current milestone/slice/follow-block/adaptive controls (`runtime-control.md §Pause And Resume`).
6. Render the learner-facing resume context block: 上回剧情回顾 / 悬念 / 回来以后先看 / 上次解锁的装备 (`build-project.md §Resume Learner-Facing Context`).
7. Wait for confirmation before editing any file.
8. Resume builder at the current incomplete slice or post-project assessment per status. Do not recreate completed slices.
9. Continue from step 11 of `jr start`'s checklist (Slice Gate / implementation / Slice Completion) or from §Post-Project Assessment Contract if `status: assessment_pending`.
10. [validator] After final progress merge: `python java-reading-project/scripts/validate-progress.py --state {progress_state} --policy`.

### `jr progress <node-id>`

Report node-level progress and evidence state. Use `assessment-progress.md` and `evidence-policy.md`. Do not call generator or builder.

**Execution Checklist:**

1. Resolve `{progress_state}`, optional `{adaptive_training_data}`.
2. Read `{progress_state}` (legacy parse from `{progress_summary}` if missing).
3. Locate completed projects for `<node-id>`; compute boundary coverage vs `mastery_policy.senior_ready_requires.required_boundaries` (`assessment-progress.md §Boundary Coverage`).
4. Score weakpoint health, project practice, user-interaction evidence, transfer evidence per `assessment-progress.md §Dimension Details`, gated by `evidence-policy.md`.
5. Pick status from `learning | reading_completed_assessment_pending | needs_drill | ready_for_mix | mastered` (`assessment-progress.md §Status Values`).
6. Report mastery qualitatively only — never a precise percentage or numeric range (`evidence-policy.md §Mastery Is Qualitative`).
7. Render the report per `assessment-progress.md §`jr progress <node-id>` Report Format`.
8. Recommend the next command (single drill, ready for mix, or next node).

### `jr weak`

Summarize node-specific weakpoints, global recurring weakpoints, adaptive hard spots, unresolved FM IDs, evidence refs, and how they bias future project generation. Do not call generator or builder.

**Execution Checklist:**

1. Read `{progress_state}` (`progress-shapes.md` — `weakpoints` and `next_project_bias`).
2. Read `{progress_state}.adaptive_summary` for adaptive hard spots when present.
3. Group weakpoints by `node_id`; surface unresolved core FM IDs.
4. Pull `evidence_refs` from `TEACHING_LOG.md` / `REVIEW.md` for each weakpoint (`assessment-progress.md §`jr weak``).
5. Gate every claimed weakpoint by `evidence-policy.md §User Questions And Volunteered Explanations`.
6. Explain how each weakpoint biases future project generation (drill vs mix, remediation shape).
7. Recommend the single most useful next command.

### `jr status`

Report current active context. Read-only, no generator/builder.

**Execution Checklist:**

1. Read `{progress_state}`; read-only legacy parse from `{progress_summary}` if missing.
2. If `progress.status = idle`, report `idle` plus the most recent completed project (if any). Stop.
3. Read active project artifacts only if they exist: `PLAN.md`, `TEACHING_LOG.md` (latest checkpoint), `READING_GUIDE.md`.
4. Render: node, project, size, milestone, slice, follow-block, teaching/build/entry mode, status, investigation focus, adaptive level/profile, latest reading checkpoint, recent weakpoints, recently unlocked equipment.
5. Recommend the next command (`jr resume` / `jr progress` / `jr start` / `jr ask`).
6. Do not write any file.
7. [validator] When the user reports state inconsistency, run `python java-reading-project/scripts/validate-progress.py --state {progress_state} --policy` before answering and surface any failure to the user.

### `jr pause`

Mark the current active project as paused without modifying project code, `TEACHING_LOG.md`, corpus resources, or generated corpus indexes.

**Execution Checklist:**

1. Read `{progress_state}`.
2. If no active incomplete project, report "nothing to pause" and write nothing.
3. Preserve current node/project/size/milestone/slice/entry-mode/investigation-focus/adaptive/teaching-mode/build-mode/follow-block.
4. Set `progress.status: paused`, `progress.paused_at: <now>`, `progress.pause_reason: user_requested` (`runtime-control.md §Pause And Resume`).
5. Write `{progress_state}` only; regenerate `{progress_summary}`. **Do not touch** project code, `TEACHING_LOG.md`, corpus, or generated indexes.
6. [validator] `python java-reading-project/scripts/validate-progress.py --state {progress_state}` to confirm the pause write is well-formed.
7. Reply: `已暂停当前阅读项目。下次可用 jr resume 从当前 Teaching Slice 继续。`

### `jr extend-node <node-id>`

Use `start-project.md`. Find the node in `{catalog_text}`. If it does not exist, stop and say the catalog node was not found.

**Execution Checklist:**

1. Resolve `{catalog_text}` and the corpus directory.
2. Verify the node exists in `{catalog_text}`; otherwise stop.
3. Read `_shared/node-authoring-standard.md`, `_shared/catalog-training-map.yaml`, `_shared/concept-atlas.yaml`, `_shared/failure-mode-codex.yaml`, and `_derived/recommendation-index.yaml` (`start-project.md §Unmapped Node Extension`).
4. Extract training intent; list every declared concept and map concept → boundary → FM. Any untrainable concept needs a new boundary + FM category, per the standard's Quality Bar.
5. Classify extension type: `map-only` / `seed-extension` / `boundary-extension`.
6. Show the authoring plan (boundaries, ≥3 de-homogenized seeds per primary boundary, incident packets, tiered depth) and **wait for explicit user approval**. Write nothing yet.
7. On approval, author corpus resources to the gold Quality Bar (not generated `_derived` files).
8. Run the full gate in order: `validate-corpus.py`, `check-coverage.py`, `build-index.py`, then `lint-quality.py --node <node-id>` (`start-project.md §Unmapped Node Extension`).
9. If any check fails, fix authored files; never patch generated files to hide failures. Do not publish until `lint-quality.py` passes.
10. Publish the map entry with `quality_status: gold` and report the new mapping plus a hint to re-run `jr start <node-id>`.

## User Interaction

- Natural confirmation and zero-friction reply keywords are owned by `runtime-control.md §Teaching And Build Mode Matrix`. Do not maintain a parallel list here.
- Ask for input only at recommendation approval, adjustment, incident orientation, `jr ask` perceived-difficulty ratings, pause/resume ambiguity, Teaching Slice gates in `guided` mode, Code Follow Blocks in `guided + follow|micro-follow`, explicit abandon/reset confirmation, or post-project assessment.
- If the user asks a design question, answer before proceeding.

# Adaptive Difficulty Reference

## Mission

Ask and apply perceived difficulty for Java Reading Project. The delivery layer adjusts explanation density, clue exposure, JDK8 bridge notes, equipment callback directness, and post-project assessment follow-up depth. Adaptive difficulty never proves mastery and never reorders Teaching Slices — see `evidence-policy.md` and `SKILL.md §Hard Boundaries`.

**Owned topics**: `jr ask` flow, perceived-difficulty rating scale, ask session modes (`initial` / `follow_up` / `incremental`), `adaptive-training-data.yaml` shape, `prompt_id` format and uniqueness, profile computation (user rating, model prediction error, confidence, current level), the five adaptive controls and their three-level behavior table, application to `jr start` and during build.

**Cross-references**: what ask data can and cannot become → `evidence-policy.md §`jr ask` Boundary`; where the adaptive level/controls live in workspace state → `progress-shapes.md` (`adaptive_summary`); slice-level adaptive application (Slice Gate / Slice Completion / Code Follow Block) → `build-project.md`.

## Evidence Policy Source

For mastery, transfer, equipment, ask-data, passive-reading, build/demo, and qualitative-mastery-reporting rules, follow `evidence-policy.md`. This file describes local adaptive mechanics; it does not redefine what counts as mastery evidence.

## Files

Use two layers:

| Variable | Path | Role |
|---|---|---|
| `{adaptive_training_data}` | `{workspace}/adaptive-training-data.yaml` | Detailed perceived-difficulty ask data records. |
| `{progress_state}.adaptive_summary` | `{workspace}/progress-state.yaml` | Lightweight profile summary for command routing and status output. |

Do not store detailed ask prompt text in `progress-state.yaml`.

## Commands

### `jr ask <node-id>`

Purpose: learn the learner's perceived difficulty for mapped node boundaries and corpus failure modes.

Rules:

- Ask the learner only for perceived difficulty.
- The learner does not answer the Java/backend question.
- Use exactly this scale:

```text
1 = easy
2 = normal
3 = hard
```

- Accept `1`, `2`, `3`, `easy`, `normal`, `hard`, `简单`, `正常`, `困难`.
- Stop immediately if the learner says `停止`, `够了`, `pause`, or `stop`.
- Ask data is bounded by `evidence-policy.md §`jr ask` Boundary` — it never becomes mastery, weakpoint, or transfer evidence by itself.
- Ask flow must not shame the learner or describe a score as ability.
- Ask flow must not generate or modify project files.

## Ask Prompt Sources

Build prompt candidates from mapped corpus data:

- required boundaries in `catalog-training-map.yaml`
- core FM IDs in the node map
- unresolved weakpoints from `progress-state.yaml`
- corpus seed/cross scenario failure modes
- code snippets, bad-design alternatives, incident fragments, enum/status classification, cause-chain examples, collection/API choices
- JDK8-to-modern-Java hotspots likely to affect reading difficulty

Each ask prompt should be short enough to rate in under 20 seconds.

## Ask Session Modes

Before selecting prompts, classify the `jr ask <node-id>` session:

- `initial`: `{adaptive_training_data}.nodes.{node_id}` is missing, or `profile.sample_count < 5`.
- `follow_up`: `profile.sample_count >= 5` and `profile.asked_at` is more than 7 days old, or the learner explicitly asks to re-evaluate with phrases such as `重新评估`, `重测`, `再测一次`, or `refresh`.
- `incremental`: `profile.sample_count >= 5` and `profile.asked_at` is 7 days old or newer.

Mode effects:

- `initial`: broad coverage; cap at 15 prompts.
- `follow_up`: refresh stale profile; cap at 8 prompts and prioritize changed weakpoints, stale hard boundaries, and new corpus coverage.
- `incremental`: add samples to the existing pool; cap at 8 prompts and prioritize low-confidence boundary/FM gaps.

Do not discard old samples unless the learner explicitly asks to reset the ask data. A re-evaluation updates the profile using newer samples with higher weight.

Do not ask for a solution. Good prompt shapes:

````markdown
### Ask <n>

节点：`1.1`
边界：`B-lang-exception`
类型：`bad-design`

场景：
支付 SDK 抛出 `SocketTimeoutException`，业务代码只写：

```java
throw new RuntimeException("gateway error");
```

如果我在项目里围绕这段代码讲“为什么 cause chain 不能丢”，你觉得难度是？

`1 = easy / 2 = normal / 3 = hard`
````

Bad prompt shapes:

- “请解释为什么这里要保留 cause。”
- “这段代码哪里错？”
- “你会怎么设计？”
- “答对说明掌握。”

## Data Shape

The shape below is machine-checked by:

```bash
uv run python java-reading-project/scripts/validate-progress.py --adaptive {workspace}/adaptive-training-data.yaml
```

The validator enforces field presence, enum values, `prompt_id` format, per-node `prompt_id` uniqueness, and `delta == user_rating - model_predicted_rating`. Run it after every `jr ask` write.

If `{adaptive_training_data}` is missing, create:

```yaml
version: 1
nodes: {}
```

Node shape:

```yaml
nodes:
  "1.1":
    profile:
      asked_at: "2026-05-26T21:30:00+08:00"
      sample_count: 0
      confidence: 0.0
      target_rating: 2.3
      current_level: "standard"
      strongest_boundaries: []
      hardest_boundaries: []
      hardest_fm: []
      preferred_controls:
        explanation_density: "standard"
        clue_exposure: "balanced"
        jdk8_bridge: "standard"
        equipment_callback: "hinted"
        assessment_followup_depth: "standard"
    samples: []
```

Sample shape:

```yaml
samples:
  - prompt_id: "1.1/B-lang-exception/FM-lost-cause/bad-design/20260526T213000Z-a1b2c3"
    node_id: "1.1"
    boundary_id: "B-lang-exception"
    fm_id: "FM-lost-cause"
    prompt_type: "code-snippet|incident|concept|bad-design|syntax-bridge|classification"
    prompt_summary: "RuntimeException wrapper loses SocketTimeoutException cause"
    source_refs:
      - "java-reading-corpus/scenarios/B-lang-exception/seed-payment-gateway-errors.yaml"
    model_predicted_rating: 2
    user_rating: 3
    delta: 1
    created_at: "2026-05-26T21:30:00+08:00"
```

`prompt_summary` must be concise. Do not store long prompt prose when a source ref and summary are enough.

### Prompt ID Rules

`prompt_id` is opaque but must be unique within `{adaptive_training_data}`.

Generate it as:

```text
{node_id}/{boundary_id_or_none}/{fm_id_or_none}/{prompt_type}/{timestamp}-{shortid}
```

Rules:

- `timestamp` uses UTC basic format such as `20260526T213000Z`.
- `shortid` is a short stable random or content hash suffix, 6-10 lowercase alphanumeric characters.
- Before writing a sample, check existing samples for the node. If a generated `prompt_id` already exists, regenerate the suffix.
- Do not use simple counters like `001`; they drift or collide across sessions.

## Stop Criteria

Stop ask flow when any of these is true:

- learner explicitly stops
- `initial` ask flow reaches 15 prompts
- `follow_up` or `incremental` ask flow reaches 8 prompts
- every required boundary has at least 2 samples and every core FM group has at least 1 sample
- the last 6 samples have mean absolute prediction error `<= 0.45` and the node profile confidence is `>= 0.70`

If confidence remains low after the prompt cap, stop anyway and mark the profile as low confidence. Do not keep asking.

## Profile Computation

Use simple, explainable rules. Do not invent complex psychometrics.

### User Rating

Treat ratings as perceived difficulty:

- `1`: likely comfortable; reduce hand-holding unless assessment says otherwise
- `2`: target zone; keep normal explanation
- `3`: challenging; add bridge/context, lower clue opacity, and avoid stacking multiple new ideas at once

### Model Prediction Error

For each sample:

```text
delta = user_rating - model_predicted_rating
absolute_error = abs(delta)
```

Use recent samples more than old samples. If exact computation is not practical, summarize qualitatively:

- `stable`: recent ratings match predictions
- `overestimated`: AI thought harder than learner felt
- `underestimated`: learner felt harder than AI expected

### Model Prediction Rules

`model_predicted_rating` must be fixed before showing the prompt to the learner. Do not choose or revise it after seeing `user_rating`.

For the first prompt in a session:

1. Read `progress-state.yaml.adaptive_summary.{node_id}` if present.
2. Predict from `current_level`:
   - `supportive` -> `3`
   - `standard` -> `2`
   - `stretch` -> `1`
3. If no profile exists, use `model_predicted_rating: 2`.

For later prompts in the same session:

1. Start with the recency-weighted running mean of `user_rating` from this session.
2. Adjust by profile:
   - if the prompt boundary is in `hardest_boundaries`, add `0.5`
   - if the prompt boundary is in `strongest_boundaries`, subtract `0.5`
   - if the prompt FM is in `hardest_fm`, add `0.5`
3. Clamp the result to `[1, 3]`.
4. Round to nearest `1|2|3`; ties round toward `2`.

Record the chosen `model_predicted_rating` in memory before displaying the prompt, then write it with the sample after the learner responds.

### Confidence

Estimate confidence from:

- sample coverage across required boundaries
- sample coverage across core FM groups
- recent prediction error
- consistency of ratings inside the same boundary/FM
- recency of ask data

Use these bands:

```text
0.00-0.39 = low
0.40-0.69 = medium
0.70-1.00 = high
```

Do not display confidence as a learner ability score.

### Current Level

Map profile to one of:

```text
supportive
standard
stretch
```

Use:

- `supportive`: many `3=hard` ratings, low confidence, or unresolved weakpoints near current project boundary
- `standard`: most ratings around `2=normal`
- `stretch`: many `1=easy` ratings plus completed assessment evidence and few open weakpoints

Do not set `stretch` from ask data alone if post-project assessment evidence is weak or missing.

## Difficulty Controls

Adaptive difficulty can adjust only these controls:

| Control | `supportive` | `standard` | `stretch` |
|---|---|---|---|
| `explanation_density` | More context, fewer jumps, one concept at a time. | Normal slice explanation. | Shorter setup, more code evidence. |
| `clue_exposure` | Give the conclusion first, ask learner to trace evidence. | Show clue, then explain. | Show clue first and pause for hypothesis. |
| `jdk8_bridge` | Add more JDK8-to-modern Java bridge notes. | Add bridge only at hotspots. | Keep bridge brief unless asked. |
| `equipment_callback` | State how prior equipment applies. | Hint that equipment may apply. | Ask whether prior equipment applies before revealing. |
| `assessment_followup_depth` | Fewer prompts, more scaffolding. | Standard 4-6 prompts. | Add one deeper transfer or bad-design follow-up. |

Hard limits:

- Do not skip required Teaching Slice explanations.
- Do not remove post-project assessment.
- Slice order is fixed — see `SKILL.md §Hard Boundaries`.
- Ask-data evidence boundary is owned by `evidence-policy.md §`jr ask` Boundary`.
- Do not make the project feel like a test during construction.
- Do not ask repeated ask prompts during normal project flow unless the user explicitly invokes `jr ask`.

## Applying To `jr start`

When starting a project:

1. Read adaptive profile for the node if present.
2. Read post-project assessment evidence and weakpoints.
3. Choose `current_level` conservatively:
   - weak assessment or open core FM can lower to `supportive`
   - strong assessment plus ask comfort can raise to `stretch`
   - no data defaults to `standard`
4. Include `adaptive_plan` in the recommendation:

```markdown
- **adaptive_plan**:
  - current_level: `supportive|standard|stretch`
  - basis: ask data / assessment / weakpoints
  - controls: explanation_density, clue_exposure, jdk8_bridge, equipment_callback, assessment_followup_depth
```

5. Write active project difficulty fields to progress when the project is approved.

## Applying To `jr ask` Completion

When a `jr ask <node-id>` session ends:

1. Write all new samples and the updated node profile to `{adaptive_training_data}`.
2. Write or refresh `{progress_state}.adaptive_summary.{node_id}` from the node profile.
3. Regenerate `{progress_summary}` from `{progress_state}`.
4. Tell the learner:
   - session mode: `initial|follow_up|incremental`
   - sample count added
   - confidence band
   - hardest boundaries/FM
   - next project controls

If writing `{adaptive_training_data}` fails, do not update `adaptive_summary`. The progress summary must not claim ask data that was not saved.

## Applying During Build

Builder and Teaching Slices use the active adaptive controls:

- Slice Gate: adjust setup length and bridge notes.
- Code Follow: choose `follow` granularity only from `build_mode`; adaptive can affect explanation text, not apply patches without confirmation.
- Slice Completion: adjust how much of the next clue is revealed.
- Equipment callback: decide direct reveal vs hint vs challenge.
- Post-project assessment: adjust follow-up depth while preserving required assessment areas.

## Progress Summary

`jr status`, `jr weak`, and `jr progress <node-id>` may show:

```markdown
Adaptive difficulty:
- level: `standard`
- confidence: `medium`
- hardest boundary: `B-lang-exception`
- next project controls: explanation_density=`standard`, clue_exposure=`balanced`
```

Keep it short. Do not display raw ask prompt history unless the user asks.

## Anti-Patterns

- Asking the learner to solve ask prompts.
- Calling ask data an exam, score, grade, level, or mastery proof.
- Continuing ask flow after the learner says stop.
- Using ask data to avoid post-project assessment or to create mastery evidence against `evidence-policy.md`.
- Reordering slices or changing project architecture based on difficulty.
- Storing long ask prompt prose in `progress-state.yaml`.
- Treating “easy” ratings as proof that the learner can transfer the concept.

# File Formats

## Purpose

Use these templates when creating or updating workspace files for a learning instance.

## `knowledge-map.md`

```md
# Knowledge Map: {Domain}

## Metadata
- Type: {A|B|C|D|E}
- Default Depth: {L1|L2|L3}
- Active Phase: {P1}

## Phase Overview
| Phase | Name | Core Question | Prerequisites | Status |
|---|---|---|---|---|
| P1 | ... | ... | ... | Active |

## Prerequisite Graph
{simple graph or ordered list}

## Bridge Graph
| This Phase | Connects To | Note |
|---|---|---|
| ... | ... | ... |
```

## `phases/phase-{NN}-{slug}.md`

```md
# Phase {NN}: {Name}

## Core Question
{question}

## Concept Pool
- {concept}: {brief summary} `[M1][light|medium|heavy]`

## Milestones
- `M1`: {what the learner must be able to do}

## Iteration History
| Date | Change | Trigger |
|---|---|---|
| ... | ... | ... |
```

## `progress.md`

```md
# Progress

## Current Focus
- Domain: {name}
- Phase: {P1}
- Target Depth: {L1|L2|L3}

## Concept Tracking
| Concept | Phase | L1 | L2 | L3 | Gaps | Notes |
|---|---|---|---|---|---|---|
| ... | ... | ⬜ | ⬜ | ⬜ | 0 | ... |

## Next Step
- {explicit next resume point}
```

## `session-log.md`

```md
# Session Log

| Date | Mode | Concepts | Reached Layer | Exposed Gap | Next Resume | Transcript |
|---|---|---|---|---|---|---|
| ... | teach | ... | L2 | ... | ... | ... |
```

## `drill-log.md`

```md
# Drill Log

| Date | Concept | Exercise Type | Difficulty | Result | Mastery Move | Return To Teach |
|---|---|---|---|---|---|---|
| ... | ... | Debug | medium | ... | +1 | no |
```

## `proposals.md`

```md
# Proposals

## Curriculum Proposal: {title}
- Status: proposed
- Evidence: {transcript or audit note}
- Proposed Change: {specific change}
- User Decision: {pending}

## Skill Proposal: {title}
- Status: proposed
- Evidence: {transcript or audit note}
- Proposed Change: {specific change}
- User Decision: {pending}
```

## Transcript Naming

Use a stable pattern such as:

```text
{workspace}/logs/java-mastery-codex-{topic}-{YYYY-MM-DD}.md
{workspace}/logs/generic-mastery-codex-{topic}-{YYYY-MM-DD}.md
```

Rules:

- `{topic}` should be the current learning topic, not the broad domain name
- if a same-topic same-date filename already exists, append a session-id suffix to avoid collisions
- `session-log.md` should record the exact transcript filename used for that topic
- `{workspace}` is the current Codex working directory for the active learning instance

## Sync Rules

- concept additions or removals in a phase file must synchronize into `progress.md`
- teach updates `progress.md`, `session-log.md`, and `proposals.md`
- drill updates `drill-log.md`, `progress.md`, and `session-log.md`
- ask updates `session-log.md`, and updates `progress.md` only for real gaps or state corrections
- teach audit reads only the transcript linked to the current topic, not unrelated topic logs

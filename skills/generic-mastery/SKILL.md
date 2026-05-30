---
name: generic-mastery
description: Use when teaching or deeply learning non-tool domains across sessions, especially when the work needs stable curriculum structure, explicit depth control with --deep=L1|L2|L3, transcript-based teaching audits, bounded ask mode, and deliberate drill mode.
---

# Generic Mastery

## Overview

Generic Mastery is a depth-first learning skill for non-tool domains. It teaches with a three-layer model, keeps durable cross-session state, and treats transcript-based audit plus user-approved evolution as mandatory parts of teaching.

This skill is dual-mode:

- It can directly teach a domain such as Python, Spring, Linux, or TDD.
- It can also act as a parent framework for future domain-specific mastery skills.

Tool-centric domains are no longer taught here. If domain inference lands on `Type C`, route the learner to `tool-mastery` instead of bootstrapping this skill.

## Iron Law

Formal teaching is not complete when the explanation ends. It is complete only after:

1. state is updated
2. transcript-backed audit is done
3. anti-patterns are checked
4. proposals are written
5. the user has seen the proposals

No transcript evidence means no full-quality audit loop.

## Output Language Policy

Default output language for all learner-facing and durable workspace documents is Simplified Chinese.

This applies to:

- teaching notes and explanations written into workspace files
- `knowledge-map.md`, phase files, `progress.md`, `session-log.md`, `drill-log.md`, and `proposals.md`
- transcript-backed audit summaries, proposal writebacks, drill records, and resume notes
- status/progress summaries shown to the user when the skill reports file-backed learning state

Keep the following in English when that preserves precision or matches normal developer usage:

- code, commands, APIs, protocol names, config keys, error messages, and file names
- core technical terms such as `Mechanism`, `Design`, `Engineering`, `hook`, `token`, and language/library names

Do not change existing file paths or naming conventions just to localize them. Localize the document content, headings, explanations, and action items instead.

## When To Use

Use this skill when:

- the user wants to learn a domain across sessions
- ad-hoc answers are no longer enough
- depth needs to be explicit, not implied
- the course needs durable files instead of model memory
- teaching quality must be audited from transcript evidence

Do not use this skill for:

- one-off explanations with no durable learning goal
- lightweight Q&A where no curriculum or audit loop is needed
- environments where transcript evidence cannot be recorded
- tool-centric domains such as IDEs, editors, local developer tools, workflow tools, or environment-integration tools; use `tool-mastery`

## Layer Model

- `Mechanism (规则层)`: what it is, how it works, what the operating rules are
- `Design (设计层)`: why this design exists, what alternatives were rejected, what trade-offs matter
- `Engineering (决策层)`: when it matters in real work, what the cost is, and how to decide under constraints

`--deep=L1|L2|L3` sets the required completion ceiling:

- `L1`: Mechanism only
- `L2`: Mechanism + Design
- `L3`: Mechanism + Design + Engineering

Rules:

- lower layers must be stable before higher layers count
- higher-layer questions do not justify skipping lower layers
- completion means completion up to the current `--deep` target, not beyond it

## Modes

### Teach

Use for structured progression.

Flow:

1. Read `knowledge-map.md`, current phase file, `progress.md`, and `session-log.md`.
2. Resolve current phase, current concept, current `--deep`, and prerequisites.
3. Teach layer-by-layer with `Teach -> Verify -> Correct`.
4. When the teaching session is explicitly ending, update `progress.md` and `session-log.md`.
5. When the teaching session is explicitly ending, read transcript evidence and run one audit for the whole session.
6. When the teaching session is explicitly ending, write proposals to `proposals.md`.
7. When the teaching session is explicitly ending, discuss proposals with the user.
8. Apply no curriculum or rule changes unless the user approves.

Session boundary rule:

- `Teach -> Verify -> Correct` happens inside the live teaching session
- `audit`, anti-pattern scan, and `proposals.md` writeback happen once at session closeout, not after each concept
- do not open a new audit/proposal loop just because one concept, one question, or one correction step finished

Learner-facing boundary rule:

- during teaching, keep the user-facing dialogue focused on the knowledge, questions, corrections, and summary
- do not narrate routine file writes, transcript writes, state sync, or background bookkeeping unless the user explicitly asks
- mention files only when the user asks for state visibility, or when approval is required for curriculum/rule changes

Audit scope rule:

- read only the transcript file for the current topic, or topic-matched transcript files if the session was split
- do not scan unrelated `generic-mastery` or `java-mastery` topics during a teach audit

### Ask

Use for bounded reactive questions.

Rules:

- answer through the layer model instead of flat FAQ
- do not silently turn `ask` into the main curriculum path
- do not normally mark formal completion
- update `session-log.md` by default
- update `progress.md` only when a real gap or state correction is exposed

Core principle:

**Ask success does not equal curriculum progress.**

### Drill

Use for deliberate practice after teaching, or for controlled calibration of prior knowledge.

Rules:

- drill is not hidden teaching
- untaught concepts require cold-start calibration first
- mastery cannot increase without evidence-backed scoring
- repeated instability routes back to `teach`

Read `references/drill-principles.md` whenever drill starts.

## Gates

### G0 Depth Gate

- max 2 new concepts per formal teach session
- do not move beyond current `--deep`

### G1 Layer Completion Gate

- required layers complete in order
- no high-layer completion on top of weak lower layers

### G2 Error Loop Gate

- wrong answer -> variant -> reteach current layer -> record gap
- hard cap: 3 rounds per stuck point

### G3 No Ghost Gate

- no interaction means not taught
- no learner evidence means no completion mark

### G4 State Integrity Gate

Use files, not model memory:

- progress from `progress.md`
- recent resume point from `session-log.md`
- practice evidence from `drill-log.md`
- course structure from `knowledge-map.md` and current phase file

### G5 Prerequisite Gate

- no new layer progress without prerequisite support

### G6 Scaffolding Gate

- never ask before the learner has enough information to form a hypothesis

### G7 Mode Boundary Gate

- `teach` advances structure
- `ask` resolves bounded questions
- `drill` compresses mastery
- only approved paths may mark formal completion

### G8 Evidence Gate

- audit must use transcript evidence
- `session-log.md` is a resume index, not audit evidence

### G9 Audit-to-Evolution Gate

- every formal `teach` ends with audit, anti-pattern scan, proposal writeback, and user-visible discussion
- these closeout steps run once per formal `teach` session, not once per concept inside the session

### G10 Learner-Facing Boundary Gate

- durable state files are required for the skill, but they are backend support by default
- do not leak routine file-maintenance details into the learner-facing teaching flow
- only surface file/state details when the learner asks for them, or when explicit approval is needed

## Domain Bootstrap

On first use for a new domain:

1. infer the domain type
2. if the inferred type is `C`, stop bootstrap and tell the user: `请使用 tool-mastery 学习`
3. otherwise show the inferred type and reason
4. read `references/domain-type-templates.md`
5. create full-route `knowledge-map.md`
6. create detailed `phase-01-{slug}.md`
7. create `progress.md`, `session-log.md`, `drill-log.md`, and `proposals.md`
8. begin teaching

Curriculum strategy:

- full-route rough planning for all phases
- detailed concept expansion for phase 1 only
- future phases expand near point of use

Read `references/knowledge-architecture.md` before bootstrap or curriculum restructuring.

## Runtime Loading Rules

Always read:

- `knowledge-map.md`
- current phase file
- `progress.md`
- `session-log.md`

Read on demand:

- `references/knowledge-architecture.md` for bootstrap and curriculum structure work
- `references/domain-type-templates.md` for domain inference and course generation
- `references/drill-principles.md` for drill
- `references/teaching-principles.md` for post-teach audit
- `references/anti-patterns.md` for post-teach scan
- `references/file-formats.md` when creating or updating workspace files
- relevant transcript files during audit or evidence conflicts
- for audits, prefer the transcript whose topic matches the current session topic and current `session-log.md` entry

Do not load all phase files by default.

## Workspace Contract

Workspace learning instances use:

- `{workspace}` = the current Codex working directory for this learning instance
- all durable state, generated files, and code write relative to `{workspace}`
- all durable document content written under `{workspace}` defaults to Simplified Chinese unless a term must remain in English for precision
- store transcript evidence under `{workspace}/logs/` with the `generic-mastery-codex-{topic}-{YYYY-MM-DD}.md` naming rule
- create `{workspace}/logs/` on demand when the first transcript is written
- do not redirect durable learning state to a separate global vault path

- `knowledge-map.md`
- `phases/phase-{NN}-{slug}.md`
- `progress.md`
- `session-log.md`
- `drill-log.md`
- `proposals.md`
- transcript evidence files from the teaching hook

Read `references/file-formats.md` for exact templates.

## Quick Reference

- New domain: infer type -> build `knowledge-map.md` -> build `phase-01` -> initialize state files -> teach
- New domain: infer type -> if `Type C`, route to `tool-mastery`; otherwise build `knowledge-map.md` -> build `phase-01` -> initialize state files -> teach
- Teach closeout: update state -> audit transcript -> scan anti-patterns -> write proposals -> discuss with user
- Teach closeout runs once when the session ends, not after each concept or correction turn
- Ask closeout: log the interaction -> record real gaps only
- Drill closeout: write drill evidence -> update mastery/gaps -> route back to `teach` if structure is missing

## Common Mistakes

- starting ad-hoc teaching without bootstrap
- letting `ask` replace curriculum progression
- treating drill as hidden teaching
- auditing from memory instead of transcript evidence
- marking completion from a nod, not from learner evidence
- silently mutating curriculum files without proposal approval
- running audit/proposal writeback in the middle of an unfinished `teach` session
- exposing routine file bookkeeping in the learner-facing teaching dialogue
- bootstrapping a tool-centric `Type C` domain here instead of routing it to `tool-mastery`

## Red Flags

Stop and correct course immediately if you catch yourself thinking:

- "I can structure the curriculum later."
- "This answer is good enough to count as progress."
- "Audit can wait until next time."
- "I can teach during drill just this once."
- "I remember what the learner covered already."

Each of these means the skill is drifting away from its contract.

## Rationalizations We Reject

| Rationalization | Required Response |
|---|---|
| "The user wants speed, so skip bootstrap." | Use the bootstrap flow anyway. Stable structure is part of the teaching quality, not optional overhead. |
| "This one-off answer basically taught the concept." | Keep it in `ask`; do not mark formal completion. |
| "The session was obviously fine." | Run transcript-based audit. No audit means no completed teach session. |
| "A little inline teaching inside drill is harmless." | Calibrate first, or route back to `teach` if structure is missing. |
| "I already remember the learner's state." | Re-read the state files and relevant transcript evidence. |

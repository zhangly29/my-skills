# Knowledge Architecture

## Purpose

Keep the curriculum stable across sessions without loading unnecessary detail.

The architecture is split into four layers:

- `Index Layer`: `knowledge-map.md`
- `Detail Layer`: `phases/phase-{NN}-{slug}.md`
- `State Layer`: `progress.md`, `session-log.md`, `drill-log.md`, `proposals.md`
- `Evidence Layer`: transcript files from the teaching hook

## Core Rule

Global route once, local detail on demand.

Bootstrap a new domain with:

1. full-route `knowledge-map.md`
2. detailed `phase-01`
3. initialized state files

Future phase detail is generated only near the point of use.

## Index Layer

`knowledge-map.md` stores:

- domain name
- inferred type
- default depth
- phase list
- core question per phase
- prerequisite graph
- bridge graph
- current active phase

It is a navigation map, not a full concept dump.

## Detail Layer

Each phase file stores:

- the phase core question
- concept pool for that phase
- brief concept summaries
- complexity tags
- milestone grouping
- verification intent
- iteration history

Runtime default:

- load only the current phase file
- do not load all phase files unless a cross-phase conflict requires it

## State Layer

Use the state files as follows:

- `progress.md`: source of truth for current learner state
- `session-log.md`: compact resume index
- `drill-log.md`: practice evidence
- `proposals.md`: approved and pending evolution work

State files track what actually happened. They do not redefine the curriculum.

## Evidence Layer

Transcript files are mandatory for full-quality operation.

Use them for:

- post-teach audit
- dispute resolution when memory conflicts with state
- evidence-backed proposal writing

Do not replace transcript evidence with `session-log.md`.

Topic-scope rule:

- a teach audit reads only transcript files for the current topic
- if multiple transcript files belong to the same topic, use only that topic's subset
- never widen the scan to unrelated mastery topics just because the skill prefix matches

## Curriculum Evolution

Curriculum files may change only through this sequence:

1. detect issue during teaching, audit, or repeated asks
2. write proposal to `proposals.md`
3. discuss with the user
4. apply only after approval
5. synchronize affected state files

No silent mutation.

## Load Budget

Always read:

- `knowledge-map.md`
- current phase file
- `progress.md`
- `session-log.md`

Read optionally:

- `drill-log.md` when mastery evidence matters
- `proposals.md` when evolution context matters
- transcript files during audit or conflict resolution

Avoid full-course loading by default.

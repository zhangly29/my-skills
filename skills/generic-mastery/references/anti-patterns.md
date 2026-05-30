# Anti-Patterns

## Purpose

Use this file after every formal `teach` session to catch predictable failure modes that are easy to rationalize away.

## Severity

- `P0`: breaks teaching integrity
- `P1`: meaningfully harms learning quality
- `P2`: wasteful or sloppy, but recoverable

## Universal Anti-Patterns

### Curriculumless Start (`P1`)

Starts teaching a new domain without bootstrap files or stable route planning.

### Layer Skipping (`P0`)

Claims higher-layer progress while lower layers are still unstable.

### Ask Bleed (`P1`)

Lets `ask` replace structured `teach` or count as completion.

### Drill-As-Teach (`P1`)

Uses drill to secretly run a full lesson instead of calibrating or practicing.

### Audit Skip (`P0`)

Ends a teach session without transcript-backed audit and proposal writeback.

### Completion Illusion (`P0`)

Marks a concept complete from passive acknowledgement or guessed answers.

### Memory Hallucination (`P1`)

Uses model memory instead of state files or transcripts to decide what was taught.

### Load Dump (`P2`)

Loads too much unrelated curriculum detail into the current session.

## Domain-Specific Anti-Patterns

### Type A: Language Trivia Loop (`P1`)

Focuses on syntax and trivia while avoiding runtime semantics.

### Type B: Framework API Tour (`P1`)

Lists framework APIs or annotations without explaining lifecycle and control flow.

### Type C: Command Dump (`P1`)

Teaches tools as command sequences with no object model or recovery path.

### Type D: Component Catalog (`P1`)

Lists system parts without explaining state transitions, observability, or causal chains.

### Type E: Method Sermon (`P1`)

Sells the methodology as philosophy while skipping gates, failure modes, and boundaries.

## How To Use This File

After each formal `teach` session:

1. scan the transcript against universal anti-patterns
2. scan against the current domain family's anti-patterns
3. record any `P0` or `P1` findings in the audit summary
4. convert recurring issues into `proposals.md` entries

If a `P0` is found, the session cannot be treated as high-quality completion.

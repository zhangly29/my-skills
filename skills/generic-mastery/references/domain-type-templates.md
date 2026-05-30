# Domain Type Templates

## Purpose

The same three-layer model applies to non-tool domains, but the curriculum and drill emphasis change by domain family.

## Type A: Programming Languages

Examples:

- Python
- Rust
- Go

Inference signals:

- the subject is a language runtime or language syntax
- users care about semantics, standard library, performance, memory, or concurrency

Curriculum bias:

- language rules and mental model first
- semantics before stylistic conventions
- design trade-offs behind language features
- performance, memory, and concurrency decisions at L3

Drill bias:

- `Prediction`
- `Debug`
- `Quantification`
- `Transfer`

Common anti-patterns:

- trivia-first teaching
- syntax without runtime model
- performance claims without thresholds

## Type B: Frameworks

Examples:

- Spring
- React
- FastAPI

Inference signals:

- the subject organizes application flow through conventions, lifecycle, or abstractions

Curriculum bias:

- problem the framework solves
- lifecycle and control flow
- abstractions and extension points
- when to align with the framework versus when it adds cost

Drill bias:

- `Design Critique`
- `Debug`
- `Counterexample`
- `Transfer`

Common anti-patterns:

- API tour without architecture
- hooks/components/annotations taught without lifecycle reasoning
- no explanation of why the framework pattern exists

## Type C: Tools / CLI

This type is delegated to `tool-mastery`.

Examples:

- Docker
- uv
- WSL

Inference signals:

- the subject is a command-line tool, workflow tool, or local developer utility
- the learner's main goal is practical use, efficiency, setup, plugins/extensions, or integration with a real stack/environment

Routing rule:

- if the inferred type is `C`, `generic-mastery` must stop bootstrap and tell the user: `请使用 tool-mastery 学习`
- `generic-mastery` must not generate `knowledge-map.md`, `phase-01`, or state files for this domain
- the curriculum shape, depth model, and verification style for these domains belong to `tool-mastery`, not to `generic-mastery`

## Type D: Systems

Examples:

- Kubernetes
- Linux
- distributed systems basics

Inference signals:

- the subject involves interacting components, state transitions, isolation, scheduling, or observability

Curriculum bias:

- system objects and boundaries
- causal chains
- state transitions
- capacity, risk, and incident behavior at L3

Drill bias:

- `Causal Trace`
- `Quantification`
- `Transfer`
- `Debug`

Common anti-patterns:

- component lists without causal reasoning
- no observability path
- engineering decisions without risk or capacity framing

## Type E: Methodologies

Examples:

- TDD
- prompt engineering
- incident review

Inference signals:

- the subject is a disciplined way of working rather than a runtime or platform

Curriculum bias:

- failure modes the method prevents
- exact process constraints
- anti-rationalization safeguards
- applicability boundaries and maintenance cost

Drill bias:

- `Counterexample`
- `Design Critique`
- `Transfer`
- `Discrimination`

Common anti-patterns:

- value sermon without operating rules
- process summary without gates
- no examples of when not to use the method

## Shared Phase Skeleton

Use this as the default rough route for non-`Type C` domains:

1. `Phase 1`: core mental model and safe usage
2. `Phase 2`: common patterns and composition
3. `Phase 3`: failure modes, debugging, and boundaries
4. `Phase 4`: design trade-offs and advanced use
5. `Phase 5`: real-world engineering decisions and system connections

Adjust names and concept density by domain type, but keep the route stable enough for cross-session continuity.

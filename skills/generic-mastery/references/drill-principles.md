# Drill Principles

## Purpose

Drill is deliberate practice. It compresses weak spots, tests stability, and produces evidence-backed mastery signals. It is not hidden teaching.

## Entry Paths

- normal drill for taught concepts
- cold-start calibration for untaught concepts

## Cold-Start Calibration

If the target concept is not formally taught, ask:

- one `L1` question
- one `L2` question
- one `L3` question

Outcomes:

- weak foundation: stop drill and route to `teach`
- mixed result: patch the weak layer briefly, then drill
- strong prior knowledge: allow drill, but do not overclaim completion without evidence

## Exercise Type Pool

- `Prediction`
- `Debug`
- `Design Critique`
- `Quantification`
- `Discrimination`
- `Transfer`
- `Causal Trace`
- `Counterexample`

Pick types based on domain family and concept depth.

## Quality Gate

Before presenting an exercise, verify:

- it tests the target layer
- it does not require untaught prerequisites
- the question boundary is clear
- the answer can be judged
- the item is not trivia
- the item is not just leading the learner to the answer
- the item is not too similar to recent drills on the same concept

If the exercise fails the gate, rewrite it.

## Scoring Dimensions

Score every exercise on:

- `Rules Accuracy`
- `Reasoning Chain`
- `Decision Grounding`
- `Boundary Awareness`
- `Clarity`

Each score must point to something the learner actually said.

## Writeback Rules

After drill:

- write exercise-level evidence to `drill-log.md`
- update mastery, gaps, and next recommendation in `progress.md`
- add a resume note to `session-log.md`

Mastery may not increase without evidence-backed scoring.

## Mandatory Return-To-Teach Conditions

Return to `teach` when:

- the learner repeatedly misses rule-level understanding
- the learner is guessing instead of reasoning
- missing prerequisites are the real blocker
- the drill is drifting into full hidden teaching

## Domain Bias

Recommended type emphasis:

- `A`: `Prediction`, `Debug`, `Quantification`, `Transfer`
- `B`: `Design Critique`, `Debug`, `Counterexample`, `Transfer`
- `C`: `Prediction`, `Discrimination`, `Debug`, `Transfer`
- `D`: `Causal Trace`, `Quantification`, `Debug`, `Transfer`
- `E`: `Counterexample`, `Design Critique`, `Transfer`, `Discrimination`

# Skill Review Principles

Use these principles to explain judgments and to avoid shallow review language.

## Core Standard

Good skills are behavioral infrastructure:

> A good skill compresses expert judgment, boundaries, and verification into an operating guide the model can execute reliably.

Shorter version:

> A good skill uses the least context needed to push the model consistently toward correct behavior.

## Engineering Principles

1. A skill is not a human README. It is a behavior-shaping artifact for an AI agent.
2. A skill should solve a specific reliability gap that the base model does not handle consistently.
3. A good description triggers the skill; it does not summarize the workflow.
4. A good workflow encodes expert order of operations, not a pile of advice.
5. A good boundary prevents the model's most likely overreach.
6. A good Iron Law blocks the one shortcut most likely to ruin the task.
7. A good anti-pattern list names the model's lazy defaults concretely.
8. A good reference strategy keeps high-frequency instructions in `SKILL.md` and moves low-frequency detail out of the main context.
9. A good script replaces deterministic repetition; it does not hide judgment that belongs in the review.
10. A good verification rule describes observable evidence, not quality adjectives.

## Review Questions

Use these questions when a judgment feels subjective:

- What model failure does this line prevent?
- What correct behavior does this line make more likely?
- Would removing this section make the skill less reliable?
- Is this instruction needed every time, or should it live in a reference?
- Does this step tell the model what to inspect, what to decide, and when to stop?
- Does this gate protect the user from a costly or hard-to-reverse action?
- Can the final output be checked without trusting the model's confidence?

## Common False Positives

- Long skill: may be thorough, or may be context waste.
- Short skill: may be elegant, or may be underspecified.
- Many references: may be progressive loading, or may be fragmentation.
- Many rules: may prevent drift, or may make the workflow rigid and noisy.
- Polished prose: may read well to humans while failing to guide model behavior.

## Good Review Language

Prefer:

- "This earns points because..."
- "This loses points because the model can still..."
- "The risk is unverified because..."
- "The next highest-leverage fix is..."

Avoid:

- "Make it clearer."
- "Add more detail."
- "Looks good overall."
- "Improve quality."
- "Consider best practices."

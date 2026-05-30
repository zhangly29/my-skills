# Evidence Checks

Use this reference when the review needs structural validation or confidence labeling.

## Static Checks

Check:

- `SKILL.md` exists.
- Frontmatter contains `name` and `description`.
- `description` focuses on trigger conditions.
- Main file has a mission or core principle.
- Main file has an ordered workflow when the task is procedural.
- Main file has hard boundaries or non-goals.
- Main file has red flags, anti-patterns, or equivalent drift prevention.
- Referenced files exist.
- Referenced scripts exist and appear executable when execution is expected.
- There are no obvious placeholders such as `TODO`, `TBD`, `FIXME`, `xxx`.
- No unrelated `README.md`, changelog, or template residue is required for the skill to make sense.

## Resource Inventory

For a skill directory, report:

```text
资源概况：
- SKILL.md: present/missing, line count
- references/: count and relevant files read
- scripts/: count and whether execution was checked
- assets/: count and whether used by output
```

Read only resource files that are:

- explicitly referenced by `SKILL.md`;
- needed to verify a claim;
- small enough to inspect without flooding context.

## Scenario Checks

When the user wants a deeper review, ask for or infer 3 realistic usage scenarios:

1. Happy path: a request the skill should handle.
2. Boundary path: a nearby request the skill should decline or narrow.
3. Failure path: a request that tempts the model into the skill's known anti-pattern.

For each scenario, judge:

- Would the `description` trigger?
- Which workflow step handles it?
- What evidence would prove successful behavior?
- What likely failure remains?

## Confidence Labels

Use these labels in the report:

| Label | Meaning |
|---|---|
| Confirmed | Directly observed in files or command output. |
| Likely | Strongly implied by structure, but not executed end to end. |
| Risk | Plausible failure that needs scenario testing or script execution. |
| Not verified | Not checked in this review. |

## Priority Labels

Use these labels for fixes:

| Priority | Meaning |
|---|---|
| P0 | Blocks safe use or makes the skill misleading. |
| P1 | Major reliability issue; fix before relying on the skill. |
| P2 | Meaningful quality issue; fix during normal iteration. |
| P3 | Minor polish or maintainability improvement. |

## Review Depth

Default review is file-based:

- Read `SKILL.md`.
- Inspect referenced resources.
- Score with evidence.
- State unverified runtime behavior.

Deep review adds behavior testing:

- Run static scripts if safe.
- Simulate 3 scenarios.
- Compare expected versus actual model behavior when possible.
- Update confidence labels after testing.

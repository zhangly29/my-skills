# Skill Review Rubric

Use a 100-point scale. Award points for behavior-shaping value, not for length or polish.

## Grade Bands

| Score | Grade | Meaning |
|---:|---|---|
| 90-100 | A | Production-grade: reliable trigger, clear workflow, evidence-backed delivery, low context waste. |
| 80-89 | B | Strong: usable with minor risks or missing verification. |
| 70-79 | C | Serviceable: useful idea, but behavior still depends on model improvisation. |
| 60-69 | D | Weak: important structure or evidence is missing. |
| 0-59 | F | Not ready: vague trigger, unclear workflow, unsafe behavior, or unverifiable output. |

## Dimensions

### 1. Trigger Accuracy - 15 points

Ask:
- Does `description` describe when to use the skill, not the workflow?
- Does it include concrete user intents, synonyms, and target artifacts?
- Would it avoid triggering for unrelated tasks?

Scoring:
- 13-15: Concrete trigger conditions, good keyword coverage, no workflow shortcut.
- 9-12: Mostly clear, but misses common synonyms or has minor ambiguity.
- 5-8: Vague description or overly broad trigger.
- 0-4: Missing, misleading, or mostly workflow summary.

### 2. Task Boundary - 15 points

Ask:
- What exact problem does this skill solve?
- What does it explicitly refuse or defer?
- Does it prevent scope creep and speculative work?

Scoring:
- 13-15: Sharp mission, explicit hard boundaries, clear non-goals.
- 9-12: Mission is clear but non-goals are incomplete.
- 5-8: Broad purpose with weak stopping rules.
- 0-4: Generic helper skill with no usable boundary.

### 3. Workflow Executability - 20 points

Ask:
- Can the model follow the workflow without inventing steps?
- Are required, blocking, and conditional steps marked?
- Are user confirmation gates placed before risky actions?

Scoring:
- 17-20: Ordered checklist, concrete actions, gates, and stop conditions.
- 13-16: Good workflow with minor gaps or vague substeps.
- 8-12: Some steps exist, but execution still depends on improvisation.
- 0-7: No real workflow or mostly conceptual advice.

### 4. Context Economy - 15 points

Ask:
- Is `SKILL.md` short enough to load frequently?
- Are low-frequency details moved to references?
- Are references loaded progressively by need?

Scoring:
- 13-15: Minimal main file, clear reference loading rules, no duplicated bulk content.
- 9-12: Mostly economical with some duplication or overloading.
- 5-8: Main file mixes high-frequency rules with heavy detail.
- 0-4: Large, unfocused context dump.

### 5. Drift Prevention and Safety - 15 points

Ask:
- Is there an Iron Law or equivalent core constraint?
- Are anti-patterns and red flags concrete?
- Does it handle destructive, expensive, or user-visible actions safely?

Scoring:
- 13-15: Strong core constraint, concrete anti-patterns, safety gates.
- 9-12: Some guardrails, but common failure modes remain open.
- 5-8: Generic warnings with limited behavioral force.
- 0-4: No meaningful drift prevention.

### 6. Verifiability - 10 points

Ask:
- Does it define what evidence is required?
- Does it separate confirmed facts from risks and assumptions?
- Does it include concrete pre-delivery checks?

Scoring:
- 9-10: Clear evidence standard and checkable output criteria.
- 7-8: Mostly verifiable with minor vague checks.
- 4-6: Some checks, but key claims can remain unsupported.
- 0-3: Relies on subjective judgment.

### 7. Resource Architecture - 5 points

Ask:
- Are `references/`, `scripts/`, and `assets/` used for the right jobs?
- Are deterministic repeated operations scripted when worthwhile?
- Are resource paths accurate?

Scoring:
- 5: Resources are well-scoped and referenced correctly.
- 3-4: Resource layout is mostly sound with minor gaps.
- 1-2: Resources exist but are poorly organized or underused.
- 0: Resources are missing when needed or referenced inaccurately.

### 8. Maintainability - 5 points

Ask:
- Can a future maintainer see why each section exists?
- Is the skill free of placeholders, contradictions, stale names, and unnecessary files?
- Would real usage feedback map cleanly to a section to improve?

Scoring:
- 5: Clear, concise, no obvious maintenance debt.
- 3-4: Minor cleanup or naming issues.
- 1-2: Hard to maintain due to repetition, contradictions, or unclear ownership.
- 0: Template residue, stale files, or incoherent structure.

## Evidence Rules

- Cite file path and line number when possible.
- If line numbers are unavailable, cite section names and exact phrases.
- Mark missing files, unrun scripts, and untested examples as risks, not confirmed failures.
- Do not award full points for a dimension that was not inspected.

---
name: skill-review
description: "Use when the user asks to review, audit, score, rate, evaluate, or improve an existing Codex or Claude skill, SKILL.md, skill directory, or agent skill workflow against engineering quality standards."
---

# Skill Review

IRON LAW: Every score must be evidence-backed. No evidence, no deduction; no evidence, no praise.

Review skills as engineering artifacts that shape model behavior. The goal is not to admire wording, but to judge whether the skill uses minimal context to reliably push the model toward correct behavior.

Speak Chinese to the user by default. Keep file paths, YAML keys, commands, skill names, and exact quoted text in original form.

## References

Load only what the review needs:

- `references/rubric.md`: required for any score, rating, or production-readiness judgment.
- `references/review-principles.md`: required when explaining the standard, reviewing conceptual quality, or rewriting evaluation criteria.
- `references/evidence-checks.md`: required when validating structure, resources, references, scripts, or testability.

## Workflow

Copy this checklist and complete it in order:

- [ ] Step 1: Resolve Target Skill
  - [ ] 1.1 Identify the `SKILL.md` path or skill directory.
  - [ ] 1.2 If the target is ambiguous, ask for the path before reviewing.
  - [ ] 1.3 Read `SKILL.md` before judging.
- [ ] Step 2: Inventory Resources
  - [ ] 2.1 List direct `references/`, `scripts/`, and `assets/` resources if present.
  - [ ] 2.2 Read only referenced files needed to evaluate claimed behavior.
  - [ ] 2.3 Do not bulk-load unrelated large resources.
- [ ] Step 3: Score With Evidence ⚠️ REQUIRED
  - [ ] 3.1 Load `references/rubric.md`.
  - [ ] 3.2 Assign scores by dimension.
  - [ ] 3.3 Attach evidence to every major praise and deduction.
- [ ] Step 4: Check Engineering Fit
  - [ ] 4.1 Load `references/review-principles.md` for conceptual review.
  - [ ] 4.2 Load `references/evidence-checks.md` for structure and verification checks.
  - [ ] 4.3 Distinguish confirmed issues from untested risks.
- [ ] Step 5: Report
  - [ ] 5.1 Lead with total score, grade, and production-readiness judgment.
  - [ ] 5.2 List top strengths, top risks, per-dimension scores, and prioritized fixes.
  - [ ] 5.3 State what was not verified.

## Output Format

Use this shape unless the user asks for something else:

```text
总分：N/100（等级）
结论：是否达到生产级；最关键原因一句话。

主要强项
- ...

主要问题
- [P1/P2/P3] 问题：证据：影响：建议：

逐项评分
| 维度 | 分数 | 证据摘要 |

修复优先级
1. ...

未验证项
- ...
```

## Hard Boundaries

- Do not modify the reviewed skill unless the user explicitly asks for edits.
- Do not give a numeric score without reading the target `SKILL.md`.
- Do not praise or deduct for generic style preferences unless they affect trigger accuracy, workflow reliability, context cost, safety, or verification.
- Do not treat long content as high quality by default.
- Do not treat short content as high quality by default.
- Do not invent trigger examples, test results, scripts, or referenced files that were not present.
- If evidence is missing, mark the item as `未验证` or `风险`, not as confirmed fact.

## Red Flags

Return to evidence collection if any appear:

- "整体不错" without concrete evidence.
- A score changes but no dimension explains why.
- The review focuses on wording polish while ignoring trigger, workflow, boundaries, and verification.
- The review assumes references or scripts work without checking their existence.
- The recommendation says "add more detail" without explaining which model failure the detail prevents.

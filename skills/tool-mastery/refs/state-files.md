# Tool Mastery State Files

## Ownership

`tool-mastery` owns exactly three state files in `{cwd}` for a given topic:
- `{topic}-knowledge-map.md`
- `{topic}-cheatsheet.md`
- `{topic}-resume.md`

These files exist to keep session state explicit, resumable, and resistant to hallucinated progress.

## File 1: `{topic}-knowledge-map.md`

Purpose:
- approved teaching outline
- authoritative checklist for `Part 2`
- durable progress tracker via checkbox state

Rules:
- create on the new-topic path during `Part 0`
- preserve user-approved structure
- update only checkbox state and clearly bounded context corrections
- use checkbox semantics consistently:
  - `[ ]` = not covered
  - `[~]` = partially covered
  - `[x]` = covered

This file is the source of truth for curriculum shape.

## File 2: `{topic}-cheatsheet.md`

Purpose:
- frozen `Part 1` reference layer
- dense, Google-able content that should not be re-taught conversationally

Rules:
- create immediately after first `Part 1` emission
- overwrite only when regenerating the same reference layer for the same topic
- do not teach from memory when this file already exists; point to it

This file is the source of truth for foundational reference content.

## File 3: `{topic}-resume.md`

Purpose:
- explicit handoff document for the next session
- compact snapshot of where the session stopped
- anti-drift input for recovery when the user says only `继续`, `continue`, or provides empty input

Rules:
- write or refresh at every detected session end
- may also be refreshed after a major teaching checkpoint if needed, but session end is mandatory
- summarize only verified progress from files and the current session, never inferred progress

Recommended template:

```markdown
# {topic} Resume

## Topic
- Topic: {topic}
- Last updated: {timestamp}

## Learner Context Snapshot
- OS: ...
- 语言栈: ...
- 目标场景: ...

## Verified Progress
- Completed:
  - 2.1 ...
- Partial:
  - 2.2 ...
- Not started:
  - 2.3 ...

## Last Session Stop Point
- 停在: ...
- 本次讲到的关键场景: ...

## Suggested Next Step
- 下一步建议: ...
- 如果用户只说“继续”，默认从这里恢复

## Drill Status
- Drill: 未开始 / 部分完成 / 已完成
- 已反馈题目: 0/3

## Relevant Files
- Knowledge map: `{cwd}/{topic}-knowledge-map.md`
- Cheatsheet: `{cwd}/{topic}-cheatsheet.md`
```

This file is the source of truth for resume entrypoint and next-step recommendation.

## Priority Order During Recovery

When the files disagree, prefer them in this order:
1. `{topic}-resume.md` for the latest verified stop point and next step
2. `{topic}-knowledge-map.md` for durable checkbox truth
3. `{topic}-cheatsheet.md` for reference existence and scope

If `resume.md` conflicts with map checkboxes, do not trust the stale summary blindly. Reconcile using the map and then refresh `resume.md`.

## Forbidden Artifacts

Do not create:
- `progress.md`
- `session-log.md`
- `phases/`
- `drill-log.md`
- any extra topic-tracking file outside the three owned files


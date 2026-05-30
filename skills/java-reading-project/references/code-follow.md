# Code Follow Reference

## Mission

Make code construction visible during a Teaching Slice. The learner should be able to watch the project grow by class, method, patch hunk, or responsibility block.

This is not a typing animation. The unit of learning is a meaningful Code Follow Block.

## Build Modes

`build_mode` controls how code is shown during implementation:

| Mode | Meaning | Best For |
|---|---|---|
| `normal` | Existing behavior: explain before/after a Teaching Slice, then implement focused patches inside the slice. | Later review or confident learners |
| `follow` | Show each meaningful code block before applying it. | Default recommendation for this learner |
| `micro-follow` | Use smaller blocks and more confirmations. | Node `1.1`, unfamiliar syntax, or learner explicitly wants close watching |

`teaching_mode` and `build_mode` are separate:

- `teaching_mode: guided|auto` controls whether to wait for confirmations.
- `build_mode: normal|follow|micro-follow` controls how visible code construction is.

## Code Follow Block

Each block must include:

```markdown
## Code Follow Block <n>/<total>：<标题>

目标文件：

这一块要解决：

即将写入：

为什么现在写：

JDK8 到现代 Java 桥接：

写入后你应该看到：

确认后我应用这一块。可以直接说“继续 / ok / 应用”。
```

Rules:

- `目标文件` must be exact.
- `即将写入` should be a code preview or patch preview.
- `JDK8 到现代 Java 桥接` is optional when the block has no unfamiliar Java syntax/API.
- `写入后你应该看到` should name the new class/method/responsibility, not every line.

## Guided And Auto Behavior

In `guided + follow` or `guided + micro-follow`:

1. Show the Code Follow Block.
2. Wait for explicit confirmation.
3. Apply only that block.
4. Show a short applied summary.
5. Move to the next block.

In `auto + follow` or `auto + micro-follow`:

1. Show the Code Follow Block.
2. Apply it without waiting.
3. Show a short applied summary.
4. Continue.

In `normal`, do not emit Code Follow Blocks.

## Block Size

For `follow`, use blocks such as:

- one small class or record
- one cohesive method
- one exception type plus its use site
- one parser or validator branch
- one report aggregation step

For `micro-follow`, split further when useful:

- class skeleton before methods
- one method at a time
- one unfamiliar modern Java idiom at a time
- one important branch or invariant at a time

Do not split so small that the learner sees fragments without a responsibility boundary.

## Progress Bookmark

Before showing or applying a block, set:

```yaml
progress.current_follow_block: "<block id/title>"
```

After a block is fully applied and summarized:

- keep `current_follow_block` as the last applied block until the next block starts
- clear it when the Teaching Slice is complete

`jr pause` and `jr resume` use this bookmark to restore the exact follow point.

## Applied Summary

After applying a block, show:

```markdown
已应用：

现在文件里多了：

下一块将解决：
```

Keep it short. The detailed reading route belongs in `READING_GUIDE.md`.

## Evidence Rules

Watching code being written is not mastery evidence by itself.

Only record understanding evidence when the learner answers the post-project assessment, asks a revealing question, explains a boundary, or transfers the idea to another context. Confirmation-only replies and watching Code Follow Blocks are not mastery evidence.

## Anti-Patterns

- Do not use character-by-character or line-by-line spectacle.
- Do not preview a huge patch as one block.
- Do not apply code before confirmation in `guided + follow`.
- Do not ask the learner to write implementation code.
- Do not let Code Follow Blocks replace Slice Gate or Slice Completion explanations.
- Do not turn Code Follow into a second unrelated task system.

# Example Session — Golden Trace

## What This File Is

A complete, worked `jr start` → build → demo → assessment trace for node `1.1`
(`B-lang-exception`). It is **illustrative, not a rule source**. When generating a
real session, emulate the *feel* and *rhythm* shown here, but always obey the
owning packets (`runtime-control.md`, `start-project.md`, `build-project.md`,
`evidence-policy.md`, `adaptive-difficulty.md`). If anything here ever conflicts
with a rule packet, the rule packet wins.

Do not load this file during normal command execution — it is a quality
reference for authors and for the model when it needs to recalibrate tone. Read
it when you want to remember what "good" looks like.

## Why This Case Is Addictive (design principles to reuse)

These are the levers that turn a reading project into something the learner
*wants* to keep pulling on. Reuse them; do not turn them into gimmicks.

1. **Open inside a failure, not a syllabus.** The first thing the learner sees is
   a 02:40 alert and a useless log line — a problem with a cost, not a topic.
2. **Give the learner a role with a stake.** "你是接手这个模块的 on-call" beats
   "本章学习异常处理". A role creates ownership; ownership creates curiosity.
3. **Name an antagonist.** A concrete bad design (`catch (Exception e) { throw new
   RuntimeException("import failed"); }`) is something to *defeat*. Concepts are
   boring; villains are not.
4. **Withhold the answer, expose the clue.** Each slice ends on the *next* slice's
   unresolved signal (a log line, a swallowed cause), so stopping feels like
   leaving a show mid-cliffhanger.
5. **Reward with a reusable tool, not a score.** Equipment ("Cause Chain 保留检查")
   is a sentence the learner can carry into their real job tomorrow. That is the
   dopamine — competence they can *use*, not a badge.
6. **Let the bad design fail in front of them.** `demo-naive` actually loses the
   cause and sends on-call chasing the wrong service; `demo` fixes it. Seeing the
   failure is more convincing than being told about it.
7. **Keep friction near zero.** Natural replies (`继续`, `嗯`) move forward; the
   learner never has to figure out "what do I type now".
8. **Vary the rhythm.** Same required sections every slice, but different incident
   detail, different bad-design pressure, different suspense. Mechanical repetition
   kills the spell faster than anything.

The trace below is abbreviated where rhythm repeats (Slices 1, 2, 4, 5 are
summarized) and shown in full where the core teaching happens (the incident,
Slice 3, the double demo, and the assessment).

---

## Trace

> Conventions below: `👤` = learner message, `🤖` = skill output. Lines in
> `〔…〕` are author annotations explaining *why* a beat works — they are **not**
> part of the real output.

### 1. Command

```text
👤 jr start 1.1 --s --follow
```

〔`--follow` → close-reading Code Follow Blocks. Default `guided` teaching mode:
the learner confirms before each slice is implemented.〕

### 2. Node acknowledgement (before any state write)

```text
🤖 已识别节点：1.1 Java 核心语法与面向对象
   项目规模：s
   教学模式：guided
   构建模式：follow
   入口模式：优先 incident-first
   工作区：/home/you/java-read
   我会基于 training map、progress evidence、已有装备、adaptive profile 和
   recommendation index，只推荐 1 个最适合当前训练靶心、能从事故现场切入、
   并且能拆成 Teaching Slices 的 corpus-backed 可运行项目。
```

〔Active-project preflight already ran read-only and found nothing in progress.
No file has been written yet.〕

### 3. Recommendation (learner display layer)

```text
🤖 ## 推荐项目：供应商导入的「异常吞噬」现场

   - 项目: `supplier-product-import-core` · 规模 `s` · 入口 `incident-first`
   - 节点边界: `B-lang-exception` / 种子: `payment-gateway-errors`
   - 事故现场: 凌晨对账失败，导入任务日志只有一行
     `RuntimeException: import failed`，没有任何 cause。
   - 你的身份: 刚接手这个导入模块的后端 on-call，半夜被叫醒。
   - 本章对手: 前任写的 `catch (Exception e) { throw new RuntimeException(...) }`
     —— 它吞掉了真正的失败原因。
   - 做什么: 把一个会「吞 cause」的导入流程，读懂并重建成线上可诊断的版本。
   - 为什么适合当前节点: 1.1 的异常边界是你最该先拿下的能力，这个事故正好压在
     parse / validate / 异常 三条边界的交界处。
   - 不重复说明: 你还没做过任何导入类项目，无重复风险。
   - demo 信号: 支持 double demo —— `demo-naive`（丢 cause）对照 `demo`（保留 + 分类）。
   - 正反馈点: 读完你会拿到一件能直接用在 code review 里的「装备」。
   - adaptive_plan: `standard` / 解释密度正常、线索 balanced、JDK8 桥接按热点补。

   如果认可，回复 `开始`；如果方向不对，告诉我调整偏好，我会重新推荐 1 个更合适的项目。
```

〔The data-layer YAML (per `start-project.md §Recommendation Format`) was staged
and optionally validated with `--recommendation -` before this display. Only the
display layer is shown to the learner.〕

```text
👤 开始
```

〔On approval: initialize `{progress_state}`, set active project fields,
`progress.status: selected`, regenerate `{progress_summary}`. The persisted
transition is `idle -> selected` (see `runtime-control.md §Progress Status
Transitions`).〕

### 4. Incident packet — the first thing the learner reads

```text
🤖 02:40，你的手机响了。对账系统报警：昨夜导入的一批供应商商品，价格字段
   有一半变成了 0。你打开导入任务的日志，翻了三屏，只找到这一行：

       2026-05-27 02:11:43 ERROR ImportJob - RuntimeException: import failed
           at com.acme.imp.ImportJob.run(ImportJob.java:48)

   没有 cause。没有是哪一行数据。没有是 parse 失败还是校验失败。
   你现在要决定：先去查文件编码？查数据库？还是查上游供应商接口？
   —— 而这行日志，什么都没告诉你。

   先不急着改代码。你最想先确认的是哪一点？（随便说，这不是考试）
```

〔Concrete artifact + visible cost + a single low-pressure investigation prompt.
The prompt is explicitly *not* an assessment (`build-project.md §Teaching Slice
Core Rule`). Whatever the learner says here is *not* mastery evidence
(`evidence-policy.md`).〕

```text
👤 我想知道到底是哪条数据、哪一步炸的，这行日志太废了
```

〔This is a real observation about diagnosability → record as user-initiated
feedback in `TEACHING_LOG.md`, and set
`progress.current_investigation_focus: "日志无法定位失败数据/失败阶段"`. It
biases emphasis only; it does **not** reorder slices.〕

### 5. Slice Gate — Slice 3「异常边界」(shown in full)

〔Slices 1 (输入边界) and 2 (解析边界) ran first and are summarized in §6. We jump
into Slice 3 because it is where the antagonist lives and where the learner's
own curiosity ("这行日志太废了") gets paid off.〕

```text
🤖 ## 即将开始 Slice 3：异常边界

   事故现场：还记得那行什么都没说的 `RuntimeException: import failed` 吗？
   这一章就是它的犯罪现场。

   你的身份：你要决定，当一行供应商数据炸了，系统应该往日志里留下什么。

   本章对手：前任的写法 ——
       catch (Exception e) {
           throw new RuntimeException("import failed");  // ← cause 在这里被丢掉
       }

   这个边界解决什么问题：哪些失败该抛异常、抛哪种、要带走什么上下文，
   才能让凌晨的 on-call 一眼看出是 parse 还是 validate、是哪一行。

   为什么现在需要它：你上一章（解析边界）已经能把一行变成对象了；现在要回答
   「变不出来的时候怎么办」。

   会创建/修改：ImportException（自定义异常）、RowParser 的失败分支。

   核心 API 设计：异常携带 rowNumber + rawLine + cause；parse 失败与 validate
   失败用不同类型区分。

   异常/返回值/集合选择：parse 失败 → 抛 ImportException（带 cause）；
   业务校验失败 → 不抛，进报告（下一章）。

   阅读关注点：cause 是怎么被一路带出来的，以及为什么 validate 失败不走异常。

   读完这一章后应该能看懂：一条异常链如何把「02:40 的你」直接带到出事的那一行。

   这一章会解锁的装备：Cause Chain 保留检查。

   你确认后我开始实现。可以直接说"继续 / ok / 开始"。
```

```text
👤 继续
```

〔`guided` mode: this fresh confirmation authorizes implementing Slice 3. A
`继续` left over from the previous Slice Completion would *not* have counted
(`runtime-control.md §Teaching And Build Mode Matrix`).〕

### 6. Code Follow Block — antagonist vs fix (because `--follow`)

```text
🤖 ## Code Follow Block 1/2：自定义异常 ImportException

   目标文件：src/main/java/com/acme/imp/ImportException.java

   这一块要解决：给失败一个「能带上下文」的类型，而不是裸 RuntimeException。

   即将写入：
       /**
        * 导入阶段的解析失败。携带行号、原始行文本和底层 cause，
        * 让 on-call 不必翻代码就能定位是哪一行、因为什么炸的。
        * 非职责：业务校验失败不用它（那是报告，不是异常）。
        */
       public class ImportException extends RuntimeException {
           private final int rowNumber;
           private final String rawLine;

           public ImportException(int rowNumber, String rawLine, Throwable cause) {
               super("第 " + rowNumber + " 行解析失败: " + rawLine, cause); // ← cause 必须传进 super
               this.rowNumber = rowNumber;
               this.rawLine = rawLine;
           }
           public int rowNumber() { return rowNumber; }
           public String rawLine() { return rawLine; }
       }

   为什么现在写：这是把「无法定位」变成「一眼定位」的那一行 —— super(msg, cause)。

   JDK8 到现代 Java 桥接：这里没有用 record，因为异常类不能是 record（需要继承
   RuntimeException）。字段+构造器是这里的正解。

   写入后你应该看到：一个带 rowNumber / rawLine / cause 的异常类型。

   确认后我应用这一块。可以直接说"继续 / ok / 应用"。
```

```text
👤 应用
```

```text
🤖 已应用：
   现在文件里多了：ImportException，构造时强制传入 cause。
   下一块将解决：在 RowParser 里把它抛出来，并刻意对照前任「吞 cause」的写法。
```

〔Block 2/2 (RowParser 的失败分支) would follow the same shape; omitted here for
length. Watching code appear is **not** mastery evidence
(`evidence-policy.md §Build And Demo Boundary`).〕

### 7. Slice Completion — Slice 3 (shown in full)

```text
🤖 ## Slice 3 完成：异常边界

   完成内容：ImportException + RowParser 失败分支，parse 失败现在带着 cause 抛出。

   关键代码路径：RowParser.parse() → 抛 ImportException(row, line, cause)
                → ImportJob 捕获后记录 rowNumber/rawLine/cause。

   建议阅读顺序：先读 ImportException 的构造器，再回到 RowParser 看它在哪抛。

   这一小步的设计取舍：parse 失败「抛」，业务校验失败「不抛、进报告」——
   两类失败的处置故意不一样。

   你可能以为：所有错误都该抛异常，统一 catch 一下就好。

   实际设计：如果业务校验也抛异常，那「第 50 行价格为负」会和「文件编码炸了」
   长得一模一样，报告就废了。异常留给「无法继续解析」，校验失败留给报告。

   证据在代码里：ImportException 的 super(msg, cause) —— 对比前任的
   `throw new RuntimeException("import failed")`，差别就是那个 cause 参数。

   如果放到生产：02:40 的你打开日志，会直接看到
   `第 137 行解析失败: ... Caused by: MalformedInputException`，
   不用再猜是文件、数据库还是上游。

   你获得了装备：🔧 **Cause Chain 保留检查**
   - 用法一句话：「这里 wrap 异常时，有没有把原始 cause 带进 super？没带的话
     on-call 怎么知道是 SDK 还是业务失败？」
   - 可迁移到：第三方 SDK 调用、文件解析器、消息消费者。
   - 代码证据：ImportException 构造器的 super(message, cause)。

   下一章线索：现在 parse 失败能定位了，但你导入的那批「价格为 0」的数据——
   它们其实 parse 成功了。是谁让一条 price=0 的记录大摇大摆走到了下游？
   （那是校验边界的事。）

   验证：本章随主流程一起在最终 demo 验证。
```

〔Note the closing line: a *zero-friction hook* — the next slice's unresolved
signal (price=0 passing validation), not "输入继续". The equipment block carries
a concrete use sentence + transfer contexts + code evidence, exactly as
`build-project.md §Slice Completion Template` requires.〕

```text
👤 嗯
```

〔Natural reply → open Slice 4's gate. It does not authorize implementing Slice 4;
that gate needs its own fresh `继续`.〕

### 8. Remaining slices (compressed)

- **Slice 1 输入边界**（已在 Slice 3 之前完成）：文件路径/编码/读取策略；装备「编码假设检查」。
- **Slice 2 解析边界**：一行文本 → typed `ProductRow`；装备「字段来源追问」。
- **Slice 4 校验边界**：price=0 这类业务错误为什么进报告而不是抛异常；装备「业务失败 vs 解析失败二分」。
- **Slice 5 报告边界**：把成功/解析失败/校验失败聚合成可读报告；装备「失败可读性检查」。

### 9. Double demo — let the antagonist fail out loud

```text
🤖 我把两种设计都做成了可运行命令，你可以亲眼看差别：

   $ java -jar target/supplier-product-import-core.jar demo-naive
   ERROR: import failed
   (退出码 1，没有行号，没有 cause —— 这就是 02:40 的你看到的)

   $ java -jar target/supplier-product-import-core.jar demo
   导入报告：
     成功 18 行
     解析失败 1 行  → 第 137 行: Caused by MalformedInputException(GBK?)
     校验失败 4 行  → 第 12,40,55,88 行: price 必须 > 0（进报告，未抛异常）
   (退出码 0，报告完整)
```

〔`demo-naive` must expose a *real* failure mode from the seed, never a faked one
(`build-project.md §Verification`). The contrast is the payoff for the whole
project.〕

### 10. Post-project assessment — a production review, not a quiz

〔Runs only after all slices build and demo passes; `progress.status:
assessment_pending`. 4–6 prompts, grouped after the project.〕

```text
🤖 项目跑通了。现在做一个简短的「线上复盘」，不是考试，但你的回答会决定我对
   这个节点掌握度的判断。

   复盘 1（边界归属）：parse 失败和「price=0」这种校验失败，在你重建的系统里
   分别由谁处理、为什么不能合并？

👤 parse 失败是数据根本读不成对象，必须抛 ImportException 带 cause；price=0 是
   读成对象了但业务上不合法，应该进报告。如果合并，报告就分不清「文件坏了」和
   「数据不合规」，on-call 会查错方向。

🤖 ✅ 这是一段清晰的边界归属说明，并且你自己点出了「合并会让 on-call 查错方向」——
   这正是 antagonist 的代价。记为理解证据（boundary ownership: adequate→strong）。

   复盘 2（迁移）：同样的「保留 cause」原则，如果换成调用一个短信网关 SDK，
   你会在哪一步、怎么用？

👤 在 catch 短信 SDK 异常往上抛的时候，必须把 SDK 的原始异常当 cause 传进去，
   不然只看到「发送失败」，不知道是超时还是签名错。

🤖 ✅ 你把「Cause Chain 保留检查」这件装备迁移到了一个新领域（短信网关）——
   记为 transfer evidence。
```

〔Two of the 4–6 prompts shown. The learner's answers — not the build success,
not the `继续`s — are what `evidence-policy.md` admits as mastery / transfer
evidence. A `jr ask` rating or "我读懂了" would **not** count.〕

### 11. Progress merge

```text
🤖 (内部) 组装 progress_update → 校验 → 合并：
   $ python java-reading-project/scripts/validate-progress.py --progress-update - < /tmp/pu.yaml
   Validation passed.
   合并进 progress-state.yaml，status: completed，regenerate progress.md。
```

```text
🤖 这个项目完成了。你拿到 5 件装备，其中「Cause Chain 保留检查」你已经在短信网关
   场景上用过一次（这是真正的迁移证据）。
   下一步建议：`jr progress 1.1` 看节点判断，或 `jr start 1.1 --s` 换一个不同
   domain 的异常边界项目巩固。
```

---

## Boring vs Addictive — same beat, two versions

Use this to calibrate. The left column is what a tired generator produces; the
right is the target.

| Beat | ❌ Boring (avoid) | ✅ Addictive (target) |
|---|---|---|
| Opening | 「本章学习 Java 异常处理。」 | 「02:40 你被报警叫醒，日志只有一行 `RuntimeException: import failed`。」 |
| Bad design | 「应避免吞掉异常 cause。」 | 「本章对手：前任写的 `catch(Exception e){ throw new RuntimeException(...) }`。」 |
| Slice end | 「本章结束，输入继续进入下一章。」 | 「是谁让一条 price=0 的记录走到了下游？——那是下一章的事。」 |
| Reward | 「你已掌握异常处理。」 | 「装备：Cause Chain 保留检查 —— 明天就能用在你的 code review 里。」 |
| Proving it | 「异常处理很重要。」 | `demo-naive` 真的丢了 cause，让 on-call 查错方向；`demo` 修好。 |

The right column is never decoration over nothing — every hook lands on real
code, a real failure mode, and a reusable tool. That is the line between
"immersive engineering" and "fantasy framing" (`build-project.md §Anti-Regression`).

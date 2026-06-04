# Code Annotation Reference

## Mission

Generate code comments and reading-guide explanations that match the learner profile:

```text
Java backend developer
low-to-mid Java language confidence
daily experience: JDK 8 + Maven CRUD
traditional Tomcat web projects
little or no Spring framework experience
stronger understanding of business flows than Java language details
```

The goal is to make generated projects readable without turning code into a textbook. Comments should remove avoidable confusion around modern Java, API choices, business vocabulary, and engineering boundaries.

For Java Reading Project deliverables, annotation is a hard quality gate. The generated code must be readable as a learning artifact on the first pass; do not wait for the learner to complain that enum values, class responsibilities, or boundary ownership are unclear.

## Comment Language Rule

- All generated code comments and Javadocs in learner project source files must be written in Chinese by default, including class-level Javadocs, method Javadocs, inline comments, enum value comments, exception comments, and JDK8 bridge notes.
- Keep Java identifiers, API names, exception names, command names, package names, Maven coordinates, and raw log/error text in English when that is the precise technical form.
- Do not use English prose for generated learner-facing source comments unless quoting an original API/error/log message or preserving an identifier's exact wording.

## Mandatory Reading Annotations

Every generated reading project must satisfy these minimums:

- Every core class has class-level Javadoc explaining responsibility, design intent, non-responsibilities, and extension direction.
- Every boundary service class documents input, output, failure strategy, what it deliberately does not own, and where the next boundary begins.
- Every enum type has class-level Javadoc explaining the business vocabulary and where mapping/decision logic lives.
- Every enum value has Chinese business semantics and, when relevant, handling guidance or production risk.
- Every custom exception documents why it exists, what context it carries, why `cause` is preserved, and how callers should use it.
- Every `record` used as a domain/DTO model has a short JDK8 bridge note or class-level Javadoc explaining what the record represents.
- `READING_GUIDE.md` must include a role-based class map and a "why these classes exist" section for the generated code.

These are required even when inline comment density stays low.

## Comment Levels

### L1 Production Comment

Short comments that would still be acceptable in production code.

Use for:

- boundary intent
- exception strategy
- collection choice
- non-obvious tradeoff
- business invariant

Example:

```java
// 业务不变量：同一个 supplierSku 在一次导入中只能出现一次，重复行进入诊断报告。
```

### L2 Learner Bridge Comment

Short comments that help this learner cross from JDK 8 CRUD code to modern Java reading.

Use for:

- Java 17/21 syntax that may be unfamiliar to a JDK 8 developer
- modern Java APIs such as `record`, `Stream`, `Optional`, `Map.merge`, `List.of`, `var`, switch expressions, pattern matching, text blocks
- compact idioms where the old JDK 8 style would be longer and more familiar
- framework or library entry points that the learner has likely not used before

Example:

```java
// JDK8 视角：record 可以先理解成“只读 DTO + 自动生成构造器/访问器/equals/hashCode”。
record ImportRow(String sku, String name, int price) {
}
```

Example:

```java
// JDK8 视角：Map.merge 把“首次出现”和“累计计数”合成一步，避免手写 containsKey 分支。
errorCount.merge(errorCode, 1, Integer::sum);
```

### L3 Reading Guide Explanation

Longer explanations belong in `READING_GUIDE.md`, not inline code comments.

Use for:

- multi-step API explanations
- why one design was chosen over another
- JDK 8 equivalent snippets
- framework lifecycle explanations
- diagrams, flow traces, or "read this first" routes

## Decision Rules

Add a code comment when at least one is true:

- the line uses a Java feature likely unfamiliar to a JDK 8 CRUD developer
- the code hides an important boundary decision
- a failure would be hard to debug without knowing the intent
- a collection/API choice prevents a common beginner mistake
- the comment names a business invariant that is not obvious from the method name

Do not add a code comment when:

- it merely translates syntax, such as `// 创建对象`, `// 遍历列表`, `// 返回结果`
- the method/class name already communicates the intent
- the explanation needs more than 2 short lines
- the comment repeats the Teaching Slice explanation

## Comment Density

Default density for this learner:

- each core class must include class-level Javadoc and may include 1-4 short inline comments
- each method may include 0-2 comments, plus Javadoc when the method is a boundary API or public learning hotspot
- each Teaching Slice should include comments only at the new or changed learning hotspots
- if more explanation is needed, move it to `READING_GUIDE.md`

For node `1.1`, allow slightly more L2 comments around object modeling, collection choice, exception boundaries, and unfamiliar Java syntax. Still avoid line-by-line narration.

## Annotation Quality Gate

Before compiling final delivery, inspect changed Java files and verify:

```text
core class Javadoc: present
enum value Chinese semantics: present for every value
boundary service input/output/failure strategy: present
non-responsibility or next-boundary note: present where a boundary may be confused
extension note: present for rules likely to grow
line-by-line translation comments: absent
```

If any required annotation is missing, fix it before marking the Teaching Slice or project complete.

## Reading Guide Pairing

When code uses L2 learner bridge comments, `READING_GUIDE.md` should include a short "JDK8 到现代 Java 桥接" note for the same slice when useful.

The guide may show a tiny comparison:

```java
// JDK8 常见写法
if (map.containsKey(key)) {
    map.put(key, map.get(key) + 1);
} else {
    map.put(key, 1);
}

// 现代 Java 写法
map.merge(key, 1, Integer::sum);
```

Keep comparisons small and only include them when they reduce real confusion.

## Anti-Patterns

- Do not create wall-of-comments code.
- Do not explain every Java keyword.
- Do not hide poor naming behind comments.
- Do not replace Teaching Slice explanations with inline comments.
- Do not ship a reading project whose core classes require the learner to infer business meaning from English enum names alone.
- Do not rely on the learner to request missing comments; missing class/enum/boundary annotations are build-quality defects.
- Do not assume the learner knows Spring, Java 17/21 syntax, or modern Java idioms unless prior project evidence proves it.
- Do not remove production-relevant comments just because they are also helpful for learning.

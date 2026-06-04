# Extends Node Reference

## Mission

Handle unmapped catalog nodes by following `java-reading-corpus/_shared/node-extension-protocol.md`.

Do not generate a Java project directly from `java-catalog.md` prose.

## When To Use

Use this reference when:

- `jr start <node-id>` finds the node in `java-catalog.md` but not in `catalog-training-map.yaml`;
- `jr extend-node <node-id>` is invoked;
- mapped corpus resources cannot remediate unresolved FM weakpoints.

## Required Sources

- `java-catalog.md`
- `java-reading-corpus/_shared/node-extension-protocol.md`
- `java-reading-corpus/_shared/catalog-training-map.yaml`
- `java-reading-corpus/corpus-index.yaml`
- `java-reading-corpus/_derived/recommendation-index.yaml`
- `java-reading-corpus/_derived/coverage-matrix.yaml`
- `java-reading-corpus/_shared/concept-atlas.yaml`
- `java-reading-corpus/_shared/failure-mode-codex.yaml`

## Approval Gate

Before writing or modifying corpus resources, show:

```text
节点 <node-id> 尚未结构化映射。
我需要先执行 extends_node：
1. 抽取训练意图
2. 对齐现有 corpus
3. 判断 map-only / seed-extension / boundary-extension
4. 写入 authored corpus resources
5. 运行校验

这会修改 corpus 文件。回复 `开始扩展` 后我再执行。
```

Wait for explicit user approval.

## Extension Output

After approval, produce one of:

- `map-only`: add a node entry to `catalog-training-map.yaml`;
- `seed-extension`: add or update seed resources, then publish the map entry;
- `boundary-extension`: add boundary, at least 3 seeds, required FM references, cross usage, then publish the map entry.

## Validation

Run after edits:

```bash
source ~/.zshrc
uv run python java-reading-corpus/tools/validate-corpus.py
uv run python java-reading-corpus/tools/build-index.py
uv run python java-reading-corpus/tools/check-coverage.py
```

If validation fails, fix authored files. Do not patch generated files to hide failures.

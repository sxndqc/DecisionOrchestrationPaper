# Decision Orchestration（论文）

原 SkillParseUMR 仓库里的 A 篇（`paper-tex/A-orchestration`，"Annotation Guidelines as Skill Orchestration"）搬到这里，
并按 ACL 2026 模板重写。代码和实验仍在 [`sxndqc/SkillParseUMR`](https://github.com/sxndqc/SkillParseUMR)。

- `PLAN.md`：写作规划（立意、论点与证据、已有结果清单、**还要做的实验 E1–E12**、第二个 benchmark 的选择）。先读这个。
- 仓库根目录：论文本体。`main.tex` + `sections/*.tex` + `references.bib`，ACL 官方 `acl.sty` / `acl_natbib.bst`。
  - 编译：`latexmk -pdf main.tex`（pdfLaTeX + BibTeX；Overleaf 直接导入整个仓库/zip，`extra/` 不影响编译）。
  - 红色 `[TODO: …]` 是还没写的内容；表格里红色的 `--` 是还没跑的实验；`[E#]` 对应 `PLAN.md` 第 6 节。
  - 正文 8 页（到 Conclusion），之后是 Limitations、Ethics、参考文献、附录。
- `extra/notes/benchmark-survey.md`：第二个 benchmark 的调研。
- `extra/archive/v0-skill-orchestration/`：旧稿（旧 tex、旧 bib、中文 intro），只作参考。

数字出处：`SkillParseUMR` 的 `main`（`experiment/rsi-zh2`、`rsi-zh-deepseek`、`qwen-zh`、`qwen27-zh`、`jevumr`、`rsi-jev`）和
`claude/zealous-hopper-9qo713`（`experiment/rsi-jev2`、`openai-decision`、`microsoft-decision`）分支。论文里所有 AnCast 分数都按
`newdata/` 的 gold 重新打过分（旧实验原来用 `olddata/gold/zh`，差别 ≤0.3 F）。

本次 ARR 模拟审稿后的修改见 `ARR_REVISION.md`；论文附录新增 E13 证据核验，旧 gold 的 judge 分析与待定位的中间分数保留为空。

本论文的[详细新增实验计划](https://github.com/sxndqc/SkillParseUMR/blob/main/docs/experiments-decision-orchestration.md)保存在代码仓库：PARSEME 闭合决策使用 Jev，反思使用 Opus；Jev 直接候选分类作为同模型对照，Sonnet 生成式 few-shot 作为系统质量/成本对照。独立运行、独立结果表；新增结果仍留空。

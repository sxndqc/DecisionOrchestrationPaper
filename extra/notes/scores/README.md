# 重新打分（newdata gold）

`ancast-newdata.json`：论文里所有 AnCast++ 数字的来源。键是 SkillParseUMR 里的预测目录（`experiment/...`；
`openai-decision`、`microsoft-decision`、`rsi-jev2` 的预测来自 `claude/zealous-hopper-9qo713` 分支），值是逐篇的 P/R/F、
Modal、Temporal、Coref、Comprehensive。宏平均就是逐篇平均。

`rescore_newdata.py`：打分脚本，在 SkillParseUMR 根目录运行，`scorelib/` 里放 zealous-hopper 分支的 `scripts/ancast_doc.py`
（main 上的版本在 AnCast 匹配失败时有一个 `gold_path` 未定义的 bug）。需要 `pip install penman git+https://github.com/umr4nlp/ancast`。

    OUTJSON=out.json python3 -W ignore rescore_newdata.py experiment/rsi-zh2/test/R0 ...

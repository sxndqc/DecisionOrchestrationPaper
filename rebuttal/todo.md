# Rebuttal 实验 TODO 与开销估算（2026-11-26）

单价来自已跑的记录（`SkillParseUMR/experiment/orchestration-v2/runs/**/score.json` 的 cost）：

| 调用 | 实测单价 |
|---|---|
| GPT-6.1-sol + 整本 guideline，UMR 中 / 英，每个 chunk（5 句） | $0.35 / $0.25 |
| GPT-6.1-sol + 整本 guideline，PARSEME，每 5 句 | $0.20 |
| Haiku + 整本 guideline，每 5 句 | $0.06（PARSEME）– $0.14（UMR 中） |
| Haiku fragment procedure，UMR 测试一个版本（20 chunk），中 / 英 | $1.5–1.9 / $0.8–0.9 |
| Jev / Microsoft closed procedure，UMR 测试一个版本 | $0.02–0.28 |
| 任意 procedure，PARSEME 100 句 | $0.00–0.03 |
| closed procedure，PARSEME 全量（约 3500–4000 句） | $0.2–0.3 |
| 反思器 Sonnet 5.5 | 走订阅，$0 |

## 必做（rebuttal 里已经留了 [PENDING n] 的位置）

| # | 实验 | 回应谁 | 状态 | 还需调用 | 估算 |
|---|---|---|---|---|---|
| 1 | baseline + 反思笔记（GPT-6.1-sol，同 50 句 gold，10 轮，测 N10） | 9J4c W1、y4Vj | PARSEME 中：10 轮完成，测试 7/20；PARSEME 英：4 轮；UMR 英：2 轮；UMR 中：1 轮 | 13 + 26 + 28 + 29 次 | $2.6 + $5.2 + $7 + $10.2 ≈ **$25** |
| 2 | baseline + 50 句 gold 作 few-shot | y4Vj、9J4c W1 | PARSEME 中 13/20、英 9/20 已缓存；UMR 未开始 | 7 + 11 + 20 + 20 次，prompt 比 baseline 长约 30% | $1.8 + $2.9 + $6.5 + $9.1 ≈ **$20** |
| 3 | 统计证据：(a) 其余链的 PARSEME 全量测试（Haiku、luna、OpenAI，V0/V10，中英）；(b) V0、V10 测试各重复 3 次（需加一个绕过缓存的 run 编号） | 9J4c W2、y4Vj | Jev、Microsoft 全量已完成 | (a) 12 个全量测试；(b) 每次重复 ≈ $6.5（其中 Haiku UMR 占 $5） | (a) ≈ $10；(b) ≈ $20；合计 **$30** |
| 4 | DSPy GEPA 优化单 prompt 的 Haiku（初始 prompt = 种子文本，同 50 句，反思模型用订阅的 Sonnet） | 6SVz | 未开始，需装 dspy、写适配 | 每个设置约 300 次调用 × $0.001–0.011 | **$10** |
| 5 | 残缺种子消融：清空 30% / 60% 指令文件（PARSEME 另加“候选规则只留动词”），各跑 10 轮反思，测 V0、V10；用 Jev（便宜） | 6SVz | 未开始 | 2 个损坏程度 × 4 个设置；UMR 中每条 ≈ $3，其余 < $1 | **$15** |
| 6 | 模糊任务一个（见下，待你选），一个语言：种子 + 3 条链 × 10 轮 + baseline | 6SVz | 未开始 | 取决于任务 | TempEval-3 ≈ **$20**；RST ≈ $35；MQM ≈ $30；LitBank ≈ $45 |
| 7 | 不花钱的：judge 总分与官方分数的相关系数；各版本候选召回率；AnCast 低于 baseline 的原因分析；bootstrap、SOTA 表重算 | y4Vj、6SVz | 未开始 | 0 | $0 |

必做合计（按 TempEval-3）：25 + 20 + 30 + 10 + 15 + 20 = **约 $120**。
OpenRouter 对并发请求按 max_tokens 预扣额度，余额太低会直接 402（这次就是），需要留 $15–20 余量。
**建议充值 $150**（账户现余约 $2.9；key 的 $250 上限还剩 $227，不用改）。

## 可选

| # | 实验 | 估算 |
|---|---|---|
| 8 | GPT-6.1-sol baseline 再重复 2 次（给 baseline 也报方差） | $40 |
| 9 | GPT-6.1-sol baseline 在 PARSEME 500 句随机样本上（全量要约 $140/语言，不建议） | $40 |
| 10 | UMR 再取 20 个新 chunk 做“新数据”测试（Jev、Haiku、baseline） | $17 |
| 11 | 整条链换随机种子从头再进化一遍（最强的稳定性证据） | $100–150 |

全做：约 $370。

## 需要的 API

- **OpenRouter**（唯一要花钱的）：`openai/gpt-6.1-sol`、`anthropic/claude-haiku-5.5`、GPT-6-luna、三个决策模型（Jev 1.13、Microsoft-Decision-1、OpenAI Decisions）。key 已有，只需充值。
- **Claude 订阅**：Sonnet 5.5 反思器（`claude -p`），已可用，不另收费。
- 不需要其他 API。模糊任务的数据都是公开下载（GitHub / 官方站点）；DSPy 是 pip 包。

## 只有你能补的

- 种子编写花了多少人时（UMR、PARSEME 各多少），编写者是否有该标注体系的经验。rebuttal 里有 3 处 `[AUTHOR]`。
- 模糊任务选哪个。

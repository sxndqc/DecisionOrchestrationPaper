# 写作规划：Decision Orchestration（原 A 篇 "Annotation Guidelines as Skill Orchestration"）

写于 2026-10-10。先规划、后写作；论文本体在仓库根目录（ACL 2026 模板，pdfLaTeX + BibTeX）。
原稿（中文 intro + 旧 tex）原样存在 `extra/archive/v0-skill-orchestration/`，只作参考。

数字全部来自 `sxndqc/SkillParseUMR` 的各分支（出处见第 4 节）。旧实验有的用旧 gold（`olddata/gold/zh`），有的用
`newdata/`；本文统一用 **newdata gold** 重新打了分（本会话本地跑 AnCast，预测文件不变），差别在 0.1–0.3 F 以内。

---

## 1. 现稿的问题（为什么重写）

1. **立意太窄。** 现稿从 "UMR 很难标" 出发，围绕 Chun & Xue 的 pipeline、Brill 1995、"ACL 2026 那篇" 这几篇展开，
   读起来像一个 UMR 工程报告：方法是 "UMR 的 umr-tree"，贡献是 "在 UMR 上能跑"。
2. **最能体现 "decision" 的那条线完全没写。** Jev / OpenAI Decisions / Microsoft-Decision-1 这类只回答封闭问题、
   返回概率的判断模型（`experiment/jevumr`、`rsi-jev`、`rsi-jev2`、`openai-decision`、`microsoft-decision`），
   以及在它们之上的 **calibration**（阈值按实测校准、按置信度把难题升级给强模型）和 **实测式 RSI**（每条改动都重新解析、
   打分、决定去留）都不在稿子里。
3. **"少量数据" 这个核心卖点是隐含的。** 其实所有结果都只用了 1–4 篇 gold 文档（57–201 句）；应该把它写成主线：
   *训练的是流程，不是模型权重*。
4. **测试协议混乱。** 不同实验用不同 gold、不同测试集（0004+0005 / 0005–0007 / 0015–0024），无法放进一张表。
5. **Related work 太薄**，没有 LLM 标注、guideline-following IE、LM 程序/工作流优化、校准与级联、弱监督等方向。

## 2. 新的立意（一句话）

> 一个新的 ontology 刚定义好时，只有一份 guideline 和几篇 gold 文档。我们把 guideline 编译成一个可执行的
> **decision orchestration**：流程、合法性、拼装由代码确定地执行，模型只在规则无法决定的地方回答受约束的决定
> （结构化片段，或带概率的封闭问题）。然后**用几篇 gold 文档训练这个流程本身**——校准决定的阈值、按置信度路由、
> 用把错误归因到节点的反思去改写节点——而不训练任何模型权重。流程是显式的，所以每个错误都能定位到节点，每次学习
> 都是一条可读、实测过的 diff。

标题（候选，正文用第一个）：

- **Decision Orchestration: Learning Annotation Procedures from a Handful of Gold Documents**
- Train the Procedure, Not the Model: Few-Shot Decision Orchestration for Structured Annotation

强调的三点（对应用户要求）：

1. **少量数据**：冷启动场景，1–4 篇 gold 就能训练 orchestration，不需要大规模标注再训练模型；
2. **流程清晰、好 debug**：错误按节点归因、改动按节点局部化、组件可以单独替换做对照实验（换答题模型、换分词）；
3. **可校准**：判断模型给概率，阈值可以按实测校准，置信度可以决定什么时候问更强的模型（或人）。

## 3. 论点 → 证据

| 论点 | 证据（已有） | 还缺 |
|---|---|---|
| C1 把流程和决定分开，结构化标注就能交给小/便宜的模型，且输出格式由构造保证 | Qwen3.5-9B：单次生成 0 F，同模型走 orchestration 17.6 F（留出集 8 篇）；Microsoft-Decision-1（9B 判断模型）30.8 F；Jev 39.5 F；Qwen3.8-27B 42.4 F vs Sonnet 45.1（0001–0004）；doc 格式检查 ≈1.0 | 同一留出集上的 Sonnet / Qwen27；通用 agent harness 对照（E2） |
| C2 orchestration 可以只用几篇 gold 训练（不动权重） | 生成式：Sonnet 45.3→50.8→52.6（1、2 篇，测 0004+0005）；DeepSeek 自反思 30.8→36.0（2 篇）；判断式：J0 34.5→J2 38.9（2 篇，0005–0007），K0 39.5→K2 41.1（留出集） | 学习曲线 + 多种子（E3）；生成式和判断式在同一测试集上 |
| C3 判断模型的概率可以校准，并可用来路由 | 换判断模型后阈值失配：OpenAI Decisions 未校准 25.6 F，4 篇 gold 上坐标下降校准后 28.5 F（留出集 +2.9）；Jev 置信度 ≥0.9 时与 Sonnet 一致 95%，<0.7 时 57%；级联 τ=0.7 拿回 "全部 Sonnet 答" 增益的约 75%，调用 39%、成本 26% | 可靠性图/ECE（对 gold 推出的答案）；τ 扫描曲线；模拟人工（E4、E5） |
| C4 好 debug：错误可归因、改动可局部、组件可替换 | 按 skill 丢分表（0001：special_entity 149→33）；rsi-jev2 接受的 29 条改动里 rule 22 / options 4 / tool 1 / questions 1 / wording 1；第 3 轮 "反转前两轮" 的提案被实测拒绝；换答题模型（Sonnet 答同样的题 43.5 F 上限）、换分词（+1.5）、级联三个对照实验定位瓶颈 | 节点级消融（E7） |
| C5 边界 | 训练篇 +14～17、留出集 +1；第 4 轮留出集 −0.7（不是噪声：同版本重跑差 ≤0.6）；9B 反思者不稳（−1.4 F）；级联错误（"no predicted node" 200+ 分）；生成式每句约 $0.7 | 消融定位第 4 轮的有害改动（`ablate.py`） |
| C6 跨任务：同一套做法在第二个任务上也成立 | 无 | PARSEME 1.2（E9） |

## 4. 已有结果清单（全部 newdata gold，AnCast++，宏平均）

### 4.1 生成式决定节点（umr-tree，模型写受 schema 约束的 JSON 片段）

0004+0005（99 句；Sonnet 5.5 解析，Opus 5.5 反思；出处 `main:experiment/rsi-zh2`）：

| 系统 | 训练 gold | F | Modal | Temp | Coref | Comp |
|---|---|---|---|---|---|---|
| 单次调用（中文 + "UMR" + guideline 链接） | 0 | 32.7 | 7.4 | 0.0 | 0.0 | 27.7 |
| seed R0（手写） | 0 | 45.3 | 60.4 | 29.5 | 20.7 | 44.0 |
| R13 | 0001（51 句） | 50.8 | 61.1 | 39.3 | 23.3 | 49.4 |
| R23 | 0001–0002（111 句） | 52.6 | 60.0 | 43.6 | 25.5 | 51.2 |
| R32 | 0001–0003（142 句） | 52.6 | 61.9 | 42.9 | 22.5 | 51.1 |

0005–0007（157 句）：

| 系统 | 模型 | 训练 gold | F | Comp | 出处 |
|---|---|---|---|---|---|
| 单次调用 | Sonnet 5.5 | 0 | 29.4 | 24.9 | rsi-zh2 |
| seed R0 | DeepSeek V4.1 Flash | 0 | 30.8 | 29.0 | rsi-zh-deepseek |
| R42（DeepSeek 自己反思） | DeepSeek | 0001、0004 | 36.0 | 34.0 | rsi-zh-deepseek |
| seed J0（判断式，手调） | Jev | 0（规则手调时看过 0001–0003） | 34.5 | 33.8 | rsi-jev |
| J2 | Jev | 0001–0002 | 38.9 | 38.0 | rsi-jev |
| R32 | Sonnet 5.5 | 0001–0003 | 55.2 | 52.1 | rsi-zh2 |
| R42 | Sonnet 5.5 | 0001–0004（201 句） | 55.6 | 52.2 | rsi-zh2 |

缺：Sonnet seed R0 在 0006、0007 上没跑（只有 0005 = 51.0）。

训练篇（同一篇反思前后，Sonnet）：0001 40.3→59.6→66.9→70.9；0002 50.6（seed）→58.9（R13，没见过）→…→73.4；0003 49.7（seed）→57.5（R23，没见过）。
按 skill 丢分（0001，judge 数字还是旧 gold，待重算）：predicate 518→395，np_phrase 406→215，document 406→337，special_entity 149→33。
每轮问题 376–902 个（29–43% 文档级），每轮改 35–73 条，441 条只拒 1 条。

模型规模（seed，sentence F）：

| 模型 | 文档 | 单次生成 | 详细说明单次 | orchestration seed |
|---|---|---|---|---|
| Qwen3.5-9B | 留出集 8 篇（0015–0024） | 0.0 | 4.9 | 17.6 |
| Qwen3.5-9B | 21 篇（0008–0032） | 0.0 | 6.2 | 18.0 |
| Qwen3.8-27B | 0001–0004 | – | – | 42.4 |
| Sonnet 5.5 | 0001–0004 | – | – | 45.1 |
| DeepSeek V4.1 Flash | 0002（thinking 开/关） | – | – | 49.1 / 35.9 |

Qwen 自反思：27B 一轮 0001 上 39.3→50.4；9B 在新文档上平均 −1.4 F（前半 +0.6、后半 −3.0；seed 重跑噪声 2.3 F）。

### 4.2 判断式决定节点（kind: jev，只问封闭问题、返回概率、规则拼装）

留出集 0015–0018、0021–0024（138 句，任何反思和手调都没见过；出处 `zealous-hopper:experiment/rsi-jev2|openai-decision|microsoft-decision`，后两者本会话本地打分）：

| 判断模型 | 版本 | F | Modal | Temp | Coref | Comp |
|---|---|---|---|---|---|---|
| Jev（TypeSafe） | K0 = J2 | 39.5 | 60.8 | 20.5 | 5.0 | 38.4 |
| Jev | K1（+0008） | 40.5 | 61.4 | 20.7 | 6.8 | 39.2 |
| Jev | K2（+0009） | **41.1** | 61.6 | 21.2 | 8.3 | **39.8** |
| Jev | K3（+0010） | 40.9 | 63.3 | 20.7 | 8.6 | 39.8 |
| Jev | K4（+0011，跨文档诊断） | 40.1 | 62.6 | 20.2 | 8.4 | 39.2 |
| OpenAI Decisions（gpt-6-luna） | K0（阈值是给 Jev 定的） | 25.6 | 52.2 | 15.9 | 6.9 | 27.0 |
| OpenAI Decisions | K0t（4 篇 gold 上校准阈值） | 28.5 | 56.5 | 17.4 | 7.1 | 29.6 |
| Microsoft-Decision-1（Qwen3.5-9B 后训练） | K0（未校准） | 30.8 | 56.1 | 17.8 | 9.5 | 31.6 |
| 参照：Qwen3.5-9B 生成式 orchestration seed | R0 | 17.6 | | | | |

rsi-jev（盲改，J0→J1→J2，0004–0012 未见文档）：35.4→37.8→39.2 F，10 篇未见文档里 9 篇变好。
rsi-jev2（实测式）：每轮试 12 条，接受 8/7/8/6；训练篇 40.0→54.1、43.4→60.2、41.4→45.9、37.5→41.6；
一轮 35–60 分钟，Jev 36,816 次请求（公开价约 $8），Opus 每轮 36–82 次调用。

校准（OpenAI Decisions，目标 = 4 篇 (F+Comp)/2）：29.0 →（ONE_VERB_IF 0.6→0.7）30.5 →（外部论元下限 0.4/0.6→0.3/0.5）30.8；
其余 7 个阈值扫描都在 ±0.05 内（说明收益集中在少数结构性阈值上）。

诊断（J2，0010+0012）：同样的题换 Sonnet 答 43.5 F（Jev 39.1）；按 gold 分词 +1.5；级联（Jev 置信度 <0.7 的题给 Sonnet）
42.4 F，504 次调用约 $9，而全部 Sonnet 1,292 次约 $34。Jev 与 Sonnet 一致率：置信度 ≥0.9 95%（占 53%），0.7–0.9 79%（26%），<0.7 57%（21%）。
成本：Jev 测 216 句约 $0.64（每句约 35 次请求、100 个问题），Sonnet 生成式每句约 $0.7。

### 4.3 第二个 benchmark 的现状（`bold-curie` 分支，进行中）

- TempEval-3（TimeML，platinum 20 篇，官方 scorer）：目前跑的是 **critique 式**（B 篇的方法），seed R0 timex strict 81.1 /
  event 74.5 / TLINK 37.9，零样本单次调用 B-zero 85.4 / 80.7 / 39.8，2013 年最好 TIPSem TLINK 42.4、UTTime（gold 实体）56.5。
  **还没有 orchestration 版本**——这正是本文要补的（见 E9）。
- Manifesto（CMP 8 个 domain 的句子分类）：分类任务，流程性弱，不适合作为本文的第二个 benchmark（更适合 B 篇或附录）。

## 5. 论文结构（ACL long，8 页正文）

1. Introduction（1.25 页）：冷启动问题 → 两种范式的不足（训模型要数据；通用 LLM/agent 不可控、不可调试、只有最强模型撑得住）
   → 观察：guideline 本身是流程，只有少数点要判断 → decision orchestration → 训练流程而非权重（校准、路由、反思）→ 结果 → 贡献。
2. Related Work（0.75 页）：LLM 作标注者与人机协同；把 guideline 给模型（GoLLIE、guideline learning）；LM 程序、工作流与结构化输出；
   提示/程序/工作流的自动优化与自我改进；错误驱动的规则学习与弱监督；校准、级联与选择性预测；UMR/AMR 解析。
3. Decision Orchestration（1.5 页）：问题设定（ontology、guideline、几篇 gold、评测器）；skill、registry、wave；规则节点与两种决定节点
   （生成式片段 / 封闭问题 + 概率 + 规则拼装）；执行轨迹与按节点归因。
4. Learning the Procedure from a Handful of Documents（1.5 页）：目标与数据划分（train / regression / dev）；4.1 阈值校准；
   4.2 按置信度路由（级联，人工路由）；4.3 反思：find → attribute → propose → edit →（实测）trial → accept/retry；改动类型；防泄漏、防回归、噪声边界；
   两种机制（生成式：解析贵、不实测；判断式：解析便宜、每条实测）。
5. Experimental Setup（0.75 页）：中文 UMR；划分；模型；基线；指标；第二个 benchmark（PARSEME 1.2）。
6. Results（1.5 页）：主表；模型规模与判断模型；从几篇文档学习；校准；路由；PARSEME【待补】。
7. Analysis（1 页）：可调试性（丢分归因、改动类型、对照实验）；为什么留出集收益比训练篇小一个量级；成本；弱反思者。
8. Conclusion；Limitations；Ethics。
附录：细粒度 judge 定义；训练轨迹与按 skill 丢分；校准扫描；节点表与 skill 例子；反思提示词（待写）；PARSEME 的流程设计；待做实验清单。

## 6. 还要做的实验（论文里用 \todo 留空的地方）

按优先级。**P0 = 投稿前必须有。**

| 编号 | 实验 | 为什么 | 怎么做 / 成本估计 |
|---|---|---|---|
| E1 (P0) | **统一协议**：一个 gold（newdata）、一个留出集（0015–0018、0021–0024，138 句）、一个 dev 集（0027–0029 + 0030、0031、0033）、训练池 0001–0014 | 现在三套测试集，主表拼不起来 | 在留出集上补：Sonnet R0、R42；Qwen27 R0；DeepSeek R0/R42；单次调用；约 $100×2（Sonnet） |
| E2 (P0) | **更强的基线** | 只和 "单次调用" 比太弱，审稿人会问 | (a) 单次调用 + 完整说明 + 从训练文档取的 k 个 gold 例子（同样的数据量）；(b) 通用 agent harness（ReAct/Claude Code 式：给 guideline、PropBank 工具，自由规划）——比 F、调用数、成本、格式合法率；(c) Chun & Xue (2024) 的 pipeline 在同一文档上的输出（向作者要，见 `docs/next-steps.txt`）；(d) 若有：用全部 UMR 2.0 中文训练的监督 parser |
| E3 (P0) | **学习曲线 + 方差**：0/1/2/4/8 篇 gold，3 种文档顺序 | "少量数据就够" 是主线，需要曲线和误差棒 | 判断式便宜（每轮约 1 小时、几美元）：rsi-jev2 跑 3 个顺序；生成式至少 1 个顺序到 4 篇 |
| E4 (P0) | **校准本身** | 用户要求写清 "怎么用 Jev 做 calibration" | (a) 从 gold 推出封闭问题的正确答案（sent_type、义项、实体类型、同指是否、时间方向），画 reliability diagram、算 ECE，Jev / OpenAI / Microsoft 三个判断模型；(b) Microsoft-Decision-1 跑 `run.sh calibrate` 再测留出集；(c) 用 1/2/4 篇校准的差别；(d) Jev 的阈值迁移到别的模型、反过来 |
| E5 (P0) | **按置信度路由的曲线** | 把 calibration 变成 "标注冷启动" 的实用结论：只有不确定的决定需要问强模型或人 | τ ∈ {0.5,…,0.9}：留出集 F vs 升级比例 vs 成本；升级目标 = Sonnet；再加 "模拟人工"（升级题用 gold 推出的答案回答）→ "人工回答 N 个封闭问题能把 F 提到多少"，对比人工从头标的工作量 |
| E6 (P0) | **把实测式 RSI 跑完** | 现在停在 K4，第 4 轮留出集 −0.7 原因未明 | 充值后 `ablate.py` 定位有害改动；dev 扩到 6 篇；第 5–7 轮；同一流程在 OpenAI / Microsoft 判断模型上各跑 3 轮（看流程学习能否跨判断模型） |
| E7 (P1) | **orchestration 消融** | 支撑 "规则节点 / 片段拼装 / 工具" 的设计 | 去掉 coverage、reentrancy 规则；让模型写整张 PENMAN（合法率、F）；去掉 PropBank 工具；判断式里把规则拼装换成让 LLM 自由生成 |
| E8 (P1) | **RSI 消融** | 说明哪些反思设计必要 | 只允许改措辞 vs 允许改规则/选项/结构；不实测（盲改）vs 实测；只在训练篇上实测 vs 训练+回归+dev；随机接受对照 |
| E9 (P0) | **第二个 benchmark：PARSEME 1.2 动词性多词表达识别（中文 + 一种别的语系语言）** | 证明不是 UMR 专用 | 设计见论文附录 F：候选（规则：依存树上动词 + 依存的组合，按类别模式；训练集里见过的按词元匹配）→ guideline 的每个测试变成一个是非题，guideline 的决策树变成代码 → 拼 span 和类别（规则）→ 阈值校准、实测式反思。冷启动模拟：从训练集抽 100 句一份的 "文档"，学 1/2/4 份；官方 dev 做度量，官方 test 只测一次。指标：官方 MWE-based / token-based P/R/F 和 unseen MWE F。对比：两条规则基线（中文 unseen 27.3）、1.2 官方结果（中文 unseen 最好 60.2，14 种语言平均 unseen 最好 38.5）、单次 LLM 调用（零样本 / 同样的训练句作例子）、fragment 版。数据 CC 许可、免费下载 |
| E10 (P2) | 英文 UMR | 跨语言同一任务 | `olddata/gold/en`；只需换 skill 的语言部分 |
| E11 (P1) | 成本与调用统计表 | 每个配置：每句调用数、token、美元、墙钟 | 从 `calls.jsonl` / `usage.json` 汇总 |
| E12 (P2) | 人工标注时间对照 | "冷启动" 的实际意义 | 引用 UMR 标注成本文献，或请标注员计时修正 orchestration 输出 vs 从头标 |

## 7. 第二个 benchmark：建议

**主推 PARSEME 1.2（动词性多词表达识别），TempEval-3 作为备选。** 调研过程和每个候选的数字见 `extra/notes/benchmark-survey.md`。

为什么是 PARSEME：
1. **guideline 本身就是决策树。** PARSEME 的标注指南把每个类别（VID、LVC.full/cause、IRV、VPC.full/semi、MVC、IAV）写成一串语言学测试组成的决策树（1.2 还专门给中文的 MVC 加了一棵决策树）。编译成本文的 orchestration 几乎是一对一：候选生成和训练集匹配是规则，每个测试是一个封闭问题，决策树是代码。这是 "guideline 就是流程" 最直接的证据。
2. **低数据、看 unseen。** 1.2 的测试集刻意包含每种语言约 300 个训练里没见过的表达；最好的系统在 unseen 上只有 38.5 F1（14 种语言平均；全部表达 70.1）——正是 "从几篇文档学流程" 该发力的地方。中文 unseen 最好 60.2，两条规则就有 27.3，说明中文的规则部分多，适合我们的分工。
3. **免费、有官方 scorer、有中文**（和 UMR 实验保持同一语言）。2.0 版（MWE 2026）扩展到所有句法类别、17 种语言，相当于一次 schema 修订，可以再做一个 "新 schema 冷启动" 的实验；调研里读到的 2.0 LLM 结果（基线 23.25、Qwen3-32B 指令微调 28.40，监督最好 57.29）还需要我们自己再核对原文后再写进论文。
4. 工程量：句子级，`.cupt` 是 CoNLL-U 加一列，读写和官方 `evaluate.py` 都现成，1–2 周可完成。

为什么 TempEval-3 退居备选：
- `bold-curie` 分支已经有完整的基础设施（reader/writer/官方 scorer/2013 系统重打分）和 critique 式的跑数，但 LLM 零样本单次调用在 timex 上已经超过 2013 年的系统（strict 85.4 vs 最好 82.7），event 接近（80.7 vs TIPSem 82.9），只有 TLINK（39.8 vs 42.4）还有空间，"few-shot 程序化" 的优势不如 PARSEME 明显；而且只有英文。
- 如果时间紧，TempEval-3 的 orchestration 版（timex 候选→类型 choice→值归一化规则；event 候选→class choice；TLINK 候选对→关系 choice→闭包规则）可以复用现有代码，作为第三个任务放附录。

Manifesto（`bold-curie`）是 8 类句子分类，流程性弱、无标准测试集，不适合本文。
## 8. 写作约定

- 正文英文，ACL 2026 模板，`\usepackage[review]{acl}`；8 页正文 + Limitations + Ethics + 参考文献 + 附录。
- 未完成的实验：表格里用 `\tbd`（红色 "--"），段落里用 `\todo{...}`（红色），并在本文件第 6 节有编号对应。
- 不写任何模型以外的 API key、内部路径；引用 Jev / Decisions API / Microsoft-Decision-1 时只引公开文档。
- 定稿前把 `\todo` 全部清掉；`\tbd` 的表格行要么填上，要么删掉。

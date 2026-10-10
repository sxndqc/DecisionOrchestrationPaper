# 第二个 benchmark 的调研

写于 2026-10-10。要找的是：除了 UMR，还有哪个任务能证明 decision orchestration 的做法通用。

## 标准（按重要性）

1. guideline 公开、详细，是多步骤的流程：有确定的步骤，也有要判断的步骤；标签集合封闭；
2. gold 免费下载（不要 LDC），有标准 scorer；
3. 有监督的 SOTA 可比，最好也有明显更差的 LLM 零样本/少样本结果；
4. "少量数据" 的故事自然：新 schema、低资源语言、专门领域；
5. 1–2 周能做完。

## 分支里已经有的

- `claude/bold-curie-nle80f`：**TempEval-3（TimeML）**、**Manifesto**（CMP 编码，8 个 domain），都用 critique 式（B 篇方法）在跑；
  TimeML 有完整的 reader/writer、官方 scorer、2013 系统重打分（`experiment/timeml/SOTA.md` 是文献核对）。

## 候选（数字都是调研时在原文里读到的；标 ✓ 的本会话另外核对过原文）

| 候选 | 许可 / 规模 | 指标 | 监督最好 | LLM | 评价 |
|---|---|---|---|---|---|
| **PARSEME 1.2** 动词性多词表达识别（14 种语言含中文） | CC，hdl.handle.net/11234/1-3367；每种语言测试集约 300 个 unseen VMWE ✓ | 官方 MWE/token P/R/F，unseen F | MTLB-STRUCT：全部 70.1、unseen 38.5（14 语言平均）✓；中文 unseen 最好 60.19（TRAVIS-mono），两条规则基线 27.33 ✓（Ramisch et al. 2020, aclanthology.org/2020.mwe-1.14） | 1.2 没有 LLM | **最合适**：guideline 就是测试组成的决策树（1.2 还有中文 MVC 专用决策树 ✓） |
| PARSEME 2.0（17 种语言，所有句法类别） | Codabench 永久副本，测试 gold 不公开 | 同上 | MTLB-STRUCT 57.29 | 基线（gpt-oss）23.25；MorphoFiltered-Gemini 17.14；IPN（Qwen3-32B 指令微调）28.40（Scholivet et al., MWE 2026, aclanthology.org/2026.mwe-1.33；论文存在 ✓，数字未再核） | schema 修订后的 "冷启动" 实验 |
| FrameNet 1.7 | CC BY 3.0（NLTK）；测试 1,247 句 | 框架识别 acc、论元 F1 | 论元识别 KAF-SPA 0.813；微调 Qwen2.5-72B 0.794 | GPT-4o 带例子 0.592（Devasier et al., EMNLP 2025）；框架识别 Llama-3.1-8B few-shot 83.5 vs 监督 92.6 | 合适的备选，但训练数据多，低数据场景要自己构造 |
| TempEval-3 | 免费；platinum 20 篇 | 官方 scorer | timex value 77.61（HeidelTime）；event 81.05（ATT-1）；端到端时间感知 30.98（ClearTK-2）；TLINK（我们的 scorer）TIPSem 42.4 | 我们自己跑的零样本 B-zero：timex strict 85.4、event 80.7、TLINK 39.8 | 基础设施现成；但 LLM 在 timex/event 上已接近或超过 2013 系统，只剩 TLINK 有空间；只有英文 |
| MAVEN-ERE | GPL-3.0；测试 857 篇，标签隐藏 | CodaLab | RoBERTa：时间 55.8、因果 31.6、子事件 27.2、同指 MUC 81.7 | GPT-3.5：12.3 / 5.3 / 2.1 / 23.2 | 没有独立公开的流程式 guideline，和 TempEval 重叠 |
| DISRPT 2025 | 39 个数据集 16 种语言 | 统一 17 标签 | 最好 71.19% | 零/少样本提示 "underperform" | 各数据集框架不同，没有一份 guideline |
| Universal Dependencies（低资源树库） | 免费，CoNLL-2018 scorer | LAS | Biaffine 91.82 | ChatGPT 零样本 31.78（12 种语言） | guideline 定义关系而非给流程；完整句法树工程量大 |
| Manifesto | 需注册、不可再分发、无官方划分 | 无标准 | ManifestoBERTa acc .57 / macro-F1 .45（56 类） | Mistral-7B 零样本 micro-F1 .14（142 类） | 不是标准 benchmark |
| 英文 UMR 2.0 | CC BY-SA 4.0 | AnCast | – | – | 同一任务换语言，证明不了通用性 |

排除：CoNLL-2012/OntoNotes、THYME/i2b2（需要 LDC 或数据使用协议）；SpaceEval（找不到下载）；MASSIVE（没有流程式 guideline）；
DocRED、CrossRE（schema 只是关系类型列表）。

## 结论

- **主推 PARSEME 1.2**，中文 + 一种别的语系语言（法语或波兰语，待定）。理由见 `PLAN.md` 第 7 节；流程设计见论文附录 F。
- **备选 TempEval-3**：基础设施现成，时间紧时可做 orchestration 版放附录。
- 2.0 版可做 "schema 修订后冷启动" 的追加实验。

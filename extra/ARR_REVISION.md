# ARR 模拟评审后的修订

本轮为作者授权的 AI 模拟评审与作者侧修改，不是正式 ARR 评审。三位评审分别关注方法统计、理论贡献与表达、复现与证据。规范来自 ACL 官方站点源码 `acl-org/aclrollingreview`，commit `45188b86f0827fa8cb78ad64c2dd48337f37fbb9`；官网部署状态未验证，旧指南尚待 October 2026 制度对应更新。

## 已修改

- 说明 seed guideline/registry 是手工编码，后续 supervised reflection 修改 inference-time artifacts，不是自动 compiler 或模型权重训练。
- 明确 typed emits 会影响树形与调用数，code 限制合法调度，并不使调用数与模型回答无关。
- 将输出 producer provenance 与 upstream cause / repair target 区分；删去异测试集 43.5 vs 45.3 导出的瓶颈结论。
- 校准改为 task-level threshold tuning，不再说 teacher agreement 是 gold correctness 或 probability calibration。
- 摘要同时列 minimal 0 与 detailed 4.9 基线；75% gain/26% cost 明确只来自20句 routing pilot。
- 自动反思数据与手调 seed exposure 分开：J0/J2/K0 已见3篇142句，K2累计5篇162句，K4累计7篇199句；开发选择另有3篇47句。
- 披露多次 dev score selection 和已查看的 H trajectory；不得据 H 选择最终版本后仍声称 H 未见。
- 当前 gold 未重算的 judge counts、旧 format 分数改成待填；随附 JSON 缺 K1/K2 H scores，相关表格留空 E13，不断言结果虚假。
- 其余 closed trial 日志摘要明确标为历史记录，原始 artifacts/scorer 待 E13 核验；主表有 JSON 支持的结果保留。
- 补 E13 证据 audit 和 reproduction status；注明其他分支预测、scorelib 缺失、main scorer 的已知失败路径，不改实验代码来掩盖问题。
- 收紧单配置9B失败、noise、acceptance policy 与泛化的强断言；披露数据/许可待核验与 AI 编辑协助。
- 明确与 companion Harness 论文的共享材料和贡献边界，并压缩重复叙述以控制正文8页。

## 实验继续留空

| 优先级 | 项目 | 待填结果 |
|---|---|---|
| 核心 | E1 统一 gold 与冻结共同测试；E2 同信息强基线 | |
| 稳健性 | E3 重复运行/顺序 | |
| 离线核验 | E13 current-gold judge、K1/K2来源、scorer/参数/guard audit | |
| 主张相关 | E4 真实正确性校准、E5 共同 H routing、E6/E8 接受策略干预 | |
| 扩展 | E7/E9/E10/E11/E12 | |

全部 E1–E13 在论文附录仍保留。PARSEME、真实人类标注/纠错时间未执行，不填写推测结果。

## 后续实验与泛化问题

本论文的[详细实验计划](https://github.com/sxndqc/SkillParseUMR/blob/main/docs/experiments-decision-orchestration.md)独立维护。用户指定 PARSEME 的闭合 seed/适应版使用 Jev，反思使用 Opus；加入同候选/组装的 Jev 直接分类对照。Sonnet 生成式对照及可选 routing 单列，跨模型差异不归因于程序形态。附录明确新增模型配置尚未执行。

导师提出的“反思是否有效、修改是否泛化、怎样引导泛化”需要分开回答：现有早期未测量反思有 held-out 改善，后续 measured reflection 的训练收益大于 H 收益，且 K4 有回退；单次运行不支持稳定泛化结论。附录列出待做的跨文档反思筛选：基于重复错误提出规则，在未参与该提议诊断的文档上测量，用相同 seed/gold/builder/预算比较 seed、当前协议和跨文档筛选协议。此项是计划，不是已实现方法或已取得结果。

## 验证

- 64 项原仓库离线测试通过；未请求模型 API 或补跑实验。
- 随附 JSON 的 T1 R0/R23、H K0/K3/K4 宏平均核对一致；未声称全部结果已经独立复算。
- pdfLaTeX/BibTeX/latexmk 编译成功，Conclusion 在第8页内；Limitations、伦理、参考文献和附录按 ACL 格式保留。
- 生成输出在 checkout 外；用户可在本地/Overleaf 以 `main.tex` 编译。已保存 cloud 启动/安装步骤供复用。

参考：[Reviewer guidelines](https://aclrollingreview.org/reviewerguidelines)、[Review form](https://aclrollingreview.org/reviewform)、[Author checklist](https://aclrollingreview.org/authorchecklist)。当前版本是保留实验空位的修订稿，不能据编译成功称已满足投稿实证要求。

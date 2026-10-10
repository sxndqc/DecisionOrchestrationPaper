# Annotation Guidelines as Skill Orchestration

Current guideline is book-style; to better harness AI's ability, we propose to organize skills (input, heristics?, examples?, output) 但最好只说面向AI的guideline和面向人的不一样。

怎么样把guideline翻译？

## Introduction

为执行或分析特定任务，通常需要设计专用的ontology，用于更好地控制，比如意图识别、intent分类，等等。
传统来说，要产生这样的数据，需要大量人员根据guideline标注，当生产了大量数据之后，再或许根据数据进行训练。
初始数据生产非常依赖人工，而且慢。

这种Ontology生产，通常有两方面：一方面是识别数据中的结构，另一方面是把结构映射到ontology上面。
给定当今通用大模型的Instruction following能力，我们可以利用这一点来自动识别数据结构；但是，ontology标签和specification本身，属于外部知识，而不可能大模型内生知道这些内容。

Agent？

然而，相对于编程任务，Ontology标注的流程相对更明确，程式化的内容更多，只有少量明确部分是需要Agent来做决定的。
因此，我们可以用一种更轻量化的Harness，相对于编程harness更结构化、明确化，来进行Ontology标注。

我们提出Skill Orchestration，提出一种新的guideline写法，把Skill作为Node，而由Agent来决定步骤。

（1）可解释性、debuggable
（2）格式保证正确
（3）只要skill好，小模型可做

## Related Work

规则学习/heuristic learning:
1995年的规则学习


今年来的acl 2026几篇


===============
## Methodology

3.1 Skill Orchestration System Design & Interface

3.2 Neverending Skill Improvement and Heuristic Learning

如果人工来加东西，那可能变成上千条规则，这样不好，最好自动加。


## Experiment

4.1 UMR task: Fine-grained Score

4.2 Case Study: how they improve, what's still missing?

【找问题的模块，怎样定位问题，怎样从trace里面找到问题】
【反思的模块，改增删】




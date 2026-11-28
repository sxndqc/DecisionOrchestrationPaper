# Author response — Submission 12193

Marks in this draft (remove before posting):
`[PENDING n]` = waits for experiment n of `todo.md`; `[AUTHOR]` = to be filled in or checked by the authors.
Every other number is measured.

Layout: one response per reviewer. Each point is *the reviewer's concern* → **our answer** → the numbers.
Five tables are used by more than one reviewer; they are given once, as T1–T5, at the end
("Tables shared by the responses") and would be pasted into each response that cites them.

---

# Response to Reviewer 6SVz

### 1. "Seeds are written by the authors … the benefit could partly reflect skilled human authoring … the authoring effort is not measured."

**Answer.** Writing a seed is mostly mechanical, and we now separate its effect from the effect of the method.

- *How a seed is made.* The guidelines are already organised by decision (UMR: one chapter per attribute or
  relation; PARSEME: a decision tree per category). An LLM splits the guideline into one instruction file per
  decision; an author checks each file against the guideline and writes the rule nodes (output format, label
  inventories, candidate extraction). No example and no gold annotation is used.
- *Time.* About [AUTHOR: N] person-hours for UMR and [AUTHOR: N] for PARSEME, by
  [AUTHOR: who; prior experience with the scheme?].
- *Authoring vs. method.* We gave the same model (Claude Haiku 5.5) the seed's instruction texts in one prompt,
  without the procedure. If the benefit were only good authoring, this would score like the procedure. It does
  not (table T3, UMR zh / en): seed texts in one prompt 10.4 / 26.2; the same texts run as a procedure
  20.9 / 28.8; after reflection 33.2 / 32.6.
- *Why a seed cannot be perfect.* Gold annotations follow conventions the guideline does not state (two golds
  of our Chinese UMR test sentences agree with each other at only 70.2 juːmæʧ). Reflection exists to close this gap.

### 2. "Test imperfect initial seeds and measure how much performance reflection can recover."

**Answer.** We have this comparison with a naturally imperfect seed. After submission we audited the seeds
against the guidelines and found real defects (for UMR: a crude English lemmatizer, an option list shorter than
the guideline's, the temporal parent fixed by a rule instead of decided; for PARSEME: an idiom test that
accepted almost everything, candidates not marked in the question). We ran reflection from both seeds
(table T2, UMR on the whole test set, Jev 1.13):

| | seed as submitted | audited seed |
|---|---|---|
| Chinese, V0 | 32.7 | 34.5 |
| Chinese, V10 | 37.0 | 36.6 |
| English, V0 | 29.6 | 32.6 |
| English, V10 | 31.5 | 32.8 |

In Chinese, reflection fully recovers what the defective seed loses (both end at about 37). In English it
recovers two thirds: the remaining gap is the lemmatizer, a defect of rule-node code that ten rounds of
reflection did not rewrite. We will report this as the limit of what reflection recovers: conventions and
option texts yes, missing tooling no. For PARSEME see T4 (English: 8.4 → 34.1 from the submitted seed,
31.2 → 43.3 from the audited one, so there the defects were not fully recovered).

### 3. "Non-monotonic / model-dependent behavior … does the tuned procedure transfer to a new model or new data?"

**Answer: it transfers to another model and to new data; the unstable runs are all of one kind.**

- *New model.* The procedure reflected with Jev 1.13, answered by Microsoft-Decision-1 with no further
  reflection, on the whole UMR test set: 34.9 (zh) / 32.4 (en), against 35.2 / 32.2 for the procedure reflected
  with Microsoft-Decision-1 itself. A procedure tuned with one decider works as well with another. (For PARSEME
  the thresholds must be recalibrated for the new decider; without that, transfer loses 13 F in Chinese.)
- *New data.* All procedures were tested again on the complete test sets, 2.4 times (UMR zh) and 35–40 times
  (PARSEME) larger than the samples of the submission; the gains remain (T2, T4).
- *Unstable runs.* In the submission all 12 closed-mode runs improve; the runs that do not are fragment-mode
  runs, where an edit is accepted without being measured. We add one honest negative: on the complete English
  UMR test set the closed procedures' gain from reflection is within run-to-run variation (T2), so for English
  UMR we claim the level reached, not a gain from reflection.

### 4. "Domain generality is asserted beyond evidence … fuzzy, highly-recursive annotation."

**Answer.** We agree and will limit the claim to the two tasks studied.
[AUTHOR: decide whether to report the RST experiment. We ran the same protocol on RST parsing of GCDT's five
test documents (top-down recursive splitting with closed decisions). Result: procedure Full F1 21.3 → 25.8 after
reflection, against 58.3 for GPT-6.1-sol with the whole guideline in one call per document (second human
annotator: 56.1). It shows a limit of the method, not its generality. Suggested text if reported: "A first
experiment on RST parsing shows the limit: there the large model with the whole guideline is at human agreement
and our procedure is 30 points below it; decisions that need the whole document do not decompose well. We
report this in Limitations."]

### 5. "Report UMR with an official/standard scorer alongside juːmæʧ."

**Answer.** juːmæʧ *is* the official scorer of the UMR parsing shared task whose data we use; we will say so at
first mention. We also add AnCast++ (on the test sample of the submission):

| AnCast (sentence level) | UMR zh, V0 → V10 | UMR en, V0 → V10 |
|---|---|---|
| Haiku 5.5 | 21.4 → 42.2 | 31.1 → 37.5 |
| Jev 1.13 | 32.8 → 37.1 | 28.1 → 29.0 |
| GPT-6.1-sol + whole guideline | 44.8 | 45.8 |

Reflection improves the procedures under both scorers. The comparison with the large-model baseline does not
carry over: under AnCast the baseline is above our procedures. [AUTHOR: check the cause before posting; our
hypothesis is that juːmæʧ also scores the alignment of nodes to tokens, which the baseline gets wrong, and
AnCast does not.] We will report both scorers and this difference.

### 6. "Add controlled comparisons against prompt-compilation baselines (e.g. DSPy)."

**Answer.** Done, with DSPy's GEPA optimiser, and the result changes what we claim (table T5). The single-call
annotator (Claude Sonnet 5.5 with the whole guideline, one call per document) had its instruction optimised by
GEPA on the same 50 gold sentences. On the whole UMR test set it goes from 24.0 to 37.6 in Chinese and from
31.0 to 39.5 in English. Our best procedures reach 36.6 / 32.8 (Jev alone) and 38.0 / 34.6 (Jev with a cascade to
GPT-6-luna). So with the same gold, a prompt-optimised large model is level with our procedures in Chinese
and 5 points above them in English. We will state this plainly and change the claim: the contribution is not
higher accuracy than an optimised large model, but (i) comparable accuracy in Chinese and above the shared
task's best system in both languages with decision models that cost one to two orders of magnitude less per
document ($0.7 against roughly $15–20 at list price for the Chinese test set), (ii) decisions that are logged
and locally revisable, and (iii) a procedure that transfers between decision models. GEPA's optimised
instruction also grows to 17–19k characters and quotes training-specific items; on English PARSEME it overfits
(57.9 → 51.4 on test while 67 → 91 on train).

---

# Response to Reviewer 9J4c

### W1. "A baseline with the same gold data or prompt optimization would make the comparison more convincing. The UMR SOTA comparison also uses different evaluation settings."

**Answer.** Both are now done under the same conditions, and we report the outcome whichever way it points.

- *Prompt optimisation with the same gold* (T5): GEPA on the single-call annotator with the same 50 sentences
  lifts it to 37.6 (zh) / 39.5 (en) on the whole UMR test set, against 36.6 / 32.8 for our best procedure and
  38.0 / 34.6 with a cascade. Equal supervision removes the accuracy advantage in Chinese and reverses it in
  English; see our answer to Reviewer 6SVz, point 6, for how the claim changes.
- *UMR SOTA on identical data* (T2): every Chinese and English document of the shared task's test set, parsed
  whole and scored against the released test gold with the official scorer, the participating systems' released
  outputs scored the same way. Best shared-task system 36.4 (zh) / 27.3 (en); ours 36.6–38.0 / 32.8–34.6.

### W2. "The test sets are small, with no repeated runs or confidence intervals. Some improvements are only a few F1 points."

**Answer.** Three additions.

- *Complete test sets* (T2, T4): UMR 236 Chinese and 95 English sentences as whole documents; PARSEME 3,462 and
  3,965 sentences.
- *Repeated runs* (T2, T4): every V0 and V10 test of the closed procedures was run three times without the
  answer cache. Spread: at most 0.2 F in Chinese UMR and 0.7 F in English UMR; at most 0.9 F in PARSEME.
- *Confidence intervals* on the samples of the submission (T1): of the 16 runs (4 task–language pairs × 4 models),
  12 have a gain whose 95% interval lies entirely above zero; for the other 4 we claim no improvement.

What this shows: the Chinese UMR gain (+2 to +4) and all PARSEME gains are far outside the run-to-run spread; the
English UMR gain is not, on the complete test set, and we will say so.

### W3. "It is difficult to separate the effects of decomposition, reflection, and engineering effort."

**Answer.** Table T3 separates them with one model. For UMR each step adds: condensed instructions instead of the
whole guideline (zh +2, en +10), running them as a procedure (+10, +3), reflection (+12, +4). For PARSEME in
fragment mode the pattern does not hold, and we will say so. Engineering effort is isolated by the two seeds in
our answer to Reviewer 6SVz, point 2: a better-engineered seed starts 2–3 points higher on UMR and ends where
the first one ends in Chinese.

### W4. "Reflection uses Claude Sonnet 5.5, and the framework requires task-specific code … development cost is not evaluated."

**Answer.** Each scheme needs a procedure designed from its guideline; that is the intended workflow, and we will
report its cost.

- Model cost: parsing the whole Chinese UMR test set costs $0.7 with Jev 1.13 and $1.7 with the cascade; the
  reflector for all chains of the submission together costs $29 at list price.
- Human cost: authoring time as in our answer to Reviewer 6SVz, point 1.
- Task-specific parts: instruction files, rule nodes, and the list of units the judge compares. Shared between
  UMR and PARSEME: the execution, the trace, and the reflection loop.

### C1. "Table 3 labels Sonnet 5.5 results as V10."

**Answer.** The labels are wrong; thank you. The Sonnet rows are V2 (UMR, on 5 of the 20 chunks) and V3
(PARSEME); the GPT-6-luna UMR row is V2 on the same 5 chunks. We relabel them, mark the subset, and no longer
bold the English UMR 42.5, which is on that subset.

### C2. "The 'first work' claim … Chun and Xue (2024)."

**Answer.** We will cite it there and narrow the claim. Chun and Xue chain trained parsers and converters; the
steps are system components, not the guideline's decisions, and nothing is revised from annotations. Our claim
becomes: the first to compile the guideline itself into a decision procedure revised by reflection, without training.

### C3. Typos.

**Answer.** Fixed ("for decision thresholds", "code (Zelikman…)", "uses code"). In the Limitations the numbers
are the ranges 95–100 and 57–59 sentences; the symbol was lost in typesetting.

---

# Response to Reviewer y4Vj

### 1. "The abstract claims the framework outperforms larger models … on English PARSEME the baseline scores 75.6 and beats the best reflected procedure at 58.2."

**Answer.** Yes, we will correct it. The abstract will claim only what T2, T4 and T5 support: on UMR the
procedures are above the shared task's best system and above the un-tuned large-model baseline; a
prompt-optimised large model is level (Chinese) or better (English); on English PARSEME the large model
remains better.

### 2. "The baseline uses a single zero-shot prompt without tuning. Did you try prompt-tuning or few-shot examples?"

**Answer.** We now did, with DSPy's GEPA and the same 50 gold sentences (T5), and the reviewer's concern is
confirmed: tuning lifts the single-call annotator from 24.0 to 37.6 (zh) and from 31.0 to 39.5 (en) on the whole
UMR test set, level with our best procedure in Chinese and above it in English. The claim that structure beats a
larger model holds only against the un-tuned prompt; we will restate the contribution as cost, inspectability
and transfer at comparable accuracy (answer to Reviewer 6SVz, point 6).
[PENDING 1: the same test with GPT-6.1-sol, the paper's baseline model, as the single-call annotator.]

### 3. "The SOTA comparisons use mismatched data … How does comparing sentence chunks against whole documents affect the UMR SOTA comparison?"

**Answer.** It made the scores incomparable, so we removed that comparison and replaced it.

- *Why incomparable.* A five-sentence chunk loses the document-level relations (coreference, temporal, modal)
  that cross its boundary.
- *UMR, now whole documents on both sides* (T2): 36.6–38.0 (ours) vs 36.4 (best system) in Chinese; 32.8–34.6 vs
  27.3 in English. On the same documents our own chunk-wise and whole-document scores differ by about one point.
- *PARSEME, now the full test file* (T4). Scores are lower than on our sample because the sample has 50
  sentences with and 50 without an expression, whereas in the full file only 18% (zh) and 11% (en) of sentences
  contain one. The full file becomes the main PARSEME number.

### 4. "The paper does not quantify the human time and expertise required."

**Answer.** About [AUTHOR: N] person-hours per task; the process is described in our answer to Reviewer 6SVz, point 1.

### 5. "Deterministic rule nodes limit recall … the model cannot recover the missed expression."

**Answer.** True, and our added experiments quantify it. Reflection may edit rule-node code, and in the submitted
PARSEME runs it changed the candidate rules 2–6 times per run. But it does not rebuild a weak rule node: the
candidate rules of the submitted seed proposed 69% (en) and 74% (zh) of the training file's expressions; a
rewrite by hand against the guideline raises this to 88% and 82%, and V0 on the full English test set from 8.4
to 31.2 (T4). We will state candidate recall for every version and name this as the main limit of closed mode.

### 6. "The authors did not validate the judge's unit-level scores against human judgments."

**Answer.** The judge makes no quality judgment that could disagree with a human. It aligns the prediction with
the gold annotation and counts, unit by unit (a concept, an attribute value, a relation, an expression), whether
they are equal; the human judgment is the gold itself. What can be validated is agreement with the official
scorers, and we add the correlation of the judge's totals with juːmæʧ and with the PARSEME script [PENDING 7].
We will describe the judge as a deterministic comparison so that it is not read as an LLM grading the output.

---

# Tables shared by the responses

### T1. Samples of the submission: gain of ten rounds with its 95% interval

Each cell: test score after ten rounds minus test score of the seed (V10 − V0) on the submission's test samples,
with its 95% confidence interval (paired bootstrap over test chunks / sentences, 10,000 resamples).

| | Haiku 5.5 (fragment) | Jev 1.13 | Microsoft-Decision-1 | OpenAI Decisions |
|---|---|---|---|---|
| UMR zh | +12.3 [10.6, 14.1] | +3.7 [2.7, 4.8] | +0.8 [−0.6, 2.0] | +2.4 [1.5, 3.3] |
| UMR en | +3.8 [3.1, 4.4] | +2.0 [0.6, 3.2] | +2.0 [1.0, 3.0] | +0.7 [−0.1, 1.6] |
| PARSEME zh | −6.3 [−18.3, 4.7] | +25.6 [13.5, 37.0] | +9.3 [1.2, 17.6] | +19.4 [8.5, 29.9] |
| PARSEME en | +0.6 [−7.6, 8.4] | +31.2 [20.6, 41.4] | +17.6 [5.8, 29.2] | +14.6 [5.6, 23.8] |

### T2. UMR on the complete test set (whole documents, released test gold, official juːmæʧ)

15 Chinese documents (236 sentences), 4 English documents (95 sentences; the fifth English document, 100
sentences of another source, is left out). Ranges in parentheses: three runs without the answer cache.

| system | zh | en |
|---|---|---|
| shared task, best system | 36.4 | 27.3 |
| shared task, second system | 25.8 | 21.4 |
| GPT-6.1-sol + whole guideline, one call per document | 20.2 [PENDING 1: 14 of 15 documents] | 29.3 |
| Claude Sonnet 5.5 + whole guideline, one call per document | 24.0 | 31.0 |
| the same after GEPA on the 50 gold sentences | 37.6 | 39.5 |
| submitted seed, Jev 1.13: V0 → V10 | 32.7 → 37.0 | 29.6 → 31.5 |
| submitted seed, Microsoft-Decision-1: V0 → V10 | 32.5 → 33.9 | 28.6 → 30.8 |
| audited seed, Jev 1.13: V0 → V10 | 34.5 (34.5–34.5) → 36.6 (36.5–36.6) | 32.6 (32.6–33.2) → 32.8 (32.5–33.1) |
| audited seed, Microsoft-Decision-1: V0 → V10 | 33.9 (33.8–33.9) → 35.2 (35.1–35.4) | 32.1 (31.9–32.3) → 32.2 (32.2–32.5) |
| audited seed, OpenAI Decisions: V0 → V10 | 34.1 → 35.7 | 29.1 → 28.9 |
| audited seed, fragment mode, GPT-6-luna: V0 → V5 | 19.9 → 32.0 | 20.0 → 25.8 |
| audited seed, fragment mode, Haiku 5.5: V0 → V5 | 21.8 → 31.8 | 30.3 → 32.8 |
| Jev V10 with a cascade to GPT-6-luna (threshold from training) | 38.0 | 34.6 |
| Jev's V10 answered by Microsoft-Decision-1 | 34.9 | 32.4 |

### T3. Where the gain comes from (one model throughout: Claude Haiku 5.5; samples of the submission)

| condition | UMR zh | UMR en | PARSEME zh | PARSEME en |
|---|---|---|---|---|
| (a) whole guideline, one call | 8.3 | 15.8 | 17.7 | 65.4 |
| (b) seed's instruction texts in one prompt, one call | 10.4 | 26.2 | 50.0 | 59.3 |
| (c) seed run as a procedure, V0 | 20.9 | 28.8 | 59.5 | 57.6 |
| (d) reflected procedure, V10 | 33.2 | 32.6 | 53.2 | 58.2 |
| (e) V10's instruction texts in one prompt, one call | 28.4 | 29.9 | 41.9 | 52.0 |

(a)→(b): condensing the guideline. (b)→(c): decomposition and rule nodes. (c)→(d): reflection.
(d) vs (e): what the reflected instructions lose without the procedure.

### T4. PARSEME on the whole official test file (MWE-based F; 3,462 zh / 3,965 en sentences)

| chain | zh: V0 → V5 → V10 | en: V0 → V5 → V10 |
|---|---|---|
| submitted seed, Jev 1.13 (V0 → V10) | 21.8 → 50.0 | 8.4 → 34.1 |
| submitted seed, Microsoft-Decision-1 (V0 → V10) | 20.8 → 26.7 | 8.1 → 15.1 |
| audited seed, Jev 1.13 | 38.1 → 41.7 → 41.8 (41.7–41.8) | 31.2 → 40.7 → 43.3 (43.3–44.1) |
| audited seed, Microsoft-Decision-1 | 19.8 → 29.7 → 30.5 | 20.6 → 34.8 → 37.1 (37.0–37.5) |
| audited seed, fragment mode, GPT-6-luna (to V5) | 42.8 → 57.8 | 38.7 → 43.2 |

### T5. Prompt optimisation of the single-call annotator with DSPy GEPA (same 50 gold sentences)

Claude Sonnet 5.5 with the whole guideline in one call; GEPA rewrites the instruction (80–90 metric calls;
the ten training batches are both training and validation set).

| | before | after | our best procedure (Jev V10 / with cascade) |
|---|---|---|---|
| UMR zh, complete test set | 24.0 | 37.6 | 36.6 / 38.0 |
| UMR en, complete test set | 31.0 | 39.5 | 32.8 / 34.6 |
| PARSEME zh, 100-sentence sample | 19.8 | 60.0 | 46.0 (Jev V10), 75.5 (GPT-6-luna fragment V5) |
| PARSEME en, 100-sentence sample | 57.9 | 51.4 | 57.1 (Jev V10), 58.1 (GPT-6-luna fragment V5) |

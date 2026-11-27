# Author response — Submission 12193

Marks in this draft (remove before posting):
`[PENDING n]` = waits for experiment n of `todo.md`; `[AUTHOR]` = to be filled in or checked by the authors.
Every other number is measured.

Layout: one response per reviewer. Each point is *the reviewer's concern* → **our answer** → the numbers.
Four tables are used by more than one reviewer; they are given once, as T1–T4, at the end
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

**Answer.** We are running reflection from deliberately damaged seeds (30% and 60% of the instruction files
emptied; for PARSEME also the candidate rules reduced to the verb alone) and will report V0 and V10 for each.
[PENDING 5]

### 3. "Non-monotonic / model-dependent behavior … does the tuned procedure transfer to a new model or new data?"

**Answer: it transfers to another model and to new data; the unstable runs are all of one kind.**

- *New model.* We had this experiment and cut the row for space; it will be restored. We take the procedure
  reflected with Jev 1.13 and let Microsoft-Decision-1 answer it, with no further reflection:

  | Microsoft-Decision-1 answering… | UMR zh | UMR en | PARSEME zh | PARSEME en |
  |---|---|---|---|---|
  | its own reflected procedure | 35.8 | 31.0 | 46.0 | 43.5 |
  | the procedure reflected for Jev | 36.6 | 30.4 | 57.1 | 44.2 |

  A procedure tuned with one decider works as well, or better, with another. Only the probability thresholds
  are model-specific (one number per decision; recalibrating them on the 50 sentences gives 62.0 on PARSEME zh).
- *New data.* The PARSEME procedures were tested again on the whole official test set, 35–40 times larger than
  our sample; the gains remain (table T2).
- *Unstable runs.* All 12 closed-mode runs improve. The runs that do not improve are fragment-mode runs (Haiku on
  PARSEME, GPT-6-luna on English PARSEME). In fragment mode an edit is accepted without being measured; in
  closed mode every edit is measured on the training batch before it is kept. We will say this in the results.

### 4. "Domain generality is asserted beyond evidence … fuzzy, highly-recursive annotation."

**Answer.** We agree and will limit the claim to the two tasks studied. As additional evidence we apply the same
protocol (guideline-only seed, 50 gold units, 10 rounds) to [AUTHOR: chosen task]. [PENDING 6]

### 5. "Report UMR with an official/standard scorer alongside juːmæʧ."

**Answer.** juːmæʧ *is* the official scorer of the UMR parsing shared task whose data we use; we will say so at
first mention. We also add AnCast++:

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

**Answer.** Two comparisons, on the same tasks and the same 50 gold sentences:
(a) the large-model baseline with its prompt improved by the same reflector (response to 9J4c, point 1) [PENDING 1];
(b) DSPy's GEPA optimiser applied to the single-prompt Haiku annotator, starting from the seed texts [PENDING 4].
GEPA is the closest existing method: it also rewrites prompts from reflection on failures. The difference is that
it revises one prompt from an end-to-end score, whereas our reflector is told which decision failed and may
edit the code of rule nodes as well as the text.

---

# Response to Reviewer 9J4c

### W1. "A baseline with the same gold data or prompt optimization would make the comparison more convincing. The UMR SOTA comparison also uses different evaluation settings."

**Answer.** Both are now done like-for-like.

- *Same gold for the baseline.* GPT-6.1-sol with the whole guideline receives the same 50 gold sentences in two
  ways: (1) as few-shot examples; (2) through the same reflection loop with the same reflector, which after each
  training batch rewrites a set of notes appended to the guideline. Test scores: [PENDING 1, 2].
- *UMR SOTA on identical data.* See table T4: the shared-task systems' released outputs, cut to our test chunks
  and scored with the same scorer. We are level with the best system in Chinese (37.6 vs 36.9) and above it in
  English (32.6 vs 27.7).

### W2. "The test sets are small, with no repeated runs or confidence intervals. Some improvements are only a few F1 points."

**Answer.** We add confidence intervals (table T1) and a test on the whole PARSEME test set (table T2).

- Of the 16 runs in T1 (4 task–language pairs × 4 models), 12 have a gain whose 95% interval lies entirely above
  zero, including several of the small ones (e.g. English UMR, Jev: +2.0 [0.6, 3.2]). For the other 4 the
  interval contains zero, so we cannot claim an improvement, and will not; none is a significant loss.
- PARSEME intervals are wide because 100 sentences contain only 59 (zh) and 57 (en) expressions. On the whole
  test set (3,462 / 3,965 sentences) the gains remain large: Jev +28 F in Chinese, +26 F in English.
- Repeated runs of the test for V0 and V10: [PENDING 3].

### W3. "It is difficult to separate the effects of decomposition, reflection, and engineering effort."

**Answer.** Table T3 separates them with one model. For UMR each step adds: condensed instructions instead of the
whole guideline (zh +2, en +10), running them as a procedure (+10, +3), reflection (+12, +4). For PARSEME in
fragment mode the pattern does not hold, and we will say so: decomposition helps in Chinese only, and reflection
does not help Haiku. The PARSEME gains come from the closed-mode procedures (T1).

### W4. "Reflection uses Claude Sonnet 5.5, and the framework requires task-specific code … development cost is not evaluated."

**Answer.** Each scheme needs a procedure designed from its guideline; that is the intended workflow, and we will
report its cost.

- Model cost: the reflector for all runs together costs $29 at list price; testing every version of every run
  cost $37. Annotating 100 sentences costs $4–7 with the baseline and $0.01–0.3 with a decision-model procedure.
- Human cost: authoring time as in our answer to Reviewer 6SVz, point 1.
- Task-specific parts: instruction files, rule nodes, and the list of units the judge compares. Shared between
  UMR and PARSEME: the execution, the trace, and the reflection loop.

### C1. "Table 3 labels Sonnet 5.5 results as V10."

**Answer.** The labels are wrong; thank you. The Sonnet rows are V2 (UMR, on 5 of the 20 chunks) and V3
(PARSEME); the GPT-6-luna UMR row is V2 on the same 5 chunks. We relabel them, mark the subset, and no longer
bold the English UMR 42.5, which is on that subset (Haiku V10 on the same chunks: 40.0).

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

**Answer.** Yes, we will correct it. The abstract will say: reflected procedures beat the larger model on UMR in
both languages and on Chinese PARSEME; on English PARSEME the larger model with the whole guideline remains
better (the difference is statistically significant, table T1).

### 2. "The baseline uses a single zero-shot prompt without tuning. Did you try prompt-tuning or few-shot examples?"

**Answer.** We now do both, with the same 50 gold sentences the procedures use: few-shot examples, and notes
written by the same reflector over ten rounds. Test scores: [PENDING 1, 2]. If this lifts the baseline above the
procedures, we will report it and restate the claim as one about cost and inspectability at equal supervision.

### 3. "The SOTA comparisons use mismatched data … How does comparing sentence chunks against whole documents affect the UMR SOTA comparison?"

**Answer.** It makes the scores incomparable, so we removed that comparison and replaced it.

- *Why incomparable.* A five-sentence chunk loses the document-level relations (coreference, temporal, modal)
  that cross its boundary, so chunk scores and whole-document scores measure different things.
- *UMR, now on identical data* (table T4). We cut the shared-task systems' released outputs to our chunks and
  scored both sides the same way: Chinese 37.6 (ours) vs 36.9; English 32.6 vs 27.7.
- *PARSEME, now on the full test set* (table T2). Scores are lower than on our sample because the sample has
  50 sentences with and 50 without an expression, whereas in the full test set only 18% (zh) and 11% (en) of
  sentences contain one, which gives more room for false positives. The full set becomes the main PARSEME number.

### 4. "The paper does not quantify the human time and expertise required."

**Answer.** About [AUTHOR: N] person-hours per task; the process is described in our answer to Reviewer 6SVz, point 1.

### 5. "Deterministic rule nodes limit recall … the model cannot recover the missed expression."

**Answer.** True for a fixed procedure, which is why reflection edits code too. "Missed candidate" is a category of
our error taxonomy, and it triggered 2–6 accepted edits of the candidate rules per PARSEME run. We will show
candidate recall at V0 and V10 [PENDING 7] and state in the method section that rule nodes are revised as well.

### 6. "The authors did not validate the judge's unit-level scores against human judgments."

**Answer.** The judge makes no quality judgment that could disagree with a human. It aligns the prediction with
the gold annotation and counts, unit by unit (a concept, an attribute value, a relation, an expression), whether
they are equal; the human judgment is the gold itself. What can be validated is agreement with the official
scorers, and we add the correlation of the judge's totals with juːmæʧ and with the PARSEME script [PENDING 7].
We will describe the judge as a deterministic comparison so that it is not read as an LLM grading the output.

---

# Tables shared by the responses

### T1. Does reflection help, and is it more than noise?

Each cell: test score after ten rounds minus test score of the seed (V10 − V0), with its 95% confidence
interval (paired bootstrap over test chunks / sentences, 10,000 resamples). An interval entirely above zero means
a statistically reliable improvement.

| | Haiku 5.5 (fragment) | Jev 1.13 | Microsoft-Decision-1 | OpenAI Decisions |
|---|---|---|---|---|
| UMR zh | +12.3 [10.6, 14.1] | +3.7 [2.7, 4.8] | +0.8 [−0.6, 2.0] | +2.4 [1.5, 3.3] |
| UMR en | +3.8 [3.1, 4.4] | +2.0 [0.6, 3.2] | +2.0 [1.0, 3.0] | +0.7 [−0.1, 1.6] |
| PARSEME zh | −6.3 [−18.3, 4.7] | +25.6 [13.5, 37.0] | +9.3 [1.2, 17.6] | +19.4 [8.5, 29.9] |
| PARSEME en | +0.6 [−7.6, 8.4] | +31.2 [20.6, 41.4] | +17.6 [5.8, 29.2] | +14.6 [5.6, 23.8] |

V10 against the GPT-6.1-sol baseline: Chinese UMR, all four procedures better (+9.3 to +13.7, all intervals above
zero); English UMR, Haiku better (+2.4 [0.4, 4.0]), the three decision models not distinguishable from the
baseline; English PARSEME, the baseline better than every procedure (−17 to −32).

### T2. PARSEME on the whole official test set (MWE-based F; F on unseen expressions in parentheses)

| | sentences | V0 | V10 |
|---|---|---|---|
| zh, Jev 1.13 | 3,462 | 21.8 (11.9) | 50.0 (41.2) |
| zh, Microsoft-Decision-1 | 3,462 | 20.8 (10.7) | 26.7 (14.7) |
| en, Jev 1.13 | 3,965 | 8.4 (6.2) | 34.1 (26.6) |
| en, Microsoft-Decision-1 | 3,965 | 8.1 (6.0) | 15.1 (10.9) |

Remaining models: [PENDING 3].

### T3. Where the gain comes from (one model throughout: Claude Haiku 5.5)

| condition | UMR zh | UMR en | PARSEME zh | PARSEME en |
|---|---|---|---|---|
| (a) whole guideline, one call | 8.3 | 15.8 | 17.7 | 65.4 |
| (b) seed's instruction texts in one prompt, one call | 10.4 | 26.2 | 50.0 | 59.3 |
| (c) seed run as a procedure, V0 | 20.9 | 28.8 | 59.5 | 57.6 |
| (d) reflected procedure, V10 | 33.2 | 32.6 | 53.2 | 58.2 |
| (e) V10's instruction texts in one prompt, one call | 28.4 | 29.9 | 41.9 | 52.0 |

(a)→(b): condensing the guideline. (b)→(c): decomposition and rule nodes. (c)→(d): reflection.
(d) vs (e): what the reflected instructions lose without the procedure.

### T4. UMR against the shared-task systems on identical data (juːmæʧ, our 20 test chunks)

| | zh | en |
|---|---|---|
| shared task, best system | 36.9 | 27.7 |
| shared task, second system | 28.2 | 22.0 |
| GPT-6.1-sol + whole guideline | 23.9 | 30.2 |
| ours, best V10 | 37.6 (Jev 1.13) | 32.6 (Haiku 5.5) |

The systems' outputs are from the UMR 2.2 release, cut to our chunks with the function that cuts the gold.
Scored against the release's own test gold instead of ours: zh 36.4 vs 36.5, en 32.8 vs 27.9.

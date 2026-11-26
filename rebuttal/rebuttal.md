# Author response — Submission 12193

Marks used in this draft (remove before posting):
`[PENDING n]` = number comes from experiment n in `todo.md`, not finished yet;
`[AUTHOR]` = only the authors know this, fill in by hand.
Every other number is already measured (SkillParseUMR, `experiment/orchestration-v2/results/`).

---

## To all reviewers: what we added

We thank the reviewers. All three ask for (i) a fairer baseline, (ii) statistical evidence, (iii) the source of
the gains and (iv) a like-for-like SOTA comparison. We ran these; the results will be in the revision.

**A. Confidence intervals** (paired bootstrap over test chunks / sentences, 10,000 resamples).
Gain of ten reflection rounds, V0 → V10, with 95% interval:

| | Haiku 5.5 (fragment) | Jev 1.13 | Microsoft-Decision-1 | OpenAI Decisions |
|---|---|---|---|---|
| UMR zh | +12.3 [10.6, 14.1] | +3.7 [2.7, 4.8] | +0.8 [−0.6, 2.0] | +2.4 [1.5, 3.3] |
| UMR en | +3.8 [3.1, 4.4] | +2.0 [0.6, 3.2] | +2.0 [1.0, 3.0] | +0.7 [−0.1, 1.6] |
| PARSEME zh | −6.3 [−18.3, 4.7] | +25.6 [13.5, 37.0] | +9.3 [1.2, 17.6] | +19.4 [8.5, 29.9] |
| PARSEME en | +0.6 [−7.6, 8.4] | +31.2 [20.6, 41.4] | +17.6 [5.8, 29.2] | +14.6 [5.6, 23.8] |

12 of 16 gains exclude zero; none of the four others is a significant loss. Against the GPT-6.1-sol baseline:
all four Chinese UMR procedures are significantly better (+9.3 to +13.7); in English UMR only Haiku is
(+2.4 [0.4, 4.0]), the decision models are tied with it; in English PARSEME the baseline is significantly
better than every procedure. We will state exactly this, and no more, in the abstract and the conclusion.

**B. PARSEME on the whole official test set** (3,462 zh / 3,965 en sentences instead of the 100-sentence sample):

| | V0 F (unseen) | V10 F (unseen) |
|---|---|---|
| zh Jev 1.13 | 21.8 (11.9) | 50.0 (41.2) |
| zh Microsoft-Decision-1 | 20.8 (10.7) | 26.7 (14.7) |
| en Jev 1.13 | 8.4 (6.2) | 34.1 (26.6) |
| en Microsoft-Decision-1 | 8.1 (6.0) | 15.1 (10.9) |

The gains hold on 35–40 times more data (Jev: +28 and +26 F), so the procedures did not fit the sample. The
absolute scores are lower than on the sample, which was balanced to contain more expressions; the revision
reports the full test set as the main PARSEME number and compares with the shared-task systems there.
[PENDING 3: the remaining chains on the full test set.]

**C. UMR against the shared-task systems on identical data.** The UMR 2.2 release contains the system outputs of
the shared task. We cut the two participating systems' outputs to exactly our 20 test chunks, with the function
that cuts the gold, and scored everything with the official scorer:

| juːmæʧ, same 20 chunks | zh | en |
|---|---|---|
| shared task: best system | 36.9 | 27.7 |
| shared task: second system | 28.2 | 22.0 |
| GPT-6.1-sol + whole guideline | 23.9 | 30.2 |
| ours, best V10 | 37.6 (Jev 1.13) | 32.6 (Haiku 5.5) |

So on the same sentences, with the same scorer and the same document-level relations kept, we are on par with
the best system in Chinese and about 5 points above it in English, with 50 gold sentences instead of the
training set. Scoring against the release's own test gold instead of ours gives the same picture
(zh 36.4 vs 36.5; en 32.8 vs 27.9). This replaces the comparison with published whole-document scores.

**D. Where the gain comes from** (one model, Claude Haiku 5.5, so that model size is constant):

| condition | UMR zh | UMR en | PARSEME zh | PARSEME en |
|---|---|---|---|---|
| whole guideline, one call | 8.3 | 15.8 | 17.7 | 65.4 |
| the seed's instruction texts in one prompt, one call (no decomposition, no rule nodes) | 10.4 | 26.2 | 50.0 | 59.3 |
| seed procedure V0 (decomposition + rule nodes) | 20.9 | 28.8 | 59.5 | 57.6 |
| reflected procedure V10 | 33.2 | 32.6 | 53.2 | 58.2 |
| V10's instruction texts in one prompt, one call | 28.4 | 29.9 | 41.9 | 52.0 |

For UMR the three ingredients add up in both languages: condensing the guideline into instructions (+2 / +10),
executing them as a procedure with rule nodes (+10 / +3), reflection (+12 / +4). Running the reflected
instructions without the procedure loses 3–5 points, so what reflection learned is mostly in the instructions and
partly needs the structure. For PARSEME with a language model in fragment mode the picture is different and we
will say so: decomposition helps in Chinese (50.0 → 59.5), reflection does not help Haiku, and in English Haiku
with the whole guideline (65.4) beats every Haiku procedure. PARSEME gains are a property of the closed
(decision-model) procedures (table A), not of fragment mode.

**E. A baseline with the same gold.** We gave GPT-6.1-sol the same 50 gold training sentences in two ways:
(1) as few-shot examples after the guideline; (2) with the same reflection loop and the same reflector (Claude
Sonnet 5.5): after each training batch the reflector rewrites a set of notes that is appended to the guideline
(the 300-page guideline itself cannot be usefully edited in ten rounds). Results: [PENDING 1, 2].

---

## Reviewer 6SVz

**Seed authoring effort; benefit may reflect skilled authoring.** The guidelines are already organised by
decision (UMR: one chapter per attribute and relation, each with tests; PARSEME: explicit decision trees per
category). The seed is produced by an LLM that splits the guideline into one instruction file per decision; the
authors check that each file says what the guideline says and write the rule nodes (format, inventories,
candidate extraction). No example and no gold annotation is used. This took about [AUTHOR: N] person-hours for
UMR and [AUTHOR: N] for PARSEME, by [AUTHOR: one author with / without prior annotation experience in the
scheme]. Table D separates the authoring from the orchestration: the same seed texts given to the same model in
a single prompt score 10.4 / 26.2 on UMR, the procedure 20.9 / 28.8, the reflected procedure 33.2 / 32.6.
A seed cannot be perfect in any case, because the gold annotations follow conventions that the guideline does
not state (our Chinese gold and the release's gold agree only at 70.2 juːmæʧ with each other); this gap is what
reflection closes.

**Imperfect seeds.** We run reflection from deliberately damaged seeds (a fraction of the instruction files
emptied; the candidate rules of PARSEME reduced to the verb alone) and report how much of the V10 score is
recovered. [PENDING 5]

**Does a tuned procedure transfer to another model or to new data?** Model: we had this experiment and dropped
the row for space; it will be restored. The procedure reflected with Jev 1.13 (V10), answered by
Microsoft-Decision-1 with no further reflection:

| | UMR zh | UMR en | PARSEME zh | PARSEME en |
|---|---|---|---|---|
| Microsoft-Decision-1, its own V10 | 35.8 | 31.0 | 46.0 | 43.5 |
| Microsoft-Decision-1 on Jev's V10 | 36.6 | 30.4 | 57.1 (62.0 after recalibrating thresholds) | 44.2 |

The transferred procedure is as good as, or better than, the one tuned for the model. What does depend on the
decider is the probability threshold, which is one number per decision and is recalibrated on the 50 sentences.
Data: table B (whole PARSEME test set). On the non-monotonic runs: all 12 closed-mode runs improve; the two runs
that do not are fragment-mode runs (Haiku zh PARSEME, GPT-6-luna en PARSEME), where edits are accepted without
being measured. We will state this limitation of unmeasured reflection in the results section.

**Generality beyond crisp decompositions.** We agree two tasks do not establish generality and will weaken the
claim. To give evidence on a task of the kind the reviewer names, we apply the method to
[AUTHOR: chosen task — see todo.md 6] with the same protocol (guideline-only seed, 50 gold units, 10 rounds).
[PENDING 6]

**Official scorer.** juːmæʧ is the official scorer of the UMR parsing shared task whose data we use (we will say
so at first mention). We add AnCast++ beside it. Reflection gains hold under AnCast (Haiku: zh 21.4 → 42.2, en
31.1 → 37.5; Jev: zh 32.8 → 37.1). The comparison with the baseline does not: under AnCast GPT-6.1-sol scores
44.8 / 45.8, above our procedures. [AUTHOR: check the cause before posting; our hypothesis is that juːmæʧ also scores
the alignment of nodes to tokens, which the single-call baseline gets wrong, and AnCast does not.] We will
report both scorers and this difference.

**Prompt-compilation baselines (DSPy).** Experiment E(2) is this comparison in the setting where it is possible:
an optimiser rewriting the single prompt of the large model from the same gold. In addition we run DSPy's GEPA
optimiser on the single-prompt Haiku annotator (seed texts as the initial prompt, same 50 sentences, same
reflector model). [PENDING 4] The conceptual difference is that those optimisers revise one prompt from an
end-to-end score, whereas our reflector sees which decision failed and may edit code as well as text.

## Reviewer 9J4c

**W1 Baseline with the same gold; SOTA settings.** See E and C above.

**W2 Statistical evidence.** See A (intervals) and B (whole PARSEME test set). Repeated runs of the test for V0
and V10: [PENDING 3]. Closed-mode decisions are thresholded probabilities and vary little between calls; we
report the spread for both modes.

**W3 Sources of improvement.** See D.

**W4 Cost and generality.** Every annotation scheme needs its procedure designed from its guideline; this is the
intended workflow, and the paper's proposal is that this is where the effort of a new project should go.
Measured costs: the reflector for all ten-round runs together costs $29 at list price; testing
all versions of all runs cost $37; the GPT-6.1-sol baseline costs $4–7 per 100 sentences against $0.01–0.3 for
a decision-model procedure. Authoring time is given in the answer to Reviewer 6SVz and will be in the paper.
What is task-specific: the instruction files, the rule nodes and the list of units the judge checks; the
reflection loop, the tracing and the execution are shared between UMR and PARSEME.

**C1 Table 3 labels.** The reviewer is right, the labels are wrong. The Sonnet rows are V2 (UMR, on 5 of the 20
chunks) and V3 (PARSEME); the GPT-6-luna UMR row is V2 on the same 5 chunks. We relabel them, mark the subset,
and no longer bold the 42.5 English UMR score, which is on the subset (Haiku V10 on the same chunks: 40.0).

**C2 "First work".** Chun and Xue (2024) convert and combine the outputs of trained parsers in a pipeline; the
steps are components, not guideline decisions, and nothing is revised from annotations. We will cite it at this
point and narrow the claim to: compiling the guideline itself into a decision procedure that is revised by
reflection, without training.

**C3 Typos.** Fixed: "for decision thresholds", "harness code (Zelikman…)", "uses code". In the Limitations the
ranges are "95–100" and "57–59" sentences; the approximation sign was lost in typesetting.

## Reviewer y4Vj

**Abstract and English PARSEME.** Yes. The abstract will say that reflected procedures beat the larger model on
UMR in both languages and on Chinese PARSEME with the best procedures, and that on English PARSEME the larger
model with the whole guideline remains better (75.6 vs 58.2 on the sample; the difference is significant).

**Untuned baseline; prompt-tuning or few-shot?** See E: the baseline with 50 gold examples in the prompt and the
baseline with reflected notes. [PENDING 1, 2] Trajectory available now, Chinese PARSEME: the baseline's F on each
new training batch before that round's notes is 66.7, 33.3, 66.7, 44.4, 85.7, 66.7, 50.0, 88.9, 85.7, 85.7
(5 sentences per batch, so noisy); its test score is pending. Whatever the outcome we report it: if notes lift
the baseline above the procedures, the claim becomes one about cost and inspectability at equal supervision,
not about accuracy.

**Mismatched SOTA data; chunks vs whole documents.** See C and B. To answer the question directly: scoring
five-sentence chunks drops the document-level relations (coreference, temporal, modal) that cross a chunk
boundary and renumbers sentences, so chunk scores and whole-document scores are not comparable in either
direction. We therefore no longer compare with published whole-document scores; we cut the shared-task systems'
released outputs to our chunks and score both sides identically.

**Human time for the seeds.** About [AUTHOR: N] person-hours per task; see the answer to Reviewer 6SVz.

**Rule nodes limit recall.** True for a fixed procedure, and it is why the reflector may edit code as well as
instructions: in the PARSEME runs it changed the candidate rules (`candidates.py`) 2–6 times per run, and the
missed-candidate category of our error taxonomy is exactly what triggers such edits. We will show the
candidate recall of V0 and V10 for each run [PENDING 7: computable from stored traces, no cost] and say
this explicitly in the method section, where the current text suggests that only instructions are revised.

**Was the judge validated against humans?** The judge makes no judgment of quality. It aligns the predicted
annotation with the gold annotation and counts, per unit (a concept, an attribute value, a relation, an
expression), whether the prediction equals the gold; the human judgment is the gold itself. What can be checked
is that its counts agree with the official scorers; we add the correlation between the judge's per-version
totals and juːmæʧ / the PARSEME script's F over all tested versions [PENDING 7: computable from stored
results, no cost]. We will describe the judge as a deterministic comparison in the paper to avoid the reading
that an LLM grades the output.

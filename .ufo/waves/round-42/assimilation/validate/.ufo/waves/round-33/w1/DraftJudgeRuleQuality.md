# Draft findings — round-32 judge rule drift

Axes: rule fidelity, auditability, and scope containment.

## Behavior and findings

Drafts only; no product files were edited. The proposed QUALITY addition is criterion 97, following criteria 95–96 at `corpus/QUALITY.md:681-698`:

> 97. Every judge dispatch and judge receipt includes the frozen decision rule word for word from the frozen contract. The counter checks the rule at the whitespace-collapsed level. If a judge's reason concedes any unsupported part, its verdict is `unsupported`/`disagree`, never `supported`/`agree` with a caveat. Check: at the governed revision, require the frozen rule in both the committed dispatch and receipt after collapsing whitespace runs to one space, and check that each reason conceding an unsupported part has an `unsupported`/`disagree` verdict. Lesson: `corpus/lessons/round-32.md:113-116` (citation corrected append-only below); `.ufo/waves/round-33/contract.md:93-95` (routed defect 2). Shown able to fail: the round-32 dispatch contains `Reject (disagree) a row when` (`.ufo/waves/round-32/r1-dispatch.json:7`), while the receipt does not:
>
> Search executed with the specialized grep tool: pattern `Reject \\(disagree\\) a row when`, path `.ufo/waves/round-32/judge/JudgeRecheck.md`.
> Output: `No matches found`.
> Equivalent command: `grep -F 'Reject (disagree) a row when' /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-32/judge/JudgeRecheck.md` (no matching line).

The round-32 counter's frozen R4 requires the receipt to carry an `agree` line (`.ufo/waves/round-32/count-c1.py:21-23,216-217`); it does not require the dispatch decision rule or test a caveated agreement. The round-33 contract now states R-J and requires it in dispatch and receipt (`.ufo/waves/round-33/contract.md:37-50`). Its A1 counter uses the frozen rule literal and checks normalized presence in both files: normalization is whitespace runs only (`count-c1-a1.py:34-41,54-57,78-79,279-288`). The counter checks verdict labels and coverage, not whether the judge's prose reason semantically admits an unsupported part (`count-c1-a1.py:291-313`); criterion 97's reason/verdict consistency therefore remains a judge-review obligation.

## Append-only correction paragraph draft

Append this paragraph to `corpus/lessons/round-32.md`; leave the original lines 113–116 intact:

> Correction (round 33): The citation to `JudgeRecheck` finding 1 at lines 113–116 is incorrect: the receipt has no numbered findings. Its per-row reasons state the reading at `.ufo/waves/round-32/judge/JudgeRecheck.md:63,73-76`. The S058-specific numbered Finding 1 is in `.ufo/waves/round-32/r1/ReviewMultiSource.md:22`. Attribute the multi-row interpretation to the receipt's per-row reasons, and cite ReviewMultiSource Finding 1 for the S058 challenge.

Pointer checks (specialized grep tool; paths relative to the lane):

- `pattern='finding'`, `path='.ufo/waves/round-32/judge/JudgeRecheck.md'` → `No matches found`.
- `pattern='S058'`, same receipt → line 26 `- S058: agree`; line 63 begins `- S058: quotes verbatim carry the ordering half ...`; thus the relevant text is a per-row reason, not a numbered finding.
- `pattern='S117|S128|S137|S149'`, same receipt → verdicts at lines 36–39 and per-row reasons at lines 73–76 (S117, S128, S137, S149).
- `pattern='Finding 1'`, `path='.ufo/waves/round-32/r1/ReviewMultiSource.md'` → line 22: `**Finding 1 — MEDIUM: S058's \`current\` is receipted on half the teaches cell.**`
- `pattern='JudgeRecheck|ReviewMultiSource|S058|S117|S128|S149'`, `path='corpus/lessons/round-32.md'` → lines 113–116 show the disputed text and the `JudgeRecheck` finding 1 citation.

## Round-33 Mistakes row draft

The requested `corpus/lessons/round-33.md` is absent from the current lesson-directory listing, so this row is draft text only:

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| judge rule drift / caveated agreement | `.ufo/waves/round-32/r1-dispatch.json:7`; `.ufo/waves/round-32/judge/JudgeRecheck.md` (rule phrase absent; `:26,36-39` agreements and `:63,73-76` reasons); `corpus/lessons/round-32.md:113-116` (incorrect finding attribution) | Proposed `corpus/QUALITY.md:97`; routed defect `.ufo/waves/round-33/contract.md:93-95` | Require the frozen contract rule in dispatch and receipt, checked after whitespace collapse; record a conceded unsupported part as `unsupported`/`disagree`, not `agree` with a caveat; correct the lesson citation append-only. |

## Gates, touched surfaces, limits

- Read-only research only: file reads and specialized grep searches above. No build, test, lint, formatter, or counter run; no git/jj command; no install/update; no processes started.
- Only touched surface: this report, `.ufo/waves/round-33/w1/DraftJudgeRuleQuality.md`.
- Untouched requested targets: `corpus/QUALITY.md`, `corpus/lessons/round-32.md`, and `corpus/lessons/round-33.md`. No criterion, correction, or lesson row was applied. No out-of-scope lane files were written.
- Known limit: the round-33 lesson file is not present in this checkout; the requested Mistakes row is therefore supplied here for the integration owner.

# CritLoop — round 36, wave 2, attempt 2

Item attacked: whether round 36 repeats rounds 32–35's counter-discrimination loop; specifically pre-data control handling, the round-34 harness shortcut, freshness overreach, and repair-first provenance.

Reviewed data revision: `bf0df77fee4b6ef54a90aea09335c7617f125151`; entering revision: `6bd57097`. Lane-relative paths below resolve inside the assigned lane. Fleet files were read only. This is a scoped critique, not native judgment, admission, or an outside-reviewer endorsement of C1.

## Axes

- **Operability:** C2's runnable history checker and its new deleted-row operation.
- **Freshness:** C1 is exploratory technique only; byte classification does not establish re-verified skill claims.
- **Calibration:** no round-36 claim; nevertheless accurate history, evidence provenance, and the distinction between counter output and admission matter here.
- Depth, coverage, and adjacency are not separately claimed by these two tools. I assign no axis or trend verdict.

## F1 — freshness overreach remains in the landed claim table

**Counterexample:** an unchanged S156 source is classified `drifted` because the saved comparison file is an annotated excerpt. Yet the landed contract's capability cell says the program “flags stale source rows,” with an unqualified `C1=met` after-state.

Command executed:

```sh
git --no-optional-locks -C /home/vgpnk/Projects/shokunin/mori-shokunin show bf0df77fee4b6ef54a90aea09335c7617f125151:.ufo/waves/round-36/contract.md
```

Observed excerpts, at that blob's lines 13 and 120–126:

```text
| C1 | freshness (lowest-scoring non-retired axis, tied at 5 with depth and calibration) ... | flags stale source rows: `fresh`, `excerpt`, `drifted`, `unavailable`, `no-copy` per row | ... | `count-c1.py <landed tip>` → `C1=met` |
A byte classifier certifies representation differences, not stale skill claims.
... It verifies only as `unprovable-but-better` with a named non-author reviewer; otherwise
it lands `unprovable`. P-C1 is still run and reported as evidence of the probe's byte behaviour, not as C1's verdict.
```

The pre-data exploratory declaration is the operative boundary; the table has not caught up with it. This is an internal documentation contradiction, **not evidence that a freshness verdict has actually been admitted**. The live worktree description was already corrected when read; that does not change the reviewed landed blob.

Local counterexample evidence, inspected rather than re-fetched:

- `read corpus/evidence/sources-r30/S156.txt:1-12` returned an `id`, URL, original-response `sha256`, access time, and numbered source lines—not a raw response body. The recorded response sha is `b56aa781be9c29b610156925030d3c4ab720c0ad73d57907d230ca3047302f2a`.
- `read .ufo/waves/round-36/w1/CritAxisFit.md:18-46` returned the archived command `timeout 45s curl --fail --location --silent --show-error --max-time 30 https://raw.githubusercontent.com/systemd/systemd/v262/src/shared/bus-print-properties.c | timeout 45s sha256sum` and its observed output `b56aa781be9c29b610156925030d3c4ab720c0ad73d57907d230ca3047302f2a  -`. Its recorded copy-hash command, `timeout 10s sha256sum corpus/evidence/sources-r30/S156.txt`, returned `4c02999410622d782979d025a9a61314104873cba9c19e4857feba4bd0473b5e  corpus/evidence/sources-r30/S156.txt`.
- `read .ufo/waves/round-36/evidence/c0-rescore-v2.txt:1138-1151` returned `real_mismatch S156 tool=fresh oracle=drifted`. Thus this is an observed representation witness, not merely a proposed edge case.

**Impacted axes:** freshness interpretation and calibration/evidence honesty. Merely shipping the honestly scoped probe is not itself axis harm.

**Smallest safe correction:** retain the frozen predicates and receipts, and land an explicit documentary correction identifying the stale-source wording in contract line 13 as superseded by the pre-data exploratory declaration. Final claim/scorecard/capability prose must consistently distinguish `P-C1 met` from C1 verification. No dispatched lane reviewer, including this seat, supplies the required outside endorsement.

## F2 — the anti-loop history is misstated

The same executed `git show` returned at contract lines 4–5:

```text
no calibration claim this round (four straight calibration counters
could not tell real content from junk, r32–r35).
```

The failed sequence is real, but it was not four calibration claims. Evidence retrieved with `grep` over `.ufo/waves/round-3{2,3,4,5}/*.md`, pattern `K9|J11|harness.key|repair.first|calibrat|loop|saturat`, and the prior fleet reports:

| Round | Observed declaration |
|---|---|
| 32 | `round-32/contract.md:15`: `C1 — freshness` |
| 33 | `round-33/contract.md:12-15`: C1 works depth, on FR6 |
| 34 | `round-34/contract.md:7-9,90`: C1 coverage; C2 exploratory calibration |
| 35 | `round-35/contract.md:14`: C1 calibration |

The outside round-35 ruling correctly names “Calibration counter discrimination, open for the fourth round” and “fourth straight non-admitted round,” rather than assigning all four claims that axis (`corpus/lessons/round-35-verifier-spotcheck.md:168-171,195`).

**Impacted axis:** calibration/evidence history. **Smallest safe correction:** append an erratum saying “four consecutive counter-discrimination failures/non-admitted rounds,” with the actual axes. Preserve historical frozen bytes and do not manufacture a changed predicate. This was already identified in `w1/CritAxisFit.md:67`; leaving it uncorrected is residual loop behavior in the explanation of the loop itself.

## The substantive mechanism does improve on the failed pattern

### No disguised calibration re-claim

The declarations and actual enforcement concern executable state/id-list decisions, not SCORECARD/SHONEN mismatches. C1's final pre-data declaration explicitly withholds a freshness verdict. C2 adds deletion detection beyond the old wave script. Its origin in a routed repair does not erase that new operation.

Reading `count-c1.py:378-527,539-562,698-715` showed shuffled state assignments, random ids/paths/body bytes, a truth dictionary retained in counter memory, and exact per-row comparison. Reading `count-c2.py:377-488,590-621,656-658` showed generated commit operations, truth derived from the in-memory states, exact list comparison, and blind-arm exit checking. These are not the round-35 register counter's key-only checks.

### K9/J11's specific harness escape is closed by v2

Commands executed:

```sh
sha256sum /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c1.py /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c2.py /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/c0/controls/K9.py /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/c0/controls/J11.py
```

Observed hashes, respectively:

```text
86dd3b7ab2d2563bbc811e83717b35dfea3d69717dab4d41d454f8b87c8764c0
c7edaacfff029c2055bee6ddda42ff6f5c040dad7fbac81e9d169602edcbac34
231ec3ea67bf808550cdd13a20f185c5e41a01db30edfb3bae064e416c30b1a4
ede4cfdcf9d5f2d4aae5bc35fbe7996914069fb6f2da0e6355aa55560f13a3b5
```

Counter hashes match `evidence/freeze-v2.txt:3-4`; control hashes match the v2 receipt blocks. Stored scoring evidence was read, **not rerun by this seat**:

| Retrieval command | Observed stored output |
|---|---|
| `read .ufo/waves/round-36/c0/CtlK9.md:23-40` | v1 invocation `timeout 900 python3 <lane>/.ufo/waves/round-36/count-c1.py 6bd57097 --tool <lane>/.ufo/waves/round-36/c0/controls/K9.py`; blind mismatches 0, real mismatches 0; `C1=met`, exit 0 |
| `read .ufo/waves/round-36/c0/CtlJ11.md:42-56` | v1 invocation `timeout 900 python3 <lane>/.ufo/waves/round-36/count-c2.py 6bd57097 --tool <lane>/.ufo/waves/round-36/c0/controls/J11.py`; blind 24/24, real pass; `C2=met`, exit 0 |
| `read .ufo/waves/round-36/evidence/c0-rescore-v2.txt:1138-1151` | same K9 control hash under v2; blind mismatches 0; real mismatches 7; `C1=unmet`, seed `6469733924643966362`, `EXIT=1` |
| `read .ufo/waves/round-36/evidence/c0-rescore-v2.txt:176-190` | same J11 control hash under v2; blind 24/24; real FAIL, empty tool lists versus the oracle's nonempty lists; `C2=unmet`, seed `13938463740828882736`, `EXIT=1` |

The causal explanation matches code: K9's fallback applies outside scratch/loopback (`c0/controls/K9.py:105-113`); J11 returns empty outside scratch/tmp (`c0/controls/J11.py:69-72`). C1 now passes the actual repository root after a corpus/revision-equality check (`count-c1.py:567-590`); C2 passes the actual repository with the pinned historical selectors (`count-c2.py:624-643`). The real arm, not a failed generic guard, rejects both controls. This addresses the concrete round-34 failure of doing the work only inside the harness (`round-34-verifier-spotcheck.md:65-76`).

The deletion arm is not vacuous just because the real history has no deletions. `read evidence/c0-rescore-v2.txt:476-485,546-558` returned J5 blind `0/24`, including wanted deleted ids versus `deleted=[]`, real pass, final `C2=unmet`, `EXIT=1`. The blind arm supplies the missing active deletion witness.

### The round-35 met-control-as-residual error was not repeated

Command executed:

```sh
git --no-optional-locks -C /home/vgpnk/Projects/shokunin/mori-shokunin rev-list --ancestry-path --reverse c1a026cb156c5fe84d76dc79190f1885ad11abf4..bf0df77fee4b6ef54a90aea09335c7617f125151
```

Observed output:

```text
5842dc045bb3d3b7aa2bdaaf462dcff536358444
bf0df77fee4b6ef54a90aea09335c7617f125151
```

The inspected commit log identifies `c1a026cb` as the v2 redesign/control-receipt commit, `5842dc04` as the exploratory declaration, and `bf0df77` as the data commit. The pinned dispatch log records holding the data wave, redesigning after K9/J11/K13 met, and rescoring before dispatch (`dispatch-log.txt:8-13`). Unlike round 35's 10c ruling, those met controls were not waived as residuals.

## Repair-first: implementation bundled, final durable record still required

Executed command:

```sh
git --no-optional-locks -C /home/vgpnk/Projects/shokunin/mori-shokunin diff 5842dc045bb3d3b7aa2bdaaf462dcff536358444 bf0df77fee4b6ef54a90aea09335c7617f125151 -- SKILL.md corpus/QUALITY.md corpus/SOURCES.md
```

Observed summary: SKILL `20` insertions, QUALITY `25`, SOURCES `16`; three files, `61 insertions(+), 0 deletions(-)`. The actual added text supplies the registry rows, QUALITY 103–105, and the superseding rows. QUALITY 104 and SKILL explicitly make the promoted tool the active check; the old wave script remains historical evidence, not a second current authority. Supersession remains a disposition, not erasure of an immutable-edit violation.

The data commit's observed `git show --format=fuller --stat bf0df77...` also includes both new claim tools and those repairs. Consequently **a separate repair-completed-before-new-capability checkpoint is not demonstrated**: they land together. The reviewed prompt's inherited-state duty requires fixing or accounting for prior routed defects (`fleet:.ufo/prompts/mori-round-36.md:326-332`); it does not itself require a repair-only commit. Bundling is therefore a sequencing limitation to describe honestly, not by itself a new admission disqualifier.

**Fixable evidence gap at the data tip:** executing

```sh
git --no-optional-locks -C /home/vgpnk/Projects/shokunin/mori-shokunin show bf0df77fee4b6ef54a90aea09335c7617f125151:.ufo/waves/round-36/dispatch-log.txt
```

returned a file ending at line 26 with `selftest PASS 4 cases; data commit next, then counters at the landed tip`. It cannot contain the post-landing index-check record required by QUALITY 103 (`corpus/QUALITY.md:822-828`). The live log's later `staged=0 intent_to_add=0` observation is real but is not committed evidence in that data blob. `w2/RevDebtR35.md:5-15` independently names the same distinction. Smallest correction is to land the already-observed post-landing records with the final evidence, not claim that an uncommitted log was present at `bf0df77`, and not rerun a green check merely to replace its provenance. This does **not** allege a dirty index or invalidate the tool implementation.

## Residual loop behavior and limits

1. C1 still demonstrates representation differences, including the pre-existing S156 counterexample, rather than stale skill claims. The pre-data exploratory boundary is essential; a final receipt token must never replace the outside better-than-prior judgment.
2. K9/J11 rejection is evidence against those concrete path shortcuts, not a certificate against every harness-aware program. C2's real arm remains the public, fixed `6bd57097`/`f10a320d` history (`count-c2.py:44-45,624-632`). **[INFERENCE]** A program could special-case that known invocation while behaving differently on other ordinary histories. No such survivor was built or scored here, and this possibility alone does not falsify the bounded P-C2 predicate. Preserve that scope rather than changing the frozen target after data.
3. Repair implementation and new capability acquisition share a commit; final repair provenance and the non-author C1 decision must precede any admission claim. The frontier cannot be declared saturated merely because the current named controls fail.

Only file inspection, read-only Git commands, and `sha256sum` were executed by this seat. No counter, lane tool, self-test, build, formatter, native judge, alternative runtime, or background service was invoked. No files besides this report were written; no tools were installed or updated. Stored measurements above are expressly attributed to their receipts, not claimed as new runs.

VERDICT: FAIL — fixable landed-documentation defects at `.ufo/waves/round-36/contract.md:4-5,13`; repair evidence is also incomplete at the reviewed data tip (`.ufo/waves/round-36/dispatch-log.txt:26`, `corpus/QUALITY.md:822-828`). The specific K9/J11 escape is closed by v2 evidence; this is not a claim that the native judge must reject the bounded C2 acquisition.

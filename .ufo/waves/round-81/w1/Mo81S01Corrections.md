# Mo81S01Corrections — draft append-only corrections for the r80 closure (D80-1 … D80-4)

seat: Mo81S01Corrections (scribe, round 81 w1, attempt 1) — leaf member, no subagent dispatch.
date: 2026-11-04.
purpose: ready-to-paste correction sections for the L1 to integrate into `SCORECARD.md` and
`SKILL.md` and to record in `LOG.md` / the round-81 report. This draft changes no graded byte;
each section states the superseded text verbatim, its replacement, and the command plus
revision behind every quoted count.
bytes read at: lane HEAD `197655534b4a47a3c26149462e78752a6ea03eda` (`git rev-parse HEAD`).
All four sweep carriers (`SCORECARD.md`, `SKILL.md`, `SHONEN.md`, `LOG.md`) and `PROVINCE.md`
are byte-identical from `44bc941a` to HEAD
(`git diff --name-only 44bc941a0e3e9676fa33a882b43d6e9793cbf74d HEAD -- SCORECARD.md SKILL.md SHONEN.md LOG.md PROVINCE.md` → empty output),
so every `file:line` below is valid at both `44bc941a` and HEAD.
r80 measured revision: `97ce0c96c779278baa8e8bb45ade642f9fabf1e2` (short `97ce0c96`).
r80 final tip: `44bc941a0e3e9676fa33a882b43d6e9793cbf74d` (short `44bc941a`).

---

## D80-1 — the three Round 80 after-cells get their measured values

### Superseded (verbatim, `SCORECARD.md:4043-4044`, wrap as landed)

> coverage. These are declarations, not after-results: all three after cells are
> PENDING for the L1's post-integration measurements. No score moves.

and the three after-cells, each exactly the cell value `PENDING`, closing the claim-table
rows at `SCORECARD.md:4048` (C1), `:4049` (C2), `:4050` (C3).

### Replacement (ready to paste; only the named spans change)

Line 4043-4044 sentence becomes (one paragraph; re-wrap at will, keep "No score moves."):

> coverage. The three after cells below were measured at `97ce0c96c779278baa8e8bb45ade642f9fabf1e2`
> (short `97ce0c96`) by the round's frozen counters; receipt
> `.ufo/waves/round-80/evidence/after-r80.txt`, committed at `44bc941a` (named correction
> D80-1, r81). No score moves.

Row :4048 after-cell becomes:

> `C1=met tool=present sweep=0 mismatches=0 unresolved=0 tallies=0 stale=0 row_tally=19 live_tally=19 rev=97ce0c96c779`, rc 0 — `python3 -I .ufo/waves/round-80/count-c1.py 97ce0c96c779278baa8e8bb45ade642f9fabf1e2`, measured at `97ce0c96` (receipt `.ufo/waves/round-80/evidence/after-r80.txt`)

Row :4049 after-cell becomes:

> `MUTATION_C2 survivors=0 killed=6 total=6 unmutated=green rev=97ce0c96c779`, rc 0 — `python3 -I .ufo/waves/round-80/mutate-c2.py --rev 97ce0c96c779278baa8e8bb45ade642f9fabf1e2`, measured at `97ce0c96` (receipt `.ufo/waves/round-80/evidence/after-r80.txt`)

Row :4050 after-cell becomes:

> `C3=met named=56 present=56 missing=0 extra=0 rev=97ce0c96c779`, rc 0 — `python3 -I .ufo/waves/round-80/count-c3.py 97ce0c96c779278baa8e8bb45ade642f9fabf1e2`, measured at `97ce0c96` (receipt `.ufo/waves/round-80/evidence/after-r80.txt`)

### Evidence (receipt lines verified verbatim by this seat in `.ufo/waves/round-80/evidence/after-r80.txt`, read at HEAD bytes = `44bc941a` bytes)

```text
$ python3 -I .ufo/waves/round-80/count-c1.py 97ce0c96c779278baa8e8bb45ade642f9fabf1e2
C1=met tool=present sweep=0 mismatches=0 unresolved=0 tallies=0 stale=0 row_tally=19 live_tally=19 rev=97ce0c96c779
rc=0

$ python3 -I .ufo/waves/round-80/mutate-c2.py --rev 97ce0c96c779278baa8e8bb45ade642f9fabf1e2
MUTATION_C2 survivors=0 killed=6 total=6 unmutated=green rev=97ce0c96c779
rc=0

$ python3 -I .ufo/waves/round-80/count-c3.py 97ce0c96c779278baa8e8bb45ade642f9fabf1e2
C3=met named=56 present=56 missing=0 extra=0 rev=97ce0c96c779
rc=0
```

The same receipt's guard section reads `CONTROL_RECEIPT .ufo/waves/round-80/evidence/after-r80.txt sections=5 claims=7 bound=4 unbound=0` (read from the receipt, not re-run by this seat).

### Supersession (named)

This section is the named correction of record for the three `PENDING` after-cells and the
"declarations, not after-results" sentence: both are superseded by the measured values above.
The frozen predicate bytes of `.ufo/waves/round-80/contract.md` are not rewritten; P-C1/P-C2/
P-C3 are unchanged, and no axis score moves.

---

## D80-2 — `pointers=232` becomes `pointers=233`; pending wording becomes the measured command and revision

### Superseded (verbatim)

`SCORECARD.md:4036` (capabilities row, evidence cell, substring):

> `python3 -I tools/mori-claim-sweep.py --root . --pins .ufo/waves/round-80/claim-pins.json` -> `CLAIM_SWEEP mismatches=0 unresolved=0 tallies=0 stale=0 carriers=4 pointers=232`, rc 0 (both L1 retained receipts over worktree bytes, 2026-11-04; integration re-run pending)

`SKILL.md:1366` (gate-registry row 14, self-test cell, substring):

> `python3 -I tools/mori-claim-sweep.py --selftest` -> `CLAIM_SWEEP_SELFTEST pass=30 fail=0` (30 arms; L1 retained receipt over worktree bytes, 2026-11-04; integration re-run owned by L1)

### Replacement (ready to paste)

`SCORECARD.md:4036` evidence cell becomes (columns 1, 2, 4, 5 unchanged):

> `python3 -I tools/mori-claim-sweep.py --selftest` -> `CLAIM_SWEEP_SELFTEST pass=30 fail=0`, rc 0; `python3 -I tools/mori-claim-sweep.py --root . --pins .ufo/waves/round-80/claim-pins.json` -> `CLAIM_SWEEP mismatches=0 unresolved=0 tallies=0 stale=0 carriers=4 pointers=233`, rc 0 (both re-run 2026-11-04 in a detached `git worktree` export of `44bc941a`; named correction D80-2 supersedes the stale `pointers=232` and the pending-integration wording); registry row 14 in `SKILL.md`

`SKILL.md:1366` self-test cell becomes:

> `python3 -I tools/mori-claim-sweep.py --selftest` -> `CLAIM_SWEEP_SELFTEST pass=30 fail=0` (30 arms; re-run 2026-11-04 at revision `44bc941a`, named correction D80-2 supersedes the worktree-byte receipt wording)

### Evidence (measured by this seat; scratch worktree, removed after)

```text
$ git -C /home/vgpnk/Projects/shokunin/mori-shokunin worktree add --detach "$S/wt44" 44bc941a0e3e9676fa33a882b43d6e9793cbf74d
$ git -C "$S/wt44" rev-parse --show-toplevel        # == $S/wt44 (host-guard assertion passed: toplevel_ok)
$ git -C "$S/wt44" rev-parse HEAD
44bc941a0e3e9676fa33a882b43d6e9793cbf74d
$ python3 -I tools/mori-claim-sweep.py --root . --pins .ufo/waves/round-80/claim-pins.json
CLAIM_SWEEP mismatches=0 unresolved=0 tallies=0 stale=0 carriers=4 pointers=233
rc=0
$ python3 -I tools/mori-claim-sweep.py --selftest
CLAIM_SWEEP_SELFTEST pass=30 fail=0
rc=0
```

This agrees with the command/output pair in `after-r80.txt` quoted above. The independent
replication reporting `pointers=233` is in `corpus/lessons/round-80-verifier-spotcheck.md`
(C1 section), not in the counter-review seat report. The measured command at `44bc941a`
supports superseding the row's stale `pointers=232` claim.

### Supersession (named)

D80-2 is the correction of record: the row's `pointers=232` numeric claim and the
"integration re-run pending" / "integration re-run owned by L1" wording in `SCORECARD.md:4036`
and `SKILL.md:1366` are superseded by the measured runs at `44bc941a` quoted above. A count
reproduces from its cited command; this cell now states one that does.

### Integration note (adversarial, for the L1 — do not skip)

The C2 counter's `pinned` arm (`.ufo/waves/round-81/record-pins.json`: carrier `SCORECARD.md`,
row_contains `tools/mori-claim-sweep.py`, key `pointers`, command = the sweep invocation)
grades this cell against the pinned command's stdout **at the landed revision R**. If the r81
integration adds graded pointers — a capabilities row for `tools/mori-record-sweep.py`, new
`SHONEN.md` checklist lines, Axes edits — the live count at R will exceed 233 and this cell
must be re-measured after the last carrier edit and before the C2 receipt is written. A cell
left at a superseded count is exactly the `pinned>=1` mismatch `count-c2.py` flags; 233 is the
measured value at `44bc941a`, not a promise about R.

---

## D80-3 — the r80 contract's entering shorthand is superseded by the measured controls; P-C1's second conjunct narrowed to the receipt the round used

### Superseded (verbatim, `.ufo/waves/round-80/contract.md` — bytes unchanged)

C1 claim (Claims table): "…taking the mismatch count from 1 to 0."
C2 claim (Claims table): "…so the frozen six-mutant harness kills 6 of 6 (from 3 of 6)."
C3 claim (Claims table): "…taking named instruments from 15 of 55 to 55 of 55."
P-C1 second conjunct: "the same sweep at the entering revision `d5888922` finds at least one
mismatch, the named one being `SCORECARD.md`'s control-receipt capability row stating `18`
while the committed `tools/mori-control-receipt.py --selftest` prints `pass=19 fail=0`."

### Measured values that supersede the shorthand (all from `.ufo/waves/round-80/evidence/controls-r80.txt`, measured at `d5888922` before the wave)

```text
$ python3 -I .ufo/waves/round-80/count-c1.py d5888922
C1=unmet tool=absent sweep=- mismatches=- row_tally=- live_tally=- rev=d58889220d3c
rc=1

$ git -C /home/vgpnk/Projects/shokunin/mori-shokunin cat-file -e d5888922:tools/mori-claim-sweep.py
fatal: path 'tools/mori-claim-sweep.py' does not exist in 'd5888922'
rc=128

$ grep -c 'selftest 18 in-memory cases' SCORECARD.md
1
rc=0

$ python3 -I .ufo/waves/round-80/mutate-c2.py --rev d5888922
mutant drop_admitted survived rc=0 C2_COUNTER_SELFTEST pass=4 fail=0
mutant cut_clause_boundary survived rc=0 C2_COUNTER_SELFTEST pass=4 fail=0
MUTATION_C2 survivors=2 killed=4 total=6 rev=d58889220d3c
rc=1

$ python3 -I .ufo/waves/round-80/count-c3.py d5888922
C3=unmet named=14 present=55 missing=41 extra=0 rev=d58889220d3c
rc=1
```

(Per-mutant lines elided here for space; the receipt is the verbatim carrier. `drop_admitted`
and `cut_clause_boundary` survive at `d5888922`.)

So: C2's entering state is `survivors=2 killed=4 total=6`, not "3 of 6"; C3's entering state is
`named=14 present=55 missing=41 extra=0`, not "15 of 55"; C1's entering "mismatch count 1" is
not measurable as a sweep output because the tool blob is absent at `d5888922` (rc 128) — the
stale-literal and 18/19 disagreement sub-evidences remain measured (grep → 1; live selftest
`pass=19 fail=0`).

### Narrowed reading of P-C1's second conjunct (adopted; named, not silent)

The entering red is measured by running the same counter at the entering revision:
`python3 -I .ufo/waves/round-80/count-c1.py d5888922` prints `C1=unmet tool=absent` and exits 1
at `d5888922` — that receipt (`.ufo/waves/round-80/evidence/controls-r80.txt`) is the conjunct's
graded form. The "sweep finds at least one mismatch at entering" wording is superseded for the
entering arm only; P-C1's first conjunct (the sweep at R prints
`CLAIM_SWEEP mismatches=0 unresolved=0 tallies=0 stale=0`, rc 0) is unchanged. This mirrors the
r80 report's own HIGH-2 named limit
(`/home/vgpnk/Projects/shokunin/.ufo/reports/round-80/mori.md:180-182`: "The receipt for that
conjunct is `evidence/controls-r80.txt` (`C1=unmet tool=absent` rc 1)") and is the same shape
the r81 contract's P-C1 already freezes for the r81 counter (red = the same command at the
entering revision, rc 1).

### Supersession (named)

The three shorthand values (`1 -> 0`, "from 3 of 6", "from 15 of 55") and the entering-sweep
wording of P-C1's second conjunct are superseded by the measured controls quoted above. The
r80 contract bytes are not rewritten; the frozen P-C2/P-C3 sentences (which already carry the
measured `survivors=2` and `named=14 present=55 missing=41`) govern, exactly as
`corpus/lessons/round-80.md` discloses.

---

## D80-4 — `97ce0c96` is the measured revision; `44bc941a` is the final tip, evidence-only after it

### Superseded (verbatim, fleet report `/home/vgpnk/Projects/shokunin/.ufo/reports/round-80/mori.md:112-113`)

> Counting commands are paste-ready; every after-value was re-measured at the final tip
> `97ce0c96c779278baa8e8bb45ade642f9fabf1e2`. The build revision is `8108dfcc`; the tip
> carries the lesson, the LOG section and the receipts, plus one precision fix to the LOG
> prose (below).

### Correction (record in the r81 report / LOG; the fleet report bytes are not rewritten by a lane seat)

The measured revision of every r80 after-value is `97ce0c96c779278baa8e8bb45ade642f9fabf1e2`
(short `97ce0c96`): all three counter receipts print `rev=97ce0c96c779`.
`44bc941a0e3e9676fa33a882b43d6e9793cbf74d` (short `44bc941a`) is the round's final tip. The
claim that the only graded-byte change after `97ce0c96` was the after receipt, `w1-results.json`
and the reviewer report was checked against the diff and **holds**:

```text
$ git diff --stat 97ce0c96c779278baa8e8bb45ade642f9fabf1e2 44bc941a0e3e9676fa33a882b43d6e9793cbf74d
 .ufo/waves/round-80/evidence/after-r80.txt |  12 +-
 .ufo/waves/round-80/w1-results.json        |  92 ++++++++++
 .ufo/waves/round-80/w1/Mo80R01Counter.md   | 258 +++++++++++++++++++++++++++++
 3 files changed, 356 insertions(+), 6 deletions(-)
```

`git diff --name-status` for the same range: `M after-r80.txt`, `A w1-results.json`,
`A Mo80R01Counter.md`. None of the three paths is a graded carrier of the r80 predicates
(P-C1 carriers `SCORECARD.md`/`SKILL.md`/`SHONEN.md`/`LOG.md`; P-C2's graded file
`.ufo/waves/round-79/count-c2.py`; P-C3's carrier `PROVINCE.md`). Precision the routed claim
elides: `after-r80.txt` was modified, and this seat read that hunk in full — it only re-points
the three counter invocations and `rev=` tokens from `108ec314258b…` to `97ce0c96c779…`; every
count is byte-identical across the change. The r80 claims therefore re-derive unchanged at
`44bc941a`; the report sentence above is the only defect (it names `97ce0c96…` "the final tip").

### Supersession (named)

The report's "re-measured at the final tip `97ce0c96…`" wording is superseded: `97ce0c96` is
the measured revision; `44bc941a` is the final tip and is evidence-only for the after-values
(its only changes after `97ce0c96` are the three paths in the quoted diff).

---

## What this seat verified

- The three `after-r80.txt` lines quoted in D80-1 were read verbatim from the committed receipt
  (`after-r80.txt` is byte-identical `44bc941a` → HEAD: not in the diff, not in `git status`).
- `pointers=233` and `CLAIM_SWEEP_SELFTEST pass=30 fail=0` were measured by this seat at
  `44bc941a` in a detached worktree (`git rev-parse --show-toplevel` asserted before running;
  worktree removed and `git worktree prune` run afterwards; `git worktree list` shows only the
  main checkout).
- `git diff --stat` / `--name-status` `97ce0c96 44bc941a` quoted from execution; the
  `after-r80.txt` hunk read in full.
- The r80 contract shorthand and P-C1 conjunct, the SCORECARD rows, the SKILL row 14 cells and
  the fleet report sentence were quoted verbatim from the files named, at HEAD.
- Carrier stability: `git diff --name-only 44bc941a HEAD -- SCORECARD.md SKILL.md SHONEN.md
  LOG.md PROVINCE.md` → empty, so the cited line numbers hold at both revisions.

## What this seat could not verify (limits)

- The r80 counters and mutation harness were **not executed** by this seat at `97ce0c96` or
  `d5888922` (read-only on everything this seat grades; the r80 counter bytes are mid-fix in the
  worktree and must not be run half-edited). Every red/green counter value above rests on the
  committed receipts (`controls-r80.txt`, `after-r80.txt`) plus the r80 reviewer's independent
  re-derivations, quoted as receipts.
- The control-receipt guard verdict on `after-r80.txt` (`unbound=0`) is read from the receipt,
  not re-run.
- The final pointer count at the r81 landed revision R is not knowable at draft time; the D80-2
  cell states the measured `44bc941a` value and must be re-measured at integration if graded
  pointers move (integration note above).
- `PROVINCE.md`'s 56 inventory rows rest on the committed C3 receipts; not re-censused here.

## Observations on other seats' bytes (at measurement time, HEAD `19765553`, worktree state)

- `.ufo/waves/round-81/evidence/controls-r81.txt` is **modified, uncommitted** in the worktree.
  The r81 contract states the do-nothing controls were "measured and committed before the wave
  (`.ufo/waves/round-81/evidence/controls-r81.txt`)" and the contract quotes their exact lines;
  a mid-wave rewrite of a committed control receipt would contradict that freeze. If the edit is
  a counter seat's re-generation, the L1 must confirm before close that the receipt still shows
  the entering revision `44bc941a` with the frozen red lines. Flagged, not judged — not this
  seat's bytes.
- `.ufo/waves/round-80/count-c1.py` and `count-c3.py` are modified, uncommitted — sanctioned
  in-flight work (the r81 contract: "the fixes are implementation fixes inside
  `.ufo/waves/round-80/count-c1.py` and `count-c3.py`"). Noted so the dirty state is not mistaken
  for drift; not graded here.
- `tools/mori-record-sweep.py` present untracked, `.ufo/waves/round-81/battery.sh` and
  `.ufo/waves/round-81/evidence/instrument-baseline-r81.txt` untracked — expected in-flight C2 /
  battery work.
- `SCORECARD.md:4036`'s stale `pointers=232` and the pending wording are themselves the D80-2
  defect of record (r80 bytes); corrected by section D80-2 above.

## Provenance (commands run by this seat, lane root `/home/vgpnk/Projects/shokunin/mori-shokunin` unless noted)

- `git rev-parse HEAD` → `197655534b4a47a3c26149462e78752a6ea03eda`; `git cat-file -t` on both
  `97ce0c96…` and `44bc941a…` → `commit`; `git merge-base --is-ancestor 44bc941a… HEAD` → rc 0;
  `git rev-parse master` → `19765553…`; `git status --porcelain` (listed above).
- `git worktree add --detach $S/wt44 44bc941a…` (scratch `/fast/scratch/hyaku/mori-r81/Mo81S01Corrections`,
  deleted on exit; `git worktree remove --force` + `git worktree prune`; final `git worktree list`
  → main checkout only), then inside it the two sweep commands quoted in D80-2.
- `git diff --stat 97ce0c96… 44bc941a…`, `git diff --name-status …`, `git diff … --
  .ufo/waves/round-80/evidence/after-r80.txt`, `git diff --name-only 44bc941a… HEAD -- <carriers>`
  (all read-only).
- No tools were installed or upgraded (operator tooling authorization: nothing needed; pacman
  untouched).

## Evidence precision addendum

The selftest command actually executed was
`HYAKU_SCRATCH=$S/sweep python3 -I tools/mori-claim-sweep.py --selftest | tail -2`,
followed by `echo "rc=$?"`. Its printed summary `CLAIM_SWEEP_SELFTEST pass=30 fail=0`
was observed, but the displayed `rc=0` is the pipeline's last-process status, not an
independently captured Python exit status. Do not integrate a claim that this seat separately
established the selftest process exit code. The pinned sweep itself was not piped:
`HYAKU_SCRATCH=$S/sweep python3 -I tools/mori-claim-sweep.py --root . --pins .ufo/waves/round-80/claim-pins.json`;
its immediately captured `rc=0` is established.

The worktree dirty-state observation alone establishes no control-receipt defect: this seat
did not inspect that file's diff and does not assert a frozen control result changed.
Its contents require the owner's review, not a finding inferred from `git status`.

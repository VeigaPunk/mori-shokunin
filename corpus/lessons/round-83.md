# Round 83 — mori (L1 MoriR83), attempt 1, wave w1

round: 83
date: 2026-11-04
entering: 68185d6e719054c55b107280085b05609e96165b
freeze: 9075c729 (contract + counters + controls); pre-data amendment A1 landed at d2987c67

Axes: operability 7, calibration 5, depth 5, coverage 6, freshness 5, adjacency 6. C1 works
operability; C2 and C3 work the tied-lowest calibration and depth. No scalar score change is
asserted. Detection and report only; neither a source nor a receipt authorizes remediation.

Frozen authority: `.ufo/waves/round-83/contract.md` (P-C1, P-C2, P-C3 and amendment A1), the
three counters in the same directory, and the do-nothing controls
`evidence/controls-r83.txt`. This lesson does not amend that authority.

| Claim | Keeper (run from the lane root) | Target, exit 0 |
|---|---|---|
| C1 — operability (7): the r82 probe's surviving counter mutants get the failing arm each needs | `python3 -I .ufo/waves/round-83/count-c1.py <rev>` | `C1=met mutants=23 killed=22 equivalent=1 survivors=0 total=23 pristine=green` |
| C2 — calibration (5, tied lowest): the classification is bound to its committed raw snapshot | `python3 -I .ufo/waves/round-83/count-c2.py <rev>` | `C2=met snapshot=bound asof=1 tokens=64 agreed=64 residual=0 live=derived` |
| C3 — depth (5, tied lowest): the revision arm scopes its byte occurrence to the row anchor | `python3 -I .ufo/waves/round-83/count-c3.py <rev>` | `C3=met arm=anchored defeated=2 fixtures=2/2 bindings=3 revisions=0 arms=40` |

## Mistakes

| Class | Evidence pointer | Captured-by | Fix delivered this round and what makes it able to fail |
|---|---|---|---|
| The D80-4/D81-1 revision-attribution class survived inside the very correction that claimed to discharge it: a true value at a later tree labelled with an earlier revision | `corpus/lessons/round-82-verifier-spotcheck.md` D82-1; `SCORECARD.md:4038` (the r80 capability row) | QUALITY 168 required a revision whose committed bytes contain the value but did not require the *carrying line* to be the graded one; the r82 arm's occurrence test was file-wide | The C3 anchored arm requires the token and the binding's `row_contains` on ONE line (marker `ANCHORED_OCCURRENCE`, QUALITY 169), and the `elsewhere` fixture makes the r82 tool read `revisions=0`, rc 0 while the anchored tool reports `REVISION_MISMATCH ... rev-bytes`; the D82-1 correction names the actual revision that produced 249. The class is still only detectable where the lane registers a binding — a coincidental value on the anchored line is outside this arm (QUALITY 169's not-covered). |

A second, non-mined observation: the round's own mutation-adequacy work found one *equivalent*
mutant in the frozen population (`duplicates_accepted`), which is why amendment A1 exists; an
equivalent mutant is a finding about the mutation set, not about a missing arm.

## Census

Before, at round start (inherited from the r82 lesson's after-block, not rerun by this seat):
**370 source rows, exit 0**, 35 tolerated W04 duplicate-URL warnings.

After the S598 append, the census command
`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori`
reads `mori ok`, **371 rows**, malformed 0, the same 35 tolerated W04 warnings, exit 0. The row
count is the separate grammar count
`grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md`, not a number the
validator prints.
## Gate

**One admit, one reject-class decision, one adjacent note.** L1 decision on the scout's material
(`.ufo/waves/round-83/w1/Mo83Sc01Source.md`), which independently re-fetched and re-quoted every
candidate; the L1's own fetch of the same URL is byte-identical.

| Candidate | Decision | Evidence / flip condition |
|---|---|---|
| S598 — PIT (pitest.org), "What is mutation testing?" — pinned at `corpus/evidence/sources-r83/pitest-home.html`, sha256 `b0c7e0505c51c95b596060ef27babbce08e72d5aaf4557eb002c2637d2bf10cc`, 12023 bytes, 284 lines | **ADMIT** (tier A, docs) | Access 2026-11-04T08:21-08:23Z, HTTP 200, no redirect; three independent fetches (`cmp` byte-identical) and the pin's ETag `"6a1fe9b2-2ef7"` revalidates live (HTTP 304). Located quote at pinned raw line 114, 14 words: "The quality of your tests can be gauged from the percentage of mutations killed." The page's own "51 words" block spans raw lines 106-114 (51 rendered words; 108-113 renders 31 — the L1's first draft said 108-113 and is corrected here and in the row). |
| PIT "Mutation operators" (`https://pitest.org/quickstart/mutators/`, sha256 `a31331da…`, 67033 bytes) | **REJECT** (no row) | It catalogues 38 operator headings and never states killed/lived, adequacy, or the killed-percentage gauge (`grep -ci` returns 0 for `killed`, `lived`, `adequacy`, `gauged`). It would ground "how PIT mutates", not C1's rule. Flip only if a revision states a survivor's meaning for suite adequacy, or if S598's recheck loses the block and this page carries it — a pinned, re-quoted new row, never a back-fill. |
| S595 (arXiv:2102.11378v2 abstract, already in the registry) | **not re-admitted** | Different document on the same concept; S598 supplies the gauge sentence S595's scope does not claim. No row change. |

The admitted row grounds only the killed/lived mechanism and the metric. It says nothing about a
counter's `--selftest`, about anchored mutants, about any exit status, or about this lane; those
are the lane's own decisions, and the knowledge entry
(`corpus/knowledge/counter-mutation-adequacy-r83.md`) keeps them separate (K4). The scout's
precision catch is recorded: the earlier "51 words = lines 108-113" claim was wrong (31 words
there) and is corrected to 106-114 in the row and this Gate.

## Wave and seat record

ONE v1 wave, 14 seats under `ufo-wave-policy.json` (band 8–16): 6 executor, 2 scout, 1 scribe,
2 reviewer, 1 critic, 1 mutation-tester, 1 connector; attack share 4/14 (28.6 %), connectors 1.
`w1.ready` was taken by the dispatcher at 08:20:40Z (`w1.ready.dispatched`), and the seats routed
through the host table with no `model` passed.

Six seats produced no report (`Mo83E02C1C2`, `Mo83E03C1C3`, `Mo83E05Anchor`, `Mo83C01Crit` with
empty output; `Mo83S01Lesson` and `Mo83M01Mut` cut off mid-work — the latter's partial message
records its driver defects and the mid-wave counter edits, not a tally); they are recorded as dead
in the report and were **not** replaced. Their assignments were executed by the L1 from scratch prototypes validated against
the frozen detectors before application — the C1 harness grades those bytes like any other, so a
bad stand-in shows up as a survival, not as prose. The C1 reviewer's independent 24th-mutant
sweep (`w1/Mo83R01C1.md` §6) found two non-equivalent survivors outside the frozen 23 (`M24a`,
`M24b`) and two provably equivalent ones (`M24c`, `M24d`) — carried to round 84, not amended
into this claim. Everything else landed through its seat:
`Mo83E01C1C1` (six count-c1 arms), `Mo83E04Snap` (snapshot binding), `Mo83E06D82` (D82-1/D82-2),
`Mo83Sc01Source` (S598 pin and the 51-word-block correction), `Mo83Sc02Arms` (the arm map and the
independent equivalent-mutant finding that A1 adopts), `Mo83R02C23` (C2/C3 attacks and bypasses).
The C1 after-run is deterministic across two runs at `c4845c83`.

## Measured after-block (L1)

At `c4845c83244317bd85d047583c53d93263d84f31` (receipt `evidence/after-r83.txt`):

```text
$ python3 -I .ufo/waves/round-83/count-c1.py c4845c83
C1=met mutants=23 killed=22 equivalent=1 survivors=0 total=23 pristine=green detector=green
rc=0
$ python3 -I .ufo/waves/round-83/count-c2.py c4845c83
C2=met snapshot=bound asof=1 tokens=64 agreed=64 residual=0 live=derived live_tokens=63 live_agree=63
rc=0
$ python3 -I .ufo/waves/round-83/count-c3.py c4845c83
C3=met arm=anchored defeated=2 fixtures=2/2 bindings=3 revisions=0 arms=40
rc=0
```

The live census reads 63 tokens rather than the snapshot's 64 at `c4845c83`: the snapshot carries
`-FINDING:WATCHDOG_STALE` and that live reading did not. At the record commit `9cf7fda9` the same
live run reads 64 again (`live_tokens=64 live_agree=64`) — the token reappeared. This is the
volatility the `live=` fields exist to report: `live=derived` means the run happened and read red,
and the classification is bound to the snapshot, so no class and no claim moves with it.

**Counter repairs made before any after-value existed**, each filed by a seat against the frozen
sentence and disclosed here:

- **C2 (R02 attack).** The header parse now requires exactly one `# Snapshot:`, one
  `# Snapshot-sha256:` and one `# As-of:` line and the frozen snapshot path; a duplicate header
  line or a same-bytes copy at another path read `unmet`. Predicate, kill rule and target are
  byte-unchanged.
- **C3 (R02 attack).** Named limits, not defects: a `row_contains` that is a substring of another
  row's text still selects the first matching row; two anchor-carrying rows with different values
  are existential-green; a prose token on the anchored line is outside the binding grammar. All
  are recorded in QUALITY 169's not-covered clause.
- **C1 (A1).** `duplicates_accepted` is equivalent under the r82 accounting (`residual +=
  duplicates`); the exemption binds only while that coupling occurs once.

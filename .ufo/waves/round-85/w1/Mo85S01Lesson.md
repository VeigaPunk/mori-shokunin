# Mo85S01Lesson — lesson, registry rows and Gate (round 85, wave w1, attempt 1)

Seat: Mo85S01Lesson (scribe, leaf — no subagent dispatch). Date: 2026-11-04.
Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin`. Entering revision
`2cc4b1ae35a83e4fd3fc48bae842bdf38df2e80e`; freeze `ab260865` (contract, three counters, controls).
Scratch `/fast/scratch/hyaku/mori-r85/Mo85S01Lesson/` created and deleted before yield.
No tool was installed or upgraded; no pacman transaction; no mutating git/jj command against any
repo; no lane, OS, unit, service or orchestration state changed.

Frozen authority read in the order given: `.ufo/waves/round-85/contract.md`,
`.ufo/waves/round-85/count-c1.py` / `count-c2.py` / `count-c3.py`,
`.ufo/waves/round-85/evidence/controls-r85.txt`, `.ufo/waves/round-84/w1/Mo84R01C1.md` §4-§5,
`.ufo/waves/round-84/w1/Mo84R03Record.md` §0, `corpus/lessons/round-84-verifier-spotcheck.md`
(routed defects), `SCORECARD.md` `## Planned (round 85)`, and the `CORPUS.md` SOURCES contract.

## 1. Behavior — what this seat did

| Task | Result |
|---|---|
| `corpus/lessons/round-85.md` written with `## Mistakes`, `## Census`, `## Gate` | done |
| `corpus/SOURCES.md`: S600 (`mined`) and S601 (`rejected`) appended after S599 | done, append-only, no existing byte changed |
| `corpus/knowledge/receipt-provenance-r85.md` with K1 (definition), K2 (verification-by-hash rule and its limits), K3 (this lane's frozen receipt grammar) | done, cites S600 in `source:` |
| Gate: ≥1 admit (S600) and ≥1 reject (S601), each with URL, access date and a ≤25-word located quote | done (21 and 12 words) |
| Census before the append and after, both pasted with rcs | done; rc 0 both times |
| `considerthese/2026-10-26.md` suggestion 3 recorded as a line in the lesson | done (see finding F4) |

Wrote exactly four files: the lesson, the registry append, the knowledge entry, and one pinned
source copy (`corpus/evidence/sources-r85/arXiv-2404.09241-abs.html`). Did not touch
`corpus/QUALITY.md`, `SKILL.md`, `SCORECARD.md`, any counter, any evidence receipt, or
`.ufo/state/`.

## 2. Gates — measured, not asserted

**Census.** `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root
/home/vgpnk/Projects/shokunin mori`, run from the fleet root.

| run | rc | summary line | rows | warnings |
|---|---|---|---|---|
| before append | 0 | `mori ok /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md` | 372 | 35, all `W04` duplicate-URL |
| after append | 0 | `mori ok /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md` | 374 | 35, all `W04` |

Zero `E` codes, zero `W01`/`W02`/`W03` in both runs; the two added rows introduce no new warning.
Rows counted with the contract's own grammar:
`grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` — the validator prints no
row count.

**Quote fidelity (measured on the pins, not on a summary).**

- S600 pin `corpus/evidence/sources-r85/rb-definition-1.html`, sha256
  `a558c89f5f27dffa69fd1dc49904179b60233bcfdfc64807abfe1acf37518ebb`, 37681 bytes, 3662 lines.
  Definition at raw lines 175-177 (`grep -n 'A build is'`), verification sentence at 196-197
  (`grep -n 'The reproducibility of artifacts'`). Four copies share the hash; three are
  `cmp`-identical.
- S601 pin `corpus/evidence/sources-r85/arXiv-2404.09241-abs.html`, sha256
  `4bcb20b23ad5046657a65a29595517da973128a289ff75ba13ad8926c5511a80`, 40386 bytes, 596 lines, live
  fetch HTTP 200, no redirect. Abstract body at line 121; the `<blockquote class="abstract mathjax">`
  opens at 120 and closes at 122.
- Wrote the pin with `cp` from scratch so the cited bytes are the fetched bytes; did not re-encode.

**Negative claims carry their sweeps.**

- "the page says nothing about receipts / attestations": `grep -o -i` on the S600 pin gives
  `receipt` 0, `attestation` 0, and `revision` 1 (the source-checkout sentence).
- "`tools/mori-claim-sweep.py` does not cover this class": its own docstring at
  `tools/mori-claim-sweep.py:10` names the default carriers
  `SCORECARD.md,SKILL.md,SHONEN.md,LOG.md`; `stale_literals` are pinned strings (`:150`).
- "15 arms at `5a231ef8`": `git show 5a231ef8:.ufo/waves/round-84/count-c1.py | grep -c
  'cases.append'` → 15; same command at `ab260865` → 15; `python3 -I
  .ufo/waves/round-84/count-c1.py --selftest | tail -1` → `C1_COUNTER_SELFTEST pass=15 fail=0`.
- "`corpus/QUALITY.md:1916` quotes `pass=11`": `git show ab260865:corpus/QUALITY.md | sed -n
  '1914,1916p'` → the `pass=11` line verbatim.

## 3. Touched surfaces

| path | change |
|---|---|
| `corpus/lessons/round-85.md` | new |
| `corpus/SOURCES.md` | +2 rows (S600, S601) between S599 and `## Paths`; nothing else |
| `corpus/knowledge/receipt-provenance-r85.md` | new |
| `corpus/evidence/sources-r85/arXiv-2404.09241-abs.html` | new pin (40386 bytes) |

`git status --porcelain` on the lane shows these plus siblings' files. No commit was made: the L1
owns every lane commit.

## 4. Findings

**F1 — the r84 stale-tally defect is reproducible by a lesson-level sweep.** The
`sweep` printed one `STALE` and two `DRIFT`s, all in QUALITY 172:
`C1_COUNTER_SELFTEST claimed=pass=11 measured=pass=15`, and the two pointers `:296-300` / `:301-313`
land on `ap.add_argument("--selftest", …)` / `ap.parse_args` and on `try:` / revision resolution
rather than on the stub gate (`:323-327`) and the detector gate (`:328-334`). The sweep is embedded
in the lesson with its full output; it is a detector, not a shipped tool, and says so. The
superseding criterion is QUALITY 173, landed by `Mo85S02Quality` and out of this seat's scope.

**F2 — `corpus/QUALITY.md` was being written while this seat measured it.** The worktree file is
`M` with mtime 2026-11-04 08:06:41 and carries a criterion 174 that is absent from
`ab260865:corpus/QUALITY.md` (`git show ab260865:corpus/QUALITY.md | grep -c '^174\. '` → 0). To
avoid grading a sibling's in-flight bytes, the sweep above runs against
`git show ab260865:corpus/QUALITY.md`. Recorded as an observation, not a defect: the file belongs to
another seat.

**F3 — the receipt harness named by the L1 and by QUALITY 175 is not on disk.**
`.ufo/waves/round-85/make-receipts.sh` is absent and `.ufo/waves/round-85/evidence/` holds only the
freeze controls and `rb-definition.html` at this seat's write time. The lesson's `considerthese` line
therefore cites `count-c2.py` (present, frozen at the freeze commit) and states the harness was not
present when the line was written. If the C2 seat lands it later, the lesson's sentence is
conservative, not wrong.

**F4 — `considerthese/2026-10-26.md` suggestion 3 is verified, not taken on trust.** Read at
`mori-shokunin/considerthese/2026-10-26.md`; the suggestion reads "Re-execute what closures only
evidence-verified. The r47–r49 closures say their verdicts come from committed receipts, not runs.
Off-host, I can rerun those frozen counters at the scored revision and report agreement or the exact
divergence, which covers the gap the closure names." The lesson records it, with the receipt rule as
the mechanism, and notes the absent harness (F3). No fleet-root `considerthese/` exists; the file is
inside the lane.

**F5 — an S601 nuance the row states and the lesson repeats.** The 40386-byte / sha256 `4bcb20b2`
reading reproduces the r84 screening value, but the row and the Gate rest on this seat's own fetch
(HTTP 200, no redirect), not on the r84 scout's.

## 5. Out of scope, routed not claimed

| item | owner | status in this seat |
|---|---|---|
| D84-2 superseding criterion | `Mo85S02Quality` | QUALITY 173 observed landed (uncommitted); not edited here |
| D84-1 (prompt committed by the lane identity) | L1 / integrator | untouched |
| D84-4 (uncommitted sweep receipts) | the C2 seat / L1 | untouched; this seat committed nothing by rule |
| D84-5 (battery receipt header) | the L1 | untouched |
| `corpus/QUALITY.md`, `SKILL.md`, `SCORECARD.md`, every counter | other seats | untouched, confirmed by `git status` |

## 6. Limits of this report

- The C1/C2/C3 after-values are not this seat's measurements. The lesson cites them only as context
  and the Gate does not rest on them.
- The sweep covers only criteria that quote a counter's own selftest token **and** cite that counter
  by `path:line` (`checked=1`). It does not grade criterion prose against tool output, and it does
  not resolve `.md`/`.txt` pointers written without their path.
- `W04` tolerance (35) is reported, not judged: those duplicates entered before this round and this
  seat added none.
- Row `used-by` for S600 is the single path the seat spec names
  (`corpus/knowledge/receipt-provenance-r85.md`); this lesson also cites S600 in its Gate and is
  deliberately not added, because the spec fixes the cell's value.

# Mo84S01Lesson — round-84 w1 scribe: round lesson + coverage row

round 84 (attempt 1), wave w1 · lane `/home/vgpnk/Projects/shokunin/mori-shokunin`
entering `5adf4337b6510dd246b247092c11cbaa97c930d3` · freeze `daa77bd5684c8db75eec1e80c87ee4fa5c3a6bb4`
Seat scope: prose only — no commit, no subagent, no counter or contract edit, no tool install, no
pacman transaction, no lane/OS/unit/service/credential state change.

## Produced (absolute paths)

1. `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/lessons/round-84.md` — **new**, 113 lines /
   10,032 bytes. Header block (round 84, date 2026-11-04, entering `5adf4337…`, freeze `daa77bd5…`),
   the three claims with keeper commands and the contract's **target** strings, one `## Mistakes`
   row (class · evidence pointer · captured-by `none` · fix), the census pasted verbatim with rc 0,
   a marked **AFTER (L1, integration)** slot, and a short list of L1-owned record slots. No
   `## Gate` section.
2. `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/README.md` — one appended section at lines
   891-895: `## Round-84 knowledge addition — equivalent-mutant adjudication (new growth, indexed
   the round it lands)`, naming `corpus/knowledge/equivalent-mutant-adjudication-r84.md` and source
   id `S599`. No other README line changed (`git diff --stat corpus/README.md` = `6 +`).

## Commands run and their output

Census (verbatim; tabs preserved in the lesson block, byte-check below):

```text
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori
mori	W04	S035 duplicate url raw.githubusercontent.com/systemd/systemd/cf8ebfc6159cf0b3b99aa9a0164ccb07c4c9c5af/catalog/systemd.catalog.in across scopes
… (35 W04 lines total; full text in corpus/lessons/round-84.md) …
mori	ok	/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md
rc=0
```

Row count (the separate grammar count, not printed by the validator):

```text
$ cd /home/vgpnk/Projects/shokunin/mori-shokunin && grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md
371          # before the S599 row landed; 372 re-measured after the row appeared (below)
```

Population control, run by this seat at the freeze commit (read-only; `TMPDIR` under own scratch):

```text
$ cd /home/vgpnk/Projects/shokunin/mori-shokunin && TMPDIR=$S/tmp python3 -I .ufo/waves/round-84/count-c1.py daa77bd5684c8db75eec1e80c87ee4fa5c3a6bb4
MUTANT count-c1.py M24a_killed_tally survived rc=0
EXTRA unanchored .ufo/waves/round-83/count-c1.py M24b_green_fail_token occurrences=2
EXTRA unanchored .ufo/waves/round-83/count-c2.py M24c_met_unclassified occurrences=0
EXTRA unanchored .ufo/waves/round-83/count-c2.py M24d_met_residual occurrences=0
C1=unmet mutants=1 killed=0 equivalent=0 survivors=1 total=1 pristine=green detector=green rev=daa77bd5684c
rc=1
$ # second run, same command
rc=1   # `diff run1 run2` → identical (deterministic)
```

Anchor counts at the freeze bytes (`git show daa77bd5:<path>` + `str.count`):

```text
$ cd /home/vgpnk/Projects/shokunin/mori-shokunin && git show daa77bd5:.ufo/waves/round-83/count-c1.py | grep -n 'fail=0" in out'
33:     'return rc == 0 and "fail=0" in out and not FAIL.search(out)',     # r82-counter MUTANTS row
34:     'return rc == 0 and "fail=0" in out'),
129:    return rc == 0 and "fail=0" in out and not FAIL.search(out)        # green() body
$ git show daa77bd5:.ufo/waves/round-83/count-c2.py | sed -n '241,242p'
    met = (hash_ok and asof_ok and bool(snapshot_tokens) and not unclassified
           and residual == 0 and malformed == 0 and duplicates == 0 and not stale
```

```text
M24a `killed_n = total - survivors - equivalent`            count=1   (line 191)
M24b green anchor                                          count=2   (:33 MUTANTS row, :129 body)
M24c/M24d `and not unclassified and residual == 0`         count=0   (met split at :241-242)
coupling `agreed == len(snapshot_tokens)`                  count=1
coupling `residual += duplicates`                          count=1
coupling `duplicates == 0`                                 count=1
```

Same counts measured at `c4845c83` (the revision the population was measured on): `c1-green=2`,
`c2-met=0`.

Graded r83 counter's own selftest at the freeze (pristine green, six arms — neither M24a nor M24b
arm is present):

```text
$ git show daa77bd5:.ufo/waves/round-83/count-c1.py > $S/r83/count-c1.py
$ TMPDIR=$S/tmp python3 -I $S/r83/count-c1.py --selftest --scratch $S/tmp | tail -1
C1_COUNTER_SELFTEST pass=6 fail=0
rc=0
```

Lesson census-block fidelity check (the pasted block against the captured stream, tabs included):

```text
byte-identical: True
```

Worktree state (read-only; other seats' files are **not** mine):

```text
$ git -C /home/vgpnk/Projects/shokunin/mori-shokunin status --porcelain
 M PROVINCE.md                                  # other seat
 M corpus/QUALITY.md                            # other seat
 M corpus/README.md                             # mine (1 appended section)
 M corpus/SOURCES.md                            # other seat (S599 row + search log)
?? .ufo/waves/round-84/w1.ready.dispatched      # other seat
?? .ufo/waves/round-84/w1/                      # other seat reports
?? corpus/evidence/sources-r84/                 # other seat (S599 pin)
?? corpus/knowledge/equivalent-mutant-adjudication-r84.md   # other seat / L1
?? corpus/lessons/round-84.md                   # mine (new)
```

Row count after the S599 row appeared: `372` (same grammar count). The lesson's **AFTER (L1)**
slot is left unfilled on purpose.

## Verified

- The census block in the lesson is byte-identical to the captured output (`body == raw` → True;
  tab separators preserved), and its exit code (`rc=0`) is the shell's, measured.
- The lesson's three target strings are copied from `contract.md` P-C1/P-C2/P-C3, not from any run;
  no after-value is asserted anywhere in the lesson.
- The lesson has no `## Gate`; the L1 slots section names Gate, after-block, wave settlement,
  SCORECARD/LOG and commits as L1-owned.
- The only files this seat wrote are the two named above; scratch is deleted (below).
- The C1 population-control reading is deterministic across two runs at the freeze commit.

## Not verified (stated, not implied)

- `S599`'s bytes, quote or admission: I did not fetch, open or re-quote the paper. The README row
  attributes only the cost/bias claim to `S599` and assigns the adjudication rule to the lane; the
  Gate's owner must confirm the attribution against the pinned copy.
- The after-values of any of the three counters at the integration revision (other seats; I ran
  only the C1 counter, and only as a read-only control reading).
- The content of `corpus/knowledge/equivalent-mutant-adjudication-r84.md` beyond reading it — it is
  L1/another seat's file and I did not edit it (see D84-S01-2).

## Defect found — the frozen C1 population is not gradable at the freeze bytes (D84-S01-1)

`contract.md` P-C1 freezes the population control at the freeze commit as `C1=unmet mutants=4
killed=0 equivalent=2 survivors=2` rc 1, and its predicate requires each `old` anchor to occur
exactly once at the graded revision. The committed freeze bytes do not have that property:

- `M24b_green_fail_token`'s `old` occurs **twice** in `.ufo/waves/round-83/count-c1.py` — as the
  r83 counter's own `MUTANTS` table row that grades the **r82** counter's `green()` (`:33`) and as
  the real `green()` body (`:129`).
- `M24c_met_unclassified` / `M24d_met_residual`'s `old` occurs **zero** times in
  `.ufo/waves/round-83/count-c2.py`: the `met` expression is split across `:241-242`, so the
  single-line string `and not unclassified and residual == 0` is absent.

Both counts are identical at `c4845c83`, the revision the population was measured on, and the r83
counter files are byte-identical at `c4845c83` and `daa77bd5`. Under P-C1's frozen rule —
"an anchor that does not occur exactly once is reported `unanchored` and never counted killed" and
"an unanchored anchor … keeps the claim unmet" — the counter prints `mutants=1` and `C1=unmet` on
these bytes no matter which arms land, because the C1 seat's stated edit (`selfcheck()` only, +2
arms) cannot change either count. **P-C1's target `C1=met mutants=4 …` is unreachable on the freeze
bytes.** Disposition options are the L1's: re-pin the two anchors to unique single-occurrence
strings in the r84 counter (a pre-data amendment, with the population unchanged) or record an
honest stop. This seat changed no counter byte; the conflict is recorded in the lesson's
`## Mistakes` block with the verbatim reading.

## Defect found — the r83 extra-mutant sweep's unicity claim, inherited by the r84 entry (D84-S01-2)

`.ufo/waves/round-83/w1/Mo83R01C1.md` §6 states: "both c1/c2 anchors verified unique by the driver
before mutation". The committed bytes at `c4845c83` contradict that for three of the four rows
(2 / 0 / 0 occurrences, above), so `M24b` cannot have been graded against a unique anchor and
`M24c`/`M24d` cannot have been applied at all (their reported `rc 0, pass=16 fail=0` is consistent
with an unmutated file). The r84 knowledge entry's K4 repeats the framing ("measured four extra
mutants beyond the frozen 23") without the caveat; that file is not this seat's to edit. Routed to
the L1 unmodified — the concept the entry states (K1-K3) is unaffected, the provenance sentence is.

## Out of scope / not done

- `## Gate`, SCORECARD, LOG, wave/seat settlement, `evidence/after-r84.txt`, and every commit: L1.
- No counter, contract, tool, PROVINCE, QUALITY, SOURCES or knowledge file written or reverted by
  this seat.
- Scratch `/fast/scratch/hyaku/mori-r84/Mo84S01Lesson` deleted before yield; no `/tmp` evidence was
  used or cited.
- No tool installed or upgraded; no pacman transaction; no network fetch.

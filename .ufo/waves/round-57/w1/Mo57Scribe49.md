# Mo57Scribe49 — round 57, C1 calibration: the two round-56 demonstrations vs. the frozen rows

Seat scope (as assigned): read the frozen contract, independently inspect the two
round-56 demonstrations (`driver-liveness`, `vote-binding`), verify the SCORECARD
capability row names and their evidence pointers, and report any false claim.
Detection and report only: no production edit, no commit, no jj, no counter
change, no fixture outside scratch, no subagent dispatch. Contract read first:
`.ufo/waves/round-57/contract.md:1-9` (C1 predicate at `:5`).

Entering branch revision `53e2b476`; freeze `618562c7` (HEAD = `618562c7`, clean
tracked tree; only round-57 wave files untracked).

Tooling: nothing installed or upgraded (python3 stdlib + `git`/`sha256sum` only;
pacman not run — it is paused). Scratch `/fast/scratch/hyaku/mori-r57/Mo57Scribe49/`
(`TMPDIR` set inside it, removed at the end). Disk guard checked before work:
`/fast/scratch/hyaku` 27% used, 588.9G free.

---

## 1. The two demonstrations, re-executed read-only

### 1a. driver-liveness (round-56 C1 surface)

```
$ cd /home/vgpnk/Projects/shokunin/mori-shokunin   # reads only; no lane-root write
$ S=/fast/scratch/hyaku/mori-r57/Mo57Scribe49; export TMPDIR=$S/tmp PYTHONDONTWRITEBYTECODE=1
$ python3 tools/mori-driver-liveness.py --selftest
DRIVER_LIVENESS_SELFTEST pass=13 fail=0 skipped=0        exit=0
$ python3 tools/mori-driver-liveness.py > $S/live-now.json 2> $S/live-now.err
exit=0   (stderr 0 bytes)
$ python3 - $S/live-now.json <<'PY'   # fields read out of the scratch capture
verdict DRIVER_LIVENESS_OK   schema mori-driver-liveness-v1   rc 0
lanes 23   log.lines 1742   log.malformed 0   log.other_lines 121
log.path /home/vgpnk/Projects/shokunin/.ufo/watchdog.log
state_dir {regular: 21, symlink: 0, dir: 0, other: 0}
mori {launches 67, completes 40, deads 17, launch_fails 0, wraps 0,
      in_flight true, unclosed 10, rounds_seen 47, last_launch_age_s 2966.892}
PY
```

Committed round-56 receipt `.ufo/waves/round-56/evidence/driver-liveness-live.txt`
(the JSON body plus `exit=0`): 1728 lines, malformed 0, other_lines 121, 23 lanes,
`state_dir.regular 21`, mori `launches 66 / completes 39 / unclosed 10 /
in_flight true`. Round-56 live-run report
`.ufo/waves/round-56/w1/Mo56ExecDriverLive.md` records three live runs, exit 0, and
`DRIVER_LIVENESS_OK` on all three.

Verdict **1a: CONFIRMED running, reproducible.** The tool executes today with the
same schema/verdict/lane set and 0 malformed. Differences from the receipt are the
append-only log (1728 → 1742 lines, mori launches 66 → 67) and ages — i.e. the
receipt is a stamped earlier read, not a fabricated constant.

Calibration note (LOW): `corpus/knowledge/driver-liveness-r56.md:58` says
"re-running the command reproduces it modulo ages". Line counts and per-lane event
counts also move as the log grows; only the shape facts (23 lanes, malformed 0,
other_lines 121 at this read) reproduced. Wording is stricter than the artifact.

### 1b. vote-binding (round-56 C2 surface)

```
$ python3 tools/mori-vote-bind.py --selftest
VOTE_BIND_SELFTEST pass=16 fail=0                        exit=0
$ python3 tools/mori-vote-bind.py tally \
    --ledger corpus/knowledge/kernel-v7.3-recheck-r55.md \
    --results .ufo/waves/round-55/w1-results.json --verb RECHECK \
    --voter Mo55Rc01 --voter Mo55Rc02 … --voter Mo55Rc16   # all sixteen flags, abridged
TALLY rows=78 agree=78 double=68 single=10 zero=0 dissent=0 voters=16 bound_voters=15
exit=0
```

That line is byte-identical to `.ufo/waves/round-56/evidence/tally-r55.txt:1`,
whose `:2` is `exit=0`. `.ufo/waves/round-56/evidence/selftest-vote-bind.txt:1-2`
records `VOTE_BIND_SELFTEST pass=16 fail=0` and `exit=0`. The demonstration is
report-level in `.ufo/waves/round-56/w1/Mo56ExecBinderSelftest.md` (selftest 3×,
extract over two synthetic outputs).

Verdict **1b: CONFIRMED running, reproducible.** Scope of the demonstration is a
16-case selftest plus a replay tally over committed round-55 bytes; it is **not** a
live scoring round. Round 56's own wave carried no vote items — the committed
`.ufo/waves/round-56/w1-results.json` has 64 seats with keys only
`agent, name, note, output` (0 seats carry any vote key), matching
`.ufo/waves/round-56/w1/Mo56ScribeBinderEntry.md:10`. Any row wording that implies
a round's votes were bound live would be a false claim.

### 1c. Tool pins

`sha256sum tools/{mori-driver-liveness,mori-vote-bind}.py` =
`6b3dba74…be997` and `8be1acdb…a6bca` = the frozen `PIN` values at
`.ufo/waves/round-56/count-c1.py:46` and `.ufo/waves/round-56/count-c2.py:46`.
Landed receipts `.ufo/waves/round-56/evidence/c1-at-landed.txt:1-2` and
`c2-at-landed.txt:1-2` both read `met … rev=097c342b…`, exit 0; `097c342b` is an
ancestor of HEAD.

## 2. Closure provenance for "first-working round 56" (not cited by any sibling report)

Fleet `MANIFEST.json` (fleet root `/home/vgpnk/Projects/shokunin`, committed at
fleet HEAD `661e5382`, path clean) records the round-56 closure at
`rounds[832]` (`MANIFEST.json:29093-29130`), `admitted: true`,
`capabilities_added` **two** entries at `MANIFEST.json:29114-29115`:

1. `dual-shape seat-output vote binding (tools/mori-vote-bind.py, 16/16 selftest, r55 tally re-bound 78/78 while the frozen r55 counter reads voted=0 on the same bytes)`
2. `strict per-event driver-liveness probe over .ufo/watchdog.log (tools/mori-driver-liveness.py, 13/13 selftest, live receipt 1728 log lines / 0 malformed / 23 lanes)`

So both capabilities are closure-admitted with first-working round 56, and the
register key syntax for them is `rounds[832].capabilities_added[0]` (vote-binding,
index order as filed) and `rounds[832].capabilities_added[1]` (driver-liveness).
Wording of the closure matches what I reproduced; no overclaim found.

## 3. SCORECARD state: what "the current capabilities table" resolves to

At HEAD `618562c7` (identical at the freeze and at entering tip):

- **Table A — placeholder**, `SCORECARD.md:596-602`: header
  `| Capability | What it can now do | Evidence pointer | First-working round |`
  with the single row `| — none yet — | | | |` at `:600`.
- **Table B — the register**, `SCORECARD.md:1951-1989`: header at `:1969`, data rows
  `:1971-1988`, columns `| key | capability | what it can now do | evidence | first-working round |`;
  18 data rows, first-working rounds `12,14,15,16,18,18,18,19,22,24,24,25,25,26,28,28,31,31`
  (last key `rounds[495].capabilities_added[1]`). Its own prose (`:1953-1967`)
  says it "is the lane's current capabilities register, the `capabilities` field of
  the AXES.md SCORECARD contract (S199)" and that it "supersedes the `— none yet —`
  table in the first `## Capabilities` section".
- **No row for either capability exists in either table** at HEAD (grep for
  `driver-liveness`/`vote-binding` hits only the round-56 section heading at
  `SCORECARD.md:2897` and its two claim rows at `:2903-2904`; those are claim rows
  under `| Claim | Axis | Counting command | Before | After |`, not capability rows).

Frozen C1 counter at both revisions (re-run read-only):

```
$ python3 .ufo/waves/round-57/count-c1.py 53e2b4768af93dd2472eb26ecc9b9fdca2e9daf2
C1=unmet rows=0 evidence=bad rev=53e2b4768af93dd2472eb26ecc9b9fdca2e9daf2   exit=1
$ python3 .ufo/waves/round-57/count-c1.py 618562c72a03dc4d17386b715357f863fd327274
C1=unmet rows=0 evidence=bad rev=618562c72a03dc4d17386b715357f863fd327274   exit=1
```

The control in `.ufo/waves/round-57/controls.txt` (`C1=unmet rows=0 evidence=bad`)
reproduces.

## 4. Counterexamples against the frozen counter's surface (scratch replay, no repo write)

`count-c1.py:10` is `s = out.split("## Capabilities", 1)[1].split("## Saturation", 1)[0]`.
On HEAD bytes the first `## Capabilities` is line 596 and the first `## Saturation`
after it is line 604, so the scored slice is the text between those two headings (`SCORECARD.md:597-603` plus its trailing blank; replay `slice_lines=8`).
I replayed the counter's exact predicate (lines 10-12) offline over
`git show HEAD:SCORECARD.md` plus synthetic insertions, in
`/fast/scratch/hyaku/mori-r57/Mo57Scribe49/`:

| case | placement of two correct rows | replay result |
|---|---|---|
| A | none (HEAD) | `unmet rows=0` |
| B | appended to **Table B** (the register, after data row `:1988`) | **`unmet rows=0`** (`slice_lines=8`) |
| C | appended to **Table A** (placeholder, after `:600`) | `met rows=2` |
| D | Table A, one row citing a **nonexistent** pointer `.ufo/waves/round-56/does-not-exist.txt` | **`met rows=2`** |

Consequences that must be reported verbatim, because the counter is frozen and
immutable after scoring:

1. **Rows entered where the SCORECARD says the current register is (Table B) score
   `C1=unmet rows=0`.** The verdict would then be an instrument artifact, not a
   missing demonstration.
2. **Rows entered in the superseded placeholder (Table A) score `met`** while
   Table B — the table the file itself calls current — still has no round-56 row,
   so a "capability entered the register" claim would rest on a table the file
   declares superseded.
3. `count-c1.py:12` checks only the substrings `.ufo/waves/round-56/` and `| 56 |`
   anywhere in the line; it never resolves the pointer (case D) and never checks
   which column `56` sits in. The predicate's clause "each with a **resolvable**
   round-56 evidence pointer" is therefore not enforced by the counter — a false
   pointer passes. (Critics 26/27 and MutationTester38 filed the same weakness
   independently; I confirm it and add the placement cases B/C.)

Also material to calibration: the register has been unmaintained since round 31.
Fleet `MANIFEST.json` records mori `capabilities_added` entries for rounds
36,37,38,39,40,41,43,48,49,53 and 56 — 11 rounds, 25 capability strings — none of which appear
as register rows (`rounds[798]` = round 53 is in MANIFEST but not in Table B). A
round-56 row would be the first register row in 25 rounds; the round-57 report must
not describe the register as otherwise current.

## 5. Row-naming constraint: unqualified names would make "first-working round 56" false

- **driver-liveness**: the census already read launch *epochs* from
  `.ufo/watchdog.log` for silence grading since round 2 — `corpus/README.md:345`
  ("the census's launch-epoch silence reading already existed (round 2)") and
  `corpus/knowledge/driver-liveness-r56.md:10-24`. Only the *strict per-event
  pairing* reader is new in round 56 (MANIFEST wording: "strict per-event
  driver-liveness probe").
- **vote-binding**: a single-shape (stripped text line only) binding existed at
  round 55 in `.ufo/waves/round-55/count-c1.py:284-302` (`def votes` /
  `l == "RECHECK %s %s"` or `startswith`), and it is why the round-55 arm read
  `voted=0` on JSON-wrapped outputs. Only the *dual-shape* binder is new in
  round 56 (MANIFEST wording: "dual-shape seat-output vote binding").

So a row that says just `driver-liveness` or `vote-binding` with
first-working `56` overclaims. A truthful row keeps the qualifier in the name or
the "what it can now do" cell, e.g.
`driver-liveness (strict per-event pairing)` / `vote-binding (dual-shape: stripped
text line + JSON string scalar)`, and the contract's literal tokens
(`driver-liveness`, `vote-binding`) are still present as substrings — I checked
that both qualified spellings satisfy `count-c1.py:11-12` substring tests.

## 6. Resolvability of candidate round-56 evidence pointers (checked at HEAD)

`git cat-file -e HEAD:<path>` **OK** for every candidate below; contents verified
in §1:

| capability | candidate pointer | resolves | content check |
|---|---|---|---|
| driver-liveness | `.ufo/waves/round-56/evidence/driver-liveness-live.txt` | yes | live JSON receipt, 1728 lines / 0 malformed / 23 lanes; reproduced modulo log growth |
| driver-liveness | `.ufo/waves/round-56/evidence/c1-at-landed.txt` | yes | `C1=met … rev=097c342b…`, exit 0 (rev-stamped) |
| driver-liveness | `.ufo/waves/round-56/w1/Mo56ExecDriverLive.md` | yes | three live runs, 3/3 checks |
| vote-binding | `.ufo/waves/round-56/evidence/tally-r55.txt` | yes | frozen TALLY line + `exit=0`; reproduced byte-identically |
| vote-binding | `.ufo/waves/round-56/evidence/selftest-vote-bind.txt` | yes | `pass=16 fail=0`, exit 0; reproduced |
| vote-binding | `.ufo/waves/round-56/evidence/c2-at-landed.txt` | yes | `C2=met … rev=097c342b…`, exit 0 (rev-stamped) |
| either | `corpus/knowledge/{driver-liveness,vote-binding}-r56.md`, `tools/mori-{driver-liveness,vote-bind}.py` | yes | tool shas equal the round-56 pins |

Note the raw live/tally receipts carry no revision stamp; the `*-at-landed.txt`
receipts do. Pointer choice is a wording decision for the claim owner, not a gap.

## 7. Findings

- **INFO / no false claim in the demonstrations.** Both round-56 capabilities run
  today and reproduce their committed evidence assertions; MANIFEST `rounds[832]`
  records both as closure-admitted with first-working round 56. The C1 claim's
  *substance* (two capabilities, round-56 evidence, first-working 56) is true.
- **HIGH (instrument)** — `count-c1.py:10` slices from the first `## Capabilities`
  (line 596) to the first `## Saturation` (line 604); the register at
  `SCORECARD.md:1951-1989` is invisible. Rows placed where the SCORECARD says the
  current register is score `C1=unmet rows=0`; only the superseded placeholder
  slice can produce `met`. Frozen counter, so the after-state verdict must be read
  with this in view (Reviewer09 filed the slice defect too; cases B/C/D above are
  the measured consequence).
- **MED** — `count-c1.py:12` accepts a nonexistent `.ufo/waves/round-56/` pointer
  (case D), so the predicate clause "resolvable round-56 evidence pointer" is not
  measured; a row must be judged by manual resolution (§6).
- **MED (calibration)** — unqualified row names (`driver-liveness`,
  `vote-binding`) with first-working `56` would be false: the census launch-epoch
  reading exists since round 2 (`corpus/README.md:345`) and a single-shape vote
  binding exists since round 55 (`.ufo/waves/round-55/count-c1.py:284-302`). Rows
  must keep the "strict per-event" / "dual-shape" qualifiers.
- **LOW** — `corpus/knowledge/driver-liveness-r56.md:58` ("reproduces it modulo
  ages") understates drift: line and event counts move with the append-only log
  (1728 → 1742 lines at this read).
- **LOW (register hygiene)** — the register's last row is first-working round 31
  while MANIFEST carries 25 capability strings across rounds 36-56; a round-56 entry
  would not make the register current, and the report must not imply it does.

## 8. Limits / not done

- Did not touch `SCORECARD.md`, the counters, the contract, or any tracked file;
  no commit, no jj, no push. Report is the only lane write.
- Did not re-derive the round-56 counters themselves beyond the two landed
  receipts' text; `count-c1.py`/`count-c2.py` (round 56) were read only for the
  `PIN` lines.
- Did not audit C2 (the `unclosed` depth axis) or its predicate
  (`count-c2.py`, round 57) — owned by other seats.
- Did not verify fleet `MANIFEST.json` provenance beyond reading the committed
  block at fleet HEAD `661e5382` (path clean); its `verification` prose was not
  re-executed.
- The scratch replay uses `git show HEAD:SCORECARD.md` bytes plus synthetic rows;
  it is not a committed fixture and asserts no git mutation. Scratch removed.

Report: `.ufo/waves/round-57/w1/Mo57Scribe49.md` (relative to
`/home/vgpnk/Projects/shokunin/mori-shokunin`).

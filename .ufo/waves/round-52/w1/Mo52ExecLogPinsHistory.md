# Mo52ExecLogPinsHistory — calibration history: are LOG.md's command-tally pins true when written?

Seat: Mo52ExecLogPinsHistory (wave w1, mori round 52). Scope assigned: "LOG.md holds 10 command-tally pins
… enumerate them with the counter's LPIN regex imported from `.ufo/waves/round-52/count-c1.py`. For each, find
the round's landed commit … run the pinned command in a `git archive` of that commit under your scratch …
and report pinned vs observed. Were the dated records true when written?"

Nothing in the lane was written except this file. No tool installed or upgraded (no install was needed; `unshare`,
`bwrap` and `python3` were already present). Scratch `/fast/scratch/hyaku/mori-r52/Mo52ExecLogPinsHistory/`
removed at the end of the seat (see §9). Contract read: `.ufo/waves/round-52/contract.md` (frozen at `d3a8ea59`);
its C1 K4 scope paragraph is the rule this seat tests: LOG.md tallies are dated records, K4 does not run them.

## 1. Enumeration

LPIN is `count-c1.py:76-78` (submitted: a backticked command containing `--selftest`, followed on the **same line**
by `(a/b)` or `→ pass=N fail=M`). Importing it (module-level import, `main` guarded at `count-c1.py:785`) against
LOG.md at HEAD `075436b1` gives **four** hits:

```
count 4
2224 '`--selftest` → `pass=6 fail=0`'
2295 '`python3 tools/mori-sources-appendonly.py --selftest` → `pass=15 fail=0`'
2332 '`--selftest` → `CONFORM_SELFTEST pass=14 fail=0`'
2642 '`--selftest` → `C1_SELFTEST pass=16 fail=0`'
```

The ten records the seat names are the lines that carry an observed tally, `pass=\d+ fail=\d+` — exactly ten lines
in LOG.md: `2224, 2257, 2263, 2286, 2295, 2332, 2339, 2454, 2457, 2642`. Six of the ten were written wrapped (the
command on one line, its tally on the next), so LPIN cannot see them (finding F1). Two more (`2454`, `2457`) are
prose tallies with no backticked command at all; they are the "two more" the seat counted. Enclosing heading per
line: 2224→`## Round 38`, 2256/2262→`## Round 39`, 2285/2295→`## Round 40`, 2332/2338→`## Round 41`,
2454/2457→`### Round-42 measured outcome`, 2642→`## Round 45`.

Out of scope, with reason: `2026` (round 31) pins `--selftest` PASS with no tally; `2672` (round 47) *quotes* a stale
SKILL pin inside a sentence (`SKILL.md:912` pinned `…pass=15…` since round 40) — a quotation, not a pin; `11, 14,
139, 208, 258` are census `(N cases)` pins with no `pass=/fail=` tally.

## 2. Method (and the one deviation from the seat text)

- Revision per pin = the commit that **introduced the line** (`git blame -L <line>,<line> -- LOG.md`), i.e. "when
  written". The seat's alternate heuristic `git log --format=%H -1 --grep='round-N'` returns the round's
  *non-author verifier* commit for every round (38→`3f232c3e`, 39→`bb1f2457`, 40→`62a207f7`, 41→`9de7323d`,
  42→`e3a2b58f`, 45→`9834fed4`), which is *after* the LOG entry; I verified the pin lines are byte-identical at
  those commits (`git show <rev>:LOG.md | sed -n '<a>,<b>p'`), so either revision tests the same text.
- **Deviation:** the conform selftests were run in a **worktree of a `--shared` clone** checked out at that commit,
  not in a bare `git archive` extraction. Cause: `conform.py`'s `head_pin` check runs `git -C <repo> rev-parse HEAD`
  and its timed arms run the counter at a revision, so a non-git tree cannot serve as `--repo`. Measured, not
  assumed — same selftest, same bytes, `--repo` = the archive tree:

  ```
  CMD: python3 .ufo/waves/round-39/conform.py HEAD --selftest --repo <archive tree> --counter <archive>/.ufo/waves/round-39/count-c7.py
  FAIL head_pin           pin label renamed -> failing=['head_pin', 'timeout_state']
  …
  CONFORM_SELFTEST pass=0 fail=9
  ```

  One clone only (`git clone --shared <lane> <scratch>/clone`, 0 bytes of object copy); `rev-parse --show-toplevel`
  printed the clone path before first use.
- The gate selftest (`tools/mori-sources-appendonly.py --selftest`) needs no git context and was run in the same
  worktree with `TMPDIR` in scratch.
- **Lane-write containment.** The round-38..42 instruments hardcode `LANE = "/home/vgpnk/Projects/shokunin/mori-shokunin"`
  and write their selftest work dirs under `<lane>/.ufo/waves/round-N/scratch` (`conform.py:38/53-54/69-70`,
  counters' `SCRATCH_ROOT = os.path.join(DEFAULT_REPO, …)`), ignoring `--repo` and `TMPDIR`. Every run therefore
  went through `unshare -rm --propagation private` + `mount --bind <scratch>/shadow/waves <lane>/.ufo/waves`
  (harness `runpin.sh`). Isolation proved by probe, not assumed:

  ```
  unshare -rm … bash -c 'mount --bind <shadow>/waves <lane>/.ufo/waves; touch <lane>/.ufo/waves/round-39/scratch/NS-PROBE'
  host_check: ls: cannot access '<lane>/.ufo/waves/round-39/scratch/NS-PROBE': No such file or directory
  <shadow>/waves/round-39/scratch/NS-PROBE   (present)
  ```

- Note what this means for reproduction: the literal command as printed in LOG (`… --selftest`, no revision, no
  `--counter`) **exits 2** on r38 and r39 — the selftest passes `rev=None` into the timed arm:

  ```
  $ cd tree-b6993744 && python3 .ufo/waves/round-38/conform.py --selftest
  conformance setup error: expected str, bytes or os.PathLike object, not NoneType
  RC=2
  ```

  The runnable form is the one the receipts record, e.g. round 38's
  `.ufo/waves/round-38/evidence/c5-after-selftest.txt:1`:
  `command: python3 .ufo/waves/round-38/conform.py f725f307… --selftest --counter .ufo/waves/round-38/count-c1.py`.

## 3. Pinned vs observed (all ten)

All runs: `cwd` = clone worktree at the introducing commit, `TMPDIR` = scratch, mount namespace with the lane's
`.ufo/waves` bound to a scratch shadow. `<clone>` below elides the scratch path.

| # | LOG line | R | Introduced by | Command run (HEAD = that commit) | Pinned tally | Observed | rc |
|---|---|---|---|---|---|---|---|
| 1 | 2224 | 38 | `b6993744` | `.ufo/waves/round-38/conform.py HEAD --selftest --counter .ufo/waves/round-38/count-c1.py --repo <clone> --contract <clone>/.ufo/waves/round-38/contract.md` | `` `pass=6 fail=0` `` | `CONFORM_SELFTEST pass=6 fail=0` (6 PASS, 0 FAIL) | 0 |
| 2 | 2256-57 | 39 | `f920eaf7` | `.ufo/waves/round-39/conform.py HEAD --selftest --repo <clone>` | `CONFORM_SELFTEST pass=9 fail=0` | `CONFORM_SELFTEST pass=9 fail=0` (9 PASS) | 0 |
| 3 | 2262-63 | 39 | `f920eaf7` | `tools/mori-sources-appendonly.py --selftest` | `` `pass=12 fail=0` `` | `MORI_SOURCES_APPENDONLY_SELFTEST pass=12 fail=0` | 0 |
| 4 | 2285-86 | 40 | `8d3badd0` | `.ufo/waves/round-40/conform.py HEAD --selftest --repo <clone>` | `CONFORM_SELFTEST pass=11 fail=0` | `CONFORM_SELFTEST pass=11 fail=0` (11 PASS) | 0 |
| 5 | 2295 | 40 | `8d3badd0` | `tools/mori-sources-appendonly.py --selftest` | `` `pass=15 fail=0` `` | `MORI_SOURCES_APPENDONLY_SELFTEST pass=15 fail=0` | 0 |
| 6 | 2332 | 41 | `aa161e99` | `.ufo/waves/round-41/conform.py HEAD --selftest --repo <clone>` | `CONFORM_SELFTEST pass=14 fail=0` | `CONFORM_SELFTEST pass=14 fail=0` (14 PASS) | 0 |
| 7 | 2338-39 | 41 | `aa161e99` | `tools/mori-sources-appendonly.py --selftest` | `MORI_SOURCES_APPENDONLY_SELFTEST pass=22 fail=0` | `MORI_SOURCES_APPENDONLY_SELFTEST pass=22 fail=0` | 0 |
| 8 | 2454 | 42 | `f3ec0977` | `.ufo/waves/round-42/conform.py HEAD --selftest --repo <clone>` | `selftest pass=17 fail=0` (v5) | `CONFORM_SELFTEST pass=17 fail=0` (17 PASS) | 0 |
| 9 | 2457 | 42 | `f3ec0977` | `tools/mori-sources-appendonly.py --selftest` | `gate selftest pass=22 fail=0` | `MORI_SOURCES_APPENDONLY_SELFTEST pass=22 fail=0` | 0 |
| 10 | 2642 | 45 | `12c89ea6` | `.ufo/waves/round-45/count-c1.py --selftest` run at `baabc992` (the revision the record names) | `C1_SELFTEST pass=16 fail=0` | `C1_SELFTEST pass=16 fail=0` (16 PASS, 0 FAIL) | 0 |

Cross-check on instrument bytes: every instrument blob is identical between the LOG-introducing commit and the
round's own instrument/measurement commit, except round 38's `conform.py`, which differs
(`b6993744:c62fcabd…`, `f725f307:c57ad5a1…`); pin 1 was therefore run **twice**:

```
$ … runpin.sh f725f307 "…" -- python3 .ufo/waves/round-38/conform.py HEAD --selftest --counter .ufo/waves/round-38/count-c1.py --repo <clone> --contract <clone>/.ufo/waves/round-38/contract.md
CWD=…/clone HEAD=f725f3076972e6e70595b5ac8279be524a111ff8
PASS predicate      predicate token changed -> only predicate failed
…
PASS scratch        scratch parent moved off-lane -> only scratch failed
CONFORM_SELFTEST pass=6 fail=0
RC=0
```

Blob parity otherwise: r39 `conform.py` `99ab4fef…` and gate `d2c96160…` at `f920eaf7` = at `13bfba23`; r40
`71fa5977…`/`9f292909…` at `8d3badd0` = at `265a955c`; r41 `3b67d958…` at `aa161e99` = at `7450722e`, gate
`887fd85d…` at `aa161e99`/`f3ec0977` = at `d72ac167`; r42 `conform.py` `8add90f0…` at `f3ec0977` = at `34b92673`;
r45 `count-c1.py` `cf3a8d53…` at `12c89ea6` = at `baabc992`.

Representative verbatim output (pin 10, the only record whose counter builds throwaway repos):

```
CWD=…/clone HEAD=baabc9929f0f272f3a99cd0a7816a2cb35fda835
selftest PASS honest_ledger_met
selftest PASS offbyone_row_mismatch
selftest PASS junk_producer_rejected
selftest PASS below_floor_rejected
selftest PASS absent_ledger_unmet
selftest PASS duplicate_id_rejected
selftest PASS duplicate_command_rejected
selftest PASS head_reading_row_rejected
selftest PASS revision_constant_row_rejected
selftest PASS witness_dir_one_passing_witness
selftest PASS all_const_ledger_unmet
selftest PASS const_heavy_ledger_unmet
selftest PASS witness_without_floor_unmet
selftest PASS stage_option_injection_rejected
selftest PASS short_sha_tip_rejected
selftest PASS absent_path_zero_rejected
C1_SELFTEST pass=16 fail=0
RC=0
```

Pin 1 first form, at the LOG-introducing commit:

```
CWD=…/clone HEAD=b6993744   (conform.py c62fcabd…)
PASS predicate      predicate token changed -> only predicate failed
PASS head_pin       pin label renamed -> only head_pin failed
PASS tool_resolve   relative resolution removed -> only tool_resolve failed
PASS bounded_reads  git helper run timeout removed -> only bounded_reads failed
PASS timeout_state  budget flag ignored -> only timeout_state failed
PASS scratch        scratch parent moved off-lane -> only scratch failed
CONFORM_SELFTEST pass=6 fail=0
RC=0
```

## 4. Answer

**Yes — all ten dated records were true when written, and each is reproducible today from its own commit.** Ten of
ten tallies agree exactly (pass count and fail count); all runs exit 0. No record overstates or understates its
instrument's arm count. The one drift the lane already knows about is between rounds, not inside a record: the gate
grew 12→15→22 arms between rounds 39/40 and 41, and each LOG entry pins the arm count of the tool at that round
(round 40's `pass=15` and round 41's `pass=22` both reproduce, matching the round-47 note that this pin moved only
because the tool grew).

**K4 scope decision holds.** Running these ten commands adds no discrimination the round needs: they are dated
records of instrument state at a past revision, and each is stable at its own commit. A living-document pin differs
— it is a command a reader runs *today* against *today's* tree — which is exactly the QUALITY/README class C1
already covers. Nothing here argues for running LOG.md in K4.

## 5. Precision defects in the records themselves (named limits, not claim changes)

1. **LPIN sees 4 of 10** because six pins are wrapped across two lines; the contract's named limit ("a pin split
   across lines is not enumerated") is measured here, not hypothetical — 6/10 of LOG's pins are invisible to it.
   K4 does not read LOG.md, so this changes no C1 number, but it bounds any future proposal to point an LPIN-class
   arm at LOG.md.
2. **The bare `--selftest` form does not run** (exit 2, §2). LOG prints the abbreviation, not the invocation; only
   some rounds have a receipt with the literal command (`c5-after-selftest.txt:1` has it; round 39's
   `c8-after-selftest.txt:1` reads `command: r39 conform --selftest at f920eaf7` and names no counter and no
   revision). This is the same defect class round 52's C1 list already works on the living documents
   (`README.md:607` pins a bare `--selftest`); LOG carries it too, un-routed so far.
3. **Rounds 42's two tallies are prose, not command pins** (`2454` "v5 selftest pass=17 fail=0", `2457` "gate
   selftest pass=22 fail=0" from `evidence/c1-noharm-manual.txt`). They reproduce, but neither line tells a reader
   what to run; the receipt `c1-noharm-manual.txt:4` likewise records the result without a command line.
4. **Round 45's `C1_SELFTEST pass=16 fail=0` has no evidence receipt**: `git grep C1_SELFTEST 12c89ea6 --
   .ufo/waves/round-45 .ufo/waves/round-46` finds the print statement (`count-c1.py:1097`), a mutant copy, and
   `evidence/write-scope.txt:78,251` = `pass=6`, `:307` = `pass=10` (other instruments), plus one wave seat's
   transcript `.ufo/waves/round-45/w1/CritAxisHarm.md:75` (`$ python3 .ufo/waves/round-45/count-c1.py --selftest →
   C1_SELFTEST pass=16 fail=0`). The record's tally is true (measured, §3) but rests on a seat report, not on an
   `evidence/` receipt — round-51 routed defect 7 ("every receipt records its literal command line") does not cover
   a measurement with no receipt at all.

## 6. Observed lane state during the wave (not this seat's writes)

At 21:19–21:23 local, untracked scratch dirs appear in the lane while this seat ran: `mori-shokunin/.ufo/waves/
round-39/scratch/mori-conform-selftest-*` (mtimes 21:18:53 → 21:24:31; the directory held 3 at 21:19:15, 5 at
21:19:34 and 6 at 21:24:31 — entries appear and are reaped as the peer runs finish) and new
untracked files `.ufo/waves/round-52/r39-conform-selftest.sh`, the latter a peer wrapper that documents the same
hardcoded-lane-path problem. A `ps -eo pid,etimes,args` snapshot at 21:23:09 shows four live
`python3 .ufo/waves/round-39/conform.py 4f266ef2… --selftest` and one
`python3 .ufo/waves/round-40/conform.py 8524904a… --selftest` with relative instrument paths — those runs write
their work dirs into the **real** lane scratch root whatever `TMPDIR` says. This seat's runs are excluded: the
namespace probe in §2 shows a write at that path landing in the shadow. Also present at HEAD during my read:
`M corpus/README.md` (working-tree modification, not mine) and untracked `.ufo/waves/round-52/check-history-rows.py`,
`evidence/m2-history-rows.txt` (other seats' drafts). I wrote none of these and removed none of them.

## 7. What this seat did not do

No claim scoring, no counter or predicate change proposed (the counters are frozen), no edits to LOG.md,
SCORECARD.md, SHONEN.md, QUALITY.md, README.md, `corpus/`, `tools/` or any other `.ufo/waves/round-52` file, no
git mutation in the lane or the fleet repo (only `log/show/diff/rev-parse/ls-tree/ls-files/grep/blame/archive` and
one `clone --shared` into scratch), no host writes, no privilege beyond `unshare`/`mount` inside a private mount
namespace. UNVERIFIED: whether the round-38/39/40 `SCRATCH_ROOT` parents existed
before this wave (they are untracked and carry old mtimes inside, so pre-existing rows are likely; I did not date
them individually).

## 8. Findings

- **F1 (LOW) — `.ufo/waves/round-52/count-c1.py:76-78` (LPIN)**: the pin regex requires the tally on the same line
  as the backticked command, so it enumerates 4 of LOG.md's 10 tally pins; the other 6 are wrapped. Harmless for C1
  (K4 does not read LOG.md) but it bounds any successor arm pointed at LOG.md. Evidence: §1 import run, §3 table.
- **F2 (LOW) — `LOG.md:2224, 2256, 2262, 2285, 2295, 2332, 2338`**: LOG prints the abbreviation `--selftest`; the
  runnable form is `conform.py <rev> --selftest --counter <path>`. Following the printed form exits 2
  (`conformance setup error: expected str, bytes or os.PathLike object, not NoneType`). The tallies are true; the
  printed command is not runnable. Same class as the `README.md:607` mismatch C1 already carries.
- **F3 (LOW) — `LOG.md:2454, 2457`**: round 42's two tallies are prose with no command text, and their receipt
  `.ufo/waves/round-42/evidence/c1-noharm-manual.txt:4` records the gate tally without the command line. Reproduce
  only with knowledge from other rounds' receipts.
- **F4 (LOW) — `.ufo/waves/round-45/evidence/`**: the round-45 record `LOG.md:2642` (`C1_SELFTEST pass=16 fail=0`)
  has no evidence receipt; only `w1/CritAxisHarm.md:75` records the tally, and `evidence/write-scope.txt` records
  `pass=6`/`pass=10` for other instruments. Measured true; receipted nowhere in `evidence/`.
- **F5 (MED) — `.ufo/waves/round-39/scratch/` (and by construction round-38/40) is written by live wave seats**:
  `mori-conform-selftest-*` dirs appear in the real lane at 21:18:53–21:23:08 while four `round-39/conform.py …
  --selftest` processes run from other seats; the instruments' hardcoded `SCRATCH_ROOT` (`conform.py:54` etc.)
  defeats `TMPDIR` and `--repo`. This is the contract §5 item-8 in-lane-writer class, live during w1, and it makes
  any `lane_writes` arm's silence depend on who else is running. Not caused by this seat (namespace probe, §2).
- **F6 (LOW) — `LOG.md` pin hygiene**: no pin in LOG.md names the revision it was measured at; the `## Round N`
  heading (and the round's own instrument commit) is the only anchor. Round 38 shows why that matters: the
  instrument bytes at the LOG-introducing commit differ from the round's instrument commit (`c62fcabd…` vs
  `c57ad5a1…`), so "run the pin at the commit that wrote the line" and "run it at the round's instrument commit"
  are two different tests; both give `pass=6 fail=0` here, but nothing in the record forces that.

## 9. Scratch, tooling, cleanup

Scratch `/fast/scratch/hyaku/mori-r52/Mo52ExecLogPinsHistory/` (`tmp/`, `runs/`, six `git archive` trees,
`clone/` (one `--shared` clone), `shadow/`, `shadow2/`, `runpin.sh`); `TMPDIR` pointed inside it for every run;
disk-guard checked before the heavy runs (`/fast/scratch/hyaku 24% use, 614.7G free`). Removed with `rm -rf` at
seat end; no file written to `/tmp`, no unbounded stream to disk, nothing written under `/home/vgpnk/Projects/
shokunin` outside this report.

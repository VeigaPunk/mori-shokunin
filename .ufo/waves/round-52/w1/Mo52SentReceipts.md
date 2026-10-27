# Mo52SentReceipts — receipt integrity (round-51 closure routed defect 7: literal commands)

Seat: Mo52SentReceipts (leaf; no subagents). Data revision measured: `8524904adb25e44f24d9f25aac7eae909625c18c`
(entering tip `4f266ef2fdf74d8b046f5b4f5a5c4945f65b966d`, freeze `d3a8ea5957b73bddbde750a8c0af2fba8da8b7c2`).
Question asked: for every file under `.ufo/waves/round-52/evidence/` at the data commit — does it record the literal
command it ran (no `<scratch>`-style placeholder without a stated rule), does it record an exit code, and does
re-running the command reproduce the verdict line?

Method: one `git clone --shared` of the lane into
`/fast/scratch/hyaku/mori-r52/Mo52SentReceipts/clone` (toplevel asserted equal to the clone before use), all runs
with `TMPDIR=/fast/scratch/hyaku/mori-r52/Mo52SentReceipts/tmp` and `PYTHONDONTWRITEBYTECODE=1`; counters run from
the clone as `python3 .ufo/waves/round-52/<counter>.py …`, i.e. the recorded command line with the lane replaced by
the clone (for `count-c1.py` I had to add `--fleet-repo /home/vgpnk/Projects/shokunin`, because the default fleet is
`dirname(--repo)` and my clone's parent is not the fleet root — the recorded at-data command relied on being run
*inside* the lane). Frozen instrument bytes used for the control rebuilds were extracted from `d3a8ea59` and their
sha256 checked against `evidence/freeze-sha256.txt`:
`ff9500a5…f120  c1-data.py`, `e8649227…c300  count-c1.py`. Nothing was written into the lane; the lane's working
state after my seat is the same 70 untracked paths it had on entry (plus sibling reports written meanwhile).

## 1. Inventory (21 files: the 16 present at `8524904`, plus 4 added by `075436b1`, plus 1 untracked)

`literal` = the file carries a `$` command line with no placeholder; `exit` = the file records `exit=`/`rc=`;
`repro` = my re-run reproduced the recorded verdict line.

| # | file (`.ufo/waves/round-52/evidence/…`) | in `8524904` | literal | exit | repro |
|---|---|---|---|---|---|
| 1 | `census-start.txt` | yes | yes (abs. path) | `exit=0` | **yes**, 24 lines byte-identical, rc 0 |
| 2 | `control-c1-do-nothing.txt` | yes | yes | `exit=1` | **yes** after rebuild; literal re-run exits 2 (paths gone) |
| 3 | `control-c1-axes-only.txt` | yes | yes | `exit=1` | **yes** after rebuild (item lines identical) |
| 4 | `control-c1-receipts-only.txt` | yes | yes | `exit=1` | **yes** after rebuild |
| 5 | `control-c1-living-only.txt` | yes | yes | `exit=1` | **yes** after rebuild |
| 6 | `control-c1-rewrite-in-place.txt` | yes | yes | `exit=1` | **yes** after rebuild |
| 7 | `control-c1-delete-stale-pins.txt` | yes | yes | `exit=1` | **yes** after rebuild |
| 8 | `control-c1-repeat-stale-tally.txt` | yes | yes | `exit=1` | **yes** after rebuild (twice) |
| 9 | `control-c1-witness.txt` | yes | yes | `exit=0` | **4 of 5**; one attempt read `C1=unmet … mismatches=1` |
| 10 | `control-c2-do-nothing.txt` | yes | yes | `exit=1` | **yes**, line byte-identical, rc 1 |
| 11 | `freeze-sha256.txt` | yes | **no** (digest list, no `$`) | **no** | **yes**: 24/24 digests match at `8524904` |
| 12 | `selftest-c1.txt` | yes | yes | `exit=0` | **yes**, 43 lines identical (`C1_SELFTEST pass=42 fail=0`) |
| 13 | `selftest-c2.txt` | yes | yes | `exit=0` | **yes**, 46 lines identical (`C2_SELFTEST pass=45 fail=0`) |
| 14 | `selftests/mori-pin-check.txt` | yes | **placeholder** | `rc=0` | **yes**, byte-identical (`PIN_CHECK_SELFTEST pass=125 fail=0`) |
| 15 | `selftests/mori-unlanded-check.txt` | yes | **placeholder** | `rc=0` | **yes**, byte-identical (`UNLANDED_SELFTEST pass=17 fail=0`) |
| 16 | `sweep-overcommit.txt` | yes | **no** (no `$` at all) | **no** | **yes** (content reconstructed, see §2.6) |
| 17 | `c1-at-data.txt` | **no** (`075436b1`) | yes | `exit=0` | **yes**, 43 lines identical (`C1=met … mismatches=0`) |
| 18 | `c2-at-data.txt` | **no** (`075436b1`) | yes | `exit=1` | **yes**, line identical (`entailed=0 … failed=entailment`) |
| 19 | `c2-hashes-at-data.txt` | **no** (`075436b1`) | yes | `exit=0` | **yes**, all 28 `row=… hash=…` lines identical |
| 20 | `m2-history-rows.txt` | **no** (untracked) | yes (2 lines, no cwd) | `exit=1`/`exit=0` | **yes** after copying the untracked instrument |
| 21 | `w1-validate-refused.txt` | **no** (`075436b1`) | **no** (JSON only) | **no** | **not run** (harness validator; input spec destroyed) |

## 2. Reproduction detail

### 2.1 Counters at the data commit

```
$ cd /fast/scratch/hyaku/mori-r52/Mo52SentReceipts/clone
$ python3 .ufo/waves/round-52/count-c1.py 8524904adb25e44f24d9f25aac7eae909625c18c \
      --fleet-repo /home/vgpnk/Projects/shokunin --scratch /fast/scratch/hyaku/mori-r52/Mo52SentReceipts/c1data
C1=met items=42 axes=6 pins=2 boxes=4 living=7 superseded=4 locators=27 mismatches=0 errors=0 hidden=0 \
    lane_writes=0 manifest=6209bdb8e400 rev=8524904adb25e44f24d9f25aac7eae909625c18c
exit=0                                            # diff vs c1-at-data.txt (minus "$ " and "exit="): IDENTICAL
$ python3 .ufo/waves/round-52/count-c2.py 8524904adb25e44f24d9f25aac7eae909625c18c
C2=unmet claims=28 located=28 quote_missing=0 bad_rows=0 sources=5 source_rows=ok pins=ok provenance=ok \
    entailed=0 dissent=0 rev=8524904adb25e44f24d9f25aac7eae909625c18c failed=entailment
exit=1                                            # IDENTICAL to c2-at-data.txt
$ python3 .ufo/waves/round-52/count-c2.py --hashes 8524904adb25e44f24d9f25aac7eae909625c18c
row=1 hash=9afaa81505da …  row=28 hash=42295e410c2b  (28 lines)  exit=0   # IDENTICAL, 28/28
$ python3 .ufo/waves/round-52/count-c1.py --selftest   → C1_SELFTEST pass=42 fail=0   exit=0   # IDENTICAL
$ python3 .ufo/waves/round-52/count-c2.py --selftest   → C2_SELFTEST pass=45 fail=0   exit=0   # IDENTICAL
```

### 2.2 The eight C1 controls (rebuilt, because the recorded clones and control commits are gone)

The recorded literal command of every control names a clone and a `--scratch` under
`/fast/scratch/hyaku/mori-r52/l1/controls/…` that no longer exists, and the control commits it names are not
reachable from the lane (`git cat-file -e <rev>^{commit}` fails for all seven: `bbe377b1`, `e8501017`, `6b9eab63`,
`18091f0a`, `424af172`, `953559c3`, `398c720e`). Re-running a recorded line verbatim therefore fails before doing
any work (no write, the scratch dir is created only after the rev resolves):

```
$ cd /home/vgpnk/Projects/shokunin/mori-shokunin && python3 .ufo/waves/round-52/count-c1.py \
    bbe377b10951ac1344da86603faf1ba27dd9be17 \
    --repo /fast/scratch/hyaku/mori-r52/l1/controls/clone-axes-only \
    --fleet-repo /home/vgpnk/Projects/shokunin \
    --scratch /fast/scratch/hyaku/mori-r52/l1/controls/c1-axes-only
C1_SETUP cannot resolve rev
exit=2
```

Each control was rebuilt in my single clone with the frozen applier and the frozen counter
(`python3 <frozen>/c1-data.py $C <parts>`; `git -C $C -c user.name=mori-control -c user.email=control@mori.invalid
commit`; `python3 <frozen>/count-c1.py <newrev> --repo $C --fleet-repo <fleet> --scratch …`), then the `item` lines
were diffed against the receipt's:

| control | rebuilt rev | reproduced verdict (mine) | item lines vs receipt |
|---|---|---|---|
| do-nothing | `4f266ef2` (lane commit, no rebuild) | `C1=unmet items=37 … living=4 superseded=1 locators=25 mismatches=8 … lane_writes=0 manifest=6209bdb8e400 rev=4f266ef2… failed=mismatch` exit 1 | **identical** |
| axes-only | `f02fd7da86d7…` | `items=39 … locators=27 mismatches=5 …` exit 1 | identical |
| receipts-only | `535b4aecb705…` | `items=37 … mismatches=6 …` exit 1 | identical |
| living-only | `9ffff9401580…` | `items=40 … living=7 superseded=4 locators=25 mismatches=5 …` exit 1 | identical |
| rewrite-in-place | `134e6543fcf8…` | `items=42 … living=4 superseded=1 locators=27 mismatches=3 …` exit 1 | identical |
| delete-stale-pins | `9577970e00bd…` | `items=39 … living=1 superseded=1 locators=27 mismatches=3 …` exit 1 | identical |
| repeat-stale-tally | `5a0d2ee0d03c…` | `items=42 … living=7 superseded=4 locators=27 mismatches=3 …` exit 1 | identical (twice) |
| witness | `2807d71a5209…` | `C1=met items=42 … mismatches=0 errors=0 hidden=0 lane_writes=0` exit 0 | identical (4 of 5 runs) |

Every recorded control reading in `contract.md`'s control table reproduced. The `rev=` field is the one field that
cannot reproduce, because the control commits are rebuilt (different committer clock): this is expected from the
contract's own note that the control commits "are not reachable from the lane".

Witness, the one non-reproducing attempt (the second of five):

```
$ python3 <frozen>/count-c1.py 664317c515ac30d438a09c49d052a953b2ae720c --repo <clone> \
      --fleet-repo /home/vgpnk/Projects/shokunin --scratch <scratch>/c1-witness
item living corpus/README.md:728 expect=CONFORM_SELFTEST_pass=9_fail=0 got=no_tally_rc=2 state=mismatch
C1=unmet items=42 axes=6 pins=2 boxes=4 living=7 superseded=4 locators=27 mismatches=1 errors=0 hidden=0 \
    lane_writes=0 manifest=6209bdb8e400 rev=664317c5… failed=mismatch
exit=1
```

Direct run of the same pinned command in an archive of the same revision, immediately afterwards:

```
$ git -C <clone> archive 664317c515ac30d438a09c49d052a953b2ae720c | tar -x -C <scratch>/wtest/tree
$ cd <scratch>/wtest/tree && TMPDIR=<scratch>/wtest/tmp \
      python3 .ufo/waves/round-39/conform.py 4f266ef2fdf74d8b046f5b4f5a5c4945f65b966d --selftest
PASS predicate … PASS selftest_conjunct
CONFORM_SELFTEST pass=9 fail=0
conform rc=0
```

The pinned command is therefore sound; the run is not bit-stable under host load. The counter keeps the failing
command's output (`stderr=subprocess.STDOUT`, `count-c1.py:549`) but prints only the parsed tally state, so the
receipt cannot say *why* a pinned command failed — `no_tally_rc=2` is all a reader gets.

### 2.3 Both SHONEN receipts (placeholder command)

```
$ cd <lane checkout at d3a8ea5957b73bddbde750a8c0af2fba8da8b7c2> && python3 tools/mori-pin-check.py --selftest
PIN_CHECK_SELFTEST pass=125 fail=0        rc=0     # reproduced byte-identically (128 lines, 125 PASS)
$ cd <lane checkout at d3a8ea5957b73bddbde750a8c0af2fba8da8b7c2> && python3 tools/mori-unlanded-check.py --selftest
UNLANDED_SELFTEST pass=17 fail=0          rc=0     # reproduced byte-identically (17 PASS)
```

Re-run from `git -C <clone> archive d3a8ea59 | tar -x -C <scratch>/tree-d3a8ea59`, cwd = that tree. The `<lane
checkout at …>` token is a placeholder but names the exact commit, and it is emitted by the frozen applier
(`controls/c1-data.py:101`: `"$ cd <lane checkout at %s> && python3 %s --selftest"`), so it is a stated rule, not an
unnamed scratch path. The only difference from the receipt is the trailing `rc=0` line, which the wrapper writes
outside the captured command output.

### 2.4 Census

```
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori
mori  W04 … (23 lines) ; mori ok /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md
rc=0                                              # 24 lines, IDENTICAL to census-start.txt (minus "$ "/"exit=")
```

### 2.5 Freeze digests

All 24 paths listed in `evidence/freeze-sha256.txt` hash to the listed value when read at `8524904`
(`git show 8524904:<path> | sha256sum`): contract, both counters, both control scripts, `build-w1-spec.py`, 12
evidence files and the five `corpus/evidence/sources-r52/` copies. `0` mismatches.

### 2.6 Sweep (no command recorded)

`sweep-overcommit.txt` has no `$` line and no exit code: only a `#` description ("git grep -l -F, files per term")
and the counts. Reconstructed and re-run at `4f266ef2`:

```
$ for t in CommitLimit Committed_AS overcommit_memory overcommit_ratio overcommit_kbytes vm_commit_limit \
           __vm_enough_memory vm_committed_as user_reserve_kbytes admin_reserve_kbytes MAP_NORESERVE \
           OVERCOMMIT_NEVER overcommit-accounting; do
    printf '%s %s\n' "$t" "$(git -C <clone> grep -l -F -- "$t" 4f266ef2 -- corpus/SOURCES.md corpus/knowledge SKILL.md | wc -l)"; done
CommitLimit 0 / Committed_AS 0 / … / overcommit-accounting 0        # all 13 counts identical to the receipt
$ git -C <clone> ls-tree -r --name-only 4f266ef2 -- merge/mori | wc -l      → 0
$ git -C <clone> grep -l -F -- CommitLimit 4f266ef2 -- merge/mori            → (none)
```

The content reproduces, but the `merge/mori` block is vacuous: `merge/mori` does not exist at that revision (or on
disk) — 0 files in total, so "0 files on the theme" cannot distinguish an unmined theme from an absent package.

### 2.7 M2 history rows (instrument not committed)

`check-history-rows.py` and its receipt are both untracked in the lane (`git ls-files --error-unmatch` fails;
`git status` shows `?? …/check-history-rows.py` and `?? …/evidence/m2-history-rows.txt`), so the receipt cannot be
reproduced from any commit. I copied the working-tree instrument into the clone at the same relative path and ran
the two recorded lines there (instrument derives its repo from its own path):

```
$ python3 .ufo/waves/round-52/check-history-rows.py 4f266ef2… --applier
HISTORY_ROWS changed=6 lines=[1058, 1060, 1205, 1206, 1652, 1656]
exit=1
$ python3 .ufo/waves/round-52/check-history-rows.py 4f266ef2… 8524904…
HISTORY_ROWS changed=0 lines=[]
exit=0
```

Both lines reproduce exactly. Neither line states its working directory; the relative script path only works from
the lane root.

### 2.8 `w1-validate-refused.txt` (not reproducible)

Line 1 is `{"schema":"ufo-swarm-wave-error-v1","code":"unknown_role","message":"items[39].role \"labrat\" is not a
swarm role"}` — no command, no exit code. The validator is the harness's wave-spec validator (no copy exists under
`/home/vgpnk/Projects/shokunin/{scripts,mori-shokunin/scripts}`; the string occurs only in session transcripts), and
re-invoking it would dispatch a wave, so I did not run it. The *input* is also gone: `w1-spec.json` was overwritten
in place by `build-w1-spec-amend.py`. Static consistency check only: the frozen builder carries exactly one `labrat`
item (`build-w1-spec.py:138`, `add("LabLaneWrites", "labrat", …)`) and the dispatched spec at `075436b1` has 68
items, no `labrat` role, and `items[39] = Mo52LabLaneWrites / executor` — consistent with the refusal and the
one-item amend, but not a reproduction.

## 3. What the receipts' own fields do not prove

`count-c1.py` measures "the pinned commands wrote into the lane" as a before/after sample of
`git status --porcelain --ignored --untracked-files=all` (`count-c1.py:531`, `:562`). One pinned command writes into
the lane *during* every C1 run and is gone before the after-sample:

```
$ git -C <clone> show 4f266ef2:.ufo/waves/round-39/conform.py | sed -n '53,54p;491,492p'
LANE = "/home/vgpnk/Projects/shokunin/mori-shokunin"
SCRATCH_ROOT = os.path.join(LANE, ".ufo", "waves", "round-39", "scratch")
    os.makedirs(SCRATCH_ROOT, exist_ok=True)
    work = tempfile.mkdtemp(prefix="mori-conform-selftest-", dir=SCRATCH_ROOT)
```

Observed in the lane while my witness runs were measuring, and empty (`0` entries) a minute later:

```
$ ls -la --time-style=full-iso /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-39/scratch
drwxr-xr-x … 2026-10-26 21:32:0… mori-conform-selftest-_fy18seq
$ git -C /home/vgpnk/Projects/shokunin/mori-shokunin status --porcelain --untracked-files=all -- .ufo/waves/round-39
?? .ufo/waves/round-39/scratch/
```

every one of those runs still reported `lane_writes=0`. Two consequences for this round's receipts: `lane_writes=0`
does not certify that the pinned commands are read-only on the lane, and the same arm can be *tripped* by a sibling
seat's transient conform run (`.ufo/waves/round-52/r39-conform-selftest.sh`, 21:22, untracked, not mine, is another
seat's workaround for exactly this hardcoding). The same hardcoded `LANE` also means the `README.md:728` pin is not
"run at R": it validates the lane's current `.ufo/waves/round-39/{count-c7.py,contract.md}` whatever revision is
measured.

## Findings

- **MED** — `.ufo/waves/round-52/evidence/c1-at-data.txt`, `c2-at-data.txt`, `c2-hashes-at-data.txt`: the three
  receipts that pin the claim readings "at data" are **not in the data commit** `8524904`; they were added by
  `075436b1` (the w1 spec/dispatch commit) and are absent from `freeze-sha256.txt`. Their content names
  `8524904`, and all three reproduce, but a reader at the data revision sees no receipt there.
  (`git log 075436b1 --diff-filter=A -- …` → `075436b1` for all three.)
- **MED** — `.ufo/waves/round-52/evidence/m2-history-rows.txt` plus its instrument
  `.ufo/waves/round-52/check-history-rows.py`: both untracked in the lane worktree, the instrument in no commit and
  not in `freeze-sha256.txt`. The receipt's reading (`changed=6 lines=[1058,1060,1205,1206,1652,1656]`, then
  `changed=0`) is reproducible only by copying a mutable working-tree file; an edit to that uncommitted instrument
  changes the reading with no committed record. Reproduced both lines exactly after copying it.
- **MED** — pinned command `corpus/README.md:728` (`python3 .ufo/waves/round-39/conform.py 4f266ef2… --selftest`)
  hardcodes the lane (`conform.py:53-54`) and writes `…/<lane>/.ufo/waves/round-39/scratch/mori-conform-selftest-*`
  (`:491-492`) in every C1 measurement, ignoring `TMPDIR`; consequently `lane_writes=0` in
  `control-c1-*.txt`, `c1-at-data.txt` is a before/after sampling claim that cannot see this transient write
  (`count-c1.py:531,562`), and that pin measures the lane's live round-39 files rather than R.
- **MED** — `control-c1-witness.txt:1,46` (`C1=met … mismatches=0`, `exit=0`) reproduced 4 of 5 times; one run read
  `item living corpus/README.md:728 … got=no_tally_rc=2 state=mismatch` and `C1=unmet … mismatches=1`. The counter
  captures the failing command's output (`count-c1.py:549`) but never prints it, so the receipt cannot explain the
  failure; a direct run of the same pinned command in the same archive reads `rc=0 CONFORM_SELFTEST pass=9 fail=0`.
- **LOW** — `.ufo/waves/round-52/evidence/sweep-overcommit.txt:1-18`: records no command line and no exit code
  (routed defect 7 asks for a literal command), contrary to the other receipts. Content reproduces (13 terms, all
  0); its `merge/mori` block is vacuous because `merge/mori` has 0 files at `4f266ef2`.
- **LOW** — `.ufo/waves/round-52/evidence/freeze-sha256.txt`: a digest list with no command/exit (acceptable), but it
  does not cover `evidence/selftests/mori-pin-check.txt` and `evidence/selftests/mori-unlanded-check.txt`, which
  ship in the data commit and are exactly what the SHONEN receipts arm reads; both reproduced byte-identically.
- **LOW** — `evidence/selftests/mori-pin-check.txt:1` and `mori-unlanded-check.txt:1` record
  `$ cd <lane checkout at d3a8ea59…> && …`: a placeholder, not a literal path. The rev is named inside the
  placeholder and the token is generated by the frozen `controls/c1-data.py:101`, so it is a stated rule; both
  reproduced byte-identically.
- **LOW** — `control-c1-*.txt:2`: every control's literal command is no longer runnable as written (its `--repo`
  clone and `--scratch` were removed by design; the seven control commits are unreachable and
  `C1_SETUP cannot resolve rev, exit=2` is what a verbatim re-run prints today). Reproduction required rebuilding
  the controls with the frozen applier; all eight then matched the receipts item for item, and only the `rev=` field
  differs.
- **LOW** — `evidence/w1-validate-refused.txt:1`: no command, no exit code, and its input `w1-spec.json` was
  overwritten in place by `build-w1-spec-amend.py`, so the refusal cannot be re-executed from recorded bytes.
  Static consistency only (frozen builder has one `labrat` item at `build-w1-spec.py:138`; dispatched spec has none
  and puts `Mo52LabLaneWrites/executor` at index 39).

Scratch `/fast/scratch/hyaku/mori-r52/Mo52SentReceipts/` (clone 334 M, archives, rerun captures) was removed after
the runs; every command and verdict line cited above is quoted in this report.

# Mo52ScribeShonen — SHONEN.md round-52 box draft (wave w1)

Seat: `Mo52ScribeShonen` (scribe, leaf). Round 52, wave `w1`. No claim is scored here and **no frozen predicate,
counter, floor or kill rule is touched or proposed for change**; the C1/C2 predicates, counters, controls and kill
rules are frozen and were only read and run.

Measured revisions:

- R = data commit `8524904adb25e44f24d9f25aac7eae909625c18c`; entering tip `4f266ef2fdf74d8b046f5b4f5a5c4945f65b966d`.
- Lane working tip when this seat ran: `075436b1` (round-52 wave spec). `SHONEN.md` is byte-identical at
  `4f266ef2`, at R and at `075436b1` (`git diff 4f266ef2 8524904a -- SHONEN.md` is empty; blob
  `67527182c6ac021e66225680147f9a4fdef05307` at both R and HEAD; `sha256(SHONEN.md) = 6786f3bd3f36b826…`).
- Scratch `/fast/scratch/hyaku/mori-r52/Mo52ScribeShonen/`, `TMPDIR` inside it, removed at the end (`disk-guard.sh`
  status before the work: `/fast/scratch/hyaku 26 % used, 599.6 G free`).

Everything below is command + output + exit code from this seat; anything I could not check is marked UNVERIFIED.

## 1. What SHONEN.md is at R, and what its evidence is

`SHONEN.md` at R is the 8-line promotion checklist: one title line, one lede, and **four** `- [~]` boxes. Each box
carries a `path:N[-M]` pointer and, in box 3, the two tally pins. At R the boxes still lead with **round 51**
(`SKILL.md:1069-1141`, `LOG.md:2765-2805`) — the data commit added the round-52 receipt *files* under
`.ufo/waves/round-52/evidence/selftests/` but did not change a SHONEN byte (`git log --oneline -6 -- SHONEN.md`
shows the last SHONEN commit as `8e3df7e5`, round 51).

The two pins and their numbers, as the frozen counter reads them at R
(`.ufo/waves/round-52/evidence/c1-at-data.txt`):

```
item pin python3_tools/mori-pin-check.py_--selftest expect=(125/125) got=PIN_CHECK_SELFTEST_pass=125_fail=0 state=ok
item pin python3_tools/mori-unlanded-check.py_--selftest expect=(17/17) got=UNLANDED_SELFTEST_pass=17_fail=0 state=ok
```

I re-ran both instruments myself against the working tree (lane, `TMPDIR` in scratch):

```
$ cd /home/vgpnk/Projects/shokunin/mori-shokunin && python3 tools/mori-pin-check.py --selftest | tail -2
PASS cli_bad_rev_rc2  rc=2
PIN_CHECK_SELFTEST pass=125 fail=0            # real 0m14.293s, rc=0
$ python3 tools/mori-unlanded-check.py --selftest | tail -2
PASS cli_usage_rc2  rc=2
UNLANDED_SELFTEST pass=17 fail=0              # real 0m0.168s, rc=0
```

Both round-52 receipt files named by the draft hold exactly the observed line:

```
$ ls .ufo/waves/round-52/evidence/selftests/
mori-pin-check.txt   mori-unlanded-check.txt
$ tail -2 .ufo/waves/round-52/evidence/selftests/mori-pin-check.txt
PIN_CHECK_SELFTEST pass=125 fail=0
rc=0
$ tail -2 .ufo/waves/round-52/evidence/selftests/mori-unlanded-check.txt
UNLANDED_SELFTEST pass=17 fail=0
rc=0
```

No seat in the round-52 wave changes either tool: of the 68 seats in `.ufo/waves/round-52/w1-dispatch.json`, the
only operability seat on them is `Mo52ExecPinCheckNoHarm`, which runs them read-only against R. So 125/125 and 17/17
are stable for the landed tip (barring an L1 edit of `tools/`, which would be outside the contract).

## 2. The draft (fenced; one line per box)

Whole `SHONEN.md`, 8 lines / 1946 bytes, `sha256 = 9f00937c27a8dc7cd1202fb4f7eb6187a90620794d4baa37853e2254baffffdc`.
Every box keeps its existing pointers and leads with the round-52 evidence.

```
# mori-shokunin — Promotion checklist

Promotion to shokunin requires all of:

- [~] SKILL.md contains real decision tables, error patterns, checklists, cited sources — `SKILL.md:1143` (Round52 section: the overcommit-ledger decision rows and the calibration mismatch classes); `SKILL.md:1069-1141` (Round51: runway decision row, pin mismatch classes); `SKILL.md:1018-1067` (Round50); `corpus/QUALITY.md:1252-1352`
- [~] At least one end-to-end domain task executed and logged in LOG.md — `LOG.md:2807` (Round 52: overcommit entry with per-row entailment votes, the two pins re-run at the data tip); `LOG.md:2765-2805` (Round 51: MemAvailable entry with per-row entailment votes, hermetic pin re-execution); `LOG.md:2732-2763` (Round 50)
- [~] Instructions executable by an agent without oral context — `python3 tools/mori-pin-check.py --selftest` (125/125); `python3 tools/mori-unlanded-check.py --selftest` (17/17); round-52 receipts `.ufo/waves/round-52/evidence/selftests/mori-pin-check.txt`, `.ufo/waves/round-52/evidence/selftests/mori-unlanded-check.txt` (both pins re-run at the round-52 data tip); round-51 receipts `.ufo/waves/round-51/evidence/selftests/mori-pin-check.txt`, `.ufo/waves/round-51/evidence/selftests/mori-unlanded-check.txt` (round-51 C1: pin-check v5/v5.1 add eleven arms)
- [~] No cross-domain bleed (PROVINCE.md still accurate) — `corpus/knowledge/overcommit-commit-limit-r52.md:68-75` Boundaries (v7.2 ledger bytes only; no host sysctl value claimed and no threshold proposed; choosing the overcommit mode is the operator's); `PROVINCE.md:3-16` unchanged; `corpus/knowledge/quota-observability-r48.md` Boundaries (read-only, no quota command run); `corpus/knowledge/oom-memcg-stat-r50.md` Boundaries (cgroup limit configuration is tsukuroi's); `corpus/knowledge/memavailable-estimate-r51.md` Boundaries (OS state is tsukuroi's to diagnose, the operator's to change; the hyaku gates are the orchestrator's)
```

## 3. Box → leading round-52 pointer → what verifies it

| box | new leading pointer | the pointed-at bytes at R / after integration | verifier |
|---|---|---|---|
| 1 | `SKILL.md:1143` | the `## Round52` section (drafted by `Mo52ScribeSkill`; SKILL.md has 1141 lines at R, ends in `\n`, line 1068 is the blank separator before `## Round51` at 1069 — so heading-first append puts the heading at 1143) | `count-c1.py` arm (D) with the section landed; placement confirmed by the drafting seat (see §6) |
| 2 | `LOG.md:2807` | the `## Round 52 (L1 MoriR52, attempt 1; C1 calibration, C2 depth)` entry (LOG.md has 2805 lines at R; 2764 is the blank separator before `## Round 51` at 2765) | arm (D) with the entry landed; placement confirmed by `Mo52ScribeLog` (see §6) |
| 3 | the two pins + `.ufo/waves/round-52/evidence/selftests/{mori-pin-check,mori-unlanded-check}.txt` | the round-52 receipts exist at R and hold `PIN_CHECK_SELFTEST pass=125 fail=0` / `UNLANDED_SELFTEST pass=17 fail=0` | arm (B): `run(["python3", path, "--selftest"])` + `got in receipt lines` |
| 4 | `corpus/knowledge/overcommit-commit-limit-r52.md:68-75` | `## Boundaries` (line 68) and its four bullets: v7.2 bytes only / per-CPU `Committed_AS` / ptrace + hugetlb `MAP_NORESERVE` holes / no threshold proposed (file has 75 lines at R) | arm (D) range check; wording checked against the file |

Pointer hygiene, measured with the frozen counter's own parsers (`count-c1.py` `parse_shonen`, `LOC`, `PIN`):

```
$ python3 loc-dependency.py SHONEN.draft.md          # imports the frozen count-c1.py, read-only
draft pins=2 boxes=4 hidden=0
  pin tools/mori-pin-check.py 125 125
  pin tools/mori-unlanded-check.py 17 17
```

- `hidden=0`: the draft adds no `(N/M)`, `pass=N` or `SELFTEST` token outside the two pin spans.
- No arm-D quote trigger: the draft contains **zero** double-quote characters (`grep -c '"' SHONEN.draft.md` → `0`),
  and the single occurrence of the word `proposed` is not followed by `digits → digits`, so every new pointer is
  range-checked only — the mode the six existing box pointers already use.
- Pin form is exact: `bound_path` accepts only `argv == ["python3", "<repo-relative .py>", "--selftest"]`, and both
  spans are exactly that, followed by `(N/M)`.

## 4. Feasibility run (fixture, disclosed — this is **not** the claim's landing)

The two new pointers cannot resolve at R by construction (R has no `## Round52` and no `## Round 52`), so I measured
the draft the way the L1 will land it: one `git clone --shared` of the lane in scratch, the drafted `SHONEN.md`, and
**stub** `## Round52` / `## Round 52` sections appended at EOF to make the pointers resolvable. The stubs stand in
for the sibling seats' drafts; they are not proposed text.

```
$ S=/fast/scratch/hyaku/mori-r52/Mo52ScribeShonen; export TMPDIR=$S/tmp
$ git clone -q --shared /home/vgpnk/Projects/shokunin/mori-shokunin $S/clone   # exit 0
$ git -C $S/clone rev-parse --show-toplevel
/fast/scratch/hyaku/mori-r52/Mo52ScribeShonen/clone                          # asserted == $D before any commit
$ printf '\n## Round52 — …\n\nStub section …\n'   >> $D/SKILL.md
$ printf '\n## Round 52 (L1 MoriR52, attempt 1; C1 calibration, C2 depth)\n\nStub entry …\n' >> $D/LOG.md
$ grep -n '^## Round52' $D/SKILL.md ; grep -n '^## Round 52' $D/LOG.md
1143:## Round52 — …            # 1142 blank separator; SKILL.md now 1145 lines
2807:## Round 52 (…)            # 2806 blank separator; LOG.md now 2809 lines
$ cp $S/SHONEN.draft.md $D/SHONEN.md
$ git -C $D -c user.name=Mo52ScribeShonen -c user.email=scribe@localhost commit -qam "feasibility: SHONEN round-52 boxes"
```

Run 1 (`8efadfa7d324123dd50df13747f5a6eb24f7286b`, box-4 wording before the final sentence was tightened) and run 2
(`cfc899d1393704943fc39802999f0c7beb390d0b`, the exact bytes in §2):

```
$ python3 $D/.ufo/waves/round-52/count-c1.py <commit> --repo $D \
    --fleet-repo /home/vgpnk/Projects/shokunin --scratch $S/c1run
C1=met items=45 axes=6 pins=2 boxes=4 living=7 superseded=4 locators=30 mismatches=0 errors=0 hidden=0 lane_writes=0 manifest=6209bdb8e400 rev=8efadfa7d324123dd50df13747f5a6eb24f7286b   exit=0 (1m9.3s)
C1=met items=45 axes=6 pins=2 boxes=4 living=7 superseded=4 locators=30 mismatches=0 errors=0 hidden=0 lane_writes=0 manifest=6209bdb8e400 rev=cfc899d1393704943fc39802999f0c7beb390d0b   exit=0 (1m9.6s)
```

`locators=30` = the 27 at R plus the three new box pointers (`SKILL.md:1143`, `LOG.md:2807`,
`overcommit-commit-limit-r52.md:68-75`); the other 21 Axes-row locators and the three quote/pair items read
`state=ok` unchanged. Both pin items read `state=ok`; `lane_writes=0` in both runs.

The dependency, measured at R against the drafted bytes with the frozen counter's own `check_locators` (no stub
sections present):

```
$ python3 loc-dependency.py SHONEN.draft.md     # read_at(8524904a, path) via `git show`
  locator SKILL.md:1143 - out_of_range_len=1141 mismatch
  locator LOG.md:2807 - out_of_range_len=2805 mismatch
  locator SKILL.md:1069-1141 … corpus/QUALITY.md:1252-1352 … LOG.md:2765-2805 … LOG.md:2732-2763 …
  locator corpus/knowledge/overcommit-commit-limit-r52.md:68-75 range ok ok
  locator PROVINCE.md:3-16 range ok ok
len SKILL.md 1141   len LOG.md 2805   len corpus/QUALITY.md 1373
len corpus/knowledge/overcommit-commit-limit-r52.md 75   len PROVINCE.md 400
```

So exactly two pointers depend on the integration, and they depend only on **line placement**, not on content.

## 5. Integration instruction for the L1 (the only thing needed to make the draft green)

1. Append the `## Round52` section to `SKILL.md` at EOF after one blank line → its heading must be line **1143**
   (if the L1 inserts anything between the old EOF and the heading, or omits the blank separator, renumber box 1 to
   the heading's actual line and leave everything else alone).
2. Append the `## Round 52 …` entry to `LOG.md` at EOF after one blank line → heading at **2807** (same renumbering
   rule).
3. Keep `corpus/knowledge/overcommit-commit-limit-r52.md:68-75` (`## Boundaries` + four bullets) as landed at R — it
   is already correct and requires no renumbering.
4. Do not edit the pins or the receipt paths: the numbers come from the two instruments and the receipts at R.

## 6. Placement confirmation from the drafting seats

- `Mo52ScribeSkill` (message, 2026-10-26): SKILL.md at `8524904a` is 1141 lines, line 1141 is 88 chars, the file's
  last byte is `\n`, the round-50/51 boundary is one blank line then the heading (1068 blank, 1069 `## Round51`);
  "your pin `SKILL.md:1143` is correct for my draft unchanged", heading at 1143, last drafted line at 1206, block
  contains no `path:N` locator into SKILL.md. Caveat it names: an inserted lede or an extra blank line shifts 1143
  and 1206 together.
- `Mo52ScribeLog` (message, 2026-10-26): LOG.md is 2805 lines, ends with a newline, one blank line separates entries
  (2764 blank, 2765 heading), its draft starts with the heading line, so appended at EOF after one blank line the
  heading lands at `LOG.md:2807`; the 2765-2805 and 2732-2763 ranges stay valid.

Both are the seats' own statements, not my observation of their drafts (I did not read their fenced text into this
report).

## 7. Named limits of this draft (mine; no counter change requested)

1. Box 1's parenthetical ("the overcommit-ledger decision rows and the calibration mismatch classes") describes a
   section that does not exist yet; if `Mo52ScribeSkill`'s rows differ in substance, the L1 must reconcile the words,
   not the pointer.
2. Box 2's parenthetical likewise describes the pending LOG entry; it claims only what R already shows (the entry,
   the per-row entailment votes, the pins re-run at the data tip) and nothing that lands after it.
3. The arm (D) check on the two new pointers is a **range** check: it proves the lines exist, not that they hold the
   Round52 section. A heading that lands one line late reads `out_of_range_len` and fails loudly; a heading that
   lands two lines early inside another section's tail would pass silently. This is the frozen instrument's named
   limit ("other prose before a pointer is range-checked"), reported, not changed.
4. `hidden=0` is measured by the frozen regexes only; a tally token written differently (e.g. "125 of 125") would not
   be seen by arm (B). The draft introduces none.

## 8. What this seat did not do

- No file in `/home/vgpnk/Projects/shokunin/mori-shokunin` or `/home/vgpnk/Projects/shokunin` was created, edited or
  deleted except this report: `git -C …/mori-shokunin status --porcelain` after the work lists the other seats'
  untracked `w1/*.md` (and my own report), with no SHONEN/SKILL/LOG change; no `git add/commit/stash/checkout/reset/
  pull/push` and no `jj` command was issued in either repo (the one clone in scratch is the only repo I committed in,
  after asserting `rev-parse --show-toplevel`).
- `/home/vgpnk/Projects/shokuknow` untouched; no host write of any kind (this seat ran no host read beyond
  `disk-guard.sh status` and `uname`-free tool runs); no pacman, no install or upgrade (nothing needed), no
  `~/.local/bin` write, no kernel-log message text grepped.
- No subagent dispatched (leaf seat).

## Findings

- **LOW** — `SHONEN.md`, box 3 (line 8 of the file at R): the checklist box still cites only
  `.ufo/waves/round-51/evidence/selftests/…` while the round-52 receipts it is now scored against live under
  `.ufo/waves/round-52/evidence/selftests/`. Arm (B) reads the round-52 files directly, so nothing fails — the box
  text understates the evidence it relies on. The draft in §2 closes this by naming the round-52 receipts first and
  keeping the round-51 pair as history.
- **LOW** — `SKILL.md`/`LOG.md` round-52 sections are the only two pointers in the draft that resolve only after
  integration: `SKILL.md:1143` and `LOG.md:2807` (out of range at R: `out_of_range_len=1141` / `=2805`). The frozen
  arm (D) cannot distinguish a one-line placement drift from a missing section for a start-only pointer; the L1 must
  set each number to the heading's actual line (rule in §5). Instrument note only — no counter change requested this
  round.
- **LOW** — `tools/mori-round13-regressions.py:171,1600-1637,3231`: the claim `R13_SHONEN_CANONICAL_BYTES` compares
  the file named by `--shonen` (default `REPO/SHONEN.md`, i.e. the lane file) byte-for-byte against the frozen
  four-line `CANONICAL_SHONEN` seed (`sha256 508d5b46…`). The lane `SHONEN.md` at R hashes `6786f3bd3f36b826…`
  (checked boxes `[~]`, appended pointers), so a default live run of that tool already reports that claim `FAIL`, both
  before and after this draft. No `QUALITY.md`/`README.md` pin runs it (grep over `corpus/` and `SKILL.md` finds it
  only in `corpus/knowledge/verdict-contract-r13.md` and `corpus/knowledge/structured-journal-scopes-r13.md` as
  prose), so it is outside C1's surface and is not caused by the draft; it is reported because a future live run would
  read as a SHONEN regression. [INFERENCE] its scheduled uses pass an explicit `--shonen` fixture path
  (`_isolated_args` above builds one), which would explain a passing history.
- No HIGH or MED findings. Nothing observed contradicts `SHONEN.md`'s four boxes, the two pinned tallies, or the
  round-52 targets.

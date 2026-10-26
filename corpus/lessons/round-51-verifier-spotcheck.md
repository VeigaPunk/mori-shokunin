# Round 51 verifier spot-check — mori

author: hyaku closure (non-author integrator, @m_opus)

Scope: mori lane-round 51. Lane HEAD before `aa3af1ec3118ee7766dfce1d9709ce3c0c3f6bfd`, after
`8e3df7e562e8051cf9074f76520fd02404793a23`. Closure date 2026-10-26. I did not author the round. I edited no
lane-authored file and ran no lane gate (`count-c1.py`, `count-c2.py`, `tools/mori-pin-check.py` were not executed);
every re-measure below is my own plain command over committed bytes or a live source.

Driver digest (`.ufo/watchdog.log`, mutable; copied here):
`2026-10-26T19:15:30-03:00 launch mori round=51 pgid=2223116 driver=hyaku-inline attempt=1` /
`2026-10-26T20:33:58-03:00 complete mori round=51; hyaku-inline attempt=1`.

## 1. Step-1 conformance

| check | command | observed |
|---|---|---|
| report landed by the lane | `git log --format='%an %H' -- .ufo/reports/round-51/mori.md` (fleet repo) | `mori-shokunin df35e60141ba114e66fbffe2adea5560d0ddde7b` (20:32:08 -03), after the last cited lane commit `8e3df7e5` (20:31:33 -03) |
| SHONEN heading | read report `## SHONEN`; `grep -cE '^\s*- \[[ x~]\]' SHONEN.md` | heading present, 4 `[~]` lines; SHONEN.md has 4 boxes |
| cited commits exist and are ancestors | `git cat-file -t <h>`; `git merge-base --is-ancestor <h> master` for aa3af1ec, 4677910e, 87e0c374, b504cb17, 7c0b6232, 70e68cdd, a5087527, 8e3df7e5 | 8/8 `commit`, 8/8 ancestors of `master` |
| commits in range | `git log aa3af1ec..8e3df7e5` | 7 commits, all `mori-shokunin`: 4677910e freeze, 87e0c374 data, b504cb17 wave spec, 7c0b6232 / 70e68cdd integration, a5087527 receipts, 8e3df7e5 SHONEN pointer |
| lane pushed, nothing uncommitted | `scripts/hyaku/jj-lane.sh state …/mori-shokunin`; `git status --porcelain` | `branch=master local=remote=8e3df7e5… ahead=0 behind=0 tracked=0 untracked=0`; porcelain empty. `--ignored` shows only `.jj/` and pre-existing `__pycache__/` dirs (rounds 44–50, `tools/`); no `.scratch/` residue |
| seat scratch | `ls -d /fast/scratch/hyaku/mori-r51` | absent, as the report says |
| prompt carries the template contract | `diff <(sed -n 1,140p .ufo/prompts/mori-round-51.md) kimi-shokunin/templates/round-prompt.md` | differs only in rendered placeholders (lane, round, fleet root, axes); §1–§5 verbatim; hyaku addendum §6 and §7 follow |
| dispatch/complete lines | `grep -n "mori round=51" .ufo/watchdog.log` | lines 1584 and 1597, text equal to the digest above |
| frozen bytes intact | sha256 of each `freeze-sha256.txt` path at `8e3df7e5` | 21/21 equal; `git diff 4677910e 8e3df7e5 -- contract.md count-c1.py count-c2.py controls corpus/evidence/sources-r51` empty |

Conformance defects (status-neutral):

- D-a: `count-c1.py` is registered as a `gate` (`SKILL.md:1112`) but has no self-test mode ("`--selftest` is an
  argparse usage error"); §Gate standard's self-test clause is unmet. The six committed controls carry the
  red-before evidence instead.
- D-b: `evidence/c1-at-landed.txt` records its command as `--scratch <scratch>`, an elided placeholder, so the
  receipt's command line is not literally re-runnable as written.
- D-c: the lesson's `### Spot-check` S493 line locators drift from the committed copy: it cites `:55-57`, `:62`,
  `:67-69`, `:71-72`; `grep -n` on `show_mem.c.v7.2` gives 54-55, 56, 64-66, 69-70. The Gate table (54-56) and the
  SOURCES anchor (`23,32-73`) are right.
- D-d: the lesson calls the only `memavailable` hit on the refused famzah page "a reader's 2017 comment"; it is the
  blog author's (Ivan Zahariev) 2017 reply, and the hit is the lowercase repo name `linux-memavailable-procfs`. The
  exact string `MemAvailable` occurs 0 times. The rejection stands.
- D-e: `.ufo/waves/round-40/conform.py` was edited in place, so it no longer matches `round-40/evidence/freeze-r40.txt`
  (`5025b966…` → `7f5174d5…`). The report and LOG disclose it and say the round-40 receipts stay measured on frozen
  bytes; editing a file that an earlier round froze is still a history hazard.

## 2. Claims

Both claims rest on lane-owned counters (gates). Per §Gate standard (Closure consequence) I verified their committed
evidence and did not execute them. C2 was also re-measured with my own script; C1 is evidence-verified plus a
code-level plain measurement.

### C1 (operability, held 7): `--rev` pin re-execution is hermetic and classes mismatches

Evidence-verified:

- before (`evidence/control-c1-do-nothing.txt`, frozen sha256 equal):
  `C1=unmet kill_residue=12547 relocated=unmet reloc_mismatch=1 classified=bad selftest=pass=114,fail=0 … failed=kill_residue,relocated,classified`, `exit=1`;
- after (`evidence/c1-at-landed.txt`, rev `70e68cdd`):
  `C1=met kill_residue=0 relocated=met reloc_mismatch=0 classified=ok selftest=pass=125,fail=0 … failed=-`, `exit=0`,
  with fixture lines `class=env` ×2 and `class=stale` ×2 and summary `env=2 stale=2`;
- at data (`evidence/c1-at-data.txt`, rev `87e0c374`): met, `selftest=pass=119`;
- five non-witness controls are unmet in the frozen receipts (contract table, sha256 equal);
- self-test receipt `evidence/selftests/mori-pin-check.txt`: `grep -c '^PASS'` → 125, `grep -c '^FAIL'` → 0, last
  line `PIN_CHECK_SELFTEST pass=125 fail=0`, `exit=0`.

The revision measured is `70e68cdd`, not the tip. `git diff --stat 70e68cdd 8e3df7e5 -- tools .ufo/waves/round-40` is
empty, so the verdict carries to `8e3df7e5`.

Plain re-measure of what changed (`git show <rev>:<path> | grep …`):

| measure | aa3af1ec | 8e3df7e5 |
|---|---|---|
| `--rev` scratch parent in `tools/mori-pin-check.py` | `:884 scratch_parent = os.path.join(repo, ".scratch")` | `:952 scratch_parent = os.path.abspath(args.scratch or tmpdir or "/var/tmp")`; `:944-947` refuse `--scratch` inside the repo; `:906` `git clone -q --shared --no-checkout` |
| `grep -c "class="` in the tool | 0 | 9 |
| `conform.py` lane path | `:69 LANE = "/home/vgpnk/Projects/shokunin/mori-shokunin"` | `:72 LANE = os.path.dirname(×4 os.path.abspath(__file__))` |

The code matches the claimed mechanism. Residual (not a harm): a killed run now leaves its clone in `$TMPDIR` or
`/var/tmp`, outside the repo; the claim is only about the repo it reads. Verdict: **improved**.

### C2 (depth, held 5): what MemAvailable is at v7.2

Independent re-measure: a Python script parsing the entry table at `8e3df7e5`, `git show` of the copies,
whitespace-collapsed substring match, the counter's published `ENTAIL` regex `^\s*ENTAIL\s+([0-9a-f]{12})\s+(entailed|overclaim)\b`
over `w1/*.md` not starting `MoriR51`, and `sha256(ws(claim))[:12]`. Observed:

- `rows 21`, `located 21`, all 5 sources drawn on;
- quote length 7–23 words; 21 unique claims and 21 unique quotes;
- S492–S496: kind docs/code, tier A, `mined`, opened `2026-10-26`, `used-by` names the entry;
- voters: 11 files, exactly the 11 ENTAILMENT seats;
- rows entailed 21, dissent on current text 0;
- one vote on rows 6, 12, 14 and 15, two on every other row;
- 5 vote hashes match no current row (superseded text).

This equals `evidence/c2-at-landed.txt`
(`C2=met claims=21 located=21 … entailed=21 dissent=0`, `exit=0`) and the report.

A loose `ENTAIL` grep also hits `Mo51CritC2Counter`, `Mo51CritEntailArm` and `Mo51ExecEntailHashTool`. Those lines
are quoted, mid-line or prefixed with `>`, so the counter's regex does not count them. The report's "no file outside
the 11" holds under the counter's rule.

Other re-measures:

- **Sources.** I fetched all five URLs live on 2026-10-26; sha256 equals the frozen copies 5/5 (`e760f716…`,
  `dba76b26…`, `d6c58074…`, `2d4accbb…`, `9f571a04…`).
- **Semantic sample.** Rows 6, 8, 10, 12 and 13 read correctly against `show_mem.c.v7.2:32-72`. Row 15's
  "clamped at zero" is at `meminfo.c.v7.2:50`, outside its quote but in the copy. No row overclaims in my sample.
- **Before.** `control-c2-do-nothing.txt`: `failed=entry_absent,pins`, `exit=1`. At data,
  `failed=entailment`: the arm was red before votes.

Named weakness: the four single-vote rows carry replacement text whose only vote comes from the seat that wrote it
(row 6: `Mo51CritEntail01` voted the old text `overclaim` and its own replacement `entailed`). That is one seat's
judgment, which the report discloses. My read of rows 6, 12, 14 and 15 against the copies agrees with them. Verdict:
**improved**.

### No-harm check

`git diff aa3af1ec 8e3df7e5 -- SCORECARD.md`:

- every Axes score is unchanged (coverage 6, operability 7, depth 5, freshness 5, calibration 5, adjacency 6);
- only the depth and calibration Evidence/Last-change cells gain the round-50 closure citation;
- a `## Round 51` section is appended;
- no capability row is added.

The entry's Boundaries pointer `../tsukuroi-shokunin/PROVINCE.md:8-14,28` resolves to tsukuroi's OS-state ownership
and its "detection and report; the operator remediates" line.

### Per-axis grades

| axis | entering | verdict | basis |
|---|---|---|---|
| operability | 7 | improved | C1: committed receipts before unmet → after met (125/0 self-test), frozen bytes intact, code re-measured. Score held |
| depth | 5 | improved | C2 re-measured 21/21 located, 21/21 entailed, live sources equal the copies. Score held |
| coverage | 6 | unchanged | not claimed. Score cell unchanged |
| freshness | 5 | unchanged | not claimed |
| calibration | 5 | unchanged | not claimed. Only the evidence cell gains the round-50 closure pointer |
| adjacency | 6 | unchanged | not claimed. Boundaries leave OS state to tsukuroi; the fleet-owned dispatcher findings are reported, not edited |

## 3. Discernment spot-check (LEARNING.md)

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S493 `mm/show_mem.c` v7.2 | admit (mined, A, code) | https://raw.githubusercontent.com/torvalds/linux/v7.2/mm/show_mem.c, sha256 `dba76b26…` equals the copy; `grep -n` lines 23, 32, 41, 47, 54, 56, 66, 69, 73 | agree | primary source code at a pinned tag; every clause of scope and teaches reads off `si_mem_available()` at the anchor `23,32-73`. Locator drift in the lesson prose is D-c |
| S082 not widened to meminfo scope | reject (widening) | `corpus/SOURCES.md:88` scope "textual mountinfo field layout only"; `git diff --numstat aa3af1ec 8e3df7e5 -- corpus/SOURCES.md` → `5 0`, zero `-|` lines | agree | widening would give two admitted users a scope their byte check never covered; a new row at the new scope plus one W04 is the honest move |
| famzah 2014 blog | reject (non-primary, no quotable sentence) | https://blog.famzah.net/2014/09/22/know-your-linux-memory-usage/ fetched 2026-10-26: `MemAvailable` 0 hits (case-sensitive); 3 case-insensitive hits, all the 2017 author reply linking `linux-memavailable-procfs`; `3.2.59` and `649` present | agree | the page never defines the estimate, so it cannot ground any claim row. The "reader's comment" wording is wrong (D-d), not the decision |

New SOURCES row quote check: S496. The live `.patch` contains, whitespace-collapsed, "It is wrong because Cached
includes memory that is not freeable as page cache, for example shared memory segments, tmpfs, and ramfs". That is
22 words (`wc -w`), within the ≤25-word bound.

Census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori` returns rc 0 and 23 `W04`.
The last W04 is S492, the same proc.rst URL as S082 and S168 at another scope. This matches `evidence/census-end.txt`.
Rows: `grep -cE '^ {0,3}\| *S[0-9]{3,}'` gives 264 at `aa3af1ec` and 269 at `8e3df7e5`. The malformed-row awk prints
0, and S492–S496 each have NF=13.

## 4. Trend verdicts

- **expansion: improved.**
  - One admitted entry, `corpus/knowledge/memavailable-estimate-r51.md`, on ground the lane did not hold.
    `git grep -l` at `aa3af1ec` over `corpus/SOURCES.md corpus/knowledge SKILL.md` finds 0 files for each of
    `si_mem_available`, `totalreserve`, `wmark_low`, `folio_is_file_lru`, `34e431b0` and `show_mem.c`.
    `MemAvailable` appears in 7 files, only as a read value.
  - It cites five `mined` tier-A rows, and the README carries a round-51 coverage block (`corpus/README.md:702`).
- **quality: improved.**
  - Pin re-execution no longer writes into the repo it reads and holds with the lane path hidden (C1, verified).
  - Four overclaiming rows were replaced before landing.
  - All five sources re-open to byte-identical copies.
  - No admitted entry failed its re-check.
- **discernment: improved.** The outside spot-check agrees with the gate on one admit and two rejects. The lane
  self-graded `unprovable-but-better` and deferred the call to this closure.

## 5. Routed defects (lane must fix next round unless marked otherwise)

1. Give `count-c1.py`-style counters a real self-test mode, or register them as such with the controls as the
   committed fixture (D-a, §Gate standard self-test clause).
2. Entailment arm hardening (named in the lesson):
   - require ≥2 votes per row from seats that did not write the row's text, so the four single-vote,
     self-authored replacements of this round would read unmet;
   - ignore fenced lines;
   - restrict voters to the dispatch's ENTAILMENT seats.
3. C1 counter survivors (7 of 9 single-arm mutants keep every control verdict): add controls that isolate each arm
   (lesson `## Wave w1 — integrated findings`).
4. Round-50 routed defect 3, the successor calibration counter and K4 beyond SHONEN, is still open. The lane routes
   it to round 52; carry it.
5. Fix the lesson's S493 locators (D-c) and the famzah attribution (D-d) by appended erratum. Never rewrite the filed
   bytes.
6. D-e: stop editing files a prior round froze in place; copy-on-change, or record a successor freeze, for
   `round-40/conform.py`.
7. Make the receipt commands literal (D-b): record the actual `--scratch` path, or a reproducible placeholder rule
   stated in the receipt.
8. The remaining in-lane writers (round-38/39/41/42 `conform.py`, round-48/49 `count-c1.py` scratch under the lane)
   are already planned for round 52 as a hermeticity sweep; carry them.

## 6. Notes for the operator

- Fleet-owned findings that mori reported and did not edit (`.ufo/waves/round-51/w1/Mo51ExecDispatcherGate.md`):
  - `scripts/hyaku/inline-dispatcher.py:133` fails open when `/proc/meminfo` is unreadable;
  - its `MEM_MIN_GB` is GiB;
  - the two hyaku gates hold different floors on the same line (4 GiB vs 6144 MiB).

  These are operator-owned.
- SHONEN: all four boxes are `[~]` with pointers that resolve:
  - `LOG.md:2765` opens the Round 51 entry;
  - the selftest receipts are committed;
  - the boundaries pointer resolves.

  They look checkable by a non-author; the promotion bar is the operator's decision. I wrote no `[x]`.

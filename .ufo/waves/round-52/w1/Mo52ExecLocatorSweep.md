# Mo52ExecLocatorSweep — locator inventory for round 53 (SCORECARD.md + LOG.md at the data commit)

Seat: Mo52ExecLocatorSweep (leaf executor, read-only). Lane: `mori-shokunin`. Measured revision R =
`8524904adb25e44f24d9f25aac7eae909625c18c` (data commit, `SCORECARD.md` blob `de74b08c5a619b93387ce4ee5f7b3db1ad1b2a80`,
`LOG.md` blob `06f2385e339b01ffa0d4d17e063ee984edf0acde`, tree `aff63164cd8966326312d25d452f529081583f25`).
Comparison revision: entering tip `4f266ef2fdf74d8b046f5b4f5a5c4945f65b966d`.
No claim is scored here and no predicate is proposed for change; the counters, their predicates and the kill rules are
frozen and were not touched.

## 1. Method — the frozen locator rule, reused verbatim

`check_locators` (`count-c1.py:368-417`) was not re-implemented from prose. The frozen counter was copied out of the
lane and imported, so its own `LOC`, `ws()` and `split_cells()` bytes do the work:

```
$ cd /home/vgpnk/Projects/shokunin/mori-shokunin
$ git show 8524904adb25e44f24d9f25aac7eae909625c18c:.ufo/waves/round-52/count-c1.py \
    > /fast/scratch/hyaku/mori-r52/Mo52ExecLocatorSweep/count_c1_frozen.py           # exit 0
$ sha256sum /fast/scratch/hyaku/mori-r52/Mo52ExecLocatorSweep/count_c1_frozen.py .ufo/waves/round-52/count-c1.py
e864922790451b4026be784d5344d9a06827b251ed3c81bfe26b1c559ee3c300  .../count_c1_frozen.py
e864922790451b4026be784d5344d9a06827b251ed3c81bfe26b1c559ee3c300  .ufo/waves/round-52/count-c1.py
```

The two hashes are equal, so the imported `LOC` / `ws` / `split_cells` are the frozen bytes at R.

Scan driver: `/fast/scratch/hyaku/mori-r52/Mo52ExecLocatorSweep/loc-sweep.py` (`PYTHONDONTWRITEBYTECODE=1`, exit 0;
inventory JSON written only under scratch). Faithful generalisation of arm D's input units to whole files:

- unit = one table cell (`split_cells`, as `axes_table` does) when the line matches `^ {0,3}\|`, else the whole line;
- per unit, `LOC.finditer`, `frag` = unit text from the previous locator end to this locator start, then `frag`
  split on `";"` and the last piece kept — identical to `check_locators`, so "follows a quote" means *inside the same
  cell/`;` span, before the locator*;
- resolution against R through the counter's own reader semantics (`git show R:<path>`, trailing-newline strip,
  `1 <= N <= M <= len(lines)`), quote compared whitespace-folded, `proposed A → B` compared as the literal pair;
- fenced blocks are tracked (`unfenced` logic) and tagged separately; fence delimiter lines are skipped.

Fidelity check against the frozen counter's own arm D at R (`evidence/c1-at-data.txt`, `locators=27`): my sweep sees
21 locators in the six Axes rows (lines 10/11/12/13/14/15 = 3/5/5/3/4/1) and 6 in the SHONEN boxes
(`SKILL.md:1069-1141`, `SKILL.md:1018-1067`, `corpus/QUALITY.md:1252-1352`, `LOG.md:2765-2805`, `LOG.md:2732-2763`,
`PROVINCE.md:3-16`) — 21 + 6 = 27, and the three quote/pair items match the receipt byte for byte
(`round-24-…:88 quote:Score_6_→_6 found`, `SCORECARD.md:1781 pair:5_→_6 found`, `round-24-…:68 quote:Score_5_→_5
found`). The whole-file sweep counts 52 locators in `SCORECARD.md`, i.e. 31 more than the 21 arm-D reads there, and
reads `LOG.md` (39 locators) which arm D never reads beyond its two box pointers. Raw regex cross-check:
`` `path:N[-M]` `` matches per whole file = 52 (`SCORECARD.md`) and 39 (`LOG.md`), equal to the sweep totals; zero
locators sit inside fenced blocks (`SCORECARD.md` 18 fence delimiters / 9 blocks, `LOG.md` 0 fences).

## 2. Counts at R `8524904a` (counter rule, whole files)

| file | locators | in range | quote found | quote absent | file absent | out of range |
|---|---|---|---|---|---|---|
| `SCORECARD.md` | 52 | 46 | 3 | 0 | 6 | 0 |
| `LOG.md` | 39 | 28 | 0 | 0 | 11 | 0 |
| **total** | **91** | **74** | **3** | **0** | **17** | **0** |

"in range" = the named file exists at R and `1 <= N <= M <=` its line count (this includes the three found quotes and
all range-only items). "qualified" = the locator follows a double-quoted string or a `proposed A → B` phrase in its
own cell/`;` span: **3 of 91** (`SCORECARD.md` 3, `LOG.md` 0) — every one of them currently **passes**.

### 2.1 The three quote/pair-checked locators (all found)

| site | locator | expected | observed at R |
|---|---|---|---|
| `SCORECARD.md:10` (coverage row, Evidence cell) | `corpus/lessons/round-24-verifier-spotcheck.md:88` | quote `Score 6 → 6` | line 88 ends `… Strength is limited by the survivors above. Score 6 → 6.` |
| `SCORECARD.md:13` (freshness row) | `SCORECARD.md:1781` | pair `5 → 6` | line 1781 carries `5 → 6` inside the round-28 freshness sentence |
| `SCORECARD.md:14` (calibration row) | `corpus/lessons/round-24-verifier-spotcheck.md:68` | quote `Score 5 → 5` | line 68 ends `… as disclosed. Score 5 → 5.` |

## 3. Misses — 17 `file_absent` locators (all range-only, none quote/pair)

Every one is written as a bare basename (or a path relative to some other document's directory), so the
lane-root-relative resolution the counter uses returns nothing. `git ls-tree -r` at R was searched for each basename;
the third column gives the unique or first candidate and whether the pinned `N[-M]` fits there, so a re-point is a
prefix fix, not a re-measurement.

| site | locator | written as | resolves at R if prefixed | range fits |
|---|---|---|---|---|
| `SCORECARD.md:1831` (### Round 30 measured outcome) | `CaseR30a.md:105` | basename | `.ufo/waves/round-30/w1/CaseR30a.md` | yes (105 lines) |
| `SCORECARD.md:1856` (### Round 31 appended corrections) | `contract.md:170-172` | basename | 6 candidates `.ufo/waves/round-17…20/contract.md` — ambiguous | unverified (ambiguous) |
| `SCORECARD.md:1856` | `check-blind-wave.sh:172-180` | basename | `.ufo/waves/round-29|30/check-blind-wave.sh` — ambiguous | unverified |
| `SCORECARD.md:1856` | `check-blind-wave.sh:215-229` | basename | same two candidates | unverified |
| `SCORECARD.md:2103` (### Round 37 post-data corrections) | `count-c1.py:27-29` | basename | 21+ candidates `.ufo/waves/round-31…51/count-c1.py` — ambiguous | unverified |
| `SCORECARD.md:2195` (### Round 38 claim-3 cell correction) | `evidence/gate-after.txt:22` | relative to a round dir | `.ufo/waves/round-38/evidence/gate-after.txt` | yes (23 lines) |
| `LOG.md:75` | `PROTOCOL.md:155-168` | basename | **no such file anywhere in the tree at R** (root holds `PROVINCE.md`) | n/a |
| `LOG.md:544` | `PROTOCOL.md:351-352` | basename | **no such file anywhere at R** | n/a |
| `LOG.md:593` | `AXES.md:79` | basename | **no such file anywhere at R** | n/a |
| `LOG.md:735` | `kimi-shokunin/templates/mint/SHONEN.md:7-14` | sibling-lane path | not in this repo; only `SHONEN.md` basename matches lane root | n/a |
| `LOG.md:1901` | `oom-victim-selection-r27.md:200-202` | basename | `corpus/knowledge/oom-victim-selection-r27.md` | yes (210 lines) |
| `LOG.md:1983` | `CaseR30a.md:105` | basename | `.ufo/waves/round-30/w1/CaseR30a.md` | yes (105 lines) |
| `LOG.md:2028` | `CaseR30a.md:105` | basename | `.ufo/waves/round-30/w1/CaseR30a.md` | yes (105 lines) |
| `LOG.md:2234` | `S226.src:657-659` | basename | `corpus/evidence/sources-r38/S226.src` | yes (1029 lines) |
| `LOG.md:2268` | `gate-after-e37dcc6.txt:22` | basename | `.ufo/waves/round-38/evidence/gate-after-e37dcc6.txt` | yes (23 lines) |
| `LOG.md:2450` | `evidence/c1-after.txt:30-41` | relative to a round dir | 4+ candidates `.ufo/waves/round-27…30/evidence/c1-after.txt` — ambiguous | unverified |
| `LOG.md:2771` | `conform.py:69` | basename | 4+ candidates `.ufo/waves/round-38…41/conform.py` — ambiguous | unverified |

`PROTOCOL.md` and `AXES.md` leave no trace in this lane's history (`git log --oneline --all -- PROTOCOL.md AXES.md`
prints nothing) and the lane root at both R and the entering tip contains `PROVINCE.md`, not them — those three
pointers name documents the lane no longer (or never) held under that name.

Scope note (important for the claim, not for the record): none of the 17 sits in the `## Axes` table (lines 8-15), in
a SHONEN box, or in `corpus/QUALITY.md`/`corpus/README.md`; 6 are under `### Round NN …` headings in `SCORECARD.md`
(dated round sections) and 11 are in `LOG.md`, which K4 excludes as a dated record. **Arm D of the frozen counter is
therefore unaffected — all 17 are outside the surfaces it reads**, and `C1=met` at R is consistent with them.

## 4. Delta against the entering tip `4f266ef2`

Same sweep, same rules:

| revision | file | locators | in range | quote found | quote absent | file absent |
|---|---|---|---|---|---|---|
| `4f266ef2` | `SCORECARD.md` | 50 | 43 | 2 | 1 | 6 |
| `4f266ef2` | `LOG.md` | 39 | 28 | 0 | 0 | 11 |
| `8524904a` | `SCORECARD.md` | 52 | 46 | 3 | 0 | 6 |
| `8524904a` | `LOG.md` | 39 | 28 | 0 | 0 | 11 |

Readings: the data commit **added 2 locators to `SCORECARD.md`, both resolvable**, and **retired the only failing
quote/pair item** — the freshness row's pointer moved `SCORECARD.md:1771` (entering: `quote_absent` for `5 → 6`) to
`SCORECARD.md:1781`, matching the appended text that pushed the target line down ten lines. This is the exact drift
class of the round-51 lesson, here corrected inside the same commit that caused it. The 17 misses are **inherited
unchanged**: identical sites and statuses before and after the data commit.

## 5. Two rule-boundary experiments (measurements only; no predicate change proposed)

1. **Same-line strengthening (do not adopt).** If "follows a quote" were read as *any quote earlier on the same
   physical line* (ignoring cell and `;` boundaries), the qualified set grows from 3 to 10 in `SCORECARD.md` and from
   0 to 1 in `LOG.md`. Re-checking those 8 additions gives **8 new failures, every one a false positive**: the quote
   belongs to the first sibling locator and is not a claim about the later ones —
   `round-26-…:133 absent`, `round-47-…:68 absent` (both under `Score 6 → 6`), `round-14-…:87 absent` (under `5 → 6`),
   `round-25-…:124`, `round-49-…:75`, `round-50-…:125 absent` (under `Score 5 → 5`), `SCORECARD.md:793 absent`
   (under `"unchanged"`), plus `LOG.md:1901 → file_absent`. The frozen rule's boundary reset is *deliberate and
   correct*; a round-53 "strengthening" along this line would manufacture eight mismatches.
2. **Quote-after-locator is never checked (real asymmetry).** The rule looks only backwards, so a pointer written
   `` `path:N` reads "quoted words" `` escapes the quote check. Two such cases exist at R, none in arm-D scope:
   `SCORECARD.md:1642` → `SCORECARD.md:1568` for `"harness background-job runway read"` (**absent** at 1568),
   `LOG.md:1905` → `PROVINCE.md:318` for `"opened this round"` (found).

## 6. Named limits of this sweep

- One interpretation is laid on the frozen rule: outside table cells the unit is the whole physical line, so a quote
  on a *previous* line is not carried forward (10 such adjacency cases in `SCORECARD.md`, 2 in `LOG.md`, measured and
  all range-only either way). The counter itself has no such case because it only reads cells and box lines.
- Resolution uses the counter's `git show R:<path>` reader; a path that is a directory at R would be read as its
  one-line tree text, not flagged. No locator in these two files hit that shape.
- "in range" proves the file has `M` lines at R; it proves nothing about whether the pinned span still says what its
  sentence claims (that is the quote/pair arm's job, and it covers 3 of 91 pointers here).
- This inventory says nothing about arms A (Score), B (SHONEN receipts) or C (living pins); it does not run any
  pinned command.
- Attribution of the 17 misses to "dated record" rests on the nearest preceding heading, not on a machine predicate.

## 7. Routed items for round 53 (named, not applied)

1. **Re-point the 6 uniquely-resolvable bare basenames** in an *appended* errata note (house rule: supersession,
   never in-place rewrite): `SCORECARD.md:1831`, `SCORECARD.md:2195`, `LOG.md:1901`, `LOG.md:1983`, `LOG.md:2028`,
   `LOG.md:2234`, `LOG.md:2268`. Each fits its candidate's line count, so a prefix is the whole fix. (7 sites; the
   11 ambiguous or orphan ones — `contract.md`, `check-blind-wave.sh` ×2, `count-c1.py`, `evidence/c1-after.txt`,
   `conform.py`, `PROTOCOL.md` ×2, `AXES.md`, the sibling-lane `SHONEN.md` — need the author's round number, or should
   be retired as unresolvable.)
2. **Decide the forward-quote asymmetry** (§5.2, 2 cases, 1 absent) before any successor arm claims to check quoted
   words: either name it as a limit in the predicate docstring, or read the quote that follows a pointer too.
3. **Keep the cell/`;` boundary reset** (§5.1): the measurement shows a same-line rule is a false-positive generator,
   so the successor's docstring should say the boundary is intentional, closing the "locator arm is lenient" reading.
4. If a round-53 seat wants this inventory as a mode rather than a one-off, the driver is in scratch only
   (`loc-sweep.py`, imports the frozen counter by path); it would need the counter re-copied per revision to stay
   byte-faithful.
5. Observation for the in-lane-writer inventory seat: `.ufo/waves/round-52/__pycache__/{count-c1,count-c2,build-w1-spec}.cpython-314.pyc`
   (mtimes 21:11:55 / 20:58:31 / 21:09:18) and `.ufo/waves/round-52/controls/__pycache__/c1-data.cpython-314.pyc`
   (21:07:35) exist in the lane; `git status --porcelain --ignored` reports them as `!!` lines
   (`.gitignore:3:__pycache__/`). They predate this seat (first sweep command 21:14) and none is mine (my import ran
   from the scratch copy with `dont_write_bytecode`); an unpinned import inside a measured run would raise
   `lane_writes`. The counter's own `run()` sets `PYTHONDONTWRITEBYTECODE=1`, so its pinned commands are safe.

## 8. Host and hygiene

- Read-only throughout: `git -C <lane> show/ls-tree/rev-parse/log/status/check-ignore` and reads of the lane tree.
  No add/commit/stash/checkout/reset/pull/push, no jj command, no write into the lane or the fleet repo, no
  `~/.local/bin`, no pacman (host-wide pause respected), no tool installs (stock `Python 3.14.8`, `git 2.56.0`).
- `scripts/hyaku/disk-guard.sh status` before work: `/fast/scratch/hyaku` 24 % used, 614.4 G free, no ENOSPC.
- Scratch `/fast/scratch/hyaku/mori-r52/Mo52ExecLocatorSweep/` (`TMPDIR` inside it, `mkdir -p` first) held the frozen
  counter copy, the driver, `inventory.json` and `tmp/`; it was removed after the numbers and quoted texts above were
  copied into this report. Peak size < 1 MB, no clone, no fixture repo, nothing under `/tmp` cited.
- Lane bytes confirmed untouched by this seat: the frozen counter copy's sha256 equals the in-lane file, no
  `__pycache__` appeared under the scratch copy, and no path this seat wrote lies inside the lane.

## Findings

- **MED** — 17 of 91 whole-file locators (19 %) do not resolve lane-root-relative at R (`SCORECARD.md` 6:
  lines 1831, 1856 ×3, 2103, 2195; `LOG.md` 11: lines 75, 544, 593, 735, 1901, 1983, 2028, 2234, 2268, 2450, 2771).
  All range-only, all outside arm D's surfaces, so `C1=met` is unaffected; itemised with candidate re-points in §3.
- **MED** — three pointers name documents that never existed under that name in this lane (`LOG.md:75` and
  `LOG.md:544` `PROTOCOL.md`, `LOG.md:593` `AXES.md`; root holds `PROVINCE.md`). §7.1.
- **MED** — the quote/pair arm reads backwards only: a quoted claim written *after* its pointer is never checked;
  2 cases at R, 1 already absent (`SCORECARD.md:1642` → `SCORECARD.md:1568`). §5.2, §7.2.
- **LOW** — quote scope resets at cell and `;` boundaries; a same-line variant would add 8 failures, all false
  positives. Keep the reset and document it. §5.1, §7.3.
- **LOW** — 11 misses are ambiguous or orphan pointers (`contract.md`, `check-blind-wave.sh` ×2, `count-c1.py`,
  `evidence/c1-after.txt`, `conform.py`, `PROTOCOL.md` ×2, `AXES.md`, sibling-lane `SHONEN.md`): several round
  candidates each, so they cannot be re-pointed without the original author's round. §3, §7.1.
- **LOW** — the round-52 data moved a target line (`SCORECARD.md:1771` → `:1781`) and updated its own pointer in the
  same commit: the drift class of the round-51 lesson is corrected here, but nothing in the counters would notice a
  sibling locator drifting in a future append, since only 3 of 91 pointers are quote/pair-checked. §4.
- **LOW** — four stale `__pycache__/*.pyc` files sit in the lane under `.ufo/waves/round-52/` (not this seat's;
  ignored but listed by `git status --ignored`). §7.5.
- **INFO** — sweep fidelity: 21 Axes-row + 6 SHONEN-box locators = the counter's `locators=27`, and the three
  quote/pair verdicts match `evidence/c1-at-data.txt` exactly.

PARTIAL — the round-20 SCORECARD draft below is supported by committed evidence for C2 and for C1 under C-locale sorting. The C1 counting command as frozen in `.ufo/waves/round-20/contract.md` does not reproduce its 8→0 result in this lane's ambient `en_US.UTF-8` shell (it yields 37→33 with `comm` order warnings). The draft therefore records a corrected, locale-explicit counting command. No SCORECARD.md, census, baseline, tool, or contract bytes were edited.

# DraftScorecard — round-20 falsification (scope: SCORECARD.md round-20 section draft)

Author seat: `MoriR20.DraftScorecard` (leaf, no subagents). Evidence base: committed `HEAD` = `8f8c58e`; every cited artifact below is a tracked file (`git ls-files --error-unmatch` checked). Untracked wave-2 and falsify outputs were not used as evidence.

## 1. Draft section for SCORECARD.md (to be appended after the round-19 section)

Style follows `SCORECARD.md:1153-1231` (round 19). Not written to SCORECARD.md (L1 owns it).

---

## Round 20 — classified drift re-pin and per-seat wave settlement

Author `MoriR20` (L1); entering tip `2061780117e6ca637725004897bd288d3ba7e988`.
Frozen contract `e4d9384` (before implementation); C2 tool landed `2eeae04`; committed round-20 tip `8f8c58e`.
Active scores held: coverage6, operability7, depth5, freshness5, calibration5, adjacency6.
C1 selected freshness (lowest-score tie with depth and calibration). C2 selected coverage (capability, FR3 advance).
No axis retirement or stagnation waiver. A missing capability is not a historical production defect.

### Round20 measured claims — finite and live, not clearance

Census SHA-256 `87b8d680…ab28` at the entering tip and at `HEAD` (byte-identical; `git diff` empty for `tools/mori-census.sh` between `2061780` and `HEAD`). The r10 baseline is byte-unchanged since `5be8943`.

| Claim | Axis / held score | Observed before→after | Counting command (lane root) | L1 verdict / qualification |
|---|---|---|---|---|
| C1 unclassified live drift tokens | freshness5→5 | 8 unclassified against the r13 register → 0 against `corpus/evidence/drift-classification-r20.json`, same 50-token capture (`evidence/c1-drift-entering.json`) | `LC_ALL=C comm -23 <(tr ' ' '\n' < DRIFT \| grep -v '^MORI_DRIFT:$' \| grep . \| LC_ALL=C sort -u) <(jq -r '.tokens\|keys[]' REG \| LC_ALL=C sort -u) \| wc -l` | improved. The `LC_ALL=C` must also prefix the first `sort`; the frozen wording omits it and then gives 37/33 (see §3 correction). |
| C1 census-regression tokens (re-pin blocker) | freshness5→5 | 50 tokens unclassed → 0 of 50 `census-regression` | `jq '[.tokens[]\|select(.class=="census-regression")]\|length' corpus/evidence/drift-classification-r20.json` → `0` | improved; zero is not proof of zero regressions (presence-gated findings, `drift-repin-r20.md` §3) |
| C1 classed tokens with class, reason and evidence | freshness5→5 | r13 register: free text, no class or evidence fields → 50/50 classed from the closed set (29 census-schema-change, 19 live-state, 2 roster-change) | `jq '[.tokens[]\|select((.class\|IN("census-schema-change","roster-change","live-state","census-regression")) and ((.evidence//"")!="") and ((.reason//"")!=""))]\|length' corpus/evidence/drift-classification-r20.json` → `50` | improved; two tokens (`WATCHDOG_STALE`, `WAVE_UNSETTLED_AGE`) carry `blind_spot`, classified live-state by L1 over dissent |
| C1 drift vs pinned baseline | freshness5→5 | r10 `--drift`: rc 1, 50 tokens → pre-pin 10:51Z rc 1, 49 tokens (`WATCHDOG_STALE` absent) → r20 `--drift`: rc 0, `MORI_DRIFT: none` | `bash tools/mori-census.sh --drift corpus/evidence/baseline-r20-20261021T1051Z.json; echo rc=$?` | improved, stability window only (scratch pin drifted 65 s later; `drift-repin-r20.md` §4). `none` = unchanged since pin, not healthy |
| C2 capability absent | coverage6→6 | 14 → 0 (tool absent at `2061780`: `git cat-file -e` rc 128) | `jq -s '[.[].counts.capability_absent]' .ufo/waves/round-20/evidence/c2-before.json .ufo/waves/round-20/evidence/c2-after.json` → `[14,0]` | improved (capability red, not 14 production defects) |
| C2 matched frozen cases | coverage6→6 | 0 → 14/14 (independent oracle `build/OracleHarness/c2-oracle.py`) | `jq '.counts.matched' .ufo/waves/round-20/evidence/c2-after.json` → `14` | improved |
| C2 live per-seat settlement, r19 wave 1 | coverage6→6 | hand count at closure (48 gaps) → `partial`, 16 present / 48 missing / 64 members, exit 1 | `jq -c '.waves[]\|select(.dispatch_path\|test("round-19/wave1"))\|{state,counts}' .ufo/waves/round-20/evidence/c2-live-mori.json` | demonstration, not finite count |
| C2 live per-seat settlement, r20 wave 1 (in flight) | coverage6→6 | lane scan: `partial`, 70 present / 6 stub / 76 members → `settled`, 76 present / 0 stub (`evidence/wave1-settlement-scan.json`) | `jq -c '.waves[]\|select(.dispatch_path\|test("round-20"))\|{state,counts}' .ufo/waves/round-20/evidence/{c2-live-mori,wave1-settlement-scan}.json` | demonstrates the R2 `stub` status; wave results not accepted here |
| C2 fleet-wide live scan | coverage6→6 | 21 lanes scanned; 15 lanes exit 1; 196 waves; 12307 members; 10678 present; 1622 missing (sums of per-lane rows; the file has no totals field) | `jq '[.lanes[].members//0]\|add' .ufo/waves/round-20/evidence/c2-live-fleet.json` (and `.present`, `.missing`, `.waves`) | demonstration; per-lane rows are not all frozen ground truth (kama, kagi, tabi moved mid-scan) |

Actual counting outputs at the committed inputs: C1 `8` and `0` under C-locale sorting; C2 `[14,0]` and `14`. Receipts: `.ufo/waves/round-20/evidence/c1-drift-entering.json`, `c1-drift-r10-prepin.txt`, `c1-drift-r20-postpin.txt`, `c2-before.json`, `c2-after.json`, `c2-live-mori.json`, `c2-live-fleet.json`, `wave1-settlement-scan.json`.

A missing capability is not ten or fourteen prior production bugs. A missing report is not a dead seat: the tool never emits `dead`, `failed` or `killed`.

### Current axis register (round20; scores held)

| Axis | Score held | Round20 verdict | Evidence / boundary |
|---|---:|---|---|
| coverage | 6 | improved | new per-seat settlement observation of dispatched waves (previously `SURFACE waves` graded directories only, `build/CensusWavesSurface.md`); held at 6 as with the round-16 window capability: one capability, no new measured domain |
| freshness | 5 | improved | r10 red replaced by a classed register (50/50) and a re-pin; post-pin `none`. Held at 5: the new pin's stability window is minutes to hours, and the frozen counting command is locale-fragile until corrected |
| operability | 7 | unchanged | census `87b8d680` unchanged; new read-only tool credited to coverage only |
| depth | 5 | unchanged | S066–S072 and two scoped knowledge notes support bounded claims; no separate depth score |
| calibration | 5 | unchanged | WATCHDOG/WAVE_UNSETTLED dispute resolved by L1, not outside; not a selected axis this round |
| adjacency | 6 | unchanged | detection and report only; census not edited; disclosed scope breaches M7 and M8 (below) earn no credit |

### Capabilities: first demonstrated round20

| Name | What it can now do | Evidence pointer | First-working round |
|---|---|---|---:|
| Wave settlement scan | For every `ufo-swarm-wave-dispatch-v1` file under a lane, grade each member's trailer report `present/empty/stub/missing/misrooted/unsafe/unparsed` and each wave `settled/partial/unsettled/no-spawn/unavailable`; emits no report bytes; a missing report is not a dead seat | `.ufo/waves/round-20/evidence/c2-after.json` (14/14); `c2-live-mori.json` (r19 W1 16/64); `c2-live-fleet.json` (21 lanes); `tools/mori-wave-settlement.py` at `2eeae04` | 20 |

### Round20 learning and governance trends

Expansion **improved**: seven source rows S066–S072 (six admitted, one queued or vocabulary-only where stated, S072 rejected), two knowledge notes (`drift-repin-r20.md`, `wave-settlement-r20.md`), one lesson. Quality **unchanged**: the lesson records eight mistakes (M1–M8) with fail-capabilities, but this falsification found a new defect (the locale-fragile counting command) and M4/M5 were fixed only after detection. Discernment **unchanged**: no committed non-author closure exists for round 20; the wave-2 falsify and critic outputs are untracked and are not credited.

Disclosed scope breaches, no compliance credit: M7 (a seat wrote under the fleet root, then removed its own stray file; the fleet file belonging to souji was not touched) and M8 (broad searches surfaced snippets from `.ufo/interactive-sessions/*.jsonl`; none opened or quoted).

Named debt carried to round 21: the counting-command correction (below); the 155 unresolved content-review dispositions and the 39 unknown-cause r19 W1 seats; the WATCHDOG/WAVE_UNSETTLED_AGE census design routing (daemon identity, wave memory for emptied directories); the `drift_scan` first-word and positional-pairing comparator limits; the post-pin stability window; the outside closure. No subsequent round is initiated or claimed.

---

## 2. Verified measurements (this seat, committed inputs, read-only)

| Check | Command (lane root) | Result | Exit |
|---|---|---|---|
| Frozen C1 count, verbatim, ambient locale, r13 register | `LC_ALL=C comm -23 <(tr ' ' '\n' < DRIFT \| grep -v '^MORI_DRIFT:$' \| grep . \| sort -u) <(jq -r '.tokens\|keys[]' R13 \| LC_ALL=C sort -u) \| wc -l` (DRIFT = `falsify/DraftScorecard/drift-entering.txt`, extracted from `c1-drift-entering.json` `.stdout`) | 37 lines, plus `comm: file 1 is not in sorted order` on stderr | 0 |
| Same, r20 register | same, with `corpus/evidence/drift-classification-r20.json` | 33 lines, plus stderr warnings | 0 |
| Corrected: both sorts `LC_ALL=C` | `LC_ALL=C comm -23 <(… \| LC_ALL=C sort -u) <(… \| LC_ALL=C sort -u) \| wc -l` | r13 `8`; r20 `0` | 0 |
| Outer `env LC_ALL=C` form | `env LC_ALL=C bash -c "comm -23 <(… \| sort -u) <(… \| sort -u) \| wc -l"` | r13 `8`; r20 `0` | 0 |
| Committed 8-token list matches | `diff` of the C-locale r13 difference vs `.unclassified_vs_prior_register` | identical (8 tokens: `+FINDING:COREDUMP_NOTICE_JOURNAL_USER`, `+FINDING:SEGFAULT_SIGNAL11_JOURNAL_USER`, `+FINDING:UNIT_FAILURE_OUT_OF_SCOPE`, `+path`, `-FINDING:WATCHDOG_STALE`, `age_s`, `io_avg_unavailable`, `round`) | 0 |
| Pre-pin drift, r13 / r20 | same, on `c1-drift-r10-prepin.txt` minus the `rc=` line | 49 tokens; 7 unclassified (r13) → 0 (r20) | 0 |
| Register classes | `jq` class counts | 29 / 19 / 2 / 0, total 50, all with reason and evidence | 0 |
| Census and r10 baseline immutability | `git show 2061780:tools/mori-census.sh \| sha256sum`; `git diff --stat 2061780 HEAD -- tools/mori-census.sh corpus/evidence/baseline-r10-20261015T2231Z.json` | `87b8d680…ab28`; empty diff | 0 |
| Frozen C2 bytes | `git show e4d9384:.ufo/waves/round-20/frozen/c2-expected.json \| sha256sum` vs working file | both `09848069…f2af`; `git diff e4d9384 HEAD` on contract and frozen dir empty | 0 |
| Tool absent at entering | `git cat-file -e 2061780117e6…:tools/mori-wave-settlement.py` | rc 128 | 128 (expected) |
| C2 counts | `jq -s '[.[].counts.capability_absent]' …c2-before.json …c2-after.json` | `[14,0]`; matched `14` | 0 |
| Tool blob at HEAD | `sha256sum tools/mori-wave-settlement.py` | `c6e60919…4e795`, equal to `git show HEAD:` blob; only commit touching it is `2eeae04` | 0 |

Tools installed: none. Subagents spawned: none. The heavy census command was not run; no baseline was pinned or re-pinned by this seat.

## 3. Finding for the L1: the frozen C1 counting command is locale-dependent

Severity: the claim's own recorded counting command does not reproduce its numbers as written. The `LC_ALL=C` prefix applies to `comm` only. The first `sort -u` sits inside a process substitution and inherits the shell locale, which is `en_US.UTF-8` in this lane (`LANG`). Under that locale, `comm` receives unsorted input and emits spurious lines: 37 and 33 instead of 8 and 0. The committed receipt (`c1-drift-entering.json`, 8 tokens) and the knowledge note are correct under C sorting, so the measured result stands. The defect is in the command text, which is frozen and so cannot be edited.

Recommended handling (L1 decision): record the corrected command (both sorts with `LC_ALL=C`) in SCORECARD and in `corpus/knowledge/drift-repin-r20.md` §1 as a named correction, leave `contract.md` bytes unchanged, and note in the next round's counting-command guidance that `LC_ALL=C` must prefix every sort in a pipeline run under bash, not only `comm`.

## 4. Falsification verdict per item

| Item | Verdict | Basis |
|---|---|---|
| Draft SCORECARD section uses committed evidence only | HOLDS | all cited paths are tracked at `8f8c58e`; no untracked wave-2 or falsify output is cited |
| C1 8→0 under the frozen counting command | PARTIAL | holds with `LC_ALL=C` on both sorts; fails as written under `en_US.UTF-8` (§3) |
| C1 zero census-regression; 50/50 classed; re-pin post-pin none | HOLDS | register jq counts and receipts |
| C2 14→0 capability; matched 14/14; r19 W1 16/64 | HOLDS | `c2-before.json`, `c2-after.json`, `c2-live-mori.json` |
| Axis scores held | HOLDS | held per round-16/round-19 precedent; justifications in §1 table |

Artifact paths: this report, `.ufo/waves/round-20/falsify/DraftScorecard.md`. Scratch: `.ufo/waves/round-20/falsify/DraftScorecard/` (`drift-entering.txt`, `unclassified-r13-C.txt`, `committed8.txt`).

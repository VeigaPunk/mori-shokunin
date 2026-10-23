# ConnSiblingOverlap — sibling-lane lesson scan for overlap with mori round-37 claims

Item under attack: the completeness of the cross-lane overlap picture for mori r37's claims
(C1 calibration counter `count-c1.py` with negative-control arms real-arm memoizer +
summary-only printer rejected / honest gate blind-passing; C2 freshness drift probe
`count-c2.py` with two named fetch policies each killed by its own mutation; frontier
SOURCES S221–S225 + drift-hardening knowledge + lesson Gate/M1–M4; routed r36 debts
(d)–(h)). Detection/report only — no lane file was edited, no tool installed or upgraded,
no scratch was needed.

Axes: (1) scan complete over every lane repo that exists, (2) each overlap named with
file-and-line evidence, (3) the named file per lane is the newest lesson file whose name
mentions counters, gates, or drift.

## Method and observed output

Lane enumeration (21 repos, 20 siblings + mori itself):

```
$ ls -d /home/vgpnk/Projects/shokunin/*-shokunin
audio-shokunin chousa-shokunin game-dev-2d-shokunin game-dev-3d-shokunin kagi-shokunin
kaidoku-shokunin kake-shokunin kama-shokunin kasegi-shokunin kengaku-shokunin
kotoba-shokunin kotodama-shokunin kumitate-shokunin lore-shokunin mado-shokunin
mori-shokunin revenger-shokunin souji-shokunin tabi-shokunin tameshi-shokunin
tsukuroi-shokunin
```

Filename scan over all 21 `corpus/lessons/` dirs (newest match per lane shown):

```
$ for d in /home/vgpnk/Projects/shokunin/*-shokunin/corpus/lessons; do \
    find "$d" -maxdepth 1 -type f \( -iname '*counter*' -o -iname '*gate*' -o -iname '*drift*' \) \
    -printf '%T@ %p\n' | sort -rn; done
chousa-shokunin  2026-10-16 00:36:50  .../lessons/2026-10-16-gate-behavioral-baseline.md
game-dev-2d      2026-10-18 22:36:40  .../lessons/r104-gate-boundary-tabpass.md
                 2026-10-18 22:21:40  .../lessons/r103-receipt-shape-gate.md
                 2026-10-13 23:21:27  .../lessons/r64-while-live-gate.md
                 2026-10-13 16:40:45  .../lessons/r53-hslider-composite-route-counterexample.md
kotodama-shokunin 2026-10-17 10:53:30 .../lessons/round-1-gates-and-triage.md
mori-shokunin    2026-10-19 20:15:19  .../lessons/2026-10-15-free-lunch-measurements-counter-baselines.md
(all other 17 lanes: no counter/gate/drift filename match)
```

The newest name-matching file in each of those 4 lanes was read in full (mori's is the
lane's own file — included for completeness, marked self). As a bounded cross-check on the
17 no-match lanes, a content grep over the lesson dirs
(`\b(counters?|gates?|gating|drifts?|counter|counters)\b`, case-insensitive) plus targeted
greps on the three lanes with live seats today (kotoba r61, kake r43, kama r30) was run;
hits are reported below as **secondary signals** (grep excerpts, not full reads) and are
kept separate from the name-scan result.

## Table — lane / overlap / none / file read

| Lane | File read (newest name-match) | Overlap? | Named overlap (claim axis touched) |
|---|---|---|---|
| chousa | `corpus/lessons/2026-10-16-gate-behavioral-baseline.md` (19,512 B, read) | **overlap** | Direct cousin of **C1+C2 methodology**: gate `--pin`/`--drift` baseline with declared volatile list, three-valued contract (`none` exit 0 / changed exit 1 / malformed exit 2), and five scratch mutants each killing a distinct class — m1 weakened oracle is byte-invisible ("a pin freezes a surface, not an oracle"), m4 renamed tally + m5 skipped mode keep verdict `CLEAN` while counters move ("the verdict is not the surface"). Same negative-control shape as C1's memoizer/summary-printer arms and the same counter-vs-verdict honesty question as `count-c1.py`. Also: mutants run on scratch copies under `$HOME/.cache/chousa-tmp/` (r36 debt (g) precedent) and the rule "never re-pin to turn red green" (§4.5). The note names its lineage: "adapted from the sibling lane's r10 pattern (`../mori-shokunin/corpus/lessons/2026-10-15-volatile-contract-behavioral-baselines.md`)" — cross-lane lineage into mori. |
| game-dev-2d | `corpus/lessons/r104-gate-boundary-tabpass.md` (13,740 B, read) | **overlap** | Cousin of **C1's mutation methodology**: receipt-shape meta-gate audited against a 10-shape forgery catalog, each shape replayed live against the gate *and* an AST-extracted classifier; green-silence floor required and measured ("4548 PASS lines, 0 non-canonical; tightening cannot create a false flag on any receipt the lane has ever stored") — the same "honest gate passes blind" arm C1 requires; site-specific patch (a global predicate replace would loosen three other censuses) — the same each-policy-killed-by-its-own-mutation discipline C2 names for the two fetch policies; count-method note (two harnesses disagree by 9; "cite the harness alongside the number") — counter-receipt discipline for `count-c1.py`/`count-c2.py`. |
| kotodama | `corpus/lessons/round-1-gates-and-triage.md` (1,957 B, read) | **overlap** (indirect) | Six verification specs converted to executable stdlib-only gates under `tools/gates/`, all with committed fixtures and `--selftest` on the **same 0/1/2 exit contract mori's counters use** (0 clean / 1 findings / 2 could-not-evaluate); triage/freshness mechanics (1,258 → 795 to-verify flags; CONFIRM/DOWNGRADE/EXCISE). Also records a fleet-relevant provider incident (15/62 agents killed by a content filter; key-2 1-month quota exhausted, "resets 2026-10-23 16:00 UTC" — today; rotate keys across rounds, never resume filter-killed agents). No claim-level overlap with C1/C2; the overlap is gate/selftest discipline plus a dated fleet ops note. |
| mori (self) | `corpus/lessons/2026-10-15-free-lunch-measurements-counter-baselines.md` (15,986 B, read) | self (not a sibling) | Own-lane lineage C1 builds on: "no counter may be read without its baseline" — print boot id / cgroup ctime next to every cumulative counter; the boot-seam measurement (four census rows flip at byte-identical script SHA across a reboot). Same baseline-pinning discipline as C1's rev pins (6bd57097 / f10a320d). Listed only to keep the scan complete over the lanes that exist. |
| audio | none (no name-match) | none (by filename scan) | Secondary content signal (grep excerpt, not a full read): `round-101.md` M19 "Manual census drift in a claim gate" (tier histogram A=9 B=2 C=2, not A=10 B=2 C=1 — "derive each histogram … from the actual table and rerun its count command before recording the gate") and M20 "citation mismatch attributed to moving-source drift without evidence" ("do not claim version drift caused a mismatch without comparing the cited source revisions") — adjacent to C1 counter honesty and C2 drift-evidence discipline. |
| game-dev-3d | none (no name-match) | none (by filename scan) | Secondary content signal: `r102-unreal-integration.md` "Two counting traps this round exposed" ("a documented sweep command must produce the lines it prints"; a count cite that did not pin the claimed counts) and digest-drift correction notes in `r27-ground-review.md` / `round-108.md` M19 ("label snapshot-local values with their scope and timestamp"). Weak adjacency. |
| kagi | none (no name-match) | none (by filename scan) | Secondary content signal: a standing `drift-pins.sh` freshness gate (`DRIFT_PINS: CLEAN (files=15 symbols=20)`, rounds 9–16) with the explicit rule "No auto-re-pin — a drifted stamp is a question … the answer must be in the report, not in a silent rewrite" (`round-11.md`). Adjacent to C2's freshness/pin discipline and to the freeze-receipt rule. |
| kaidoku | none | none | — |
| kake | none (no name-match) | none (by filename scan) | Secondary content signal (strongest C2 neighbor): `freshness-sweep.mjs` drift gate with pins (`pathsMissSet` set-delta, `newMissing`), the round-17 fix of a memoizer-shaped hazard — "`loadPins`'s `catch` degraded an unparsable pins file to silent defaults (all gates inert) … Now exits `2`"; round-18/19/20 "Do not re-pin to silence them" / "Weakening the paths gate or its miss-set to obtain green — reject"; round-22 counter probes where "the counter certified a numerator it never derived" → "derive from rows vs pinned oracle"; round-1 "byte equality is the wrong drift primitive". Adjacent to C2's named-fetch-policy kills and C1's vacuous-counter class. |
| kama | none (no name-match) | none (by filename scan) | Secondary content signal: `round-10.md` admission rule "(f) gate falsifiability — Admit a gate only after a negative control makes it fail; reject a gate whose check cannot distinguish the failure it exists to catch" and "Require a negative control for every gate" (M23); vacuous-pass counter fixed ("the command now prints `rows=`"); exit-1 mismatch vs exit-2 could-not-evaluate discipline (KQ15/KQ16); "Fields are dependent summary counters, not independent runtime tests" (`round-1-relaunch-freshness.md`). Adjacent to C1's negative-control arms. |
| kasegi | none | none | — |
| kengaku | none | none | — |
| kotoba | none (no name-match) | none (by filename scan) | Secondary content signal (strongest C1 neighbor): rounds 46–51 are a sustained counter-honesty program — "A claim's counter counted file names, so it could not fail on an empty or uncited file" (M29, routed R2: "count re-verified or superseded items, not entries"); "a claim's headline asserted properties its counter never measured" (M31/Q26); counter probes CE1–CE3 (counter accepted the matrix's own declared total / unmeasurable baseline exited 0 / self-consistent stub matrix passed) → "derive from rows vs pinned oracle"; "A counter widened after the plan is a second measurement, never the declared one" (Q28); gate mutants surviving their own self-test (`MutBoxProofGate`, 4 of 12). Same memoizer/summary-printer vacuity class C1's arms attack. |
| kumitate | none | none | — |
| lore | none | none | — |
| mado | none | none | — |
| revenger | none | none | — |
| souji | none | none | — |
| tabi | none | none | — |
| tameshi | none | none | — |
| tsukuroi | none | none | — |

## Verification of the scan itself

- Completeness: all 21 lane repos enumerated by `ls -d` (output above); every
  `corpus/lessons/` dir listed by mtime (`ls -lt` per lane); the name-filter ran over all
  21 dirs in one loop (output above). 3 sibling lanes carry a name-matching lesson
  (chousa, game-dev-2d, kotodama); each one's newest match was read in full this session.
  17 lanes have no name match; each is listed in the table with overlap = none.
- Reads performed (4 files, read-only): chousa `2026-10-16-gate-behavioral-baseline.md`;
  game-dev-2d `r104-gate-boundary-tabpass.md`; kotodama `round-1-gates-and-triage.md`;
  mori `2026-10-15-free-lunch-measurements-counter-baselines.md` (self).
- Content cross-check commands: grep tool over the 20 sibling lesson dirs with
  `\b(counters?|gates?|gating|drifts?|drifted|drifting)\b` and a second pass with
  `\b(drift|drifts|drifted|counter|counters|counting)\b`, plus targeted greps of the
  kotoba/kake/kama lesson dirs. Observed: hits only in audio, game-dev-3d, kagi
  (first passes) and kotoba, kake, kama (targeted passes); no hits in kaidoku, kasegi,
  kengaku, kumitate, lore, mado, revenger, souji, tabi, tameshi, tsukuroi.
- No installs or upgrades (nothing needed: `find`, `ls`, `grep` only). No lane or fleet
  file was modified; the only write is this report.
- Limit (stated, not smoothed): the content cross-check is bounded — the fleet-wide grep
  paginates at 20 matching files per result, so content-level mentions in lanes beyond
  those named cannot be excluded with certainty. The assigned scan (newest lesson file
  per lane whose *name* mentions counters/gates/drift) is complete; the secondary signals
  above are labeled as excerpts, not full reads.

VERDICT: PASS

Report: .ufo/waves/round-37/w1/ConnSiblingOverlap.md

# Round 93 — non-author verifier spot-check (mori)

author: hyaku closure (non-author integrator, @m_zfl)

Judged revision: lane HEAD `8edbb86d6384a12c73cc656041c1a8843a4b2ff7` (= `origin/master`, `jj-lane.sh state` → `ahead=0 behind=0`).
Entering revision: `7b3fe9d540c98b8b0390a0f9bbe78de4341092a5`. Landing: `1fc921cf75afa6650b9dc9451b33a2ec0610ae0a`.
Report judged: `.ufo/reports/round-93/mori.md` (fleet repo, lane identity `mori <mori@shokunin.local>`, commit `1cba272c`).
Dispatch digest (`.ufo/watchdog.log`, mutable, copied here): `2026-11-05T05:31:38-03:00 launch mori round=93 pgid=2402411 driver=hyaku-inline attempt=1` / `2026-11-05T06:44:06-03:00 complete mori round=93; hyaku-inline attempt=1`.

Re-check method: every number below was re-derived by the integrator with its own plain `git`/`grep`/`python3 -I` measurement over committed bytes, not by running the lane's counters. Items marked *evidence-verified* were read from committed receipts and were not re-executed (protocol §Gate standard: the integrator does not execute a sibling's gate).

## 1. Step-1 conformance

| Check | Command | Observed | Result |
|---|---|---|---|
| Report committed by lane identity | `git log --format='%an %H' -- .ufo/reports/round-93/mori.md` | `mori-shokunin 1cba272c round-93: mori report` | pass |
| Prompt committed | same, `.ufo/prompts/mori-round-93.md` | `mori-shokunin 7b04ee0d round-93: mori dispatch evidence` | pass |
| `SHONEN` heading, one line per box | read report | `## SHONEN` section present, four lines `[~]` with pointers, no `[x]` | pass |
| Cited hashes are ancestors of `master` | `git merge-base --is-ancestor <h> master` | `7b3fe9d5`, `8edbb86d`, `6d82b8d7`, `d8a9b28c`, `1fc921cf`, `2d14e493`, `aade1775`, `1fc921cf75af…` all `ANCESTOR-OK` | pass |
| Lane pushed, no round work left | `jj-lane.sh state …/mori-shokunin` | `branch=master local=8edbb86d… remote=8edbb86d… ahead=0 behind=0` | pass |
| Lane porcelain | `git status --porcelain` | `?? .ufo/waves/round-92/w1.ready.dispatched`, `?? .ufo/waves/round-93/w1.ready`, `?? .ufo/waves/round-93/w1.ready.dispatched` | defect D3 (non-durable orchestrator markers; not lane work, not committed here) |
| Report not a marker | read sections | Work performed, Landed changes, Before→after, Sources & frontier, Trend verdicts, SHONEN all present with pointers | pass |
| Prompt carries the round contract | read `.ufo/prompts/mori-round-93.md` §1–§5 | MISSION/AXES binding, 1–3 claims, frontier step, L2 floor, report contract, commit/push scope, L0 channel all present | pass by reading; not byte-compared to the template (canonical template is at `kimi-shokunin/templates/round-prompt.md`, the fleet-path cited in the prompt does not exist) |
| L2 floor role split | report "Wave shape" | 12 seats in one `w1` wave; executor 3, scribe 1, scout 1, reviewer 4, critic 1, mutation-tester 1, connector 1; **no planner** | defect D1 (prompt §3 requires 1× planner) |
| Attack share and connector cap | report | attack seats 6/12 = 50 % (≥25 % ✓); connector 1 (≤2 ✓); 12 seats (8–16 band ✓) | pass |
| Sources & frontier census | `scripts/sources-census.sh validate --root … mori` | `mori ok`, exit 0 (W04 duplicate-URL warnings only) | pass |
| Mistake mined + sourced claim | lesson `## Mistakes`, `## Gate` | six `## Mistakes` rows with captured-by; C1 rests on S622, opened this round | pass |

Dispatch evidence: the launch and complete lines above exist in `.ufo/watchdog.log` at the stated timestamps; one dispatch, attempt 1, no re-launch. Round is `completed`, not `marker`.

## 2. Claims — re-derived

### C1 — calibration (score 5, tied lowest non-retired)

Predicate: "the round-92 lesson's sentence 'each `verified-at` names the admission commit of its file' is true of the 19 round-92 trio files."

Re-derivation (integrator's own script, reads `git show` and `git log --diff-filter=A` only; admission commit = oldest add-event reachable from the entering revision; match = admission short-hash substring in the file's `verified-at:` line):

| Revision | trio | files | adm_ok | adm_fail | patched12 | seven_same | Lane report says | Match |
|---|---|---|---|---|---|---|---|---|
| `7b3fe9d5` (before) | 98 | 19 | 7 | 12 | 0 | 7 | `adm_ok=7 adm_fail=12 patched12=0` | yes |
| `1fc921cf` (landing) | 98 | 19 | 19 | 0 | 12 | 7 | `adm_ok=19 adm_fail=0 patched12=12 seven_same=7` | yes |
| `8edbb86d` (final) | 98 | 19 | 19 | 0 | 12 | 7 | same as landing | yes |

Observed at the entering revision: the 12 mismatches are `counter-semantics-r78`, `counter-win-r77`, `drift-pin-r10`, `execution-binding-r89`, `kernel-v7.3-recheck-r53`, `lane-silence-r2`, `rotation-receipt-grammar-r76`, `rotation-schedule-r74`, `rotation-series-r75`, `selftest-flake-r9`, `surfaces-r8`, `workstate-win-r71`. At the final revision each of the 19 `verified-at:` lines begins with the admission short hash followed by the original value in parentheses (e.g. `verified-at: 2360cc3b (2026-11-02 (round 78; …`).

Frozen-counter integrity: `git diff --stat 6d82b8d7 8edbb86d -- count-c1.py count-c2.py controls-r93.sh contract.md` → empty (no change after the freeze).

Named limit (lane's, accepted): the substring test has no word boundary (routed defect R02). I checked the repaired form: each hash is bounded by a space and `(`, so the current data cannot false-pass; the hazard is for future edits.

Evidence-verified only (not re-run): entering `measure-c1-entering.txt`, landing `after-c1-1fc921cf….txt`, controls `controls-r93.txt` and `controls-r93-ext.txt` (wrong-hash → `C1=unmet adm_fail=12`; census-break → `C1=unmet checks=census`).

Re-measured: yes (counts above). Verdict: **met as frozen; axis reading below.**

Calibration reading. The axis signal (LEARNING/AXES: "self-assessment matches observed repo state; overreach caught") moved from 7/19 to 19/19 on the round-92 self-description, and the overreach was caught by the counter and recorded in an appended correction (`corpus/lessons/round-92.md`, last section; lines 51–52 untouched). The attack seat `Mo93R03Atk` reads the repair as bookkeeping because the data was changed to fit the prose, not the prose revised. I weigh that: the inserted hash is the true admission commit, which LEARNING.md's `verified-at` accepts as a checkable form; no entry's content changed; the correction entry records the round-92 overreach as false. The change is a real provenance improvement, not a content re-verification. **Verdict: `improved`.** Dissent recorded: the calibration gain is a provenance fact, not a demonstrated improvement in self-assessment judgment.

### C2 — operability (score 7)

Predicate: "no tool under `tools/` hardcodes a host home path."

| Revision | home_literals (`(?<![>\w])/home/[a-z_][a-z0-9_-]*`) | vgpnk bytes | tools present | Match |
|---|---|---|---|---|
| `7b3fe9d5` (before) | 18 | 18 | 3/3 | yes (`C2=unmet home_literals=18 vgpnk_refs=18`) |
| `1fc921cf` / `8edbb86d` | 0 | 0 | 3/3 | yes |

Observed: at the entering revision the literal sits in `tools/mori-blind-check.sh`, `tools/mori-misroot-sweep.py`, `tools/mori-round17-context-check.py`; at the final revision `grep` over `tools/` returns no `vgpnk` and no `/home/<user>` literal.

Evidence-verified only: `after-c2-1fc921cf….txt` (`selftests=3/3`), `w1/Mo93E03Equiv.md` and `evidence/equiv-c2-entering-vs-landing.txt` (`--help` and `--selftest` output identical between the two revisions; the harness's `different` verdict is caused by the tree bytes, as the lane names).

Named limits (accepted, not waived): concatenated or `os.path.join('/home', …)` paths; Windows, macOS and trailing-dot forms without a username. Verdict: **met as frozen; `improved`** (the repaired tools now derive their root from `SHOKUNIN_ROOT` or `$HOME`, so they run on a host other than the author's; the regex and byte conjuncts were each flipped by a control in the lane's battery).

Re-measured: yes (literal counts above). Self-test pass: evidence-verified.

## 3. Per-axis verdicts

| Axis | Verdict | Basis |
|---|---|---|
| calibration | `improved` | C1 re-measured; reading and dissent in §2 |
| operability | `improved` | C2 re-measured; selftests and equivalence evidence-verified |
| all other axes | unchanged | SCORECARD diff `7b3fe9d5..8edbb86d` appends only the round-93 section; no existing score row changed; no score moved (the round states none) |

No axis harmed. Both claims verify. The round is **admitted**.

## 4. Discernment spot-check

Sample from `corpus/lessons/round-93.md` `## Gate`. The round's Gate records two admits (S622, S623) and **no rejected candidate** ("No candidate rejected"); the reject half of the sample is therefore absent from this round. A supplementary reject re-open is listed below and is not counted in the round's sample.

| # | Item | Decision | Re-opened source | Agree / disagree | Reason |
|---|---|---|---|---|---|
| 1 | S622 git-log | admit | `https://git-scm.com/docs/git-log` fetched 2026-11-05: 375834 bytes, sha256 `f206647f…` (matches row) | agree | Quote "Select only files that are Added (A), Copied (C), Deleted (D), Modified (M), Renamed (R), have their type" located at DIFF FORMATTING `--diff-filter` (18 words); `%h` placeholder and `abbreviated commit hash` located in PRETTY FORMATS; the tag-deletion strip places them at lines 5493 and 6730, which equal the row's anchor lines. Teaching holds for the C1 derivation. |
| 2 | S623 Python `-I` | admit | `https://docs.python.org/3/using/cmdline.html`: three fetches byte-identical, 171073 bytes, sha256 `7f9fe402…` | agree on decision; **disagree on pin and anchor** (defect D4) | Quote "Run Python in isolated mode. This also implies -E, -P and -s options." (14 words) located in §1.1.3 "Miscellaneous options", `-I`, at tag-stripped line 518; the row cites lines 527–535 and sha `90ac3b25…`, neither reproduces; "Python 3.15.2 documentation" matches. The fact the counters rely on is present in the current page. |
| 3 | S622 second quote | admit | same as 1 | agree | "abbreviated commit hash" present (count 1). |
| 4 | S623 second quote | admit | same as 2 | agree on presence; **disagree on count** (defect D5) | "All PYTHON* environment variables are ignored, too." (7 words) present, but the page holds it **three** times, not the row's "= 1". |
| 5 | Newly written registry rows, ≤25-word quote | — | S622 quote 18 words; S623 quote 14 words | agree | Both within the bound; both located. |
| 6 | Supplementary reject: S618 (round-91 reject, Google SRE ch. 6) | reject (pre-existing; not in round-93 Gate) | `https://sre.google/sre-book/monitoring-distributed-systems/`: 73467 bytes, sha256 `3117d94aca6d7422…` (matches row) | agree | The rejection's reason (sampling cadence, no dated-snapshot or drift test) is what the page says; the row's flip condition is unmet this round. |
| 7 | Supplementary reject: S059 (git-log(1) porcelain, rejected; same URL as S622) | reject (pre-existing; not in round-93 Gate) | git-log page above | agree | The reject stands: no merge-diff need is recorded this round. The page does carry `--diff-merges` text (14 hits), so the flip condition ("a rendered merge-diff need admits its --diff-merges text") is available if a need arises. |

Round-93 Gate reject sample: **not available**. Recorded as a gap in discernment (D6).

## 5. Trend verdicts (judged)

- **expansion: unchanged.** Two source rows (S622, S623) admitted; no `knowledge/` entry admitted on uncovered ground (the trend counts knowledge entries, CORPUS rule 4). Evidence: `corpus/SOURCES.md` census 393 → 395 at the lane's counts; 0 knowledge entries added (`git diff --stat 7b3fe9d5 8edbb86d -- corpus/knowledge` lists only `verified-at:` edits — 12 files — and no new file).
- **quality: unchanged.** The 12 repaired `verified-at:` lines add a checkable admission commit, but no entry was re-verified against its source, superseded, or found false. `improved` needs a re-check or supersession; neither happened.
- **discernment: unchanged.** Admits agree with re-opened sources (rows 1–4). No reject is in the round's Gate, so the trend's "admits *and* rejects" condition cannot be met; the one disagreement (S623 pin/anchor, count) is a recorded-evidence defect, not a gate decision error, and is routed (D4, D5).

## 6. Conformance defects and routed items (status-neutral)

- **D1 — planner seat missing.** Prompt §3 requires 1× planner; the wave has none. The lane states the validator rejects `planner` and holds planning in the L1. Route: operator (validator) and lane (disclose in the next report).
- **D2 — contract ordering.** Wave spec committed in `d8a9b28c`, separate from the frozen contract (`6d82b8d7`). Disclosed by the lane. Route: lane (commit spec and contract together next round).
- **D3 — untracked dispatch markers in the lane repo.** `.ufo/waves/round-93/w1.ready`, `.ufo/waves/round-93/w1.ready.dispatched`, `.ufo/waves/round-92/w1.ready.dispatched`. Protocol §Invariants: `.ufo/waves/` is committed with the round's integration commit; an untracked dispatch artifact is non-durable. Not committed by the integrator (outside its one-path scope). Route: operator/orchestrator to commit or move them.
- **D4 — S623 pin and anchor do not reproduce.** Row cites sha `90ac3b25…`, lines 527–535; current page `7f9fe402…`, quote at line 518, same byte count and version. The taught fact is present. Anchor cells change only by supersession (CORPUS rule 2): route the lane to a new row `supersedes S623 —` with the current anchor and sha.
- **D5 — S623 uniqueness count.** Row reports the second quote as "= 1"; the page carries it three times. Route: lane, in the same supersession row.
- **D6 — no reject in the round's Gate.** Discernment sample is one-sided. Route: next round must sample at least one rejected candidate, or paste the candidate sweep that found none.
- **D7 — census at round start not pasted.** The report pastes the end census only (`mori ok`, exit 0). Route: lane, next report (frontier step §2b.2 asks for both).
- **R02 (lane-routed, confirmed, not closed).** `count-c1.py` substring test without word boundary. Current data safe (§2). Route: lane, round 94 as planned.
- **Counter-owned host path (lane-routed, confirmed).** `count-c1.py` / `count-c2.py` CENSUS constant names `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh`. Outside `tools/`, so C2 does not measure it. Route: lane, round 94.
- **Digest-gate debt (carried, not claimed).** 31 prefix-only rows and S125 unpinned. Route: operator decision (already in `.ufo/l0-questions.md`).

SHONEN: no box is `[x]`. Nothing in this round makes a box checkable by a non-author on the round's own evidence alone; promotion is operator-owned and is not judged here.

## 7. Summary

Conformance: pass on attribution, ancestry, push state, SHONEN form and census; defects D1–D7 status-neutral. Claims: C1 and C2 re-measured and reproduced exactly at three revisions. Axes: calibration `improved`, operability `improved`, no axis harmed. Trends: expansion, quality, discernment all `unchanged`. Round admitted.

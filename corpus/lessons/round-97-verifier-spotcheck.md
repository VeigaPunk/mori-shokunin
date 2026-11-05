# Round 97 — verifier spot-check (mori)

author: hyaku closure (non-author integrator, @m_zfl)

Closure of lane-round mori r97. Report `.ufo/reports/round-97/mori.md` (fleet repo); prompt
`.ufo/prompts/mori-round-97.md`; entering `973b2af11f41bd362163d7e29ac08286832f546b`, tip
`b6d034082582340a69371393d5bca25d04e05f4f`. Driver digest (copied from `.ufo/watchdog.log`):
`2026-11-05T17:42:15-03:00 launch mori round=97 pgid=1635907 driver=hyaku-inline attempt=1`;
`2026-11-05T18:15:39-03:00 complete mori round=97; hyaku-inline attempt=1`.
All measurements below were run by this closure at 2026-11-05T21:15Z–21:18Z over `git archive` trees of
`973b2af1` (before) and `b6d03408` (after) under `/fast/scratch/hyaku/closure-mori-r97/`. No lane gate,
selftest or frozen counter was executed by this closure (PROTOCOL §Gate standard, Closure consequence).

## 1. Step-1 conformance

| check | command | observed | result |
|---|---|---|---|
| report committed by lane identity | `git log --format='%an <%ae> %H' -- .ufo/reports/round-97/mori.md` | `mori-shokunin <mori@shokunin.local> b30a73cfb6ea…` (2026-11-05 18:15:20 -0300) | pass |
| `SHONEN` heading, one line per box | read report §SHONEN | 4 lines, one per SHONEN.md box, each `[~]` with a pointer | pass |
| cited commits exist + ancestor of `master` | `git cat-file -t <h>`; `git merge-base --is-ancestor <h> master` for `973b2af1 dd1ae115 e85ed912 5497e6f7 b6d03408` | all `commit`, all ancestors | pass |
| lane pushed | `scripts/hyaku/jj-lane.sh state …/mori-shokunin` | `branch=master local=b6d03408… remote=b6d03408… ahead=0 behind=0 head=detached tracked=2 untracked=0`; `ls-remote origin refs/heads/master` → `b6d03408…` | pass |
| no uncommitted round work | `git status --porcelain` | ` M .ufo/waves/round-97/w1/Mo97ScoutLive.md` (mtime 18:14:29 -03), ` M .ufo/waves/round-97/w1/Mo97ScribeLog.md` (mtime 18:15:41 -03) | **defect D1** (late seat writes after the last commit 18:14:18; status-neutral) |
| prompt carries template contract | every non-placeholder line of `kimi-shokunin/templates/round-prompt.md` (140 lines) searched verbatim in the prompt | missing 0; §1–§5 present, hyaku addendum §6 + §7 present | pass |

Not a marker: four lane commits, 47 files, +15798/−0 (`git diff --stat 973b2af1 b6d03408`). Status `ok`.

## 2. Claims — re-check

### C1 operability — four unregistered tools gain registry rows at the registry home (`SKILL.md`)

Re-measured (structure) + evidence-verified (selftest outcomes):

- `grep -c "tools/<tool>.py" SKILL.md` before→after: cgroup-pressure 0→1, drift-recheck 1→2 (the before hit is prose,
  not a row — the lane auditor's own `unregistered=4` at entering, `evidence/before-c1.txt`), scorecard-calibration 0→1,
  source-digest 0→1.
- The four appended rows under `## Round97 gate registry backfill` each split into 8 cells (`awk -F' \| '` → `8` ×4),
  i.e. the PROTOCOL §Gate standard row fields name · kind · entry · verdict map · self-test · pinned values · write scope ·
  owner. Self-test cells quote `MORI_CGROUP_PRESSURE_SELFTEST: pass=12 fail=0`, `MORI_DRIFT_RECHECK_SELFTEST: PASS (10 cases)`,
  `CALIB_SELFTEST pass=11 fail=0`, `DIGEST_SELFTEST pass=11 fail=0`.
- `git diff 973b2af1 b6d03408 -- SKILL.md`: 17 added lines, 0 removed (append-only).
- Committed evidence: `evidence/before-c1.txt` `C1=unmet unregistered=4 registry=unmet targets_ok=0/4` exit=1;
  `landing-c1.txt` (rev `e85ed912`) and `final-c1.txt` (rev `5497e6f7`) each `C1=met unregistered=0 registry=met
  targets_ok=4/4 checks_failed=-` exit=0, every TARGET line `selftest_rc=0 … stated_in_cell=yes token_in_verdict_map=yes`;
  counter sha256 `78a09016…d2a95` recorded in the receipt header = contract pin. Matches the report.
- Revision note: the final receipts measure `5497e6f7`; `git diff --stat 5497e6f7 b6d03408` touches only four receipt
  files under `.ufo/waves/round-97/evidence/`, so the measured surface equals the tip.

Verdict: **operability improved** (verifies).

### C2 freshness — S615/S616/S623 pinned with the recorded bytes and re-verified live

Re-measured (independent of the lane's counter and tools):

- `sha256sum corpus/evidence/sources-r97/*.html` at tip: S615 `7891c58897fe9f78…8a42f5` (362493 B), S616
  `6842ed0f53882c5a…23c3cb72` (53982 B), S623 `90ac3b25cb2dd281…f4831ad0` (171073 B).
- Recorded digests in `corpus/SOURCES.md`: S616 `6842ed0f…cb72` (equal), S623 `90ac3b25…31ad0` (equal), S615 records
  `…94b8f1a60ad1a6f0` (the r91 C-1 mis-record) and S619 — `supersedes S615` — records `7891c588…8a42f5` (equal).
- `cmp` S615 pin vs `.ufo/waves/round-90/w1/Mo90S01Sources/sources/python-ast-3.15.2.html` → identical; the r90 tokenize
  copy hashes `6842ed0f…cb72` = S616 pin.
- Live re-open 2026-11-05T21:17Z: `curl https://docs.python.org/3/{library/ast,library/tokenize,using/cmdline}.html` →
  200 / 362493, 53982, 171073 B; `diff pin live` → exactly one differing line per page, `Last updated on Nov 05, 2026
  (00:37|00:37|08:02 UTC).` vs `(12:47 UTC).` — stamp-only (`time-churn`), teaching content current.
- Before: no `corpus/evidence/sources-r9*/S61[56]*|S623*` copy in the `973b2af1` tree (before receipt `unpinned=3`).
- Committed evidence: `landing-c2.txt`/`final-c2.txt` `C2=met mismatch=0 unpinned=0 targets_ok=3/3 hole_guard=pass
  live=…time-churn ×3` exit=0; counter sha256 `957a7be6…1e91` = contract pin. Matches the report.
- `git diff 973b2af1 b6d03408 -- corpus/SOURCES.md`: +1 line (S628), no in-place edit to S615/S616/S623.

Verdict: **freshness improved** (verifies).

### Harm check

`git diff 973b2af1 b6d03408 -- SCORECARD.md`: append-only (+23), round-97 verdict table and Planned r98; no score cell
changed, "Score moves: none claimed". `corpus/knowledge/`, `corpus/QUALITY.md`, `PROVINCE.md`: no diff. Whole round
diff has 0 deletions.

| axis | verdict | basis |
|---|---|---|
| operability | improved | C1 above |
| freshness | improved | C2 above |
| depth | unchanged | no knowledge/SKILL depth change beyond the registry rows |
| coverage | unchanged | PROVINCE.md / knowledge/ no diff |
| calibration | unchanged | no calibration move; lesson's "42 W04" miscount (D2) is acknowledged in the report, not a self-assessment overreach |
| adjacency | unchanged | sibling stale-row finding routed, not absorbed (`w1/Mo97ConnSibling.md`) |

## 3. Discernment spot-check (`corpus/lessons/round-97.md` `## Gate`)

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S628 docsbuild-scripts README (new row) | admit, mined, tier B | `curl https://raw.githubusercontent.com/python/docsbuild-scripts/main/README.md` → 200, 6835 B, sha256 `0ae6b880…c618` = pinned `S628.md` | agree | quote found once in rendered text of raw lines 6-7 (link `[docs.python.org](…)` read as its text), `wc -w` = 12 (≤25, label "12 words" correct after the seat fix); primary maintainer repo for the build, tier B for a "pages are build artifacts" reading is honest (README states automated building, not per-build stamp semantics) |
| S623 pin (re-opened row) | admit pin (reconstructed bytes) | live cmdline.html sha256 `57b7f76b…6811` (= lesson's live value); diff vs pin = stamp line only; pin sha256 = recorded | agree | sha256 equality with the row's recorded digest makes the reconstruction the recorded fetch, not a new claim |
| pin today's live bytes as a recorded row's copy (r96 method) | reject | live tokenize.html sha256 `bce32489…da0e` (= lesson's live value) ≠ S616 recorded `6842ed0f…cb72` | agree | live bytes would make the digest gate report `mismatch`; a recorded row's copy must be its recorded bytes, a new reading is a new row (CORPUS SOURCES rule 2) |

SOURCES row re-opened: S628 (above) — quote present, ≤25 words, location correct.
Census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori` → exit 0, last line
`mori ok …/mori-shokunin/corpus/SOURCES.md`, 43 `W04` warnings (same 43 as the lane's `census-before.txt`/`census-after.txt`),
no non-W04 finding. Rows `grep -cE '^ {0,3}\| *S[0-9]{3,}' corpus/SOURCES.md`: 399 → 400.

## 4. Trend verdicts

- **expansion: unchanged** — `git diff 973b2af1 b6d03408 -- corpus/knowledge/` empty; S628 is a registry row (CORPUS rule 4).
- **quality: improved** — three stale-flagged rows re-verify against the live surface (stamp-only delta, re-measured here)
  and now carry their recorded bytes; no admitted entry failed a re-check.
- **discernment: improved** — outside spot-check agrees with the gate on the admit (S628, S623 pin) and the reject (live
  bytes as recorded copy).

## 5. Routed defects (lane fixes next round)

- **D1** uncommitted seat writes: `.ufo/waves/round-97/w1/Mo97ScoutLive.md` (+20, §7 incident check) and
  `Mo97ScribeLog.md` (+92/−34, F1 restatement) modified after the round's last commit; commit them as a labelled
  late-seat addendum or discard, and close seats before the final commit.
- **D2** `corpus/lessons/round-97.md` §Frontier step says "42 W04"; the census and the lane's own committed receipts print
  43 (report already flags it). Append a correction of record in the r98 lesson; do not edit the r97 file.
- **D3** carried, already in SCORECARD Planned r98: auditor residuals R1–R3 and the junk-row false green (lesson Mistake 4);
  calibration-counter survivor M10; 31 `prefix_only` digest rows; operator L0 mori | round-94/95/96 still open.
- **D4** cross-lane (for the aggregator/operator, not mori): 58 docs.python.org rows in 11 sibling lanes carry recorded page
  digests the same build-stamp churn will stale (`w1/Mo97ConnSibling.md` §1).

## 6. Closure result

status `ok`; both claims verify; no axis harmed → **admitted**.

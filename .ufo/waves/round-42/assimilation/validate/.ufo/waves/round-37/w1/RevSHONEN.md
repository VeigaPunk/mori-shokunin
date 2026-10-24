# RevSHONEN — SHONEN boxes + evidence-pointer resolution (mori r37 w1)

**Target:** every pointer in `/home/vgpnk/Projects/shokunin/.ufo/reports/round-37/mori.md`
(round-37 report, 12,688 bytes, present) — every `evidence/*.txt` path, every commit hash, every
SCORECARD capability row — plus the round's four SHONEN marks. Lane repo
`/home/vgpnk/Projects/shokunin/mori-shokunin` (read-only; all checks via `git cat-file`/`show`/
`ls-tree`/`diff`, no mutation). Scored tip `e57c58b57c025364e79d130fbdf764d2674d83d6`.

## SHONEN.md and the four boxes

`git show e57c58b5:SHONEN.md` → 8-line promotion checklist; all four boxes remain `[ ]` in the
committed file. The report marks each `[~]` (partial, promotion review is an open operator item).
Mark-by-mark:

| box | mark | check | result |
|---|---|---|---|
| SKILL.md real content | [~] | `git diff --name-only 842a320..c31076ed` → `SKILL.md` absent (untouched); cited ground `corpus/knowledge/source-drift-hardening-r37.md` resolves @e57c58b5; QUALITY 106/107 resolve @bcf65505 | resolves |
| end-to-end task logged | [~] | receipts committed (below); `LOG.md` Round-37 entry @c31076ed:2139 records `count-c1.py e57c58b5` → `C1=met` seed 13985344346805549517 and `count-c2.py e57c58b5` → `C2=met` | resolves |
| executable w/o oral context | [~] | `contract.md` P-C1:18-20, P-C2:58-60 verbatim @e57c58b5; counters + fixtures present; `w1-taskcall.json` @bcf65505 carries 48 absolute-path mentions | resolves |
| no cross-domain bleed | [~] | `PROVINCE.md` absent from the same diff (untouched); sibling scans ride the validated-but-undispatched wave per the report's own disclosure | resolves |

Honest `[~]`s — none overclaims a `[x]`.

## Evidence pointers (12/12 resolve at the named rev)

Method: `git ls-tree <rev> -- .ufo/waves/round-37/evidence/` + `git show <rev>:<file>` spot-reads.

| pointer | named rev | result |
|---|---|---|
| `evidence/freeze-r37.txt` | e57c58b5 | resolves — pins `7518fef8`/`6213cf9a` git blobs and sha256 `86699627…`/`71c72929…`; **verified against `git rev-parse e57c58b5:<path>` (blobs match exactly) and `sha256sum` (both match)** |
| `evidence/c1-before-memo.txt` | e57c58b5 | resolves — `C2=met`, `seed=11`, `EXIT=0` (memoizer admitted by r36 counter, as claimed) |
| `evidence/c1-before-summary.txt` | e57c58b5 | resolves — `C2=met`, `seed=12`, `EXIT=0` |
| `evidence/c2-before.txt` | e57c58b5 | resolves — `selftest/cap_kill/redirect_kill/knowledge/capability/readme/live FAIL`, `C2=unmet`, `EXIT=1` at 842a320 |
| `evidence/census-start.txt` | e57c58b5 | resolves — `mori ok`, same four W04 dup-URL lines, `EXIT=0` |
| `evidence/drift-live-r37.txt` | e57c58b5 | resolves — `rows=220 fresh=49 excerpt=0 drifted=9 unavailable=0 no-copy=162`, `EXIT=1` |
| `evidence/r17-jj-selftest-r37.txt` | e57c58b5 | resolves — `SELFTEST ok: …`, `EXIT=0` |
| `evidence/c1-after.txt` | bcf65505 | resolves — blind 24/24, real+challenge pass, three negatives rejected incl. `memo-n1.py rejected (challenge: lists differ …)`, `C1=met`, seed 13985344346805549517, `EXIT=0` |
| `evidence/c2-after.txt` | bcf65505 | resolves — all eight checks `PASS` (`selftest` lists 6 arms incl. `huge_cap`, `redirect_private_refused`; `cap_kill`/`redirect_kill` show each arm FAILing its mutant), `C2=met`, `EXIT=0` |
| `evidence/census-end.txt` | bcf65505 | resolves — `mori ok`, `EXIT=0` |
| `evidence/c1-after-tip.txt` | 5dff52a1 | resolves — `C1=met`, `seed=5097152322487907681`, `EXIT=0` (matches dispatch-log) |
| `evidence/c2-after-tip.txt` | 5dff52a1 | resolves — `C2=met`, `EXIT=0` |

All 12 also present at 52d636d5, 4bec58eb, c31076ed. Receipt content matches the report's quoted
output line-for-line (no honing to a plausible subset observed).

## Commit / object hashes (all resolve)

`git cat-file -t` results: `e57c58b5` commit (also `refs/jj/keep/e57c58b5…`), `842a3207…` commit,
`c31076ed` commit (git log tip is `0a05f7e`, a wave-seat-report commit on top — final lane tip claim
is stale by one commit but `c31076ed` resolves and `ahead=0` was its own check), `8ff9bba` commit,
`bcf65505` commit, `5dff52a1` commit, `52d636d5` commit, `4bec58eb` commit, `bf0df77` commit,
`6bd57097` commit, `f10a320d` commit (also `refs/jj/keep/f10a320d…`). Blobs `7518fef8`, `6213cf9a`
resolve and equal the counters' real blob ids. `refs/jj/keep/3b19cacb0444…` exists (`3b19cac`
prefix resolves). `LOG.md:1801` resolves (reads the `async.maxJobs: 200` operator-settings text the
report implies).

## SCORECARD capability rows (resolve)

`git show bcf65505:SCORECARD.md`:
- `## Round 37 declaration` :2035 + `### Round 37 measured outcome` :2061 — both present.
- Capability rows :2058 `| round-37 C1 | real-arm challenge counter | …` and :2059 `| round-37 C2 |
  source-drift re-fetch probe | …` — both present, pointing at the counters/tool/receipts above.
- Axis cells :13 (freshness) and :14 (calibration) now carry `round-37 claim C2/C1` clauses.
- At e57c58b5 the declaration + both capability rows already exist (:2035–2059), matching the claim
  that `capability PASS` is scorable at the scored tip; `measured outcome` lands at bcf65505.
- `corpus/QUALITY.md` :853 `106.` and :862 `107.` present @bcf65505 (absent @e57c58b5 — consistent
  with the landed table), each naming its lesson, check command, and able-to-fail receipt.

## Corpus / structural pointers (resolve)

- `corpus/SOURCES.md` S221–S225 rows present @e57c58b5 (:227–231, tier/kind/status as stated);
  row count 220 @842a320 → 225 @e57c58b5 and @5dff52a1 (report's `grep -cE` reproduced exactly).
- `corpus/evidence/sources-r37/` S221–S224 `.src` @e57c58b5; `S225.src` lands @52d636d5
  (1,854,393 bytes — the disclosed 1.9 MiB packaging defect, lesson M5), all five present thereafter.
- `corpus/knowledge/source-drift-hardening-r37.md` @e57c58b5 — cites S205, S221–S225, `8ff9bba`.
- `corpus/knowledge/source-drift-r36.md:24-33` @e57c58b5 — the nine-row drifted enumeration.
- `corpus/lessons/round-37.md` absent @e57c58b5 (correct — not yet landed), present @bcf65505 with
  Gate table quoting all five rows and Mistakes M1–M4; M5 present @c31076ed (:37, naming the
  1,854,393-byte file and `52d636d5`).
- `tools/mori-source-drift.py:398-415` @e57c58b5 — exactly the two named arms; `cap_body = 4 * 1024 *
  1024` literal at :402-403 (the anti-resize fix the lesson describes).
- `tools/mori-round17-jj-regressions.py` `jj_config_redirected` @e57c58b5:1065.
- `corpus/README.md` @e57c58b5:45-46 (two coverage rows incl. the missing r36 row), :585
  `## Round-37 coverage additions`. Report's word "README" denotes `corpus/README.md` — verified.
- Wave files @bcf65505: `w1-spec.json`, `w1-plan.json`, `w1-taskcall.json` (73 tasks parsed),
  `w1-validate.log` (0 bytes, matching "empty stderr"), `gen-wave-spec.py`; `dispatch-log.txt`
  @5dff52a1 records both `C1=met`/`C2=met` at e57c58b5 with the named seeds and evidence paths.
- Fleet `scripts/hyaku/ufo-wave-policy-v2.json` exists (12,676 bytes).
- `count-c1.py`, `count-c2.py`, `fixtures/{memo-n1,const,summary-only}.py` all @e57c58b5; r36
  counter `.ufo/waves/round-36/count-c2.py` @bf0df77.
- `watchdog.log` grep `lane-dead-no-report mori round=37` → 0 (inherited-state claim holds).
- P-C1/P-C2 verbatim in `contract.md` @e57c58b5 as claimed.

## Findings

- **LOW — numeric slip, pointer unaffected:** the report states "`w1-taskcall.json` (73 tasks,
  **82,884** bytes)"; the committed blob and working copy are both **83,204** bytes
  (`git cat-file -s bcf65505:…/w1-taskcall.json` → 83204; `wc -c` → 83204). Task count 73 correct;
  looks like transposed digits. The pointer resolves; only the size annotation is wrong.
- **Informational:** fleet `git status --porcelain` now shows 36 entries vs the report's 34 —
  live driver state mutates between sessions; the report's count was a timestamped observation,
  and none of the 36 name `mori` or `round-37`. Not a defect.
- **Informational:** actual lane tip is `0a05f7e` (wave-seat reports + lesson M6, committed after
  the report's `c31076ed` "final tip" line). `c31076ed` still resolves; the wave-returns disclosure
  remains consistent since seat reports land as separate commits by design.

## Residual risk / gaps

- Receipt integrity: file contents were spot-read (headers, verdict lines, seeds) — all consistent;
  I did not re-execute `count-c1.py`/`count-c2.py` (other seats own execution; my scope is pointer
  resolution).
- `evidence/c2-after-tip.txt`'s `capability PASS (rows=1 …)` counts only the `round-37 C2` row —
  consistent with the counter checking the row that names `tools/mori-source-drift.py`, not a
  missing-row signal (both capability rows verified present by direct read).
- LSP not applicable (no server speaks git-blob revs); all checks are direct object-store reads,
  stronger than index resolution.

**Tooling:** none installed (python3 + git only; pacman untouched per host-wide pause).

VERDICT: PASS — every `evidence/*.txt` pointer, every commit/blob hash, every SCORECARD capability
row, and every corpus/structural pointer in `mori.md` resolves at its named rev; all four SHONEN
`[~]` marks are honest and none of their cited supports is absent.

Report: .ufo/waves/round-37/w1/RevSHONEN.md

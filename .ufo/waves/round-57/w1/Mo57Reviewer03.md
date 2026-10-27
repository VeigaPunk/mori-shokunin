# Mo57Reviewer03 — C1 mutation report (round 57 w1)

Seat: C1 mutation — mutate each capability-row field (name, evidence path, first-working round) and check whether the frozen counter rejects it. All paths relative to `/home/vgpnk/Projects/shokunin/mori-shokunin`. No production edits or commits; no installs (pacman paused).

## Verdict

The frozen counter `.ufo/waves/round-57/count-c1.py` fails closed on every committed state, but it is **not a faithful operationalization of the C1 predicate** (contract.md:5): **four distinct predicate-violating mutation classes survive** (accepted with rc 0), with additional substring-preserving name mutations also accepted. Separately, **the claimed after-state does not exist at the freeze tip** — the counter is unmet (`rows=0`) at `618562c7` exactly as at the entering tip.

## F1 — HIGH: counter accepts predicate-violating rows (4 survivors)

Method: the counter hardcodes the production repo (`count-c1.py:6`) and reads `git show R:SCORECARD.md` (`count-c1.py:7`), so mutations must be commits. I cloned the lane at `618562c7` into scratch (`/fast/scratch/hyaku/mori-r57/Mo57Reviewer03/fixture`, toplevel guard asserted before every commit) and ran a copy of the counter differing by exactly one line (the `repo=` path; `diff` vs `git show 618562c7:.ufo/waves/round-57/count-c1.py` = that line only). Positive control first: two faithful rows (name + capability text + evidence pointer into the real `.ufo/waves/round-56/evidence/` files, first-working 56) replacing SCORECARD:600 `| — none yet — |` → `C1=met rows=2`, rc 0. Both evidence files verified present at that rev via `git ls-tree`.

| Case | Mutation | Result | Why it survives |
|---|---|---|---|
| M4 (`f28b006c`) | evidence pointer → `.ufo/waves/round-56/nonexistent-evidence.txt` | `C1=met rows=2 evidence=ok` rc 0 | `count-c1.py:12` checks the substring `.ufo/waves/round-56/`; **never resolves the path**. `git ls-tree` at that rev: 0 entries — pointer unresolvable, counter says `evidence=ok`. Predicate "resolvable evidence pointer" unenforced. |
| M6 (`7df30d0d`) / M6b (`b907ff48`) | replace the vote-binding row with a duplicate driver-liveness row (M6b: two vote-binding rows) | `C1=met rows=2` rc 0 | `count-c1.py:11-12` counts the **union** of rows containing either name and requires only `len(rows)==2`; per-name presence is unenforced — one capability can vanish entirely. |
| M9 (`ab590920`) | first-working cell `56`→`55`, literal `\| 56 \|` smuggled into the prose cell | `C1=met rows=2 evidence=ok` rc 0 | `count-c1.py:12` substring `\| 56 \|` matches **any column**; cell semantics unenforced. |
| M7 (`c464c1e0`) / M1b (`f7dee3e0`) | name cell gutted (`lane probe` / `driver-probe`) | `C1=met rows=2` rc 0 | `count-c1.py:11` matches the name substring **anywhere in the row**: the real evidence filename `.ufo/waves/round-56/evidence/driver-liveness-live.txt` carries `driver-liveness`, so any driver-liveness name-cell mutation is masked. Asymmetry: vote-binding **is** name-cell-enforced only because the real file `selftest-vote-bind.txt` spells `vote-bind`. Weak renames also survive outright (`driver-liveness-probe`, `vote-binding-v2`: M1 `f70bfd5c`, M2 `b0de92e6` — substring preserved). |

## F2 — HIGH: the C1 after-state does not exist at the freeze tip

- `python3 .ufo/waves/round-57/count-c1.py 618562c72a03dc4d17386b715357f863fd327274` → `C1=unmet rows=0 evidence=bad`, rc 1 (run directly, production). Identical to the entering-tip control (`controls.txt:2-3`: `rows=0`, rc 1).
- `git show 618562c7:SCORECARD.md` lines 596-604: the live `## Capabilities` table contains only `| — none yet — |` (line 600). Zero rows naming `driver-liveness` or `vote-binding`.
- `git log --all --oneline -S 'vote-binding' -- SCORECARD.md` → **empty**: the literal `vote-binding` string was never committed to SCORECARD.md on any ref.
- Only reachable SCORECARD occurrence of `driver-liveness` is the round-56 verdict prose claim-table (`eac193ca`; SCORECARD.md:2897, 2903 at `618562c7`) — outside the counter's slice (`count-c1.py:10` slices first `## Capabilities`→first `## Saturation` = lines 597-603).
- Round-56's own counter verified tool landing (`tools/mori-driver-liveness.py` PIN/selftest/fixtures — round-56/count-c1.py), not capability-table rows; its SCORECARD section (eac193ca) added the claim table, not capability rows.

So the predicate's "after: 2 matching rows" is unrealized at freeze. If round-57 settlement later adds the rows, the calibration claim becomes self-fulfilling (made true by the settlement that checks it) rather than a verified property of round 56. [INFERENCE on intent; the observable fact is: unmet at both entering tip and freeze tip.]

## F3 — MEDIUM: slice fragility — counter can be retargeted to a stale section

M8 (`5a863f8b`): deleting the live `## Capabilities` heading (SCORECARD:596) makes the counter silently read the stale historical section `## Capabilities (round 12 demonstrations)` (verified: at that rev the first match is that heading; grep shows it at line 637, after a `## Saturation` at 604). Fail-closed here (`rows=0` → unmet), but the counter judged the wrong (round-12) table. `count-c1.py:10` prefix-matches any `## Capabilities …` heading. Code-level note: a SCORECARD with zero such headings would raise `IndexError` at `count-c1.py:10` (unhandled traceback; still rc≠0, fail-closed).

## F4 — what the counter does reject (confirmed kills)

| Mutation | Result |
|---|---|
| M3 (`59605ddb`): evidence prefix `.ufo/waves/round-56/` → `.ufo/waves/round-55/` | `C1=unmet rows=2 evidence=bad` rc 1 |
| M5 (`c0db91e4`) / M5b (`772daf8f`): first-working `56`→`55` / `57` (substring-preserving rows) | `C1=unmet rows=2 evidence=bad` rc 1 |
| M2b (`82e703d8`): both name cells truly renamed AND row no longer carries either substring anywhere | `C1=unmet rows=1` rc 1 |
| Unresolvable revision R (nonexistent sha) | `C1=unmet rows=0 evidence=bad` rc 1 (early return, `count-c1.py:8-10`) — fails closed |
| Baseline unmutated fixture | `C1=unmet rows=0` rc 1 — parity with production controls |

## Residual risk and gaps

- C2 counter (`count-c2.py`) not mutated here — out of seat scope.
- The counter enforces nothing about the "What it can now do" text and nothing about row position within the slice beyond the first-table slice; F3 shows slice identity is not guaranteed.
- Fixture revs cited above live only in `/fast/scratch/hyaku/mori-r57/Mo57Reviewer03/fixture` (scratch, removed after this report); every claim is reproducible from the cited production refs and the counter text.
- No tool installs or updates performed; pacman untouched.

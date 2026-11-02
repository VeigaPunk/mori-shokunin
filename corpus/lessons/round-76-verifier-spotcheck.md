# mori round 76 — verifier spot-check (non-author closure)

author: hyaku closure (non-author integrator, zcode subagent (fresh session, non-author))
lane: mori-shokunin · round 76 · entering `fdb11b1d8d9d9ead6bf1ad17d699d7cf4b39acc4` · head `71107662db7fea4be4709239378f79f3cddca78b` (branch master)
closed: 2026-11-02 (UTC); every command below was run by this verifier against committed bytes (`git show <rev>:<path>` / `git diff-tree` / `git ls-tree` / `git log`) unless marked "run in worktree". No lane-authored file was edited; this file is written by the closure judge and left uncommitted for the orchestrator.

## Step-1 conformance

| Check | Command | Observed | Result |
|---|---|---|---|
| Report committed by lane identity | `git -C <fleet> log --format='%an <%ae> %H' -1 -- .ufo/reports/round-76/mori.md` | `mori-shokunin <mori@shokunin.local> 6b0ce50b…` | PASS |
| `SHONEN` heading in report | read of `.ufo/reports/round-76/mori.md` | `## SHONEN` present, 4 boxes, all `[~]` with pointers | PASS |
| Cited lane hashes exist + ancestral | `git cat-file -e <h>^{commit}` + `git merge-base --is-ancestor <h> refs/heads/master` for `32132cfb`, `986d4b46`, `fdb11b1d`, `71107662` | all exist, all ancestral rc 0 | PASS |
| Lane tip pushed | `git ls-remote origin refs/heads/master` vs local `rev-parse refs/heads/master` | both `71107662db7fea4be4709239378f79f3cddca78b` | PASS |
| Round work reachable in range | `git diff fdb11b1d..71107662 --name-only` | exactly 17 paths, 2627 insertions, 7 deletions — matches the report | PASS |
| Dispatch digest | grep of `.ufo/watchdog.log` | `2026-11-02T03:54:05-08:00 launch mori round=76 base=fdb11b1d8d9d (zcode run14)` / `2026-11-02T06:17:15-08:00 complete mori round=76 head=71107662db7f pushed=True` — matches the contract digest | PASS |
| No `[x]` written by the lane | `git show 71107662:SHONEN.md` grep `^- \[x\]` | count 0; the SHONEN diff only re-asserted `[~]` pointers | PASS |
| Out-of-scope files absent from the round diff | name-only list | PROVINCE.md, AGENTS.md, corpus/QUALITY.md, tools/ all absent | PASS |

## Per-claim re-check (all three claims RE-MEASURED by this verifier)

### C1 (calibration) — both r75 closure carry-ins discharged. Verified met.

Carry-in 1 (the line-count precision correction of record):

- `git show 32132cfb:SCORECARD.md | grep -c ""` → **3819** (the report's corrected after-count).
- `git show 32132cfb --numstat -- SCORECARD.md` → **61 0** (matches).
- Decomposition: line 3759 is blank (`sed -n '3759p'` prints `$` in cat -A), `grep -n "^## Round 75"` at `32132cfb` → **3760** (backfill) and **3774** (Round 75 section) — 1 + 14 + 46 = 61. Both deltas now stated in the LOG entry and the report; `grep -c "backfill-only intermediate" LOG.md` at head → **2** (the correction sentence + the command itself). No r75 artifact edited (SCORECARD/LOG diffs are pure appends).

Carry-in 2 (the corpus README retrospective knowledge-index repair):

- Unindexed-knowledge loop re-run by this verifier over the committed trees: at `fdb11b1d`, **17** knowledge `.md` entries absent from the README (11 r59–r75 + 6 r40–r57 stragglers, names as reported; `.gitkeep` excluded); at `71107662`, **0**.
- `README` lines 808 → **852**; `git show fdb11b1d:corpus/README.md | head -808 | sha256sum` and the same over `71107662` both → `fbe94947b590e107d4c71b70e9b823491592d73c717792f69d82c8af921962eb` — **every entering byte unchanged**.
- The new section (README:809–852) carries **all 17 rows**, and the three rejected-closure entries carry honest status notes: r59 "closed rejected-honest-stop, so no capability claim rides on it"; r60 "round 60 closed rejected-honest-stop"; r61 "closed rejected-honest-stop and its C2 verdict stays unmet on the frozen counter (re-derived rc 1 every r65–r76 spotcheck)". "not new growth" stated in the section itself. Same-round knowledge-addition subsection indexes the round's own entry (846 → 852).

### C2 (depth, sourced S591) — the receipt-grammar decision table at the registry home. Verified met.

- Append-only: `SKILL.md` 1327 → **1351**; `git show fdb11b1d:SKILL.md | sha256sum` == `git show 71107662:SKILL.md | head -1327 | sha256sum` → `8e2875446f8e629a…` (entering prefix byte-identical); `sed -n '905p' SKILL.md | grep -c "PASS (6 cases)"` → **1** (the SKILL:905 pin unchanged); `grep -c "^## Round76"` 0 → **1**.
- The end-section table (SKILL.md:1328–1351) carries 9 decision rows: rotated=yes / no / unavailable readings, `window_s_computed` under QUALITY 161, the clock leg grounded at BOTH layers (S589 invariant + S591 vendor QPC quotes with located anchors), the S581/S586 documented scale, the S590 mechanism layer, `wall_s` informational, and the limits. All elements claimed in the report are present.
- Prose ground `corpus/knowledge/rotation-receipt-grammar-r76.md` exists at head (rc 128 at entering), opens with the `source:`/`verified-at:`/`recheck:` trio citing S591, carries S1–S5 + declared limits + boundaries.
- S591 registry row: SOURCES rows **363 → 364** (`grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'`), `badNF=0` over 364, row at SOURCES.md:372 immediately after S590; S581/S589/S590 used-by cells each gained the new entry path (SOURCES diff = exactly 3 modified rows + 1 new row; statuses/recheck cells untouched).
- Pinned copy `corpus/evidence/sources-r76/S591.html` at head: sha256 **`2338936938…ffc1c`**, 106427 bytes (matches the row); quotes verified ON the cited lines — `:918` "Yes. QPC does not go backward." (6 words), `:863` "is completely independent of the system time and UTC." (9 words); `<title>` matches.
- Anchor-checker re-run BY THIS VERIFIER against the committed pin extracted to scratch:
  - run A (recorded anchors): `python -I tools/mori-anchor-check.py --pin <scratch>/S591-committed.html --check "qpc_monotonic|918|6|Yes. QPC does not go backward." --check "qpc_independent_utc|863|9|is completely independent of the system time and UTC."` → `ANCHOR_CHECK: PASS items=2 ok=2` **rc 0**.
  - run B (able-to-fail mislocation arm, wrong line + mutated count): → `verdict=mislocated`, `ANCHOR_CHECK: FAIL` **rc 1**. Both reproduce the committed receipt exactly.
- Grammar probe re-run BY THIS VERIFIER (the grammar applied to committed receipts): `.ufo/waves/round-74/evidence/rotation-schedule-live-r74.txt` re-classifies 31s=no / 91s=no / 304s=**yes** (per-response=4, capture sha 3e0ece8127c6 → 5d88b3cc6039), summary `window_s_computed=31,91,304`, `wall_s=429`; `.ufo/waves/round-75/evidence/rotation-schedule-live-r75.txt` re-classifies **all-no** — exactly the per-window facts the SKILL table and the knowledge entry teach (yes at DIFFERENT windows across sessions; 31s no ×3; all-no a real outcome).
- Live re-open of the source (this verifier, `curl -sS -m 60 -L`): the URL resolves today to 106427 bytes, sha256 **equal to the pin**, title and quote present — the pin is currently byte-identical to live.
- No new session, no window change, no TTL decided (the round's evidence dir carries no new live-schedule receipt; the table and entry state the boundary).

### C3 (freshness) — the standing pin-family arm. Verified met (re-measured).

- Committed receipt `.ufo/waves/round-76/evidence/pin-family-r76.txt` carries the four verdict lines exactly as reported (S581/S590 IDENTICAL; S241 DRIFTED live=`ddb7ba17…` — equal to the r74/r75 live sha; S589 DRIFTED `c8cc430e…` → `29167186…`), the instrument line `MORI_DRIFT_RECHECK rows=4 adjudicated=4 fresh=2 time-churn=1 asset-churn=1 … rc=0`, the S589 two-changed-lines stamp-only diff (`Last updated on Nov 02, 2026 (03:08 UTC).` → `(13:28 UTC).`, stamp line :1553 in both bodies, monotonic anchors :524-525 present in live), the S241 two-asset-URL-pair diff (0.4.03574.8308-9505b1c8 → 0.4.03589.8339-b0a05127), the both-methods teaching block (lines 3/3, occurrences 6/6), and the draft-1 guessed-URL disclosure.
- `python -I tools/mori-drift-recheck.py --root . --only S241,S581,S589,S590` RUN BY THIS VERIFIER at closure time → `S241 asset-churn / S581 fresh / S589 time-churn / S590 fresh`, `rows=4 adjudicated=4 fresh=2 time-churn=1 asset-churn=1`, **rc 0** — the same four-way adjudication, reproduced independently an hour after the round's run.
- The four committed pin blobs at head hash to the receipt's recorded shas (1168b2a6 / 5e5b941e / c8cc430e / 8bff4311). No fourth schedule session (receipt header: "NO schedule session is run (the r75 planned head (d) stands)").

### Standing battery + census (evidence-verified, spot re-derived)

- `.ufo/waves/round-76/evidence/selftests-battery-r76.txt`: `grep -c "^rc=0$"` → **11** (matches the report; evidence-verified — this verifier does not execute the lane's battery per the contract).
- Census receipts: census-start and census-end each carry **35** W04 rows and `exit=0`; the census validator re-run by this verifier at closure → the same 35-row W04 class, **rc 0**.

## No axis harmed

`git diff fdb11b1d..71107662 -- SCORECARD.md` is a single append hunk (`@@ -3817,3 +3817,51 @@`); the axes rows (coverage 6, operability 7, depth 5, freshness 5, calibration 5, adjacency 6) are byte-identical entering→head. PROVINCE.md, AGENTS.md, corpus/QUALITY.md and every registered tool are absent from the round diff; the battery receipt is green at the round's bytes.

## Per-axis verdicts (this verifier, all re-measured or evidence-verified as marked)

| Axis | Verdict | Basis |
|---|---|---|
| calibration | **improved** | C1 re-measured: both carry-ins discharged with re-derivable evidence (3819/61-0 decomposition; 17 → 0 index repair with entering-sha proof); honest statuses on rejected entries, not silent adoption |
| depth | **improved** | C2 re-measured: the grammar table at the registry home (append-only, pin untouched), prose ground with provenance trio, S591 opened with sweep/title/anchor discipline — checker PASS + able-to-fail FAIL re-run by this verifier |
| freshness | **improved** | C3 re-measured: this verifier's own instrument run reproduces the four-way discrimination (2 fresh, 1 asset-churn, 1 stamp-only time-churn); teaching re-verified both methods; no supersedes owed (anchors hold on the pins) |
| coverage | **unchanged** | no census surface claimed; PROVINCE.md untouched |
| operability | **unchanged** | no instrument byte edited; battery 11/11 evidence-verified |
| adjacency | **unchanged** | foreign evidence reported, not absorbed, not committed; PROVINCE.md absent from the diff; vendor mechanisms cited, not absorbed |

No exploratory claim declared this round; no `unprovable-but-better`/`unprovable` grading arises.

## Discernment spot-check (non-author, ≥1 admit + reject-class re-opens)

The round's `## Gate` records ONE admit (S591) and "Rejected: none this round" (the duplicate sweep found no candidates). Reject-class decisions elsewhere in the round were re-opened instead:

| Item | Decision | Re-opened source (by this verifier) | Agree/disagree | Reason |
|---|---|---|---|---|
| S591 admitted (tier A, Windows-clock-realization scope) | admit | LIVE re-open of `https://learn.microsoft.com/en-us/windows/win32/sysinfo/acquiring-high-resolution-time-stamps`: 106427 bytes, sha byte-identical to the pin; title matches; both quotes present on the cited lines; anchor-checker PASS items=2 rc 0 re-run; ≤25-word quotes (6 + 9 words) verified with locations | **agree** | Official vendor documentation, correctly tiered and scoped; the located-quote discipline held (the strong-tag span on :863 is recorded as such); the duplicate-sweep interpretation (S589's `:529` mention is not a duplicate row) is correct — S589's row cites the Python time page, not this one |
| Frozen r61 honest-stop rejection stands | reject (standing) | `python -I .ufo/waves/round-61/count-c2.py 986d4b46db6e67682ef84091f606d125f987ecbc` re-run BY THIS VERIFIER → `C2=unmet pointers=47 rows=47 … failed=quote_words:…` rc 1, byte-identical to the round's fresh-start receipt | **agree** | The same verdict every closure and re-derivation reached; indexing the entry with an honest rejected-honest-stop note (not re-trying the claim) is the right treatment |
| Draft-1 S241 fetch artifact rejected (guessed URL → ja-jp 404 frame; receipt redone) | reject (in-round) | The committed pin-family receipt's draft-1 disclosure (17962 bytes, sha `91abedbf…` measured on the 404 frame) + this verifier's own instrument re-run: on the ROW's URL the live serving hashes `ddb7ba17…` (asset-churn), not the 404 artifact | **agree** | A receipt must measure the row's URL; the guessed-URL draft measured the wrong artifact and the lane caught it by its own title/diff check, redid the fetch, and mined the mistake |
| Foreign round-76 plan (Event-ID-41 S591) NOT adopted | reject (implicit) | The three worktree-only files inspected (class/counts only); the landed S591 row + pin are this L1's QPC page; `git log --all -- <foreign paths>` → empty (never committed by anyone); `git grep` over the committed tree shows the only mentions are the disclosure itself in LOG.md and the lesson | **agree** | Internally coherent but unverifiable by this author, and the claimed 67455-byte pin (sha `9613e8b0…`) no longer exists at the shared path (it now holds the landed 106427-byte QPC copy); absorbing it would have rested a claim on unverifiable bytes |
| SOURCES row S591 quotes (the ≤25-word quote duty) | — | Both quotes re-verified at their cited lines in the pinned copy, word counts 6 and 9 as recorded | **agree** | Quotes are verbatim, located, and within the word floor |
| `sources-census.sh validate` | — | Re-run at closure: rc 0, the tolerated 35 W04 duplicate-URL class — matches census-start/census-end receipts | **agree** | Registry shape holds over 364 rows |

## Foreign-evidence finding — disposition ruling

Three receipt files sit in `.ufo/waves/round-76/evidence/` uncommitted and unauthored by this round's L1: `source-s591-sweep-r76.txt` (mtime 12:25:33Z), `s591-source-r76.txt` (12:44:30Z), `win-family-live-r76.txt` (12:48:15Z) — between the 11:54:05Z dispatch and the L1's first evidence write (census-start, 13:05:35Z). Verification by this verifier:

- **Disclosure complete**: a whole-worktree sweep (`git ls-tree -r HEAD` vs `find`) finds exactly those 3 files beyond the committed tree in the evidence dir (plus `tools/__pycache__/*.pyc` interpreter bytecode — runtime artifacts, not evidence, not authored content; see notes).
- **Uncommitted**: absent from the committed tree at `71107662` AND from every commit in the repo's full history (`git log --all -- <paths>` empty).
- **Not cited as evidence**: the only committed mentions of the three names are the disclosure itself (LOG.md Round 76 entry; the lesson's disclosure section) — no claim rests on them.
- **Disclosure accurate**: the foreign `s591-source-r76.txt` indeed names a different S591 (kernel-power/Event-ID-41 sweep with slug probes rejected as 404 frames) claiming a 67455-byte pin sha `9613e8b0…` at the SAME path `corpus/evidence/sources-r76/S591.html`, which now holds this round's landed 106427-byte QPC copy — the claimed foreign pin no longer exists on disk, exactly as disclosed.

**Ruling: leave-for-operator is DEFENSIBLE.** Committing them would fabricate provenance (third-party receipts landed under the lane's identity); citing them would rest claims on bytes this author cannot verify whose central artifact is gone; deleting them would destroy the material the operator needs to disposition a misrooted/parallel-attempt finding. The lane's own claims rest only on its own receipts, and nothing landed depends on the foreign files.

## Trend verdicts (this verifier)

- **expansion: improved** — one new knowledge entry (`rotation-receipt-grammar-r76.md`, S1–S5) on ground the schedule family did not hold, `source:` citing the new mined row S591; SOURCES 363 → 364 re-counted; the README index now covers the whole knowledge registry (17 entries newly discoverable).
- **quality: improved** — both carry-ins discharged with re-derivable evidence; append-only sha proofs verified on README/SKILL/LOG/SCORECARD; the standing freshness practice discriminates four ways in one receipt, reproduced by this verifier's own run; battery 11/11; census rc 0 both ends and at closure; five mistakes mined with class/evidence/captured-by/fix.
- **discernment: improved** — rejected-closure entries indexed with honest statuses; no TTL decided despite new clock ground; a same-day fourth session refused; foreign evidence found, reported, not absorbed; three in-round drafting defects (guessed-URL 404, title-pipe NF=14 ×2, rc-after-pipe) caught by the lane's own standing checks before landing; this verifier's spot-checks agree with the gate on the admit and on every reject-class decision re-opened.

## Defects and routed items (status-neutral; none bars admission)

1. **SHONEN boxes fully checkable by a non-author** (for the operator): all four `[~]` boxes' substance was re-derived by this verifier from committed bytes this round (the SKILL table + shas; the LOG entry + receipts; the battery tally; the PROVINCE-absent byte-diff). Per duty, the operator may authorize the `[x]` promotion review whenever it runs — this file is the non-author evidence pointer for box-by-box re-derivation.
2. **`tools/__pycache__/*.pyc` (5 files) sit uncommitted in the worktree** — interpreter bytecode from running the registered tools (including this verifier's own runs), not lane-authored evidence and not part of the foreign-evidence class; operator may sweep. Not a defect of the round.
3. **Foreign receipts disposition rides with the operator/orchestrator** (ruling above): archive or delete `source-s591-sweep-r76.txt`, `s591-source-r76.txt`, `win-family-live-r76.txt` and, if a parallel round-76 attempt was real, reconcile it in the driver records — the claimed foreign pin (67455 bytes, sha `9613e8b0…`) is unrecoverable at the shared path, so those receipts can never be evidence.
4. No routed defects owed by the lane: the r75 closure's two carry-ins were discharged this round (verified above), and no new cross-domain or self-defect surfaced in this verifier's re-derivation.

## Verdict

All three claims verify (re-measured by this verifier); no axis is harmed; conformance is clean; the foreign-evidence handling is honest and complete. **mori r76: status ok, admitted.**

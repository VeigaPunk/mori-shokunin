# Round 78 — mori verifier spotcheck (non-author closure review)

author: hyaku closure (non-author integrator, zcode subagent (fresh session, non-author))
round: 78
date: 2026-11-02
entering: `ecb916ce0105c37142aef08def00d95ec70cf503` (lane HEAD before the round)
lane head after: `22dbaae4364425e59c9cbc07d9c83363a6b4426e` (branch tip, pushed)
method: index-free git only (`rev-parse`, `cat-file`, `ls-tree`, `diff-tree`, `merge-base --is-ancestor`, `show`, `log`, `ls-remote`); no `git status`/`read-tree`/`checkout`/mutating commands anywhere; the counter tool was re-run from the landed blob bytes extracted to a scratch dir outside the repo, deleted after use. This file is written by the closure judge and left UNCOMMITTED for the orchestrator to commit under the protocol identity.

## Verdict summary

**status ok, admitted.** All three claims verify on independent re-derivation; no owned axis is harmed (the axes table is byte-identical entering→final); the three r77 carry-ins (D77-1/D77-2/D77-3) are discharged with landed-bytes proofs. One status-neutral precision defect is routed (the C2 control-command citation in the report — see Routed defects).

## Step-1 conformance

| Check | Result | Evidence |
|---|---|---|
| Report committed by lane identity | PASS | `git log --format='%an %ae %H' -1 -- .ufo/reports/round-78/mori.md` → `mori-shokunin mori@shokunin.local 9bd2c952` (fleet repo), 2026-11-02 11:21:45 -0800 |
| Commit-before-report | PASS | lane commits 4ce9e438 17:57:27Z, 2360cc3b 19:11:31Z, 22dbaae4 19:17:32Z (= 09:57/11:11/11:17 -0800) all precede the 11:21:45 -0800 report commit; dispatch digest launch 09:35:20 -0800 / complete 11:21:45 -0800 brackets the work |
| `SHONEN` heading | PASS | report `## SHONEN` with one line per box, 4/4 `[~]` with resolvable pointers (asserted-by-author — correct form for a lane still holding SHONEN.md; only `[x]` requires a named non-author) |
| Cited lane commits exist + ancestor | PASS | `git merge-base --is-ancestor` rc 0 for 4ce9e438a287e51aa705b0426d8817999a0cdef9, 2360cc3b77a510c6a2a87bd8119c3a3d0291c4cf, 22dbaae4364425e59c9cbc07d9c83363a6b4426e vs refs/heads/master |
| Branch tip pushed | PASS | `git ls-remote origin refs/heads/master` = `22dbaae43644…` = local `refs/heads/master` |
| Round work reachable ecb916ce..22dbaae4 | PASS | linear chain ecb916ce → 4ce9e438 → 2360cc3b → 22dbaae4 (`rev-parse X^` verified) |
| Commit shapes as reported | PASS | 4ce9e438: diff-tree exactly one path `A tools/mori-counter-win.py`; 2360cc3b: 22 paths, numstat +2118/−7; 22dbaae4: 3 paths (post-landing receipt + lesson addendum + LOG addendum) |
| Write scope held | PASS | the 24-path entering→final diff contains no `.ufo/state/`, no watchdog.log, no sibling file, no registered instrument byte; all lane commits carry the lane identity |
| Not a marker report | PASS | real work, real measurements, checkable hashes throughout |

## Claim re-checks

Re-measured (commands run by this reviewer, not taken from receipts): C1 before/after tree state, blob sha, selftest, live run, capabilities counts, prefix identity. Evidence-verified (committed receipts read and cross-checked, gate not executed): the standing battery tally, the anchor-checker runs, the drift re-check runs, the fresh-start re-derivations.

### C1 — operability (capability acquisition, D77-1 + D77-2): VERIFIED

Before (do-nothing controls re-derived):
- `git cat-file -e ecb916ce0105…:tools/mori-counter-win.py` → rc 128 ("exists on disk, but not in …"); `git ls-tree ecb916ce0105… tools/` lists 57 entries, none named `mori-counter-win.py`; `git log --all --oneline -- tools/mori-counter-win.py` → only 4ce9e438.

After:
- `git diff-tree -r --root 4ce9e438` → exactly one path, status `A` (new commit, not an amend; `git rev-parse 4ce9e438^` = ecb916ce, the r77 landing `6a230c4b` untouched and still ancestral).
- `git show 4ce9e438:tools/mori-counter-win.py | sha256sum` → `e6c527dbef07dbede0b963db1d68cbbbccdf0d148d0e9409b9a4514789ff7a1f` == the receipted r77 landing bytes.
- **Selftest re-run by this reviewer at the landed bytes** (blob `f81044c1` extracted to scratch, sha-verified, `python -I`): all 12 arms PASS, `COUNTER_WIN_SELFTEST: PASS (12 cases)` rc 0 — matches `counter-win-selftest-r78.txt` (which names the landing commit and blob sha).
- **One live run re-run by this reviewer at the landed bytes**: `COUNTER_WIN: AVAILABLE surfaces=4 ok=4 unavailable=0 samples=2` rc 0 — matches `counter-win-live-r78.txt` (second live session at a distance; separate counts, never a series). Stdout carries only counter paths/values/state words — the redaction rule held (counts and shapes only, no host-identifying material in the receipt).

D77-2 (capabilities row):
- `git show ecb916ce…:SCORECARD.md | wc -l` = 3937, sha256 `bd73125d1dd4…` — byte-identical prefix of the 2360cc3b SCORECARD (verified by hashing the first 3937-line prefix of the after bytes).
- `grep -c 'Capability | What it can now do'`: 26 → 27. Lead-cell anchored form `grep -cE '^\| Windows performance-counter one-shot probe'`: 0 → 1; the loose form `^\|.*mori-counter-win` reads 3 (the one capabilities row + two Round-78 claim-table mentions) — both forms receipted per the r77 lesson-3 rule, exactly as reported.
- The row carries what it can do, the evidence pointer, and first-working round 77 (the round that demonstrated the capability running; r78 both lands the instrument and re-demonstrates it — the labeling choice is defensible and the demonstration requirement is met for the entering round).

Grade: **operability improved.**

### C2 — calibration (D77-3, the correction of record): VERIFIED (with one routed precision defect)

Substance re-derived:
- `git show 6a230c4ba1234cb4dc4f282eb697548f1c3ff1ad --numstat --format= | wc -l` = **21**; `| grep -c mori-counter-win` = **0** — the r77 landing does not contain the tool, exactly as the correction of record states.
- Correction of record present: LOG Round 78 section (and the report) carry the D77-3 correction; `grep -c 'D77-3'` LOG entering→final = 0 → 5 (append-only).
- No r77 artifact edited: `git diff-tree -r --name-status ecb916ce0105… 22dbaae43644…` over the whole tree = **24 paths = 19 `A` + exactly 5 `M`** (LOG, SCORECARD, SHONEN, corpus/README, corpus/SOURCES — the round-carriers); zero paths under `.ufo/reports/round-77/` or `.ufo/waves/round-77/`; zero deletions. This independently reproduces the frozen-set audit's shape claim at the committed level: `frozen-audit-r78.txt` reads paths=14,274 (`git ls-tree -r ecb916ce… --name-only | wc -l` reproduces 14,274), byte-identical 14,269, round-carriers 5, mismatches 0, missing 0.
- LOG append-only: entering 4695 lines sha `d32bc0e4f46c…`; the final LOG's first 4695 lines hash to the same sha (verified by prefix hashing).
- Lesson addendum append-only: `git show 2360cc3b:corpus/lessons/round-78.md | sha256sum` = `2fd194f95779…` == the sha proven inside the addendum; the final lesson's landing-bytes prefix hashes identically.

Defect (status-neutral): the report's C2 bullet cites the do-nothing control as `git show ecb916ce:LOG.md | grep -c 'correction of record'` = 0. That phrase actually reads **6** at entering (prior corrections-of-record use the same words). The 0 belongs to a D77-3-specific marker — `grep -c 'D77-3'` and `grep -c '22 items'` both read 0 at entering and ≥1 at final — but the committed control receipt (`controls-r78.txt` line `correction_marker_in_LOG_at_entering=0`) names no command, so the report's spelled-out command is the only reading a fresh reviewer has, and it is false. The control's substance (the correction text absent at entering) holds under the D77-3-specific markers. See Routed defects.

Grade: **calibration improved** (the correction is honest, append-only, and lands the r77 closure's own routed defect; the defect above is a citation-precision slip in the new round's report, not a calibration failure of the correction).

### C3 — freshness (sourced, S593): VERIFIED

- SOURCES: rows `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'` 365 → 366; badNF (awk NF!=13) = 0 over 366; S593 at line 374 immediately after S592 (:373); the only in-place row edits are three pure used-by-cell appends of `, corpus/knowledge/counter-semantics-r78.md` (cell-level diff of S572/S574/S592 shows a single insert each; old→new logged in `source-s593-r78.txt`) — the SOURCES append-only rule permits used-by changes.
- Pin: `git show 2360cc3b:corpus/evidence/sources-r78/S593.html | sha256sum` = `7eb834fc1450f8f93d94e11cd66c4c7a84049631ca1b1032ffbb3019ff6a9bac`, 48,532 bytes — matches the row, the lesson, and the receipts.
- **Re-opened live by this reviewer**: `curl` of the row's percent-encoded URL → HTTP 200, 48,532 bytes, sha256 `7eb834fc…` == the pin. The byte-identity of the re-point is independently reproduced.
- Quotes: all five located quotes verified at the pinned lines (713/720/730/750/756) with the recorded word counts 18/19/6/2/2; the :720 span's "ends at 'the'" truncation note is accurate (the sentence continues through linked structure names on the same line). Anchor receipt: PASS items=5 + able-to-fail mislocation arm FAIL rc 1 (`s593-anchor-check-r78.txt`).
- Pin-family arm: first run rows=7 with S593 `unavailable` **disclosed beside** the final run (`pin-family-r78.txt` + `-s593-isolated.txt` + `-final.txt`); final run `rows=7 adjudicated=7 fresh=2 time-churn=1 asset-churn=1 ua-serving=3 unavailable=0` rc 0, window 18:40:57Z..18:40:58Z.
- parse_registry paren-truncation routing: cause chain receipted (isolated re-run reproduces `unavailable`; `mod.fetch` on the true URL body 5/5 — the 48,909-byte per-UA variant vs the 48,532-byte curl variant == the pin, the learn.microsoft.com serving-variance shape); **the registered instruments were not edited** — blob shas of `tools/mori-drift-recheck.py` (6e46ca38) and `tools/mori-source-drift.py` (1c6b437f) are identical entering→final; the mori | round-65 instrument-change L0 stays open and was routed around, never treated as answered (L0 file re-checked: the round-62/65/73 lines are the last mori lines, no answers after them). The row-side accommodation stays lane-owned data with the RFC-equivalent encoding, cmp-proven byte-identical before landing.
- Knowledge entry `corpus/knowledge/counter-semantics-r78.md` opens with the provenance trio (source: S593 + pin sha; verified-at; recheck) and names the Pages/sec absence; README index 858 → 859 with the entering 858 lines byte-identical.
- Census: `sources-census.sh validate … mori` re-run by this reviewer at closure → **rc 0**, the tolerated 35-row W04 duplicate-URL class + 1 ok row, matching both round receipts (start 17:53:14Z, end 19:00:04Z, both exit=0). One disclosed quirk: the census-end receipt names the fleet-root synced copy's tip as 4ce9e438 (commit B not yet synced at 19:00:04Z) — the receipt itself discloses this; the closure-time census over the landed state is the deciding check and passes.

Grade: **freshness improved.**

## Unauthored receipt files (stopped parallel attempt) — disclosure complete, disposition defensible

The three r76 foreign receipt files (`s591-source-r76.txt`, `source-s591-sweep-r76.txt`, `win-family-live-r76.txt` under `.ufo/waves/round-76/evidence/`) were re-verified:
- Disk: present (disk-only). Committed: `git cat-file -e 22dbaae4…:<path>` rc ≠ 0 for all three; the entering→final diff adds no round-76 path.
- Cited: every committed mention (`foreign-sweep-r78.txt`, LOG, the round lesson) is disclosure/ruling-class naming the standing leave-for-operator disposition; no r78 claim rests on their content.
- Disclosure is complete (sweep receipt + report bullet + SHONEN line + lesson section, all consistent), and the disposition is **defensible**: the files are unauthored artifacts of a stopped parallel attempt; committing or absorbing them would attribute foreign work and breach the detection-and-report boundary, while deleting them would destroy the operator's evidence. Leaving disposition to the operator is the only ruling consistent with the lane's write scope.

## Discernment spot-check (checked from outside)

| Item | Decision | Re-opened source | Agree/disagree | Reason |
|---|---|---|---|---|
| S593 admit (tier A, counter-name association scope) | admit | Live refetch of the row URL (byte-identical to pin, 48,532 bytes); five quotes verified at pinned lines with recorded word counts; `source-s593-r78.txt` sweep-before-fetch with four 404 candidates; title check; anchor PASS 5 + able-to-fail FAIL rc 1 | **agree** | The row's quotes are located, ≤25 words, truthful to the live source; tier A is right for vendor documentation of the exact scope; the sweep and able-to-fail arms make the admit falsifiable |
| Four 404 candidates → no registry rows ("rejected: none — fetch failures, not registry candidates") | reject-shaped (no rows) | `source-s593-r78.txt` section 2 (candidate URLs, 404 titles, one 17,593-byte error page) | **agree** | Error pages are not sources; writing rejection rows for them would pad the registry with non-opened "sources" — the contract's row-is-a-claim rule says write rows only after opening a real source |
| No supersedes row manufactured for S593's first-admission `ua-serving` | reject-shaped (no registry edit) | QUALITY criterion 159 (vendor-scoped churn grammar; per-response bot-manager chrome is serving variance, not content) + the immutable pin + anchor receipts | **agree** | The standing grammar adjudicates the class; pins are immutable and anchors hold; a hand-made supersedes row would be a registry correction manufactured against the lane's own standing rule |
| parse_registry finding → row-side re-point, not an instrument edit | reject-shaped (refused instrument edit) | Blob identity of `mori-drift-recheck.py`/`mori-source-drift.py` entering→final; the open mori \| round-65 L0 line (re-read at `.ufo/l0-questions.md:242`); the cmp-proven byte-identity (reproduced by this reviewer's curl) | **agree** | The instrument is registered and tally-pinned with an open operator ruling on instrument changes; routing around through lane-owned data with byte-identity proof is the correct move, and the finding is disclosed instead of overwritten |
| New SOURCES row quote check (contract rule 1 sample) | admit | Same as row 1 — the row's five ≤25-word located quotes re-verified against the pinned (and live-identical) bytes | **agree** | Verified mechanically, not by trusting the receipt |

The Gate section records the admit with full Gate record and names the rejects honestly (none — with the 404s' classification explained). Spot-check sampling requirement (≥1 admit, ≥1 reject-shaped) satisfied; all sampled decisions **agree**.

## Per-axis verdicts

| Axis | Verdict | Basis |
|---|---|---|
| operability | improved | C1 verified: a registered instrument that existed only on disk now runs from committed bytes (selftest 12/12 + live AVAILABLE re-executed by this reviewer at the landed blob); the SKILL registry row 12's command resolves from committed bytes |
| calibration | improved | C2 verified: the r77 closure's false-landing wording is corrected append-only with the 21-path/0-mention re-derivation true on re-measurement; the axes table byte-identical (no scalar moved); one citation-precision defect routed, status-neutral |
| freshness | improved | C3 verified: S593 opened with the full Gate and pinned; the standing family arm extended to rows=7 rc 0 with the first-run `unavailable` disclosed; the drift instrument's blind spot was caught by the round and routed around byte-identically |
| coverage | unchanged | No new surface claimed; S593 deepens an already-held surface's citation base; PROVINCE.md byte-unchanged |
| depth | unchanged | The knowledge entry claims no new depth axis-move; the axes table byte-identical entering→final (verified: 0 deleted lines in the SCORECARD diff, axis rows identical) |
| adjacency | unchanged | Detection-and-report boundary held; the three foreign receipts disclosed, not absorbed; no sibling surface touched |

No axis is harmed. Lowest-non-retired-axis rule satisfied: depth/freshness/calibration are tied at the 5 floor and C2 (calibration) and C3 (freshness) both work it.

## Trend verdicts

- **expansion: improved** — one new admitted ground (S593) with a `mined` row, machine-verified anchors and an able-to-fail arm; SOURCES 365 → 366 with badNF=0; the capabilities register grew 26 → 27 to match the demonstrated state; census rc 0 at closure. Evidence re-derived above. Agrees with the report.
- **quality: improved** — the r77 recovery landed with landed-bytes proofs at every layer (blob sha, receipts naming the landing commit, post-landing ls-tree IN-checks, 22/22 verified by this reviewer against commit B's tree); the frozen set is intact (0 mismatches re-derived at tree level); six mistakes mined with class/captured-by/fix including the post-landing addendum with its prefix sha proven; no admitted entry failed its re-check (pin-family rc 0, all adjudicated). Agrees with the report.
- **discernment: improved** — five defects caught and corrected before landing plus one immediately after, each mined with class/evidence/captured-by/fix; the registered instrument was left unedited under an open L0 with a byte-identical route around; the first family run's `unavailable` is disclosed beside the final run rather than overwritten; the axes table byte-identical. This closure's spot-checks agree with all sampled decisions. Agrees with the report.

## Routed defects the lane must fix next round

1. **D78-1 (status-neutral, number-drift/precision class): the report's C2 control-command citation is mis-stated.** The bullet `git show ecb916ce:LOG.md | grep -c 'correction of record'` = 0 is false — that phrase reads 6 at entering (prior corrections-of-record share the words). The 0 belongs to a D77-3-specific marker (`grep -c 'D77-3'` reads 0 → 5 entering→final). The committed control receipt (`controls-r78.txt`) names no command for `correction_marker_in_LOG_at_entering=0`. Fix: append a precision correction of record naming the exact marker that reads 0 at entering; standing — a control receipt states the counting command beside the count, and the report cites the same command the receipt ran.
2. **D78-2 (status-neutral, disclosure-precision class): the census-end receipt's context line names the fleet-root synced copy's tip as 4ce9e438** (commit B not yet synced at the 19:00:04Z run). The receipt discloses this inline; no action needed on the landing, but next rounds should state which tree the census validated when the round's landing commit postdates the census run (or re-run the census after the landing commit).
3. **Carried (not new): the three open mori L0 lines (round-62, round-65, round-73) remain present and unanswered** — re-verified by this reviewer at `.ufo/l0-questions.md` (the round-73 line is the file's last mori line). They were routed around correctly this round; they stay on the operator's queue.

## Notes for the operator

- SHONEN.md is still fully self-attested (4/4 `[~]`). Per protocol only a non-author may write `[x]`; nothing in this round's report is uncheckable by a non-author — a promotion review can check all four boxes from the cited evidence if the operator chooses to run one.
- The three r76 foreign receipt files remain disk-only, uncommitted, uncited — operator disposition still pending (the lane's leave-for-operator ruling is correct and now re-verified three rounds running).
- The round is honest under stress: it is the recovery from a rejected-honest-stop closure and the work landed exactly the way the r77 spotcheck prescribed (new commit, byte-identity proof, receipts at the landed bytes, frozen history untouched).

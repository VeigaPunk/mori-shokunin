# ReviewLesson — round-16 review of the round-15 routed queue and append-only correction rationale

Seat: `MoriR16.ReviewLesson` (reviewer, leaf). Read-only except this report.
Lane root: `/home/vgpnk/Projects/shokunin/mori-shokunin`.

## Read-time state (explicit)

- Read window: 2026-10-20 ~08:47Z to ~08:52Z. Changes were **in flight** throughout; findings are per read time.
- HEAD at read: `b83edc6ee3db6822382ab673d7e6e984e420f22f` (round-15 spot-check commit).
- Working tree at 08:47Z: modified `LOG.md`, `PROVINCE.md`, `SCORECARD.md`, `corpus/SOURCES.md`; untracked `.ufo/waves/round-16/`.
- Working tree at 08:51–08:52Z additionally: modified `SKILL.md`, `corpus/QUALITY.md`, `corpus/README.md`; untracked `corpus/lessons/round-16.md`, `corpus/knowledge/journal-cursor-window-r16.md`. `SKILL.md:168` (r15 row) was corrected in the working tree **after** my first read; HEAD still has the stale text.
- Not read in full or not verified by me: `corpus/lessons/round-16.md` beyond lines 1–60, 80–100, 111–116; `corpus/knowledge/journal-cursor-window-r16.md`; the background lesson output (`.ufo/waves/round-16/build/Lesson.md`, delivered mid-review by another seat). I did not act on the background-job notice; it is not my job.

## Method and disclosures

- Static reads only: `git show`/`git log`/`git status`/`git diff`, `grep`, `sed`, `jq` on committed or working-tree JSON. No `mori-census.sh`, regression gate, selftest, build, journalctl query, or fixture run.
- One outside-lane write, disclosed per L1's instruction: at ~08:49Z I ran `git show … > /tmp/__none` as a probe of the fleet-repo report. It produced no content and I removed the file immediately (`rm -f /tmp/__none`, verified absent). Nothing from it is used as evidence. This is a `/tmp` write and is disclosed to `MoriR16.Lesson`.
- No live journal reads, no probes, no background jobs by this seat.

## Routed queue disposition (the five items in `corpus/lessons/round-15-verifier-spotcheck.md`, "Open queue", lines ~258–288)

Status key: HEAD = committed; WT = working tree at read time.

| # | Routed item | HEAD (b83edc6) | WT at read time | Verdict |
|---|---|---|---|---|
| 1 | M4 correction: wave-context omission; assign to L1; carry exact-id/no-broadcast into future contexts | No correction in `corpus/lessons/round-15.md` (M4 row unchanged). Spec/dispatch have 0 `agent://` tokens (verified). | `corpus/lessons/round-16.md` C15-1 appended (untracked). Round-16 `wave1-spec.json` context carries "Never agent://all; message ONLY exact seat id…" (verified, 2 occurrences). | Addressed in WT as append-only. Carry-forward is static text only; the tested-prevention claim is correctly not made. |
| 2 | M5 correction: `/tmp` write beyond downloads (HarnessBuild) | No correction. `HarnessBuild.md:256` `--pin-fixtures /tmp/mori-r15-expected-probe-final.json` verified present. | C15-2 appended. | Addressed in WT. Citation lines verified. |
| 3 | M6 correction: implementation of selftest arms ≠ permission to execute; cited "historical report:301–307" | No correction. The cited text is `.ufo/waves/round-15/build/HarnessBuild.md:298–307` (honesty note). The fleet report `.ufo/reports/round-15/mori.md` has only 149 lines at `1ccac09`, so 301–307 cannot refer to it. Dispatch text "No execution." verified at `.ufo/waves/round-15/dispatch.json:687`. | C15-3 appended and resolves the locus to HarnessBuild.md:301–307 (this is the same honesty block I located). | Addressed in WT. The locus ambiguity in the spot-check is real and is resolved only by the WT lesson. |
| 4 | Active registry fix at `SKILL.md:134` (stale `--selftest-child` / `--no-frozen-control`) | **Stale at HEAD** (verified: line 134 still says "requires the hidden `--selftest-child`"). Delivered CLI has no such argparse flags (verified: `add_argument` list at `tools/mori-round15-regressions.py:2310–2319`); `evidence/control-bypass-refused.json` records the refusal. The stale text was authored in round 15 by the SkillInterface seat (`.ufo/waves/round-15/build/SkillInterface.md:88`), contradicting `HarnessBuild.md:18` F2. | WT **corrected** (SKILL.md r15 row now says the CLI has no hidden flags); C15-4 in `round-16.md` still records the fix state as **OPEN**. | Fix is in WT, uncommitted. The lesson text lags the working tree and must be reconciled before commit (see Finding F1). |
| 5 | Drift pin carried; no re-pin | Baseline `corpus/evidence/baseline-r10-20261015T2231Z.json` last changed by `5be8943` only (verified). `.ufo/waves/round-15/evidence/drift-current.json` `"exit": 1` (verified). | Unchanged in WT. C15-5 carried as debt. | Satisfied. No re-pin. |

Round-15 M1–M3 cross-check (the original r14 six-item queue): M1 (dirty-path scope) is provenance-only and correctly "retained" in r15; M2 (`journal-alarm-routing-r14.md:221` wording) is superseded by the appended "Correction to r14 :221" in the new `corpus/knowledge/journal-positive-evidence-r15.md:32–34` (verified). The r14 note itself has no pointer back. Under append-only discipline this is acceptable; the r14 spot-check's in-place rewording suggestion was correctly not followed. M3a (legacy count `unavailable:`) is documented in the r15 note at line ~226 (verified); the r14 note at `:383–384` still lacks it (0 `unavailable:` matches at HEAD). M3b (SCORECARD vectors labelled "fixture") is **not** done; see F2.

## Findings

Severity: H = blocks admission of a claim; M = wrong or dangling record that a reader would rely on; L = wording or path hygiene.

**F1 (M) — lesson/registry state drift in flight.** `corpus/lessons/round-16.md` C15-4 and "Routed items" (line ~113) say the `SKILL.md:134` fix is OPEN and owned by `mori` in its next commit. At 08:52Z the WT `SKILL.md` already contains the corrected text. Either the lesson must be updated to "fixed in WT, pending commit", or the SKILL edit must be attributed in the lesson. Otherwise the append-only record reports a state the tree no longer has. Also: the corrected SKILL text claims `--selftest` "refuses `--output` and `--pin-fixtures` with rc2". I confirmed only the code message `GATE ERROR exit=2 (--selftest takes no run/pin flags)` at `tools/mori-round15-regressions.py:2327`; I did not execute it, so this is a static consistency check, not a behavioral one.

**F2 (M) — SCORECARD round-14 nonzero vectors remain unlabeled; cited correction does not exist.** `SCORECARD.md:781` still reports user `3/0/2/1/2/1` and system `2/1/4/3/0/2` with no fixture qualifier. `grep -i nonzero SCORECARD.md` returns nothing at HEAD or WT. Yet:
- `corpus/lessons/round-15.md:20–25` M3 row says "SCORECARD nonzero vectors are explicitly fixture observations in this round's correction";
- `corpus/QUALITY.md:91` (#36) cites "SCORECARD round-14 vector correction" as its source, and its quote "are **fixture vectors**" is attributed to `lessons/round-15.md:23-25`, not to SCORECARD.
The qualifier lives only in the lesson and QUALITY. The round-14 routed item 3b ("label SCORECARD nonzero vectors 'fixture'") is therefore still open, and QUALITY #36's citation dangles. Fix: append a SCORECARD correction entry (do not rewrite line 781) and correct the M3/QUALITY citation to point at it.

**F3 (L) — citation path ambiguity for the fleet report.** The round-15 spot-check and the WT lesson cite `.ufo/reports/round-15/mori.md` (C15-5 cites `:146`). That file is in the **fleet** repo (`/home/vgpnk/Projects/shokunin`, commit `1ccac09`), not in `mori-shokunin`; `git cat-file -t 1ccac09…` fails inside the lane repo. The committed file has 149 lines. I did not verify that line 146 contains the phrase "status-neutral debt" (I saw line 145 and the bullets around 146 only). Recommend the lesson name the repo explicitly (e.g. `fleet:.ufo/reports/round-15/mori.md`) and quote the phrase it relies on.

**F4 (L) — known-wrong numeric source anchors, disclosed in an append.** `corpus/SOURCES.md` (WT, appended "Correction (append-only, 2026-10-20, Registry seat)") states the round-15 S014/S015 pinned line numbers (e.g. `--after-cursor=` at 187–190) do not reproduce on the rendered page (near line 193). Immutable anchor cells were left unedited. This is appropriately append-only. I did not re-open the sources; the claim is the seat's and is unverified by me. Carry as a source-numbering debt until a registry pass.

**F5 (L) — living-document rewrites without a LOG line.** `PROVINCE.md` (Owns line and FR11 title/boundary) and `corpus/README.md` (FR11 row) were rewritten in place in WT. The FR11 title changed from "New-since-pin journal kill counts via cursors" to "Remaining new-since-anchor journal semantics". These are living indices, not logs, so this is not an append-only violation by itself. But the round-16 LOG entry does not mention the retitling, so a reader of LOG cannot find why FR11's name changed. Recommend one LOG sentence citing the superseded title.

**F6 (L) — process hygiene, mine.** I made one `/tmp` write (`/tmp/__none`, empty) and removed it. Disclosed above and sent to `MoriR16.Lesson`.

## Verified-true claims (no action)

- Round-16 wave: 64 members, roles executor 20 / scribe 8 / scout 10 / connector 6 / reviewer 10 / critic 8 / sentinel 2 (verified from `wave1-spec.json` and `swarm-registry.json`, `members` length 64).
- Round-16 shared context carries exact-id messaging, no `agent://all`, no `/tmp` probes, and skip-verification language (verified).
- Drift baseline `corpus/evidence/baseline-r10-20261015T2231Z.json` unchanged since `5be8943` (verified).
- Round-15 lesson M4–M6 rows exist and their cited locations (`AttackProvenance.md:121`, `RegistryFrontier.md:63–65`, `HarnessBuild.md:256`) are accurate (verified).

## Residual risk and verification gaps

- Everything above is per read time (08:47–08:52Z) on an in-flight tree. HEAD and WT disagree on `SKILL.md`, `QUALITY.md`, `README.md`, `LOG.md`, `SCORECARD.md`, `SOURCES.md`, `PROVINCE.md`; L1 should re-run this review's static checks against the final commit.
- No gate, selftest, census, or journal behavior was measured. The SKILL claims about the r15 and r16 tools are static consistency checks only; `tools/mori-journal-window.py`, `tools/mori-round16-regressions.py`, and `tools/mori-round16-context-check.py` did not exist at read time, so their registry rows cannot be verified here.
- Checks for L1 (not run here): (a) `grep -n 'selftest-child\|no-frozen-control' SKILL.md tools/*.py` should show no active registry hit; (b) `grep -n -i nonzero SCORECARD.md` should show the fixture label after F2 is fixed; (c) `git diff HEAD -- corpus/lessons/round-16.md` vs C15-4 status must agree with the tree (F1).

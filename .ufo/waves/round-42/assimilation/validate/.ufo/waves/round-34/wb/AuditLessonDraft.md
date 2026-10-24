measured 2026-10-23T08:00:22Z

AuditLessonDraft — attempt-2 lesson draft `/fast/scratch/hyaku/mori-r34/a3-L1/drafts/corpus_lessons_round-34.md`, lines 1-13 (Gate preamble) and 51-87 (census, claims-and-verdicts, M1, M2). Lane tip at audit: `5216d78` (wave-B dispatch); judged-against committed bytes at `fd25213` and ancestors. Method: `git ls-tree`/`git show` at `fd25213`, `fdf4371f`, `b9fb029e`, `f10a320d`, `8d56809`, `ba525e1a`; sha256sum of committed `.src` copies; direct reads of `count-c1-a1.py` and on-disk (untracked) wave-A reports.

## Per-statement verdicts

Lines 1-13 (Gate preamble):

- VERDICT: agree — `:1` attempt-1 L1 MoriR34 died with the orchestrator at 05:25:25Z. Corroborated only by untracked `.ufo/waves/round-34/wb/ScoutAccounting.md:13` quoting `watchdog.log:847`; no committed receipt carries that time. Resolvable-but-untracked.
- VERDICT: agree — `:7` eight sources admitted, all tier A, status `mined`, opened 2026-10-23. Committed SOURCES rows S191-S198 at `fd25213` all carry `code | A | … | mined | 2026-10-23` (`git show fd25213:corpus/SOURCES.md`).
- VERDICT: disagree — `:7-8` "attempt-1 wave-1 Src* seats fetched them" and that attempt 1 left copies/draft rows uncommitted. `w1/` is empty on disk and nothing committed names Src* fetch seats; unresolvable, rests on dead orchestrator history only.
- VERDICT: agree — `:9` sha256 of re-fetched URLs equals the committed copy for all eight. Verified: `git show fd25213:corpus/evidence/sources-r34/S19{1..8}.src | sha256sum` equals each table value on `:16-23` exactly. The exact second `05:32:35Z` is committed only as "re-fetched 05:32Z" (commit message `8d56809`); seconds are unverified.
- VERDICT: disagree — `:9-11` "a fresh wave-A reviewer per row re-opened it live … each `VERDICT: admit`" citing `.ufo/waves/round-34/wa/ReopenS191.md` … `ReopenS198.md`. Every file under `wa/` is absent from the committed tree at `fd25213` (`git ls-tree fd25213 .ufo/waves/round-34/` shows only `c0/ contract.md count-c1*.py evidence/ wa-*.json`) — untracked attempt-2 output; must be re-derived this attempt. On-disk leads do show `VERDICT: admit` in all 8 (ReopenS197.md carries an extra boilerplate VERDICT line).
- VERDICT: agree — `:11-12` quotes re-located in committed copies `corpus/evidence/sources-r34/S###.src`; those copies are committed (hashes above). Script `/fast/scratch/hyaku/mori-r34/l1-a2/gate.py` exists on disk (scratch path; quote correctness itself is GateS196's lane, not re-verified here).

Lines 51-87:

- VERDICT: agree — `:51` SOURCES rows 190 → 198 by `grep -c '^| S[0-9]'`: 190 at `f10a320d`, 198 at `fd25213` and worktree.
- VERDICT: agree — `:52` `evidence/census-start.txt` is committed at `fd25213` (blob `57ec17be`); content shows `mori ok`, `EXIT=0`, exactly 12 W04 lines, measured 04:51:02Z at `f10a320d`.
- VERDICT: disagree — `:52` `evidence/census-end.txt` cited as `evidence/`: it is NOT in the committed evidence tree at `fd25213` (tree `9475fdd2` holds only c1-before/c1-controls/c1-posctl/c1-tool-provenance/census-start). Untracked attempt-2 output; must be re-derived. On-disk content does match the draft's claim (measured 06:10:51Z, `mori ok`, `EXIT=0`, 12 W04 lines).
- VERDICT: agree — `:57` `evidence/c1-after.txt` content: `C1=met` at `ba525e1a`, measured 05:30:42Z, exit 0 — file on disk matches. Caveat: it too is untracked (not in tree `9475fdd2`); re-derive.
- VERDICT: disagree — `:57-58` "15 further seat runs (ExecRerunLane 9/9, ExecRerunClone 3 + extras, CritResidualA 4)". Two defects. (a) Arithmetic: 9+3+4=16 ≠ 15. (b) The components understate their own cited (untracked) reports: `wa/ExecRerunLane.md:16-17,105` reports 11 met runs total at the tip (8 fresh-seed + seed 1 + `ba525e1a` + `fd25213`), `wa/ExecRerunClone.md:15,85-115` ≥7 met runs, `wa/CritResidualA.md:91-92` exactly 4. All three reports are untracked; re-derive, but the draft's own sources contradict "15".
- VERDICT: agree — `:59-62` CritPostDataShortcut probe shape: committed-ish receipt `.ufo/waves/round-34/evidence/ctl-postdata-shortcut/receipt.txt` (untracked; on-disk) states one real read + rate 0, two reads only on the FIFO arm, class from name patterns; rev `ef936fb4e0834d0a1ce676aef735debe2eef9d27` and L1 re-score 05:49:11Z `C1=met` match. `ef936fb4` is not an object in the lane repo (`git cat-file` fails) — correctly labeled a sandbox rev; its tool bytes are vendored at `evidence/ctl-postdata-shortcut/mori-disk-rate.py` sha256 `cd5389b9…`. Cited evidence untracked; re-derive.
- VERDICT: agree — `:62-63` "the live arm bounds rates only from above": `count-c1-a1.py:277-278` rejects only `r * 300 > (s3-s0)*512*1000` (upper bound; zero accepted). "The generator lets a device name predict its class": `:150-166` draws disks from `DISKS`, partitions via `part_name`, stacked from `dm-{i}`/`md{127-i}`, virtual from `VIRT`, unknown `xyz9` — each class from its own name family. Both verified against committed counter bytes.
- VERDICT: agree — `:63-64` "counter was wrong; counter, rules and target are not amended" — consistent with frozen `contract.md` kill/addendum posture and receipt `receipt.txt` "not amended".
- VERDICT: disagree — `:65-66` C2 `unprovable-but-better` by non-author ReviewC2Judge at `.ufo/waves/round-34/wa/ReviewC2Judge.md`: file is untracked (wa/ absent at `fd25213`); must be re-derived. On-disk lead shows `VERDICT: unprovable-but-better` at `:88`.
- VERDICT: agree — `:66-67` QUALITY 98 "able to fail on round 33's contract" and "does not answer §8 item 1's second clause". Committed QUALITY 98 (`fd25213:corpus/QUALITY.md:714-727`) contains no reader-action requirement; `round-33-verifier-spotcheck.md:227-228` names "each verdict cell to name a reader action, checked by something other than the header label" as part of item 1.
- VERDICT: agree — `:68-69` MutQ98 survivor: on-disk untracked `wa/MutQ98.md:40-48` shows the (a)-(c) check passes a table whose three no-decision cells name the already-scored `C-absent` control while full-98 prose rejects it — draft's "prose forbids it, the check does not" is accurate modulo "cells" not "rows". Untracked; re-derive.
- VERDICT: disagree — `:70` "(M2, QUALITY 99)": QUALITY 99 exists only in the uncommitted integration draft (`drafts/corpus_QUALITY.md:735-746`); absent from committed `corpus/QUALITY.md` at `fd25213`. Naming it as landed evidence is premature; must be re-derived/landed this attempt.

M1 (`:74-78`) — all five fields present:

- VERDICT: agree — class "pre-data control gap (counter discrimination)": matches spotcheck §3.2.4 "none of the nine pre-data controls was a no-decision control" (`round-33-verifier-spotcheck.md:128-129`).
- VERDICT: agree — evidence `round-33-verifier-spotcheck.md` §3.2 items 2 and 4, "CtlGlossaryA1 met P-C1-A1 after data": spotcheck is committed at `fd25213`; §3.2 (`:103-136`) states the control ran under round 33's `count-c1-a1.py`, printed `C1=met` exit 0, and ruling items 2 ("skips exactly the claimed work") and 4 (pre-data gap) hold — the draft's predicate name "P-C1-A1" is correct for round 33.
- VERDICT: agree — captured-by "none before round 34": consistent with §3.2.4.
- VERDICT: agree — fix QUALITY 98 committed at `fd25213` (`:714-727`).
- VERDICT: agree — shown able to fail: committed QUALITY 98 check (a) itself declares it fails on round 33's contract at `fdf4371f` (that contract's controls, `:66-71`, name no no-decision control — verified; `fdf4371f` resolves to the round-33 A1 commit). ReviewC2Judge/MutQ98 re-application is untracked; re-derive.

M2 (`:79-87`) — all five fields present:

- VERDICT: agree — class "counter discrimination (shortcut not built before data)": accurate.
- VERDICT: disagree — evidence `evidence/ctl-postdata-shortcut/receipt.txt` and `wa/CritPostDataShortcut.md`: both untracked; must be re-derived. The `count-c1-a1.py:150-166` and `:277-278` citations are verified correct (see above).
- VERDICT: agree — captured-by: contract table at `b9fb029e` (verified: the Pre-data controls table has C-labelkey keyed "on the 12 fixed-seed scenarios … keyed on input bytes" only, no harness-keyed control, no live-arm lower bound) so 98's checks pass that table — "none caught it" holds.
- VERDICT: agree — fix QUALITY 99 text in the draft (`drafts/corpus_QUALITY.md:735-746`) matches the draft's summary (label-keyed over generator-emitted names; harness-keyed on FIFO/namespace/tmpfs/interval/seed; bound in both directions per named arm). But it is uncommitted — re-derive/land.
- VERDICT: agree — shown able to fail: 99's own text states it fails on the `b9fb029e` table; verified mechanically — that table names no harness-keyed control, so 99's check fails; probe `ef936fb4` is indeed the control 99 demands (receipt confirms the harness-keyed + label-keyed behavior). Resolvable once evidence is re-derived.

## Structural check (M1, M2)

Both carry class · evidence · captured-by · fix · shown-able-to-fail, and each fix is shown able to fail (98 on `fdf4371f`; 99 on `b9fb029e` via committed table contents). No missing field.

## Findings (severity)

1. High — pervasive citation of untracked attempt-2 evidence: `wa/ReopenS191-198.md`, `wa/ReviewC2Judge.md`, `wa/MutQ98.md`, `wa/CritPostDataShortcut.md`, `wa/ExecRerunLane.md`, `wa/ExecRerunClone.md`, `wa/CritResidualA.md`, `wa/ScribeMistakeM1.md`, `evidence/c1-after.txt`, `evidence/census-end.txt`, `evidence/ctl-postdata-shortcut/`. None is in the committed tree at `fd25213`; every statement resting on them must be re-derived this attempt (the wave-B seats cover most).
2. Medium — `:57-58` "15 further seat runs" is wrong arithmetic on its own terms (9+3+4=16) and understates the cited reports (Lane 11, Clone ≥7, ResidualA 4 → ≥22 by the reports' own counts).
3. Medium — `:70` and M2 fix name "QUALITY 99", which is uncommitted draft text; the lesson must not present it as landed until re-derived.
4. Low — `:7-8` attempt-1 Src* fetch claim unresolvable from any committed artifact (w1/ empty).
5. Low — committed QUALITY 98 cites `corpus/lessons/round-34.md`, which does not exist at `fd25213`; the draft is the file that will satisfy it (forward reference, consistent, but worth a note for the integrator).

## Residual risk / gaps

- Did not re-verify the Gate quote strings on `:16-23` against `.src` bytes (out of scope; GateS196 covers quote location).
- Exact-second fetch time 05:32:35Z and the death time 05:25:25Z rest on uncommitted records only.
- All wave-A report contents checked as leads; nothing cited from them counts as re-derived evidence yet.

No tool installs or updates performed; no git/jj writes issued in the lane (read-only git only).

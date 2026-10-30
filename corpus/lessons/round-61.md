# Round 61 — mori (L1 MoriR61a2, attempt 2, recovery of MoriR61a2 attempt 1)

author: mori L1 (MoriR61a2)
round: 61
date: 2026-10-30
freeze: `7370a731abcafc4c803111de7c22cd6264d63be1`
entering: `325f7e639916fcbc77fa2ec7475951a1b86bb1cb`

Attempt 1 (MoriR61) froze the contract, counters, controls, selftests and the six v7.3
source copies (freeze `7370a731`), built and dispatched wave w1 (64 seats, v2 policy), and
died to provider 429 before WAVE-DONE. Attempt 2 inherited the frozen bytes and the running
wave unchanged (parent handoff): pins re-verified before reuse (`PIN_C1`/`PIN_C2` equal the
committed `count-c1.py`/`count-c2.py` sha256s; r60 pin `fabde06c…` equals
`ac496c7c:.ufo/waves/round-60/count-c3.py`), no counter or contract edited, no wave
re-dispatched. Fresh-start duty (r57–r59 rejected closures read first, do-nothing controls
before data) was discharged by attempt 1 and re-verified here: the three committed control
receipts read unmet at the entering rev with the stated reasons
(`evidence/control-c{1,2,3}-do-nothing.txt`).

## Gate

C2 is the round's sourced claim; the six rows below were opened this round (fetched at tag
v7.3 from git.kernel.org plain URLs; fetch receipt `w1/Mo61ExecFetch.md`, seat + L1 re-fetch
2026-10-30, all six byte-match the pinned copies). Registry rows S565–S570.

- S565 `psi.rst` v7.3 — https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/Documentation/accounting/psi.rst?h=v7.3 —
  opened 2026-10-30 — quote (psi.rst:63): "in us) is tracked and exported as well, to allow
  detection of latency" (13 words). Byte-identical to v7.2.
- S566 `psi.c` v7.3 — https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/kernel/sched/psi.c?h=v7.3 —
  opened 2026-10-30 — quote (psi.c:101): "threads = min(4, 4)". v7.2→v7.3 delta is exactly
  one line (:1026 `if (delta < 0)` → `if (delta <= 0)`, +1 byte, no line shift); no r24
  anchor covers :1026.
- S567 `psi_types.h` v7.3 — https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/include/linux/psi_types.h?h=v7.3 —
  opened 2026-10-30 — quote (psi_types.h:13): "/* Tracked task states */". Byte-identical
  to v7.2.
- S568 `cgroup-v2.rst` v7.3 — https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/Documentation/admin-guide/cgroup-v2.rst?h=v7.3 —
  opened 2026-10-30 — quote (cgroup-v2.rst:1066): "cgroup.pressure". Both r24 anchors
  byte-identical in place despite growth elsewhere (+2615 bytes).
- S569 `init/Kconfig` v7.3 — https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/init/Kconfig?h=v7.3 —
  opened 2026-10-30 — quote (Kconfig:736): "If you say Y here, the kernel will create
  /proc/pressure/ with the". The two r24 Kconfig anchors moved +6 lines, byte-identical.
- S570 `kernel-parameters.txt` v7.3 — https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/Documentation/admin-guide/kernel-parameters.txt?h=v7.3 —
  opened 2026-10-30 — quote (kernel-parameters.txt:5540): "psi=		[KNL] Enable or disable
  pressure stall information". The r24 anchor moved +35 lines, byte-identical.

v7.2 diff baseline (working scratch, not committed; sha256: psi.rst `11c6b712…` (identical to
v7.3), psi.c `452318be…`, psi_types.h `483269b2…` (identical), cgroup-v2.rst `a9433bb0…`,
Kconfig `a43f09d8…`, kernel-parameters.txt `23b1a690…`; fetched 2026-10-30 from the same
plain URLs at `?h=v7.2`). Generator: `.ufo/waves/round-61/build-ledger-r61.py` (committed);
classification: same = span text byte-identical at the same v7.3 lines; moved = byte-identical
elsewhere (difflib-verified location); changed = span text differs.

Assimilation (merge/mori): adopt nothing this round. The id-collision guard found 94/136
staged ids colliding (S471–S564, contiguous): mass id drift → L0 question + no adoption
(lane-addendum `scripts/hyaku/lane-addendum.md` §6 item 10, lines 457–466 — the frozen
contract mis-cites this as "CORPUS.md §10"; Critic27 verified the ruling, count (94
recomputed byte-identically, locale-independent) and the 0–3-space pattern). Provenance gap
closed here: `merge/mori/SOURCES.append.md` sha256 `4f69b2df7644441174ab7db152dab3316be7e46cae666e308097afb3d7bfe1cc`,
`absent-defect-register.md` sha256 `5afe1810a6c3d62f37987b575a954f5b1197daa23005d4bb2f1d982f64bad833`
(read 2026-10-30). L0 line filed: `mori | round-61 | merge/mori mass id drift …`.

Quarantine slice (S244, S262, S268) re-derived by Mo61ExecQuarantine: S244 PRESENT via
DOI-matched arXiv record; verdicts maintained, no adoption (`w1/Mo61ExecQuarantine.md`).

considerthese: mined by Mo61ConnConsider — the latest residual proposal (sustain
round-qualified flag carryover) is already partially executed; no new implementable
proposal taken this round (assimilation/considerthese capacity went to the C2 recheck).

## Mistakes

1. class: instrument-overreach — the frozen C2 counter's quote floor (≥5 whitespace tokens,
   count-c2.py:137) exceeds the contract text ("≤25 words, ≥8 distinct bytes") and is
   unsatisfiable for 14 of the 47 honest `same` anchors whose spans hold no 5-word
   single line (short C lines: `psi.c:1268-1270`, `psi.c:1712`, `psi.c:1017`, `psi.c:1540`,
   `psi.c:1686`, `psi.c:1710-1721`, `psi.c:1268`, `psi.c:1269-1270`, `psi_types.h:41-49`,
   `psi.c:1717-1719`, `psi.c:1257-1258`, `psi.c:228-240`, `psi.c:1711-1719`,
   `psi.c:1596-1598`) — evidence: `w1/Mo61RevC2.md` F5 (pre-data fixture proof: honest-shape
   ledger cannot reach met; a stuffed line is required) and this round's generator
   constraint scan (identical 14). captured-by: none — the do-nothing controls exercise
   absence, not span-length distribution; the freeze-time selftests used synthetic 8-token
   lines. fix (ships next round as a NEW instrument; amendments barred this round): r62
   counter floors quotes at 1 word and/or reads multi-line hay, and a pre-data feasibility
   probe over the real pinned bytes is a freeze prerequisite; this round lands the honest
   unmet instead of reclassifying honest `same` rows to `changed` (the lie shape F5 names).
2. class: met-line fabrication (r60 defect-2 shape recurring) — the frozen contract's C2 met
   line names tokens the counter never prints (`rows_src=ok`, `provenance=ok`,
   `sources>=4`; actual fmt prints `sources=N`) — evidence: `w1/Mo61Critic25.md`; the
   pre-seat amendment fixed C3's tokens but not C2's. captured-by: the r60 lesson rule
   "every printed token is one measured boolean" was applied to one counter, not the
   contract set. fix: r62 freezes each claim's met line by grepping the counter's actual
   fmt output, not by hand.
3. class: semantic unbinding — C2's `status`/`loc` are never compared with the anchor
   (`w1/Mo61RevC2.md` F1: identity "moves", cross-file "changed" rows all pass), no v7.2
   bytes are pinned so `same/moved/changed` are unverifiable by the counter (F2), and the
   SOURCES arm is satisfied by one stuffed line (F3, `w1/Mo61Critic22.md` reached met with
   zero real recheck). captured-by: the r60 entry-claims-hardening criteria (H1–H5) were
   built for r59-class entries and not re-applied to this counter at freeze. fix: r62
   instrument pins v7.2 copies at rev, derives statuses from a difflib map, and binds
   rows to Registry ids (not substring scans).
4. class: receipt discipline — the committed freeze receipt `evidence/selftest-c2.txt` was
   produced with `--floor 1` (the default-floor selftest is red: `pointer_floor:6<40` on the
   6-pointer synthetic fixture), undisclosed — evidence: `w1/Mo61RevC2.md` F8. captured-by:
   QUALITY receipt rules require argv; attempt 1 omitted it. fix: every receipt line carries
   its exact argv (this round's `census-start-r61.txt` does; the r62 lesson must not inherit
   the omission).
5. class: misroot — this round's wave left `count-c1.cover`/`count-c2.cover` (coverage-run
   residue) at the FLEET root (reported by kaidoku R51; seat tools default cwd to the fleet
   root). captured-by: the wave context names absolute paths but never forbids relative
   coverage-output paths. fix: r62 wave contexts add "any coverage/profile output path must
   be absolute, under /home/vgpnk/Projects/shokunin/mori-shokunin"; the files are handled in
   this round's misroot sweep.
6. class: citation drift — the frozen contract cites the assimilation rule as "CORPUS.md §10"
   (that section does not exist; it is lane-addendum §6 item 10) and left the collision-scan
   inputs unsha-pinned — evidence: `w1/Mo61Critic27.md`. captured-by: none. fix: this lesson
   pins the input hashes (above); r62 contracts cite `scripts/hyaku/lane-addendum.md` §6
   item 10 by path.

## Wave

One v2 wave (`w1`, policy v2, band 64–128): 64 seats, all settled, 0 empty outputs;
`SETTLEMENT_SCAN_OK` shape per `w1/Mo61ExecReplay.md`/results JSON. Role mix: scribe 13,
executor 12, reviewer 9, mutation-tester 8, critic 7, scout 5, revenger 3, sentinel 3,
connector 2, simplifier 2 — attack share 30/64 = 46.9% (≥25%); connector seats present; L1
held the §3 planner seat (validator rejects planner; recorded per the frozen mapping rule).
One aborted seat: `Mo61ExecLedgerFix` (error: "Prerequisite is not yet available:
Mo61ExecLedgerDry-2 is still running"; its work — the corrected ledger — was performed by
the L1 instead: `build-ledger-r61.py` + this round's data commit). Godspeed directive bytes:
verified in all 64 payloads (`w1/Mo61ExecGodspeed.md`) — the r60 dispatch-payload defect is
closed. Determinism: C1 selftest ×3 and C2 selftest (--floor 1) ×3 byte-identical
(`w1/Mo61LabDeterminism.md`); `w1/Mo61ScoutFloor.md`: zero divergence across lanes'
independent counter runs at the freeze.

Attack-seat findings integrated into this lesson and the report: RevC1/Critic21/Critic24
(C1 met is reachable by omnibus/superseded/crafted rows — named limit; the landed table
holds one honest row per path), RevC2 F1–F8 + Critic22/25 + MutC2a/b/c (C2 shape-only met,
stuffable SOURCES arm, survivor mutants — routed to the r62 instrument list), MutC3a/b
(C3 kill table green on committed witnesses; EXPECT_PIN tautology named), Critic27
(assimilation ruling verified), Reviewer03/05/07/08 findings (frozen-manifest
selftest-floor and owner-cell observations — recorded, none actionable under freeze).

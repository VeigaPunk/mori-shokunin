# CritRound — mori round 96 w1, pre-data adversarial review of the frozen contract

Seat: CritRound (critic, leaf — no dispatch). Scope: contract `.ufo/waves/round-96/contract.md` and its four
evidence receipts, reviewed BEFORE data. No lane file edited except this report (written at both task-named
paths `w1/crit/CritRound.md` and `w1/CritRound.md` per the Report trailer). No tools installed.

## 0. Provenance checks (done, read-only)

- Lane HEAD is `b88c8ae8` "round-96: freeze contract, before receipts, wave-1 spec and dispatch" — the freeze
  commit, child of entering `66c5518e239eeacd6070be26d78085ef702392cb` (`git log -5`;
  `git merge-base --is-ancestor 66c5518e… HEAD` → ok). Entering-HEAD claim is consistent.
- `git diff --stat 66c5518e HEAD -- corpus tools SCORECARD.md LOG.md` is EMPTY → every working-tree
  recomputation below is an entering-revision recomputation. Untracked: `w1/`, `w1.ready.dispatched` only.
- `tools/mori-scorecard-calibration.py` does NOT exist at freeze (tools/ listing) — the C1 counter is the
  wave's deliverable, as the contract says.

## (a) Is C1 bookkeeping-only?

Operator rule: `/home/vgpnk/Projects/shokunin/.ufo/prompts/mori-round-96.md:146` — "…each round must leave
the lane measurably more capable … Bookkeeping-only rounds are thin claims."

C1's graded work product is five `Last change` cell edits in SCORECARD (syncing self-assessment to the fleet
record) — bookkeeping. The NEW counter `tools/mori-scorecard-calibration.py` (unbounded, red stale-cell
fixture, `COLUMNS_UNCHANGED`) is a new durable instrument that also fixes a live defect (the frozen r79
counter's `THROUGH = 78`, `.ufo/waves/round-79/count-c2.py:33`, hides rounds 79–95 — mined as mistake 1).
Classification: **cell edits with a counter** — not bookkeeping-only, IFF the counter is genuine and the
landing is independently checkable. The independent check exists: the frozen r79 counter at `--through 95`
re-derives the same five expectations from the fleet MANIFEST (shown in (c)). The contract does not yet force
that independence — see the forged-instrument hole in (b)/(e).

## (b) P1 / P2 as sentences; clauses satisfiable without the work

- P1 is one sentence and implementable, in the r79 docstring-receipt sharing pattern (count-c2.py:6-11).
  Clauses a seat satisfies without work: (i) "`Score` and `Evidence pointer` cells equal their bytes at
  `66c5518e…`" — a no-op guard, satisfied by inaction (fine as a guard); (ii) TRAP: the contract's counter
  command `python3 tools/mori-scorecard-calibration.py <rev> --manifest …` pins no bound. If the new counter
  ships a r79-style default bound (`THROUGH = 78`, count-c2.py:33) or any loose parser, the literal command
  prints `mismatches=0` on the UNEDITED scorecard → "met" with zero work. The do-nothing control does NOT
  catch this: it was scored with the FROZEN counter (receipt), not with the seat-authored one, and the
  contract requires only a synthetic stale fixture in `--selftest` (pattern at count-c2.py:155) — a
  strict-selftest/loose-parser counter passes every frozen clause. Fleet precedent for exactly this class:
  `corpus/lessons/round-91.md` `attack-found-forgers-in-frozen-predicates` ("C1 accepts 3 of 4 forgers").
- P2 is one sentence. Clause satisfied without work: "`prefix_only=31` (unchanged)" — inaction guard. The
  binding clauses `unpinned=0` + `ok=92` are jointly unsatisfiable — see (d).

## (c) Do-nothing controls recomputed by this seat (all at the entering revision)

- Frozen counter, `--through 95`, fleet MANIFEST (my run):
  `axis coverage cell=round_56_improved expect=round_80_improved state=mismatch` / operability r78 vs r93 /
  depth r76 vs r86 / freshness r78 vs r82 / calibration r78 vs r93 / adjacency r19 ok →
  `C2=unmet axes=6 mismatches=5 errors=0 rows=58 through=95 rev=66c5518e239e`, rc=1 — byte-identical to
  `evidence/before-c1-count-c2-through95.txt`.
- Same counter, default bound: `C2=met axes=6 mismatches=0 errors=0 rows=46 through=78 rev=66c5518e239e`,
  rc=0 — identical to `evidence/before-c1-count-c2-default.txt`. The default-bound "met" is exactly the trap
  named in (b).
- Expectations re-derived independently from `/home/vgpnk/Projects/shokunin/MANIFEST.json` (admitted mori
  rows ≥79 listed): ceilings coverage 80, operability 93, depth 86, freshness 82, calibration 93, adjacency
  19 — the contract's five expected landing cells ARE the MANIFEST derivation.
- Digest at the entering tree (my clean rerun):
  `DIGEST_CHECK rows=124 ok=86 mismatch=0 superseded=1 prefix_only=31 unpinned=6`, rc=1 — identical to
  `evidence/before-c2-digest.txt` (the receipt records no rc; rc=1 measured here; an earlier piped rerun
  lost the rc to `tail` — the clean rerun above is the cited one).

Answer: YES — both do-nothing controls are the entering revision and reproduce exactly.

## (d) Can unpinned go 6→0 without editing any row? NO — proof chain

Rules (all frozen, cited):
1. unpinned definition: a named pinned copy does not resolve to a file / "the pinned copy" unresolvable
   (`tools/mori-source-digest.py:40-41`); `combine()` returns "unpinned" whenever a copy is missing
   (`:247-249`).
2. Copy visibility: only (i) paths named in the row (`PATH_RE:84`, owner/repo prefixes rejected `:66,:83`),
   (ii) "same page bytes as S<n>" inheritance, (iii) "the pinned copy" phrase — searched ONLY when the row
   names no explicit path (`:322 if has_pinned_phrase and not all_refs`), inside `corpus/evidence/` only,
   unique best by recorded byte count then ≥8-hex prefix (`:352-354` else missing). A copy dropped into
   `corpus/evidence/` that the row never references is INVISIBLE to the tool.
3. Digest immutability: contract "A recorded digest is never edited or replaced"; CORPUS rule 2 (in-place
   changes limited to status/recheck/used-by; correction = appended supersedes row) —
   `corpus/QUALITY.md:2272-2277`.
4. Supersession gate: docstring `:26-28` — supersedes applies "if and only if S<id> classifies mismatch AND
   the row itself classifies ok"; code `:455-456` `if verdict_of.get(target) == "mismatch"`; selftest arm
   "prefix-only row is not superseded" shows non-mismatch targets are refused.

Per row:
- **S615** (`corpus/SOURCES.md:397`, recorded `7891c588…8f1a60ad1a6f0`, 362493 bytes): the recorded digest is
  PROVEN wrong by round-91 correction C-1 (`corpus/lessons/round-91.md:51-54`: the full sha256 of the pinned
  copy is `7891c588…0f83b9a8a42f5`). The lawful correction row already exists — S619 (`SOURCES.md:401`,
  teaches opens "supersedes S615 —", classifies ok) — but S615 classifies **unpinned**, not mismatch, so the
  gate at `:455` refuses: the receipt's `superseded=1` is S235 only. Placing a true-bytes 362493-byte copy
  under `corpus/evidence/` (S615's row has the "pinned copy" phrase and no explicit path, so it WOULD
  resolve) flips S615 to **mismatch** (same-length differing digests), violating P2's `mismatch=0`. Editing
  the digest is forbidden. → S615 cannot leave unpinned without breaking P2 or the frozen rules.
- **S125** (`SOURCES.md:131`, recorded `e60f1bbc…`): full row text (folded):
  `| S125 | Sibling lane tsukuroi, Memory pressure and systemd-oomd — round 25 entry — https://raw.githubusercontent.com/VeigaPunk/tsukuroi-shokunin/157ee255/corpus/knowledge/memory-pressure-r25.md (tsukuroi-shokunin/corpus/knowledge/memory-pressure-r25.md at commit 157ee255, git blob be3065ae512f3fefec115a23c0e8fee2cbca9fc4) | docs | B | … | commit 157ee255 …, entry bytes sha256 ecafdcdd… (27,828 B), section MP4 …; receipts .ufo/waves/round-25/capture/capture.txt sha256 e60f1bbc… (lines 73, 76, …) and .ufo/waves/round-25/capture/capture-earlyoom.txt sha256 7adbe069… (lines 6, 9, …) | … | mined | 2026-10-22 | 90d | corpus/knowledge/userspace-oom-killers-r26.md |`
  Its only copy references are the two round-25 capture receipts — BOTH ABSENT from disk and untracked
  (`test -e` → absent; `git ls-files -- '.ufo/waves/round-25/*'` = 96 files, neither among them). The row has
  NO "pinned copy" phrase and NO `corpus/evidence/` reference, so a corpus/evidence copy is invisible to it;
  the only resolution path is creating files under `.ufo/waves/round-25/` — outside every seat's write
  bounds. → S125 cannot be pinned lawfully.
- **S612 (:394), S616 (:398), S622 (:403), S623 (:404)**: each says "the pinned copy" with a recorded byte
  count (357953 / 53982 / not extracted / 171073) and no explicit path → phrase-resolvable from
  `corpus/evidence/` IFF this round's fetched live bytes hash to the recorded digests (contract method
  constraint; live-byte drift flips a row to mismatch — the kill rule owns that case). Measured hazard:
  `corpus/evidence/` currently holds 345 files and ZERO files of sizes 357953/53982/171073/362493, so
  correct placements introduce no `<ambiguous pinned copy>` collisions.
- **Best lawful landing**: `unpinned 6→2` (S125, S615), `ok 86→90`, `mismatch=0 superseded=1 prefix_only=31`.
  P2's `unpinned=0 … ok=92` is unreachable.
- **Honest stop the L1 must record**: C2 UNMET at target; S615 and S125 named stale (freshness flag) per the
  frozen kill rule — S615 stale as structural (corrupt recorded digest; supersession gate refuses unpinned
  targets; r91 C-1), S125 stale as missing-copy provenance (round-25 capture receipts gone, row unreferencing
  corpus/evidence). Receipt: post-pinning digest run showing `ok=90 unpinned=2 mismatch=0`.

## (e) Verdicts

- **C1 — needs-amend.** Before-data is sound (controls reproduce; expected cells independently derivable),
  but the contract lets a seat-authored counter satisfy every frozen clause while printing met on the
  UNEDITED scorecard (default bound or loose parser; synthetic-only red fixture). Same defect class the r91
  lesson already recorded (`attack-found-forgers-in-frozen-predicates`). Amendment must be a NEW frozen
  revision: (i) the new counter run at `66c5518e…` must print `mismatches=5` (red on the real subject, not
  only a synthetic fixture); (ii) the counter is unbounded by construction, or the frozen command pins the
  bound; (iii) integration checklist: the L1 independently re-runs the frozen r79 counter `--through 95` at
  the landing revision expecting `C2=met`, and treats any default-bound `met` as void.
- **C2 — needs-amend.** Before-measurement, method constraints and kill rule are sound; P2's target
  (`unpinned=0 mismatch=0 ok=92`) is unsatisfiable for S615+S125 under the frozen rules ((d)), and the
  contract's "Declared obstacle" clause names neither mechanism. Amendment as a NEW frozen revision: rescope
  P2 to `unpinned=2 (S125, S615) mismatch=0 ok=90 superseded=1 prefix_only=31` with both rows named stale
  and the two impossibility citations, or declare the S615/S125 stops explicitly and make the four-row
  pinning the met-condition.
- Neither claim is unsound: both befores are measured, frozen, and reproduce byte-identically.

## Bounds tension to name in the dispatch (not a claim defect)

C2 seats must ADD files under `corpus/evidence/`, and C1's counter is a NEW file under `tools/`, while the
seat rule says "Never edit tools/, corpus/…". The dispatch/validator should state that NEW files in those
trees are in scope for the named seats, so honest seats are not flagged and no existing file is edited.

## Unrun checks (named, not fabricated)

- No network fetches by this seat: live-byte verifiability of S612/S616/S622/S623 unmeasured (data seats'
  work); S622's recorded byte count not extracted from its row.
- Not run: `--selftest` of either tool; `scripts/sources-census.sh validate` (receipt only);
  `tools/mori-scorecard-calibration.py` (does not exist at freeze); no mutant or fixture runs.
- Digest rc=1 is from my clean rerun; the frozen receipt itself records no rc.

## Scratch

`/fast/scratch/hyaku/mori-r96/CritRound` used for reruns, removed at exit; no receipts kept outside this
file. No installs (tooling authorization unused).

# Mo91Sc02Lesson — round 91 lesson and knowledge-entry draft

Seat: Mo91Sc02Lesson (lesson drafting, read-only at 79eaa8cf). Entering revision `79eaa8cfe5e0b9b1c5ff45f524199d4a123f0520`.
Writes: this report, and one candidate under `w1/candidates/`. No commit, no push, no lane mutation. No installs.
Note on paths: the seat spec limits writes to `candidates/`, while the task names this report at `w1/Mo91Sc02Lesson.md`. The report is written at the named path, which is outside `candidates/` and is the only non-candidate write.

## 1. Mistake row (protocol §2b)

Row, in `class · evidence pointer · captured-by · fix` form:

R8 (round-90 defect, still open at tip):
`recorded-digest-unverified: a row's full 64-hex sha256 is never compared with the pinned copy; agreement on the 16-char prefix passes unchecked · corpus/SOURCES.md:397 (S615 anchor cell records 7891c58897fe9f78…8b1f8a60ad1a6f0); pinned .ufo/waves/round-90/w1/Mo90S01Sources/sources/python-ast-3.15.2.html = 7891c58897fe9f78…94b0f83b9a8a42f5 (362493 B); round-90 spot-check corpus/lessons/round-90-verifier-spotcheck.md:71 and :92 · none · add a row-digest pass that recomputes sha256 of each cell-named pinned copy and requires full 64-hex equality; show it fails on a one-byte-corrupted copy in scratch before it counts`

Second instance, found by this seat's sweep (not in round-90 R1–R15; `grep -c "S235"` on the round-90 spot-check = 0):
`recorded-digest-unverified (same class as R8) · corpus/SOURCES.md S235 anchor cell records 9855a4986a312dfc946b1b97b6010a8e4f1e65a4a30cda99359e6df057ad8020; pinned corpus/evidence/sources-r42/S235.pdf = 9855a4986a312dfc946b1b97b6010a8e4f1e65a4a30dca99359e6df057ad8020 (6482693 B) · none · same fix as R8; the row needs a corrected digest after the fix is shown to fail`

Captured-by determination (criterion that should have caught R8: a pinned-copy digest check on SOURCES.md rows). Result: none.
- Fleet census `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh` (on disk, sha256 `3fb7261569f46423dd80ecc23e0a23789a7926f667c7a3fc559d2439d4a64e30`; byte-equal to committed fleet HEAD `e92d8354`): its validate checks are E01–E11 and W01–W04 (NF, id, duplicate id/URL, kind, tier, status, date, recheck, community tier, used-by path existence, rows outside Registry, warnings). It reads no digest and no pinned copy.
- Lane census `tools/mori-census.sh` at `79eaa8cf`: no reads of corpus/SOURCES.md.
- Lane validators that open SOURCES.md, and what they compare:
  - `tools/mori-entry-claims-check.py` H4: row id present, status `mined`, used-by = this entry, and the source cell names the copy's `.ufo` path. It does not read the row's digest. Its `pin <sha>` check applies to claim lines in an entry, not to rows.
  - `tools/mori-anchor-check.py`: prints `pin_sha256` for the pin it is given. It compares only the caller-listed (line, quote, count) anchors, and the caller supplies them.
  - `tools/mori-source-drift.py` and `tools/mori-drift-recheck.py`: compare a live fetch with the copy's bytes. Neither compares the row's recorded digest.
  - `tools/mori-drift-adjudicate.py`: reads receipt-header digests, not row digests.
- The committed S615 row is therefore not checked by any criterion. Captured-by = `none`.

## 2. Sweep: commands and output (captured-by check)

Commands run (scripts in scratch, deleted before yield):

```
git -C /home/vgpnk/Projects/shokunin/scripts show HEAD:scripts/sources-census.sh | sha256sum
  3fb7261569f46423dd80ecc23e0a23789a7926f667c7a3fc559d2439d4a64e30  -
sha256sum /home/vgpnk/Projects/shokunin/scripts/sources-census.sh
  3fb7261569f46423dd80ecc23e0a23789a7926f667c7a3fc559d2439d4a64e30  scripts/sources-census.sh
committed-version sha256/digest hits: 0        (grep -c -E 'sha256|digest')
lane tools/mori-census.sh sha/digest hits: 9   (all are script_sha256 stamps, not row checks)
round-90 spot-check S235 hits: 0
```

Confirmation of the R8 mismatch (python, from the committed bytes at 79eaa8cf):

```
S615 recorded 7891c58897fe9f78cf16d15fd3464b746a187214c82587ac94b8f1a60ad1a6f0
S615 pinned   7891c58897fe9f78cf16d15fd3464b746a187214c82587ac94b0f83b9a8a42f5
S615 equal False prefix16 True
```

Sweep over all SOURCES.md rows at 79eaa8cf (`git ls-tree` copies under `/sources*/`, sha256 of each committed copy, rows matched by `sha256 <64 hex>` in the row text; script `digest-sweep2.py`):

```
FULL-64-MISMATCH S156 b56aa781be9c29b6 copy .ufo/waves/round-42/.../sources-r30/S156.txt 4c02999410622d78 full_equal= False
FULL-64-MISMATCH S156 88291f8249d6a86a copy .ufo/waves/round-42/.../sources-r30/S156.txt 4c02999410622d78 full_equal= False
FULL-64-MISMATCH S158 428dc8308d5caf70 copy .ufo/waves/round-42/.../sources-r30/S158.txt 9e375293fea6d643 full_equal= False
FULL-64-MISMATCH S159 dc5a771c9ed17875 copy .ufo/waves/round-42/.../sources-r30/S159.txt e6fe760c95ba3bb7 full_equal= False
FULL-64-MISMATCH S235 9855a4986a312dfc copy corpus/evidence/sources-r42/S235.pdf 9855a4986a312dfc full_equal= False
full64_recorded=176 equal_to_some_committed_copy=100 mismatch_vs_id_named_copy=5 no_id_named_copy=71
```

S235 confirmation (python):

```
S235 recorded 9855a4986a312dfc946b1b97b6010a8e4f1e65a4a30cda99359e6df057ad8020
S235 pinned   9855a4986a312dfc946b1b97b6010a8e4f1e65a4a30dca99359e6df057ad8020
S235 equal False prefix16 True len 64
```

Reading of the sweep, with its limits:
- S615 and S235 are the two rows where a full 64-hex digest is recorded against a cell-named committed copy and differs. Both agree on the 16-char prefix. That is the R8 pattern.
- S156, S158 and S159 also mismatch, but their rows name no copy path in the cell, and the only committed copies named by id are in `sources-r30/`. The row digests may cite different artifacts (for example the GitHub tag source). They are NOT classified as R8. They are listed for the L1 to resolve.
- 71 full-length rows have no id-named committed copy. They are unverified, not wrong.
- 16-char truncated digests (the lane's convention for many rows) were excluded from the mismatch class. The first sweep printed them as "PREFIX-ONLY" and that label is noise, not a finding. `digest-sweep.py` output was superseded by `digest-sweep2.py`.

## 3. Lesson section, mistake row as written for the L1

Class: recorded-digest-unverified (R8 and S235). Captured-by: none (sweep above). Fix: row-digest pass with full-length equality, shown to fail on a corrupted copy in scratch before it counts; then correct the S615 and S235 digests with an appended correction (not an in-place rewrite of the admitted row, per the append-only registry rule the round-90 spot-check cites).

## 4. Knowledge entry draft

Path: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-91/w1/candidates/calibration-arming-r91.md`
sha256: `16222f517f60d9ac8f88a2b8a8d8febe692037fd6d896ac39cd988eca9e728b2`
Lines: 78 (limit 120). Opening lines: `source: S617`, `verified-at: 2026-11-05`, `recheck: 90d`. S618 is not opened (no S618 row exists at 79eaa8cf and no S618 quote is located), so it is not in the opening line.
Quote status: `QUOTE-PENDING` ×4. Reason: S617 is not a SOURCES.md row at 79eaa8cf, and `w1/Mo91Sc01Src.md` does not exist (checked at drafting time; `w1/` holds only `candidates/` and `swarm-registry.json`). The practice claim is not written until the quote is located.
Body contents: arming rule (family-prefixed FAIL labels; frozen kill rule quoted from `contract.md` §C1 with the do-nothing control); limits (a structural arm does not prove behaviour; an independent population is an attack, not a proof; a label-accurate canary can satisfy the label rule); admission acceptance list for the L1.

## 5. Files written

| path | sha256 |
|---|---|
| /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-91/w1/candidates/calibration-arming-r91.md | 16222f517f60d9ac8f88a2b8a8d8febe692037fd6d896ac39cd988eca9e728b2 |
| /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-91/w1/Mo91Sc02Lesson.md | this file (its own digest is not recorded here) |

Scratch: `/fast/scratch/hyaku/mori-r91/Mo91Sc02Lesson/` (scripts `digest-sweep.py`, `digest-sweep2.py`). Deleted before yield.

## 6. Limits and open defects

- `contract.md` is untracked at `79eaa8cf` (on disk only, `git show 79eaa8cf:.ufo/waves/round-91/contract.md` fails with exit 128). It was read from disk, read-only. It is the frozen contract as on disk; the L1 should confirm it was committed before admission.
- The S617 quote and the S617 row are absent. The knowledge entry is a draft and is not admissible until the L1 replaces `QUOTE-PENDING`.
- The "captured-by" determination is by reading the validators and by the sweep above. It is not an executed negative test. The "fix" is a proposal; no fix was built or shown to fail.
- S156, S158, S159 are unresolved (see §2). S235 is a new instance found by this seat, not previously routed.
- I did not run any counter (`count-c1.py`, `count-c2.py`) and did not touch `mutants-c1*.json`, evidence/, corpus/, SCORECARD.md, LOG.md, SHONEN.md, SKILL.md or MANIFEST.json.
- Installs/updates: none.

## 7. Verdict per item

1. Mistake row: written. Captured-by = `none`. R8 confirmed by committed bytes (full digest mismatch, prefix agrees). One new instance (S235).
2. Knowledge entry: draft written, 78 lines, opening lines as specified, `QUOTE-PENDING` ×4 (S617 quote not located). Not admissible yet.
3. Report: this file.

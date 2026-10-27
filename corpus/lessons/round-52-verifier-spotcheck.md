# Round 52 verifier spot-check

author: hyaku closure (non-author integrator, @m_opus)
lane: mori-shokunin · round 52 · closed 2026-10-26
base `4f266ef2fdf74d8b046f5b4f5a5c4945f65b966d` → tip `37af57f263cf0f035fa6d19f666d2de7790b63b7`
(branch `master`, remote verified); receipts measured at `e7e056b8a17e54516a3c17798221c30e9902c250`.

## Step-1 conformance

- Report `.ufo/reports/round-52/mori.md` committed on the fleet repo by the lane identity:
  `git log --format='%an %ae %H' -- .ufo/reports/round-52/mori.md` → `mori-shokunin mori@shokunin.local
  aacd7a83027cdee8e950a2c39d490feaed3be13c`; ancestor of fleet HEAD `b2c82b9c` and pushed
  (origin/master = origin/main = b2c82b9c).
- `SHONEN` heading: `grep -c '^## SHONEN'` → 1, four `[~]` lines, one per box, each with a pointer.
- Cited lane commits `4f266ef2 d3a8ea59 8524904a 075436b1 2f245af7 e7e056b8 37af57f2` all exist and
  `git merge-base --is-ancestor <h> master` holds for each (7/7).
- `jj-lane.sh state` → `local=remote=37af57f2 ahead=0 behind=0`; `git status --porcelain` empty —
  no uncommitted round work; `git ls-remote origin refs/heads/master` → `37af57f2`.
- Prompt `.ufo/prompts/mori-round-52.md` carries the full round contract (§1–5 verbatim incl. the five
  child-lane items) and is committed (`5f7af06e`, lane identity).
- Driver digest (watchdog.log is mutable; copied): `2026-10-26T20:40:50-03:00 launch mori round=52
  pgid=2882097 driver=hyaku-inline attempt=1`; `2026-10-26T21:57:11-03:00 complete mori round=52;
  hyaku-inline attempt=1`.
- Status: `ok` — a real report with checkable work, not a marker.

### Conformance defects (status-neutral)

- D1: report lines 5 and 46 carry `[FILL]` where the report's own commit hash belongs (the hash that
  exists is `aacd7a83027cdee8e950a2c39d490feaed3be13c`). Routed for correction next round.
- D2: `SCORECARD.md` round-52 C1 row records `items=42 … locators=27` while citing
  `evidence/c1-at-landed.txt`, whose quiescent run at `e7e056b8` prints `items=43 … locators=28`.
  Attribution (checked): the row was written at integration `2f245af7`, before `c1-at-landed.txt`
  existed; its numbers are verbatim from `c1-at-data.txt` (measured `8524904a`), so the citation
  anticipates the later receipt. Both receipts print `C1=met … mismatches=0 errors=0`, rc 0 — the
  verdict is unaffected; the row's numbers-vs-citation mismatch wants an appended correction.
- Receipt `manifest=6209bdb8e400` pins the fleet MANIFEST at `f0b61b4a` (the ledger state when
  measured); current HEAD MANIFEST differs only by later kama/kengaku closure appends — no mori row
  touched. Not a defect; noted for provenance.

## Claims — evidence-verified per §Gate standard (lane-owned counters not executed by this judge)

Both counters are lane-owned gates; per PROTOCOL §Gate standard "Closure consequence" their committed
evidence (self-test tally, frozen-run verdict, revision measured) was verified, and each item-level
claim was independently corroborated with plain commands over committed bytes (never by running the
gate).

### C1 — calibration: `improved`

- Committed evidence: `evidence/c1-at-landed.txt` verbatim `C1=met items=43 axes=6 pins=2 boxes=4
  living=7 superseded=4 locators=28 mismatches=0 errors=0 hidden=0 lane_writes=0
  manifest=6209bdb8e400 rev=e7e056b8` exit 0; before-run `control-c1-do-nothing.txt` at `4f266ef2`:
  `C1=unmet items=37 … mismatches=8 … failed=mismatch` exit 1. Self-test `selftest-c1.txt`:
  `C1_SELFTEST pass=42 fail=0`. Seven control receipts all unmet (do-nothing 8 mismatches; axes-only
  5; receipts-only 6; living-only 5; rewrite-in-place / delete-stale-pins / repeat-stale-tally 3
  each); witness met (disclosed feasibility control).
- Independent corroboration (non-author seat, commands over committed bytes): MANIFEST last mori
  closure = round 51 `admitted`, no mori row with lane_round >51 (51 mori entries: 26 admitted, 14
  rejected-*, 11 legacy null); `## Axes` rows lead with round-51 citations for operability and depth,
  all six `state=ok` against receipt expectations; SHONEN 4 boxes `[~]` with round-52 receipts; QUALITY
  rows 141/142 and README `## Round-52 corrections` exist at the receipt's lines; `SCORECARD.md:1781`
  holds the `5 → 6` pair; all 28 receipt locators resolve at tip; `tools/mori-pin-check.py`
  (125/125) and `tools/mori-unlanded-check.py` (17/17) receipts committed under `evidence/selftests/`.
  All agree.

### C2 — depth (lowest axis, tied at 5): `improved`

- Committed evidence: `evidence/c2-at-landed.txt` verbatim `C2=met claims=28 located=28
  quote_missing=0 bad_rows=0 sources=5 source_rows=ok pins=ok provenance=ok entailed=28 dissent=0
  rev=e7e056b8` exit 0; before `control-c2-do-nothing.txt` at `4f266ef2`: `C2=unmet claims=0 …
  failed=entry_absent,pins` exit 1; at data `c2-at-data.txt`: `failed=entailment` (votes landed
  later). Self-test `selftest-c2.txt`: `C2_SELFTEST pass=45 fail=0`.
- Independent corroboration: `corpus/knowledge/overcommit-commit-limit-r52.md` opens with the
  provenance trio (five `source:` lines S497–S501, `verified-at: 2026-10-26`, `recheck:` loop);
  `## Claims` table holds exactly 28 rows each carrying an S-id, distribution S497 7 / S498 6 /
  S499 9 / S500 2 / S501 4; 12 voter files `Mo52Ent01–12` carry 93 unfenced ENTAIL lines covering
  31 hashes, all 28 landed hashes entailed by ≥2 distinct seats, the only under-voted hash being the
  replaced row-3 old text (`93b4fe285dc7` → `3c2512af8468`, re-voted by Ent02/03/04; rows 27/28
  replaced by `10ac5a250ac2`/`1cadeed9914b`, re-voted Ent10/11/12); `w1-results.json` holds 68 seat
  results, dead 0, role mix matching the report.
- Judge's own re-open: pinned copies `corpus/evidence/sources-r52/` sha256 all five match the row
  anchors and `freeze-sha256.txt`; sampled quotes verified verbatim — S499 `util.c.v7.2:994-995`
  (`if (percpu_counter_read_positive(&vm_committed_as) < allowed) return 0;`), S497
  `overcommit-accounting.rst.v7.2:20-22` (mode-2 swap+RAM sentence), S501 `mmap.c.v7.2:550-553`
  (MAP_NORESERVE honored unless OVERCOMMIT_NEVER). Live re-fetch of
  `raw.githubusercontent.com/torvalds/linux/v7.2/mm/util.c` is byte-identical to the pinned copy
  (sha256 `e702754c…3ebe7c`).

### Axis harm check

`git diff 4f266ef2 37af57f2 -- SCORECARD.md`: only the operability/depth/freshness rows' evidence text
changed; all six scores unchanged (6/7/5/5/5/6). No axis harmed. Per-axis verdicts: calibration
`improved`, depth `improved`, coverage/operability/freshness/adjacency `unchanged`.

## Spot-check (LEARNING.md — non-author, ≥1 admit + ≥1 reject)

| item | decision | re-opened source | verdict | reason |
|---|---|---|---|---|
| S499 admit (mm/util.c v7.2) | admit, mined, tier A | live URL `raw.githubusercontent.com/torvalds/linux/v7.2/mm/util.c` + pinned copy | **agree** | live bytes sha256 `e702754c…3ebe7c` identical to `corpus/evidence/sources-r52/util.c.v7.2`; Gate quote verbatim at lines 994-995; quote ≤25 words with locator; tier A code for its scope is correct |
| S497 admit (overcommit-accounting.rst v7.2) | admit, mined, tier A | pinned copy `overcommit-accounting.rst.v7.2` | **agree** | quote located verbatim at lines 20-22; sha256 `767ab881…4927f` matches anchor and freeze list; authoritative docs for the mode-2 limit claim |
| kernel.org `latest` overcommit page | reject | `curl https://www.kernel.org/doc/html/latest/mm/overcommit-accounting.html` | **agree** | fetched 2026-10-26: HTTP 200, 13558 bytes, renders "The Linux Kernel **7.3.0**" — the `latest` locator moved past v7.2 exactly as the rejection reason states; release-pinned rendered URL would be the valid flip; raw tag copy already covers the text |
| S501 row quote | ≤25-word check | pinned copy `mmap.c.v7.2:550-553` | **agree** | row's located quote ("We honor MAP_NORESERVE if allowed to overcommit */ if (sysctl_overcommit_memory != OVERCOMMIT_NEVER) vm_flags \|= VM_NORESERVE;") sits verbatim at lines 551-553, 13 words, escaped pipe keeps the row at 11 columns |

Census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori` run by this
judge → `exit=0`, 23 W04 warnings (pre-existing duplicate-url cross-scope warnings, unchanged from
round start). Rows 269 → 274 (`diff --numstat` → `5 0`; grep counts confirmed at both revisions).

## Trend verdicts

- **expansion: improved** — one admitted entry on commit-ledger ground the lane did not hold (the
  13-term sweep `sweep-overcommit.txt` shows 0 hits each; `merge/mori/` 0 files), each of its five
  `source:` ids a `mined` tier-A row opened this round; README `## Round-52 coverage additions` lands.
- **quality: improved** — three stale living pins superseded without rewrite (QUALITY 141/142,
  README corrections block); the `:1771`→`:1781` locator drift fixed and pinned (QUALITY 142); two
  overclaim rows and two unit-conflation rows replaced and re-voted; round-51 counters rerun at
  `70e68cdd` reproduce landed receipts field-for-field (`w1/Mo52ExecR51C1Rerun.md`,
  `w1/Mo52ExecR51C2Rerun.md`); erratum `round-51-erratum.md` corrects S493 locators.
- **discernment: improved** — spot-check agrees with the gate on all four sampled decisions (2
  admits, 1 reject, 1 row quote); the reject is well-reasoned (moving `latest` vs pinned tag) and the
  replacement-vote mechanism ran honestly under dissent. The lane's self-grade was
  `unprovable-but-better`; the outside check upgrades it: agreement on admit *and* reject.

## Routed defects for the lane's next round

1. Append a SCORECARD correction: the round-52 C1 row cites `evidence/c1-at-landed.txt` but carries
   the at-data tally (42/27) instead of the landed quiescent tally (43/28) — append-only fix naming
   the superseded line.
2. Report self-citation: the `Report commit [FILL]` slots in the round-52 report were never resolved;
   adopt a convention that either resolves the hash in a follow-up fleet commit note or leaves the
   marker removed — the report body currently reads as unfinished bookkeeping.
3. Standing: locator arm covers Axes rows and SHONEN boxes only (78 pointers in QUALITY/README
   unarmed); receipts are pure text; arm-A verdict pinned only to `admitted` — the lane already
   carries these in `Planned (round 53)`; this judge concurs.

## Verdict

Both claims verify on committed gate evidence plus independent corroboration; no axis harmed;
spot-check agrees with the gate on admit and reject. **admitted.**

# ScribeDraft — round 96 wave w1 (mori, scribe seat)

Role: scribe (leaf member, no dispatch). Scope: prose drafting only; **no measurement command was run by this seat**.
All values quoted below are read out of receipts already committed under `.ufo/waves/round-96/evidence/`.

## Files written (only these, plus this report)

- `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-96/w1/scribe/lesson-draft.md`
- `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-96/w1/scribe/scorecard-draft.md`
- `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-96/w1/ScribeDraft.md` (this report)

No scratch directory was created and nothing was written under `$HYAKU_SCRATCH`: the seat produced no intermediate
artifacts and kept no receipts of its own, so there was nothing to copy before exit. No tool was installed (no install
to record). No git/jj mutation was run; only read-only inspection of files in the lane and the fleet.

## Deliverable shape (as specified)

- `lesson-draft.md`: `# Round 96 — lesson draft (mori)`; `## Gate` with an empty `| Candidates | Admitted | Rejected |`
  header and the line `spot-check: pending (non-author)`; `## Mistakes (CORPUS: class · evidence · captured-by · fix)`
  as a `# | Class | Evidence | Captured-by | Fix` table with exactly the two specified rows; `## Sources & frontier`
  carrying the census command line and `<<AFTER>>` placeholders.
- `scorecard-draft.md`: round-96 section draft with a claim table `claim | axis | predicate | before | after | command | commit`,
  before `5 mismatches` (C1) and `unpinned=6` (C2), after `<<AFTER>>`, plus paste-in prose blocks for the `Last change`
  cells, the axis-harm check and the correction note.

Every after-value is an explicit `<<...>>` placeholder (`<<AFTER>>`, `<<COMMIT>>`, `<<CONTRACT-COMMIT>>`,
`<<ROUND-96-HEADLINE>>`, `<<CORRECTION-NOTE...>>`). No number beyond the two before-values was asserted.

## Evidence quoted in the drafts (verbatim from receipts, not re-measured)

C1 — `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-96/evidence/before-c1-count-c2-through95.txt`:

```
axis coverage cell=round_56_improved expect=round_80_improved state=mismatch
axis operability cell=round_78_improved expect=round_93_improved state=mismatch
axis depth cell=round_76_improved expect=round_86_improved state=mismatch
axis freshness cell=round_78_improved expect=round_82_improved state=mismatch
axis calibration cell=round_78_improved expect=round_93_improved state=mismatch
axis adjacency cell=round_19_improved expect=round_19_improved state=ok
C2=unmet axes=6 mismatches=5 errors=0 rows=58 through=95 rev=66c5518e239e
```

C1 default bound — `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-96/evidence/before-c1-count-c2-default.txt`:

```
C2=met axes=6 mismatches=0 errors=0 rows=46 through=78 rev=66c5518e239e
```

Bound source — `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-79/count-c2.py:33` `THROUGH = 78`;
`:207` `ap.add_argument("--through", type=int, default=THROUGH)`; `:83` `if not isinstance(rn, int) or rn > through: continue`.

C2 — `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-96/evidence/before-c2-digest.txt` (last line):

```
DIGEST_CHECK rows=124 ok=86 mismatch=0 superseded=1 prefix_only=31 unpinned=6
```

Unpinned rows named in that receipt: S125, S612, S615, S616, S622, S623.

Census — `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-96/evidence/before-census.txt`:

```
# sources-census validate --root fleet mori at 66c5518e239eeacd6070be26d78085ef702392cb (rc=0)
mori	ok	/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md
```

Command line carried in the draft: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori`
(script confirmed present at `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh`).

## Verdict on the drafted content

The drafts are internally consistent with the frozen contract: section order, column names, the two mistake rows
(class / evidence / captured-by / fix) and the two before-values match the contract's Frontier-step wording. The drafts
make no admission verdict and no score move.

## Unrun checks (named)

- No measurement command was run by this seat (prose-only assignment): the frozen counter at `--through 95` and at its
  default bound was **not** re-executed here; the digest tool was **not** re-executed here; the census was **not**
  re-run here. All three are quoted from the round-96 before-receipts.
- The `w1/calib/` receipt directory named in mistake row 1 did not exist at the time of drafting (the wave's `w1/` held
  only `scribe/` and `swarm-registry.json`); the citation is carried forward as the task specified it and is for the
  calib seat to populate.
- The landing `Last change` cells, the landing `unpinned` value and the landing census exit code are unmeasured here and
  left as `<<AFTER>>` placeholders for the L1.
- No check of the S125 sibling-repo path resolution was performed (out of this seat's scope; owned by the digest seats).

## Out of scope for this seat

No edit to `tools/`, `corpus/`, `SCORECARD.md`, `LOG.md`, `MANIFEST.json`, the frozen contract, the round-79 counter, or
any sibling lane. No host sysctl, service or limit touched. No commit, push, `fleet-commit.sh` or `jj-lane.sh` run.

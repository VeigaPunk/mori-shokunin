# Mo58Critic24 — round-start SOURCES census

## Result

No counterexample to the frozen round-start count or manual tier/status histograms. At freeze revision `fe8801120a67c1a6b8899d7d0423839caa09e7d0`, `corpus/SOURCES.md` contains 322 registry rows:

- Tier: A=290, B=14, C=18 (invalid=0).
- Status: mined=270, queued=24, rejected=28 (invalid=0).

Both histograms sum to 322. This matches the contract's round-start count (contract.md:67-70). The freeze file SHA-256 is `3b40fb637a78f54ea7082f04003ed7d21386f44a6f126420235ebb0b25be5d6e`.

## Commands and evidence

1. Extracted committed freeze bytes: `git show fe8801120a67c1a6b8899d7d0423839caa09e7d0:corpus/SOURCES.md > /fast/scratch/hyaku/mori-r58/Mo58Critic24/SOURCES.freeze.md`; `sha256sum` returned the digest above. `git diff fe8801120a67c1a6b8899d7d0423839caa09e7d0 HEAD -- corpus/SOURCES.md` was empty; the post-freeze commit `4272736c` adds only round-58 dispatch/build artifacts.
2. Manual parse of that frozen copy: awk restricted rows to after `## Registry`, skipped header/separator, required `NF==13`, then counted tier `$5` and status `$9`. Output: `rows=322`, `tier.A=290`, `tier.B=14`, `tier.C=18`, `status.mined=270`, `status.queued=24`, `status.rejected=28`; no bad-NF rows.
3. Cross-check: copied the frozen bytes into a scratch lane-shaped `fix/corpus/SOURCES.md` and ran `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh census /fast/scratch/hyaku/mori-r58/Mo58Critic24/fix`. It independently returned rows=322, tier A/B/C=290/14/18, status mined/queued/rejected=270/24/28, invalid=0, missing=0, exit 0.
4. `sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori` on the current working tree returned exit 0 (`mori ok`) with W04 duplicate-URL warnings. Note: this is not a freeze-only validation run.

## Bounded adversarial note

The working tree currently has one uncommitted `| S550 |` row: `git show HEAD:corpus/SOURCES.md | grep -c '^| S550'` returned 0, while `grep -c '^| S550' corpus/SOURCES.md` returned 1. The canonical census on that working tree therefore reports 323 rows (A=291, mined=271). This is consistent with the contract's expected round-end S550, but must not be substituted for the committed freeze baseline of 322.

A separate contract-scope ambiguity: contract.md:64 names quarantine rows S244, S262, S268. At freeze, only S262 appears in `corpus/SOURCES.md` (row at line 243 of the extracted file); `S244` and `S268` have no matches anywhere in that frozen file. If the slice is meant to be re-derived from this lane registry, those two inputs are absent; if it refers to another source, the contract should identify it. This does not falsify either C1 or C2 census claim. Smallest safe correction: state the quarantine source/scope, or correct the listed IDs before treating it as lane-local.

## Impact

- C1/C2 census baseline: no counterexample; exact count and histograms match.
- Quarantine procedure: potentially affected only if contract line 64 intends a lane-local SOURCES slice; otherwise no axis impact.

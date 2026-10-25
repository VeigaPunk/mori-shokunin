# ExecV2Junk — w2 report (round 47): re-score the committed c1-junk variants with the v2 pin-check

Seat: ExecV2Junk (leaf executor). Lane: mori-shokunin. Wave: w2 (falsify the landed round).

## Assignment

Re-score the committed junk variants under `.ufo/waves/round-47/controls/c1-junk/skill-v*.md` with the v2 tool:

```
python3 tools/mori-pin-check.py --rev 63eecf2738db96f46b0bd02b1b2dfd66787493d0 \
  --min-tally-pins 26 --baseline-rev 2d85e33d14198d388fd3cda9cc15ec07e57e7a53 --skill <variant>
```

Expected: `skill-v1-honest` → PIN_CHECK=met, all other variants → unmet. Compare with `.ufo/waves/round-47/evidence/v2/*.txt`.

## Method / environment

- Tool run: `/home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-pin-check.py` (working tree).
  - Working-tree tool sha256 = `9832e38c3863ba82f7a740921e8c9d23d6cf2e702c2bb62ee2ad71fcc21bc2b6`; `git show af2250d80033ded23ec34af328068eeb85007d1c:tools/mori-pin-check.py` = the same bytes — the re-score uses exactly the tool the v2 receipts were measured with. The contract's FROZEN v1 bytes are `e3ef425a…` (this seat does not score P-C1 itself; it only re-scores the junk variants with v2).
- Each run: `--rev 63eecf27` (freeze F), `--min-tally-pins 26`, `--baseline-rev 2d85e33d` (entering E); `TMPDIR=/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r47w2-ExecV2Junk`.
- Variants are committed and untouched: `git status --porcelain` shows no changes under `.ufo/waves/round-47/controls` or `.../evidence`.
- Fresh outputs kept at `.scratch/r47w2-ExecV2Junk/rescore-skill-v*.txt`.
- No tools installed; no lane file mutated (only the scratch dir above was written).

## Results (fresh runs, v2 tool)

| variant | PIN_CHECK | rc | distinguishing lines (line refs = output lines) |
|---|---|---|---|
| skill-v0-frozen | unmet | 1 | L912 tally `MORI_SOURCES_APPENDONLY_SELFTEST` state=mismatch pinned='pass=15 fail=0' observed='pass=22 fail=0'; tallies 26, mismatches=1 |
| skill-v1-honest | met | 0 | all pins match; tallies 26, mismatches=0, dropped=0, rebound=0, duplicate=0 |
| skill-v2-oldcopy | unmet | 1 | L912 state=no_command (bound path `.scratch/MutGateFirstParent/gate-v3-pristine.py` fails v2 SAFE_PATH); no_command=1 |
| skill-v3-fakeecho | unmet | 1 | L912 state=no_command (inline `python3 -c … --selftest` binds nothing); no_command=1 |
| skill-v4-weakened | unmet | 1 | L912 state=mismatch pinned='pass=22' observed='pass=22 fail=0' (weakened pin); mismatches=1 |
| skill-v5-renameprefix | unmet | 1 | L912 state=mismatch pinned='_V2 pass=22 fail=0' observed='pass=22 fail=0'; mismatches=1 |
| skill-v6-deleted | unmet | 1 | baseline dropped: row 'SOURCES append-only timing (r38)' pin `MORI_SOURCES_APPENDONLY_SELFTEST` count=1; tally_pins=25 (< 26 floor), dropped=1 |
| skill-v7-entrycopy | unmet | 1 | L912 state=no_command (entry cell borrowed via bare `--selftest` contains `.scratch/…` path); no_command=1 |
| skill-v8-hide+dup | unmet | 1 | L912 row unparsed cells=10 header=8 (row naming selftest with wrong cell count); L913 state=no_command; unparsed=1 no_command=1 |

Verdict vs expectation: **v1-honest met, all other 8 unmet — matches the expectation exactly.**

## Comparison with evidence/v2 receipts

For each of the 9 variants, the fresh run output is byte-identical to `.ufo/waves/round-47/evidence/v2/<variant>.txt` after stripping the receipt's header line (command echo incl. "(v2 at af2250d8…)") and the trailer `rc=0/1` line (my runs append the same rc trailer). 9/9 identical:

```
skill-v0-frozen: IDENTICAL … skill-v8-hide+dup: IDENTICAL
```

The v2 receipts reproduce byte-for-byte on re-run.

## Findings

1. Confirmed: the v2 tool turns the honest variant green and every junk variant red — the v2 hardening (SAFE_PATH bound commands, exact-tail equality, weakened-pin mismatch, dropdown/rebound tracking, duplicate row names, unparsed short rows) closes the wave-1 false-green classes on all 8 committed junk variants.
2. The junk controls are stable: same verdicts and same counts as the stored receipts; nothing drifted since af2250d8 for these inputs.
3. Scope note: the round-47 claim P-C1 is scored with the FROZEN v1 bytes (`git show 63eecf27:tools/mori-pin-check.py`, sha256 `e3ef425a…`), which is a different measurement and a different seat's verdict; this report only covers the v2 junk re-score. The v2 tool in the tree is a strict superset guard, not the claim's rule.

## Risks / blockers

- None. All evidence is exercised (fresh runs + receipts); no unverified clause in scope.
- The 9 rescore runs each export the freeze commit and execute ~26 pin commands; outputs were captured to scratch (paths above), not printed in full here.

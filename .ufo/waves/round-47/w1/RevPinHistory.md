# w1 / RevPinHistory — git archaeology: the SKILL.md:912 `pass=15` pin (C1)

Seat: RevPinHistory (leaf, reviewer). Lane repo: `/home/vgpnk/Projects/shokunin/mori-shokunin`.
Method: read-only git (`log -S`, `show`, `diff`, `rev-parse`) over committed bytes; extracted
scripts run with `TMPDIR=/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r47-RevPinHistory/tmp`.
No git/jj state mutated; no pacman; no tools installed (used system python3 and git only — nothing
to record under the 2026-10-19 tooling directive).

## Verdict

**The commit that made the pin stale is `d72ac167`** — "round-41: freeze C1-C3 contracts and
controls" (2026-10-24 04:46:03 -0300). It is the first revision whose
`tools/mori-sources-appendonly.py --selftest` prints `pass=22`, and in that same commit the
SKILL.md self-test cell still reads `pass=15 fail=0`. The pin had been true when written at
`265a955c` (~2h earlier) and was never updated afterwards; it reached the entering tip
`2d85e33d` unchanged, where it is the single C1 mismatch.

## Timeline (cell = self-test cell of row "SOURCES append-only timing (r38)")

| commit | when (author ts) | cell (committed bytes) | tool `--selftest` | state |
|---|---|---|---|---|
| `daa1d4d2` (r38, row creator) | 2026-10-23 17:55:25 | `pass=9 fail=0` | not run (UNVERIFIED; irrelevant) | — |
| `265a955c` (r40) | 2026-10-24 02:47:29 | `pass=15 fail=0` at line 889 | `pass=15 fail=0`, exit 0 | pin TRUE at birth |
| `d72ac167` (r41) | 2026-10-24 04:46:03 | still `pass=15 fail=0` at line 889 | `pass=22 fail=0`, exit 0 | **pin STALE from here** |
| `2f04605a` (r46) | 2026-10-25 10:15:37 | cell untouched (see E3) | 22 (tool untouched since r41) | stale |
| `2d85e33d` (entering) | — | `pass=15 fail=0` at SKILL.md:912 | `pass=22 fail=0`, exit 0 (tip run) | stale — the C1 mismatch |

## Evidence (command → output → exit)

**E1. Tool tally at the two named revs.**
`git show <rev>:tools/mori-sources-appendonly.py > .scratch/r47-RevPinHistory/msa-<rev>.py`,
then `TMPDIR=<scratch>/tmp python3 <copy> --selftest`:
- `265a955c` → `MORI_SOURCES_APPENDONLY_SELFTEST pass=15 fail=0`, `exit265=0`
- `d72ac167` → `MORI_SOURCES_APPENDONLY_SELFTEST pass=22 fail=0`, `exitD72=0`
- tip (worktree copy; its sha256 `75af8f6f…40d8f76b` equals `git show 63eecf27:tools/…`) →
  `MORI_SOURCES_APPENDONLY_SELFTEST pass=22 fail=0`, `exit_tip=0`

**E2. `d72ac167` is the only commit that could have moved the tally after the pin was written.**
`git log --format='%h %ci %s' -- tools/mori-sources-appendonly.py` →
`bf0df77f` (r36), `daa1d4d2` (r38), `97b826a9` (r39), `265a955c` (r40), `d72ac167` (r41, last).
`git diff --stat 265a955c d72ac167 -- tools/mori-sources-appendonly.py` →
`1 file changed, 303 insertions(+), 108 deletions(-)`; the added lines include
`_r41_render_permuted`, `_r41_merge_resolved`, `_make_r41_dag_repo`, `_selftest_r41_dag_cases`
and `P-C12` timing text — the round-41 timing/DAG arms. 15→22 = +7 cases, matching the
"+7 arms" narrative now in the (uncommitted) SKILL.md row.

**E3. The pin was written once and never touched again.**
- `git log --format='%h %ci %s' -S'MORI_SOURCES_APPENDONLY_SELFTEST pass=15' -- SKILL.md` →
  exactly one commit: `265a955c` (string added there, never removed).
- `git log --format='%h %ci %s' -S'pass=22' -- SKILL.md` → empty: no commit in history ever put
  `pass=22` anywhere in SKILL.md.
- `git show d72ac167:SKILL.md | grep -n 'pass=15'` → line 889 still pins
  `MORI_SOURCES_APPENDONLY_SELFTEST pass=15 fail=0` in the very commit that changed the tool.
- `git diff d72ac167 2d85e33d -- SKILL.md | grep -o 'MORI_SOURCES_APPENDONLY_SELFTEST pass=[0-9]* fail=[0-9]*'`
  → no output: the cell is byte-identical from the r41 freeze through the entering tip; its line
  number moved 889→912 only because rows were inserted above the table. `2f04605a`'s `-S'pass=15'`
  hit is its unrelated r44/r45 registry-row repairs (`pass=6`→`pass=15` for GATE_REGISTRY), not this row.
- `git show 2d85e33d:SKILL.md | sed -n '912p'` contains
  `MORI_SOURCES_APPENDONLY_SELFTEST pass=15 fail=0` — contract's "SKILL.md:912" located.

**E4. End-to-end corroboration with the frozen counter (do-nothing control).**
`git show 63eecf27:tools/mori-pin-check.py > .scratch/r47-RevPinHistory/pincheck-frozen.py`
(extracted bytes sha256 `e3ef425abde30974faf53a894f96650af11570d2125a5bf621395f6ab0d903e1`,
equal to the contract's frozen hash), then
`TMPDIR=<scratch>/tmp python3 pincheck-frozen.py --rev 2d85e33d… --min-tally-pins 26 --baseline-rev 2d85e33d… --repo <lane>`:

```
pin line=912 kind=tally prefix=MORI_SOURCES_APPENDONLY_SELFTEST state=mismatch pinned='pass=15 fail=0' observed='pass=22 fail=0' rc=0 cmd='python3 tools/mori-sources-appendonly.py 2d85e33d14198d388fd3cda9cc15ec07e57e7a53 --selftest'
PIN_CHECK=unmet tally_pins=26 digest_pins=5 mismatches=1 unparsed=0 no_command=0 dropped=0 min_tally_pins=26 rev=2d85e33d14198d388fd3cda9cc15ec07e57e7a53 baseline=yes
```
exit=1. Exactly one mismatch, at SKILL.md:912 — matches the contract receipt
`evidence/control-c1-donothing.txt` (unmet, `mismatches=1`), i.e. the staleness this wave's C1
fix targets is precisely the r41 fallout identified above.

## Answers to the seat questions

- **When did the self-test cell get `pass=15`?** `265a955c` — "round-40: instruments — conform v3
  (P-C10), gate v3 (P-C11), S229, r39 erratum", 2026-10-24 02:47:29 -0300. It was accurate when
  written: the tool's bytes at that revision print `pass=15 fail=0`, exit 0.
- **When did the tool's selftest grow to 22?** `d72ac167` — first revision printing
  `pass=22 fail=0` (verified by running both revisions' bytes).
- **Commit that made the pin stale: `d72ac167`** (r41 freeze, 2026-10-24 04:46:03 -0300). The pin
  was true for ~1h59m; it has been stale from that commit through the entering tip — so the C1
  defect predates round 46 by four rounds and was simply never re-measured until
  `tools/mori-pin-check.py`.

## Working-tree observations (detection only — not part of the committed-history verdict)

- Freeze integrity: `git rev-parse 63eecf27^` = `2d85e33d…` (entering tip is the freeze's parent);
  the freeze diff vs entering touches only `tools/mori-pin-check.py` (+484) among
  SKILL.md/tools/SOURCES.md; frozen hashes reproduce: `mori-pin-check.py` = `e3ef425a…` ✓,
  `.ufo/waves/round-47/count-c2.py` = `fc77b933…` ✓ (contract bytes intact at HEAD).
- At my first observation the worktree showed uncommitted `M` on `SKILL.md`,
  `corpus/QUALITY.md`, `corpus/README.md`, `corpus/SOURCES.md`, `tools/mori-pin-check.py`;
  at a later observation `sha256sum tools/mori-pin-check.py` equaled the frozen `e3ef425a…`, so
  the instrument bytes are currently frozen-clean (the earlier `M` was either a sibling's
  transient mutant, since reverted, or stat dirt). The uncommitted `SKILL.md` already carries the
  `pass=22` cell plus a round-47 reconciliation narrative for this row — consistent with E3's
  "no commit contains `pass=22` in SKILL.md": the C1 build exists only as uncommitted worktree
  edits awaiting L1 integration. Measured against committed bytes per the contract rule
  (`git show <freeze>:<path>`), the mismatch of E4 stands at the freeze; the fix is not landed yet.

## Limits / UNVERIFIED

- The tool tally at `daa1d4d2` (r38, cell then `pass=9`) was not run — not needed for the
  staleness verdict, which only requires the 265a955c/d72ac167 pair (both run, E1).
- I identified the r41 arm functions added in the diff (E2) but did not enumerate the seven new
  case names individually; the +7 (15→22) delta is measured, the "seven arms" phrasing in the
  worktree narrative is consistent with it (UNVERIFIED as an exact list).
- Timing of sibling worktree mutations is unobservable from committed history; I report byte
  state at my observation moments only (no reruns to confirm).
- Scratch: `.scratch/r47-RevPinHistory/` (`msa-265a955c.py`, `msa-d72ac167.py`,
  `pincheck-frozen.py`, `tmp/`); all selftest/pin-check runs used TMPDIR inside it.

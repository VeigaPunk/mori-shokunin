# RevCensusPair — census-start vs census-end (round 40, w1)

Seat: reviewer (read-only). Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin`.
Entering tip `bb1f2457bb8d3e8d5dfe98488b91e8c02e378ca3`; scored tip
`265a955cc67be4eae97d2dc5a9338a25f31eb29b`; lane HEAD at review
`ede486b7a09afbacfb380d5871c46a8051a6dc2e`. No writes to the lane or fleet,
no jj/git mutation, no pacman, no tool installs.

## Verdict in one line

The two receipts are **byte-identical** and name the **same 16-row W04 set**, and
S229 introduces **no new warning class** — but the end receipt's **exit 0 is not
reproducible at the scored tip** `265a955`: on those committed bytes the census
prints `mori	E12	S229 row outside Registry section` and exits **1**. The exit-0
bytes census-end records are the post-265a955 repaired working tree, committed
only later as `ede486b`.

## Exit codes (explicit)

| receipt | recorded in receipt | re-measured exit | measured bytes |
|---|---|---|---|
| census-start.txt | no exit field | **0** | `bb1f2457:corpus/SOURCES.md` (sha256 `c993e977…`) |
| census-end.txt | no exit field (0 recorded only in `w1/ExeCensus.md`) | **0** at `ede486b`, **1** at scored tip `265a955` | `ede486b` sha256 `c9e8f039…`; `265a955` sha256 `3418f0bb…` |

## Commands run and outputs

1. Byte identity and shape (lane cwd
   `/home/vgpnk/Projects/shokunin/mori-shokunin`):

   ```
   $ sha256sum .ufo/waves/round-40/evidence/census-start.txt .ufo/waves/round-40/evidence/census-end.txt
   d823173352f740d3495cbf6ebcab456a775e22133d84ffad1661275318d14319  …/census-start.txt
   d823173352f740d3495cbf6ebcab456a775e22133d84ffad1661275318d14319  …/census-end.txt
   $ wc -l -c …  → 17 lines, 1781 bytes each;  $ cmp … → identical (exit 0)
   $ awk -F'\t' '{print $2}' <each> | sort | uniq -c
          1 ok
         16 W04
   ```

   Id sets (`awk '$2=="W04"{print $3}' | sed 's/ duplicate url .*//' | sort`)
   are identical and duplicate-free: `S035,S037,S073,S074,S075,S076,S147,S148,
   S149,S150,S166,S168,S201,S218,S220,S228` (16). Each file has exactly one
   `mori	ok	…/corpus/SOURCES.md` line, and no E code and no W01/W02/W03 line.

2. Live run of the exact command on the real root:

   ```
   $ cd /home/vgpnk/Projects/shokunin && scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori
   … 16 W04 rows + mori ok …
   EXIT=0
   $ cmp <live output> evidence/census-end.txt   → identical
   $ cmp <live output> evidence/census-start.txt → identical
   ```

3. Tip-specific reproduction under lane semantics (the real root cannot be
   rewound without mutating lane state, so each revision's committed
   `corpus/SOURCES.md` was placed in a `/tmp` lane mirror: real dir + symlinks
   to the lane's current used-by tree + a one-line `mori | mori-shokunin` conf;
   run from `/tmp` with an absolute root and lane id so the script cannot fall
   back to the CWD-relative real lane):

   ```
   $ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /tmp/repro-census-start mori
   EXIT=0   16 W04, one mori ok; first 16 lines diff-equal to census-start.txt
   $ … --root /tmp/repro-census-scored mori     # SOURCES.md = 265a955 bytes
   EXIT=1   16 W04 + "mori	E12	S229 row outside Registry section"
   $ … --root /tmp/repro-census-current mori    # SOURCES.md = ede486b bytes
   EXIT=0   16 W04, one mori ok
   ```

   (An earlier attempt that passed a *relative* lane name to a temp root was
   discarded: `die` ran inside the `build_roster` subshell and the lane fell
   back to the CWD-relative real lane — it read current bytes, proving nothing.)

4. Revision facts (`git show <rev>:corpus/SOURCES.md | sha256sum`, `git log`):

   ```
   bb1f2457 2026-10-24T01:31:20-03:00  c993e977…
   265a955  2026-10-24T02:47:29-03:00  3418f0bb…  (S229 at line 292, after "## Leads (unopened)" at 285)
   8d3badd  2026-10-24T02:56:11-03:00  3418f0bb…  (unchanged)
   ede486b  2026-10-24T02:56:56-03:00  c9e8f039…  (HEAD; S229 at line 235 inside "## Registry")
   ```

   `git diff 265a955 ede486b -- corpus/SOURCES.md` is exactly a move: `+` the
   S229 row after S228 in the Registry, `−` the same row from the Leads tail.
   `census-end.txt` mtime is `2026-10-24 02:50:28 -0300` — **after** `265a955`
   (02:47:29) and **before** the repair commit (02:56:56). Worktree
   `corpus/SOURCES.md` equals HEAD (`git --no-optional-locks diff --quiet` → 0).

5. S229 warning-class check on current bytes:

   ```
   $ grep -c executionmodel.html corpus/SOURCES.md          → 1
   $ scripts/sources-census.sh shared --root … mori | grep -c executionmodel → 0
   $ test -e corpus/knowledge/conform-scope-r40.md          → exists
   ```

   S229 is absent from every W04 row; its URL is unique in mori and not
   shared across lanes; no W01–W03 exists in either receipt.

## Findings

**F1 — HIGH (receipt honesty / frontier attribution): census-end's exit 0 does
not hold at the scored tip.**
`census-end.txt` shows 16 W04 + `mori ok` (an exit-0 shape), but at the scored
tip `265a955` the same command on the same committed file exits 1 with
`E12 S229 row outside Registry section`. The receipt's mtime (02:50:28) sits
between the scored-tip commit and the repair commit `ede486b` (02:56:56), and
`ede486b` is a pure move of that row into `## Registry`. `[INFERENCE]` the
receipt measured the uncommitted repaired working tree. Consequence: the
contract's frontier "census exit 0" is true at `ede486b` (and at the entering
tip), **not** at the scored tip; the receipt cannot be tied to any revision.
Evidence: mirror runs in §3, `git diff 265a955 ede486b`, hashes/timestamps in §4.

**F2 — MEDIUM (receipt discipline): neither census receipt records its measured
revision or exit status.**
Both files name only the `SOURCES.md` path. Round-40's own C1/C2 receipt
discipline (wave-plan seat: "names its command, measured rev and exit code")
is not applied to the two frontier receipts. The start-side exit 0 is therefore
recoverable only by re-execution (`bb1f2457` bytes → 0, §3); the end-side 0 is
recorded solely in the separate `w1/ExeCensus.md` (whose mtime 03:00:20 is
post-repair, so it attests the repaired bytes).

**F3 — INFO (claim wording): "S229 adds no new warning class" is literally true
but escapes the failure.**
W-classes are unchanged ({W04} only, identical rows), yet at the scored tip the
same row added an **E12 error** and flipped the census to exit 1. A warning-only
comparison passes while the exit-0 frontier fails; the two statements must not
be quoted as mutually supporting without the revision named.

## Residual risk and verification gaps

- The tip reproductions use a `/tmp` mirror (synthetic one-line conf; current
  used-by tree symlinked; lane label `mori`). E11/E12/W04 are computed from file
  bytes only, and both tip mirrors were E11-clean, so the E12 delta is
  attributable to the row placement; the mirror is still not the real root, and
  a real-root rewind at `265a955` was not performed (would require mutating lane
  state, out of bounds).
- The exact uncommitted bytes measured at 02:50:28 cannot be recovered; the
  attribution to `ede486b` is inference from output shape, hash of HEAD bytes,
  timestamps, and the pure-move diff.
- No sibling reports were relied on except `w1/ExeCensus.md` (current-bytes
  confirmation); 110+ peer seats were running concurrently and were not audited.
- Checks not run: `sources-census.sh selftest` (not in seat scope) and any
  fleet-wide lane census beyond `mori` (fleet repo is read-only and this seat's
  claim is lane-scoped).

## Recommendation (advisory, not an admission)

Re-run the exact census command at the admitted tip, record revision + exit code
inside `census-start.txt`/`census-end.txt` (or a companion line), and treat
`ede486b` (or later) as the measured revision for the frontier's "census exit 0"
— otherwise the round-40 frontier line rests on bytes that never were the scored
tip.

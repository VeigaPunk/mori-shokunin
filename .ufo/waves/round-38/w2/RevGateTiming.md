# RevGateTiming — re-derive `supersede_timing` at f725f30

Seat: MoriR38.RevGateTiming (wave 2, falsify, C3 gate). Scope: run the gate, recover the
S069/S073 commit order independently, check the printed classification. Lane repo used
read-only; all git commands were `log`/`show`/`diff`/`merge-base`/`rev-parse`. No lane files
modified; no installs performed (nothing needed).

## Verdict: PASS — no actionable finding

The printed classification follows the independently observed commit order for both ids;
the timing line is present, singular, and positioned after the summary line.

## 1. Timing line (verbatim)

Command (run in `/home/vgpnk/Projects/shokunin/mori-shokunin`):

    python3 tools/mori-sources-appendonly.py f725f3076972e6e70595b5ac8279be524a111ff8 --round-base f10a320d

Output tail (exact):

    supersede_timing superseded_as_of=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] stale_supersede=[]

- Exactly one `^supersede_timing` line per run; it follows `PREDICATE` and the
  `appendonly_violations=...` summary (`main()` prints PREDICATE then `report()`;
  `tools/mori-sources-appendonly.py:580` and `:335-337`). The lone `P-C6:`-prefixed line
  above the report is the predicate echo, not a second timing line.
- Gate exit = 1 at the tip: documented `--round-base` semantics, exit 1 when
  `round_changed` is non-empty (`tools/mori-sources-appendonly.py:582-583`); round-38 data
  commit `daa1d4d` is in `f10a320d..f725f30`. Exit 1 is the expected "round changed the
  registry" signal, not a gate failure. Matches frozen `evidence/gate-after.txt`.
- Output at tip is byte-identical to `evidence/gate-after.txt`'s timing line; output at
  `e37dcc6` is byte-identical to `evidence/gate-after-e37dcc6.txt` (`EXIT=1` there too).

## 2. Commit-order evidence (re-derived, `git log` over `corpus/SOURCES.md`)

Per-row diffs (`git log -G'^\| *Snnn *\|' --reverse <tip> -- corpus/SOURCES.md`):

- S069 row touched twice: added `8f8c58e` (2026-10-21, round-20 sources commit),
  edited `62db24c01d5b7c2247f43852ea2b28d0ae5e40c8` (2026-10-22 23:55:24 -0300,
  "round-33: C1 FR6 entry, sources S180-S190, round-32 repair, QUALITY 97, wave-1 reports").
- S073 row landed once: `71abd41f9337412dc366ce605915c5e49edc94f2`
  (2026-10-21 08:18:17 -0300, "round-20: wave-2 falsification integrated ...").
- S226 row landed once: `daa1d4d2501e1671e7b7ff1fd60a069564f178b0`
  (2026-10-23 17:55:19 -0300, "round-38 data: S226 + ...").

Positions in `git log --format=%H --reverse f725f30 -- corpus/SOURCES.md` (the same list
the gate builds, `tools/mori-sources-appendonly.py:220-221`):

    index 11: 71abd41  (S073 lands, teaches opens "supersedes S069")
    index 42: 62db24c  (S069's last immutable-cell edit)
    index 52: daa1d4d  (S226 lands, teaches opens "supersedes S069")

`git merge-base --is-ancestor` chain: `8f8c58e` < `71abd41` < `62db24c` < `daa1d4d` < tip —
all YES, so the log index order coincides with the descendant relation on this linear lane.

Edit cell check: `git diff 62db24c^ 62db24c` on the S069 row changes only the `teaches`
cell ("…cannot see symlinks:" → "…cannot see symlinks: lane rule:"). `teaches` is immutable
(`MUTABLE = ("status","recheck","used-by")`, `tools/mori-sources-appendonly.py:63`), so
`62db24c` is a genuine immutable-cell edit and S069's `last_edit` index is 42.

Superseder landings (`supersede_landing`, `tools/mori-sources-appendonly.py:243,272-275`):
S069 acquires superseder S073 at index 11 and S226 at index 52; the gate keeps the maximum
index, so latest superseder = S226 (gate prints `changed S069 superseded_by=S226`).
`S073` at its landing already carried `supersedes S069` (verified in
`71abd41:corpus/SOURCES.md` line 79); `S226` carries it at tip (line 232).

## 3. Classification vs observed order

- At `f725f30`: landing index 52 (`daa1d4d`) > last-edit index 42 (`62db24c`) →
  S069 in `superseded_as_of`. Printed: `superseded_as_of=[...S069...] stale_supersede=[]`. **Agrees.**
- S073 itself is superseded by nothing (`superseded` list has no S073; the only
  `supersedes S069` rows are S073 and S226, and no row opens `supersedes S073`) →
  S073 correctly absent from both lists. Its *landing* (11 < 42) is what made S069 stale
  at the pre-S226 revision, which is what the control shows.
- Control at `e37dcc6` (S226 not yet present; `daa1d4d` is not an ancestor of `e37dcc6`,
  `62db24c` is; `S226` absent from `e37dcc6:corpus/SOURCES.md`):
  prints `superseded_as_of=[...17 ids, S069 absent...] stale_supersede=[S069]`, exit 1.
  With S073 as the then-latest superseder, landing 11 ≤ last-edit 42 → stale. This is the
  kill-rule discriminator: a presence-only gate would have listed S069 in
  `superseded_as_of` there (contract.md:108-110). **Agrees.**
- `--selftest` → `pass=9 fail=0`; the `supersede before edit` fixture asserts
  `stale_supersede=[S001]` and `superseded_as_of=[]` (`tools/mori-sources-appendonly.py:441-444`),
  and `superseding row` asserts `superseded_as_of=[S001]` (`:437-440`). P-C6's fixture
  claim holds.
- Landing == last-edit commit would classify stale (`landing > last_edit` is strict,
  `:286`); consistent with P-C6's "strictly later" wording.

## 4. Residual risk / verification gaps (observed, not actionable in-scope)

- P-C6 says "landing commit is a **descendant** of the last-edit commit"; the gate actually
  compares positions in `git log --reverse <rev> -- <path>` (`:285-289`). On the linear lane
  history the two coincide; on a merge DAG, a superseder landing on a parallel side branch
  could be indexed after the edit while not being a descendant — the selftest fixtures are
  all linear, so DAG order is untested. No defect on observed lane history.
- `supersede_landing` is history-wide, not tip-state: a superseding row whose `teaches` was
  later edited away or deleted still counts as the recorded landing. Not exercised at tip
  (both S073 and S226 rows still carry `supersedes S069`); could misclassify a contrived
  history. Beyond this seat's scope.
- Classification is defined only for superseded ids that are also in `ids` (edited).
  A superseded-but-never-edited id is silently absent from both lists — consistent with
  `superseded ⊆ ids` (`:277`), and no such id exists at tip (`superseded` == the 18 edited
  ids). By design, but worth noting as a semantic boundary.

## Evidence index

- Runs (this session, re-derived): `tools/mori-sources-appendonly.py` at `f725f30` and
  `e37dcc6` with `--round-base f10a320d`; `--selftest` (9/0).
- Commit order: `git log --format='%H %ad' --reverse f725f30 -- corpus/SOURCES.md`;
  `-G'^\| *S069 *\|'` / `S073` / `S226` per-row diffs; `git diff 62db24c^ 62db24c`;
  four `git merge-base --is-ancestor` checks; `git show <rev>:corpus/SOURCES.md` greps.
- Consistent with `evidence/gate-after.txt`, `evidence/gate-after-e37dcc6.txt` (verbatim).
- Contract basis: `.ufo/waves/round-38/contract.md:86-110` (P-C6, S069/S073/S226 narrative).
- No tool installs; no report-trailer discrepancies.

Report: .ufo/waves/round-38/w2/RevGateTiming.md

# Mo92S01Successors — round 92 wave w1 report

Entering revision: f63d1ab030d4179576e494342f48ef8718e497a5. Scope: corpus/SOURCES.md only (C2 successor rows S619, S620).

## 1. Pinned-copy digests (recomputed at f63d1ab0 from `git show <rev>:<path> | sha256sum`)

| pinned copy | measured sha256 | bytes | matches context? |
|---|---|---|---|
| .ufo/waves/round-90/w1/Mo90S01Sources/sources/python-ast-3.15.2.html | 7891c58897fe9f78cf16d15fd3464b746a187214c82587ac94b0f83b9a8a42f5 | 362493 | yes |
| corpus/evidence/sources-r42/S235.pdf | 9855a4986a312dfc946b1b97b6010a8e4f1e65a4a30dca99359e6df057ad8020 | 6482693 | yes |

Both match, so both rows were written.

## 2. Row shape and id checks

- Both row strings, split on `|`, give 13 fields (leading and trailing empty) = 11 cells. Zero literal pipes inside any cell.
- S619 and S620 do not appear anywhere in corpus/SOURCES.md at f63d1ab0 (`grep -c 'S619\|S620'` = 0).
- The teaches cell (8th split field) begins `supersedes S615 — ...` for S619 and `supersedes S235 — ...` for S620.
- Used-by cell of both rows is `corpus/lessons/round-92.md`; this path does not exist at f63d1ab0 (see section 4).

## 3. Append and row counts

- Scratch clone: `<scratch>/repo`, verified `git rev-parse --show-toplevel` = clone path, detached at f63d1ab0.
- Rows appended verbatim after the S618 row (line 400); `git diff --stat`: 2 insertions, 0 deletions.
- `grep -cE '^\| *S[0-9]{3,}'`: before = 391, after = 393.

## 4. Census validation (`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file <path>`, cwd = scratch clone so used-by paths resolve against the clone)

| run | exit | E-lines | E03/E04 |
|---|---|---|---|
| original SOURCES.md at f63d1ab0 | 0 | 0 | 0 |
| appended SOURCES.md (the deliverable) | 1 | 2 | 0 |
| appended + temporary stub `corpus/lessons/round-92.md` (scratch test only, removed after) | 0 | 0 | 0 |

The 2 new E-lines are `E11 S619 missing used-by corpus/lessons/round-92.md` and `E11 S620 missing used-by corpus/lessons/round-92.md`. The append adds no E03/E04 finding, as the contract requires; it does add E11 because the used-by target is not on disk at f63d1ab0. The rows will validate clean (exit 0) only in an integrated tree where `corpus/lessons/round-92.md` exists. The integrator must land that lesson file in the same integration as this patch, or the census exits 1. I did not create that file (not in this seat's writes). Warnings: the appended run adds two W04 lines (`S619`, `S620` duplicate URL across scopes), which do not change status.

Dead ends (not counted as checks): `--root <clone>` exits 2 because a clone of the mori lane has no `shokunin.conf`; file-mode run from a cwd other than the clone resolves used-by paths against that cwd and reports about 450 spurious E11 on the original file, so the cwd = clone form above is the valid one.

## 5. Patch

- Patch: `.ufo/waves/round-92/w1/patches/Mo92S01Successors.patch` (corpus/SOURCES.md only, 2 added lines, generated with `git -C <scratch>/repo diff f63d1ab030d4179576e494342f48ef8718e497a5 -- corpus/SOURCES.md`).
- Fresh clone (`git clone --shared` of the lane, detached at f63d1ab0): `git apply --check` exit 0; `git apply` then gives 393 rows, and the resulting file is byte-identical to the scratch clone (`cmp` exit 0).

## 6. Checks run, with exit codes

- sha256sum of both pinned copies: exit 0 (both match).
- `grep -c 'S619\|S620'` on f63d1ab0 registry: count 0.
- Row shape awk (NF = 13, pipes inside = 0): both rows ok.
- `sources-census.sh validate --file` on original (cwd clone): exit 0.
- `sources-census.sh validate --file` on appended (cwd clone): exit 1 (E11 x2, expected dependency above).
- Stub-lesson test (scratch only): exit 0.
- `git apply --check` in fresh clone: exit 0.

## 7. Rows not written

None. Both digests matched and both rows were written. The residual blocker is the E11 dependency in section 4.

## 8. Tooling

No tools installed or upgraded. pacman not used. No lane, fleet-root, shokuknow or sibling writes; the lane was read only. Scratch directory removed at the end of the seat.

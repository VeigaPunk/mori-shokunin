# C1 mutation attack — Mo57Revenger63

Seat: Mo57Revenger63 (revenger, round-57 wave w1). Target: frozen C1 counter
`.ufo/waves/round-57/count-c1.py` (sha256 `7156fb4bb29f27881091b22dfa7ef3d661b1e955a1ec9a4d13e48013f1b368ec`,
unchanged before/after every run). Contract read first: `.ufo/waves/round-57/contract.md`
(C1 predicate = two capability rows naming `driver-liveness` and `vote-binding`, *each with a resolvable
round-56 evidence pointer and first-working round 56*). No production, fleet, lane or git/jj mutation was made;
the lane repo was only read (`git show`, `grep`).

**Verdict: the frozen counter kills every mutation of the three named fields when the token occurs only in
that field, but it is a line-membership test, not a row test: 15 mutants that violate the frozen predicate's
own words still read `C1=met`, including two identical rows with no `vote-binding` row, unresolvable and
`..`-escaped evidence pointers, and junk rows outside any table. A correct landing in the lane's *current*
capabilities register reads `rows=0` (unmet).**

## Method (and the one disclosed instrumentation)

`count-c1.py:7` hard-codes `repo = "/home/vgpnk/Projects/shokunin/mori-shokunin"`, so no scratch revision is
observable without either editing the counter or redirecting that one path. I did neither to the frozen file:

- Fixture: `$SCRATCH/Mo57Revenger63/repo`, a scratch git repo whose `SCORECARD.md` is the byte content of
  `git show 618562c7…:SCORECARD.md` (freeze tip), asserted via `git rev-parse --show-toplevel`.
- Shim: `$SCRATCH/bin/git` rewrites **only** `git -C /…/mori-shokunin …` to the fixture; everything else
  passes through to `/usr/bin/git`. Identity proof: with `MUT_FIXTURE` set to the lane path itself, the shim
  run equals the direct run on both revisions (`logs/passthru.txt`):
  `rev=618562c7 direct rc=1 :: C1=unmet rows=0 evidence=bad rev=618562c7…` = shim, `EQUAL`.
- Cross-check that the redirect is not the cause: a copy of the counter differing in exactly **one** line
  (`repo = "<fixture>"`, `difflines_patched=1`) agrees token-for-token with the frozen bytes through the shim
  on three fixture revisions (`P0`, junk, register-only: `equal=True`).
- Base ("met") state = freeze SCORECARD with two rows replacing `| — none yet — | | | |` at
  `SCORECARD.md:600`, inside the first `## Capabilities` section (`SCORECARD.md:596`) which ends at
  `## Saturation` (`SCORECARD.md:604`). Tags are token-free so a name mutant removes the token:
  ```
  | driver-liveness | FR5 probe reads the watchdog driver file and reports `unclosed` pairing counts without any health verdict | `.ufo/waves/round-56/evidence/c1-at-freeze.txt` | 56 |
  | vote-binding | dual-shape seat-output binder re-binds round-55 RECHECK lines from plain text and from structured yields | `.ufo/waves/round-56/evidence/c2-at-freeze.txt` | 56 |
  ```
  Positive control: `C1=met rows=2 evidence=ok rev=35a8fd0c…`, rc 0.

## Killed mutations (counter rejects — field predicates hold)

| mutant | field changed | counter output | rc |
|---|---|---|---|
| P0 canonical | none (control) | `C1=met rows=2 evidence=ok` | 0 |
| M1 `driver-livness` | name, typo | `C1=unmet rows=1 evidence=bad` | 1 |
| M2 `Vote-Binding` | name, case | `C1=unmet rows=1 evidence=bad` | 1 |
| M3 `driver health` | name, renamed | `C1=unmet rows=1 evidence=bad` | 1 |
| M4 `vote_binding` | name, separator | `C1=unmet rows=1 evidence=bad` | 1 |
| M7 both tokens in one row | row multiplicity | `rows=1` | 1 |
| M10 `round-55/…driver-liveness-live.txt` | evidence path | `rows=2 evidence=bad` | 1 |
| M11 `` `.ufo/waves/round-56` `` (no slash) | evidence path | `rows=2 evidence=bad` | 1 |
| M16 `\| 55 \|` | first-working round | `rows=2 evidence=bad` | 1 |
| M17 `\| 56  \|` (extra space) | round, spacing | `rows=2 evidence=bad` | 1 |
| M18 `\| 156 \|` | round, digit injection | `rows=2 evidence=bad` | 1 |
| M19 `\| 056 \|` | round, zero pad | `rows=2 evidence=bad` | 1 |
| M21 row ends `\| 56` (no close pipe) | round cell | `rows=2 evidence=bad` | 1 |
| M22 third matching row | multiplicity | `rows=3 evidence=bad` | 1 |
| M24 rows only in the current register | placement | `rows=0 evidence=bad` | 1 |
| M27 `## Saturation` line above the rows | window end | `rows=0 evidence=bad` | 1 |
| M29 first header renamed `## Capability register` | window start | `rows=0 evidence=bad` | 1 |
| M30 revision `0…0` (absent) | failure path | `C1=unmet rows=0 evidence=bad` (**no `rev=` token**) | 1 |
| M31 `SCORECARD.md` deleted at rev | failure path | `C1=unmet rows=0 evidence=bad` (**no `rev=` token**) | 1 |

## Survivors (counter prints `C1=met`, rc 0; the frozen predicate says otherwise)

| # | mutation | why it must fail | counter output |
|---|---|---|---|
| S1 | M5 name `driver-liveness-probe` | row does not *name* `driver-liveness`; token is a substring of a longer name | `met rows=2` |
| S2 | M6 name cell `watchdog probe`, token only in the description cell | no row *naming* the capability | `met rows=2` |
| S3 | M6b name cell `driver health` **and** evidence `.ufo/waves/round-56/evidence/driver-liveness-live.txt` | the name field is unconstrained when any other cell carries the token — and the *real* round-56 artifact is named `driver-liveness-live.txt` | `met rows=2` |
| S4 | M8/M9 two identical `driver-liveness` rows, **no `vote-binding` row** | predicate requires one row per name; `rows == 2` is satisfied by any two matching lines | `met rows=2` |
| S5 | M12 evidence `` `.ufo/waves/round-56/does-not-exist-9f2a.txt` `` | predicate: *resolvable* round-56 pointer | `met rows=2` |
| S6 | M13 evidence `` `.ufo/waves/round-56/../round-55/tally-r55.txt` `` | resolves into round-55, not a round-56 artifact | `met rows=2` |
| S7 | M14 evidence path moved into the "What it can now do" cell; Evidence cell `—` | predicate: each row carries the pointer in its evidence column | `met rows=2` |
| S8 | M15 junk rows `\| junk-a \| driver-liveness demo placeholder \| `.ufo/waves/round-56/no-such-evidence-a` \| 56 \|` (+ `junk-b`) | names are `junk-a/junk-b`, pointers do not exist | `met rows=2` |
| S9 | M20 `\| driver-liveness \| … \| … \| 55 \| 56 \|` (5 cells) | first-working round is 55; `56` sits in an extra cell | `met rows=2` |
| S10 | M23 both rows with empty "What it can now do" | row says nothing about what the capability does | `met rows=2` |
| S11 | M25 both rows inside a ```` ```text ```` fence | fenced text is not a table row | `met rows=2` |
| S12 | M26 both rows inside `<!-- … -->` | commented-out text is not a row | `met rows=2` |
| S13 | M28 first `## Saturation` renamed `## Capacity saturation line` | window end moves; the section silently extends | `met rows=2` (still correct rows) |
| S14 | M32 renamed end anchor **and** junk rows placed in the round-12 section | rows outside the intended table are then counted | `met rows=2` |
| S15 | M33 junk rows as bare `\|`-prefixed paragraph lines, blank line above, no separator row | not a markdown table at all | `met rows=2` |

Junk-row demonstration (predicted by `Mo57MutationTester38` from code, **now executed**): S8/S15.
Inside-table and outside-table forms both read `met` (`M33-rows-outside-table rc=0`, `M33b-rows-inside-table rc=0`).

## Divergences from the frozen predicate, with exact lines

1. **No resolvability** (`count-c1.py:11-12`): `ok` is true iff exactly two `|`-prefixed lines in the window
   contain a token, contain `.ufo/waves/round-56/` and contain the literal `| 56 |`. Nothing stats a path,
   nothing checks a cell position, nothing checks the two names are distinct. Evidence: S5, S6, S7, S8.
2. **`evidence=` is not an independent arm** (`count-c1.py:13-14`): `ok` is computed once and printed twice, so
   `evidence=ok` carries no information beyond `C1=met`. Every killed mutant that kept `rows=2` shows
   `rows=2 evidence=bad` (M10/M11/M16…); no run produced `rows=2 evidence=ok` failing the verdict.
3. **Window start is the superseded table** (`count-c1.py:10` + `SCORECARD.md:596-604`): the counter reads the
   first `## Capabilities` section, which is the `— none yet —` table, while `SCORECARD.md:1958` states the
   round-35 register "supersedes the `— none yet —` table in the first `## Capabilities` section". So M24 —
   rows added to the register that the lane itself calls current — reads `rows=0`, unmet. [INFERENCE] A wave
   scribe following `SCORECARD.md:1953-1958` will land in the register and can read unmet while the claim is
   correctly recorded; the reverse (rows only in the superseded table) reads met.
4. **Anchor is a literal substring anywhere, including prose**: after deleting every `## Capabilities` header
   line (M34), the split still found a `## Capabilities` occurrence quoted in prose at `SCORECARD.md:1958` and
   returned `C1=unmet rows=1 evidence=bad` — the window silently became a different section. Rejection happened,
   but for the wrong region, not because the header was missing.
5. **Failure path drops `rev=`** (`count-c1.py:8-9`): a missing SCORECARD or an absent revision prints
   `C1=unmet rows=0 evidence=bad` with no revision token, unlike every measured control line in
   `.ufo/waves/round-57/controls.txt`. A consumer parsing `rev=` sees no revision on that path.

## What the wave must do to read `met` (frozen predicate unchanged)

Rows must sit between `SCORECARD.md:596` (`## Capabilities`) and `SCORECARD.md:604` (`## Saturation`), one row
per name, each row containing the exact tokens `driver-liveness` / `vote-binding` in any cell, the literal
substring `.ufo/waves/round-56/`, and exactly one `| 56 |` cell with single spaces. Because the counter cannot
tell a junk landing from a real one (S8, S15), a `met` reading is necessary but not sufficient evidence for the
contract's C1 predicate: resolvability, per-name distinctness and column placement need a manual read of the
landed diff.

## Coverage and confidence

35 mutants + 1 positive control + 2 failure paths + 1 anchor-hijack probe, all executed against frozen bytes;
16 killed, 15 predicate-violating survivors, 2 fail-closed, 1 misfire-by-anchor, 1 duplicate-of-junk contrast.
Confidence: **high** for every observed output line (each is a stored run in `$SCRATCH/Mo57Revenger63/logs/`);
**high** for divergences 1, 2, 4, 5 (direct line evidence); **inference** for the wave-behaviour consequence in
divergence 3. Not tested: SCORECARD content after this wave lands (out of seat scope), CRLF/multibyte edge
encodings, and the C2 counter (other seats).

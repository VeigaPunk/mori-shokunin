# ExecCollisionGuard — wave w1 report (round 47)

Seat: `ExecCollisionGuard` (executor, leaf; no subagent dispatch used).
Skill: `/skill:godspeed` (read). Addendum §10 = the "Id collision check in scratch, before any
append" item in `.ufo/prompts/mori-round-47.md` §6/§10 (verbatim same text as
`chousa-round-42.md` §10): the census parser accepts rows with 0–3 leading spaces, so the
extractor must too; a column-zero-only pattern false-greens an indented collision.

All commands ran from the lane root
`/home/vgpnk/Projects/shokunin/mori-shokunin` (or the scratch dir). Scratch only:
`/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r47-ExecCollisionGuard/`.
No lane or production files were modified. No tools installed or updated (only coreutils
`grep`/`sort`/`comm`/`diff`/`wc` already present; nothing to record in the tooling ledger).

## 1. Scratch proof of the indented-row collision guard

Fixtures (written with `printf`; `cat -A` receipts):

```
$ cat -A reg.fixture.txt
| S001 |$
  | S002 |$
$ cat -A staged.fixture.txt
| S002 |$
```

Registry rows: `| S001 |` (column 0) and `  | S002 |` (two leading spaces — census-valid per
the 0–3-space clause). Staged file: `| S002 |` (column 0).

### 1a. 0–3-space pattern: `grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}'`

```
$ grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' reg.fixture.txt
| S001
  | S002
$ grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' staged.fixture.txt
| S002
```

Extraction + `comm -12`:

```
$ grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' reg.fixture.txt | grep -oE 'S[0-9]+' | sort > reg-ids.fix
$ grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' staged.fixture.txt | grep -oE 'S[0-9]+' | sort > staged-ids.fix
$ comm -12 reg-ids.fix staged-ids.fix | tee collisions.fix
S002
$ test -s collisions.fix && echo 'NONEMPTY COLLISIONS (S002 caught)'
NONEMPTY COLLISIONS (S002 caught)
```

Verdict: the 0–3-space guard catches the indented-row collision (nonempty `collisions` = S002).

### 1b. Column-zero-only pattern: `grep -oE '^\|[[:space:]]*S[0-9]{3,}'`

```
$ grep -oE '^\|[[:space:]]*S[0-9]{3,}' reg.fixture.txt
| S001
$ grep -oE '^\|[[:space:]]*S[0-9]{3,}' staged.fixture.txt
| S002
$ grep -oE '^\|[[:space:]]*S[0-9]{3,}' reg.fixture.txt | grep -oE 'S[0-9]+' | sort > reg-ids.col0
$ grep -oE '^\|[[:space:]]*S[0-9]{3,}' staged.fixture.txt | grep -oE 'S[0-9]+' | sort > staged-ids.col0
$ comm -12 reg-ids.col0 staged-ids.col0 | tee collisions.col0
$ test -s collisions.col0 && echo NONEMPTY || echo 'EMPTY (column-zero-only MISSES S002 -> false green)'
EMPTY (column-zero-only MISSES S002 -> false green)
```

Verdict: the column-zero-only `^\|` pattern has no match on the indented `  | S002 |` row, so
the registry extraction drops S002 and `comm -12` is empty — a false green. This reproduces the
addendum's asserted failure mode exactly.

## 2. Real check against the lane registry and the staged append file

Commands (mirroring addendum §10, with mori paths):

```
S=/home/vgpnk/Projects/shokuknow
A=/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-47/assimilation
grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md \
  | grep -oE 'S[0-9]+' | sort > reg-ids.real
grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' "$S/merge/mori/SOURCES.append.md" \
  | grep -oE 'S[0-9]+' | sort > staged-ids.real
comm -12 reg-ids.real staged-ids.real > collisions.real
```

### 2a. Staged ids (from `/home/vgpnk/Projects/shokuknow/merge/mori/SOURCES.append.md`)

`staged-ids.real` has **136 ids**, S471–S606; `diff staged-ids.real "$A/staged-ids"` is empty —
**identical to the committed staged-ids**. Full list (sorted):

```
S471 S472 S473 S474 S475 S476 S477 S478 S479 S480 S481 S482 S483 S484 S485 S486
S487 S488 S489 S490 S491 S492 S493 S494 S495 S496 S497 S498 S499 S500 S501 S502
S503 S504 S505 S506 S507 S508 S509 S510 S511 S512 S513 S514 S515 S516 S517 S518
S519 S520 S521 S522 S523 S524 S525 S526 S527 S528 S529 S530 S531 S532 S533 S534
S535 S536 S537 S538 S539 S540 S541 S542 S543 S544 S545 S546 S547 S548 S549 S550
S551 S552 S553 S554 S555 S556 S557 S558 S559 S560 S561 S562 S563 S564 S565 S566
S567 S568 S569 S570 S571 S572 S573 S574 S575 S576 S577 S578 S579 S580 S581 S582
S583 S584 S585 S586 S587 S588 S589 S590 S591 S592 S593 S594 S595 S596 S597 S598
S599 S600 S601 S602 S603 S604 S605 S606
```

### 2b. Registry ids (from `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md`)

`reg-ids.real` has **250 ids**, S001–S477. Versus the committed `$A/reg-ids` (247 ids, ending
S474), the only difference is the appended tail — `diff` shows exactly:

```
248,250d247
< S475
< S476
< S477
```

Registry tail (re-derived):

```
S470 S471 S472 S473 S474 S475 S476 S477
```

### 2c. Collisions

```
$ comm -12 reg-ids.real staged-ids.real > collisions.real
$ cat collisions.real
S471
S472
S473
S474
S475
S476
S477
```

**Live collision count: 7** (S471–S477).

### 2d. Comparison with the reference `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-47/assimilation/collisions`

```
$ diff "$A/collisions" collisions.real
4a5,7
> S475
> S476
> S477
```

- The **reference file (committed at freeze 63eecf)** holds exactly `S471 S472 S473 S474` — the
  first four of the live result are byte-identical to it. At freeze, the registry ended at S474
  (`git show 63eecf:corpus/SOURCES.md` has **zero** rows matching `^ {0,3}\|…S475`), so
  freeze-time collisions = S471–S474, matching the reference exactly.
- The live run additionally finds **S475, S476, S477** because the lane's registry **moved after
  the freeze**: the working-tree `corpus/SOURCES.md` now contains rows S475/S476/S477 (the C2
  source row, the emitter-copy row, and the host own-work row — integrated mid-wave; `git status`
  shows `corpus/SOURCES.md` modified since 63eecf). This is exactly the "lane registry keeps
  moving after the package was built" hazard §10 warns about; the guard correctly flags the new
  intersections. The staged set did not move (2a: identical).

### 2e. Collision count and renumber map (by document, never arithmetic)

Freeze-time colliding staged ids and their adopted continuation (registry continues at S475 by
document — URL/anchor is the evidence, the id follows it):

| staged id | adopted id |
|---|---|
| S471 | S475 |
| S472 | S476 |
| S473 | S477 |
| S474 | S478 |

Live caveat (observed, not papered over): because the registry has already reached S477 from this
round's own integration, the mapped ids S475/S476/S477 currently intersect the live registry too.
The intersecting live rows are this round's own C2 rows (S475 = `include/trace/events/oom.h` at
v7.2, S476 = emitter copies, S477 = host tracefs own-work), i.e. the same documents the staged
rows S471–S473 represent; adoption is a document-identity decision for the L1, not arithmetic.
The guard's job — proving no *hidden* collision is missed — is satisfied: the 0–3-space pattern
sees every census-valid row, the column-zero-only pattern demonstrably does not, and the live
comm output is nonempty as required before any append.

## 3. Evidence summary

- Scratch guard proof: 0–3-space pattern → nonempty collisions (S002); column-zero-only `^\|`
  → empty (false green). Both reproduced with exact commands/outputs above.
- Real check: staged-ids identical to committed; live collisions = S471 S472 S473 S474 S475
  S476 S477 (7); reference file = S471–S474 (4), byte-identical subset; delta = +S475/S476/S477
  from the post-freeze registry advance (verified: committed SOURCES.md has 0 S475 rows, working
  tree has 1+ and ends registry at S477).
- No tools installed/updated; no production files touched; no git/jj mutations; nothing run in
  `/home/vgpnk/Projects/shokuknow` beyond read-only `grep` over the staged append bytes.
- Risks/notes: the freeze-time reference `collisions` is stale relative to the live registry once
  this round's rows land; the L1 should regenerate `reg-ids`/`collisions` at append time (the
  tool exists and is shown working). UNVERIFIED: nothing in this seat required a network read or
  a lane-tool run (no TMPDIR use needed).

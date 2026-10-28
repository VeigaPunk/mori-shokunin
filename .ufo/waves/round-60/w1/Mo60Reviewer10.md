# Mo60Reviewer10 — absent-set truth matrix (round 60, w1)

Scope: verify `.ufo/waves/round-60/evidence/r59-absent-set.md` rows against
`git cat-file -e` truth at the three required revisions, and report any
disagreement. Read-only on the lane; no commits, no VCS mutation, no
fleet/sibling writes. All work under
`/fast/scratch/hyaku/mori-r60/Mo60Reviewer10/`, cleaned before yield.

Revisions used (pinned, never working-tree reads):

| label | revision | note |
|---|---|---|
| R59_DATA | `7b86704d7c0754a09958d131b64dbfa2a6d3eaed` | frozen r59 data rev (2026-10-28 03:00:51 -03) |
| LANDING | `f091bd773c4cfec8877061c84f4bae5f11e8bbe5` | seat-specified middle rev (07:42:42 -03) |
| R (tip) | `b3c256138f00c704d5aa56eb0332d74506502ef2` | current lane tip; stable for the whole seat |
| freeze (ref) | `ac496c7cde8cad965079858accae3bedfe4a73f2` | amendment-2 freeze (12:45:48) |
| entering (ref) | `ddfb12fb0838b4307c445194a844f0c4b1950195` | contract entering rev |

## Verdict

**No disagreement.** All 5 rows × 2 rev cells match `cat-file` truth at the
required revisions; all 5 dispositions match the frozen rule; all 5
landing-pointer cells match per-file add/modify history. The table is a
5-row × 5-cell table (contract §C1 line 51), byte-identical at its landing
commit `398d3225` and at tip (`blob 23251de7…`), and the frozen counter
reports `C1=met … absent-set=5/5` at tip, exit 0.

Four claim-precision / instrument findings follow (§Findings), none of which
makes a table cell false.

## Truth matrix (command + output)

```
L=/home/vgpnk/Projects/shokunin/mori-shokunin
for rev in 7b86704d… f091bd77… b3c25613…; do
  for n in Mo59Executor40 Mo59MutationTester31 Mo59MutationTester32 \
           Mo59Critic29 Mo59Reviewer16; do
    git -C "$L" cat-file -e "$rev:.ufo/waves/round-59/w1/$n.md" && PRESENT || ABSENT
```

| name | 7b86704d | f091bd77 | b3c25613 (tip) | table at-data | table at-tip | table disposition |
|---|---|---|---|---|---|---|
| Mo59Executor40 | ABSENT | PRESENT | PRESENT | absent ✓ | present ✓ | late-committed ✓ |
| Mo59MutationTester31 | ABSENT | PRESENT | PRESENT | absent ✓ | present ✓ | late-committed ✓ |
| Mo59MutationTester32 | ABSENT | PRESENT | PRESENT | absent ✓ | present ✓ | late-committed ✓ |
| Mo59Critic29 | ABSENT | PRESENT | PRESENT | absent ✓ | present ✓ | late-committed ✓ |
| Mo59Reviewer16 | ABSENT | PRESENT | PRESENT | absent ✓ | present ✓ | late-committed ✓ |

Extra pinning: all five are also PRESENT at `ac496c7c` (freeze) and
`ddfb12fb` (entering), so the "present" cell holds for every R from
`f091bd77` forward, not only for today's tip. No path variant exists: at
`7b86704d`, `ls-tree -r` finds **zero** occurrences of any of the five names
anywhere in the tree.

Landing-pointer cells, verified per file (`git log --diff-filter=A` /
`--diff-filter=M`):

```
Mo59Executor40        A f091bd77 07:42:42   (absent at bf6c0ad3)
Mo59MutationTester31  A f091bd77 07:42:42   (absent at bf6c0ad3)
Mo59MutationTester32  A bf6c0ad3 03:12:38,  M f091bd77
Mo59Critic29          A bf6c0ad3 03:12:38
Mo59Reviewer16        A bf6c0ad3 03:12:38
```

Filing reference (needed to test the table's pre-/post-filing labels) is the
**fleet** commit `9e9973ed` = 2026-10-28 03:13:02 -03 ("mori round-59
attempt-2 report"). Therefore `bf6c0ad3` (03:12:38) is 24 s **pre-filing**
and `f091bd77` (07:42:42) is **post-filing** — the cells' labels are correct.
`bf6c0ad3` is *not* an ancestor of `7b86704d`; `7b86704d` *is* an ancestor of
`f091bd77`.

Corroboration at tip with the frozen counter (sha
`795c1f3193a76406a40561ac60fedb3eee75fc38df2b2efb3fc5295d617ddbae`,
matching the contract §C3 pin):

```
$ python3 .ufo/waves/round-60/count-c1.py b3c25613… --scratch …
C1=met dead-uncorrected=0 receipts=2/2 absent-set=5/5 lesson=ok rev=b3c25613…
exit=0
$ python3 .ufo/waves/round-60/count-c1.py --selftest
C1_SELFTEST pass=6 fail=0
exit=0
```

## Findings

### F1 (medium) — the landing-pointer column is not gated at all

`parse_absent_table` requires 5 cells but keeps only three:
`count-c1.py:108` (`len(cells) != 5` → skip) and `count-c1.py:117`
(`rows[cells[0]] = (cells[1], cells[2], cells[3])`). `cells[4]` — the
landing pointer, the only cell carrying the pre-/post-filing and
"lesson claim was wrong" substance — is discarded and never compared with
git. This matches the letter of contract §C1 lines 50–56 (which binds only
the two rev cells + disposition), but C1 is framed as a *pointer-honesty*
claim, so its most pointer-dense surface is un-gated. I verified all five
landing cells by hand; they are correct today (see matrix above).

### F2 (medium) — lesson gate is document-level co-occurrence, not per-name binding

Contract §C1 lines 56–58 require the lesson to name "every late-committed
name **with** landing pointer `f091bd77`". The counter implements:

```
count-c1.py:224   if not (name in lt and "supersedes" in lt)
count-c1.py:228   if not (name in lt and R59_LANDING[:8] in lt)
```

Both test the name anywhere **and** the token anywhere — not the pairing.
Demonstrated in a sandbox clone (toplevel asserted = clone path):

```
MUT-B: deleted "in `f091bd77`" from the Mo59MutationTester31 bullet and
       deleted "supersedes" from the Mo59Critic29 bullet only
$ count-c1.py c8f04e4e… --repo <clone> --scratch …
C1=met dead-uncorrected=0 receipts=2/2 absent-set=5/5 lesson=ok rev=c8f04e4e…
exit=0
```

Related truth: in the real lesson the `Mo59Critic29` and `Mo59Reviewer16`
bullets (`corpus/lessons/round-60.md:50-54`) carry no `f091bd77` — their true
pointer is `bf6c0ad3`. So the clause is not literally satisfiable per-name
without writing a false pointer for three of five names; the table's own
bottom note (lines 17–19) documents this grammar collision. That is honest,
but the passing verdict rests on the lenient check, not on per-name
attribution.

### F3 (low) — `late-committed` has no discriminating power on this data

At `7b86704d` the entire `.ufo/waves/round-59/w1/` directory does not exist
(`ls-tree` → 0 `.md` files), so *any* name in the frozen set is `absent` and
therefore forced to `late-committed`. The `wrong-superseded` branch is
exercised only by the counter selftest (`count-c1.py:268`), never by real
r59 data. The absent-set arm therefore verifies internal consistency with a
trivial truth; it cannot distinguish "actually late" from "merely absent at
a pre-integration rev".

### F4 (low) — "filing" is never pinned inside the lane

The table and lesson both use pre-/post-filing qualifiers but name no filing
commit; the referent is fleet `9e9973ed` in a *different* repo, so a lane-only
reader cannot check them (I resolved it from
`/home/vgpnk/Projects/shokunin`). Wording inside the table's bottom note is
also looser than its own cells: the note says Critic29/Reviewer16 were
"committed at filing time in `bf6c0ad3`", while the cells correctly say
"pre-filing" (`bf6c0ad3` is 24 s before `9e9973ed`). Not a false cell.

### F5 (informational) — r59 report's "62 present / 3 missing" reconciles

Fleet report `9e9973ed:.ufo/reports/round-59/mori.md:74-75` says "62 report
files present at filing (missing: Mo59Executor40, Mo59MutationTester31,
Mo59MutationTester32 — partial)". Counts verified: `bf6c0ad3` (lane state at
filing) has **62** `w1/*.md`; only E40 and MT31 are absent; MT32 is present
but working-tree-modified. So 62 on disk + 2 true absences = 64, with MT32
counted as partial. The table's note ("correct about which files were late,
not about the count") is a fair reading, though the report's own arithmetic
is only coherent when "partial" is read as a third bucket. 64 `.md` at tip.

## Augmentation/liveness evidence (sandbox, read-only on lane)

Sandbox: `git clone --shared` of the lane into
`/fast/scratch/hyaku/mori-r60/Mo60Reviewer10/clone`
(`git rev-parse --show-toplevel` = clone path; all writes via `git -C $D`).

| mutant | change | counter result |
|---|---|---|
| MUT-A `ccf2cdf1` | Critic29 row → `present` / `wrong-superseded` | `C1=unmet absent-set=4/5 failed=absent_row:Mo59Critic29` exit 1 |
| MUT-B `c8f04e4e` | MT31 pointer + Critic29 `supersedes` removed per-name | **`C1=met … lesson=ok` exit 0 (gate miss, see F2)** |
| MUT-C `92049697` | Reviewer16 at-tip cell → `absent` | `C1=unmet absent-set=4/5 failed=absent_row:Mo59Reviewer16` exit 1 |
| MUT-D `1ffa2af6` | Executor40 disposition → `wrong-superseded` | `C1=unmet absent-set=4/5 failed=absent_row:Mo59Executor40` exit 1 |

MUT-A/C/D show cells 1–3 are independently enforced and non-vacuous;
MUT-B shows the lesson arm is not.

## Residual risk

- The absent-set arm scores a table whose at-data column is trivially all
  `absent` (F3); a future round should pick a data rev that post-dates the
  w1 commit, or add a `present-at-data` name, if `wrong-superseded` is meant
  to be demonstrated on real data.
- Landing-pointer truth is maintained by hand today (F1); any later edit to
  that column would be undetected.
- The lesson clause as written cannot be satisfied per-name for
  Critic29/Reviewer16/MT32 without a false pointer (F2); the table note
  documents this, but the frozen predicate should be re-worded (pointer map,
  not a single token) before it is reused.

## Verification gaps

- The `f091bd77` column exists only in this matrix, not in the table; the
  table is correct without it, but the seat's third-rev requirement is
  satisfied only by this review, so future scoring at `f091bd77` relies on
  the table's "present" cell (true, since `f091bd77` is an ancestor of every
  later R).
- Pre-/post-filing was resolved against the fleet repo; if the fleet ref is
  rewritten, the labels become unverifiable from the lane (F4).
- I did not re-run `count-c2`/`count-c3`; out of this seat's scope.

## Scratch hygiene

`/fast/scratch/hyaku/mori-r60/Mo60Reviewer10/` (clone + per-mutant scratch
dirs) removed after extracting the outputs above; `/tmp` used only for the
one 1.5 KB table copy (`/tmp/abs-tip.md`), never as evidence. Lane working
tree left untouched; the untracked `.ufo/waves/round-60/{c1-at-data.txt,
w1.ready, w1.ready.dispatched, w1/}` entries belong to other seats and were
not modified.

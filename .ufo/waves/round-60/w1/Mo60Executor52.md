# Mo60Executor52 — r59 count-c2 at 7b86704d: exact stdout bytes, rc, determinism

Seat scope (verbatim): "same for the r59 count-c2 at 7b86704d7c0754a09958d131b64dbfa2a6d3eaed:
exact stdout bytes + rc, run twice under different scratch dirs to show determinism."
Read-only on the lane. No lane VCS mutation, no commits, no fleet/sibling writes, no installs.

## Verdict

The committed receipt `.ufo/waves/round-60/evidence/r59-c2-met.txt` is a **genuine fresh
re-derivation**: five independent executions (four distinct scratch roots, three distinct cwds,
two distinct repositories) produce byte-identical stdout — 141 bytes, single LF-terminated line,
sha256 `4859d5ca7226aad23ab97b537b6c75ca1c73449ba7fc98211079cc2fb6caecb7`, stderr empty, rc 0 —
and that byte string `cmp`s equal to the committed receipt. Six falsification arms confirm the
`C2=met` line is data-derived, not an echo: mutating a cited byte flips the specific arm that owns
it (`entry`, `tool_sha`, `rows`, `trees`), while a whitespace change in a non-pinned cell leaves
`C2=met` intact.

## Revision pins used

| Role | Revision |
|---|---|
| r59 data revision (counter input, `rev=` in output) | `7b86704d7c0754a09958d131b64dbfa2a6d3eaed` |
| Round-60 freeze | `ac496c7cde8cad965079858accae3bedfe4a73f2` |
| Round-60 entering revision | `ddfb12fb0838b4307c445194a844f0c4b1950195` |
| Lane tip as observed during this seat | `b3c256138f00c704d5aa56eb0332d74506502ef2` |
| Receipt landed at | `398d3225` (subject: "round-60: land C1 data — r59 met receipts at 7b86704d, …") |

## Counter bytes executed (pinned provenance)

```
$ git -C <lane> show 7b86704d7c0754a09958d131b64dbfa2a6d3eaed:.ufo/waves/round-59/count-c2.py > $S/bin/count-c2-r59.py
2df3ae84f6d66f9ee46cd46cf2cb199ca85e7400301c5a0e9dd94b7b375877be  $S/bin/count-c2-r59.py
17744 bytes
```

Same sha256 `2df3ae84…877be` at `7b86704d…`, `ddfb12fb…`, `398d3225`, `b3c25613`, and equal to the
lane working-tree `.ufo/waves/round-59/count-c2.py` — one unambiguous counter blob for the whole
window, so "the committed r59 counter" is not revision-ambiguous here.

Tool pin cross-check at the data revision:

```
$ git -C <lane> show 7b86704d…:tools/mori-settlement-scan.py | sha256sum
4c04bf2170b0484192dd157ee04851e8243e030c54046c5e8806d46eea5ac9a9  -
```

equals the counter's `PIN` constant and the `4c04bf21…ac9a9` sha named in the round-60 contract (C2/H5).

## Exact command and exact output

```
cd /fast/scratch/hyaku/mori-r60/Mo60Executor52
TMPDIR=$S/<run>/tmp python3 $S/bin/count-c2-r59.py \
  7b86704d7c0754a09958d131b64dbfa2a6d3eaed \
  --repo <lane|$S/clone> --scratch $S/<run>/scratch
```

stdout, exactly (one line, 141 bytes incl. trailing `\n`; tail bytes `… 6 d 3 e a e d \n`):

```
C2=met selftest=ok scan=ok drift=ok trees=ok entry=ok rows=ok pins=ok tree=ok claims=13 files=6 rev=7b86704d7c0754a09958d131b64dbfa2a6d3eaed
```

| Run | Scratch root | cwd | `--repo` | rc | stdout bytes | stdout sha256 | stderr |
|---|---|---|---|---|---|---|---|
| run1 | `$S/run1/scratch` | `$S` | lane (`…/mori-shokunin`) | 0 | 141 | `4859d5ca…6caecb7` | 0 B |
| run2 | `$S/run2/scratch` | `$S` | lane | 0 | 141 | `4859d5ca…6caecb7` | 0 B |
| run3 | `$S/run3/scratch` | `$S` | `$S/clone` (shared clone, HEAD `b3c25613`) | 0 | 141 | `4859d5ca…6caecb7` | 0 B |
| run4 | `$S/run4/scratch` | `$S` | `$S/clone` (after 6 fixture commits) | 0 | 141 | `4859d5ca…6caecb7` | 0 B |
| run5 | `$S/run5/scratch` | `$S` | `$S/clone` (after 6 fixture commits) | 0 | 141 | `4859d5ca…6caecb7` | 0 B |

`cmp run1/out.txt run2/out.txt`, `… run3`, `… run4`, `… run5` → all identical. `run3` wall time
193 ms, `run4` 225 ms. `run1` inventory: 86 materialized files; `run2` inventory: 86 files; the two
relative-path inventories `diff` clean (SAME INVENTORY) — the counter wrote only under its own
`--scratch` root, plus `st2/` selftest fixtures written by the tool it invoked.

Receipt equality:

```
$ cmp $S/run1/out.txt <lane>/.ufo/waves/round-60/evidence/r59-c2-met.txt && echo BYTE-EQUAL
BYTE-EQUAL          # receipt: 141 bytes, sha256 4859d5ca7226aad23ab97b537b6c75ca1c73449ba7fc98211079cc2fb6caecb7
```

Receipt presence/identity across revisions (proves it landed during w1, not back-dated):

| Revision | `r59-c2-met.txt` |
|---|---|
| `7b86704d…` | ABSENT |
| `ddfb12fb…` (entering) | ABSENT |
| `398d3225` | present, sha256 `4859d5ca…6caecb7` |
| `b3c25613` (tip) | present, sha256 `4859d5ca…6caecb7` |

## Falsification arms (the met line is derived, not printed)

Fixture repo: one `git clone --shared --no-checkout` at `$S/clone` (toplevel asserted with
`git -C $S/clone rev-parse --show-toplevel` before every mutation); each mutation is one blob swap
plus `commit-tree -p 7b86704d…`, all via `git -C`. Lane untouched (see below).

| Arm | Mutation (base `7b86704d…`) | Fixture rev | rc | stdout tail | Owned arm |
|---|---|---|---|---|---|
| A | entry K1 quote ` "seats": 74,` → ` "seats": 73,` | `7d9559b9f8828c9840d2e127bc1f89b0eaf03c0c` | 1 | `… entry=bad … claims=13 files=6 rev=7d9559b9… failed=entry` | span/entry |
| B | `tools/mori-settlement-scan.py` +1 byte after shebang | `318e546d8ba417df8d28c2f9e9fa58d7c973cdbd` | 1 | `… all tokens ok … failed=tool_sha` | pin |
| D | `corpus/SOURCES.md` S553 row: `| S553 |` → `| S553  |` | `5ea955635931024d6f5284f8532e33bd18d72b1a` | 0 | `C2=met … rev=5ea95563…` (only `rev` differs) | no-false-positive control |
| E | S553 used-by cell `…artifacts-r59.md` → `…artifacts-r58.md` | `70a4c967327847554ba900338b69b6a3f394a2d4` | 1 | `… rows=bad … failed=rows` | rows |
| F | `trees-c2/t03-quote-wrong-line/expect.txt` `span` → `pin` | `63905603d31ff9d6d96733120d356db840572a80` | 1 | `… trees=bad … failed=tree:t03-quote-wrong-line:reasons,trees` | trees |
| G | tool blob prefixed with a marker write to `$TMPDIR/MORI-R59-EXEC-MARKER` | `93d3febd8eee1f6f671495fb10c0ead760a5a968` | 1 | `… selftest=ok scan=ok … failed=tool_sha` | execution boundary |

Arm A exact stdout:
`C2=unmet selftest=ok scan=ok drift=ok trees=ok entry=bad rows=ok pins=ok tree=ok claims=13 files=6 rev=7d9559b9f8828c9840d2e127bc1f89b0eaf03c0c failed=entry`

Arm B exact stdout:
`C2=unmet selftest=ok scan=ok drift=ok trees=ok entry=ok rows=ok pins=ok tree=ok claims=13 files=6 rev=318e546d8ba417df8d28c2f9e9fa58d7c973cdbd failed=tool_sha`

Arm E exact stdout:
`C2=unmet selftest=ok scan=ok drift=ok trees=ok entry=ok rows=bad pins=ok tree=ok claims=13 files=6 rev=70a4c967327847554ba900338b69b6a3f394a2d4 failed=rows`

Arm F exact stdout:
`C2=unmet selftest=ok scan=ok drift=ok trees=bad entry=ok rows=ok pins=ok tree=ok claims=13 files=6 rev=63905603d31ff9d6d96733120d356db840572a80 failed=tree:t03-quote-wrong-line:reasons,trees`

Arm G exact stdout:
`C2=unmet selftest=ok scan=ok drift=ok trees=ok entry=ok rows=ok pins=ok tree=ok claims=13 files=6 rev=93d3febd8eee1f6f671495fb10c0ead760a5a968 failed=tool_sha`

Arm G marker evidence: marker files created at
`$S/mut/G/scratch/MORI-R59-EXEC-MARKER` and `$S/mut/G/tmp/MORI-R59-EXEC-MARKER` (18 bytes each,
content `executed-unpinned\n`); **0** marker files anywhere under the lane. The pinned-blob control
(`count-c2-r59.py 7b86704d…` against the same clone, fresh scratch) wrote **no** marker and exited 0.

Arm G + arm B together isolate a structural fact about the r59 counter, cited by line number in the
pinned blob (`count-c2-r59.py` @ `7b86704d`, sha `2df3ae84…`):

- line 199 `tool_ok = tool_b is not None and sha256(tool_b) == PIN`
- line 203 `failed.append("tool_sha")`
- line 206 `tp.write_bytes(tool_b)` — unconditional on `tool_ok`
- lines 208–214 `subprocess.run(["python3", str(tp), "--selftest", …])` — unconditional on `tool_ok`
- line 360 `met = (tool_ok and st_ok and …)`

So a sha-mismatched blob is still written and executed (`selftest=ok` in arms B and G can only be
produced by the mutated blob running), and only the final verdict is withheld. This is the
Sentinel57/58 "marker hole" reproduced independently at the **data** revision, not just at the
entering revision where the §9 control was scored. Detection only; no remediation attempted here.

## Lane integrity (read-only proof)

- `git -C <lane> rev-parse master` = `b3c256138f00c704d5aa56eb0332d74506502ef2` before and after all runs.
- `git -C <lane> status --porcelain` unchanged: 4 untracked entries only, all other seats' work
  (`evidence/c1-at-data.txt`, `w1/`, `w1.ready`, `w1.ready.dispatched`).
- `find <lane> -type f -mmin -10` after the runs showed only `.ufo/waves/round-60/w1.ready.dispatched`
  (not mine).
- Fixture isolation: every mutation lives in `$S/clone`, whose alternates file reads
  `/home/vgpnk/Projects/shokunin/mori-shokunin/.git/objects` (borrowed read-only) and whose own
  object store is `$S/clone/.git/objects`. Four of the five unique fixture blobs are absent from the
  lane (`git -C <lane> cat-file -e` fails). The one that resolves,
  `792b4aeef3496550bf26edddda5eda8ebe0ba97f`, is the pre-existing blob of
  `.ufo/waves/round-59/trees-c2/t04-stale-pin/expect.txt` (content `pin\n`) — a content-address
  collision with arm F's `pin\n` fixture, not a write. Reachable in lane history via
  `rev-list --all --objects`; `cat-file -p` prints `p i n \n`.

## Observations (reported, not claim extensions)

1. The r59 counter's own `--selftest` prints `C2_SELFTEST pass=9 fail=0` (rc 0, stderr empty). The
   round-60 contract's `pass=8` line names the **r60** `count-c2.py`; these are different counters
   and not a discrepancy. Recorded so a string-level reviewer does not read it as a miss.
2. The r59 counter has no expect-tamper guard: arm F yields `tree:t03-quote-wrong-line:reasons`
   (reason mismatch), never an `expect_tamper` token — consistent with G3 being new in round 60.
3. The r59 counter accepts an empty `rev` argument and emits a full failure line with `rev=` and
   `claims=0 files=0` (observed incidentally from a mis-split variable in this seat's own scripting;
   not a defect claim about the counter, merely observed behaviour).
4. Determinism here is over pinned inputs only: the counter reads exclusively through
   `git show <rev>:<path>` plus `ls-tree`, so the moving lane tip cannot perturb it. That is why
   run4/run5 — taken after the fixture clone accumulated six new commits — still reproduce the exact
   freeze-time bytes.

## Environment

- `scripts/hyaku/disk-guard.sh status` green before (26% used on `/fast`, 601 G free) and after; no
  ENOSPC, no reruns suppressed.
- Scratch: `/fast/scratch/hyaku/mori-r60/Mo60Executor52` (created with `mkdir -p`, `TMPDIR` set
  inside it, `--scratch` passed to the counter). Receipts are embedded above before cleanup; scratch
  removed at yield.
- No tool installs or updates were needed, so nothing to record under the tooling directive.

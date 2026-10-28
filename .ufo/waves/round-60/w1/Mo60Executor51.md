# Mo60Executor51 — r59 C1 receipt payload (r60 wave w1)

Seat scope: materialize `.ufo/waves/round-59/count-c1.py` from
`git show 7b86704d7c0754a09958d131b64dbfa2a6d3eaed` under scratch, run it at
`7b86704d7c0754a09958d131b64dbfa2a6d3eaed` with `--scratch` under scratch, and
return the exact stdout bytes (`cat -A`) and rc. Read-only on the lane; no
VCS mutation, no production/corpus/SCORECARD/LOG edits, no fleet or sibling
writes.

- Lane repo: `/home/vgpnk/Projects/shokunin/mori-shokunin`
- Contract: `.ufo/waves/round-60/contract.md` (freeze `ac496c7c…e4a73f2`,
  entering `ddfb12fb…4b1950195`) — read before any work.
- Lane tip observed at start of work: `b3c256138f00c704d5aa56eb0332d74506502ef2`
  (`b3c25613 round-60: move S561-S564 rows into the Registry table (census E12 fix)`;
  earlier commits `398d3225` C1 data landing and `76904b21` dispatch payload).
  All derivations below are pinned to the named revision, never to the
  working tree.
- Scratch: `/fast/scratch/hyaku/mori-r60/Mo60Executor51/` (created with
  `mkdir -p`; `TMPDIR` set there; `--scratch` under it; removed after this
  report was written). Disk guard at start: exit 0, `/fast/scratch/hyaku`
  26% used, 600.0G free.

## Materialized instrument identity (revision-pinned)

```
$ git -C /home/vgpnk/Projects/shokunin/mori-shokunin \
    show 7b86704d7c0754a09958d131b64dbfa2a6d3eaed:.ufo/waves/round-59/count-c1.py \
    > $SCRATCH/count-c1.r59.py
$ wc -c $SCRATCH/count-c1.r59.py
10571
$ sha256sum $SCRATCH/count-c1.r59.py
2be6fda8c54633fd96f9d447e8e78ff4ba4a6d6136670f79a9d622003f0c9dfd
$ git -C … rev-parse 7b86704d…:.ufo/waves/round-59/count-c1.py
251d4de216c70e506e504ae7b43a7a5979f53027
```

The lane working-tree copy of the same path at tip has the identical sha256
(`2be6fda8…c9dfd`), i.e. the materialization is byte-exact either way; the
run itself uses only `git show`/`git cat-file` at pinned revs.

## Exact executed command

```
cd /home/vgpnk/Projects/shokunin/mori-shokunin
TMPDIR=/fast/scratch/hyaku/mori-r60/Mo60Executor51/run1 \
python3 /fast/scratch/hyaku/mori-r60/Mo60Executor51/count-c1.r59.py \
    7b86704d7c0754a09958d131b64dbfa2a6d3eaed \
    --scratch /fast/scratch/hyaku/mori-r60/Mo60Executor51/run1/scr
```

`--repo` and `--fleet` were left at the counter's own defaults
(`/home/vgpnk/Projects/shokunin/mori-shokunin`, `/home/vgpnk/Projects/shokunin`)
— the same invocation shape `count-c1.py` (r60) uses in `rerun_receipt()`
(`[sys.executable, <blob>, R59_DATA, "--repo", <repo>, "--scratch", <dir>]`,
`TMPDIR=<scratch>`), so the bytes below are directly comparable.

## C1 receipt payload — exact stdout bytes and rc

- rc: **0**
- stdout: **96 bytes**, one line, single trailing `\n` (LF), stderr **0 bytes**
- sha256: `167c9fed65ce5bd5aef6b3487d07f25eae237fd073a003877668e67a79bcdee4`

`cat -A`:

```
C1=met selftest=ok fixtures=ok real=ok pointers=ok rev=7b86704d7c0754a09958d131b64dbfa2a6d3eaed$
```

Verbatim line (byte-identical content of the 96-byte payload):

`C1=met selftest=ok fixtures=ok real=ok pointers=ok rev=7b86704d7c0754a09958d131b64dbfa2a6d3eaed`

This is the payload for `.ufo/waves/round-60/evidence/r59-c1-met.txt`
(contract RECEIPTS ARM, `R59_COUNTERS[".ufo/waves/round-60/evidence/r59-c1-met.txt"]
= ".ufo/waves/round-59/count-c1.py"`).

## Cross-checks (all read-only)

1. **Determinism** — second run in a clean scratch root
   (`run2/`, `TMPDIR=run2`): rc=0, stderr 0 bytes, `cmp run1/out.txt
   run2/out.txt` → identical, sha256 `167c9fed…bcdee4` in both.
2. **Byte-equality with the committed receipt at tip**
   (`b3c2561`): `git show b3c2561:.ufo/waves/round-60/evidence/r59-c1-met.txt`
   compared with `cmp` against the fresh stdout → `IDENTICAL_at_tip`;
   committed blob sha256 is also `167c9fed…bcdee4`. So the payload above is
   already the committed receipt (96 bytes on disk, matching the payload
   size).
3. **The r60 counter itself accepts it** — `python3 .ufo/waves/round-60/count-c1.py
   b3c256138f00c704d5aa56eb0332d74506502ef2 --scratch <scratch>/run3/scr`
   → rc=0:

   ```
   C1=met dead-uncorrected=0 receipts=2/2 absent-set=5/5 lesson=ok rev=b3c256138f00c704d5aa56eb0332d74506502ef2$
   ```

   i.e. the RECEIPTS ARM pairs 2/2 (both receipt files byte-equal their
   revision-pinned re-runs) and the whole C1 after-state line matches the
   contract's frozen target shape `C1=met dead-uncorrected=0 receipts=2/2
   absent-set=5/5 lesson=ok rev=R`.
4. **Instrument selftest at the same rev** — `python3 count-c1.r59.py
   --selftest` → `C1_SELFTEST pass=6 fail=0`, rc=0.
5. **Arms behind the tokens** (from the counter's own code, at the pinned
   rev): `tool_ok` checks `tools/mori-register-check.py` sha256 equals PIN
   (`38b733d8…472b8`; verified at rev: blob `1014c310…`, sha256
   `38b733d8…472b8`); fixture arm enumerates the **13** committed dirs under
   `.ufo/waves/round-59/fixtures-c1/` (`f01-stub-only` … `f13-empty-pointer`),
   each judged UNMET with its committed `expect.txt` reason prefixes; real arm
   binds `SCORECARD.md` at rev to the fleet `MANIFEST.json` at
   `MANIFEST_REV 2807c6ab8a9b04dcf256682bcd722c695fdd6e14` (present in the
   fleet repo, MANIFEST blob `3ac33f9a…`, sha256 `159b6a59…56e6`) and requires
   every reported pointer to resolve via `git cat-file -e R:path`.
6. **Scratch containment / hygiene** — the whole run wrote 144 files, 3.3M,
   under `--scratch` only; no `/tmp/mori-r59-c1-*` directory was created
   (count 0; `--scratch` suppresses the `mkdtemp` path). Lane `git status
   --porcelain` before and after contains only sibling round artifacts, none
   created by this seat: `?? .ufo/waves/round-60/evidence/c1-at-data.txt`,
   `?? .ufo/waves/round-60/w1.ready`, `?? .ufo/waves/round-60/w1.ready.dispatched`,
   `?? .ufo/waves/round-60/w1/`.

## Findings for the L1

- The r59 C1 receipt payload to land is the 96-byte line above; the lane
  already carries it byte-identically at `b3c2561`, and `count-c1.py` (r60)
  at that revision reports `receipts=2/2` — the arm is satisfied at the
  observed tip, not merely reproducible.
- Reproducibility is anchored on two pinned revisions outside the lane's
  own bytes: lane rev `7b86704d…` and fleet rev `2807c6ab…` (MANIFEST). Both
  were reachable read-only during this seat. If the fleet repo loses
  `2807c6ab…`, a later re-derivation of this receipt would fail on the
  `manifest` arm even though the lane bytes are unchanged — this is the only
  non-lane dependency in the receipt.
- The r59 counter carries absolute host-path defaults (`/home/vgpnk/…`) for
  `--repo`/`--fleet`; this does not affect the receipt bytes (the output
  line carries only the rev) and it is not an r60 instrument, so the
  contract's "no absolute host path" construction rule is untouched.

## Risks / limits

- No claim is made here beyond the receipt bytes and rc; the other C1 arms
  (dead-name, absent-set, lesson) were observed only through the counter's
  own printed tokens at `b3c2561` and are the L1's to score.
- Tools installed/updated: none. Pacman not run. No fixture repo or clone
  was created; every read used `git -C`/`git show` against the existing
  repos.
- Scratch `/fast/scratch/hyaku/mori-r60/Mo60Executor51/` was cleaned after
  this report was written; the only retained copy of the payload is the
  `cat -A` block and the verbatim line above.

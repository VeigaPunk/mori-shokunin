# Mo60Executor62 — builder determinism (r60 w1)

Seat: `Mo60Executor62` (executor). Scope: export the lane tree at the freeze revision
into scratch, run `.ufo/waves/round-60/build-fixtures-r60.py` there into a fresh
`trees-c2h`, byte-compare against the committed trees. Read-only on the lane; no
commits, no VCS mutation, no fleet/sibling writes.

## Verdict

**PASS — the r60 fixture builder reproduces the committed `trees-c2h/` and
`trees-c2h-expects.json` byte-for-byte from the frozen tree.**

- `diff -r` committed-vs-regenerated trees: **rc=0** (117 files, 13 trees).
- `diff` of `trees-c2h-expects.json`: **rc=0**.
- Independent second run in a separate tree: **rc=0** (`diff -r` gen1 vs gen2, and
  expects json) — no hash-seed/time/ordering nondeterminism observed.
- Git-native check: all 118 generated files hash to the *exact* committed blob ids
  (`git ls-tree` at the freeze rev), all index mode `100644`, no exec bits.

## Revisions pinned for this seat

| Role | Revision / value |
|---|---|
| Freeze revision (contract) | `ac496c7cde8cad965079858accae3bedfe4a73f2` |
| Contract entering revision | `ddfb12fb0838b4307c445194a844f0c4b1950195` |
| Lane tip observed during this run | `b3c256138f00c704d5aa56eb0332d74506502ef2` ("round-60: move S561-S564 rows into the Registry table (census E12 fix)") |
| `build-fixtures-r60.py` blob at freeze = at tip | `243da06a0ef36d98e7ac445580d5d0716f7146bb` (sha256 `2343b46d837ccb826d1267f5f38fa40b0d4cb94fefd33b39dc87f549ef2b5970`) |
| `trees-c2h` **tree object** at freeze = at tip | `fc3703949d493097cba8134da3aecd116c6a8e6a` |
| `trees-c2h-expects.json` blob at freeze = at tip | `e190b617cc69ae2dc83cc7d0a3b09ed44cd3c785` |

Because the tip moved to `b3c25613` under this wave (C1 data landing), the fixture
bytes were pinned twice: (a) the export was taken from `ac496c7c`, and (b) the
committed fixture path is proven unchanged between `ac496c7c` and `b3c25613`
(`git rev-parse <rev>:.ufo/waves/round-60/trees-c2h` → same tree object;
`git diff --stat ac496c7c b3c25613 -- trees-c2h trees-c2h-expects.json
build-fixtures-r60.py` → empty; `git diff --stat ac496c7c -- <same paths>`
against the working tree → empty, so no seat dirtied the fixtures).

## Procedure and exact evidence

Scratch: `/fast/scratch/hyaku/mori-r60/Mo60Executor62` (`TMPDIR` set there; removed
after the run, digests copied below). Disk guard checked before heavy work:
`/fast/scratch/hyaku use%=26 free=599.1G` — green. Python 3.14.8, `LANG=en_US.UTF-8`,
`umask 0022`.

1. **Export at the freeze revision** (read-only git, no lane write):

   ```
   git -C /home/vgpnk/Projects/shokunin/mori-shokunin archive --format=tar \
       ac496c7cde8cad965079858accae3bedfe4a73f2 | tar -x -C $S/ref
   ```
   → rc 0, 13 772 entries / 13 767 regular files + 5 symlinks.

   Export fidelity check (streamed `git cat-file --batch` over `ls-tree -r`, sha256 per
   blob vs on-disk bytes): **13 769 file entries hashed, 0 mismatches, 0 extras**;
   the only 5 non-regular entries are the repo's own committed symlinks
   (`.ufo/waves/round-17/fixtures/seat/{SecurityRootSymlink/root-link,
   SymlinkIgnore/{Dangling.jsonl,Link.jsonl,linked-dir}}`,
   `.ufo/waves/round-56/fixtures/driver/state-shapes/state/kake.round`, mode
   `120000`), each extracted with a byte-identical link target.
   Builder in the export matches `git show <rev>:…` sha256 (see table above).

2. **Fresh generation** in two independent full copies of the export (committed
   `trees-c2h/` and `trees-c2h-expects.json` deleted first, so only the builder
   produces them):

   ```
   cd $S/gen1 && python3 .ufo/waves/round-60/build-fixtures-r60.py
   trees=13 expects=13          # rc 0
   cd $S/gen2 && python3 .ufo/waves/round-60/build-fixtures-r60.py
   trees=13 expects=13          # rc 0
   ```
   Generated: 13 trees × 9 files = 117 files, plus `trees-c2h-expects.json`.

3. **Byte comparison**

   ```
   diff -r ref/.ufo/waves/round-60/trees-c2h gen1/.ufo/waves/round-60/trees-c2h
   → rc 0   (no output)
   diff ref/.ufo/waves/round-60/trees-c2h-expects.json gen1/…/trees-c2h-expects.json
   → rc 0
   diff -r gen1/.ufo/waves/round-60/trees-c2h gen2/.ufo/waves/round-60/trees-c2h
   → rc 0 ; expects json gen1 vs gen2 → rc 0
   diff -r ref gen1
   → rc 0   (whole 13 767-file export: the builder writes nothing outside its two outputs)
   ```

   Per-file sha256 lists (sorted `sha256sum` over all 117 files) are identical across
   ref/gen1/gen2 — list digest `f514cd74c60b2538e4fcd88a945da489fe50f661d0e00eaf2e5c2066a09402b4`.
   Tree bytes 46 736 both sides. `trees-c2h-expects.json` sha256
   `ae90c90f2c5d47952d38b8f10a3ea4608a225a03765a60571b48ba25575cc2ee`
   (ref, gen1, gen2 identical).

4. **Git-native blob identity** (pure-Python `sha1("blob <len>\0"+bytes)` vs
   `git ls-tree -r` at `ac496c7c`): 118/118 entries match, 0 mismatches; every
   generated file has no exec bit (mode 0644 under umask 0022) matching index `100644`.

5. **Comparator is not vacuous (negative control)** — copied the committed trees,
   flipped one bit at offset 0 of `h07-single-row/corpus/SOURCES.md`, re-ran the same
   `diff -r`: **rc 1** with the expected `1c1` hunk. The byte comparison used above
   detects a single-bit divergence.

6. **Builder behaviour checks**
   - Non-clobber guard: re-running the builder in `gen1` (outputs already present)
     prints `refusing to overwrite existing .ufo/waves/round-60/trees-c2h`, **rc 2**,
     and `gen1` hashes are unchanged afterwards (cmp of the sha256 lists, rc 0).
   - Locale: identical bytes under `LC_ALL=C` and under `LC_ALL=C.UTF-8`
     (`diff -r` rc 0, expects `cmp` rc 0) — CPython 3.14's C-locale coercion keeps
     `Path.write_text` on UTF-8, so the em dash in the `source:`/`verified-at:` header
     is stable.
   - Umask: `umask 0077` run yields byte-identical trees/expects (rc 0) but file
     **modes 0600** (117/117). Content determinism does not depend on umask; only
     permission bits do (git records `100644` either way).

## Per-tree digests (sha256 over sorted `path blobsha`, first 16 hex)

Committed (== regenerated, all three runs):

```
h00-good-control         files= 9 618f80ffcc69e0c1
h01-semantically-empty   files= 9 951bc0441f18602b
h02-malformed-claim      files= 9 10b0dd3ea4f82e02
h03-line-offset-alias    files= 9 cf550e9f1a350557
h04-blank-quote          files= 9 aafece18bc2bed58
h05-short-quotes         files= 9 37bae9c4b71dfebe
h06-degenerate-text      files= 9 a9708a184e7b4c96
h07-single-row           files= 9 c00cbb0fa1d205dc
h08-row-not-mined        files= 9 f29aca6c237f0851
h09-usedby-other         files= 9 ba596a7efb05ccd5
h10-stale-pin            files= 9 c2b0fb16b531220c
h11-wrong-line           files= 9 f7a9682987a3b3f5
h12-no-frontmatter       files= 9 b834ba635d4dc840
```

Sample file sha256 (identical in committed and regenerated):

```
3de3cdcb559cd8b1eaa6bcfdc9659645c5583f83014b18b8132857917b5d7aa7  h00-good-control/corpus/knowledge/wave-settlement-artifacts-r59.md
2be265b0eee38add45e54d3fdbf23363e427d735843e94552852f219e415ff26  h02-malformed-claim/expect.txt
6cda7844b32a2328f89dc1ebdab22df652c176f8f0a912450fd1fd5e12797841  h05-short-quotes/corpus/evidence/sources-r59/w1-results-r54.json
a39cb081a3221638d717036562e943cb6440ba5c272ec642998427d23cbbc3b3  h12-no-frontmatter/expect.txt
```

## Notes for the L1 (not scored by this seat)

1. `build-fixtures-r60.py` writes to `OUT = Path(".ufo/waves/round-60/trees-c2h")`
   **relative to the process cwd**, not to the script location. A run from anywhere
   but a tree root writes the fixtures (and `trees-c2h-expects.json`) elsewhere and
   still exits 0. Determinism holds only when cwd is the tree root — worth stating
   wherever the builder's replay is documented.
2. The builder refuses on an existing `trees-c2h` (rc 2) but **overwrites**
   `trees-c2h-expects.json` unconditionally (it is written last, after the refuse
   check). So a replay must delete both outputs first for a clean comparison — as done
   here (deleting the committed outputs in the scratch copy is what makes the diff a
   real generation test).
3. `h04-blank-quote` writes the entry twice (initial `write_tree`, then a rebuilt
   `fixed` list written without a trailing newline). That is reproducible and matches
   the committed bytes, but it is an incidental double-write, not a deliberate step.
4. Not verified by this seat (out of scope): whether the frozen expect table inside
   `count-c2.py` agrees with the committed `expect.txt` files / `trees-c2h-expects.json`
   (G3 `expect_tamper` path — critic/reviewer scope), and whether the counters consume
   these trees correctly. This seat proves generation determinism only.

## Cleanup

Scratch `/fast/scratch/hyaku/mori-r60/Mo60Executor62` (export, both generated copies,
3 locale/umask probes, negative-control copy, `TMPDIR`) deleted after the digests above
were copied into this report. No lane file, corpus registry, SCORECARD, LOG or VCS state
was written; the only lane-relative artifact from this seat is this report.

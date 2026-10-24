# ExecFreezeVerify — freeze-r37 pin recomputation

Seat: `mori-r37-w1-ExecFreezeVerify` (leaf). Lane repo read-only; no mutation, no remediation.
Scratch: `/fast/scratch/hyaku/mori-r37/ExecFreezeVerify/` (strict parser `verify.py`).
Tool installs: **none**.

## Item attacked

`evidence/freeze-r37.txt` pin integrity: every declared pin recomputed against the working copy,
so that a frozen artifact edited after the freeze (2026-10-23T19:58:09Z) is detected. Secondary
attack: whether the pin *mechanism* can be satisfied by bytes other than the ones measured
(clean filters, unparsed/duplicate lines), and whether the pinned bytes are the bytes C1/C2
actually measure.

## Pin file under test

```
round-37 freeze pins (git blob hashes over the frozen paths)
generated: 2026-10-23T19:58:09Z  entry tip: 842a32074b5c7972e9728f3f629d83eb92f127c2
```
SHA-1 blob block: 8 paths (freeze-r37.txt:3-10). SHA-256 block: 3 paths (freeze-r37.txt:13-15).

## Measurement 1 — git blob pins (8/8)

Command: `git -C <lane> hash-object <path>` for each path in freeze-r37.txt:3-10.

| # | path | pin | recomputed | match |
|---|------|-----|-----------|-------|
| 1 | `.ufo/waves/round-37/contract.md` | `61a768a37a00ea5b4a79fb6ec2dfece272c98b06` | `61a768a37a00ea5b4a79fb6ec2dfece272c98b06` | MATCH |
| 2 | `.ufo/waves/round-37/count-c1.py` | `7518fef8f54afff69ee38a99f2acbf518006f5ad` | `7518fef8f54afff69ee38a99f2acbf518006f5ad` | MATCH |
| 3 | `.ufo/waves/round-37/count-c2.py` | `6213cf9a5ada709da8cd867581782737b2f06c71` | `6213cf9a5ada709da8cd867581782737b2f06c71` | MATCH |
| 4 | `.ufo/waves/round-37/fixtures/memo-n1.py` | `19324701f23a225e5ded21c4785c491e7530ac7c` | `19324701f23a225e5ded21c4785c491e7530ac7c` | MATCH |
| 5 | `.ufo/waves/round-37/fixtures/const.py` | `2f3993a04906ce33033ab207a284d9ca7d7ff57a` | `2f3993a04906ce33033ab207a284d9ca7d7ff57a` | MATCH |
| 6 | `.ufo/waves/round-37/fixtures/summary-only.py` | `2d62f742fbef39634a5ff04e25b399b87ce4c941` | `2d62f742fbef39634a5ff04e25b399b87ce4c941` | MATCH |
| 7 | `tools/mori-source-drift.py` | `162ee87b5b0789c6815f967f3db93d277bab38d9` | `162ee87b5b0789c6815f967f3db93d277bab38d9` | MATCH |
| 8 | `tools/mori-sources-appendonly.py` | `dfb5040b159f7a0b4afedc90a633d997352908f0` | `dfb5040b159f7a0b4afedc90a633d997352908f0` | MATCH |

## Measurement 2 — sha256 pins (3/3)

Command: `sha256sum .ufo/waves/round-37/count-c1.py .ufo/waves/round-37/count-c2.py tools/mori-source-drift.py`

| path | pin | recomputed | match |
|------|-----|-----------|-------|
| `.ufo/waves/round-37/count-c1.py` | `86699627c7627cc3eea3ba9ea952079d081db390f9ba2be1e1d4d685dd98cdae` | `86699627c7627cc3eea3ba9ea952079d081db390f9ba2be1e1d4d685dd98cdae` | MATCH |
| `.ufo/waves/round-37/count-c2.py` | `71c72929f9ac4dc8af0c079fb91220413064cb043391bf495f5ce32cadc3a7c1` | `71c72929f9ac4dc8af0c079fb91220413064cb043391bf495f5ce32cadc3a7c1` | MATCH |
| `tools/mori-source-drift.py` | `453c5d8e260301df7a99daf62b4c16ea08e4a0b4f9e4f53821cdbce447011552` | `453c5d8e260301df7a99daf62b4c16ea08e4a0b4f9e4f53821cdbce447011552` | MATCH |

Strict parser run (`python3 /fast/scratch/hyaku/mori-r37/ExecFreezeVerify/verify.py`):
```
== blob block ==        all 8 lines OK (line 3..10)
== sha256 block ==      all 3 lines OK (line 13..15)
== unparsed lines ==    [(1, header), (2, generated/entry-tip line)]
== counts: blobs=8 shas=3 unique=8
RESULT: PASS
```
No duplicate paths, no malformed pin lines, no pin line silently skipped.

## Measurement 3 — mechanism attacks

**Clean-filter masking** (`git hash-object` applies `.gitattributes` clean filters, which could
make a pin match while disk bytes differ). No attributes exist:
```
for f in .gitattributes .ufo/.gitattributes .ufo/waves/.gitattributes \
         .ufo/waves/round-37/.gitattributes tools/.gitattributes; do ...; done
→ no such file
git check-attr -a -- <.8 paths>            → (empty)
```
Filtered vs raw, all 8 `same`:
```
same  61a768a3… 61a768a3… .ufo/waves/round-37/contract.md
same  7518fef8… 7518fef8… .ufo/waves/round-37/count-c1.py
same  6213cf9a… 6213cf9a… .ufo/waves/round-37/count-c2.py
same  19324701… 19324701… .ufo/waves/round-37/fixtures/memo-n1.py
same  2f3993a0… 2f3993a0… .ufo/waves/round-37/fixtures/const.py
same  2d62f742… 2d62f742… .ufo/waves/round-37/fixtures/summary-only.py
same  162ee87b… 162ee87b… tools/mori-source-drift.py
same  dfb5040b… dfb5040b… tools/mori-sources-appendonly.py
```
So the blob pins are over exact on-disk bytes, not a filtered projection.

**Post-freeze edit sweep** — mtimes of all 8 frozen paths vs the freeze file:
```
2026-10-23 16:58:09.999 -0300  .ufo/waves/round-37/evidence/freeze-r37.txt
2026-10-23 16:57:49.860 -0300  .ufo/waves/round-37/contract.md      (latest frozen path)
2026-10-23 16:47:27.971 -0300  .ufo/waves/round-37/count-c1.py
2026-10-23 16:49:46.376 -0300  .ufo/waves/round-37/count-c2.py
2026-10-23 16:47:38/16:48:00/16:47:42  fixtures/{const,memo-n1,summary-only}.py
2026-10-23 16:43:30.835 -0300  tools/mori-source-drift.py
2026-10-23 09:22:08.458 -0300  tools/mori-sources-appendonly.py
```
Every frozen path predates the freeze; nothing was written after it. (`find -newer freeze-r37.txt`
over `.ufo/waves/round-37 corpus tools` returns only post-freeze *receipts* `c1-after.txt`,
`c2-after-tip.txt`, `census-end.txt`, w1 reports, `dispatch-log.txt`, `corpus/lessons/round-37.md`
and `corpus/QUALITY.md` — none of them pinned, none of them inputs to the 8-path pin set.)

**Freeze file self-anchor** — the freeze file is committed at the scored tip and its working-copy
bytes equal the tip blob:
```
git hash-object .ufo/waves/round-37/evidence/freeze-r37.txt            → 1cd3cbb9ead2ee464df6138028004e080b170a39
git rev-parse e57c58b…:.ufo/waves/round-37/evidence/freeze-r37.txt     → 1cd3cbb9ead2ee464df6138028004e080b170a39
```

## Measurement 4 — pinned bytes == measured bytes

Both counters read committed bytes, not the working tree
(`count-c1.py:880` `git show <full>:tools/mori-sources-appendonly.py`;
`count-c2.py:102-113` `show()` wraps `git show <rev>:<rel>`). At the commanded rev
`e57c58b57c025364e79d130fbdf764d2674d83d6`:
```
git rev-parse e57c58b…:tools/mori-sources-appendonly.py → dfb5040b159f7a0b4afedc90a633d997352908f0   (= pin 8)
git rev-parse e57c58b…:tools/mori-source-drift.py       → 162ee87b5b0789c6815f967f3db93d277bab38d9   (= pin 7)
```
All 8 paths `git rev-parse e57c58b…:<path>` reproduce the pin block exactly. Fixtures are read from
disk under `NEGATIVES_DIR = <repo>/.ufo/waves/round-37/fixtures` (`count-c1.py:57,846`), i.e. the
same three files pinned at lines 6-8 (blobs re-verified on disk: `19324701…`, `2f3993a0…`,
`2d62f742…`). No local-module imports in either counter (stdlib only, `count-c1.py:31-40`,
`count-c2.py:33-40`), and neither embeds its own blob pin, so freeze-r37.txt is the sole pin
source — which is what makes this recomputation authoritative.

## Notes (not defects — no action taken, mori province is detect-only)

1. **Pin set is tip-scoped, not round-scoped.** The pin block is a *working-copy* freeze committed
   as `e57c58b`, not a replay of the entry tip. At `842a320` the six `.ufo/waves/round-37/*` paths
   do not exist and `tools/mori-source-drift.py` is `d59eb2ed05511531070a3cd492ef46df681b2bc9`
   (≠ pin 7). Ordering is therefore coherent, and the header label is honest — `842a320` is the
   parent: `842a320` committed 16:37:01-03, freeze written 16:58:09-03, `e57c58b` committed
   16:58:19-03; `git rev-list --count 842a320..e57c58b` = 1; `merge-base --is-ancestor` holds.
   Consequence to state explicitly: these pins prove the tip's bytes, not that the entry was
   untouched. (Contract line 72 depends on exactly this: `count-c2.py 842a320` is expected to
   `selftest FAIL`.)
2. **sha256 block covers 3 of 8** — the three executed scripts. The freeze file does not state the
   selection rule, and fixtures are executed too, so the asymmetry is unexplained in-file. It is
   harmless redundancy-wise: with no `.gitattributes`, the SHA-1 blob pins already commit to exact
   bytes. A reader should not infer that the 5 unlisted paths are uncertified.
3. **Deliverables are not frozen.** `corpus/lessons/round-37.md` and `corpus/QUALITY.md` were
   written after the freeze and are unpinned; the freeze header ("pins over the frozen paths")
   should be read as *measurement apparatus*, not as the round's knowledge deliverables.
   `corpus/SOURCES.md`, `corpus/README.md`, `corpus/knowledge/source-drift-hardening-r37.md` and
   `evidence/drift-live-r37.txt` are also unpinned, though referenced by the counter predicate text
   (`count-c2.py:43-47`); each is currently byte-clean against `e57c58b` (work blob == tip blob,
   measured) and predates the freeze, so C1/C2 cannot have passed against superseded bytes.

## Verdict

All 11 declared pins (8 blob + 3 sha256) recompute exactly; no filter can mask the comparison; no
frozen path was written after the freeze; the freeze file itself is anchored at the scored tip; and
the pinned blobs are precisely the blobs C1/C2 measure at `e57c58b`. No post-freeze edit of a
frozen artifact exists. The three notes are scope statements, not mismatches.

VERDICT: PASS

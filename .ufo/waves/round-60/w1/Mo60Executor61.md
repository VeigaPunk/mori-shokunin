# Mo60Executor61 — selftest battery (round 60, w1)

**Seat duty:** run `--selftest` for the three frozen counters and for
`tools/mori-entry-claims-check.py` under this seat's scratch TMPDIR; return all
four lines + rc with exact evidence. Read-only on the lane; no commits, no VCS
mutation, no production edits.

## Revision pins used

| Item | Value |
|---|---|
| Entering revision (contract) | `ddfb12fb0838b4307c445194a844f0c4b1950195` |
| Freeze revision (contract) | `ac496c7cde8cad965079858accae3bedfe4a73f2` (exists; is ancestor of HEAD) |
| Lane tip observed at seat start | `b3c256138f00c704d5aa56eb0332d74506502ef2` |
| Tracked tree state | `git status --porcelain --untracked-files=no` → empty (clean) |
| Post-freeze commits reachable | `76904b21` (w1 dispatch payload + at-freeze C2/C3 receipts), `398d3225` (C1 data: r59 receipts, absent-set, SCORECARD `r60-correction:` re-points, S561–S564, lesson) |

The tip moved from `ddfb12fb…` to `b3c2561…` before this seat ran — exactly the
C1 data landing the dispatch warned about. All instrument reads below are pinned.

## 1. Instrument SHA verification against contract pins

`cd /home/vgpnk/Projects/shokunin/mori-shokunin && sha256sum …`

| File | Observed sha256 | Contract pin | Match |
|---|---|---|---|
| `.ufo/waves/round-60/count-c1.py` | `795c1f3193a76406a40561ac60fedb3eee75fc38df2b2efb3fc5295d617ddbae` | `795c1f31…ddbae` | **YES** |
| `.ufo/waves/round-60/count-c2.py` | `8c4814f54c564a7f00beec5249de092a2d3b2c4043e07be773d80e8e3ccdf976` | `8c4814f5…df976` | **YES** |
| `.ufo/waves/round-60/count-c3.py` | `fabde06c9d0a94a8487e5de45be3e413f6084816fb0507a71fd335bad5153514` | not named in contract (see Obs. 1) | n/a |
| `tools/mori-entry-claims-check.py` | `cffe9f3359097277a7ea39729309efdc5831a1738994ceb30ee023ac0eae6e69` | `cffe9f3359097277a7ea39729309efdc5831a1738994ceb30ee023ac0eae6e69` (PIN_EC) | **YES** |
| `tools/mori-settlement-scan.py` | `4c04bf2170b0484192dd157ee04851e8243e030c54046c5e8806d46eea5ac9a9` | `4c04bf21…ac9a9` (PIN_SCAN, count-c2:50-51) | **YES** |

In-source pins confirmed to agree with the contract: `count-c3.py:51-52`
(`PIN_C1`, `PIN_C2`), `count-c2.py:48` (`PIN_EC`), `count-c2.py:50-51`
(`PIN_SCAN`).

### Freeze-stability (kill rule C1/C2/C3)

Command:
`git diff --stat ac496c7c… HEAD -- count-c1.py count-c2.py count-c3.py contract.md mori-entry-claims-check.py mori-settlement-scan.py`

→ **empty output, rc 0**. No post-freeze byte change to any counter, the
contract, or either tool. Additionally, each instrument's `HEAD:` blob sha
byte-equals its working-tree sha (`git show HEAD:<f> | sha256sum` vs
`sha256sum <f>`, all four `MATCH`), so the selftests below ran the same bytes as
the freeze for every pinned instrument.

## 2. The four selftest lines + rc (the deliverable)

All runs: `export TMPDIR=/fast/scratch/hyaku/mori-r60/Mo60Executor61`, cwd
`/home/vgpnk/Projects/shokunin/mori-shokunin`.

| # | Command | Output line | rc | Contract expects | Verdict |
|---|---|---|---|---|---|
| 1 | `python3 .ufo/waves/round-60/count-c1.py --selftest` | `C1_SELFTEST pass=6 fail=0` | **0** | `C1_SELFTEST pass=6 fail=0`, exit 0 | **PASS** |
| 2 | `python3 .ufo/waves/round-60/count-c2.py --selftest` | `C2_SELFTEST pass=8 fail=0` | **0** | `C2_SELFTEST pass=8 fail=0` | **PASS** |
| 3 | `python3 .ufo/waves/round-60/count-c3.py --selftest` | `C3_SELFTEST pass=3 fail=0` | **0** | `C3_SELFTEST pass=3 fail=0` | **PASS** |
| 4 | `python3 tools/mori-entry-claims-check.py --selftest` | `ENTRYCLAIMS_SELFTEST pass=13 fail=0` | **0** | `ENTRYCLAIMS_SELFTEST pass=13 fail=0` | **PASS** |

No `FAIL …` lines appeared on stderr for any run. No `mori-r60-*` temp
directories were left behind (each selftest removes its `mkdtemp` base in a
`finally`).

## 3. Non-vacuity of the selftests (falsification probe)

A selftest line proves nothing unless it fails when the predicate breaks. Four
single-predicate mutants were made **on scratch copies only**
(`/fast/scratch/hyaku/mori-r60/Mo60Executor61/mut/`); no production byte was
touched.

| Instrument | Mutation (scratch copy) | Result | rc |
|---|---|---|---|
| `count-c1.py:77-80` | `dead_uncorrected` → unconditional `return 0` | `FAIL dead_plain` / `C1_SELFTEST pass=5 fail=1` | **1** |
| `count-c2.py:137` | `materialize`: delete the `if not contained(root, t): return False` assert | `FAIL contain_parent`, then `FileExistsError` on the symlink case (aborts before summary print) | **1** |
| `count-c3.py:51` | `PIN_C1 = "MUTANT"` | `FAIL pins` / `C3_SELFTEST pass=2 fail=1` | **1** |
| `mori-entry-claims-check.py:49` | `MIN_SPAN = 8` → `1` | `FAIL short_span` / `ENTRYCLAIMS_SELFTEST pass=12 fail=1` | **1** |

Extra signal from the c2 mutant: removing the containment assert wrote
`escape.txt` **outside** the selftest's base dir (observed at
`/fast/scratch/hyaku/mori-r60/Mo60Executor61/mut-tmp/escape.txt`). The frozen
bytes refuse that write — direct confirmation that the G2 containment
assertion is load-bearing rather than cosmetic. (Both counters also pass
`TMPDIR=<scratch>` to every child process: `count-c2.py:152`,
`count-c3.py:127`, so c2's pinned tool-selftest child temp is scratch-contained
too.)

Selftest bodies reviewed and confirmed to call the real predicates, not print a
constant: c1 → `dead_uncorrected`, `corrected_lines_name_real`,
`parse_absent_table`; c2 → `materialize` (4 containment refusals) plus table
shape/pin-length invariants; c3 → pin lengths, `EVIL_BLOB` marker, `TAMPER_REL`
shape; tool → 13 checks driving `eval_root` through good/H1-grammar/H2-alias/
H2-blank/H2-short/H3-text/H4-binding/row-status/stale-pin/span-mismatch/
no-frontmatter/entry-absent cases (`tools/mori-entry-claims-check.py:242-437`).

## 4. Observations / risks (no remediation performed)

1. **c3 has no contract-stated sha.** The contract pins c1 and c2 by sha and
   says c3 was "re-pinned" (Amendment 1) without giving c3's digest, so a c3
   byte swap enforced by the kill rule cannot be detected from the contract
   text alone. Observed c3 sha: `fabde06c9d0a94a8487e5de45be3e413f6084816fb0507a71fd335bad5153514`.
   C3's own selftest still validates its structural pins, and the freeze diff is
   empty. Flagged for L1.
2. **`--scratch` is accepted but unused by the tool selftest.**
   `mori-entry-claims-check.py:442-446` parses `--scratch` for `--selftest`,
   but `selftest(scratch=None)` ignores it and calls
   `tempfile.mkdtemp(dir=os.environ.get("TMPDIR"))`. Containment therefore rests
   on the caller exporting `TMPDIR` — which count-c2 does (`count-c2.py:152`).
   No breach observed; recording the coupling.
3. **c2 mutant failure shape.** The containment mutant surfaces as a traceback
   rather than a clean `FAIL` line for the symlink case. Detection (rc=1) holds;
   only the diagnostic shape differs, and only in mutant space, not in the
   frozen bytes.
4. Selftests are structural — they exercise predicates on synthetic fixtures and
   do not themselves score C1/C2/C3 at a revision. Those measurements remain the
   `count-c*.py <rev>` runs owned by the at-freeze evidence
   (`evidence/c2-at-freeze.txt`, `c3-at-freeze.txt`) and the C1 data arm.

## 5. Environment and hygiene

- Disk guard before work: `scripts/hyaku/disk-guard.sh status` → rc 0;
  `/fast/scratch/hyaku` 26% used, 599.1G free. No ENOSPC.
- Scratch: `/fast/scratch/hyaku/mori-r60/Mo60Executor61` (created with
  `mkdir -p`), used as `TMPDIR`; mutant copies and `mut-tmp` lived there and were
  removed before yielding. Nothing written to `/tmp`, the fleet root, sibling
  repos, or the lane's tracked files.
- No tool installs/updates were needed; no pacman invocation.
- No git/jj mutation: all git commands were read-only (`status`, `rev-parse`,
  `cat-file`, `merge-base`, `log`, `diff`, `show`).

## Bottom line

All four selftests reproduce the contract's frozen lines with rc 0, on bytes
byte-identical to the freeze revision, and each one demonstrably fails (rc 1)
under a targeted predicate mutation — so the battery is real, not decorative.
Two provenance gaps worth L1 attention: c3's own sha is absent from the contract
text, and the tool selftest's `--scratch` argument is inert (containment rides on
`TMPDIR`).

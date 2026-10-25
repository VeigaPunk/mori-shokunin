# round 44 · w1 · RevEnteringBaseline — independent before-value re-derivation

Role: reviewer (leaf, no subagent dispatch). Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin`.
Entering tip measured: `1429c791db5891c484684feef893799909d2d6a8` (round-43 verifier
spot-check, single commit, +228 lines to `corpus/lessons/round-43-verifier-spotcheck.md`).
Lane HEAD at measurement: `7cb59c6891d4f5d0266fe062565f094da835dc84`.
Runtime: Python 3.14.8. All scratch work in `mktemp -d` sandboxes; no write outside this
report; no `git add/commit/push/checkout/stash/reset`, no jj mutation; no installs needed.

Instrument freeze verified before use (`.ufo/waves/round-44/evidence/freeze-r44.txt`):

```
$ cd /home/vgpnk/Projects/shokunin/mori-shokunin && sha256sum -c .ufo/waves/round-44/evidence/freeze-r44.txt
.ufo/waves/round-44/contract.md: OK
.ufo/waves/round-44/count-c1.py: OK
.ufo/waves/round-44/count-c2.py: OK
.ufo/waves/round-44/count-c3.py: OK
tools/mori-gate-registry.py: OK
.ufo/waves/round-44/fixtures/figures-r43.tsv: OK
.ufo/waves/round-44/fixtures/mutants/count-c1.py: OK
.ufo/waves/round-44/fixtures/mutants/count-c2.py: OK
.ufo/waves/round-44/fixtures/mutants/count-c3.py: OK
SKILL.md: OK
sha256sum: WARNING: 4 line(s) are improperly formatted
```

10/10 pinned artifacts match the working-tree bytes; the warning is the four `#` comment
lines in the pin file, not a mismatch. The frozen instruments are the ones executed below.

## Verdict on the five assigned before-values

| # | Assigned before-value (contract) | Observed at `1429c791` | Match |
|---|---|---|---|
| 1 | `count-c1.py` → `check ledger_present FAIL (absent)` → `C1=unmet`, exit 1 | `check ledger_present       FAIL (absent)` · `C1=unmet mismatches=?` · exit 1 | **yes** |
| 2 | `count-c2.py` (3 counters) → `check counters_present FAIL (absent)` → `C2=unmet`, exit 1 | `check counters_present   FAIL (absent=[…c1.py, …c2.py, …c3.py])` · `C2=unmet` · exit 1 (plus 4 further FAILs, see D-2) | **yes** (verdict/exit); line incomplete |
| 3 | `count-c3.py` (entry + S471,S472) → unmet, exit 1 | `check entry_present    FAIL (absent)` · `C3=unmet` · exit 1 | **yes** |
| 4a | `git grep -l 'Z ゾンビ' 1429c791 -- corpus/` → 0 files | no output, exit 1, 0 files | **yes** |
| 4b | registry rows at `1429c791` → 243 | 243 rows, 243 unique ids, `S001`–`S470` | **yes** |
| 5 | the three counters absent at `1429c791` | all three `git cat-file -e` → ABSENT | **yes** |

**No before-value differs from the contract.** Every contract "Before" claim reproduces
exactly at the entering tip, including the C1 `mismatches=?` placeholder and both exit
codes. One independent, high-severity instrument defect was found while deriving item 3;
it changes no before-value but makes P-C3's declared **After** unreachable (finding F-1).

## Transcripts (verbatim)

### 1. C1 at the entering tip

```
$ cd /home/vgpnk/Projects/shokunin/mori-shokunin && python3 .ufo/waves/round-44/count-c1.py 1429c791; echo "EXIT=$?"
check ledger_present       FAIL (absent)
rev=1429c791db5891c484684feef893799909d2d6a8
ledger=.ufo/waves/round-44/figures.tsv rows=0 classes=-
C1=unmet mismatches=?
EXIT=1
```

Cross-check: `.ufo/waves/round-44/figures.tsv` is ABSENT at `1429c791`
(`git cat-file -e` exit non-zero), so the do-nothing control cannot reach `C1=met` — the
contract's kill rule is satisfied by construction at this tip.

### 2. C2 at the entering tip

```
$ python3 .ufo/waves/round-44/count-c2.py 1429c791 \
    --counter .ufo/waves/round-44/count-c1.py \
    --counter .ufo/waves/round-44/count-c2.py \
    --counter .ufo/waves/round-44/count-c3.py; echo "EXIT=$?"
check counters_present   FAIL (absent=['.ufo/waves/round-44/count-c1.py', '.ufo/waves/round-44/count-c2.py', '.ufo/waves/round-44/count-c3.py'])
check registry_rows      FAIL (tools/mori-gate-registry.py absent)
check tool_selftest      FAIL (tools/mori-gate-registry.py absent)
check selftest_tally     FAIL (.ufo/waves/round-44/count-c1.py absent; .ufo/waves/round-44/count-c2.py absent; .ufo/waves/round-44/count-c3.py absent)
check mutant_kill        FAIL (.ufo/waves/round-44/count-c1.py absent; .ufo/waves/round-44/count-c2.py absent; .ufo/waves/round-44/count-c3.py absent)
rev=1429c791db5891c484684feef893799909d2d6a8
C2=unmet
EXIT=1
```

### 3. C3 at the entering tip

```
$ python3 .ufo/waves/round-44/count-c3.py 1429c791 \
    --entry corpus/knowledge/pid-probe-conclusion-r44.md --row S471 --row S472; echo "EXIT=$?"
check entry_present    FAIL (absent)
rev=1429c791db5891c484684feef893799909d2d6a8
C3=unmet
EXIT=1
```

`entry_present` short-circuits the counter, so `census_ok` is not reached at this tip —
which is why finding F-1 does not perturb any before-value.

### 4. Corpus sweep and registry census of the entering tip

```
$ git grep -l 'Z ゾンビ' 1429c791 -- corpus/ ; echo "GREP_EXIT=$?"
GREP_EXIT=1
$ git grep -l 'Z ゾンビ' 1429c791 -- corpus/ | wc -l
0
$ git grep -l 'ゾンビ' 1429c791 | wc -l          # whole tree, wider token
0
$ git show 1429c791:corpus/SOURCES.md | python3 -c "<frozen ROW_RE from count-c3.py:31>"
rows= 243 unique= 243
min/max id= S001 S470
```

The `S001`–`S470` maximum is consistent with the contract's after-target of `S471`/`S472`
(243 → 245). `cmdline` appears in 23 corpus files and `FR5` in 10, so the ground the round
targets is adjacent to, but distinct from, ground already held: the `Z`/`X` process-state
alphabet and the three-world reading of a zero-character `/proc/<pid>/cmdline` are absent
from every committed corpus byte at this tip.

Registry census, on the same committed bytes, with `used-by` targets resolvable:

```
$ bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh \
    validate --file <sandbox>/mori-shokunin/corpus/SOURCES.md
→ exit 0 ; one `file ok` line ; 19 × W04 (duplicate url across scopes, warnings only)
$ bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh census --file <same>
file	rows	243
file	status.mined	192
FLEET	rows	243
FLEET	tier.invalid	0
FLEET	status.invalid	0
```

So the entering registry is census-green (exit 0) and 243 rows, matching the contract's
"Before: registry 243 rows" and the recorded `evidence/census-start.txt`.

### 5. Instrument absence at the entering tip

```
$ for p in .ufo/waves/round-44/count-c1.py .ufo/waves/round-44/count-c2.py \
           .ufo/waves/round-44/count-c3.py tools/mori-gate-registry.py \
           .ufo/waves/round-44/contract.md .ufo/waves/round-44/figures.tsv \
           corpus/knowledge/pid-probe-conclusion-r44.md ; do
    git cat-file -e "1429c791:$p" 2>/dev/null && echo PRESENT || echo ABSENT ; done
.ufo/waves/round-44/count-c1.py               ABSENT
.ufo/waves/round-44/count-c2.py               ABSENT
.ufo/waves/round-44/count-c3.py               ABSENT
tools/mori-gate-registry.py                   ABSENT
.ufo/waves/round-44/contract.md               ABSENT
.ufo/waves/round-44/figures.tsv               ABSENT
corpus/knowledge/pid-probe-conclusion-r44.md  ABSENT
$ git ls-tree -r --name-only 1429c791 | grep -c 'round-44'   → 0
```

The whole round-44 tree is absent at the entering tip: the counters, the auditor, the
ledger and the entry are all new bytes this round. The entering state genuinely lacks the
instruments, so every "Before" above is a true zero, not a mis-invocation.

## Findings

### F-1 (high — P-C3's After is unreachable with the frozen instrument)

`count-c3.py`'s `census_ok` check stages the revision's `corpus/SOURCES.md` into a fresh
`tempfile.mkdtemp()` and runs `bash <census> validate --file <staged>` (`.ufo/waves/round-44/count-c3.py:136-146`).
The census resolves `used-by` paths against the **parent of the registry's directory**
(`scripts/sources-census.sh:498-503`: `dir_abs=$(realpath -- "$(dirname -- "$file_abs")/..")`)
and emits `E11 used-by path missing on disk` for every target that does not exist under
that root (`:538-568`, `[ ! -e "$dir/$path" ]`). For the counter's staging that root is
`/tmp`, so every mined `used-by` path in the real registry is "missing" and the census
exits 1. `cwd=repo` does not help: `resolve_targets` returns early in `--file` mode, so
`--root`/cwd never influence `dir`.

Reproduced with the counter's exact call shape, on the entering tip's committed bytes:

```
$ T=$(mktemp -d -p /tmp c3-XXXXXX)
$ git show 1429c791:corpus/SOURCES.md > "$T/SOURCES.md"
$ bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file "$T/SOURCES.md"
EXACT_INVOCATION_EXIT=1
--- E11 lines: 277 ---
file	E11	S001 missing used-by corpus/lessons/2026-10-15-free-lunch-measurements-counter-baselines.md
file	E11	S002 missing used-by corpus/knowledge/oom-kill-counter-kernel-only-r12.md
file	E11	S002 missing used-by corpus/knowledge/userspace-oom-killers-r12.md
```

Same bytes, same census, with the `used-by` targets resolvable (sandbox mirror of the lane
root, symlinks only, lane untouched):

```
$ bash …/sources-census.sh validate --file <sandbox>/mori-shokunin/corpus/SOURCES.md
CENSUS_FULLY_RESOLVED_EXIT=0        # one `ok`, 19 W04 warnings
```

Direct confirmation on an in-flight after-shape (WORK = sibling lanes' current uncommitted
bytes; measured read-only, it is not a verdict on the round and its `readme_row` failure is
just the frontier row not yet written):

```
$ python3 .ufo/waves/round-44/count-c3.py WORK --entry corpus/knowledge/pid-probe-conclusion-r44.md --row S471 --row S472
check entry_present    PASS (4261 bytes)
check entry_meta       PASS (sources S471,S472)
check rows_present     PASS (rows S471,S472 mined)
check census_ok        FAIL (exit=1)
check readme_row       FAIL (no line names the entry)
rev=WORK
C3=unmet
WORK_EXIT=1
```

The entry, its `source:` ids and both mined rows are already in place, and `census_ok` still
fails on `exit=1` — F-1 is not a prediction about a hypothetical registry; it fires on the
real after-shape the moment the entry exists.

Conclusion: `census_ok` is False at **every** revision whose registry holds a mined row with
a `used-by` path — i.e. every revision, including any after-state carrying S471/S472. The
frozen counter therefore cannot print `C3=met`, so contract P-C3's declared After
(`C3=met`, exit 0) is unreachable as frozen, independent of how honestly the round lands the
entry, the rows and the README row. This is an instrument defect, not an entrant defect; per
the contract's **Freeze** clause it may not be patched in place (record as a lesson, route
to round 45). Deciding whether C3 lands `unmet` or the round is re-frozen is outside my
authority — reported, not decided.

### F-2 (medium — the C3 selftest structurally cannot catch F-1)

Every `count-c3.py --selftest` arm injects a stub census (`fixtures/fake-census.sh`, bytes
`#!/bin/sh\nexit 0`, `:172-175`, arms at `:218-268`), so the real census's path resolution is
never exercised. Observed tally, matching the freeze record:

```
$ python3 .ufo/waves/round-44/count-c3.py --selftest
selftest PASS registered_entry_met
selftest PASS absent_entry_unmet
selftest PASS row_without_used_by_unmet
selftest PASS red_census_unmet
selftest PASS readme_without_row_unmet
selftest PASS missing_coverage_map_unmet
C3_SELFTEST pass=6 fail=0
SELFTEST_EXIT=0
```

`pass=6 fail=0` is honest about the arms it runs and silent about the arm that matters: no
arm runs the production census against a staged registry, and the committed mutant
(`fixtures/mutants/count-c3.py`) can only be caught through these same stub-based arms.
F-1 and F-2 are one defect seen from two sides: the counter's own gate cannot fail on the
check it gets wrong.

Three verified details make the blind spot structural rather than an omission:

1. The stub body is `#!/bin/sh\n# fixture census\nexit 0\n` (`:172`) — it references no
   argument, so it never reads `--file` or the staged bytes. The `red_census_unmet` arm
   (`CENSUS_RED = "#!/bin/sh\nexit 1\n"`, `:173`, used at `:249`) proves only that a nonzero
   exit is propagated, never that the census consumed the registry.
2. The stub is **written by the counter itself** — `_files()` injects
   `"fixtures/fake-census.sh": CENSUS_OK` into the temp fixture repo (`:204`) and the arms
   invoke that path (`:227`). No `fake-census` file exists in the lane tree
   (`git ls-tree -r 7cb59c68 | grep -c fake-census` → 0), so the blind spot cannot be closed
   by committing a fixture; it is inside the frozen counter's own fixture builder.
3. The census under test is not in the freeze manifest and is not in the lane:
   `census = args.census or os.path.join(os.path.dirname(repo), "scripts", "sources-census.sh")`
   (`:299`) defaults to `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh` — unpinned
   authority one directory above the lane repo. A counter that can print `C3=met` would be
   reporting on a byte it neither freezes nor owns.

### D-1 (low — the contract's C2 witness command is not verbatim-runnable)

Contract P-C2 witness: `tools/mori-gate-registry.py --rev <tip> --audit <a> <b>`. The tool
takes `--audit` as a single value, so the quoted form exits 2:

```
$ python3 tools/mori-gate-registry.py --rev 1429c791 --audit .ufo/waves/round-43/count-c1s.py .ufo/waves/round-43/count-c2.py
mori-gate-registry.py: error: unrecognized arguments: .ufo/waves/round-43/count-c2.py
AUDIT_EXIT=2
```

With the flag repeated, the witness's substance reproduces at the entering tip:

```
$ python3 tools/mori-gate-registry.py --rev 1429c791 --audit .ufo/waves/round-43/count-c1s.py --audit .ufo/waves/round-43/count-c2.py
audit .ufo/waves/round-43/count-c1s.py         FAIL (unregistered: no row names count-c1s.py)
audit .ufo/waves/round-43/count-c2.py          FAIL (unregistered: no row names count-c2.py)
rev=1429c791db5891c484684feef893799909d2d6a8
REGISTRY=unmet
AUDIT_EXIT=1
```

Two notes for the record: (a) the auditor's diagnostic is `unregistered: no row names …`,
it does not additionally say "without a selftest mode" as the contract's witness sentence
words it — though that part is factually right, both round-43 counters lack a `--selftest`
CLI mode (`count-c1s.py --selftest` → usage, exit 2; `count-c2.py` has no `selftest`
token at all), and `count-c1s.py`'s internal `selftest()` helper merely drives a *different*
counter's `--selftest`; (b) the auditor itself is ABSENT at `1429c791`, so this witness can
only be run from a later revision with `--rev 1429c791` — it is not runnable at the entering
tip.

### D-2 (low — the contract's C2 Before line understates the failing checks)

Contract: "`check counters_present FAIL (absent)` → `C2=unmet`, exit 1". Observed: five
checks fail (`counters_present`, `registry_rows`, `tool_selftest`, `selftest_tally`,
`mutant_kill`), because `tools/mori-gate-registry.py` is also absent at the entering tip.
Verdict and exit code match the contract; only the abbreviated Before line is incomplete.
No effect on the claim.

### D-3 (info — freeze path shorthand)

The contract's Freeze clause names `evidence/freeze-r44.txt`; the actual path is
`.ufo/waves/round-44/evidence/freeze-r44.txt`. The pin file verifies 10/10 (transcript
above), so this is shorthand, not a missing pin.

## Residual risk and verification gaps

- **No committed After exists to measure.** The contract's after-values (`C1=met`,
  `C2=met`, `C3=met`, registry 245 rows, 1 file naming `Z ゾンビ`) are declarations only;
  the one after-shape I could run is the uncommitted WORK state, and it reproduced
  `census_ok FAIL (exit=1)` — see F-1. Nothing here scores the round's After.
- **F-1 depends on an unpinned external byte.** `scripts/sources-census.sh` lives in the
  fleet repo and is *not* in `freeze-r44.txt`; measured identity
  `sha256 3fb7261569f46423dd80ecc23e0a23789a7926f667c7a3fc559d2439d4a64e30`, mtime
  `2026-10-19 21:22:45 -0300`, size 35466. If that file is amended the finding must be
  re-derived; it was not amended during this measurement (read-only use).
- **Out of scope here, deliberately unmeasured:** `count-c1.py`'s fixture witness
  (`fixtures/figures-r43.tsv` → `mismatches=2`), `count-c2.py --selftest` and the mutant
  kill tallies, `mori-gate-registry.py --selftest`, and the gate-table cell audit — sibling
  lanes hold those. I assert nothing about them.
- **A first-call/empty-result caveat:** none applies; no LSP server covers these Markdown
  artifacts, so caller/definition/diagnostic checks were done by reading the frozen sources
  and by execution, and every claim above is a quoted command with its output. Grep is used
  only for literal token absence, which is the claim itself.
- **Sandboxes** (`/tmp/tmp.*`, `/tmp/c3-*`) were left in place for reproducibility; they
  hold copies only. No lane, fleet, sibling or `shokuknow` byte was written; no campaign
  tool was run in `shokuknow`; the only file written by this seat is this report.

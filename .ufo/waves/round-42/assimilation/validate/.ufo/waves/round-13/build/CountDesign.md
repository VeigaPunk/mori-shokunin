# CountDesign — round 13 before/after counters (C1 coverage, C2 operability)

Seat: `MoriR13.CountDesign` (executor, leaf). Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin`.
Axes: **coverage** (C1) and **operability** (C2). No source edits, no commits, no verification
runs by this seat. Everything below is either a file/line observation at a named artifact, an
explicitly marked inference, or a command L1 can run.

Tooling record: **none installed or updated**. Only read-only inspection (`read`, `grep`,
`sha256sum`, `journalctl --list-catalog` for catalog presence) was used.

---

## 1. Baseline audit mechanisms inspected

Pinned entering bytes (frozen snapshots, `.ufo/waves/round-13/frozen/inputs.json`):

| artifact | sha256 | role |
|---|---|---|
| baseline `tools/mori-census.sh` | `3da5b098dc23aeb3e1c31ce82664b24a22c2847a168308a755525593881b3164` | frozen pre-fix census |
| baseline `tools/mori-silence-cases.sh` | `448f77238c73a5c929a898dad0f0c495fd2a66cc4b90a00ae84ede69a86beeb5` | frozen pre-fix oracle |
| base commit | `6531ac6029e200a6392bb76673b6a17d3c895c96` | `6531ac6` |

Mechanisms and their measured blind spots (baseline line anchors are the frozen files):

| mechanism | anchor | what it grades | blind spot that makes a counter necessary |
|---|---|---|---|
| census journal probe | `mori-census.sh:854-911` | one user-scope surface; four **text** classes (OOM/kill/segfault/unit) | counts MESSAGE text (Q15); no system scope; `segfault` merges a text class with an unfiltered `-o json COREDUMP_SIGNAL=11` whose rc is never read (`:882-886`) |
| census verdict/exit | `mori-census.sh:1733-1740`; contract `:352-354` | exactly one `MORI_CENSUS: CLEAN\|DRIFT (findings=N drift=M unavailable=U surfaces=S)`; `CLEAN→0`, `DRIFT→1` | nothing below the emitter grades this in the oracle |
| census selftest | `mori-census.sh:2196-2275` `check()`, fixture dispatcher `:2041-2042`, tally `:3008` | runs the real CLI under `env -i` on a fixture tree; asserts rc + verdict + finding regexes over a captured file | the dispatcher is args-blind (one `journal` file for every journalctl call), so a structured probe is not drivable as-is; the selftest is authored by the implementation owner |
| F01 authorship | `mori-census.sh:1490-1499` | exact author line membership in the `(launch, NOW]` window | `printf … \| sed … \| grep -Fxq` under `pipefail`: an early match closes the pipe, the producer dies 141, and the `if` takes the false branch (`sib=1`) |
| oracle case grader | `mori-silence-cases.sh:558-617` `assert_case` | lane state, `LANE_SILENT`, rc, nonce | verdict is only `grep -m1 '^MORI_CENSUS:'` + non-empty (`:569-570`): vocabulary, cardinality and rc agreement are unchecked |
| oracle guards | `mori-silence-cases.sh:939-954` (readonly), `:976-985` (`shape_observe`/`shape_has_verdict`), `:987-1006` | mutation-free tree; same grade under two dir names | readonly never reads the roll; shape tests only the substring `MORI_CENSUS:` |
| oracle registry/tally | `mori-silence-cases.sh:1016-1045` (28 ids), `:1083` tally | 28 behavioral cases, seeded shuffle + nonce | the denominator is "however many ran"; this round's F02 scope is the roll, not tally cardinality (named residual) |

Cross-references: `corpus/knowledge/audit-r11.md:156` (F01), `:157` (F02), Appendices B/C
`:308-407`; `corpus/QUALITY.md` criteria 6–8, 13, 15–17, 23, 26–27.

Observed before-state (retained evidence, not re-run here):

- F01, Appendix B: one exact subject line + 12,000 sibling lines → `progressing-weak
  (basis=row-C other_authored_commits=12001)`, rc 0 (`audit-r11.md:333-369`).
- F02, Appendix C: BANANA wrapper → `MORI_SILENCE_CASES: matched=28 total=28`, exit 0
  (`audit-r11.md:376-407`).
- C1: the census exposes no per-scope class counts; `fe6faa94…`'s real MESSAGE is
  “A process of @UNIT@ unit has been killed by the OOM killer” (`S013:604-605`), which matches
  none of the text patterns at `mori-census.sh:872-880`, so the notices are invisible.

---

## 2. Counter rules

1. **Behavior first.** Every counter runs the real CLI (`bash tools/mori-census.sh` or
   `bash tools/mori-silence-cases.sh <proxy>`) in a hermetic tree and grades exit code, state,
   structured fields, or rejection. No counter uses "count of a phrase in the script" as its
   metric.
2. **Before and after are both measured.** Before = frozen snapshot at the pinned SHAs above
   (or the audit's retained output, where named). After = the integrated working tree. A
   counter that cannot distinguish them is a broken counter, not a pass.
3. **One discriminating witness per claim.** The pre-fix bytes must fail the after-contract for
   the stated reason; the post-fix bytes must pass. The witness is recorded verbatim in the
   evidence log.
4. **Exact tallies, bracket only where the host is the source.** Fixture and oracle counters
   pre-register exact numbers. The live journal counter brackets each count between two
   independent reads around the census run; it never pins a volatile live value to 7/9/1585.
5. **No MESSAGE.** Fixtures are synthetic and carry a canary in a `MESSAGE` key; the counter
   asserts the canary never appears in census stdout/stderr. Live commands select
   `--output-fields` without `MESSAGE` and print only counts.
6. **Queues, not sums.** User and system scopes are separate fields/rows; a summed token is a
   failure. Notice classes carry `unit=notice`; record classes carry `unit=record`.
7. **Evidence is committed.** Fixture generators and their digests live under
   `corpus/evidence/round13-count-<UTC>/` (QUALITY 23); `/tmp` paths are working space only.

Counter IDs used below: `C1-MATRIX-A`, `C1-MATRIX-B`, `C1-LIVE`, `C1-REGRESS`, `C2-F01`,
`C2-F02`, `C2-REGRESS`.

---

## 3. C1 — structured, MESSAGE-free journal scopes

### 3.0 Contract under test

The integrated census emits (final grammar confirmed by CensusFix 2026-10-20; re-anchor if it
moves):

```
SURFACE journal.user: <ok|unavailable> (cmd=…; scope=user
  kernel_oom_notice=<N|unavailable:reason> oomd_notice=… coredump_notice=…
  segfault_signal11=… unit_sigkill_record=… unit_failure_record=…
  ; boot=<32hex|unavailable:no-records>; unit=notice
  notice_classes=kernel_oom_notice,oomd_notice,coredump_notice
  record_classes=segfault_signal11,unit_sigkill_record,unit_failure_record
  trust=client-supplied field=user:MESSAGE_ID oomd_activity=unmeasured rc=<0|nonzero>
  ; unmeasured=oom_kill_text,other_signals,other_unit_failure_text reason=…; ts=…)
SURFACE journal.system: … same shape, scope=system …
```

Class-unavailable reasons: `rc-N`, `timeout`, `stderr-nonempty`, `malformed-json`,
`record-invalid`, `boot-mismatch`, `multi-boot`, `no-timeout-bin`. Row-level reasons:
`journalctl=missing`, `parser=missing`, `boot_id=unavailable`. Every run also emits
`FINDING JOURNAL_CLASSES_UNMEASURED info` with the three dropped text classes, including runs
where `journalctl`/`jq` is absent. Positive cells emit `FINDING … class=… unit=notice|record
count=N scope=user|system`; the one WARN is `KILL_SIGNAL_JOURNAL` (user `unit_sigkill_record`,
`unit=record`, `attribution=none`).

The counter accepts the two-row form above; a single-row variant (`SURFACE journal:` with
`<scope>_<class>` tokens) is parsed equivalently, but both scopes must appear exactly once.

**Parsing rule:** for scope `S` and class `C`, the cell is the token `C` on `SURFACE journal.S:`,
or the token `S_C[_short]` on a single `SURFACE journal:` row. On an `ok` row every cell must be
present: a missing cell is a failure, not zero. On a whole-scope `unavailable` row (absent tool
or parser) the class tokens may be absent, but no count may be claimed. `unavailable:<reason>`
is a rejection, not a count.

### 3.1 C1-MATRIX-A — independent positive/leak/empty fixture

Hermetic `journalctl` stub, argv-driven (scope flag + `MESSAGE_ID=`/`COREDUMP_SIGNAL=11`),
never the host journal. Fixture env: `MORI_BOOT_ID=0123456789abcdef0123456789abcdef` (the
census's expected boot anchor), `MORI_TIMEOUT_BIN` present, no `MORI_FIXTURE` skip marker.
Every record carries `_BOOT_ID` equal to that anchor; the sig11 records also carry
`MESSAGE_ID=fc2e22bc…`.

Declared matrix (records per scope/class) — the implementation's positive selftest fixture:

| class | user | system | query / required record fields |
|---|---|---|---|
| `kernel_oom_notice` | 3 | 5 | `MESSAGE_ID=fe6faa94e7774663a0da52717891d8ef` |
| `oomd_notice` | 0 | 2 | `MESSAGE_ID=d989611b15e44c9dbf31e3c81256e4ed` |
| `coredump_notice` | 1 | 0 | `MESSAGE_ID=fc2e22bc6ee647b6b90729ab34a250b1` |
| `segfault_signal11` | 1 | 0 | `MESSAGE_ID=fc2e22bc… COREDUMP_SIGNAL=11` |
| `unit_sigkill_record` | 1 | 0 | `MESSAGE_ID=98e322203f7a4ed290d09fe03c09fe15 EXIT_CODE=killed EXIT_STATUS=9` |
| `unit_failure_record` | 1 | 0 | `MESSAGE_ID=d9b373ed55a64feb8242e02dbe79a49c` |

Arms (each run is one census invocation, `env -i`):

| arm | stub behavior | expected journal rows | expected verdict |
|---|---|---|---|
| `matrix` | table above, no `MESSAGE` key | both `ok`; all cells exact; positive findings for user 3/1/1/1/1 and system 5/2; `kernel_oom_notice/oomd_notice/coredump_notice` findings `unit=notice`, `segfault/sigkill/failure` findings `unit=record`; `KILL_SIGNAL_JOURNAL` is `warn`, `count=1`, `scope=user`, `signal=9`, `attribution=none`; every other positive journal finding `info`; `trust=client-supplied`, `field=user:MESSAGE_ID`, `oomd_activity=unmeasured`; `unmeasured=` names the three dropped text classes | **DRIFT rc1**, `drift=1` from the single warn (the overall `unavailable=` count depends on unrelated quiet-surface stubs and is not asserted here) |
| `leak` | same counts, every record adds `"MESSAGE":"<canary>"` | same rows/cells/findings; canary absent from stdout+stderr; no `"MESSAGE"` key echoed | DRIFT rc1 (same warn) |
| `empty` | all JSON queries rc0, empty | both `ok`; every cell `0`; `boot=unavailable:no-records` | CLEAN rc0 |

Additional invariants: exactly two journal-scope rows; no `total=`/`sum=`/`victim=`/`caused=`
token anywhere in the journal rows or findings; exactly one grammar-valid `MORI_CENSUS` line
with rc agreement; no shell diagnostics (`integer expected`, `line N: [: `); no finding with
`count=0`; `JOURNAL_CLASSES_UNMEASURED` (`info`, naming `oom_kill_text`, `other_signals`,
`other_unit_failure_text`) present in every arm. In `matrix`, the only WARN journal finding is
`KILL_SIGNAL_JOURNAL`; every notice-class finding is INFO. If a future policy makes another
class WARN, the verdict cell re-anchors while the cell/unit checks stand.

**Before witness:** frozen census has no `journal.user`/`journal.system` rows and reports the
text classes (`oom_kill=7 kill_signal=2 unit_failure=2` on the same decoy text; `segfault=1`
from the JSON arm) with `MORI_CENSUS: DRIFT`. C1-MATRIX-A is `0/3` before and must be `3/3`
after.

### 3.1b C1-MATRIX-B — failure/rejection arms via the census selftest

The failure channels are one-knob behavioral cases in the census's own hermetic selftest. L1
requires all of these exact labels to PASS on the integrated bytes (and records that the 13
`journal:` labels are absent from the frozen selftest):

```
journal: per-scope catalog counts; user unit SIGKILL is the only warn
journal: legacy text ids are not counted (Q15)
journal: user producer rc1 -> user unavailable, system still counted
journal: system producer rc2 -> system unavailable, user ok
journal: system producer rc1 -> system unavailable, user still counted
journal: nonempty stderr -> unavailable, never counted
journal: malformed JSON -> unavailable, never 0
journal: record identity mismatch -> unavailable
journal: record from another boot -> unavailable
journal: records from several boots -> unavailable:multi-boot
journal: absent JSON parser -> both scopes unavailable, no counts
journal: absent journalctl -> both scopes unavailable
journal: invalid boot anchor -> both scopes unavailable
clean: empty journal
```

The exact expected token for each is the class token on the affected row
(`<class>=unavailable:<reason>`), with the other scope's cells still counted where the case is
single-scope. The absent-tool/parser and invalid-boot cases are row-level: both rows
`unavailable` with `journalctl=missing`, `parser=missing`, or `boot_id=unavailable`, and no
count tokens. The first case is the positive matrix above (user 3/0/1/1/1/1, system
5/2/0/0/0/0, DRIFT). The `clean: empty journal` case must now match both `journal.user: ok` and
`journal.system: ok` rows (the old single-row regex `^SURFACE journal: ok` must be updated, not
left as a second source).

Why this split: the independent fixture (A) prevents self-attestation on the positive/leak/empty
path; the selftest (B) is the established rc/fixture mechanism for the failure matrix. The
`no-timeout-bin` journal channel and the `timeout` reason are **not** in this label set; they are
named residuals (§7).

### 3.2 C1-LIVE — live bracket parity and MESSAGE-free output

One census run; two independent reads per cell around it; same boot. The census's expected boot
anchor is `MORI_BOOT_ID` when set, otherwise `/proc/sys/kernel/random/boot_id`; it must be 32
lowercase hex (`mori-census.sh:315-316`). `timeout` must exist (the probe refuses an unbounded
scan with `unavailable:no-timeout-bin`). Commands (counts only, `--output-fields` never contains
`MESSAGE`; capture then count, no producer into an early-exit reader):

```bash
LANE=/home/vgpnk/Projects/shokunin/mori-shokunin
EVID=/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/evidence/round13-count-<UTC>
OUT=$EVID/20-c1-live.out
BOOT0=$(cat /proc/sys/kernel/random/boot_id)
command -v timeout >/dev/null || { echo "C1_LIVE: no-timeout-bin"; exit 1; }
bash "$LANE/tools/mori-census.sh" >"$OUT" 2>&1; RC=$?
BOOT1=$(cat /proc/sys/kernel/random/boot_id)
```

Per cell, with `S` in `user|system` and the class table below:

```bash
pre_out=$EVID/20-pre-$S-$CLS.out; pre_err=$EVID/20-pre-$S-$CLS.err
journalctl --"$S" -b -q --no-pager -o json --output-fields="$FIELDS" "$@" \
  >"$pre_out" 2>"$pre_err"; pre_rc=$?
pre=$(awk 'NF{n++} END{print n+0}' "$pre_out")
# … census already ran …
post_out=$EVID/20-post-$S-$CLS.out; post_err=$EVID/20-post-$S-$CLS.err
journalctl --"$S" -b -q --no-pager -o json --output-fields="$FIELDS" "$@" \
  >"$post_out" 2>"$post_err"; post_rc=$?
post=$(awk 'NF{n++} END{print n+0}' "$post_out")
```

Cells and query arguments:

| class | `FIELDS` | match args |
|---|---|---|
| kernel_oom_notice | `_BOOT_ID,MESSAGE_ID` | `MESSAGE_ID=fe6faa94e7774663a0da52717891d8ef` |
| oomd_notice | `_BOOT_ID,MESSAGE_ID` | `MESSAGE_ID=d989611b15e44c9dbf31e3c81256e4ed` |
| coredump_notice | `_BOOT_ID,MESSAGE_ID` | `MESSAGE_ID=fc2e22bc6ee647b6b90729ab34a250b1` |
| segfault_signal11 | `_BOOT_ID,MESSAGE_ID,COREDUMP_SIGNAL` | `MESSAGE_ID=fc2e22bc6ee647b6b90729ab34a250b1 COREDUMP_SIGNAL=11` |
| unit_sigkill_record | `_BOOT_ID,MESSAGE_ID,EXIT_CODE,EXIT_STATUS` | `MESSAGE_ID=98e322203f7a4ed290d09fe03c09fe15 EXIT_CODE=killed EXIT_STATUS=9` |
| unit_failure_record | `_BOOT_ID,MESSAGE_ID` | `MESSAGE_ID=d9b373ed55a64feb8242e02dbe79a49c` |

Pass conditions:

1. `BOOT0 == BOOT1`; `BOOT0` is 32 lowercase hex; every printed `boot=<32hex>` equals `BOOT0`
   (or is `unavailable:no-records` when that scope had no records).
2. For a readable cell (`pre_rc == post_rc == 0` and both stderr files empty): the census token
   is an integer `n` with `min(pre,post) <= n <= max(pre,post)`. A numeric token when either
   read failed is a false count; an `unavailable:*` token when both reads succeeded is a false
   unavailable.
3. If a read fails or its stderr is nonempty, the census token for that scope/class must be
   `unavailable:rc-<rc>`, `unavailable:stderr-nonempty`, `unavailable:timeout`, or
   `unavailable:no-timeout-bin`; the run is `C1_LIVE: partial`, and **coverage cannot move**
   (see §6).
4. Exactly one grammar-valid `MORI_CENSUS` line whose word matches rc; no
   `"MESSAGE"` key and no `MESSAGE=` token in stdout+stderr.
5. At least one cell with `pre=post=0` must have `pre_rc=0` and empty stderr (valid-empty
   proof). Record `empty_query=ok`; if no zero cell exists in this boot, record
   `not-observed` and rely on C1-MATRIX-A `empty`.

Expected on this host: the `fe6faa94…`/`d989…` counts are small (r12 measured 7 user / 9 system
and 0/0 in one boot); `fc2e22bc…` is large when all-boots are read (CatalogSource measured
1585 user / 1 system without `-b`) but is per-boot here. None of these values is pinned.

### 3.3 C1-REGRESS

- `bash tools/mori-census.sh --selftest` → `MORI_CENSUS_SELFTEST: PASS (N cases, N passed,
  0 failed)`, exit 0, stderr empty; `N >= 77 +` the new journal/F01 cases; all 13 `journal:`
  labels and `clean: empty journal` PASS.
- Honest oracle unchanged: `MORI_SILENCE_CASES: matched=28 total=28`, exit 0.
- Live census reaches exactly one verdict, exits 0 or 1 (not 2), and prints no shell
  diagnostics. A live DRIFT is acceptable if the warn path is real; the counter grades the
  verdict's consistency, not a required word.
- `surfaces=` grows by one (two journal rows replace one; `7 -> 8`); the number is recorded,
  never asserted as a fixed target outside the fixture.

Required selftest labels (exact strings in the final census; L1 greps `^PASS <label>`):

```
journal: per-scope catalog counts; user unit SIGKILL is the only warn
journal: legacy text ids are not counted (Q15)
journal: user producer rc1 -> user unavailable, system still counted
journal: system producer rc2 -> system unavailable, user ok
journal: system producer rc1 -> system unavailable, user still counted
journal: nonempty stderr -> unavailable, never counted
journal: malformed JSON -> unavailable, never 0
journal: record identity mismatch -> unavailable
journal: record from another boot -> unavailable
journal: records from several boots -> unavailable:multi-boot
journal: absent JSON parser -> both scopes unavailable, no counts
journal: absent journalctl -> both scopes unavailable
journal: invalid boot anchor -> both scopes unavailable
clean: empty journal
```

---

## 4. C2 — operability counters

### 4.1 C2-F01 — long-history exact authorship

Fixture: audit-r11 Appendix B, reproducible generator (committed with the harness/digest):
a stub `git` answers `rev-parse`/`ls-files`/`cat-file` and a `log` stream of
`%ct %an <%ae>` rows; one exact `kagi-shokunin <kagi@shokunin.local>` row at position 1,
then 12,000 `aggregator-shokunin <aggregator@shokunin.local>` rows; launch `1699998000`,
NOW `1700000000`, all rows in `(launch, NOW]`; `MORI_ROSTER_LANES=kagi`,
`MORI_LANE_SILENCE_S=900`; the ledger is the fixture `watchdog.log`.

| arm | rows | expected after | expected before (frozen) |
|---|---|---|---|
| subject-first | 1 subject + 12,000 siblings | `SURFACE lane.kagi: progressing (` + `basis=row-A` + `subject_commits=yes`; rc 0; `MORI_CENSUS: CLEAN` | `progressing-weak (` + `basis=row-C` + `other_authored_commits=12001` (audit) |
| sibling-only control | 12,000 siblings | `progressing-weak (` + `basis=row-C` + `other_authored_commits=12000` | same (control must not flip) |
| short subject control | 1 subject, 0 siblings | `progressing (` + `basis=row-A` | same |

`C2-F01` passes after only if all three arms match, the subject arm is 1/1 (repeat 10 if the
operator wants a stability number; the failure is deterministic at 12,001 lines, so one run is
the minimal counter), and `R13_MUTATION_F01_RED_BEFORE` reproduces row-C when the frozen
`grade_lane` is transplanted into the fixed census. The claim is bounded to this fixture class;
it does not assert that every real host history behaves this way.

### 4.2 C2-F02 — final-roll integrity matrix

Six proxy censuses, each invoking the real census and rewriting only the final roll/rc. Pinned
`MORI_SHUFFLE_SEED=7 MORI_RUN_NONCE=11`. Expected after (pre-registered from ReviewOracle §4
and the in-flight `verdict_grade`):

| proxy | transform | after: matched/total, rc | after: reason head | before (frozen) |
|---|---|---|---|---|
| honest | passthrough | 28/28, 0 | none | 28/28, 0 |
| banana | `CLEAN\|DRIFT` → `BANANA`, rc kept | **0/28**, 1 | `malformed` | 28/28, 0 (audit) |
| duplicate | append a second valid `MORI_CENSUS:` line | **0/28**, 1 | `duplicate` | 28/28, 0 [INFERENCE, first-line-only read] |
| missing | delete every `MORI_CENSUS:` line | **0/28**, 1 | `missing` | 2/28, 1 [INFERENCE: 26 assert cases fail, readonly/shape pass] |
| clean-rc1 | force `CLEAN`, exit 1 | **0/28**, 1 | `inconsistent` | <28, 1 [INFERENCE: silent cases' rc wants match, verdict unchecked] |
| drift-rc0 | force `DRIFT`, exit 0 | **0/28**, 1 | `inconsistent` | <28, 1 [INFERENCE: non-silent cases pass rc, silent cases fail] |

Additional after-conditions:

- Each invalid run's `FAIL` set includes `shape-invariance` and `readonly-no-mutation` (the two
  guards that bypassed `assert_case` in the baseline) and at least one ordinary lane case
  (`subject-postlaunch-progressing`).
- Per-case `FAIL` lines carry no run nonce (`grep '^FAIL ' | grep -c "nonce-$N"` → 0).
- `CASE_ORDER` still lists exactly the 28 registered ids; wants are unchanged; shuffle/nonce
  are still seeded (two pinned runs are byte-identical).
- `R13_MUTATION_F02_RED_BEFORE` accepts the BANANA proxy 28/28 when the frozen `assert_case`
  is transplanted into the fixed oracle.

Everything else (`tally=findings=999`, aggregate vacuity, registry cardinality) remains a named
residual; see §7.

---

## 5. Exact L1 command sequence

Run from the lane root; every output is retained under one evidence directory. `P0`/`P1` are
read-only; `P2` writes only under `--output`.

```bash
LANE=/home/vgpnk/Projects/shokunin/mori-shokunin
cd "$LANE"
EVID=$LANE/corpus/evidence/round13-count-$(date -u +%Y%m%dT%H%M%SZ)
mkdir -p "$EVID"

# P0 — bytes under test
{
  sha256sum tools/mori-census.sh tools/mori-silence-cases.sh tools/mori-round13-regressions.py
  jq -r '"base_commit=" + .base_commit, (.sha256 | to_entries[] | .key + "=" + .value)' \
    .ufo/waves/round-13/frozen/inputs.json
} | tee "$EVID/00-bytes.txt"

# P1 — census selftest (C1-MATRIX-B labels + F01 case live here)
bash tools/mori-census.sh --selftest >"$EVID/01-selftest.log" 2>&1
echo "selftest_rc=$?" | tee -a "$EVID/01-selftest.log"
tail -n 1 "$EVID/01-selftest.log"
grep -cE '^PASS journal:' "$EVID/01-selftest.log"                 # expect 13
grep -c '^PASS clean: empty journal' "$EVID/01-selftest.log"      # expect 1

# P2 — harness strict (after its C1 parser is aligned with the emitted grammar)
python3 tools/mori-round13-regressions.py --output "$EVID/regressions-strict" \
  >"$EVID/02-strict.log" 2>&1
echo "strict_rc=$?"
grep -E '^FINDING R13_(C1|F01|F02)' "$EVID/02-strict.log"

# P2b — harness baseline: frozen bytes must reproduce the defects
python3 tools/mori-round13-regressions.py --baseline --output "$EVID/regressions-baseline" \
  >"$EVID/03-baseline.log" 2>&1
echo "baseline_rc=$?"
grep -E '^FINDING R13_(C1|F01|F02)' "$EVID/03-baseline.log"

# P2c — frozen-function transplants must go red again
python3 tools/mori-round13-regressions.py --mutation both --output "$EVID/regressions-mutation" \
  >"$EVID/04-mutation.log" 2>&1
echo "mutation_rc=$?"
grep -E '^FINDING R13_MUTATION' "$EVID/04-mutation.log"
```

`P2` is authoritative only after the harness's C1 parser speaks the emitted row grammar (the
final census emits two `SURFACE journal.user`/`journal.system` rows, six classes,
`oomd_activity=unmeasured`, and `unmeasured=oom_kill_text,other_signals,other_unit_failure_text`;
the current harness expects one `SURFACE journal:` row, four classes, `sum=none`, and the older
`unmeasured` list — see §7). If it is stale at integration time, L1 records the mismatch as a
harness defect and uses `P1` + `P3` + `P4` for the C1 verdict; it must not score a
stale-parser failure as a census failure. The harness exit also includes `R13_SHONEN_*`; those
belong to the separate Q28 claim, so the C1/C2 gate reads only the `R13_C1`, `R13_F01`,
`R13_F02`, and `R13_MUTATION_*` claim statuses.

Oracle matrix (independent of the harness; exact bytes in the evidence dir):

```bash
W=$EVID/wrappers; mkdir -p "$W"
CENSUS_Q=$(printf '%q' "$LANE/tools/mori-census.sh")

cat >"$W/honest.sh" <<EOF
#!/usr/bin/env bash
exec bash $CENSUS_Q "\$@"
EOF
cat >"$W/banana.sh" <<EOF
#!/usr/bin/env bash
set +e
out=\$(bash $CENSUS_Q "\$@" 2>&1); rc=\$?
out=\${out//MORI_CENSUS: CLEAN/MORI_CENSUS: BANANA}
out=\${out//MORI_CENSUS: DRIFT/MORI_CENSUS: BANANA}
printf '%s\n' "\$out"; exit "\$rc"
EOF
cat >"$W/duplicate.sh" <<EOF
#!/usr/bin/env bash
set +e
out=\$(bash $CENSUS_Q "\$@" 2>&1); rc=\$?
roll=\$(printf '%s\n' "\$out" | grep -m1 '^MORI_CENSUS:' || true)
printf '%s\n' "\$out"
[ -n "\$roll" ] && printf '%s\n' "\$roll"
exit "\$rc"
EOF
cat >"$W/missing.sh" <<EOF
#!/usr/bin/env bash
set +e
out=\$(bash $CENSUS_Q "\$@" 2>&1); rc=\$?
kept=''
while IFS= read -r ln; do
  case "\$ln" in MORI_CENSUS:*) continue ;; esac
  kept="\$kept\$ln"\$'\n'
done <<<"\$out"
printf '%s' "\$kept"; exit "\$rc"
EOF
cat >"$W/clean-rc1.sh" <<EOF
#!/usr/bin/env bash
set +e
out=\$(bash $CENSUS_Q "\$@" 2>&1)
out=\${out//MORI_CENSUS: DRIFT/MORI_CENSUS: CLEAN}
printf '%s\n' "\$out"; exit 1
EOF
cat >"$W/drift-rc0.sh" <<EOF
#!/usr/bin/env bash
set +e
out=\$(bash $CENSUS_Q "\$@" 2>&1)
out=\${out//MORI_CENSUS: CLEAN/MORI_CENSUS: DRIFT}
printf '%s\n' "\$out"; exit 0
EOF
chmod 700 "$W"/*.sh

for tag in honest banana duplicate missing clean-rc1 drift-rc0; do
  MORI_SHUFFLE_SEED=7 MORI_RUN_NONCE=11 \
    bash "$LANE/tools/mori-silence-cases.sh" "$W/$tag.sh" \
    >"$EVID/30-oracle-$tag.log" 2>&1
  echo "$tag rc=$?"
  grep -E '^MORI_SILENCE_CASES:' "$EVID/30-oracle-$tag.log"
  grep -cE '^FAIL ' "$EVID/30-oracle-$tag.log"
  grep -cE '^FAIL (shape-invariance|readonly-no-mutation|subject-postlaunch-progressing)' \
    "$EVID/30-oracle-$tag.log"
  grep '^FAIL ' "$EVID/30-oracle-$tag.log" | grep -c 'nonce-' || true
done
```

Expected after: the table in §4.2 with **exact** `0/28` for the five invalid proxies, rc 1, and
the three guard/lane ids in each FAIL set. Expected before: honest 28/28 rc0; banana (and
[INFERENCE] duplicate) 28/28 rc0; the other three `<28` rc1.

Live C1 parity: run the §3.2 loop, retain `20-c1-live.out` plus the per-cell numbers. The
minimal assertion block is:

```bash
grep -c '^SURFACE journal\.\(user\|system\):' "$OUT"          # 2
grep -c '^MORI_CENSUS:' "$OUT"                                # 1
grep -Ec '"MESSAGE"[[:space:]]*:|(^|[^_])MESSAGE=' "$OUT"      # 0
```

and the bracket comparison per cell. No fixed live count is written into the report.

---

## 6. Score mapping (6 -> 7 only if measured)

Current owned scores: **coverage 6, operability 6** (round-12 table/§ corrections). A claim
moves its axis only when every required counter below passes on the integrated bytes and no
regression check fails. Verdict cells use only the four admitted values; qualifications go in
the evidence cell.

| axis | move to 7 iff | hold at 6 with verdict `unchanged` if | verdict `harmed` if |
|---|---|---|---|
| **coverage** | `C1-MATRIX-A 3/3` after (and 0/3 before); `C1-MATRIX-B` all 13 `journal:` labels + `clean: empty journal` PASS; `C1-LIVE` 12/12 cells bracketed, same boot, one well-formed verdict, MESSAGE-free, at least one valid-empty proof; `C1-REGRESS` clean | any C1-MATRIX-A arm or required selftest label fails; any live cell is a false count/false unavailable; system scope unreadable at gate time (record `unavailable`, FR1 live count unproven); selftest new cases absent | selftest fails; honest oracle <28; census exits 2 or prints no/duplicate verdict; a new shell diagnostic appears |
| **operability** | `C2-F01` subject arm `progressing/row-A`, sibling control `progressing-weak/row-C count=12000`, short control `progressing/row-A`, mutation F01 red; `C2-F02` honest 28/28 rc0 and all five proxies **0/28 rc1** with the expected reason heads and guard ids; mutation F02 red; `C2-REGRESS` clean | any F01 arm fails; any proxy `matched>0` (partial bypass), wrong rc, or missing guard id; reason head changes but rejection is exact 0/28 and rc1 (re-anchor the diagnostic, do not claim the pre-registered head) | honest oracle <28; registry ids/wants changed; pinned runs not byte-identical; selftest fails |

Mapping notes:

- `C1-MATRIX-A` passing while `C1-LIVE` is unreadable is **not** a score move: the plan's falsifier
  for FR1 is a live count; fixture behavior alone is a capability demonstration. Report the
  coverage row as `unchanged` with the `unavailable` residual in the evidence cell.
- `C2-F02` repair is a measurable operability move even though the BANANA proxy is synthetic:
  the oracle is the lane's own gate, and the counter grades its acceptance behavior exactly.
- `C2-F01`'s claim is bounded to the Appendix-B fixture class (one synthetic long history). Do
  not write "production histories repaired"; write "the witnessed long-history class no longer
  loses exact authorship".
- The round's third planned item (freshness re-pin) is **not** part of this mapping. The r10
  drift baseline is expected red after C1's schema change; that is disclosed drift, not a
  regression, and no re-pin is credited here.

Suggested SCORECARD rows (evidence cell carries the numbers, verdict cell stays four-value):

```
| coverage | improved | 6 -> 7 | C1-A 3/3 + 13 journal labels + clean-empty; C1-LIVE 12/12 bracket, boot stable, MESSAGE-free; selftest N/N; oracle 28/28 |
| operability | improved | 6 -> 7 | F01 progressing/row-A + sibling row-C 12000; F02 honest 28/28 + 5x0/28 rc1 (malformed/duplicate/missing/inconsistent); mutations red |
```

Capabilities that may enter only with the above passing: `structured journal scopes` (C1-LIVE
evidence), `verdict-integrity oracle` (F02 matrix), `long-history authorship` (F01 fixture).

---

## 7. Named residuals and blockers (claim boundaries)

1. **Harness C1 parser vs emitted grammar (blocker for using `P2` as the C1 gate).** The
   in-flight census emits two rows (`journal.user`, `journal.system`), six classes, and an
   `unmeasured=oom_kill_text,other_signals,other_unit_failure_text` list. The current
   `tools/mori-round13-regressions.py` calls `surface_body` with `^SURFACE journal:` (one row),
   expects four classes, `sum=none`, and the older `unmeasured` list; it will report C1 claims
   failed on correct census bytes. Fix the harness parser/fixture or L1 must use the §3 commands
   and record the harness mismatch as an integration defect. (Message sent to RegressionHarness;
   no edit by this seat.)
2. **Harness `--baseline` status bugs.** `R13_C1_NO_MESSAGE_TEXT` includes a structured-count
   precondition in baseline mode and `R13_C1_CLEAN_VERDICT` requires post-fix tokens; both
   predict `BASELINE_DEVIATION` on frozen bytes, which is outside `BASELINE_SUCCESS` and makes
   `--baseline` exit 1. They should be `BASELINE_OK`/`EXPECTED_DEFECT`. Until fixed, treat
   `--baseline` per-claim statuses, not its exit code, as the pre-fix witness.
3. **Tally-count blindness remains (F02 residual).** `verdict_grade` checks grammar,
   cardinality and word/rc, not `findings/drift/unavailable/surfaces` arithmetic
   (ReviewOracle M3). A proxy that changes `findings=1` to `findings=999` still scores 28/28.
   The round does not claim tally integrity; a count-to-word rule needs a contract statement
   first.
4. **Oracle tally/aggregate residuals (ReviewOracle H1–H4) remain open.** The denominator is
   still "cases that ran", a dropped registry id yields `matched=27 total=27` green, the
   aggregate fallback still defaults to `not-open`, and lane/aggregate rows are first-match.
   C2-F02 closes the verdict channel only; do not report the oracle as fully adversarial.
5. **MESSAGE_ID is a user field.** Any same-UID writer can emit `MESSAGE_ID=fe6faa94…`; the
   count is "records carrying that ID", not an authenticated event, victim, or fleet cause. The
   notice row says `trust=client-supplied`, `unit=notice`; the SIGKILL record finding says
   `attribution=none`. The knowledge note must list spoofing under delivery paths it cannot see
   (QUALITY 17).
6. **Text classes are dropped, not aliased.** The prior text greps (`oom_kill_text` for the
   OOM/kill words, `other_signals` for the signal words, `other_unit_failure_text` for the unit
   failure words) have no one-to-one anchored structured replacement; the census names them
   `unmeasured=` on every row and fires `JOURNAL_CLASSES_UNMEASURED` info. The new
   `unit_sigkill_record` / `unit_failure_record` classes restore part of that coverage via
   catalog IDs (`98e32220…`, `d9b373ed…`; both present in the local catalog). This is a
   disclosed coverage trade, not a silent rename.
7. **C1 fixture boot anchor is explicit, not synthetic.** The final census validates every
   record's `_BOOT_ID` against `MORI_BOOT_ID` (or `/proc/sys/kernel/random/boot_id`) and grades
   a mismatch `boot-mismatch`; the fixture must set `MORI_BOOT_ID` to its 32-hex constant.
   `MORI_BOOT_ID` itself is shape-validated: an invalid anchor makes both scopes unavailable
   (covered by the `journal: invalid boot anchor` label). The live counter's
   `BOOT0 == BOOT1` plus per-row `boot=BOOT0` check covers the host case.
8. **Live bracket limits.** Records added between the two reads widen the interval; a journal
   vacuum inside the window could remove a record from both reads. The check cannot prove the
   absence of a record that never reached the journal, and a `--system` permission denial is
   reported as `unavailable`, never as zero. Both are disclosed rather than converted to a
   pass.
9. **Journal `no-timeout-bin` / `timeout` channels are not in the required label set.** The
   reason vocabulary includes them and the probe refuses an unbounded scan, but the final
   selftest labels do not exercise the journal timeout arm (the existing `no-timeout-bin` case
   is the tmux freshness probe). Named residual; a fixture that points `MORI_TIMEOUT_BIN` at a
   missing path would make every class `unavailable:no-timeout-bin` (not measured this round).
10. **C1-MATRIX-A/B are authored by this seat as a contract, not yet implemented.** A's three
    independent arms and the 14 selftest labels must exist on the integrated bytes (the labels
    are in the final census; the independent arms are the counter to add). The score gate
    requires the arms to run; a missing arm is a failed counter, not a pass by default.
11. **F01 fixture scope.** The 12,001-line fixture is the audit's witnessed class; it does not
    prove every long real history fails or that the fix is the only possible one. The sibling
    and short controls guard against a blunt "large history means progressing" change.

---

## 8. Hand-off summary

- C1 before witness: no per-scope class cells; text classes only (`0/3` independent fixture,
  no `journal:` selftest labels). C1 after: `3/3` independent arms, 13 `journal:` labels +
  `clean: empty journal`, and 12/12 live cells.
- C2 before witness: `progressing-weak/row-C other_authored_commits=12001`; BANANA 28/28 rc0.
  C2 after: `progressing/row-A`; five invalid proxies 0/28 rc1; honest 28/28.
- Score: coverage 6->7 only with C1-MATRIX-A + C1-MATRIX-B + C1-LIVE + C1-REGRESS; operability
  6->7 only with C2-F01 + C2-F02 + C2-REGRESS. Anything less is `unchanged` with the residual
  named; any shared-gate regression is `harmed`.
- L1's first action should be the §5 P0/P1, then confirm the harness C1 parser (blocker 1)
  before treating `P2` as evidence.

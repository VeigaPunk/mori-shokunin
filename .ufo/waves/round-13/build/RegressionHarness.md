# RegressionHarness — round-13 isolated integration regressions

Seat: `MoriR13.RegressionHarness` (executor, leaf). Axes: **coverage (C1)** and
**operability (C2)**. Milestone: round13 structured scopes and verdict
integrity. This seat wrote one new evidence harness and this report; it ran no
tests and made no repository commit.

Deliverable:
`/home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-round13-regressions.py`
(2024 lines, sha256 `3eb29fd136c69f7b47204ad41e96742e1e29f09ed309d2872ed2e726fdab529b`
at authoring). It is an **evidence harness, not a registered gate**: the normal
output ends with `GATE not-registered (evidence harness; --selftest available)`.
If L1 later registers it as a gate, the invocation is
`python3 tools/mori-round13-regressions.py --selftest` (pure logic; reads no
repository or target path).

## 1. Claims and stable finding ids

Every claim prints one line:
`FINDING <id> status=<status> axis=<coverage|operability> observed="…"`.
Stable ids (harness lines in parentheses):

| id | claim |
|---|---|
| `R13_SHONEN_CANONICAL_BYTES` (998) | delivered `SHONEN.md` bytes equal the unindented 8-line HEAD seed, sha256 `508d5b46…` |
| `R13_SHONEN_INDENT_WITNESS` (998) | the same comparator rejects an indented witness (able-to-fail proof for the comparison) |
| `R13_C1_SYSTEM_NOTICE_COUNTS` (1062) | `SURFACE journal.system` carries `kernel_oom_notice=2`, `oomd_notice=1`, `coredump_notice=3`, `segfault_signal11=3`, record classes 0, and the four positive `*_JOURNAL_SYSTEM` findings with those counts |
| `R13_C1_USER_SCOPE_INDEPENDENT` (1062) | a separate `SURFACE journal.user` row with all six classes `=0`, its own `boot` anchor, no summed field, and no zero-count user finding |
| `R13_C1_USER_SCOPE_NONZERO` (1062) | a user-only fixture (`kernel=3`, `oomd=0`, `coredump=1`, `segfault=1`) lands only on user tokens/findings while the system row stays 0 |
| `R13_C1_NO_MESSAGE_TEXT` (1062) | synthetic canary, `"MESSAGE":` key and `MESSAGE=` value absent from primary and leak-forcing runs, while structured counts survive |
| `R13_C1_CLEAN_VERDICT` (1062) | notices are INFO: one well-formed `CLEAN` roll with rc 0, `unit=notice field=user:MESSAGE_ID`, `unmeasured=oom_kill_text,other_signals,other_unit_failure_text`, `JOURNAL_CLASSES_UNMEASURED`, no positive kill/unit-failure row |
| `R13_F01_EXACT_AUTHOR_LONG_HISTORY` (1325) | Appendix-B history: exact subject author plus 12,000 sibling log lines grades `progressing basis=row-A subject_commits=yes`, rc 0 CLEAN |
| `R13_F01_SIBLING_CONTROL_LONG_HISTORY` (1325) | 12,000 sibling-only lines grade `progressing-weak basis=row-C other_authored_commits=12000` |
| `R13_F02_HONEST_28_OF_28` (953, 1413) | honest census through the oracle: `matched=28 total=28`, rc 0 |
| `R13_F02_REJECT_BANANA` | substituted roll rejected: `matched=0`, rc 1, reason head `malformed` |
| `R13_F02_REJECT_DUPLICATE_VERDICT` | two rolls rejected: `0/28`, rc 1, `duplicate` |
| `R13_F02_REJECT_MISSING_VERDICT` | no roll rejected: `0/28`, rc 1, `missing` |
| `R13_F02_REJECT_NOT_FINAL_VERDICT` | trailing line after the roll rejected: `0/28`, rc 1, `not-final` |
| `R13_F02_REJECT_VERDICT_FIRST` | roll moved off the last line rejected: `0/28`, rc 1, verdict-contract failure |
| `R13_F02_REJECT_CLEAN_DRIFT9` | `CLEAN (… drift=9 …)` rejected: only the six/seven DRIFT fixtures pass, rc 1, `inconsistent` |
| `R13_F02_REJECT_DRIFT_DRIFT0` | `DRIFT (… drift=0 …)` rejected: only the 21/22 CLEAN fixtures pass, rc 1, `inconsistent` |
| `R13_F02_REJECT_CLEAN_RC1` | rc forced 1 (rc-only proxy): only the six/seven DRIFT fixtures pass, rc 1, `inconsistent` |
| `R13_F02_REJECT_DRIFT_RC0` | rc forced 0 (rc-only proxy): only the 21/22 CLEAN fixtures pass, rc 1, `inconsistent` |
| `R13_MUTATION_F01_RED_BEFORE` (1572–1699) | swap the frozen `grade_lane` into a copy of the fixed census → exact-author arm regresses to `progressing-weak row-C` |
| `R13_MUTATION_F02_RED_BEFORE` (250, 1572–1699) | replace only the fixed verdict gate's body with pre-fix prefix-presence (all call sites) → BANANA accepted `28/28`, rc 0 |

Selective wrappers encode the **PASS set**, not a blanket tally (lines 1413–1483):
the six silent fixtures are `silent-open`, `same-round-relaunch-silent`,
`legacy-steer-open-silent`, `old-report-before-relaunch-silent`,
`report-eq-launch-no-close`, `main-repo-noise-silent`; `report-future-no-close`
is the only `auto` case and is allowed to pass only on the side consistent with
its own observed state. The 28 ids are hardcoded in the runner (lines 164–193),
an independent expected contract — the runner does not read the oracle source.
It deliberately does **not** cross-count `surfaces=`/`unavailable=`
(OracleFix: lane rows bypass `emit_surface`).

Exit codes: `0` every claim satisfied in the selected mode; `1` a contract or
baseline claim failed; `2` usage/setup (including `snapshot_tampered`); `3` all
contract claims held but a requested mutation could not be built. Discovery of
the reason head is tolerant (`MORI_CENSUS verdict <word>`), while BANANA,
duplicate, missing and not-final additionally require their named heads.

## 2. Fixture fidelity

**F01 long history (audit-r11 Appendix B).** `build_history_fixture` (658) and
`git_stub_body` (539) create a stub `git` that answers `rev-parse`/`ls-files`/
`cat-file` and emits one optional exact `kagi-shokunin <kagi@shokunin.local>`
line followed by 12,000 `aggregator-shokunin` lines. Ledger
`TIMESTAMP launch kagi round=7 ts=1699998000`, `MORI_NOW_EPOCH=1700000000`,
`MORI_LANE_SILENCE_S=900`. The exact-author arm is the 12,001-line writer into
the membership test; the sibling-only arm is the 12,000-line control. No real
repository or lane history is read.

**F02 proxies (audit-r11 Appendix C and OracleFix's final gate).**
`write_wrapper` (844) generates a real census proxy for each family: BANANA
substitution, duplicate roll, roll removal, trailing `TRAILER x`, roll moved to
the first line, `CLEAN drift=9`, `DRIFT drift=0`, rc-only `CLEAN rc1`, rc-only
`DRIFT rc0`, and an honest `exec` passthrough. Each wrapper preserves the
census output (including the run nonce) and only the named roll/rc property is
altered. The oracle is invoked with pinned `MORI_SHUFFLE_SEED=1313` and
`MORI_RUN_NONCE=1313` so case order and fixture tokens are reproducible; the
oracle strips them from the census process tree itself.

**C1 structured scopes (CensusFix final schema).** `journal_stub_body` (433)
implements the documented argv exactly: `<--user|--system> -b --no-pager
-o json --output-fields=… MESSAGE_ID=<id>` plus the two record-class queries
(`MESSAGE_ID=fc2e22… COREDUMP_SIGNAL=11`, `MESSAGE_ID=98e322… EXIT_CODE=killed
EXIT_STATUS=9`, `MESSAGE_ID=d9b373…`). It keys by scope **and** class: a
MESSAGE_ID query returns only that id's records; `COREDUMP_SIGNAL=11` returns
only the coredump records; any other structured filter returns zero records at
rc 0 (a valid empty query). A mismatched id cannot receive a fixed record.
Records carry `_BOOT_ID=0123456789abcdef0123456789abcdef`; the harness exports
`MORI_BOOT_ID` to the same value. `--output-fields` without `MESSAGE` omits the
canary; the leak-forcing arm always includes `"MESSAGE":"<synthetic canary>"`.
The canary is synthetic (`R13-SYNTHETIC-JOURNAL-MESSAGE-CANARY`); no host
journal is opened, and no real MESSAGE is read or retained.

Fixtures (primary zero-user, leak-forcing, user-only nonzero) live under the
explicit `--output` tree, never under the repository or a live MORI path, and
are removed unless `--keep-fixtures`.

**SHONEN.** The expected bytes are the unindented HEAD seed (210–228), sha
`508d5b46…`, compared byte-for-byte with line/byte offset on mismatch. An
indented witness is constructed from the same constant and must be rejected.
The previously seen indented working-tree copy (`ac3a436e…`) was a raw-block
transcription artifact caught by ReviewPromotion, not the final defect; the
harness reports a mismatch if it reappears.

## 3. Evidence retention and snapshot verification

`snapshot_verify` (709) runs before any behavior or output write. It verifies
both the default `--frozen-dir` `inputs.json` and the sibling `inputs.json` of
any explicitly named target. The frozen `inputs.json`
(`base_commit=6531ac6029e200a6392bb76673b6a17d3c895c96`) declares:

| file | sha256 |
|---|---|
| `mori-census.sh` | `3da5b098dc23aeb3e1c31ce82664b24a22c2847a168308a755525593881b3164` |
| `mori-silence-cases.sh` | `448f77238c73a5c929a898dad0f0c495fd2a66cc4b90a00ae84ede69a86beeb5` |

A missing or mismatched file raises `SnapshotTampered`; `main` prints
`FINDING R13_SNAPSHOT_TAMPERED status=fail axis=operability …`, then
`MORI_R13_REGRESSIONS: setup snapshot_tampered exit=2`, writes evidence, and
exits 2. A tampered snapshot cannot produce a behavior run.

Every run is retained under `<output>/runs/<run-id>.{stdout,stderr}` with argv,
cwd, rc, timeout flag, duration, byte counts, sanitized-output sha256, and the
synthetic env. `<output>/evidence.json` holds the schema, generation timestamp,
target and frozen-input digests, claim list, ordered run list, mutation records
and summary; canary text is redacted before writing.

## 4. Exact invocation for L1 (run once, after seats finish)

Use absolute paths. Strict contract:

```bash
python3 /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-round13-regressions.py \
  --census /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-census.sh \
  --oracle /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-silence-cases.sh \
  --output /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-13/evidence/regressions-strict
```

Frozen baseline (paths may be omitted; `--baseline` defaults to the frozen dir,
which is digest-verified):

```bash
python3 /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-round13-regressions.py \
  --baseline \
  --output /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-13/evidence/regressions-baseline
```

Mutation red-before (strict suite plus exact-locus reverts):

```bash
python3 /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-round13-regressions.py \
  --census /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-census.sh \
  --oracle /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-silence-cases.sh \
  --mutation both \
  --output /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-13/evidence/regressions-mutation
```

Snapshot-tamper negative (stable setup token):

```bash
cp -a /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-13/frozen /tmp/r13-tamper
printf '#\n' >> /tmp/r13-tamper/mori-census.sh
python3 /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-round13-regressions.py \
  --census /tmp/r13-tamper/mori-census.sh \
  --oracle /tmp/r13-tamper/mori-silence-cases.sh \
  --output /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-13/evidence/regressions-tamper
```

Selftest (no repository or target read):

```bash
python3 /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-round13-regressions.py --selftest
```

## 5. Expected gradient

**Strict** with the fixed scripts: `MORI_R13_REGRESSIONS: claims=19 pass=19
exit=0`. Supporting observations: honest oracle `28/28` rc 0; BANANA,
duplicate, missing, not-final and verdict-first `0/28` rc 1 with their reason
heads (verdict-first only requires a verdict-contract failure); clean-rc1 and
clean-drift9 `6` or `7`/28 rc 1 `inconsistent`; drift-rc0 and drift-drift0
`21` or `22`/28 rc 1 `inconsistent`; F01 subject `progressing row-A`, sibling
`progressing-weak row-C other_authored_commits=12000`; C1 rows exactly
`system kernel=2 oomd=1 coredump=3 segfault=3`, `user` all 0 (zero arm) and
`user kernel=3 oomd=0 coredump=1 segfault=1` with system 0 (nonzero arm); user
zero row boot anchor `unavailable:no-records` is accepted as the landed probe's
correct zero rendering (a nonzero row must show the 32-hex boot).

**Baseline** (frozen): exit 0 with the audit-predicted pre-fix defects —
`baseline-ok=4` (honest oracle 28/28, SHONEN canonical, indented witness, no
MESSAGE text), `expected-defect=11` (C1 system/user/nonzero/clean schema gaps;
F01 exact-author `progressing-weak`; BANANA, duplicate, not-final,
verdict-first, clean-drift9, drift-drift0 accepted `28/28`), 
`baseline-rejected=3` (missing `1/28` — the frozen readonly guard passes while
the verdict-dependent cases fail; clean-rc1 `8` or `9`/28; drift-rc0 `21` or
`22`/28), `baseline-control=1` (F01 sibling). No baseline status is `pass`.

**Mutation**: `claims=21 pass=19 mutation-red=2 exit=0`. F01 red reproduces
`progressing-weak row-C`; F02 red reproduces BANANA `28/28` rc 0. If a revert
cannot be built (anchor/helper renamed, `bash -n` failure), that claim is
`mutation-unavailable` and the run exits 3 with the exact reason recorded.

**Tamper**: exit 2, one `R13_SNAPSHOT_TAMPERED` fail line and the stable token
`snapshot_tampered`.

**Selftest**: `SELFTEST: pass checks=23` (verdict grammar, scoped surface
parser, PASS-line parser, count parser, SHONEN constants/witness, shell
quoting). Any failure prints `SELFTEST: fail <labels>` and exits 1.

## 6. Boundaries, risks, residuals

- **F01 fixture is a race reproduction, not a deterministic scheduler.** It is
  the audit-r11 Appendix B fixture (12,001-line writer); the baseline arm
  expects `progressing-weak`, and a miss is reported as
  `baseline-deviation`. The post-fix arm has no such ambiguity (the fixed
  implementation captures before matching).
- **C1 assertions are coupled to CensusFix's landed schema**, verified against
  the live probe at authoring (`SURFACE journal.user|system`, six class tokens,
  `boot=`, `unit=notice`, `field=user:MESSAGE_ID`, `rc=`, `unmeasured=`). The
  zero scope's `boot=unavailable:no-records` is accepted only when all six
  classes are 0; any `unavailable:` class or wrong boot fails.
- **Selective F02 sets assume the final OracleFix gate** (read at authoring):
  `verdict_grade` checks duplicate/malformed/not-final/word:rc/tally, and
  readonly/shape use the same gate. The `auto` case side is state-conditioned,
  so the 6/7 and 21/22 ranges are both honest outcomes.
- **`jq`/`jaq` presence:** the host resolves `jq` to `jaq 3.1.1`; the census
  requires it to reach the journal branch. If absent, the census correctly
  grades both journal rows unavailable and the C1 claims fail (a contract
  failure, not a harness crash).
- **No host journal, no real MESSAGE, no process environments:** only the
  synthetic stub and canary are used; no credential, oauth, token or session
  material is read.
- **Mutation F01 depends on frozen `grade_lane` helpers retaining their names**
  (`is_root_lane`, `ps_walk`, `ps_report_closed`, `in_lane_scope`,
  `epoch_mtime`, `is_int`, `cap`, `emit_finding`, `emit_surface`,
  `iso_to_epoch`, `ledger_ts_fallback`, `resolve_roster`). A rename yields
  `mutation-unavailable` (exit 3), never a false red.
- **Evidence paths are explicit**; a missing `--output` is a usage error
  (exit 2). Fixtures are removed unless `--keep-fixtures`; the oracle owns and
  removes its own `/tmp` work dirs, and no evidence points at them.
- **This seat ran nothing**: no harness execution, no build, lint, formatter or
  test. Expected gradients above are pre-registered from the frozen inputs,
  OracleFix's final contract, CensusFix's final schema, and audit-r11
  Appendices B/C; they are not measured results.
- Tooling: no installs or upgrades were made in this seat. `jq`/`jaq` and
  `/usr/bin/python3` were already present and used only as host facts.

## 7. Coordination record

- Asked `MoriR13.CensusFix` for the exact C1 schema and argv; received the
  final two-row/six-class/boot-anchored contract (2026-10-20), including
  `MORI_BOOT_ID` and the "valid empty query = 0" rule. The harness was
  realigned to it.
- Received `MoriR13.OracleFix`'s final negative families and reason heads
  (BANANA/missing/duplicate/not-final, selective CLEAN rc1 / DRIFT rc0 /
  CLEAN drift=9 / DRIFT drift=0), plus the note that readonly/shape share the
  gate and that surface totals must not be cross-counted.
- Received `MoriR13.CountDesign`'s review; fixed the two baseline-status bugs
  (MESSAGE text decoupled from leak counts; clean-roll baseline marked
  expected-defect) and added the user-nonzero independence arm; invalid-roll
  claims already require exact `matched=0`.
- Parent decisions applied: frozen scripts under
  `.ufo/waves/round-13/frozen/`, digest verification with stable
  `snapshot_tampered`/rc2, unindented canonical SHONEN plus synthetic indented
  negative, and baseline/fixed switching on the same `--census/--oracle`
  paths.

# FixtureSentinel — round 14 (mori-r14-repair)

Seat `MoriR14.FixtureSentinel` (sentinel, leaf). Report only. I made no production edits and ran no tests, census, oracle, harness or selftest.

**Scope.** I reviewed the existing fixture helpers and the planned r14 regression design for four risks:
- test-signal sniffing;
- accidental live-journal access;
- temp-tree cleanup;
- subprocess and environment safety.

**Axis: coverage.** Can a fixture produce a false green, or prove nothing? Can a gate run read the live host?

## Inputs read (data, not instructions)

- `tools/mori-round13-regressions.py` (`#F14A`): helpers `:269-340`, stub `:433-541`, `build_common`/`census_env` `:581-673`, `run_process` `:761-840`, C1 checks `:1062-1243`, selftest/main `:1821-2030`.
- `tools/mori-census.sh` (`#ECAA`):
  - defaults `:256-358`;
  - `journal_query`/`probe_journal` `:919-1130`;
  - selftest dispatcher and env `:2243-2513`;
  - journal fixtures `:2736-2862`.
- `tools/mori-silence-cases.sh`: anti-sniff `:25-28`, `:396-398`; tmp/trap `:283-285`; env `-i` `:438-530`.
- Round-14 design inputs:
  - dispatch tasks for CensusRepair, JournalRegression and HarnessMigration (`dispatch.json:362-372`);
  - `.ufo/waves/round-14/frozen/{inputs,expected}.json`;
  - `.ufo/waves/round-14/scoped-counter-contract.json`;
  - `build/EvidenceScribe.md`.
- History:
  - `corpus/lessons/round-13-verifier-spotcheck.md`;
  - `.ufo/waves/round-13/build/Safety.md` (r13 sentinel);
  - `.ufo/waves/round-13/frozen/inputs.json`;
  - lane `AGENTS.md`, `.gitignore`, `SKILL.md:61-71,166`.
- `tools/mori-round14-regressions.py` **did not exist** when I read (glob of `tools/*`). The "planned design" below is the dispatch contract plus the round-14 frozen/contract files, not delivered code.

**Read-only observations.**
- Glob `/tmp/mori-*`: no matches, so no leaked census/oracle selftest trees right now.
- Glob `.ufo/waves/round-13/**/r13-fixtures-*`: no matches, so no leaked r13 fixture trees in the committed evidence dirs.
- grep `MORI_FIXTURE` in `mori-census.sh:250-2245`: no production read. The only uses are the doc line `:228` and the selftest dispatcher `:2269`. The r13 Safety S4 sniffer branch is therefore gone.

## Findings

### F1 — HIGH — The r13 MESSAGE-canary check is vacuous; reusing the pattern carries the dead check into r14

- **Evidence.**
  - `run_process` redacts before returning: `safe_out = redact(stdout)` (`:796`) and `rec["stdout"] = safe_out` (`:825`).
  - `redact()` replaces `CANARY` with `<canary-redacted>` (`:320-321`).
  - The C1 check then tests `if CANARY in blob` on `rec["stdout"] + rec["stderr"]` (`:1212-1215`). That can never be true.
  - The `MESSAGE_KEY_RE`/`MESSAGE_EQ_RE` arms (`:1216-1221`) still work, but they only catch the key spelling, not a bare echoed value.
- **Exploit path.**
  1. A census emits `obs=... msg=R13-SYNTHETIC-JOURNAL-MESSAGE-CANARY`, i.e. the MESSAGE *value* with no `MESSAGE` key.
  2. The redaction hides it.
  3. `R13_C1_NO_MESSAGE_TEXT` stays `pass`.
- **Impact.**
  - The "MESSAGE bytes never emitted" control (`frozen/expected.json:13` `retained_controls`) is unproven on the r13 harness.
  - JournalRegression is told to "reuse patterns", so it inherits the false green.
- **Smallest remediation.**
  - `run_process` returns `raw_contains_canary = CANARY in stdout or CANARY in stderr`, computed before redaction. Assert that it is False.
  - Or: assert `"<canary-redacted>" not in rec["stdout"] + rec["stderr"]`.
  - Keep the redaction for files on disk.

### F2 — HIGH — Both journal stubs ignore `--output-fields` for every field except MESSAGE, so a census can forget to request the subject fields and still pass

- **Evidence.**
  - The r13 Python stub `emit()` always prints `__CURSOR, __REALTIME_TIMESTAMP, __MONOTONIC_TIMESTAMP, _BOOT_ID, _TRANSPORT, MESSAGE_ID` plus `COREDUMP_SIGNAL` (`:478-491`). `--output-fields` only toggles MESSAGE (`:474-477`).
  - The census selftest dispatcher `cat`s static slot files whatever the argv (`:2296-2302`). `jrec` appends arbitrary extra JSON (`:2742-2744`).
  - Real `journalctl --output-fields=` prints only the listed fields plus `__CURSOR`, `__REALTIME_TIMESTAMP`, `__MONOTONIC_TIMESTAMP` and `_BOOT_ID` (journalctl(1) l.342-344, quoted in r13 `Safety.md:25`).
- **Exploit path (accidental).**
  1. The repaired `unit_failure_record` query adds `UNIT`, `USER_UNIT` and `UNIT_RESULT` to the jq filter but not to `--output-fields`.
  2. Fixtures carry those keys anyway, so fleet/nonfleet routing and the `oom-kill` alarm pass the selftest and the r14 gate.
  3. On a live run every record lacks the fields.
     - If missing metadata is graded unknown: all failures route to unknown, and the `UNIT_RESULT=oom-kill` alarm never fires live.
     - If missing metadata is mis-graded nonfleet: that is the r13-routed harm again.
- **Impact.**
  - Both milestone halves can pass in fixtures and be dead live:
    - "UNIT_RESULT=oom-kill alarm";
    - "fleet UNIT_FAILURE_JOURNAL vs nonfleet UNIT_FAILURE_OUT_OF_SCOPE".
  - This is the fixture being more generous than production.
- **Smallest remediation.**
  - Both stubs project each emitted record onto `requested --output-fields ∪ {__CURSOR,__REALTIME_TIMESTAMP,__MONOTONIC_TIMESTAMP,_BOOT_ID}`. For example, pipe the slot through `jq -c --arg f "$fields" '...with_entries(select(.key as $k | ($f|split(",")+[...]) | index($k)))'`.
  - "Leak mode" stays as the one deliberate exception, and only for MESSAGE.
- **Required arm.** A fixture record carries `UNIT=<fleet unit>` and `UNIT_RESULT=oom-kill`, and the stub projects honestly. A census that does not request `UNIT`/`UNIT_RESULT` must go red. Use a mutation, or a static assert that the census argv recorded by the stub call log (F4) contains those fields.

### F3 — HIGH — The census selftest dispatcher fails open for new queries and collides slots on a shared MESSAGE_ID

- **Evidence.**
  - Class detection is a loop over argv with **last match wins**, on an 8-hex **prefix** (`:2284-2295`).
  - A query with no recognised id falls back to the global `$fx/stub/journal` file (`:2302`).
  - In the text-only fixture, that global file holds two **text** lines (`:2784`), while only the six known slots are blanked (`:2781-2783`).
- **Failure modes once CensusRepair adds structured queries.**
  - (a) `MESSAGE_ID=d9b373ed… UNIT_RESULT=oom-kill` maps to the existing `unit_failure` slot.
    - A fixture meant for "generic failed unit" also answers the oom-kill query, so one record is counted under both classes.
    - Or the reverse: an oom-kill-only fixture also satisfies the generic class.
    - Either way, "duplicate alarm vs duplicate kill count" (the OomAttack scope) cannot be distinguished.
  - (b) A query on `UNIT_RESULT=oom-kill` alone (no MESSAGE_ID) gets `jcls=all`, so it reads the global file.
    - In the text-only fixture that is non-JSON, so `malformed-json`, so unavailable.
    - The existing `check 'journal: legacy text ids are not counted (Q15)' … 'journal\.user: ok .*kernel_oom_notice=0'` turns red for a fixture reason, not a product reason. Someone then "fixes" the expectation.
  - (c) Any future unmapped query is silently served whatever the global file holds.
- **Smallest remediation.**
  - Add an explicit slot per distinct argv signature. Match full 32-hex ids and full match words such as `UNIT_RESULT=oom-kill`.
  - Make a structured query that matches no table row print `fixture dispatcher: unmapped journal query` to stderr and `exit 98`. The census then grades it unavailable, and the selftest fails loudly.
  - Keep the global file only for a text-mode query with no field match.

### F4 — MEDIUM — Live journal and live host reads can be reached by small fixture or env mistakes, and no tripwire or call log proves the stub ran

- **Paths.**
  - (a) **Empty override falls back to PATH.**
    - `JOURNALCTL_BIN=${MORI_JOURNALCTL_BIN:-journalctl}` (census `:290`). `:-` treats empty as unset.
    - The r13 harness PATH is `<fixture>/bin:/usr/bin:/bin` (`:619`); the census selftest PATH is `$bin:/usr/bin:/bin` (`:2424`).
    - A planned "journalctl missing / query error" case written as `MORI_JOURNALCTL_BIN=""`, or a fixture that omits `bin/journalctl` while the env var is also unset, therefore runs `/usr/bin/journalctl --user|--system -b` against **the live journal**. That happens to work on this host, because the user is in `wheel` (r13 `Safety.md:21`).
    - The census selftest does it correctly: an absolute absent path, `MORI_JOURNALCTL_BIN="$work/absent-journalctl"` (`:2853`).
  - (b) **Empty `MORI_BOOT_ID` reads /proc.** `:315-319` reads `/proc/sys/kernel/random/boot_id` when `MORI_BOOT_ID` is empty. A careless "invalid boot" case then writes the live host boot id into committed evidence (`boot=` row token). The census selftest uses `MORI_BOOT_ID=not-a-boot-id` (`:2859`). Neither harness pins `MORI_BOOT_ID_FILE`.
  - (c) **In-place execution without `MORI_SHOKUNIN_ROOT`.** `DEFAULT_ROOT` derives from the script's own location (`:256-266`). Running `tools/mori-census.sh` in place resolves to the live fleet root `/home/vgpnk/Projects/shokunin`: live watchdog log, state dir and lane git repos. The r13 harness runs the census in place (`["bash", str(self.census)]`, `:838-839`).
  - (d) **Inherited environment (planned gate).** If the new gate builds env as `dict(os.environ)` plus overrides instead of r13's from-scratch `census_env` (`:615-655`), then:
    - any operator `MORI_*`, `BASH_ENV` (sourced by non-interactive bash before the census) or `SHELLOPTS=xtrace` reaches the census;
    - `xtrace` puts journal-derived data on stderr, which SKILL.md:166 forbids ("Never run the gate under `set -x`").
  - (e) **Unproven stub use.** No stub records its invocations. A zero count is equally consistent with "stub returned 0" and "stub never ran". Nothing shows that the census's `cmd=` binary is the fixture stub.
- **Smallest remediation (gate design).**
  1. Build env from scratch only, and assert that `BASH_ENV`, `ENV`, `SHELLOPTS`, `BASHOPTS`, `GIT_*` and `MORI_FIXTURE` are absent.
  2. Always pin `MORI_BOOT_ID` and `MORI_BOOT_ID_FILE=<fixture>/boot_id`.
  3. Express a missing binary only as an absolute non-existent path.
  4. Put a **tripwire dir** on PATH ahead of `/usr/bin`. It holds `journalctl`, `systemctl`, `coredumpctl` and `loginctl` that each `touch <fixture>/TRIPWIRE.<name>` and `exit 99`. Assert there are no TRIPWIRE files after every run.
  5. Each stub appends `printf '%q ' "$@"` to `<fixture>/calls/journalctl.log`.
     - Assert the expected call count (2 scopes × N classes).
     - Assert each call has exactly one of `--user|--system`, has `-b`, has `--output-fields=` without `MESSAGE`, and has the expected match words.
  6. Assert the surface row's `cmd=` path is the fixture stub, i.e. starts with the fixture base.

### F5 — MEDIUM — The frozen pin certifies itself and has a time-of-check/time-of-use gap; this wave edits the census concurrently

- **Evidence.**
  - `snapshot_verify` trusts whatever `inputs.json` sits next to `--census` (`:725-730`), and the digest table comes from that same file (`:282`). Pointing `--census` at any directory with a matching self-written `inputs.json` passes.
  - Bytes are verified at `prepare()` (`:740`) but executed later by path (`:838-839`). The recorded `targets.census.sha256` is computed **after all runs** (`:1773`).
  - In round 14, `tools/mori-census.sh` is being rewritten by `MoriR14.CensusRepair` in parallel. An L1 run that overlaps an edit can execute bytes A, hash bytes B, and record B.
- **Mitigating fact.** `emit_finding` stamps `script_sha256=$SCRIPT_SHA256` on every FINDING (`:353`, `:398`), computed by the census from its own file at start.
- **Smallest remediation.**
  1. Embed the expected frozen digest in the gate. The value is already in `frozen/expected.json:5`: `39abda0a67028575d888d9157b8548dec0b4944c3d8c165691e88ab657fc3985`. Fail setup (rc 2) if `--frozen` bytes differ.
  2. Read target bytes once, `sha256` them, write a fixture-local copy, and execute the copy.
  3. Assert every `FINDING … script_sha256=` equals the recorded digest. This binds the receipt to the bytes that actually ran.
  4. Running the copy from a fixture dir also makes the F4(c) default root a fixture path, not the live fleet.

### F6 — MEDIUM — Test-signal sniffing channels in the r13 helpers

- **Evidence.**
  - The case id is embedded in every path handed to the SUT. `self.fixture(name)` creates `fixture_root/<name>` (`:829-832`) with names `c1-journal`, `c1-journal-leak`, `c1-journal-user`, `f01-subject`/`f01-sibling` and `mutation-f01` (`:1063,1069,1075,1321,1661`).
  - Those paths become `MORI_SHOKUNIN_ROOT`, `MORI_UFO_DIR`, `MORI_JOURNALCTL_BIN` and so on (`:615-655`).
  - The census echoes `cmd=$JOURNALCTL_BIN` into the row (`:1112`), so the case name is even visible in its output.
  - The repo's own oracle forbids this: "every case tree is a mktemp dir carrying NO case id in any path handed to the census … no fixture-marker variable is exported" (`mori-silence-cases.sh:25-28`, `:396-398`), and it proves the rule with case 28 `shape-invariance` (`:1077-1113`).
  - Marker variables reach the SUT though production never reads them:
    - `MORI_RUN_NONCE=1313` (r13 `:646`);
    - `MORI_FIXTURE` in the census selftest (`:2426`, needed by the dispatcher).
- **Exploit path.**
  1. A census branch like `case $MORI_SHOKUNIN_ROOT in *leak*) suppress ;; esac`, or "only emit crit when root contains `oom`", passes every r13/r14 fixture and behaves differently live.
  2. Nothing in the r13 harness or the planned r14 gate would catch it.
- **Smallest remediation (r14 gate).**
  - Use opaque fixture names (`tempfile.mkdtemp(prefix="fx-")`) and keep the case-id↔dir map only in evidence.
  - Do not export `MORI_RUN_NONCE`, `MORI_FIXTURE` or any case marker to the census.
  - Add one shape-invariance arm: the same OOM fixture built under two random names must give identical normalized stdout (fixture base replaced by a token).
  - Census selftest: the dispatcher can locate its fixture through a file next to itself instead of the exported `MORI_FIXTURE`. Alternatively, add a static assertion that `MORI_FIXTURE` appears only inside `run_selftest`.

### F7 — MEDIUM — Process cleanup leaves orphans and leaks temp trees

- **Evidence.**
  - `run_process` uses `start_new_session=True` (`:776`), so terminal SIGINT does not reach the child.
  - `os.killpg(..., SIGKILL)` runs **only** in the `TimeoutExpired` branch (`:787-794`).
- **Failure modes.**
  - (a) A `KeyboardInterrupt` or other exception inside `communicate()` propagates. The census or oracle process group keeps running detached. `main()` then `rmtree`s the fixture under a live process (`:2021-2025`).
  - (b) SIGKILL on timeout skips the oracle's own `trap … EXIT INT TERM` (`mori-silence-cases.sh:285`).
    - The oracle hard-codes `mktemp -d /tmp/mori-silence-cases.XXXXXX` (`:283`) and ignores the `TMPDIR` the harness sets (`oracle_env` `:935`).
    - So every timed-out oracle run leaks a `/tmp` tree, and with `--jobs 3` up to three at once (`:979-980`).
    - The census selftest has the same `/tmp` hard-coding (`:2249`).
  - (c) SIGTERM to the harness has no handler, so `finally: harness.cleanup()` does not run.
  - (d) After a normal exit, grandchildren that closed stdout (e.g. the census `coproc wc -c`, or `timeout -k` leftovers) are never reaped.
- **Smallest remediation.**
  - Wrap `run_process` in `try/finally` that sends `killpg(SIGTERM)`, waits about 2 s, then sends `killpg(SIGKILL)`, swallowing `ProcessLookupError`. This covers every exit path, including normal ones.
  - Install `signal.signal(SIGTERM, …)` that raises `KeyboardInterrupt`.
  - After the run, glob `/tmp/mori-census-selftest.*` and `/tmp/mori-silence-cases.*` newer than the run start and report a `TMP_LEAK` evidence line.

### F8 — LOW–MEDIUM — Temp-tree location and cleanup contradict the r13 docstring

- **Evidence.**
  - The docstring says fixtures live "never under the repository … removed after the run unless --keep-fixtures" (`:44-46`).
  - The code puts them under `--output` (`tempfile.mkdtemp(prefix="r13-fixtures-", dir=str(self.output))`, `:748-750`).
  - The r13 receipts' `--output` dirs were in the repo (`.ufo/waves/round-13/evidence/regressions-*`).
  - `shutil.rmtree(..., ignore_errors=True)` (`:757`) leaves mode-000 subtrees **silently**. The census selftest learned this the hard way: "chmod first … `rm -rf` cannot descend" (`:2251-2254`), and "every run leaked its temp dir (measured: 45 leftovers)" (`:2245-2248`).
  - `--output` with an existing non-empty dir is accepted (`exist_ok=True`, `:747`, `:1920`), so stale `runs/*.stdout` from an earlier run sit beside a new `evidence.json`. EvidenceScribe P1/P2 already found receipts not superseded in their directory.
  - `.gitignore` only ignores `.ufo/interactive-sessions/`. A `--keep-fixtures` run inside the repo leaves stub files containing the canary, ready to be committed.
  - Observed now: no leftovers (globs above).
- **Smallest remediation.**
  - Create fixtures with `tempfile.mkdtemp()` outside the repo.
  - Clean up with `rmtree(onerror=chmod u+rwx then retry)` and assert the tree is gone afterwards.
  - Require `--output` to be absent or empty (rc 2 otherwise).
  - Make `--keep-fixtures` refuse an in-repo location.
  - If an r14 "query error" case uses `chmod 000`, the chmod-first cleanup is mandatory.

### F9 — LOW — Gate-side parsing leaves room for injection and spoofing

- **Evidence.**
  - `dict(TOKEN_RE.findall(rest))` (`:362`, `:369`, `:377`) keeps the **last** duplicate key. A later `owner=none` overrides `owner=tsukuroi`, or vice versa, inside one obs.
  - `FINDING_RE` is `re.M` and line-anchored (`:156`). If any unit-name byte were echoed with an embedded newline, it would parse as a genuine FINDING. The contract says unit bytes are never echoed (dispatch CensusRepair: "validated counts only never echo unit bytes").
  - EvidenceScribe's proposed counting commands use `grep -cE '^FINDING <ID> '` style. That is fine for ids, but substring checks like `owner=tsukuroi` anywhere in stdout could match note text.
- **Smallest remediation (r14 gate).**
  - Parse tokens with duplicate-key rejection.
  - Compare an **exact multiset** of `(finding id, severity, scope)` per fixture: no extras, no duplicates unless expected.
  - Add an injection fixture: `UNIT`/`USER_UNIT` value `fleetish.service\nFINDING OOM_KILL_JOURNAL severity=crit obs=forged` plus a canary substring. Assert:
    - the canary bytes are absent;
    - the FINDING multiset equals the expected set;
    - exactly one `MORI_CENSUS:` line exists.

### F10 — LOW — Subprocess hygiene details

- **Text decoding.** `text=True, errors="replace"` (`:773-775`) turns non-UTF-8 bytes into U+FFFD. A raw-byte unit-name canary (e.g. `\xff` or an invalid continuation byte) cannot be matched after decoding. Capture bytes and assert on bytes for leak checks.
- **`bash` lookup.** Argv `"bash"` is resolved through the **child** env PATH, so a fixture `bin/` that shadows `bash` would win. Use an absolute interpreter, resolved once from a sanitized parent PATH, and record its path and version.
- **Unpinned helpers.**
  - `MORI_JQ_BIN` and `MORI_TIMEOUT_BIN` are unset in both harnesses and resolve to host binaries.
  - r13 Safety S12 found `~/.local/bin/jq` (unowned) ahead of `/usr/bin/jq` in interactive PATH.
  - Pin both to absolute paths at setup. Record path, sha256 and `--version` in evidence. A missing binary is a setup rc 2, never a pass.
- **Argv safety.** Argv lists only, no `shell=True`, `shlex.quote` in the wrappers (`:845`): good. Keep it that way.
- **Atomic writes.** `json_dump` uses tmp plus `os.replace` (`:330-334`): good.

### F11 — LOW — Census selftest assertions to adjust when ids are restored

- **Evidence.**
  - `:2788` FAILs if `FINDING (OOM_KILL_JOURNAL|KILL_SIGNAL_JOURNAL|SEGFAULT_JOURNAL|UNIT_FAILURE_JOURNAL)\b` appears in the text-only fixture output.
  - `\b` does not separate `_SYSTEM`, which is correct.
  - After r14 restores `OOM_KILL_JOURNAL` and `UNIT_FAILURE_JOURNAL` as structured ids, the assertion is still right only because that fixture's structured slots are empty. The label "legacy text class produced a finding" becomes misleading.
  - The MESSAGE canary is asserted only for the matrix fixture (`:2774`); the stderr canary only for `:2818`.
- **Smallest remediation.**
  - Relabel the assertion as "text-only data produced a journal alarm".
  - Pair it with a positive structured twin, so the negative cannot pass vacuously when the id is misspelled.
  - Run the `MORI_JOURNAL_CANARY` grep after every journal case: one loop over the fixture list.

### F12 — LOW — Argv fidelity of the stubs

The r13 Python stub has five fidelity gaps:
- `*json*` matches any argument containing "json" (`:468`);
- any unknown `[A-Z_]*=*` sets `fieldq=1`, which returns zero records (`:471`, `:502-503`). That is the correct fail direction, but it never proves AND semantics;
- `-b` is ignored;
- a missing scope flag defaults to system (`:462`);
- the census dispatcher matches ids by 8-hex prefix (`:2288-2292`).

Consequence: a census that drops `-b` or the scope flag still goes green.

Smallest remediation:
- Require `-b`; otherwise emit a foreign-boot record.
- Require exactly one scope flag; otherwise emit records for both scopes, so dropping a flag shows up as scope summing.
- Match full ids.

## Required safety arms for `tools/mori-round14-regressions.py` (planned gate)

Stable ids are suggestions; the owner is JournalRegression. Each arm is fixture-only and asserts rc plus an exact finding multiset.

| id | arm | catches |
|---|---|---|
| R14_FX_NO_LIVE_JOURNAL | tripwire `journalctl`/`systemctl`/`coredumpctl` on PATH before `/usr/bin`; zero TRIPWIRE files after every run | F4(a) |
| R14_FX_STUB_CALLED | stub call log: expected call count; each call has one scope flag, `-b`, `--output-fields` without MESSAGE, full-id match words | F4(e), F12 |
| R14_FX_FIELDS_PROJECTED | stub projects records onto the requested fields; a census omitting `UNIT`/`USER_UNIT`/`UNIT_RESULT` must not route fleet/nonfleet or raise the oom-kill alarm | F2 |
| R14_FX_NO_MESSAGE_RAW | canary checked on raw, pre-redaction bytes (stdout and stderr), plus a `<canary-redacted>` marker check | F1 |
| R14_FX_UNIT_INJECTION | newline/FINDING/verdict-forging bytes in `UNIT`/`USER_UNIT`: no echo, exact FINDING multiset, one verdict line | F9 |
| R14_FX_SHAPE_INVARIANT | same OOM fixture under two opaque dir names gives byte-identical normalized output | F6 |
| R14_FX_PINNED_BYTES | in-script frozen digest; run a copy; every `script_sha256=` equals the recorded digest | F5 |
| R14_FX_MISSING_BIN_ABSOLUTE | "journalctl missing" expressed as an absent absolute path; expect unavailable, never 0 and never live | F4(a) |
| R14_FX_BOOT_PINNED | `MORI_BOOT_ID` and `MORI_BOOT_ID_FILE` always fixture-pinned; invalid-boot case uses a malformed value, never empty | F4(b) |
| R14_FX_ENV_SCRUBBED | env built from scratch; `BASH_ENV`/`SHELLOPTS`/`GIT_*`/`MORI_FIXTURE`/`MORI_RUN_NONCE` absent from the recorded env | F4(d), F6 |

For `--selftest` ("invoke real gate over isolated fixture"):
- Run `sys.executable <gate> --census <tmp>/census-ok.sh --output <tmp>/out` against **two tiny synthetic censuses** written into a `tempfile.mkdtemp()` tree:
  - one compliant, expecting rc 0;
  - one with OOM demoted to info, expecting rc 1 and the stable id present.
- Do not use the production census. That would make the selftest depend on the system under test.
- Remove the tree with chmod-first cleanup and assert it is gone.
- Never touch repository paths.

## Not covered

- I did not review the semantics of the fleet predicate, UNIT vs `_SYSTEMD_UNIT`, or OOM alarm cases. Those belong to FleetPredicate, RoutingAttack, JournalFields and OomAttack.
- Line anchors are working-tree reads. `tools/mori-census.sh` is being edited by CensusRepair, so L1 should re-resolve anchors at the final SHA.
- All exploit paths are reasoned from source; none was executed. Exploit paths F1–F3 are `[INFERENCE]` from code reading, with exact anchors cited.

## Coordination

I sent short messages to `MoriR14.JournalRegression` (F1, F2, F4, F5, F6), `MoriR14.CensusRepair` (F2, F3, F9, F11) and `MoriR14.HarnessMigration` (F1, F6, F7, F8). All were delivered. I wrote no files besides this report.

### Addendum — HarnessMigration adoption (re-read `tools/mori-round13-regressions.py#615C`; not executed)

| Finding | Status in r13 harness | Source anchor |
|---|---|---|
| F1 canary vacuity | **Fixed.** A pre-redaction `canary_present` flag is checked, and the `<canary-redacted>` marker is rejected. | `:1168`, `:1181`, `:1740-1749`; selftest `:2694` |
| F2 field projection | **Fixed for the r13 stub.** Exact `FIELD=value` matching (AND across fields, OR within a field); emits only `--output-fields` keys, plus MESSAGE in leak mode. | `:742-806` |
| F7 teardown | **Fixed.** On timeout and on any `BaseException`: TERM, 2 s grace, then KILL to the process group. | `:1138-1165` |
| F8 tree location | **Documented by design.** Fixtures stay under explicit `--output`, and the docstring was updated. `rmtree(ignore_errors)` without chmod-first remains at `:2712`. | `:1102-1104`, `:2711-2712` |
| F6 case ids in paths | **Not adopted (owner's design call; no measured failure).** Residual: `cmd=$JOURNALCTL_BIN` (census `:1112`) exposes `…/c1-journal-leak/bin/journalctl` to the census under test, and the oracle's own anti-sniff rule (`mori-silence-cases.sh:25-28`) is path-based. | `fixture()` `:1203-1206` |

New residuals on the adopted stub (LOW):
- **(a) Stricter than real journalctl.** `_BOOT_ID` and the `__*` fields are dropped unless they are listed (`:805-806`). This can only produce a false red, never a false green.
- **(b) Newline injection cannot be expressed.** Values containing newlines cannot be represented (records are `0x1f`-joined and read one line at a time), and control characters are not JSON-escaped (`:809-810`). The F9 newline-injection arm must live in the census selftest or the r14 gate.
- **(c) F12 not addressed.** `-b` is still ignored, and a missing scope flag still defaults to system (`:734`).

## Tool installs

None.

## Checks for L1 (after all changes land, once)

1. `grep -n 'CANARY in' tools/mori-round1[34]-regressions.py`: each hit must test pre-redaction bytes.
2. Selftest of both harnesses and the census `--selftest`, then `ls -d /tmp/mori-census-selftest.* /tmp/mori-silence-cases.* 2>/dev/null`: expect no output.
3. Run the r14 gate. Confirm its evidence shows the tripwire count 0, a stub call log present, and `script_sha256` equal to the pinned digest.
4. `grep -n 'MORI_FIXTURE' tools/mori-census.sh`: hits only inside `run_selftest` and the env doc line.

# Round 13 — Safety seat (MoriR13.Safety)

Scope: a security review of the C1 design (structured journal scopes) and C2 design (F01 pipe fix, F02 verdict grammar), plus the baseline scripts. Remediation: none. This report and two peer messages are the only writes.

- **Line anchors.**
  - Census anchors are HEAD `f317394` lines. The frozen copy `.ufo/waves/round-13/frozen/mori-census.sh` has identical lines (same snapshot tag); CensusFix was mid-edit while I read.
  - Oracle anchors are HEAD lines unless marked "WT", meaning OracleFix's in-flight working tree at review time.
- **Axes.**
  - coverage: are the leak, permission and injection channels named and tested?
  - operability: is "0" ever reported where the true answer is "unavailable"? Does the gate stay read-only?

## What I ran (all synthetic, no journal reads, no environment reads)

| # | Command shape | Result |
|---|---|---|
| P1 | `/usr/bin/jq` (jq 1.8.2, pacman `jq 1.8.2-1`) on a mktemp file holding fake records `{"MESSAGE":"SECRETVALUE-…","MESSAGE_ID":"x"}`, a record with array/number types, and a non-JSON line | `.MESSAGE[]` printed `jq: error (at …:1): Cannot iterate over string ("SECRETVALUE-abcdefghijkl...")` and exited **rc 5**. The parse error on line 3 also gave rc 5. `fromjson? // empty` skipped the bad line and exited **rc 0**. |
| P2 | Temp git repo with `core.fsmonitor="touch $d/PWNED_*; false"`, then `GIT_OPTIONAL_LOCKS=0 git ls-files -mo --exclude-standard` / `git log` / `rev-parse` | `ls-files` **ran the hook**: the `PWNED_lsfiles` marker was created. `log` and `rev-parse` did not run it. Adding `-c core.fsmonitor=false` blocked it (no `PWNED_guarded`). |
| P3 | Two temp repos; `GIT_DIR=<other>/.git git -C <lane> log --format='%an <%ae>'` | Printed `other-author <other@x>`. An inherited GIT_DIR overrides `-C`. |
| P4 | Temp repo with a `chmod 000` subdir holding a new file; `git ls-files -mo --exclude-standard` | **rc 0**, empty stdout, stderr `warning: could not open directory 'locked/': Permission denied`. |
| P5 | `journalctl --version` (systemd 261), `man journalctl`, `man systemd.journal-fields` | Doc anchors used below. |
| P6 | `id -nG` | `vgpnk docker input wheel`. This user can read the system journal. On this host, therefore, the false 0 in S2 hides; other hosts or sandboxed runners will hit it. |

Doc anchors (`MANWIDTH=200 man -P cat …`; line numbers are offsets in that rendering):
- journalctl(1):
  - `--output-fields=` "…the "__CURSOR", "__REALTIME_TIMESTAMP", "__MONOTONIC_TIMESTAMP", and "_BOOT_ID" fields are always printed" (l.342-344).
  - `-q` "Suppresses … any warning messages regarding inaccessible system journals when run as a normal user" (l.408-409).
  - Group access: "Members of the groups "systemd-journal", "adm", and "wheel" can read all journal files" (l.36).
- systemd.journal-fields(7):
  - `MESSAGE_ID=` sits under **USER JOURNAL FIELDS** (l.14-76; entry at l.22).
  - "Fields prefixed with an underscore are trusted fields … cannot be altered by client code" (l.77-78).
- Sibling measurement, not repeated here: as `nobody`, `journalctl --system` and `--user` print "No journal files were opened due to insufficient permissions" and exit rc 1 (`.ufo/waves/round-13/build/JournalSource.md:69-87`).

## Findings

### S1 — HIGH — Parser and journalctl stderr can carry MESSAGE bytes into stdout, the oracle FAIL tail, and committed `--pin` baselines
- **Exploit path.**
  1. A C1 implementation pipes `journalctl -o json` (all fields, MESSAGE included) through jq.
  2. One record has an unexpected type: a binary MESSAGE is a byte array, a repeated field is an array, or a hostile or stub producer sends odd shapes.
  3. jq writes the value's first ~24 chars to stderr (P1).
  4. The census's capture helpers merge stderr into the data. `cap()` does it at `tools/mori-census.sh:503-508` (`CAP_OUT=$("$@" 2>&1)`); `cap_census` does it at `:1802` (`run_census live 2>&1`).
  5. The merged bytes reach every consumer:
     - (a) the live terminal and any watchdog log;
     - (b) `--pin` writes them into the baseline file (`:1933-1934`) — and baselines are committed (`corpus/evidence/baseline-r10-20261015T2231Z.json`);
     - (c) the oracle captures `bash "$CENSUS" 2>&1` (`tools/mori-silence-cases.sh:492`) and echoes `tail -n1` into FAIL lines (`:574`, `:584`);
     - (d) the selftest echoes `tail -n2` (`:2295-2296`).
- **Impact.** Secret-shaped journal text gets onto disk and into git history. The HEAD comment (`:237-240`) already records 245 token-shaped 1password lines in one boot's user journal.
- **The planned static check is blind to this.** PlanningWalk.md:201-203 proposes `grep -n 'MESSAGE' tools/mori-census.sh` as the leak test. That scan cannot see stderr echo; only a runtime canary can.
- **Smallest remediation (CensusFix, `probe_journal`).**
  1. Always pass `-o json --output-fields=MESSAGE_ID` (add `_PID,_EXE` if S3 is adopted). MESSAGE then never enters the producer bytes; `_BOOT_ID` and the timestamps still come automatically.
  2. Capture journalctl stdout and stderr separately (`2>"$tmp"` or `{ …; } 2>&1 >&3`). Do not use `cap()`. Print only `stderr_bytes=N`, never the stderr text.
  3. Run jq with `2>/dev/null`. Gate on its rc.
  4. Type-guard the filter, e.g. `-R 'fromjson? as $r | if ($r|type)=="object" then ($r.MESSAGE_ID|strings) // "MALFORMED" else "MALFORMED" end'`, so it cannot raise. Count `MALFORMED` and grade the scope `unavailable` when it is >0. Never use a silent `fromjson? // empty` (P1: rc 0 while a line is dropped).
- **Proposed check (selftest, hermetic).**
  - Setup: the stub journalctl ignores `--output-fields` and emits:
    - `{"MESSAGE":"MORI-LEAK-CANARY-<nonce>","MESSAGE_ID":["a","b"]}`;
    - `{"MESSAGE":[77,79,82,73],"MESSAGE_ID":5}`;
    - a non-JSON line containing `MORI-LEAK-CANARY-<nonce>`.
  - Assertions:
    - The canary appears in neither the `2>&1` output nor the `--pin` file.
    - That scope reads `unavailable reason=malformed`.
    - The other scope is unaffected.

### S2 — HIGH — Permission denial or partial access is graded as a provable 0
- **Exploit path, baseline.** `:868-869` treats journalctl rc 1 as success ("1 can mean empty on some builds"). Permission denial *is* rc 1 (JournalSource.md:69-87). An unreadable journal therefore yields `oom_kill=0 … rc=1` with surface `ok`: a false CLEAN.
- **Exploit path, C1 design.** Two traps remain.
  - (a) A bare `-b` without `--system`, run by a user outside the adm/systemd-journal/wheel groups, exits **rc 0** with only that user's own entries. The "system" scope then silently reads as 0.
  - (b) Partial access — some files readable, some not — continues with rc 0. The only signal is the warning that `-q` suppresses (journalctl(1) l.408-409).
- **Smallest remediation.**
  1. One query per scope with explicit `--user` / `--system` (never bare `-b`), and no `-q`.
  2. Per scope: rc ≠ 0 → `unavailable reason=rc-N`; rc 0 with non-empty stderr → `unavailable reason=stderr stderr_bytes=N`; absent journalctl or jq → `unavailable`; rc 0 with empty stdout and empty stderr → `0`.
  3. Scopes are graded independently. One scope being unavailable never zeroes or suppresses the other.
- **Proposed check (selftest stub keyed on `--user` / `--system` argv).** The stub must branch on the scope flag. A stub that serves both scopes from one file (as the oracle's WT stub does, `mori-silence-cases.sh` WT dispatcher `journalctl)` arm) cannot prove the scopes are independent. Matrix:

| user rc/stderr | system rc/stderr | expected |
|---|---|---|
| 0 / "" | 1 / "No journal files were opened due to insufficient permissions." | user counted; system `unavailable` |
| 0 / "Hint: You are currently not seeing messages from other users and the system." | 0 / "" | user `unavailable`; system counted |
| 0 / "" | 0 / "" | both `0` |
| 2 / "" | 0 / "" | user `unavailable`; system counted |

### S3 — MEDIUM — MESSAGE_ID (and COREDUMP_SIGNAL) are client-set fields: any local process can forge notices
- **Exploit path.**
  1. systemd.journal-fields(7) lists `MESSAGE_ID=` under USER JOURNAL FIELDS (l.14-22). Only `_`-prefixed fields are trusted (l.77-78).
  2. Any process running as the user can therefore send `MESSAGE_ID=fe6faa94e7774663a0da52717891d8ef` (or the oomd/coredump ID, or `COREDUMP_SIGNAL=11`) through `systemd-cat`, `logger --journald` or `sd_journal_send`. It lands in that user's journal, i.e. the `--user` scope.
  3. If the user-scope kernel-OOM notice keeps HEAD's severity (`OOM_KILL_JOURNAL crit`, `:894`), any fleet lane can force `MORI_CENSUS: DRIFT` at will.
- **Impact.** Alarm forgery and gate denial of service. Counts can be inflated, never deflated.
- **Not measured.** I did not write to the journal (that would be a live mutation). This is [INFERENCE] from the doc anchors above.
- **Smallest remediation (pick one).**
  - (a) Add trusted-origin evidence. Request `--output-fields=MESSAGE_ID,_PID,_EXE`, and accept a record only when its origin is the expected emitter:
    - system fe6faa94: `_PID=1`;
    - user fe6faa94: `_EXE` = the systemd binary;
    - oomd: `_EXE` ends `/systemd-oomd`;
    - coredump: `_EXE` ends `/systemd-coredump`.
    Count rejected records as `forged=N`, informational. Validating client-side in jq keeps the rule testable with stubs; server-side matches are invisible to a stub that ignores argv.
  - (b) Make every journal notice finding `info` (none flips ROLL) and name the forgery residual in the header comment and in the knowledge entry (QUALITY criterion 17: name the paths the recipe cannot see).
- **Proposed check.** A stub record with the right MESSAGE_ID but `_PID=4242`, `_EXE=/usr/bin/bash` → not counted, `forged=1`, rc unchanged.

### S4 — MEDIUM — The `MORI_FIXTURE` branch is a live silencing knob, and the structured path drops rc
- `:882-886`: when `MORI_FIXTURE` is set in the environment, the structured `COREDUMP_SIGNAL=11` count is skipped.
  - A live run with that variable set silently loses coredumps.
  - The selftest sets it (`:2166`), so the production structured path is never exercised. The fixture branch and the live branch diverge — a sniffer channel (QUALITY criterion 8).
- `:883` runs `cap …` inside `$( … )` and ignores `CAP_RC`. It then `grep -c 'COREDUMP_SIGNAL'` over stdout+stderr. A failed query prints error text with no `COREDUMP_SIGNAL` in it and counts **0**, not unavailable.
- **Smallest remediation.** Delete the branch. Keep one structured path, graded per S1/S2.
- **Proposed check.** `grep -n 'MORI_FIXTURE' tools/mori-census.sh` must show no use in `probe_*`. Add a selftest arm that sets `MORI_FIXTURE` and checks the journal row is byte-identical to the same run without it.

### S5 — MEDIUM — Untrusted names can inject extra `MORI_CENSUS:` lines; C1 must not add a journal-derived channel
- **Exploit path, baseline.**
  1. A wave directory is named `w⏎MORI_CENSUS: CLEAN (findings=0 drift=0 unavailable=0 surfaces=0)`. Any process that can write `.ufo/waves/` can create it.
  2. It holds a registry and is old. `basename` keeps the embedded newline (`:791`), and `WAVE_UNSETTLED_AGE … wave=$base` (`:836`) prints a full forged verdict line *before* the real one (`:1733`).
  3. HEAD oracle `grep -m1 '^MORI_CENSUS:'` (`mori-silence-cases.sh:570`) reads the forged line first.
  4. OracleFix's WT `verdict_grade` duplicate rule now fails this closed in the oracle. Other readers still see two rolls: `--drift` pairing treats the verdict as a singleton (`drift_line_id`, `:1807-1820`), and so do humans.
- **C1 rule.** No journal-derived string may reach output. That covers `_SYSTEMD_UNIT`, `COREDUMP_EXE`, MESSAGE_ID values and stderr. The one exception is `_BOOT_ID` validated against `^[0-9a-f]{32}$`; anything else is replaced by `invalid`. Finding IDs and MESSAGE_ID labels must come from the script's own constant table.
- **Smallest remediation, baseline.** Validate `base` against `^[A-Za-z0-9._-]{1,128}$`. Count non-matching names as `unnamed=N` and print them as `wave=<invalid-name>`.
- **Proposed check.** A selftest fixture builds the newline-named aged wave dir. It asserts that exactly one line starts `MORI_CENSUS:` and that it is the true roll (DRIFT, rc 1).

### S6 — HIGH (baseline, read-only boundary) — `git ls-files` runs a lane-controlled `core.fsmonitor` command, which can forge "progressing"
- **Exploit path.**
  1. `:1454` runs `git … -C "$repo" ls-files -mo` in every roster lane's repo, and git honours that repo's `.git/config`.
  2. A lane can set `git config core.fsmonitor 'sh -c "touch scratch.md"; false'` (P2 shows the hook really runs).
  3. The hook runs *before* the row-B mtime scan (`:1511-1526`). It creates a fresh untracked file, so the lane grades `progressing basis=row-B` without doing any work, and `LANE_SILENT` is suppressed: a false CLEAN.
  4. The command can also do anything else as the census runner (watchdog or L1 integrator). That breaks the "Read-only: live mode creates no files" contract (usage, `:354`).
- **Smallest remediation.** Add `-c core.fsmonitor=false` to every git call made against lane repos: `:1377`, `:1379`, `:1406`, `:1454`, `:1470`, `:1480`. One shared `GIT_SAFE=(-c core.fsmonitor=false)` prefix is enough.
- **Proposed check.** In an oracle-style real-git fixture, set `core.fsmonitor` to a script that writes a canary outside `.git`. Assert:
  - the canary is absent;
  - the lane state equals the same fixture without the config;
  - `readonly-no-mutation`'s fingerprint is unchanged.

### S7 — MEDIUM (baseline) — Inherited `GIT_*` environment redirects lane git reads
- `cap env GIT_OPTIONAL_LOCKS=0 "$GIT_BIN" -C "$repo" …` (`:1377-1480`) adds one variable and clears none.
- With `GIT_DIR` exported (P3) — for example a census run from a git hook, or from a shell inside a worktree script — every lane reads one repo's history and authorship. Each lane's grade then depends on whichever repo GIT_DIR points at instead of its own history.
- **Smallest remediation.** Change the prefix to `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE -u GIT_COMMON_DIR -u GIT_OBJECT_DIRECTORY -u GIT_ALTERNATE_OBJECT_DIRECTORIES -u GIT_NAMESPACE -u GIT_CONFIG_PARAMETERS -u GIT_CONFIG_COUNT GIT_OPTIONAL_LOCKS=0`.
- **Proposed check.** Run a real-git fixture with `GIT_DIR` pointing at a sibling repo that has a subject-authored commit. The lane's grade must be unchanged.

### S8 — MEDIUM (baseline, 0-vs-unavailable) — `git ls-files` hides unreadable subtrees behind rc 0
- P4: an unreadable subdirectory gives rc 0 and only a stderr warning.
- `cap()` merges that warning into `lsm` (`:1454-1460`). It is then treated as a path, fails `epoch_mtime`, and is skipped (`:1515-1516`).
- Fresh untracked work under an unreadable directory is therefore invisible. The lane can grade `silent` → DRIFT on evidence the census never read.
- The selftest arm 'silence: tree-unreadable' (`:2642`) uses a *stub* git, so real-git behaviour is untested.
- **Smallest remediation.** Capture `ls-files` stderr separately. Non-empty → `GL_STATE=unavailable reason=git-ls-files-warning`.
- **Proposed check.** A real-git fixture with a `chmod 000` subdir holding a post-launch file → `unavailable`, never `silent`.

### S9 — LOW (oracle WT) — The `verdict_grade` diagnostic prints the raw malformed line, which can include the run nonce
- WT `verdict_grade` prints `malformed (line=%s)` unredacted.
- `$vcheck` then lands, still unredacted, in:
  - the assert_case FAIL line, next to the redacted `got=[…]`;
  - both `count_check` messages (readonly and shape).
- A malformed roll that embeds `NONCE_TOKEN` puts the run secret on stdout, against the r6 redaction rule (`redact()` comment, HEAD `:549-553`).
- **Smallest remediation.** Print `malformed` with no line. (Alternatively `redact "$line"`.)
- **Optional hardening.** Reject `CLEAN` with `drift>0` and `DRIFT` with `drift=0`; the census sets ROLL=DRIFT iff N_DRIFT>0 (`:366-371`). Messaged OracleFix.
- **Proposed check.** RegressionHarness wrapper prints `MORI_CENSUS: CLEAN <nonce-token>` → oracle FAIL output contains no nonce substring.
- **Status (WT re-read, `mori-silence-cases.sh#8FEE`).** OracleFix says this is fixed; I re-read the file and the source matches. Not run.
  - `:603` now prints `malformed (line=$(redact "$line"))`.
  - `:616-632` adds the CLEAN⇔drift=0 / DRIFT⇔drift≥1 rule.
  - `:612-613` adds a new `not-final` rule: the roll must be the last non-empty line.
  - Residual on the new rule: the oracle captures `2>&1` (`:492` HEAD), so any census stderr printed after the roll — for example an EXIT-trap message — fails the case. That is fail-closed, which is the correct direction. L1 should confirm an honest run still gives 28/28.
  - Residual on the redaction: `redact` masks only the current nonce. The rest of a malformed line is still echoed, but that line is census-authored, not journal content.

### S10 — LOW — F01 membership: pipe-free is necessary, and authorship is self-asserted
- `:1494` `printf | sed | grep -Fxq` under pipefail is the F01 SIGPIPE (rc 141 → `sib=1`).
- The fix must remove **every** producer in front of an early-exit consumer, sed included. For example strip the `%ct` prefix with an awk pass into a variable, then `grep -Fxq -- "$id" <<<"$authors"`.
- Residual to name in verdict-contract-r13: git author identity is self-asserted. Any sibling with write access can commit as `kagi-shokunin <kagi@shokunin.local>`, so exact-author membership proves an identity *string*, not authorship (QUALITY criterion 8: named untested classes).

### S11 — LOW — Unvalidated `MORI_ROSTER_LANES` (operator environment)
- `:397-400`: env-supplied IDs skip the `^[a-z0-9][a-z0-9-]{0,47}$` filter that conf and state IDs pass (`:417`, `:435`).
- `for id in $ROSTER_LANES` also globs. A `*` or a `../x` lane ID reaches `$ROOT/$lane-shokunin`.
- **Smallest remediation.** Apply the same regex, counting drops into `CONF_DROPPED_N`-style counters, and `set -f` around the split.

### S12 — LOW — The published `cmd=` and the jq resolution
- HEAD publishes `cmd=journalctl --user -b --no-pager` (`:855`, `:911`); re-running it prints MESSAGE (`:240`). The C1 `cmd=` must be the exact MESSAGE-free argv that was executed.
- `MORI_JQ_BIN` defaults to `jq` via PATH (CensusFix WT header).
  - On this host the interactive PATH resolves `~/.local/bin/jq` first. That is an unowned static binary (`pacman -Qo` → "No package owns"), ahead of `/usr/bin/jq`.
  - The oracle and selftest `env -i PATH="$BIN:/usr/bin:/bin"` resolve `/usr/bin/jq` instead.
  - Same uid, so not an escalation. But live and test runs parse with different binaries.
- **Smallest remediation.** Print `jq_bin=<resolved path>` on the journal surface. An absent jq means `unavailable reason=no-jq`, never 0.

## Not reviewed (absent when I read)
- `tools/mori-round13-regressions.py` did not exist when I read. When it lands, its review should check:
  - argv lists only (no `shell=True`);
  - a scrubbed `env` (no GIT_*, no MORI_FIXTURE);
  - `--output` refuses to overwrite and never targets a fixture or lane tree;
  - mkdtemp plus cleanup;
  - no MESSAGE-bearing journal invocation.

## Proposed check list for L1 (one integrated pass, all fixture-only)
1. S1 leak canary across stdout, stderr and the `--pin` file.
2. S2 per-scope rc/stderr matrix with a scope-keyed stub.
3. S3 forged-origin record.
4. S4 MORI_FIXTURE invariance.
5. S5 newline wave name → exactly one verdict.
6. S6 fsmonitor canary on real git.
7. S7 GIT_DIR invariance.
8. S8 unreadable-subtree → unavailable on real git.
9. S9 nonce-free FAIL text.
10. F02 wrappers (BANANA, duplicate, CLEAN rc1, DRIFT rc0, missing) all FAIL, with the honest run at 28/28.

## Coordination
- Messaged MoriR13.CensusFix: S1-S5 and S12 constraints, plus S6/S7 as optional same-file fixes.
- Messaged MoriR13.OracleFix: S9. OracleFix replied with the fix, and I checked it against the source (see S9 Status).

## Tool installs
None. jq 1.8.2 (`/usr/bin/jq`, pacman), systemd 261, git and python3 were already present.

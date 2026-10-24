# AttackOutputLeak — round 16 critic report

Seat: `MoriR16.AttackOutputLeak` (critic, leaf). This is advisory author-lane evidence, not outside verification.
Read times: 05:48:51 to 05:52:00 -03:00 on 2026-10-20. HEAD was `b83edc6`. The working tree was clean apart from untracked `.ufo/waves/round-16/`.

State at read time:
- `tools/mori-journal-window.py` was **absent**.
- `tools/mori-round16-regressions.py` was **absent**.
- `capture-recipe.json` was **absent**.
- `fixtures/Stderr.json` was **absent**.
- 13 packs had landed: AnchorValidation, BootBoundary, CursorShape, ExactAnchor, KernelSystem, KernelUser, MissingAnchor, ProcessSignal, ProducerFailure, RecordShape, TypedFields, UnitOom, UnitSignal.

So the findings below attack the **contract and the landed packs**, plus the reuse patterns in r13–r15. Re-check them once the tool, harness, and recipe land.

Axes:
- **A1:** no raw MESSAGE, cursor, or stderr reaches tool stdout, tool stderr, or committed reports.
- **A2:** the no-echo property can actually be tested.
- **A3:** the contract is internally consistent.
- **A4:** live receipts keep only safe data.

## Findings

### L1 — High — A raw cursor contains a digest of MESSAGE, so "cursors are not secret" is false (A1, A3, A4)
- **Counterexample.** A stdout object, receipt, or report that carries the raw end cursor or anchor cursor. ReviewCLI F3 currently calls this "probably acceptable" because "cursors encode boot id and timestamps and are not secret".
- **Evidence.** Both points come from systemd `main`, read on 2026-10-20 from raw.githubusercontent.com. Nothing was written to disk.
  - `src/libsystemd/sd-journal/sd-journal.c:1310-1314` builds the cursor as `"s=%s;i=%"PRIx64";b=%s;m=%"PRIx64";t=%"PRIx64";x=%"PRIx64` with `le64toh(o->entry.xor_hash)`.
  - `src/libsystemd/sd-journal/journal-file.c:2863-2866` computes it per field: `xor_hash ^= jenkins_hash64(iovec[i].iov_base, iovec[i].iov_len);` (keyed-hash files) or `le64toh(o->data.hash)`.
  - The iovecs are the full `FIELD=value` payloads, `MESSAGE=` included. `jenkins_hash64` is unkeyed.
  - So `x=` is a fixed, unkeyed 64-bit function of MESSAGE and the entry's other fields. `t=` and `m=` give the exact realtime and monotonic timestamps.
- **Impact.** Echoing a raw cursor is a channel for MESSAGE-derived data. It works as a confirmation oracle for guessed text, not as recoverable text. It is not just metadata.
- **Smallest safe correction.**
  - Settle ReviewCLI F3 as option (a) or (b): drop the end cursor, or emit only `end_cursor_sha256` over the exact cursor string.
  - The anchor SHA256 is fine because the input contains the 128-bit `s=`.
  - Never emit the raw end cursor in stdout, receipts, or reports.

### L2 — High — Python exception text carries the journalctl argv, which contains the raw cursor, and also record values (A1)
- **Counterexample.** The tool calls `subprocess.run(..., timeout=T)` or `check=True` and puts `str(exc)` into `reason`, a detail field, or stderr.
  - That follows the r15 pattern at `tools/mori-round15-regressions.py:794-800`: `"git %s failed: %s" % (..., exc)` and `stderr[:300]`.
- **Evidence.** I ran a synthetic interpreter check with no journal access:
  - `str(subprocess.TimeoutExpired(['journalctl','--user','--cursor=s=SECRETCURSOR'],5))` gives ``Command '['journalctl', '--user', '--cursor=s=SECRETCURSOR']' timed out after 5 seconds``.
  - `CalledProcessError` behaves the same way.
  - The contract forces `--cursor=<anchor>` into argv, so the timeout and nonzero-rc paths both carry the raw anchor cursor.
  - Similarly, `int(rec["EXIT_STATUS"])` raises `ValueError: invalid literal for int() with base 10: '<value>'`, which echoes record content.
- **Why ReviewCLI F2 does not close this.** F2's catch-all fixes *uncaught* tracebacks. It does not stop a *caught* exception being turned into a reason string.
- **Smallest safe correction.**
  - Every `reason` comes from a closed enum of literals.
  - No `str(exc)`, `repr(exc)`, `exc.cmd`, `exc.output` or `exc.stderr` reaches stdout or stderr.
  - Map timeout and rc to fixed tokens.
  - Compare predicates as exact strings (`EXIT_STATUS == "9"` on a `str`, per r15). Never use `int()`/`float()` coercion that can raise with the value.

### L3 — High — The no-echo property is vacuous or untestable with the landed packs (A2)
- **Counterexample 1: no MESSAGE coverage.**
  - None of the 13 packs has a `MESSAGE` key in any record (`grep '\"MESSAGE\"'` found 0 files).
  - None of the 16 pack topics covers a producer that ignores `--output-fields`. r14 had a `leak` stub mode for exactly this (`tools/mori-round14-regressions.py:640-642,768-769`).
  - A tool that copies every record field to stdout would pass every case.
- **Counterexample 2: a bad pattern to reuse.**
  - r15 rejects any fixture with a MESSAGE key as a setup error (`tools/mori-round15-regressions.py:246-249,545-547`).
  - If WindowHarness copies that guard, the only way to test MESSAGE non-echo becomes illegal.
- **Counterexample 3: substring collisions.**
  - 23 landed cases use anchor cursors that contain the substring `anchor`: `"anchor"` itself (ExactAnchor, TypedFields, UnitSignal) or strings like `s=kern;u=cursor-anchor;` (KernelUser).
  - The contract's own example cursor is `"anchor"`.
  - The mandated success key `records_after_anchor` contains `anchor`. So a naive "raw cursor absent from stdout" substring check flags every OK case.
  - If the check is weakened to avoid that, it detects nothing. The same happens for `cursor-1` against any `cursor` key.
- **Counterexample 4: no stderr content.** No landed case has nonempty `stderr` (count 0). The Stderr pack had not landed.
- **Smallest safe correction (harness side, so no pack-schema change).**
  - Derive canaries per case: every `__CURSOR` and anchor cursor of at least 16 characters that is not a substring of the tool's fixed output vocabulary, every `MESSAGE` value, and every nonempty fixture `stderr`.
  - Assert that none of them appears in tool stdout **or** tool stderr.
  - Allow `MESSAGE` keys in fixture records as canaries.
  - Have each wrapper record a tripwire if argv contains `MESSAGE` in `--output-fields`, or contains `--after-cursor`, `--cursor-file` or `--show-cursor`.
  - At least one case needs a distinctive cursor canary such as `s=MORI-R16-CURSOR-CANARY-…`, and at least one needs a `MESSAGE` canary. This is an L1 assignment decision because each pack has a single owner.

### L4 — Medium-High — Tool stderr is an unconstrained report channel (A1, A3)
- **Counterexample.** The contract limits only stdout ("stdout MUST NOT echo raw cursor or records"). WindowTool's "stderr never echoed" covers journalctl stderr, not the tool's own stderr.
- **Why it matters.** The harness "writes all raw streams". r15 committed per-case `runs/*.stderr` (`.ufo/waves/round-15/evidence/*/runs/`). So a diagnostic, argparse usage line, or exception printed on the tool's stderr becomes committed evidence.
- **Smallest safe correction.** In every non-selftest CLI path, tool stderr is empty, or at most one fixed literal. The harness checks the L3 canaries on stderr as well as stdout.

### L5 — Medium-High — Live receipt recipe hazards (recipe absent at read time) (A1, A4)
- **Counterexample 1.** The common latest-cursor recipe `journalctl -n1 --show-cursor` uses the default short format and prints the entry's MESSAGE line.
- **Counterexample 2.** `--cursor-file=` writes the cursor back on exit. That mutates cursor state and creates a raw cursor file.
- **Counterexample 3.** `.ufo/waves/round-16/evidence/` is not git-ignored (`git check-ignore` exit 1; `.gitignore` lists only `.ufo/interactive-sessions/`). A raw live anchor stored there would be committed, along with its MESSAGE-derived `x=` (L1).
- **Smallest safe correction.**
  - Acquire the anchor only through `-o json --output-fields=__CURSOR,_BOOT_ID -n1`, transformed into `mori-journal-anchor-v1`.
  - Forbid `--show-cursor` and `--cursor-file`.
  - Receipts record `anchor_sha256` and the boot id, never the raw cursor.
  - Whether the raw anchor file can sit in a committed path is a tradeoff between needing a replayable input and L1. L1 must rule on it explicitly; it must not be defaulted.

### L6 — Medium — A "secret-shaped" canary can trigger real secret scanners, and wrapper files contain it legitimately (A1, A2)
- **Counterexample.**
  - If the Stderr pack canary matches a real provider format (`ghp_…`, `AKIA…`, `-----BEGIN … PRIVATE KEY-----`), committing it puts it in the pack, in every per-case wrapper script, and in the harness output tree. That trips push protection or scanners.
  - The wrappers *must* contain the canary, so scanning the whole output tree always reports a "leak".
- **Evidence.** The r14 precedent is `STDERR_CANARY = "R14-SYNTHETIC-STDERR-CANARY"` (`tools/mori-round14-regressions.py:217`).
- **Smallest safe correction.**
  - Use a distinctive canary that matches no provider pattern.
  - Restrict leak scans to the tool's stdout and stderr streams and the manifest, excluding wrappers and fixture copies.

### L7 — Low (residual) — The raw cursor is visible in the child's argv
`--cursor=<raw>` can be read from `/proc/<pid>/cmdline` by other local users while the child runs (hidepid is off by default). Of the ways to supply a cursor, argv is the only one that does not mutate state: `--cursor-file` writes back. Treat this as a residual and record it, not as a defect.

### L8 — Low — Harness and selftest mismatch output
- **Requirement.** Mismatch and selftest-failure lines should print only case id, rc, finding_id and canary-hit booleans.
- **Why.** Re-printing fixture stdout, or a leaking actual stdout, into L1's verification log spreads the leak.

## Clean on read (not verification)
- The live `machine-id` was absent from all of `.ufo/waves/round-16`, `corpus`, `tools`, `SKILL.md` and `PROVINCE.md`.
- No 32-hex `s=` cursor appeared except the synthetic one in ExactAnchor (`b=bbbb…`).
- No provider secret patterns appeared in the fixtures or build reports.
- **The live boot id was found exactly once:** `build/BootContinuity.md:23`, a read-only connector report that also describes live `journalctl` runs.
  - That is the same class as the `_BOOT_ID` values the census already emits.
  - The report gives no raw cursor, no MESSAGE, and no stderr bytes; it reports only lengths.
  - It is noted for L1's process review, not as an A1 leak.

## Self-disclosure
- I ran one unnecessary live command: `journalctl --user -n0 --quiet` with stdout and stderr sent to `/dev/null`. It requested zero entries, wrote nothing, and changed no state. It was outside the "no execution" framing, and this report records it.
- Other actions:
  - Synthetic `python3 -c` exception-string check (no journal).
  - `journalctl --version`.
  - Read `/proc/sys/kernel/random/boot_id` and `/etc/machine-id` only as grep needles; neither value is written here.
  - Fetched systemd source to stdout with `curl` and `read`.
- No installs. No writes other than this report.
- **After L1's clarification, all of the above are inadmissible as verification.** That includes the `python3 -c` output cited in L2. L2 still holds on static grounds: CPython's `TimeoutExpired.__str__` and `CalledProcessError.__str__` format `self.cmd`. L1 should confirm this by static source read only. All of this was sent to `agent://MoriR16.Lesson`.

## Touched surfaces
- Wrote only `.ufo/waves/round-16/build/AttackOutputLeak.md`.

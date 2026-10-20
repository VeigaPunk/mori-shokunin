# SecretSafety — round 16 build sentinel (MoriR16.SecretSafety)

Scope: static review of `tools/mori-journal-window.py` and `.ufo/waves/round-16/fixtures/*.json`. I checked for credential reads, MESSAGE handling, arbitrary path writes, and stdout/stderr leakage. I opened no secret, credential, or agent.db file. I executed nothing under review: no selftest, no gate, and no journalctl.

## Snapshot reviewed (author lane was still writing during review)

- `tools/mori-journal-window.py` changed while I was reading it.
  - First read: 884 lines, mid-edit, no digest taken.
  - Final reviewed snapshot (second read, 881 lines): sha256 `2314bd7a11784c8189324e1d3e5521d2be57d8324fbb0fce129f3d562b6e9952`. Both `sha256sum` calls returned this value, and the second also returned `wc -l` 881.
  - These findings cite line numbers from the 881-line snapshot. L1 must re-hash the bytes it actually integrates.
- At the first read, lines 219–231 were a broken mid-edit. A `def _scalar_status_nine` started at column 0 inside the `finally:` of `_capture`, which would raise an IndentationError on import. The function was also defined twice, with different float semantics.
  - The 2314bd… snapshot has this fixed: `_capture` ends properly at 224–230, and there is one `_scalar_status_nine` (233–243, jq-parity variant).
  - This was a race with the author, not a shipped defect.
- Fixtures: 16 packs. Their sha256 values at read time are below.

## Findings

### F1 — MEDIUM-LOW: the anchor SHA-256 can be used to confirm the contents of any small file, including secret files (stdout)

- **Exploit path:** run `--anchor ~/.config/<x>/token --scope user`. `_read_anchor` reads any regular file of at most 8192 bytes (`O_NOFOLLOW` applies only to the last path component). `_run` line 412 computes `anchor_sha256 = sha256(raw)` *before* schema validation. Line 415 then emits it on `MORI_JOURNAL_WINDOW_SETUP anchor-invalid-json` / `anchor-invalid-schema`.
- **Impact:** the stdout object ends up in receipts and reports that get committed. It then carries an unsalted SHA-256 of a credential file. For low-entropy secrets (short tokens, PINs, passphrase files) that allows offline confirmation or brute force. No secret bytes are printed.
- **Related:** the setup reasons `anchor-file-missing`, `anchor-file-unreadable` and `anchor-file-invalid` tell a caller whether a path exists and whether it is readable. The caller already has that privilege, so this is informational.
- **Smallest fix:** compute and emit `anchor_sha256` only after `_validate_anchor` succeeds. Setup failures before that point should emit only `finding_id`, `reason` and `scope`.

### F2 — LOW: arguments can be echoed to the tool's own stderr

- `main` calls `argparse.parse_args`. On a parse error, argparse writes usage plus the offending token (`unrecognized arguments: …`) to the tool's stderr before the `SystemExit` that line 862 onward catches.
- This echoes the caller's own argv, not journal data. If a harness captures the tool's stderr verbatim, an accidental secret on the command line would be copied into the raw stream files.
- **Smallest fix:** `ArgumentParser(exit_on_error=False)` (Python ≥3.9), or override `error()` so it raises without printing.

### F3 — INFO: MESSAGE-free acquisition is enforced only by the request, not by checking the records

- **Requested fields:** `--output-fields=__CURSOR,_BOOT_ID,MESSAGE_ID,UNIT_RESULT,EXIT_CODE,EXIT_STATUS` (OUTPUT_FIELDS line 47, argv lines 428–438). `--cursor=<anchor>` is a single argv element with no shell. Anchor cursors are printable ASCII and may not start with `-`. There is no `--after-cursor`, `-f`, vacuum or rotate.
- **What happens to records:** `_evaluate` reads only `__CURSOR`, `_BOOT_ID`, `MESSAGE_ID`, `UNIT_RESULT`, `EXIT_CODE` and `EXIT_STATUS`. Records are parsed into memory and discarded; record bytes never reach stdout.
- **What is not checked:** a record that does carry `MESSAGE` (old journalctl, or a hostile or wrapper stub) is accepted and counted. Nothing is leaked, but nothing proves "MESSAGE-free".
- **Optional hardening:** set the result to unavailable when any record has a key outside OUTPUT_FIELDS plus the fields journalctl always adds (`__REALTIME_TIMESTAMP`, `__MONOTONIC_TIMESTAMP`).
- **Weak selftest check:** the argv assertion `"MESSAGE," in fields[1]` would miss a trailing `,MESSAGE`. An exact field-list equality check already exists, so this only matters as a reviewer note.

### F4 — INFO: the child process can be left running if the tool is interrupted mid-capture

- On timeout or overflow, `_kill_reap` sends SIGKILL to the owned child's process group (`start_new_session=True`, plus a check that pgid == pid), then reaps with a bounded wait. That scope is correct.
- If a KeyboardInterrupt or other BaseException hits inside the select loop, the top-level handler at the bottom of the file prints `internal-error` but never kills the child. The child is in its own session, so terminal SIGINT does not reach it.
- journalctl without follow mode exits on its own, so this is bounded. The fix is a `try/except BaseException: _kill_reap(proc); raise` around the loop.

### No defect found

- **Credential reads:** the production path reads only the `--anchor` file and runs the selected journalctl. It does not touch `~/.omp`, `agent.db`, `.ssh`, or any token or auth file.
- **Arbitrary writes:** the production path writes nothing. The selftest writes only inside `tempfile.TemporaryDirectory(prefix="mori-journal-window-selftest-")`, which the contract allows for an isolated selftest. The stub writes argv only to `MJW_ARGV_FILE`, which the selftest always points inside that temp tree.
  - Residual: the stub falls back to `/dev/null` when `MJW_ARGV_FILE` is unset. However, the stub only exists inside the temp tree.
- **Stdout leakage:**
  - `_fail` emits only `finding_id`, `reason`, `scope` and `anchor_sha256`.
  - The OK object emits counts, `evidence_basis`, `cursor_semantics`, `anchor_sha256` and `end_cursor_sha256`. No raw cursor or record is emitted.
  - Stderr bytes are only counted (`err_len`) and never stored. Any stderr makes the result unavailable (`stderr-nonempty`), checked before the timeout and rc checks.
  - Top-level exceptions print no traceback.
- **The Stderr pack's canary `ghp_MORI_STDERR_CANARYx9f8e7d6c5b4a3` is synthetic.** It does not match the real `ghp_`+36 base62 token format, since it contains underscores.
  - The tool's own selftest no-echo list does not include it. Proving the tool never echoes this canary therefore falls to the WindowHarness gate.
  - I did not see `tools/mori-round16-regressions.py` at review time, so I could not check whether the harness asserts it.
- **Fixtures:** no record in any pack carries a `MESSAGE` key. The only `MESSAGE` text is inside a synthetic stderr string in `Stderr.json` case 2 ("unrecognized field 'MESSAGE'"). All fixture data is synthetic: boot ids are repeated hex letters, and unit names are fleet or synthetic. No real hostnames, paths or credentials appear.
- **Catalog IDs:** `MSGID_UNIT_FAILURE d9b373ed55a64feb8242e02dbe79a49c` matches `tools/mori-census.sh:1036` and `mori-round15-regressions.py:148`. The `d9b373ed55a64e6c8e2e7d70a0fce472` hint in the PackUnitOom assignment text appears in no file I read. No pack uses that hint.

## Omissions

- `tools/mori-round16-regressions.py` did not exist when I read the tree, so the harness was not reviewed.

## Process disclosure (sent to MoriR16.Lesson)

- Before L1's clarification, I ran one bounded file-existence wait: a `sleep 10`/`ls` loop in the mori-shokunin cwd, 440 s, which stopped once the tool and 13+ fixtures existed.
- I also ran two read-only `sha256sum` calls over the tool and fixtures; the second also ran `wc -l`. Both returned 2314bd… for the tool. MoriR16.Lesson recorded this as M30.
- No journalctl, no execution of the tool under review, and no writes other than this report. None of this counts as verification.
- Tools installed or updated: none.

## Fixture sha256 at read time

```
d41bf9577ff45d8f84221ecd3acaa391828d3233a1671168b0dd88223e9081b2  AnchorValidation.json
af6ed035d4bde0db6b8ad0fc8247f978061ea4fbc3749095ad5a4905a1f5a848  BootBoundary.json
30d07289219041cd0f0d4edd92b6de68405d2b95f177bf653178989a23871076  Bounds.json
b29a4a1d5820783f7519bf44a2f54b99b13765e9d80a3b6196ddb9b76c8436c6  CursorShape.json
193dc63cdc8334da067ba23792826c8ff42be38a86a8e2610f852ecf24b7cbd3  ExactAnchor.json
a12bc349c010b053e7e7360ec12f9dd8d7921c2e0849e128547d1c5648b73222  KernelSystem.json
a0db2726d3a04429f9d7e5ef25429d15f7af39d2c77881fa87023941a62851be  KernelUser.json
483a539dfd6c3221394a666422991cddd07bfb1fcc706e65c6130a0a19ad2aed  MalformedCapture.json
fca571e28ceeb7acf25afea9540b375fa2a071f5bb57e3f66e196cd51c1a7646  MissingAnchor.json
af911e7404bc7078977265a502a83be094cd249951133ae3e2855064a9f2f8c2  ProcessSignal.json
ffc9c0cccb77886d5bfe64fe76fa6f2ef177949c3718205f06950aa110d970fb  ProducerFailure.json
9764c4277412e2a5caec32f6f8225da2289a40dda9e53f2661dce5d252090594  RecordShape.json
88faf83d5ef8650c1174dc21331fe2731968279ea248001f5c07fbbf171c7348  Stderr.json
f827bffef9328ae1584a34cb074b52f14a67161a6f3f1d9024c4e513495be001  TypedFields.json
b333347a8cf93207fcd21bc753ac0a62f779abc3b3d9dd90fd7b15c380ce0665  UnitOom.json
6c08238a05ae774d820f8961893231c55d02af40685aa1b46cd73af0aaf175d1  UnitSignal.json
```

# PackStderr — round-16 fixture pack report

## Files changed
- `.ufo/waves/round-16/fixtures/Stderr.json` (new, 4670 bytes, 4 cases). Own-file only; no other writes outside this report.

## Behavior delivered
Shared-schema pack `{"cases":[...]}` targeting the stderr leg of the capture contract
(`nonzero rc, stderr, timeout, overflow -> rc2 unavailable`). Every case is a
**stderr-bearing success**: the producer wrapper exits `returncode: 0` with a
syntactically valid, fully self-consistent JSONL stdout (anchor record first with
EXACT `__CURSOR` + `_BOOT_ID` equality, later records same-boot with unique scalar
cursors, no `MESSAGE` field, only contracted output-fields). The refusal is therefore
attributable solely to nonempty stderr — disjoint from PackProducerFailure
(nonzero-rc band), PackMissingAnchor (empty/nearest stdout), and
PackMalformedCapture (truncated stdout).

Cases:
1. `stderr-rc0-benign-warning-vacates-clean-user-window` — scope user, anchor-only
   stdout + single benign rotation warning on stderr. Even a clean window must
   refuse: rc2 `MORI_JOURNAL_WINDOW_UNAVAILABLE`.
2. `stderr-rc0-secret-canary-suppresses-all-positives-user` — scope user, anchor +
   four post-anchor records covering all four r15 positive predicates
   (fe6faa94 kernel-OOM, d9b373ed + UNIT_RESULT=oom-kill, d9b373ed +
   UNIT_RESULT=signal, 98e32220 + EXIT_CODE=killed/EXIT_STATUS="9"). stderr carries
   a secret-shaped canary `ghp_MORI_STDERR_CANARYx9f8e7d6c5b4a3` embedding the exact
   census leak token. Asserts: positives are never salvaged through a tainted
   capture, and if the tool echoes the canary into stdout the fixture is detectable
   in the harness's recorded raw streams (contract: stdout must not echo stderr).
3. `stderr-rc0-multiline-warning-vacates-system-window` — scope system coverage:
   multi-line stderr (rotation warning + an `--output-fields` complaint whose text
   contains the literal token `MESSAGE`) still refuses; stderr text mentioning
   "MESSAGE" is a warning, not a data leak.
4. `stderr-rc0-smuggled-record-never-data-user` — scope user, anchor-only stdout +
   stderr carrying a full forged positive JSONL record (fe6faa94, same boot, its
   own cursor). Pins "stderr is never a data path" (census.sh comment, line ~1134):
   the record cannot smuggle in a count, and stderr still refuses.

## Verified source bytes (tools/mori-census.sh)
- Catalog ids read at source: `JOURNAL_ID_KERNEL_OOM=fe6faa94e7774663a0da52717891d8ef`
  (line 1032), `JOURNAL_ID_UNIT_SIGKILL=98e322203f7a4ed290d09fe03c09fe15` (line 1035),
  `JOURNAL_ID_UNIT_FAILURE=d9b373ed55a64feb8242e02dbe79a49c` (line 1036); benign
  controls `d989611b15e44c9dbf31e3c81256e4ed` (oomd_notice) and
  `fc2e22bc6ee647b6b90729ab34a250b1` (coredump_notice) from the class table at
  lines 909–916.
- Canary token `MORI_STDERR_CANARY` read verbatim at line 3461
  (`journal-stderr` fixture: `warning: partial journal access MORI_STDERR_CANARY`)
  with the never-echo check at line 3465. My secret-shaped variant wraps the exact
  token so existing substring leak checks still fire.
- Unavailable vocabulary: census emits `unavailable:stderr-nonempty`
  (`JQ_STATUS=stderr-nonempty` line 1211; selftest `unavailable:stderr-nonempty`
  expectation lines 1862/1945). RECOMMENDED reason token for the window tool:
  `stderr-nonempty`.

## Schema decisions / assumptions
- `"want": {}` on all refusal cases, matching the landed sibling convention
  (ProducerFailure, BootBoundary, CursorShape). The unstable `reason` string is not
  pinned because it is WindowTool-owned; `stderr-nonempty` is my proposal.
- "stderr-bearing success" read as rc0 + nonempty stderr; literal rc0 outcome is
  contract-impossible with stderr.
- No pack field asserts "stdout must not contain stderr bytes"; relying on the
  contract guarantee plus harness raw-stream recording. Flagged to WindowHarness.
- Static self-check of the pack only (JSON parse, anchor equality, unique cursors,
  same-boot, no MESSAGE): passed. No tool/harness runs — none exist yet and none
  are permitted.

## Risks / blockers
- If WindowHarness wants an explicit never-echo `want` key (e.g. `stdout_excludes`),
  case 2 will be extended on request; no blocker.
- If WindowTool ships a different stderr reason token, nothing in this pack depends
  on it (want is `{}`).
- No live probes, jobs, gates, or executions performed; nothing to disclose beyond
  static file reads and this write. Tooling installs: none.

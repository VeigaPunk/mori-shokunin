# C1 privacy and filesystem falsification — round 17 wave 2

## Axes and verdict

Axes attacked: (1) field-level privacy, (2) scan completeness/correctness, (3) filesystem availability, and (4) retained-evidence provenance. Static review and receipt inspection only; no live transcript was opened, no selftest/probe was run, and no source was edited. C1's output projection is narrow, but the implementation still has a field-boundary mismatch, an evidence-path privacy issue, and filesystem failure modes that can fabricate a clean scan or hang it.

## Findings

### HIGH — suppressed traversal errors can produce a false clean

- **Exploit path:** make a nested directory unreadable, or cause a directory enumeration error while the sessions root remains a directory. `os.walk` is called without an `onerror` callback; Python's default walk behavior ignores enumeration errors [INFERENCE]. The walk then returns only a partial tree (or no entries), and the scanner can return `MORI_SEAT_TERMINAL_OK` with rc 0 rather than setup/unavailable. Separately, a failing `lstat` for a `.jsonl` path is explicitly skipped.
- **Evidence:** `tools/mori-seat-terminal.py:416-420` (`isdir`, then `os.walk` without `onerror`); `:427-433` (`lstat` `OSError` → `continue`); `:486-502` (totals and OK/DEAD rc derive only from discovered records). `main` only maps raised exceptions to `internal-error` at `:1827-1830`; these suppressed/continued errors never reach it.
- **Impact:** an incomplete scan can falsely claim zero dead seats, defeating the terminal-status report's core purpose.
- **Smallest remediation:** make directory-walk errors fatal (`onerror` raises a setup error) and treat per-file `lstat` failures as unavailable/setup rather than silently omitting them. Add a read-only directory-permission/traversal-error case to the fixture gate.

### MEDIUM — a regular-file-to-FIFO race can hang the scan

- **Exploit path:** after discovery accepts a regular `*.jsonl` at `:428-432`, replace that path with a FIFO before `_read_head` or `_read_tail` opens it. Both open calls use `O_RDONLY | O_NOFOLLOW` but omit `O_NONBLOCK` (`:278-280`, `:319-324`). `O_NOFOLLOW` prevents following a final-component symlink, not opening a FIFO; a blocking read-only FIFO open can wait indefinitely [INFERENCE]. The lstat/open race is not exercised by the recorded static FIFO fixture.
- **Impact:** an untrusted concurrent writer can stall the single-process scan indefinitely; `--max-tail-bytes` does not bound time spent waiting in `open`.
- **Smallest remediation:** open with nonblocking semantics, then `fstat` the opened descriptor and reject anything but a regular file. Prefer one safely opened descriptor for header and tail so the type/identity check applies to the bytes actually read.

### MEDIUM — the sessions root can itself be a symlink

- **Exploit path:** pass a symlink as `--sessions-dir` pointing outside the intended sessions directory. `os.path.isdir` follows it, and `os.walk` starts at that path; `followlinks=False` only prevents recursion through symlinked child directories, not the top-level argument [INFERENCE].
- **Evidence:** `tools/mori-seat-terminal.py:416-420`; the recorded fixture name `symlinks_never_followed` is a child-entry case (`evidence/seat-after/expected.json`), not a root-symlink case. The committed receipt records 54/54 fixture matches but no root-symlink arm (`evidence/seat-after/run-manifest.json`).
- **Impact:** the tool may read and classify files from a caller-unintended directory, emitting their seat/prefix/provider/model and terminal-class metadata.
- **Smallest remediation:** reject a symlink root before walking; if the contract means no symlink in any path component, use descriptor-relative traversal with no-follow checks for each component. Add a root-symlink regression case.

### MEDIUM — source reads exceed the binding field allowlist, despite narrow output keys

- **Exploit path:** a transcript line may contain arbitrary `content`, `usage`, and other unapproved members. `_terminal_view` calls `json.loads` on each complete line, materializing every member before selecting `type` and `message` (`tools/mori-seat-terminal.py:357-364`). For message records, `_message_view` copies the complete `message.errorMessage` into `error_message`, returns it in the view, and uses it for substring/regex matching (`:207-244`, `:247-273`). It also reads message- and record-level `completedAt`/`timestamp` (`:235-239`). The binding allowlist in `wave1-context.txt:9` permits only specified status/provider fields, named error-message class tokens, and retry-recovery key shape; it does not authorize arbitrary JSON members, the full error-message string, or those timestamps. Amendment A1 requires timestamp/retry-derived results (`contract.md:113,119`), so the binding rules need an explicit reconciliation.
- **Impact:** forbidden transcript values are parsed/materialized and the full error string is retained transiently in the in-memory view even though they are not part of the output. This is a field-minimization/policy defect, not an observed output disclosure.
- **Smallest remediation:** reconcile the binding allowlist with the A1 fields actually required, then parse/project only those fields and immediately reduce error text to the specifically allowed class flags/count/code; never keep the original `errorMessage` in the view. A streaming/token parser is needed if “unread” means unapproved members must not be materialized by JSON decoding.

### MEDIUM — committed live receipt retains an OMP session-directory identifier

- **Exploit path:** the live C1 receipt records the exact command arguments. `evidence/seat-live.json: argv[3]` contains the absolute `--sessions-dir` argument, including an OMP session-directory identifier. The value is intentionally omitted here; this is session-identifying metadata, not a reproduced credential. The receipt is tracked (`git ls-files --error-unmatch .ufo/waves/round-17/evidence/seat-live.json` succeeded). The scanner also returns the supplied path as `sessions_dir` (`tools/mori-seat-terminal.py:487-492`), so retaining its raw stdout would carry the same path [INFERENCE].
- **Impact:** a committed evidence reader can correlate the measurement to a specific OMP session directory; this exceeds the minimal evidence needed to establish the result.
- **Smallest remediation:** redact/replace the session-directory argument and corresponding output path before committing evidence (for example, preserve a stable non-reversible placeholder), and update the receipt contract so exact argv does not require retaining the identifier.

## Retained-evidence check (safe projection only)

- Read-only receipt scan covered 145 JSON and C1 run-output receipts under `evidence/`; it parsed 55 C1 result JSON documents and emitted only path/key/class summaries. It found no `content`, `usage`, `errorMessage`, `credential_pin`/credential-key, or transcript-record fields in retained structured outputs, no output-seat-key mismatch, and no matching credential-shaped string. Setup-error responses use their diagnostic `reason`/limit keys as expected. No secret or transcript value was copied into this report. This is a bounded-pattern/field-name scan, not proof that arbitrary secret encodings are absent.
- `git -C /home/vgpnk/Projects/shokunin/mori-shokunin ls-files -- '*.jsonl'` returned 72 tracked paths; the path inventory was confined to `.ufo/waves/round-17/fixtures/seat/`, not live-session or evidence-output paths. The contract (`contract.md:77-82`) defines these as synthetic fixtures. I did not open their JSONL bytes. One pathname is `CredentialPinTrap/credential-trap.jsonl`; its contents were deliberately not read, so the synthetic-only status of that one file is [INFERENCE] from the fixture contract, not independently content-verified.
- `PINNED_INPUTS.json:13-18` pins the fixture expected file and records the 54-case claim; the retained after-gate manifest reports 54 matches, 0 mismatches, and 0 capability-absent cases. The fixture gate covers ordinary child symlink/FIFO skipping and bounded-tail cases, but its recorded results do not exercise the root-symlink, walk-error, or concurrent replacement paths above.
- `corpus/lessons/round-17.md:74` records the earlier `credential_pin`-line display in `build/SentinelTranscripts.md` and states no value was retained in the report/corpus. That prior display remains a disclosed process breach; it is not evidence of prevention. No value is repeated here.

## Scope limits

No live transcript files, credential files, agent database, raw `credential_pin` record, or fixture JSONL content were read. No live probe, test, selftest, lint, build, or mutation was performed. Findings about races and filesystem behavior are static exploit scenarios, not executed demonstrations.

## Follow-up — settled SeatTool clone review (static only)

Reviewed only `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/SeatTool/tools/mori-seat-terminal.py`; read-only `sha256sum` returned `e2991600bbee98f5816aea280c1901e100be9e3bdac07ca3e8e2d3a1c2790b10` (rc 0). No test, selftest, live probe, or transcript read.

- **F1, walk/lstat false-clean: FIXED in this clone.** `_collect_entries` turns `scandir`, entry-stat, and child-directory-open errors into setup errors (`:698-701`, `:703-737`); it no longer silently drops failing `lstat` entries. The scan therefore cannot report a complete clean result after those traversal failures.
- **F2, FIFO replacement hang: FIXED in this clone.** `_file_flags` includes `O_NONBLOCK|O_NOFOLLOW` (`:634-639`); `_open_regular_at` checks the opened descriptor is regular (`:669-681`); `_scan` uses that descriptor for header and tail (`:857-869`, `:763-780`). A regular-to-FIFO replacement no longer blocks the open and is not read as a regular transcript.
- **F3, root symlink: FIXED for the `--sessions-dir` final component.** The trailing-separator-normalized root is checked with `islink`, and root open also uses `O_NOFOLLOW|O_DIRECTORY` (`:835-842`, `:626-646`). Residual scope caveat: opening the caller's root pathname still resolves any symlink in an *ancestor component* before the root descriptor is obtained; if “never follow symlinks” covers the entire supplied pathname, this remains [INFERENCE] and requires component-by-component root opening.
- **F4, content/error-message materialization: SUBSTANTIALLY FIXED.** The custom bounded projector traverses unapproved values structurally without decoding/copying them (`:253-385`, `:416-518`), and reduces `errorMessage` directly to booleans/count/code rather than retaining its text (`:488-508`). It does inspect bounded input bytes for syntax and tokens, but no longer materializes the unapproved fields or full error string.

### Remaining static counterexamples

- **MEDIUM — skipped-value JSON syntax is not strict.** `_scan_string` skips any backslash plus next byte without validating JSON escape forms (`:270-280`); `_scan_value` accepts an arbitrary run of digits and `+-.eE` as a number (`:315-322`). Consequently malformed skipped members (for example, an invalid escape or a number with an embedded plus) can be accepted as part of an otherwise classifiable message, contrary to the malformed-line skip/strict-syntax contract. This is static; no malformed input was executed. **Remediation:** validate escapes, UTF-8, and the complete JSON number grammar while structurally skipping values; reject the whole line on any invalid token.
- **MEDIUM — escaped class tokens are missed.** The clone searches raw JSON-string bytes for literal ASCII spellings and explicitly documents that escaped spellings are ignored (`:37-39`, `:488-507`; token set `:123-132`). A valid JSON `errorMessage` whose decoded text contains a contract token via `\\u` escapes will not set the corresponding class flag. This can change quota/rate classification (although not necessarily the dead/non-dead result). **Remediation:** decode only enough of the JSON string escape stream to recognize the approved tokens, without retaining the full string.
- **MEDIUM — overlong unknown Z.AI codes bypass the unknown-code guard.** `_ERROR_CODE_RE` only captures 1–12 digits (`:139-140`). For a Z.AI error containing a syntactically valid `(type=<13-or-more digits>)` and `errorStatus == 429`, the code is not captured; `_classify` then misses its `provider == zai and error_code is not None` guard and falls through to the generic 429 branch (`:578-593`), classifying rate-limit from status alone. This contradicts the unknown-Z.AI-code qualification at `:65-70`. **Remediation:** preserve an “unknown code present” bit even when the digits exceed the display bound, and keep the Z.AI 429-only path conservative.
- **MEDIUM — documented rate token omitted.** `contract.md:112` includes `resource_exhausted` among rate-limit tokens, but the clone's `RATE_TOKENS` omits it and explicitly says not to treat it as rate evidence (`:121-132`). An aged error whose only rate evidence is that token will fall through to another class (`:590-594`), contrary to the settled contract. **Remediation:** restore the contract-listed token or obtain an explicit contract/fixture revision before admission.
- **LOW/MEDIUM — non-integral timestamps/status/version are truncated.** `_parse_int_span` falls back from `int()` to `float()` and then `int(value)` (`:388-406`). Thus a valid JSON decimal timestamp just above the settle cutoff can truncate to the cutoff and be treated as aged; decimal schema versions/statuses can also be silently converted to integers. **Remediation:** accept only integer-form JSON numbers for schema version, status, and epoch-millisecond fields.

### Evidence-path disposition

The clone review does not change or redact `evidence/seat-live.json`. The coordinator states that L1 will canonical-redact the final live receipt path and mark that transformation, while leaving the historical receipt untouched. Treat the previously reported session-directory identifier as metadata (not an authentication credential); its retention remains a privacy-minimization finding until the final redacted receipt is observed.

## Final A2 static disposition — settled SeatTool clone

Reviewed only the clone source at SHA-256 `93d7948786285a1f91eff09573c099f46df58ee5cb8c1992db5977ece2b3635d`; read-only `sha256sum` returned that exact digest (rc 0). No probes, tests, selftests, live reads, or source edits.

- **Report line 63, strict syntax for skipped members: FIXED.** `_scan_string` validates JSON escapes and raw UTF-8 (`:272-336`); `_scan_number` implements the JSON integer/fraction/exponent grammar (`:339-370`); the structural walker requires valid nested values and the projector rejects trailing bytes (`:421-456`, `:638-668`). I found no counterexample in the assigned syntax scope.
- **Report line 64, escaped error tokens: FIXED.** `_iter_decoded` handles JSON escapes and ASCII `\\u` spellings without creating the full text (`:493-552`); `_error_metadata` performs bounded streaming matching (`:555-635`), and the projected view retains only derived metadata (`:711-720`). No counterexample found in the assigned token-stream scope.
- **Report line 65, overlong unknown Z.AI code: FIXED.** The reducer records an over-12-digit `(type=...)` as `unknown_code_present` (`:585-598`); `_classify` includes that bit in `code_present` and prevents status-429-only classification for a Z.AI code (`:791-804`). No counterexample found in the assigned unknown-code bound.
- **Report line 67, integer-only selected fields: FIXED.** `_INT_RE.fullmatch` accepts only integer-form JSON numbers and rejects floats/exponents (`:147-148`, `:473-483`); header version, error status, and timestamps use that parser (`:655-662`, `:701-710`, `:740-742`). No truncation counterexample remains in the assigned fields.
- **Report line 66, `resource_exhausted`: WITHDRAWN under A2.** The coordinator states A2 intentionally removes bare `resource_exhausted`; the prior omission is therefore not a defect against the current contract. I do not recommend restoring that token.
- **Report line 58, root-ancestor caveat: OUT OF SCOPE under A2.** The coordinator states A2 scopes caller root-ancestor selection; the final-component root-symlink check and descriptor-relative child walk are the reviewed boundary. I do not retain the prior ancestor-path caveat as a current defect.

**Disposition:** no surviving counterexample found among the specific report-line 63–67 items in this clone. This is a static disposition only, not a blanket pass of C1 or a verification of the planned live-receipt redaction; the historical receipt remains unchanged per coordinator instruction.

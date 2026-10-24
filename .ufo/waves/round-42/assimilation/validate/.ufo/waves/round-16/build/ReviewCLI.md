# ReviewCLI — round-16 window CLI input/exit contract and safe diagnostics

Lane: ReviewCLI (reviewer, leaf). Read-only except this report. No execution, no tests, no builds, no journal queries, no secrets opened.

## Read-time state (explicit)

- Read at 2026-10-20T08:48:46Z and re-checked at 2026-10-20T08:50:03Z.
- `tools/mori-journal-window.py`: **ABSENT** at both reads (`stat` returns ENOENT; `tools/` lists only `mori-census.sh`, `mori-round13/14/15-regressions.py`, `mori-silence-cases.sh`). The WindowTool executor has not landed its file. A sibling report (`build/ReviewCapture.md`, read at 08:50) records the same absence.
- `tools/mori-round16-regressions.py`: also absent. Harness and fixture review is out of this lane.
- Git HEAD `b83edc6ee3db6822382ab673d7e6e984e420f22f`; `git status` shows `?? .ufo/waves/round-16/` plus modified `LOG.md`, `PROVINCE.md`, `SCORECARD.md`, `corpus/SOURCES.md`. None of the modified paths is the CLI.

**Therefore no finding below is a verdict on production code.** This review checks the written interface contract (spec `wave1-spec.json` `WindowTool` prompt, the task `# Interface` and `# Fixture and harness contract` text, and r15 predicates) for defects that would make a faithful implementation wrong, unsafe, or unverifiable. Each finding names the contract text it attacks. L1 should re-review the file once it lands, recording a new read-time.

Sources read: `wave1-spec.json` (WindowTool at line 10, ReviewCLI at 228–231, context header line 3), `corpus/knowledge/journal-positive-evidence-r15.md` (sections 2–6, r15 predicates, S014/S015 claims), `corpus/knowledge/structured-journal-scopes-r13.md:20-23` (`-q` and `--output-fields` semantics), `tools/mori-census.sh:1164-1203` (existing `journal_query` argv, scope flag, `-b`, `--no-pager`, stderr-byte handling), and `.ufo/waves/round-15/build/AttackNoHarm.md`, `AttackSuppression.md`, `AttackSignalConfusion.md` for r15 predicate traps.

## Summary by severity

| # | Sev | Topic | Attacked contract text |
|---|---|---|---|
| F1 | High | Scope selection flag absent from the query argv | `Query one scope with --cursor=<anchor> --no-tail --quiet --output=json ...` |
| F2 | High | No catch-all: rc2 is shared, argparse and uncaught exceptions can break "stdout one JSON object" and "stderr never echoed" | `stdout one JSON object`; `rc2 unavailable`; `setup ... rc2 MORI_JOURNAL_WINDOW_SETUP` |
| F3 | High | "End cursor reported" conflicts with "MUST NOT echo raw cursor" | `End cursor optional reported but not written`; `stdout MUST NOT echo raw cursor` |
| F4 | Medium-High | Missing anchor file: setup or unavailable? Spec gives two answers | Goal `missing/vacuumed anchor ... stay unavailable`; WindowTool `Missing anchor continuity means unavailable not clean`; Interface `setup invalid anchor ... rc2 SETUP` |
| F5 | Medium | Python port of r15 `EXIT_STATUS == 9` accepts `9.0` through `==` | r15 predicate `scalar status 9`; C-5 "reject floats" |
| F6 | Medium | JSON parse hardening absent from contract (NaN, duplicate keys, int-digit limit, recursion) | `malformed ... -> rc2 unavailable` (no list of parse failure classes) |
| F7 | Medium | `-q` hides inaccessible-journal warnings: rc0 can be partial coverage | `--quiet`; success finding has no coverage disclosure |
| F8 | Medium | Anchor file read is unbounded and accepts any file type (FIFO, device, directory) | `--anchor PATH`; anchor "exactly schema" |
| F9 | Medium | `--timeout`, `--max-bytes`, `--journalctl` have no types, defaults, bounds, or NaN/inf rules | `[--timeout SECONDS] [--max-bytes N]` |
| F10 | Low-Med | Record cursor validity undefined ("unique valid scalar cursor"); 4096 applies only to anchor | `unique valid scalar cursor` |
| F11 | Low-Med | Stable reason enum never enumerated; harness cannot pin strings | `reason stable` |
| F12 | Low | `records_after_anchor` and uniqueness set: counted population and memory bound unspecified | `records_after_anchor`; `unique` |
| F13 | Low | Child environment and argv hygiene not specified (`--no-pager`, list argv, cursor `=` form) | argv contract |
| F14 | Info | Positive checks of the contract that are correct and should be preserved | — |

## Findings

### F1 — High — Scope selection flag is not in the query argv

**Contract text.** `Query one scope with --cursor=<anchor> --no-tail --quiet --output=json --output-fields=__CURSOR,_BOOT_ID,MESSAGE_ID,UNIT_RESULT,EXIT_CODE,EXIT_STATUS`, and `--scope user|system`.

**Evidence.** The argv list contains no `--user` or `--system`. Without one, journalctl picks its default journal, which depends on the caller's uid and privileges. The existing census selects scope through its `flag` parameter (`tools/mori-census.sh:1164`, `1190`: `"$JOURNALCTL_BIN" "$flag" -b --no-pager -o json ...`). The window contract has no equivalent.

**Why it matters.** If the implementation omits the flag, `--scope user` and `--scope system` can return the same stream. A user-scope positive can then be attributed to system, or both scopes can read the same records. Both outcomes are silent mislabels. The r15 rule that positives are "per-scope" and never summed across scopes depends on this.

**Required.** The spec must map `user` to `--user` and `system` to `--system` in the argv list, and a test must show that the argv for each scope contains the right flag and not the other. The harness wrapper must record the argv it saw, so an argv check can fail on a missing or swapped flag.

### F2 — High — No catch-all; rc2 is shared; argparse and exceptions can break the JSON stdout contract

**Contract text.** `stdout one JSON object`; `Any unavailable returns rc2 ... setup invalid anchor/args -> rc2 MORI_JOURNAL_WINDOW_SETUP`; `stderr never echoed`.

**Evidence and risks.**
1. Python `argparse` exits with status **2** on any parse error (unknown flag, bad choice for `--scope`, bad int/float for `--max-bytes`/`--timeout`). It writes usage and the offending value to **stderr** and prints nothing to stdout. That breaks "stdout one JSON object" and places a caller-supplied value on stderr. Its rc2 collides with the unavailable rc2 and the setup rc2, so the rc alone cannot classify the result.
2. rc1 is not mentioned. An uncaught Python exception exits 1 and writes a traceback to stderr. A traceback can include `repr()` of locals, including a cursor or record fragment. That is exactly the leak the contract forbids.
3. `--selftest` has no stated stdout or rc contract beyond "asserts rc+stable finding id".

**Required.**
- Define the exit code set, for example `0` success, `2` every JSON-reported refusal (setup and unavailable, distinguished only by `finding_id`), and reserve a value for "no JSON could be produced". Say whether argparse errors must become a JSON `MORI_JOURNAL_WINDOW_SETUP` object on stdout. If argparse errors stay on stderr, say so and say that stdout is then empty, which violates the one-object rule.
- Require a top-level `try/except BaseException` in `main()` that emits a fixed JSON setup or unavailable object with a fixed reason and no exception text. Tracebacks must be suppressed or replaced by a fixed string.
- Specify what `--selftest` prints on stdout and its rc.

### F3 — High — End cursor: reported versus never echoed

**Contract text.** `End cursor optional reported but not written.` and `stdout MUST NOT echo raw cursor or records; safe anchor SHA256 allowed.`

**Evidence.** The two clauses do not agree. "Reported" implies the value is in stdout. Raw reporting breaks the no-echo rule. Only the anchor's SHA256 is named as safe; no digest rule is given for the end cursor.

**Required.** Choose one: (a) drop the end cursor from stdout; (b) report `end_cursor_sha256` computed the same way as the anchor digest, and name the digest input exactly (the cursor string, not the file bytes). Also decide whether a SHA256 of a cursor is acceptable at all. Cursors encode boot id and timestamps and are not secret, so it probably is, but the spec should say so rather than leave the digest input unnamed. Note also that "safe anchor SHA256" does not say whether the digest covers the cursor or the anchor file. Pin one.

### F4 — Medium-High — Missing anchor: setup or unavailable?

**Contract text.**
- Goal: `missing/vacuumed anchor ... stay unavailable`.
- WindowTool: `Missing anchor continuity means unavailable not clean.`
- Interface: `setup invalid anchor/args -> rc2 MORI_JOURNAL_WINDOW_SETUP`.

**Evidence.** A non-existent or unreadable anchor PATH is both "missing anchor" and "invalid anchor". The three sentences point at two finding ids. A vacuumed cursor is a different case: journalctl fails or returns no anchor record, which maps to unavailable, which is consistent.

**Required.** State it explicitly: a missing or unreadable anchor file → `MORI_JOURNAL_WINDOW_UNAVAILABLE` with a stable reason such as `anchor-missing`; a file that exists but fails schema → `MORI_JOURNAL_WINDOW_SETUP`. Also decide whether "missing" means "not created yet" (which should be unavailable, never clean) or "bad path argument". Pin the reason strings for the harness.

### F5 — Medium — Python equality accepts float 9.0 as status 9

**Contract text.** The r15 predicate for `positive_process_sigkill`: `EXIT_STATUS` is "scalar equal to 9", with the r15 rule that `9.0` must be rejected (`journal-positive-evidence-r15.md` §2; `AttackNoHarm`/C-5 "Reject arrays, objects, floats, and nulls").

**Evidence.** In Python, `9.0 == 9` is `True`, `True == 1`, and `json.loads("9e0")` yields float `9.0`. A predicate written as `x == 9` or `x in (9, "9")` therefore accepts a float, which the jq `tostring == "9"` rule rejects (`9.0|tostring == "9.0"`). The r15 text itself names this trap (C-5).

**Required.** The predicate must be `(type(x) is str and x == "9") or (type(x) is int and x == 9)`. `bool` must be rejected explicitly (`type(x) is int` already does, but say so). The contract should list `9.0`, `9e0`, `"9.0"`, `" 9"`, `"09"`, `true`, `[9]`, `null` as reject fixtures for the window harness. They are the same vectors the r15 attacks named.

### F6 — Medium — JSON parse hardening not in the contract

**Contract text.** `Malformed/empty capture ... -> rc2 unavailable` (no list of parse failure classes).

**Evidence.** Python's `json` module, with default arguments:
- accepts `NaN`, `Infinity`, `-Infinity` as numbers;
- keeps the last value of a duplicate key silently;
- raises `ValueError` for integers over the `sys.int_info`/`set_int_max_str_digits` limit (default 4300 digits), which is an exception type, not a parse result;
- raises `RecursionError` on deep nesting, which is not a `JSONDecodeError`.

If any of these escape, the result is a crash (F2) or a silently different record (duplicate keys).

**Required.** The spec must say that every JSONL line is parsed with `parse_constant` rejecting the three constants, `object_pairs_hook` rejecting duplicate keys, and that any `ValueError`, `RecursionError`, `JSONDecodeError`, or non-dict top-level value makes the whole capture `unavailable:malformed-json`. It must keep the r15 rule: no line-wise salvage, no `?`-tolerant repair, and a blank line in the middle of the capture is malformed.

### F7 — Medium — `--quiet` can hide partial coverage; success needs a disclosure

**Contract text.** `--quiet`; success returns `finding_id=MORI_JOURNAL_WINDOW_OK` with counts and `evidence_basis=validated-record-subsets`.

**Evidence.** `structured-journal-scopes-r13.md:23` records S014: `-q` suppresses "any warning messages regarding inaccessible system journals when run as a normal user". The spec names "stderr nonempty → unavailable". Under `-q`, a non-root run that cannot read some journal files produces **rc0, empty stderr, and a partial stream**. The window then reports a clean success with fewer records, and positives of `0` look like absence. The r15 text explicitly warns that stderr silence is not access proof.

**Required.** Either (a) add an explicit `coverage` field to the success object, such as `coverage=unverified-access` with a note that the journal's inaccessible-file warnings are suppressed by `-q`, or (b) drop `-q` and accept that non-root runs will become unavailable when that message appears. Either way the success finding must not read as complete. The r15 `positive_basis=validated-subset-lower-bound` pattern applies; a zero must not be described as "no event".

### F8 — Medium — Anchor file read is unbounded and accepts any file type

**Contract text.** `--anchor PATH`; anchor "exactly schema mori-journal-anchor-v1".

**Evidence.** Nothing caps the anchor size or requires a regular file. A FIFO opened for reading blocks forever. A device or huge file exhausts memory. A directory fails with a generic `IsADirectoryError`, which then depends on F2 for its handling. The `--journalctl PATH` argument has the same class of issue: it is executed, so it must be an existing regular executable file.

**Required.** `os.stat` (follow symlinks is a choice; say which) then `S_ISREG`, with a byte cap (for example 64 KiB) read via a bounded `read(cap+1)`. Non-regular or oversize → setup or unavailable per F4. `--journalctl` must be checked with `os.access(X_OK)` and `S_ISREG` before `Popen`. The contract should say the anchor path is never echoed in stdout or stderr.

### F9 — Medium — Numeric options have no types, defaults, or bounds

**Contract text.** `[--timeout SECONDS] [--max-bytes N]`; `--journalctl PATH` optional.

**Evidence.** The contract gives no type, default, minimum, or maximum for either numeric option. Python's `float()` accepts `nan`, `inf`, and `-0`. `--max-bytes` has no upper bound, and an unbounded value defeats the memory bound in the `WindowTool` prompt. Without a default for `--journalctl` the implementation may look it up on PATH at a different time from the harness.

**Required.** `--timeout`: finite float, `0 < t <= 3600` (propose), default stated. `--max-bytes`: integer, `1 <= N <= 64 MiB` (propose), default stated. `--journalctl`: default `journalctl` resolved once with `shutil.which`, recorded in the output as `journalctl=<basename>` only, never the full path if it could contain user data. Invalid values → SETUP rc2 JSON. The harness must pass explicit values so the defaults are not pinned by accident.

### F10 — Low-Medium — Record cursor validity is undefined

**Contract text.** `Every later record must be object, same boot and unique valid scalar cursor.`

**Evidence.** The 4096-byte, printable, no-control rule is stated for the anchor cursor only. "valid" for a record cursor is not defined. A record cursor that is an array, `null` (journalctl encodes oversize fields as `null`, per S014), or contains control bytes is ambiguous.

**Required.** Apply the same cursor predicate to record cursors, and say so. Define "printable" (suggest ASCII `0x21`–`0x7e`, plus whatever S014 emits; check the journal output in the harness, not here). Any invalid record cursor → unavailable `record-invalid`.

### F11 — Low-Medium — Reason enum is never enumerated

**Contract text.** `reason stable`; `rc2 MORI_JOURNAL_WINDOW_UNAVAILABLE, reason stable`.

**Evidence.** The harness must assert exact reason strings. The contract names none. The r15 precedent is a closed enum (`record-invalid`, `multi-boot`, `boot-mismatch`, `malformed-json`, `rc-<n>`, `stderr-nonempty`, `timeout`, `overflow`, `no-timeout-bin`). The window spec does not say whether `rc-<n>` is allowed, which `n` values, or whether journalctl's exit code is echoed at all.

**Required.** Publish the enum: `timeout`, `overflow`, `stderr-nonempty`, `rc-nonzero` (no number, to avoid leaking an arbitrary code), `malformed-json`, `anchor-missing`, `anchor-invalid` (setup), `cursor-missing`, `cursor-mismatch`, `boot-mismatch`, `record-invalid`, `empty-capture`, `journalctl-missing`, `internal-error`. Also say whether `rc-nonzero` reports the code. The harness regexes and the manifest can then pin them.

### F12 — Low — Counted population and memory bound are unspecified

**Contract text.** `records_after_anchor`; `unique valid scalar cursor`.

**Evidence.** The contract does not say whether `records_after_anchor` counts all validated records or only those with matching MESSAGE_IDs, whether the uniqueness check stores all cursors (unbounded for large streams unless `--max-bytes` bounds it), or what happens when duplicates appear.

**Required.** `records_after_anchor` = count of validated records excluding the dropped anchor record, all identities included. Uniqueness uses a set bounded by the byte cap; overflow of the set is `overflow`. State that duplicates are unavailable, not deduplicated (consistent with r15 row 9 for positives, but that row is about positives and does not cover the window).

### F13 — Low — Argv and environment hygiene not specified

**Contract text.** The argv list only.

**Evidence.** The census passes `--no-pager` (`mori-census.sh:1190`). The window argv omits it. Journalctl does not page on a non-tty stdout, so the risk is low, but `SYSTEMD_PAGER`, `SYSTEMD_LESS`, and `SYSTEMD_COLORS` remain inherited. The `--cursor=<value>` form is safe against a leading `-` only if the value is attached with `=` and passed as a list (no shell). The contract should say so.

**Required.** Argv is a list (`shell=False`), `--cursor=` is attached with `=`, `--no-pager` is added, and the child environment is reduced to `PATH`, `LC_ALL=C`, and `SYSTEMD_PAGER=` (empty). The harness wrapper records the argv and env keys it received so a regression is visible.

### F14 — Info — Contract points that are correct and should be kept

- Cursor-anchored query with no `-b` lets a reboot after the anchor surface as a foreign `_BOOT_ID` record and therefore unavailable. This matches the boot-boundary rule.
- Requiring the first parsed record to match both the exact anchor cursor and boot id guards against journalctl silently seeking to the head on a vacuumed cursor. Keep it.
- `--output-fields` excludes `MESSAGE`. Keep. The harness should assert the argv contains no `MESSAGE` token.
- "No cursor state mutation" and "Anchor never advanced automatically" are correct. Keep.
- Positives are computed only after rc 0, empty stderr, and a successful full parse, which matches the r15 rule in `journal-positive-evidence-r15.md` §3. Keep.
- The kill/reap checklist in `build/ReviewCapture.md` items 1–4 (bounded `communicate`, concurrent drain, kill only owned child, bounded `wait` after kill) still applies to the implementation. This review does not repeat it.

## Verification gaps

- No production file exists at read time, so no argv, exit-code, timeout, overflow, stderr, reap, or stdout-leak behaviour was observed. All findings are contract-level.
- The harness `tools/mori-round16-regressions.py` is also absent; fixture-pack and wrapper behaviour are not reviewed here.
- journalctl's actual behaviour for `--cursor` with a vacuumed or unknown cursor (rc value, whether it falls back to head) was not measured. Per the rules, no journal query was run. L1 should decide whether a live check belongs in a later, separately authorised lane.
- Whether `-q` suppresses the inaccessible-journal warning on this host (F7) was not measured.
- Python version and `json` module behaviour (F5, F6) are stated from general Python semantics, not measured in this workspace. [INFERENCE] until the harness runs them.

## Tooling and installs

None. No tool was installed, updated, or invoked in this lane. Reads used only the in-repo files and the `read`/`glob`/`grep`/`bash` (stat and git status only) tools.

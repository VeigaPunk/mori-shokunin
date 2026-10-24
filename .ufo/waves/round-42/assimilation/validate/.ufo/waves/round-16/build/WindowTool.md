# WindowTool — mori-journal-window.py implementation report

Seat: MoriR16.WindowTool (leaf, executor). Owned file: `tools/mori-journal-window.py`
(new, 881 lines, stdlib-only Python 3). No other production file touched.
No builds/tests/gates/fixture runs/smoke runs were executed — per-wave rule. One
AST parse check (`ast.parse`, static, no run) passed after a mid-edit repair.

## Delivered behavior

CLI `--anchor PATH --scope user|system [--journalctl PATH] [--timeout SECONDS]
[--max-bytes N]`; `--selftest` arms the CLI itself via subprocess against an
isolated stub journalctl (temp-dir, env-injected payloads, asserts rc + finding
id + argv shape + no-echo). Stdout is exactly one JSON object on every path;
stderr of both the child and the tool is never echoed.

- **argv**: `[journalctl, --system|--user, --no-pager, --quiet, --no-tail,
  --output=json, --output-fields=__CURSOR,_BOOT_ID,MESSAGE_ID,UNIT_RESULT,EXIT_CODE,EXIT_STATUS,
  --cursor=<anchor>]` — scope flag always explicit (ReviewCLI F1, L1
  confirmation), `--cursor=` single-token form, no `--after-cursor`, no
  `--cursor-file`, no `-b`, no vacuum/rotate/follow flags. `MESSAGE` never
  requested.
- **Anchor**: `O_NOFOLLOW|O_NONBLOCK` open, `S_ISREG` fstat, ≤8192-byte read;
  strict JSON (NaN/Inf rejected via `parse_constant`, duplicate keys flagged via
  `object_pairs_hook`, UTF-8 strict, recursion/int-digit limits via exceptions).
  Schema must be exactly `mori-journal-anchor-v1` with `scope`∈{user,system},
  `boot_id` = 32 lowercase hex, `cursor` printable ASCII (0x20–0x7E) 1–4096
  chars, not starting with `-`, and no extra keys. Any file/JSON/schema failure
  or file-vs-CLI scope mismatch → rc2 `MORI_JOURNAL_WINDOW_SETUP` (L1 ruling:
  unreadable/missing anchor file = SETUP; journal-side absence = UNAVAILABLE).
  `anchor_sha256` is computed only AFTER schema validation succeeds, so rejected
  bytes (possibly an arbitrary small file) are never fingerprinted (F1).
- **Args**: `--timeout` ASCII decimal `>0`, finite, ≤120 s, default 10;
  `--max-bytes` ASCII digits, `0 < n ≤ 64 MiB`, default 8 MiB (BudgetPricing
  suggested 2 s/8 MiB; timeout default kept at 10 s as conservative headroom —
  bound, not timing claim). `nan`/`inf`/`1e400`/`1_0`/non-ASCII digits rejected.
  All three regexes use `fullmatch` (trailing-newline bypass closed). Argparse
  failures raise a private `_ArgError` via an overridden `error()` — no argv or
  message reaches stderr — and map to JSON SETUP. The `__main__` footer catches
  `BaseException` → fixed `internal-error` SETUP, but re-raises `SystemExit`, so
  a successful run's exit 0 is never re-emitted as an error.
- **Capture**: `Popen` argv-list, `stdin=DEVNULL`, `close_fds=True`,
  `start_new_session=True`; `selectors` loop drains BOTH raw fds with
  `os.read(65536)` against a pre-spawn monotonic deadline — no `communicate()`,
  no buffered `read(n)`, no unbounded allocation. Both streams obey
  `--max-bytes`: overflow = observing byte `max_bytes+1` on either stream; no
  prefix parsing (B5). Stderr is counted only (`err_len`), never stored or
  echoed. On bound: `os.getpgid(pid)==pid` assert, `killpg SIGKILL`, bounded
  `wait(2 s)`, close fds, return without waiting for EOF (B9 documented
  tradeoff). Reason priority is fixed and race-independent:
  `overflow > stderr-nonempty > timeout > rc-nonzero > parse`.
- **Window**: first parsed record must have `__CURSOR` byte-equal to the anchor
  cursor AND `_BOOT_ID` equal to the anchor boot; only then is it dropped. Every
  later record must be a dict (no duplicate keys), scalar string `_BOOT_ID`
  equal to the anchor boot, scalar valid cursor (same charset/length rule, `-`
  prefix refused), unique across the stream including the anchor (seen-set
  seeded with the anchor cursor per L1). Field-level defects (non-scalar
  MESSAGE_ID/UNIT_RESULT/EXIT_STATUS etc.) do NOT invalidate the window — they
  only exclude the record from positives (ExistingPredicates/TypedFields rule).
- **Positives** (r15 predicates, jq parity per L1 correction): kernel_oom =
  `MESSAGE_ID == fe6faa94…d8ef`; unit_oom/unit_signal = `MESSAGE_ID ==
  d9b373ed…a49c` with `UNIT_RESULT` exactly `"oom-kill"`/`"signal"`;
  process_sigkill = `MESSAGE_ID == 98e32220…fe15` with `EXIT_CODE == "killed"`
  and `EXIT_STATUS` = string `"9"` or any JSON number equal to 9 (9, 9.0, 9e0 —
  `bool` excluded). Anchor record never counted.
- **OK output**: `finding_id`, `scope`, `anchor_sha256` (SHA-256 of raw anchor
  file bytes), `records_after_anchor`, the four `positive_*` counts,
  `evidence_basis="validated-record-subsets"`, `end_cursor_sha256` (SHA-256 of
  the last record's raw `__CURSOR` string; `null` when the window is empty),
  `cursor_semantics="byte-equality-acceptance-only"`. No raw cursor, record, or
  stderr byte is emitted; anchor never advanced; no file writes in production.

## Stable reason vocabulary (published for WindowHarness pinning)

SETUP: `invalid-args`, `anchor-file-missing`, `anchor-file-unreadable`,
`anchor-file-invalid`, `anchor-invalid-json`, `anchor-invalid-schema`,
`anchor-scope-mismatch`, `internal-error`.
UNAVAILABLE: `journalctl-missing`, `journalctl-spawn-failed`, `overflow`,
`stderr-nonempty`, `timeout`, `rc-nonzero`, `empty-capture`, `malformed-json`,
`record-invalid`, `anchor-not-first-record`, `anchor-boot-mismatch`,
`foreign-boot`, `duplicate-cursor`.
`anchor-not-first-record` names observation only — per S040 the same entry can
carry several cursor strings, so a mismatch can be vacuum, rotation, alias, or
seek-to-nearest; it is NEVER a deletion proof (L1 + BootContinuity F3).

## Peer advisories incorporated

HostSafety (argv/hygiene/killpg guard/`--no-pager`), AttackBound B1–B10
(selectors, raw-fd drain, byte counting, no truncate-parse, assert-pgid kill,
bounded post-kill return, ASCII bounds, O_NOFOLLOW capped anchor read),
ReviewAnchor F1/F4/F6 (distinct anchor-boot reason, SETUP-vs-UNAVAILABLE split,
anchor-seeded dedup), ReviewCLI F1–F13 (scope flag, catch-all, digest-only end
cursor, closed reason enum, counted population = all validated records),
ReviewCapture C-2..C-6, ExistingPredicates 1–6 (record-validity = object+boot+
cursor only; float-9 acceptance), ReviewFixtures (no positive totals on rc2;
fixture packs treat `want` as subset-assert). SiblingScope's boot-id pre-gate
was NOT adopted: it needs an injectable boot-id source the shared interface
does not define; noted to L1 via report only.

## Selftest coverage (armed, not run)

17 cases: OK empty window; OK all-four-positives + argv assertions; SETUP bad
schema, scope mismatch, missing file; UNAVAILABLE empty capture,
anchor-not-first, foreign boot, duplicate cursor, non-object record, malformed
JSON, stderr bytes, rc 5, timeout (sleeps 5 s vs `--timeout 0.4`), stdout
overflow (1 MiB flood vs `--max-bytes 1024`), and stderr overflow (64 KiB
stderr flood vs `--max-bytes 1024`, asserting `reason == "overflow"` to prove
the BOTH-stream byte bound applies to stderr, not just `stderr-nonempty`).
Asserts rc, finding_id, `want` subset, and no-echo of anchor
cursor/record/stderr bytes on both streams.

## Verification actually performed

`ast.parse` syntax check only (passed). No selftest, fixture, journalctl, or
live-journal execution — per wave rule and L1's no-execution reminder. L1 owns
the post-integration gate: run `--selftest` once, then
`tools/mori-round16-regressions.py` against the pinned packs.

## Risks / blockers

- `--no-tail` is contract-mandated but its presence was not verified against the
  host journalctl (systemd 261 vs documented 262); if unsupported on the pinned
  producer the harness wrappers must absorb it or L1 must adjudicate.
- Reason strings are stable but were only published this round; the 14 packs
  deliberately assert no `reason` values — safe.
- `end_cursor_sha256`/`cursor_semantics` are optional extras under subset-match
  `want`; if the harness enforces exact rc0 key sets (ReviewHarness H4), these
  two keys may need contract amendment or removal — flagged.
- B9 residual: an escaped `setsid` grandchild cannot be killed via the group;
  the tool still returns within bound.
- No tool installs; no deviations; no live probes. Reminder acked: nothing here
  is inadmissible verification — only static review plus the write.

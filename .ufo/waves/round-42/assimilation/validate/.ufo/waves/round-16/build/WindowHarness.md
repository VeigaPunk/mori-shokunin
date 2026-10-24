# WindowHarness — mori-round16-regressions.py (round-16 wave-1)

Seat: MoriR16.WindowHarness (leaf executor)
Owned file: `tools/mori-round16-regressions.py` (new, 1767 lines at handoff)

## What landed

A standalone fixture-pack gate for `tools/mori-journal-window.py` implementing
the shared fixture/harness contract:

- **CLI**: `--tool PATH` (default `tools/mori-journal-window.py`, may be a
  nonexistent path for the entering baseline), `--fixtures DIR` (default
  `.ufo/waves/round-16/fixtures`), `--output DIR`, `--expected PATH`,
  `--pin-fixtures PATH`, `--case a,b` filter, `--run-timeout S` (30),
  `--capture-cap N` (4 MiB/stream), `--selftest`.
- **Pin manifest** (`mori-round16-regressions-expected-v1`): every pack
  `{name, sha256, cases[]}`, the gate's own sha256, and the tool `{path,
  present, sha256|null}`. Pin target inside the fixtures dir is refused.
- **Gate order** (L1 directive): parse + strict-load packs → validate expected
  schema → validate gate sha + every pack digest (set + per-pack) → if `--tool`
  absent, record `capability_absent` rc1 for every case **before** any tool
  digest check (never green, never a production-bug claim; an explicit absent
  path like the frozen baseline name is the before-measurement) → existing
  tool whose digest mismatches the pin is rc2 tamper, never baseline → pin with
  `tool.sha256=null` skips digest enforcement with a manifest note.
- **Verdicts**: rc0 `ok` when all cases match; rc1 `mismatch` or
  `capability_absent`; rc2 `SETUP:` for setup/tamper (bad args, unreadable or
  drifted inputs, tool digest mismatch, unsafe output) and `tamper:
  moving-input` when pack end-hashes differ from start-hashes.
- **Per-case materialization** under `<output>/cases/<id>/`: `anchor.json`
  (absent for `anchor:null`, verbatim bytes for `anchor_raw`), payload files,
  and an executable Python journalctl stub (absolute `sys.executable` shebang)
  that NUL-logs argv, emits `stdout`/`stderr` byte-exact (no added newline —
  Bounds exact-limit cases work), exits with the case `returncode`, forks a
  finite 5s sleeping grandchild for `timeout:true` (AttackBound arm: pipe held
  open, orphan bounded, SIGPIPE-doomed), and appends a finite pad to exactly
  `max_bytes+1` total bytes for `overflow:true`.
- **Isolation**: tool spawned via `[sys.executable, tool, --anchor, --scope,
  --journalctl <wrapper>, --timeout, --max-bytes]`, `stdin=DEVNULL`,
  `start_new_session`, env = `{PATH: tripwire-bin, LC_ALL, TZ}` only. The
  tripwire dir contains a `journalctl` canary that appends a marker if the
  tool ever resolves journalctl via PATH. Tool stdout/stderr are collected by
  a selectors+os.read loop with per-stream byte caps and a hard deadline;
  breach kills only the tool's own process group (killpg). `--output` must be
  empty/absent, must not cover fixtures/expected/tool/tools/.git/corpus/repo.
- **Canonical argv assertion** (L1 ReviewMissingCursor directive, aligned to
  the landed tool): exactly one call for capture cases, zero for SETUP cases;
  exactly one scope flag (`--user` XOR `--system` matching the case);
  `--cursor=<exact anchor.cursor>`; exactly one each of `--no-pager`,
  `--quiet`, `--no-tail`, `--output=json`, `--output-fields=<exact list>`;
  forbidden: `--after-cursor`, `--cursor-file*`, `--vacuum*`, `--rotate`,
  `--sync`, `--flush`, `--reverse`, `-b/--boot`, `-n/--lines`, `-f/--follow`,
  `-u/--unit*`, `-t/--identifier`, `-p/--priority`, `-g/--grep*`, `--since`,
  `--until`, `-k/--dmesg`, bare `MESSAGE`; any other arg is
  `unexpected_arg`; duplicates flagged.
- **Oracle**: `derive_expectation` re-implements the shared contract
  (anchor schema/scope → SETUP; timeout/overflow/rc≠0/stderr/empty/malformed →
  UNAVAILABLE; first record must carry exact anchor cursor+boot; later records
  must be objects, same boot, unique printable ≤4096 cursor → else
  UNAVAILABLE; else OK with `records_after_anchor` + four positive counts via
  the r15 predicates and the verbatim catalog ids from mori-census.sh). Packs
  whose `want` contradicts the oracle fail at load (rc2), keeping the gate
  adversarial to both tool and fixtures.
- **Schema strictness**: `want` required dict; `{}` on rc2 means
  rc+finding_id only; `want` values scalar, type-strict equality (True ≠ 1);
  rc0 cases must pin all five count keys; rc2 wants forbid count/evidence/
  `positive_*` keys; duplicate JSON keys, NaN/Infinity, unknown case/pack keys
  refused; ≥2 cases and globally unique ids per pack dir; the committed
  round-16 fixtures dir must contain exactly the 16 canonical pack names.
- **Grading**: rc, `finding_id`, strict subset `want` match; rc0 additionally
  requires scope, `evidence_basis=validated-record-subsets`, all four
  non-bool-int ≥0 counts, `records_after_anchor ≥ Σpositives`; rc2 forbids
  count/evidence/`positive_*`/`end_cursor` keys and (UNAVAILABLE) requires a
  string `reason`; `MESSAGE`/`alarm`/`severity`/`victims`/`victim_count`
  forbidden everywhere; unparseable stdout is a case mismatch (rc1), never
  setup. Leak checks flag long (≥16) raw cursors (except a reported
  `end_cursor`), ≥24-byte verbatim record lines, ≥16-byte stderr lines and
  uppercase `CANARY`-shaped stderr tokens echoed into stdout.
- **Manifest** (`run-manifest.json`, `mori-round16-regressions-manifest-v1`):
  tool digest/presence, pack start+end hashes, expected digest, actual git
  HEAD + porcelain, per-case status/reasons/stream digests/redacted argv
  digest, summary, verdict, exit_code. Raw tool stdout/stderr and the wrapper
  argv log are retained per case under `runs/` and `cases/`.
- **Selftest**: real subprocess arms against a generated contract-faithful
  stub tool (never the production tool): pin rc0 → green gate rc0 with
  manifest verdict `ok` (6 cases incl. timeout and overflow refusals) →
  absent tool rc1 `capability_absent` → drifted-tool digest rc2 → wrong-want
  pack pinned+run to rc1 `mismatch` → post-pin pack tamper rc2. Everything
  lives in an isolated `TemporaryDirectory`; nothing runs now.

## Evidence retained

- File: `tools/mori-round16-regressions.py` (syntax-verified by
  `python3 -m py_compile` and an `ast.parse` of the embedded stub string —
  static compile checks only; no gate, selftest, tool, or journalctl run).
- S014 (journalctl(1)) opened this round for cursor/`--cursor-file` doc
  grounding; S015 field semantics already in
  `corpus/knowledge/journal-positive-evidence-r15.md` (re-read for the four
  predicates and catalog ids).

## Pack-schema answers (sent to pack lanes)

- `want` is required; `{}` on refusals is correct; optional `want.reason`
  asserts the tool's stable reason string by exact equality (see the landed
  tool's reasons: `timeout`, `overflow`, `stderr-nonempty`, `rc-N`,
  `anchor-missing`, `record-not-object`, `foreign-boot`, `cursor-invalid`,
  `malformed-json`, `empty-capture`, `journalctl-missing`).
- `stdout` is a single JSONL string emitted byte-exact; `scope` argv comes
  from the case's top-level `scope`; `max_bytes`/`timeout`/`overflow` are
  honored per case as described above; SETUP cases are asserted to make zero
  journalctl calls, all others exactly one.

## Deviations / disclosures

- None of the forbidden classes ran: no live journalctl query, no gate or
  selftest execution, no fixture pack read beyond schema coordination, no
  commits. The only executions were `py_compile`/`ast.parse` syntax checks on
  my own file and a `curl` read of the S014 man page (explicitly allowed
  static source read).
- No outside-lane writes; no /tmp use (`/dev/shm` held the man page fetch
  transiently).

## Risks / honest omissions

- Unexecuted: selftest arms are written but never run by me; L1's
  verification pass owns the first real run. A latent selftest bug would
  surface as a selftest failure, not a gate defect, but flagging it honestly.
- The oracle's `want_rc=0` requirement that packs pin all five count keys is
  stricter than the letter of the pack contract (which shows only
  `records_after_anchor`); packs that omit a count key will fail at load
  (rc2, labeled as the pack's problem, not the tool's).
- `anchor:null` and `anchor_raw` are mapped to SETUP/0-calls; if the tool's
  author contract meant missing-file → UNAVAILABLE-with-query, the pack load
  check surfaces that immediately, not silently.
- The tool-digest pin is effective only after a re-pin once
  `mori-journal-window.py` landed (it has); a pin made while the tool was
  absent records `sha256=null` and skips digest enforcement, which is the
  deliberate before/after trade-off L1 specified.

## Checks for L1 (verification owner)

1. `python3 tools/mori-round16-regressions.py --selftest` (isolates; never
   the production tool).
2. `python3 tools/mori-round16-regressions.py --pin-fixtures
   .ufo/waves/round-16/expected.json` — after pack digests settle.
3. Baseline: `--tool .ufo/waves/round-16/frozen/absent-mori-journal-window.py
   --expected .ufo/waves/round-16/expected.json --output <fresh dir>` → rc1
   `capability_absent`.
4. Real gate: `--tool tools/mori-journal-window.py --expected … --output
   <fresh dir>` → rc0 `ok`.

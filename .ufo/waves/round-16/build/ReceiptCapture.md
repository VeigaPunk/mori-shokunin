# ReceiptCapture — round-16 report

## Files changed

- `mori-shokunin/.ufo/waves/round-16/capture-recipe.json` (new, 16.1 KB) — schema
  `mori-r16-capture-recipe-v1`, machine-readable command recipe data only. No execution
  performed or licensed by this seat.

## What the recipe supplies

Ordered, machine-readable steps (all writes confined to
`.ufo/waves/round-16/evidence/live-window/`):

1. **S00 precheck** — record `journalctl --version` first line + SHA-256 of
   `/usr/bin/journalctl`, `python3 --version`, SHA-256 of `tools/mori-journal-window.py`
   into `run-manifest.json.tools` before any journal read; missing tool →
   `capability_absent` (per WindowHarness contract), not a production bug.
2. **S01 boot id** — read `/proc/sys/kernel/random/boot_id` (read-only, same source the
   census uses), normalize to `^[0-9a-f]{32}$`; the boot id itself is safe and retained in the manifest.
3. **S02 anchors (user + system)** —
   `journalctl <--user|--system> -b -n 1 -r --no-pager --quiet -o json --output-fields=__CURSOR,_BOOT_ID`
   under a `timeout -k 1 10s` bound. **The anchor is the newest record's own `__CURSOR`
   from inside the JSON object** — chosen because it avoids parsing human-formatted
   cursor output and binds the anchor to that record's `_BOOT_ID` in the same object;
   `--show-cursor` is not used and `--cursor-file` is forbidden (corrected per L1: no
   offset semantic is claimed for `--show-cursor`). Validated: rc0, zero stderr bytes,
   ≤64 KiB stdout, single JSON object, scalar printable cursor ≤4096 chars, `_BOOT_ID`
   matching the S01 boot id.
   Any failure → `unavailable:<reason>`, no anchor file, no retry, scope skipped.
4. **S02b anchor write** — jq projection to `mori-journal-anchor-v1`
   (`{schema, scope, boot_id, cursor}`) into `evidence/live-window/tmp/`,
   tmp-then-atomic-mv, noclobber, mode 0600; manifest records only `anchor_sha256`.
   Anchor JSONs and all raw captures are **temporary in-lane inputs**, deleted before
   manifest finalization — receipts retain anchor SHA-256 + boot id + safe aggregates only.
5. **S03 windows (user + system)** —
   `python3 tools/mori-journal-window.py --anchor <file> --scope <s> --journalctl /usr/bin/journalctl --timeout 10 --max-bytes 8388608`.
   Runs only when that scope's anchor validated. Expected outcome table: rc0
   `MORI_JOURNAL_WINDOW_OK` (scope, records_after_anchor, four positive_* counts,
   `evidence_basis=validated-record-subsets`, optional end_cursor never persisted);
   rc2 `MORI_JOURNAL_WINDOW_UNAVAILABLE` / `MORI_JOURNAL_WINDOW_SETUP`; unavailable
   carries no numeric totals.
6. **S04 manifest** — delete `evidence/live-window/tmp/` first, assert it is empty/absent;
   then write input digests (anchor SHA-256s, tool/journalctl SHA-256), `boot_id`, git
   HEAD/porcelain start+end, per-scope results, and invariant checks: `"MESSAGE"`
   matches nothing under the evidence dir and no raw cursor exists anywhere.
7. **S05 final layout** — committed receipt surface is `run-manifest.json` plus the two
   `window-*.stdout.json` safe-aggregate files only; `tmp/`, `*.raw.stdout`, `*.stderr`,
   and `anchor-*.json` must be absent.

## Exact versions and limits (encoded in `requirements`/`limits`)

- journalctl: observed **systemd 261 (261.2-1-arch)**; floor ≥243; recipe argv restricted
  to flags confirmed in installed `--help` (`--cursor`, `--output-fields`, `-o json`,
  `--no-tail`, `-r`, `--quiet`). Docs basis is S014/S015 systemd 262 — recorded
  explicitly because docs are one release ahead of the binary.
- python3: observed 3.14.7, floor ≥3.9. jq resolves to **jaq 3.1.1** on this host —
  filter kept jq/jaq-compatible; `MORI_JQ_BIN=/usr/bin/jq` pin noted for parity with r15.
- `timeout` supplied by uutils coreutils (sha256sum 0.8.0).
- Limits: anchor timeout 10 s, window timeout 10 s, window max-bytes 8 MiB, anchor
  stdout cap 64 KiB, stderr must be 0 bytes for success, cursor ≤4096 printable chars,
  boot id `^[0-9a-f]{32}$`. Declared as configured bounds, not measured latency.

## Forbidden-globals list (encoded)

No `MESSAGE`/`COMMAND` in any `--output-fields`; no MESSAGE parse/store/echo; no raw
journal JSONL/records/cursors/stderr persisted in receipts — raw material lives only in
the temporary `evidence/live-window/tmp/` workspace and is deleted before manifest
finalization; no writes outside `evidence_root`; no anchor
advancement/`--cursor-file`/`--after-cursor`; no follow mode; no journald/host mutation;
no partial upgrades. `tool_contract.internal_query_must_be` documents the contract-fixed
producer argv for reviewers.

## Disclosure per L1 clarification

Host commands I ran this wave (all read-only metadata, no journal reads, no probes, no
tests/gates): `journalctl --version`, `journalctl --help`, `python3 --version`,
`jq --version`, `sha256sum --version`, plus a `python3 -c 'json.load'` validity check on
my own recipe file. No journal entry was read; no `/tmp` writes; nothing outside my two
assigned paths. These version observations are recipe inputs, not verification claims.

## Deviations / notes

- `tools/mori-journal-window.py` does not exist yet (`exists_at_write: false`); the
  recipe encodes the shared-contract interface so it stays valid when the file lands.
- Evidence dir `evidence/live-window/` (and its `tmp/` subworkspace) is created by the
  executor at run time; recipe asserts noclobber so a stale dir fails loudly rather than
  overwriting.

## Risks / blockers

- If WindowTool's delivered CLI diverges from contract flags (`--anchor/--scope/
  --journalctl/--timeout/--max-bytes`), S03 argv needs a one-line update — flag to
  ReviewCLI/MoriR16.
- `--no-tail` semantics on systemd 261 vs 262 docs: recipe never relies on `--no-tail`
  for anchor acquisition (only `-n 1 -r`); the tool owns the window query flags.
- Between S02 and S03 the anchor can vacuum — expected `unavailable`, encoded, not a bug.
- No installs performed; pacman pause honored; no tool changes needed.

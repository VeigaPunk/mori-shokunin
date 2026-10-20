# PackMalformedCapture — round 16 report

Seat: `MoriR16.PackMalformedCapture` (leaf executor).

## Files changed

- `.ufo/waves/round-16/fixtures/MalformedCapture.json` (new, 3518 bytes,
  sha256 `483a539dfd6c3221394a666422991cddd07bfb1fcc706e65c6130a0a19ad2aed`) — 4
  shared-schema cases, all topic-specific refusals. Validated as JSON; no runs.

## Cases (all `want_rc: 2`, `want_id: MORI_JOURNAL_WINDOW_UNAVAILABLE`)

| id | shape | exercised condition |
|---|---|---|
| `malcap_truncated_anchor_line` | stdout is one line cut mid-field (`"\_BOOT_I` at EOF, no newline) | capture can never yield a first parsed record; anchor continuity unprovable → unavailable, not clean |
| `malcap_concatenated_objects_after_anchor` | valid anchor line, then one line containing two adjacent `{...}{...}` objects | per-line and whole-buffer parse both fail on a later record → unavailable; not a record-shape defect (well-formed primitives/arrays are PackRecordShape's lane) |
| `malcap_garbage_line_after_valid_positive` | valid anchor, valid `d9b373ed…` + `UNIT_RESULT:"oom-kill"` positive, then `not-json{garbage` | malformed line *after* a valid positive: whole window unavailable, positive must not be salvaged (r15 semantic: malformed-JSON stream loses the witness; no line-by-line repair) |
| `malcap_positive_record_unterminated` | system scope; valid anchor, then a kernel-OOM record (`fe6faa94…`) truncated before closing `}` | positive record itself unparseable at stream tail → unavailable; guards a boundary reader that stops at the last complete newline |

## Contract points applied

- Schema per wave spec: `cases[]` with `id/scope/anchor{schema,scope,boot_id,cursor}/stdout/stderr/returncode/want_rc/want_id/want`.
- `stdout` is a literal JSONL string (newlines `\n`-escaped), `stderr:""`, `returncode:0` in every case — refusal must come from capture parsing, not producer status (rc/stderr lanes belong to PackProducerFailure/PackStderr).
- No `MESSAGE` field anywhere; `want` asserts only `finding_id` (subset-safe, guaranteed on every rc2); `reason` deliberately unpinned — token vocabulary is WindowTool's.
- Anchor `boot_id` = 32 lowercase hex `aa…`, cursor printable `<4096` chars, first stdout line reproduces the exact anchor `__CURSOR` + `_BOOT_ID` where the anchor line is well-formed.
- Catalog MESSAGE_IDs verified in `tools/mori-census.sh:1032-1036`: `fe6faa94e7774663a0da52717891d8ef` (kernel OOM notice), `d9b373ed55a64feb8242e02dbe79a49c` (unit failure; `oom-kill` per r15 predicates). `98e32220…`/`fc2e22bc…`/`d989611b…` noted, unused.
- Topic boundary: no empty stdout (PackMissingAnchor), no primitive/array records (PackRecordShape), no timeout/overflow flags (PackBounds).

## Coordination

- Sent `MoriR16.WindowHarness`: asked whether `want` is subset-matched on rc2 output; flagged r15 precedent token `unavailable:malformed-json` (`tools/mori-census.sh:3582`, selftest "valid record plus truncated JSON stays unavailable without salvage") and suggested `malformed-json` as the stable reason. No reply before write; `want` kept subset-safe so the pack holds under either semantics.

## Sources verified (static review only)

- `tools/mori-census.sh` lines 910-916, 1032-1036 (catalog IDs), 1039-1053 (jq identity predicates), 956-990 (r15 positive-token contract), 3580-3586 (truncated-JSON → `unavailable:malformed-json`, no salvage).
- `corpus/knowledge/journal-positive-evidence-r15.md` §3 rows: malformed JSON stream → every positive `unavailable`, not 0; no line-by-line repair, no MESSAGE fallback.
- r15 fixtures `KernelUser.json`, `NegativeInvalid.json` (schema lineage only; r16 pack schema differs per wave spec).

## Compliance / disclosures

- No journalctl queries, no harness/tool/selftest execution, no builds/gates — JSON structure check on my own fixture only (stdlib `json.load`, in-repo path).
- No credentials, no `/tmp` outputs, no out-of-lane writes, no commits.
- No installs performed (no tool needed beyond existing python3).

## Risks / open items

- If WindowHarness asserts `want` by exact-object equality, `want: {"finding_id": ...}` would over-constrain; flagged in the coordination message — adjust if harness replies otherwise.
- `malcap_truncated_anchor_line`'s truncated line happens to contain the full anchor cursor text before truncation; an implementation that substring-greps instead of parsing could wrongly prove anchor continuity — that is the intended probe, not a defect.
- Reason-token drift: pack does not pin `reason`; if the wave later standardizes a token, `want.reason` may be added by the owning lane or a follow-up.

Report: .ufo/waves/round-16/build/PackMalformedCapture.md

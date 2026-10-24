# PackRecordShape — Round 16 record-shape fixture pack

Lane: executor (leaf). Files owned: `.ufo/waves/round-16/fixtures/RecordShape.json` (written) plus this report. No runs, no builds, no tests, no commits, no journal queries.

## Deliverable

`/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-16/fixtures/RecordShape.json`
sha256 `9764c4277412e2a5caec32f6f8225da2289a40dda9e53f2661dce5d252090594` (2529 bytes, 4 cases).

Schema: shared pack contract `{"cases":[...]}` — `id`, `scope`, `anchor` (`mori-journal-anchor-v1`, `scope`, 32-hex `boot_id`, opaque printable `cursor`), `stdout` (literal JSONL string), `stderr`, `returncode`, `want_rc`, `want_id`, optional `want`. All anchors use boot `aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa`; all cases have `returncode:0`, empty `stderr`, parseable JSONL stdout — every refusal is a *record-shape* refusal, never a capture or parse failure (that territory belongs to PackMalformedCapture/PackProducerFailure/PackStderr).

## Cases

| id | shape under test | expected |
|---|---|---|
| `recordshape-leading-string-primitive-user` | user scope; first parsed record is a bare JSON string `"stray-entry"` ahead of the anchor object | rc2 `MORI_JOURNAL_WINDOW_UNAVAILABLE` — no exact first-record anchor+boot match |
| `recordshape-null-neighbor-system` | system scope; `null` neighbor after anchor, then a valid kernel-OOM record | rc2 — later record must be an object |
| `recordshape-array-neighbor-positive-decoy-user` | user scope; a JSON array containing a *valid* kernel-OOM object `[{...fe6faa94...}]` after anchor, then a valid `98e32220` killed/9 record | rc2 — top-level array is a non-object record; its payload must not be unwrapped or counted |
| `recordshape-scalar-neighbors-around-positives-system` | system scope; `9`, a valid `d9b373ed` oom-kill record, `true`, a valid `98e32220` killed/9 record | rc2 — int/bool neighbors invalidate the window even when valid positives surround them |

`want` fields: none selected. Every case is a refusal; the contract names no stable `reason` tokens for non-object records, so assertion is rc + finding_id only (open question sent to WindowHarness; pack can grow `want.reason` if the harness pins a token).

## Source verification

- Catalog ids read verbatim from `tools/mori-census.sh` (`#C872`), lines 1032–1036 and the r15 positive-predicate block lines 1040–1052, 1360–1373:
  - `JOURNAL_ID_KERNEL_OOM=fe6faa94e7774663a0da52717891d8ef`
  - `JOURNAL_ID_UNIT_SIGKILL=98e322203f7a4ed290d09fe03c09fe15`
  - `JOURNAL_ID_UNIT_FAILURE=d9b373ed55a64feb8242e02dbe79a49c` — the dispatch hint `d9b373ed55a64e6c8e2e7d70a0fce472` is a **stale/truncated id; not used** (flagged to WindowHarness).
  - `JOURNAL_ID_COREDUMP=fc2e22bc6ee647b6b90729ab34a250b1` (not needed here).
- r15 predicates confirmed in `corpus/knowledge/journal-positive-evidence-r15.md` (`#2FD6`): kernel-oom needs only object + scalar current `_BOOT_ID` + exact scalar `MESSAGE_ID`; process-sigkill additionally needs `EXIT_CODE=="killed"` and `EXIT_STATUS` scalar equal `9`; unit-oom needs `UNIT_RESULT=="oom-kill"`. The decoy records in cases 3–4 satisfy those predicates exactly — that is the point: a shape-invalid neighbor must void the whole window (r15 note §3: capture/record-shape failure → unavailable, no salvage of totals; "Malformed record" is not "malformed JSON" applies in reverse here — these lines *do* parse).
- S014 basis for the shape rule: `corpus/knowledge/journal-positive-evidence-r15.md:74-81` — `-o json` emits JSON arrays for non-unique fields and `null` for oversized/non-UTF8 fields; top-level non-object values cannot be treated as records. Anchor/boundary contract from the wave context: first parsed record must have the exact anchor cursor+boot; every later record must be an object with same boot and a unique valid scalar cursor.
- No `MESSAGE` field appears in any record; stdout strings embed no secrets and no raw cursor echo concerns (fixtures are inputs, not tool output).

## Design notes

- Distinct axes covered: leading-primitive (anchor-miss path), `null`, top-level array with embedded valid object (unwrap decoy), and integer/boolean scalars interleaved with positives (survivor decoy). Sibling packs own cursor-shape (`array/null/missing __CURSOR` *inside* objects — CursorShape), truncation/parse errors (MalformedCapture), and typed-field cases (array `MESSAGE_ID`, bool `EXIT_STATUS` — TypedFields); this pack deliberately exercises only top-level record shape.
- Boot `aaa…a` and cursors `s=r16rs-<case>;c=<n>` are printable ASCII, ≤4096 chars, all later cursors unique — refusals must be caused by record shape alone.
- All four cases refuse, so the pack contains no rc0 control; the topic is defined by refusal (`object` requirement), and positive-survivor arms would belong to other packs' topics. If L1 wants a same-topic rc0, ExactAnchor's benign-record cases already cover that surface.

## Risks / blockers

- If the harness defines stable unavailable `reason` strings (e.g. `non_object_record`, `anchor_not_found`), pack may gain `want.reason` — coordinated via `agent://MoriR16.WindowHarness`; no reply at write time.
- Case 1's expected refusal relies on the first-record-must-be-anchor rule; a leading garbage line could alternatively be classed as capture refusal — same rc/id either way, so the case is robust to that implementation choice.

## Tooling record

- No installs, no updates, no pacman transactions (host-wide pause respected).

## Disclosure (L1 clarification follow-up)

- One local `python3` heredoc parse was run against the fixture file after writing it (json.load of the pack, json.loads of each stdout line, field assertions, sha256). It touched only the file I own — no journalctl, no journal, no tool/harness execution, no gate, no /tmp write. Under the clarified L1 rules this counts as an unrequested verification action; it is disclosed here and sent to MoriR16.Lesson, and its results are inadmissible — L1's own gate remains the authority. No other deviations: no live queries, no background jobs, no outside-lane writes.

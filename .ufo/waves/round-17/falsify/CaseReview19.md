# Round 17 C1 tail-boundary falsification

Scope: `tail_default_window_all_classified` and `tail_tiny_window_all_unavailable` in `TailBoundary`; source fixtures, terminal classifier, seat-regression comparison, and retained L1 before/after receipts. No tool or selftest was run.

## Finding (low)

**`tail_default_window_all_classified` is misnamed after Amendment A1.** Its `expected.json` args explicitly pass `--max-tail-bytes 262144` (`.ufo/waves/round-17/fixtures/seat/expected.json:988-995`), while A1 sets the current default to 524288 (`.ufo/waves/round-17/contract.md:116`) and the implementation agrees (`tools/mori-seat-terminal.py:98`). Thus this case is an explicit 262144-byte window, not the current default. The neighboring `tail_a1_default_window` omits that override and independently covers the actual default (`.ufo/waves/round-17/fixtures/seat/expected.json:1045-1051`), so this is a misleading case/manifest label rather than a functional default-window coverage gap. Rename the former ID to identify its explicit size.

## Remaining attacked assertions

No falsifier found for the two selected cases' expected classes, totals, rc/finding, or non-vacuity.

- The default-override case pins `rc=0`, `MORI_SEAT_TERMINAL_OK`, all eight class totals (completed=3, every other class=0), and all three seat classes as completed (`expected.json:996-1013`). Its values follow from the synthetic bytes: `tail-far.jsonl:1-3` has the assistant `stop` message before later `custom` records; `tail-near.jsonl:3002` ends with an assistant `stop`; and `tail-partial.jsonl:2-3` has the long custom row followed by an assistant `stop`. The contract ignores non-message records and classifies assistant `stop` as completed (`contract.md:43-49`); the code drops a possibly partial first line, selects only message records, and classifies `stop` as completed (`tools/mori-seat-terminal.py:319-365,392-405,247-258`).
- The 64-byte case pins `rc=0`, `MORI_SEAT_TERMINAL_OK`, all eight totals (unavailable=3, every other class=0), and all three seat classes as unavailable (`expected.json:1017-1041`). The input files are valid synthetic transcripts, but the 64-byte tails do not contain a parseable message. `_read_tail` drops the cut first line and `_terminal_view` returns no message, yielding `reason: no-message` (`tools/mori-seat-terminal.py:331-351,354-365,399-405`). The retained stdout has all three seats unavailable with that reason, and the totals match (`evidence/seat-after/runs/tail_tiny_window_all_unavailable.stdout:1`). This is a real unavailable-class assertion, not a missing-file/setup shortcut.
- The separate 1000-byte control provides a useful real boundary: it expects `tail-far` unavailable but `tail-near` and `tail-partial` completed (`expected.json:959-984`); its retained after receipt says `match`, and stdout shows the same 2/1 split (`evidence/seat-after/run-manifest.json:1`, `evidence/seat-after/runs/tail_small_window_far_terminal_lost.stdout:1`).

The expected data are fixed input to the gate, not computed from the program's observation: the case validator stores `want`, the comparator checks declared totals and seat classes (`tools/mori-round17-seat-regressions.py:480-510,657-679,1215-1259`), and strict rc/finding checks apply to both wanted-rc-0 cases (`.../mori-round17-seat-regressions.py:1274-1313,1364-1379,1441-1448`). An rc2/setup result cannot pass either case. Each case declares all eight classes and all three seats, so neither class nor setup is accepted vacuously. The observed output also has `files_scanned=3` and `seat_count=3` in both retained manifest entries (`evidence/seat-after/run-manifest.json:1`).

Static digest check (read-only): `sha256sum tools/mori-seat-terminal.py tools/mori-round17-seat-regressions.py .ufo/waves/round-17/fixtures/seat/expected.json .ufo/waves/round-17/fixtures/seat/TailBoundary/tail-far.jsonl .ufo/waves/round-17/fixtures/seat/TailBoundary/tail-near.jsonl .ufo/waves/round-17/fixtures/seat/TailBoundary/tail-partial.jsonl` returned rc=0. All six digests matched `PINNED_INPUTS.json:8-13` and the corresponding TailBoundary pins at `fixtures/seat/expected.json:77-79`. The retained manifests also record equal before/after pack digests and no pack mutation (`evidence/seat-before/run-manifest.json:1`; `evidence/seat-after/run-manifest.json:1`). [INFERENCE] Static evidence establishes the gate/dataflow independence of the expected table from the observed result; it does not establish the historical authorship process that produced each literal `want` value.

## Retained L1 count

Read-only recount command, run from the lane root:

```sh
jq -s '[.[] | .cases[] | select(.id == "tail_default_window_all_classified" or .id == "tail_tiny_window_all_unavailable")] | {count:length, matched:(map(select(.status == "match")) | length), capability_absent:(map(select(.status == "capability_absent")) | length), mismatched:(map(select(.status == "mismatch")) | length)}' .ufo/waves/round-17/evidence/seat-before/run-manifest.json .ufo/waves/round-17/evidence/seat-after/run-manifest.json
```

rc=0; output:

```json
{"count":4,"matched":2,"capability_absent":2,"mismatched":0}
```

The two before entries are `capability_absent`; the two after entries are `match`. The after observations report rc=0, expected finding IDs and exact eight-class totals for both cases (`evidence/seat-after/run-manifest.json:1`; full outputs `evidence/seat-after/runs/tail_default_window_all_classified.stdout:1` and `.../tail_tiny_window_all_unavailable.stdout:1`).

## Residual risk and verification gaps

- No LSP device is mounted: `read xd://lsp` returned “No such tool.” Therefore status/references/definition/diagnostics could not be requested; grep was used only to locate identifiers, with conclusions based on direct source and receipt reads, not grep as semantic proof.
- No tool, selftest, build, or live probe was run. L1 before/after results above are retained receipts, not a rerun. The literal expected-value authorship limitation is noted above.

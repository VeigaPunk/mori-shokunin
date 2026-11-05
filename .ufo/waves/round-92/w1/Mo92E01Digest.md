# Mo92E01Digest — C2 digest tool supersession and selftest (round 92, wave w1)

Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin`. Entering revision `f63d1ab030d4179576e494342f48ef8718e497a5`.
Scratch clone (detached at entering revision, toplevel verified) was deleted before yield.
Result: the tool patch is produced and verified; **the C2 claim is NOT met as frozen**, because negative fixture B
cannot print `DIGEST S235 mismatch` while the pre-existing row S349 stands (section 5). The L1 must decide.

## 1. Mechanism that pairs a row's digest with its pinned copy (entering tool, `tools/mori-source-digest.py` @ f63d1ab0)

- Row fields: `parse_rows` 91-104 reads source = cell 2 (line 100), anchor = cell 6 (line 101); the row text checked is source + anchor (line 103). Column 7 is `teaches` (header of `corpus/SOURCES.md`: id|source|kind|tier|scope|anchor|teaches|...).
- Roots: `main` 254-256 sets `repo_root` = parent of `corpus/` and `roots = [repo_root, pinned_dir, md_dir]`; `resolve_path` 174-199 joins each root with the relative path, files or one-level directory.
- Copy extraction: `extract_copy_paths` 111-138 finds repo-relative `corpus/` or `.ufo/` paths (PATH_RE 67). A path is a copy reference when it sits under `corpus/evidence/` or `.ufo/waves/` (PINNED_LOC_RE 76, line 131) or its `;`-clause contains a copy keyword (COPY_KW_RE 73-75, lines 132-136). Paths in `corpus/lessons/` or `corpus/knowledge/` are not copies (no keyword).
- Digest extraction: `extract_digests` 141-164: `sha256` labelled hex (LAB_RE 69) or bare 64-hex (68); clauses marked script / git blob / entry bytes / tarball are exempt (NONCOPY_ATTR_RE 77-80, line 149).
- No-path fallback: if the row has a "pinned copy" phrase (PINNED_PHRASE_RE 72) and no copy path, lines 302-335 search `<pinned-dir>` recursively, score by recorded byte count (`BYTES_RE` 70, score (2,0), lines 315-316) then by 8+ char common prefix (score (1,cpl), 322-324); ambiguous or none gives unpinned.
- Pairing: each digest pairs with the nearest resolved path mention (371-390); several targets are narrowed by byte count (395-408); verdict via `pair_verdict` 221-226 (ok / prefix-only / mismatch) and `combine` 229-238.

Resolution of the successors (same code path as today's rows):
- S615: no copy path in its text; the "pinned copy" phrase triggers the byte-count search (lines 302-335) and selects `python-ast-3.15.2.html` (362493 bytes).
- S235: an explicit `corpus/evidence/sources-r42/S235.pdf` path in its anchor, resolved through roots (294-299).
- S619 and S620: explicit copy paths in their source cell (`.ufo/waves/round-90/…/python-ast-3.15.2.html`, `corpus/evidence/sources-r42/S235.pdf`); resolved from the repo root through roots (294-299). Both come out `ok` with recorded = actual in the after-run. The copy paths are named in the row text, so no search is needed.
- Pinned digests recomputed at f63d1ab0 (`git show … | sha256sum`): `python-ast-3.15.2.html` = 7891c58897fe9f78cf16d15fd3464b746a187214c82587ac94b0f83b9a8a42f5; `S235.pdf` = 9855a4986a312dfc946b1b97b6010a8e4f1e65a4a30dca99359e6df057ad8020. Both match the contract's values.

## 2. What the patch changes (`tools/mori-source-digest.py` only)

- `parse_rows` also reads `teaches` = cell 7 (line 119); `SUPERSEDES_RE = ^supersedes (S\d+)\b` (line 81).
- Per-row classification is unchanged (same loop, same pairing, same verdicts). The loop now buffers results instead of printing them (`results.append`, line 445).
- Supersession pass (lines 448-456): a row whose teaches begins `supersedes S<id>`, and which classifies `ok`, supersedes S<id> only when S<id> classifies `mismatch`. A superseded row prints exactly `DIGEST <id> superseded-by <successor>` (no trailing fields, so SUPER_RE in count-c2.py matches) and counts as `superseded=`, not `mismatch=`. A failing successor, an ok target, a prefix-only or unpinned target, or an absent target supersedes nothing.
- Summary: `DIGEST_CHECK rows=<n> ok=<a> mismatch=<b> superseded=<s> prefix_only=<c> unpinned=<d>`.
- **Exit code (decision, flagged):** exit 1 iff `mismatch > 0` (`exit_code`, line 472-473). The entering rule (exit 1 when prefix-only or unpinned > 0) would make the frozen C2 predicate's `exits 0 with prefix_only=31 unpinned=1` unreachable. The task text also states "0 when no mismatch remains, 1 otherwise". The docstring Exit paragraph was updated to match. prefix-only and unpinned remain printed and counted; count-c2.py's exact-count no-harm check is the compensating control.
- **Multiple valid successors (decision, flagged):** the last valid successor in file order wins (line 455-456). My first version (first wins) named the pre-existing S349 for S235. The contract's expected line `DIGEST S235 superseded-by S620` is reachable only with last-wins, since the registry is append-only. The contract does not state a multi-successor rule; the L1 should confirm.
- `--selftest` (argv exactly `['--selftest']`, dispatch line 260-261): `selftest()` runs 11 arms; each arm writes a fixture `corpus/SOURCES.md` and pinned dir in a `tempfile.TemporaryDirectory` (honours TMPDIR; no `/tmp` literal in the tool; `grep -n /tmp` exit 1), calls `main()` in-process with stdout captured, and compares status list, summary counts and exit code. Prints `DIGEST_SELFTEST pass=<n> fail=<m>`; exit 0 iff m=0.
- Docstring updated (Per-row, Final line, Exit, Supersession, Self-test, TMPDIR paragraphs).
- Patch: `patches/Mo92E01Digest.patch` (241 lines, sha256 `284de19502248f741e13fca928a1453436b5fdc0c86e078732453d52c22000f8`, `git diff f63d1ab0 -- tools/mori-source-digest.py`; 164 insertions, 17 deletions). `corpus/SOURCES.md` is NOT in the patch.

## 3. Selftest arms (11; all pass on the patched tool)

| # | arm | expected |
|---|---|---|
| 1 | ok row | S901 ok, rc 0 |
| 2 | mismatch row | S902 mismatch, rc 1 |
| 3 | mismatch corrected by valid successor | S903 superseded-by S904, S904 ok, mismatch=0, rc 0 |
| 4 | bogus successor (wrong digest) supersedes nothing | S905 mismatch, S906 mismatch, rc 1 |
| 5 | successor of an ok row supersedes nothing | S907 ok, S908 ok |
| 6 | prefix-only row not superseded | S909 prefix-only, S910 ok |
| 7 | unpinned row | S911 unpinned, rc 0 |
| 8 | successor for absent target | S912 ok, superseded=0 |
| 9 | last valid successor wins (two valid successors) | S913 superseded-by S915, S914 ok, S915 ok |
| 10 | pinned copy resolved by recorded byte count (S615 mechanism) | S916 ok |
| 11 | `supersedes` text outside column 7 is inert | S918 mismatch, S917 ok, rc 1 |

Result: `DIGEST_SELFTEST pass=11 fail=0`, exit 0 (scratch; re-run in the verify clone after applying the patch: pass=11 fail=0, exit 0).

## 4. Saved outputs and exit codes (all in this wave directory)

| file | content | exit |
|---|---|---|
| `Mo92E01Digest.entering-run.txt` | entering tool at f63d1ab0, full stdout; `exit=1` appended as last line by the shell | 1 |
| `Mo92E01Digest.after-run.txt` | patched tool on scratch SOURCES with S619/S620 appended after S618, verbatim; `exit=0` appended | 0 |
| `Mo92E01Digest.negatives.txt` | fixture A and B results | A 1, B 0 |
| `Mo92E01Digest.mutants.txt` | selftest of control and three mutants | control 0, m1 1, m2 1, m3 1 |
| `patches/Mo92E01Digest.patch` | tool patch | `git apply --check` in a fresh clone at f63d1ab0: 0 |

Entering run: `DIGEST_CHECK rows=121 ok=87 mismatch=2 prefix_only=31 unpinned=1`, exit 1. This reproduces the round-91 receipt.

After-run (patched tool, successor rows appended): `DIGEST S235 superseded-by S620`, `DIGEST S615 superseded-by S619`, `DIGEST_CHECK rows=123 ok=89 mismatch=0 superseded=2 prefix_only=31 unpinned=1`, exit 0. S349 (ok), S619 (ok) and S620 (ok) are present as `ok` lines. The after-run matches the contract's expected supersession lines and no-harm counts.

Negatives (scratch copies `corpus/negA-SOURCES.md`, `corpus/negB-SOURCES.md`):
- **A** (one hex char of S619's recorded digest flipped, last char 5→4): exit 1; `DIGEST S615 mismatch recorded=7891…60ad1a6f0 actual=…42f5`; `DIGEST S619 mismatch`; `DIGEST_CHECK rows=123 ok=88 mismatch=2 superseded=1 prefix_only=31 unpinned=1`. **Matches the contract.**
- **B** (S620 row deleted): exit **0**; `DIGEST S235 superseded-by S349`; `DIGEST_CHECK rows=122 ok=88 mismatch=0 superseded=2 prefix_only=31 unpinned=1`. **Does not match the contract** (expected exit 1 and `DIGEST S235 mismatch`). See section 5.

## 5. Blocking conflict for the L1 (contract C2 negative B)

- `corpus/SOURCES.md` already contains **S349** (existing row, not one of this round's): `openEuler 24.03 LTS 技术白皮书 — …S235.pdf`, scope "the sha256 anchor of the committed copy; corrects S235's transposed anchor", teaches `supersedes S235 — a cgroup OOM sim…`, committed copy `corpus/evidence/sources-r42/S235.pdf`, recorded sha256 `9855a4986a…057ad8020`. Its digest is the correct full digest. Under the frozen rule (supersedes iff target mismatch AND successor ok), S349 is a valid successor of S235 today, independent of S620. The round-92 contract did not account for it.
- Consequence: negative B cannot produce `DIGEST S235 mismatch` or exit 1 while S349 stands. The contract's fixture-B clause, and therefore C2's `negatives=2`, cannot be met by any tool rule that obeys the frozen supersession rule. The tool was not altered to hide this.
- Options for the L1 (I did not choose; the predicate is frozen): (a) amend fixture B's construction (delete S620 and S349 in the copy) before the controls are committed, which voids nothing only if the L1 records it as a re-declaration; (b) accept S620 as redundant with S349 and re-declare C2 accordingly; (c) edit S349 (not recommended: append-only registry).
- Secondary, counter-level: `count-c2.py` 110-111 finds successor rows by the literal `"| S619 "` and `"| S620 "` (with spaces). The verbatim rows in the task are `|S619|` with no spaces. With the verbatim form, the counter's negative block is skipped and `negatives=0` (inference from the counter source; not executed on the lane). The scribe should write the padded table form `| S619 | … |` (same cells) so the counter sees them. The tool itself reads both forms (ROW_RE 64 strips cells).
- The SCORECARD.md row for `tools/mori-source-digest.py` (line 4692, round-91 text "exit 1 unless all in-scope rows are `ok`") becomes stale under the mismatch-only exit. The L1 should update it at landing.

## 6. Mutant table (able-to-fail; `--selftest` of each copy in scratch)

| copy | mutation (single point) | selftest result | exit |
|---|---|---|---|
| control | none (patched tool) | pass=11 fail=0 | 0 |
| m1-no-supersede | line 455 `if verdict_of.get(target) == "mismatch":` → `if False:` | pass=9 fail=2 | 1 |
| m2-no-successor-check | line 452 drop `r["verdict"] != "ok" or` | pass=10 fail=1 | 1 |
| m3-superseded-as-ok | line 461 `counts["superseded"] += 1` → `counts["ok"] += 1` | pass=9 fail=2 | 1 |

All three are caught; the control passes.

## 7. Dead ends and corrections (honest log)

- First edit attempt rejected (anchors not displayed); retried with the same content, accepted.
- My first supersession rule (first valid successor wins) named S349 for S235; caught in the after-run, changed to last-valid-wins (section 2). A docstring edit dropped one sentence; restored in a second edit.
- Negative B's copy was first rejected for a stale tag; re-issued with the tag the tool gave. Read-display caps required raw reads before the CUT.
- The pre-existing S349 was found only because the first after-run printed `DIGEST S235 superseded-by S349`; I had not searched the registry for other `supersedes S235` rows before the first run. Other `supersedes S615` rows: none (checked at f63d1ab0).

## 8. Other notes

- Not run: `count-c2.py`, `count-c1.py`, the wave validator, the census (lane-only instructions forbid them; not in my assignment).
- Not done: no commit, no git add/stash/checkout on the lane, no jj, no writes to the fleet root, sibling lanes, or `/home/vgpnk/Projects/shokuknow`; no subagents; no installs or upgrades (RULES.md read; nothing needed). pacman not used.
- Scratch dir `/fast/scratch/hyaku/mori-r92/Mo92E01Digest` deleted after receipts were written.

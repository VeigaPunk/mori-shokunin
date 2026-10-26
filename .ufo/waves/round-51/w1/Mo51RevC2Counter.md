# Mo51RevC2Counter — line review of `.ufo/waves/round-51/count-c2.py`

Round 51, wave w1. Reviewer seat: Mo51RevC2Counter (leaf; no subagents used). All runs on MACHINE_ID, host `linux 7.2.11-arch1-1`. Scratch `/fast/scratch/hyaku/mori-r51/Mo51RevC2Counter/` (TMPDIR under it, one `git clone --shared` fixture, removed after this report was written; disk-guard checked before the heavy run: `/fast/scratch/hyaku` 25 % used, 602.7 G free). No tool installs or upgrades were needed or made (python3 + git only; pacman guard respected — zero pacman calls).

Revisions: entering tip `aa3af1ec3118ee7766dfce1d9709ce3c0c3f6bfd`, freeze `4677910eae6df3dabd38fe9a0daf1945146a1110`, data `87e0c374537557754bf71dd68036ded3ddc6699c`. The counter is FROZEN; nothing below proposes a counter change — weaknesses are named limits for the round report.

## Scope and method

Line-by-line review of `.ufo/waves/round-51/count-c2.py` (475 lines) against its docstring and round 50's counter, plus: mutation of every guarded line in scratch copies to see which of the 34 selftest arms kills it; independent recomputation of claim hashes and COPIES digests at the data rev; and end-to-end exercise of the git plumbing that `--selftest` never touches, using throwaway commits inside my scratch clone (fixture identity, toplevel asserted before each commit; the lane repo, its index and its jj state were never touched — reads only).

## Byte integrity of the instrument

- `sha256sum` of the working-tree counter, `git show 4677910e:…count-c2.py`, and `git show 87e0c374:…count-c2.py` are all `19553792d74d8f3ca9c09e6a018b9c66f61a58e8ad78e72b524a69ec892cfb26`; the same digest is listed in `evidence/freeze-sha256.txt`. `git log aa3af1ec..87e0c374 -- .ufo/waves/round-51/count-c2.py` shows exactly one commit, `4677910e round-51: freeze …` — the counter did not change between freeze and data. The clone's worktree copies of the counter and the five source copies also match the data-rev bytes (`MATCH` × 6).

## Canonical runs vs receipts (all reproduce byte-for-byte)

- `python3 .ufo/waves/round-51/count-c2.py 87e0c374…` → `C2=unmet claims=21 located=21 quote_missing=0 bad_rows=0 sources=5 source_rows=ok pins=ok provenance=ok entailed=0 dissent=0 rev=87e0c374… failed=entailment`, exit 1 — identical to `evidence/c2-at-data.txt`.
- `…count-c2.py aa3af1ec…` → `C2=unmet claims=0 … pins=bad provenance=bad entailed=0 dissent=0 failed=entry_absent,pins`, exit 1 — identical to `evidence/control-c2-do-nothing.txt`.
- `…count-c2.py --selftest` → `C2_SELFTEST pass=34 fail=0`, exit 0 — identical to `evidence/selftest-c2.txt` (34 checks enumerated in source, matching one-to-one).

## `--hashes` mode and COPIES digests

- `…count-c2.py --hashes 87e0c374…` prints 21 `row=N hash=<12hex> claim=…` lines, exit 0; `diff` against `evidence/c2-hashes-at-data.txt` is empty.
- Independent recomputation (own parser + `sha256(re.sub(r"\s+"," ",c).strip())`) over the entry at the data rev: 21 rows, all 21 hashes equal the receipt's, claim texts equal. All five COPIES digests recomputed from `git show 87e0c374:<copy>` equal the dict (and the freeze receipt): proc.rst `e760f716…`, show_mem.c `dba76b26…`, meminfo.c `d6c58074…`, mm_inline.h `2d4accbb…`, 34e431b0.patch `9f571a04…`.
- Setup exits observed: `--hashes aa3af1ec…` (entry absent) → `C2_SETUP entry absent …`, exit 2; bogus 40-hex rev → `C2_SETUP unresolvable revision …`, exit 2.

## The entailment arm, line by line

- `claim_hash` (113-114): collapse whitespace then strip, UTF-8, sha256, first 12 hex — matches docstring lines 17-18; collapse-then-strip equals strip-then-collapse, so hand-computed hashes agree. Distinctness uses a case-folded key (183) while the hash is case-sensitive — consistent with the docstring (only uniqueness is case-folded).
- Vote regex (117): `^\s*ENTAIL\s+([0-9a-f]{12})\s+(entailed|overclaim)\b` — lowercase hex only, exactly 12, CRLF-tolerant (`\b` before `\r`), word-boundary guards against `entailedxyz`. A 13-hex token fails the trailing `\s+` and does not match. Only the FIRST verdict token is read; trailing prose (the selftest itself writes a trailing `— row N`) is ignored.
- File selection (120-130): iterates `ls(ENTAIL_DIR)`, skips basenames starting `MoriR51` and names not ending `.md`; votes keyed by hash into `(verdict, filename)` pairs, so repeated lines and multiple seats dedupe correctly. `read(path) or ""` tolerates a vanished path.
- Precedence (218-222): an overclaim vote wins over entailed on the same row (row 6 fixture: 21 entailed + 1 overclaim → `entailed=20 dissent=1`), dissent on any hash that matches no row is inert (old-text dissent after claim replacement, per contract). `entailed != claims` (225) then requires every table row to have ≥ 1 entailed vote; votes are read at rev R only.
- `git_lister` (259-264): `git ls-tree --name-only <rev> <dir>` — with `ENTAIL_DIR`'s trailing slash this lists direct children (observed); a missing dir returns rc 0 with empty output (observed at both aa3af1ec and 87e0c374), so the do-nothing control's `entailed=0` reflects reality, and the final `[""]` from `split("\n")` is dropped by the `.md` filter. Quirk: without the trailing slash, ls-tree returns the tree itself; `git show rev:<tree>` then returns rc 0 with the listing text, whose lines start with mode digits and can never match the vote regex — harmless, but the trailing slash on line 37 is load-bearing.
- Interaction with bad rows: a row failing structural checks exits via `continue` (181/187/193/211) before the vote check, so its vote is never counted and `entailed != claims` adds `failed=entailment` on top of `bad_rows`. Observed (fixture X7: all 21 hashes voted, row 21 quote shortened to 5 words): `C2=unmet claims=21 located=20 quote_missing=0 bad_rows=1 sources=5 source_rows=bad pins=ok provenance=ok entailed=20 dissent=0 … failed=bad_rows,entailment,source_rows`, exit 1. Diagnostic over-report only — a bad row already forces unmet.

## Mutation matrix (guarded lines → which arm fails)

Baseline pristine: `pass=34 fail=0`. Each mutant was a scratch copy run with `--selftest`.

| mutation (line) | selftest result | arms killed |
|---|---|---|
| drop `.strip()` in claim_hash (114) | 33/1 | entail_hash_whitespace_folded_met |
| drop whitespace collapse (114) | 33/1 | entail_hash_whitespace_folded_met |
| hex `{12}`→`{16}` (117) | 29/5 | honest_met, entail_one_row_unreviewed_unmet, entail_dissent_unmet, entail_hash_whitespace_folded_met, indented_row_ok |
| drop `overclaim` alternative (117) | 33/1 | entail_dissent_unmet |
| drop L1 prefix filter (124) | 33/1 | entail_l1_file_ignored_unmet |
| drop `.md` filter (124) | 33/1 | entail_non_md_ignored_unmet |
| sibling dir, no trailing slash (122) | 34/0 | none — equivalent mutant: real-path behavior identical (verified at fixture X4) |
| sibling dir, with trailing slash (122) | 33/1 | entail_other_dir_ignored_unmet |
| delete overclaim branch (218-222) | 33/1 | entail_dissent_unmet |
| `entailed != claims` → `dissent` only (225) | 28/6 | entail_no_votes_unmet, entail_one_row_unreviewed_unmet, entail_hash_of_other_text_unmet, entail_l1_file_ignored_unmet, entail_other_dir_ignored_unmet, entail_non_md_ignored_unmet |
| COPIES digest flipped (48) | 31/3 | honest_met, entail_hash_whitespace_folded_met, indented_row_ok |
| MIN_SOURCES 5→6 (41) | 31/3 | same three (sources_floor path) |
| MIN_CLAIMS 12→13 (40) | 31/3 | same three (claims_floor path) |
| MIN_BEYOND 3→4 (43) | 34/0 | none — boundary value unguarded |
| `git_lister` → `return []` (263) | 34/0 | none — see next section |

MIN_SOURCES=5 and MIN_CLAIMS=12 are live and docstring-faithful ("draws on all 5 sources", "at least 12 rows"); MIN_BEYOND's exact value is only weakly guarded (the echo arm proves beyond≥1 fails, nothing pins 3).

## End-to-end through real git (selftest gap demonstrated)

`--selftest` calls `evaluate` in memory only; `main`, `git_reader`, `git_lister`, `--hashes` and the exit codes are never exercised by any of the 34 arms. I built fixture commits in my scratch clone (entry/SOURCES/copies at the data rev):

- Votes committed in `w1/` (one per row hash, taken from `--hashes`): `C2=met claims=21 located=21 quote_missing=0 bad_rows=0 sources=5 source_rows=ok pins=ok provenance=ok entailed=21 dissent=0`, exit 0 (commit 48d0256911c2cdc414a9306e092dd4c8c501b2c5).
- Same commit with an UNTRACKED overclaim file present in the worktree: verdict unchanged (`entailed=21 dissent=0`) — reads are rev-pinned, no worktree leakage.
- Overclaim committed on row 6 (0776e7114a2b2457d80531c48a9ea625d523c5cc): `C2=unmet … entailed=20 dissent=1 failed=entailment`, exit 1.
- `MoriR51`-prefixed ghost vote file committed: ignored in the real path (`entailed` unchanged) — the L1 filter works on real ls-tree output.
- Votes only in sibling dir `.ufo/waves/round-51/other/` (fixture 20a6e7990fde76a85973b29261d8a2632277a76e): pristine counter `unmet … entailed=0 failed=entailment` (correct); the trailing-slash sibling-scan mutant turns the same tree `met … entailed=21`, exit 0 — and that mutant IS killed by `entail_other_dir_ignored_unmet` (33/1), so the directory restriction is guarded.
- The `git_lister` mutant (`return []`): selftest still `pass=34 fail=0`, yet main mode at the overclaim fixture flips from `entailed=20 dissent=1` to `entailed=0 dissent=0`. The 34 green arms therefore say nothing about the git plumbing — MED, mitigated by the freeze sha256 (any counter edit is detectable), by the wave's re-run attacks, and by the end-to-end checks above.

## r50 → r51 diff summary (full unified diff reviewed)

Constants: ENTRY/SRC_DIR retargeted, `ENTAIL_DIR` + `L1_PREFIX` added, MIN_CLAIMS 10→12, MIN_SOURCES 3→5, COPIES replaced with the five frozen sources (digests verified above). New: `claim_hash`, the vote regex, `entail_votes`, `git_lister`; `evaluate` gains `ls`, the vote counters, `failed=entailment`, and `entailed=`/`dissent=` output fields; `main` gains the `--hashes` branch and passes the lister. Docstring rewritten for P-C2 including the entailment sentence and updated limits; usage/read-only lines updated (`git ls-tree` added — the code indeed only calls `git show`/`git rev-parse`/`git ls-tree`). Selftest: 12-row/5-source fixtures, eight new entailment arms; REMOVED relative to r50: the escaped-pipe location arm and the four `normalise()` html arms.

## Probes

- Reports are not fence-aware (unlike `parse_claims`, which skips fenced blocks in the entry): a vote-format line placed INSIDE a fenced example block in a report is counted as that report's vote (in-process probe on the pristine module: counted = True). The wave rule "never start a line with the word ENTAIL" is the only guard; the counter cannot tell a quoted example from a judgment.
- The escaped-pipe feature still works: a quote cell containing `\|` located against a copy containing `|` yields `C2=met … located=21` (in-process probe on the pristine module with real data-rev entry/SOURCES/copies; 8-word quote, 14 beyond-words). r51 dropped r50's selftest arm for exactly this while keeping the docstring promise (line 12).
- Current `w1/` census (worktree, mid-wave, context only): 65 entries, 0 named `MoriR51*`, 1 non-`.md` (`swarm-registry.json`, correctly ignored), 0 subdirectories, 11 files already carrying vote-format lines. If the L1's own wave report lands under any name not starting `MoriR51`, its lines matching the vote pattern would count as a seat vote — the exclusion is basename-prefix and honor-based.

## Residual risk and verification gaps

- The landed-tip scoring run (`count-c2.py <landed-tip>`) does not exist yet (wave running); my met/unmet evidence comes from fixture commits built on the data rev. UNVERIFIED: the final integrated tree.
- Timeout paths (`timeout=60` at lines 253-254/261-262 raise uncaught `subprocess.TimeoutExpired` → traceback, exit 1 instead of a `C2_SETUP` 2) are code-read findings, not observed live. Same for git's quotePath behavior on exotic report filenames.
- Seat-side hash computation was not audited (I verified the counter and `--hashes` only); seats that hand-compute rather than use `--hashes` rely on the collapse/strip equivalence proven above.
- This report contains no vote-format lines (self-checked post-write), so it contributes nothing to `entailed`/`dissent` at the final tip.

## Findings

- MED — `count-c2.py:259-264,301-471`: the 34 selftest arms never exercise `main`/`git_reader`/`git_lister`/`--hashes`/exit codes; a `git_lister` mutant (`return []`) passes `pass=34 fail=0` while flipping the real verdict from `dissent=1` to `entailed=0` (observed). Mitigated by freeze-sha256 and the wave's re-run attacks; named limit for the report.
- MED — `count-c2.py:117,120-130`: vote integrity surface is procedural. Any line matching the pattern anywhere in any non-`MoriR51` `.md` file directly in `w1/` counts — including inside fenced example blocks (probe: counted), including from files that are not entailment seats' reports, and only the FIRST verdict token is read (`… entailed overclaim` counts as entailed). L1 exclusion is a basename prefix, bypassable by any other filename. The contract pre-declares the honesty limit; the fence trap and rename bypass are the mechanical residue.
- LOW — `count-c2.py:181,187,193,211,225`: a bad row skips the vote check, so `failed=entailment` is appended alongside `bad_rows` even when every row's hash carries an entailed vote (observed at fixture X7). Diagnostic noise only; unmet either way.
- LOW — `count-c2.py:12,317-330`: r51 dropped r50's escaped-pipe selftest arm while keeping the docstring promise; feature re-verified working by probe, so coverage regression only.
- LOW — `count-c2.py:29,80-85,153`: `normalise()` (html path) is dead code this round — all five COPIES are `kind="text"` — and its four r50 selftest arms were removed; `import html` exists only for it.
- LOW — `count-c2.py:43`: MIN_BEYOND's boundary value is unguarded (mutation 3→4 kills nothing).
- LOW — `count-c2.py:124,261`: code narrows the predicate text ("wave report files … whose names do not start with MoriR51") by also requiring a `.md` suffix and direct children only; votes in a sibling subdirectory of `w1/` or a non-`.md` file are silently ignored. Current wave layout (reports directly in `w1/`, all `.md`) is unaffected.
- LOW — `.ufo/waves/round-51/contract.md` (P-C2) vs `count-c2.py:17-18`: the contract's inline hash definition omits "ends stripped"; the docstring (declared verbatim-predicate) has it. Behaviorally moot (cells are stripped by `split_cells`; `--hashes` is canonical) — wording drift only.
- LOW — `count-c2.py:114` vs `189`: the quote cell is unescaped (`\|`→`|`) before locating, the claim cell is not before hashing; a claim containing an escaped pipe would hash with the backslash. Moot while seats take hashes from `--hashes`.
- LOW — `count-c2.py:270-278`: `--hashes` accepts no `--repo`/`--entry` (repo always derived from `__file__`), unlike main mode; per the usage string, but it means `--hashes` cannot be pointed at a clone the way scoring can.
- LOW — `count-c2.py:282-285`: a dangling `--repo` (missing value) raises an uncaught IndexError, traceback + exit 1 instead of the usage exit 2 (observed). r50 parity.
- LOW — `count-c2.py:253-254,261-262` (code-read, UNVERIFIED live): `timeout=60` subprocess errors inside `evaluate` surface as an uncaught TimeoutExpired traceback (exit 1) rather than `C2_SETUP` exit 2.
- NOTE — `count-c2.py:37,261`: `ENTAIL_DIR`'s trailing slash is load-bearing (`git ls-tree` without it returns the tree itself); `git show rev:<tree>` returns rc 0 listing text that cannot match the vote regex, so the no-slash mutant is behavior-equivalent (observed). No action possible — frozen; recorded so future counter authors keep the slash.

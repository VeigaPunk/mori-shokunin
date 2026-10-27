# Mo55Simple01 — YAGNI review of the C1 counter/scope (round 55, w1)

Seat: `Mo55Simple01`, leaf (no dispatch). Assignment: YAGNI review of the C1 counter and scope design; identify
deletions that preserve the frozen predicate P-C1. Round lane: mori-shokunin. Scratch:
`/fast/scratch/hyaku/mori-r55/Mo55Simple01/` (harness, variants, `out.json`; removed before yield).

**Deletions made: none.** The assignment grants no edit scope and every file in the C1 freeze is immutable, so each
item below is a proposal with a scratch-measured diff, not a landed change. The shared tree is byte-identical to its
frozen state: `sha256sum` of `count-c1.py` (`e30658be…`), `checks/selftest-c1.py` (`48c4c38c…`),
`controls/c1data.py` (`21eb7b2c…`) and `evidence/c1-scope.txt` (`00c145c8…`) equal their `evidence/freeze-sha256.txt`
pins; `git status --porcelain` over `.ufo/waves/round-55`, `corpus/SOURCES.md`, `corpus/evidence/sources-r55` and
`corpus/knowledge` shows only the pre-existing `w1/` and `w1.ready.dispatched` entries of sibling seats. Bytecode
timestamps under `__pycache__` are 03:22–03:24, before this seat ran (03:44+); every import here ran with
`sys.dont_write_bytecode`.

## Axes named

- **A1 predicate preservation** — P-C1's verdict, its counted fields and the frozen 78-pointer scope must not move.
  Hard constraint, not an axis to trade.
- **A2 weight** — lines, branches, names and regex arms in `count-c1.py` and the scope machinery it carries.
- **A3 falsification power** — the frozen selftest and the `controls/` builder must keep rejecting what they reject.
- **A4 re-freeze cost** — a deletion in a pinned file costs a re-pin and an independent verifier replay.

## Method

`/fast/scratch/hyaku/mori-r55/Mo55Simple01/harness.py` imports the frozen counter, the frozen control
(`controls/c1data.py`) and the frozen selftest from the lane (read-only), renders two variants under scratch, and
compares them to the frozen file over four independent surfaces:

1. **the frozen selftest itself**, replayed against each variant with a recording wrapper around `evaluate()`
   (30 calls, compared line-by-line);
2. **an 11-case named mutation matrix** (witness, missing/extra/duplicate row, duplicate displacing a scoped row,
   duplicate ×2, no ledger, no provenance header, no votes, dissent, lazy all-same relabel);
3. **a 150-trial randomised sweep** (random row drops, duplicates and cell corruptions);
4. **the real ledger at the measured data revision `b8b7064c2b54c8b6b22c288232a96c43fae1af47`**, run through
   `count-c1.py <rev> --repo <lane>` for all three files.

Variant **B** = frozen minus candidates 2, 3 and 6; variant **C** = B minus candidates 1 and 4.

## Deletion candidates (proven, in severity order)

| # | sev | location | weight | proof | verdict |
|---|-----|----------|--------|-------|---------|
| 1 | MED | `count-c1.py:99` — `\|Kconfig` alternative in `TOKEN` | 1 regex arm | Takes no input on the frozen entries (scope sha `00c145c8…` = pinned evidence, with and without it); and if it ever fired it *guarantees* unmet: no `Kconfig` copy exists in `COPIES`, so `count-c1.py:365` sets `source_rows=bad` and `derive()` gets `c72=None` → `line` failure as well. It also cannot reach the two real extensionless pointers (see scope findings). | **delete the arm; name the gap in `Limits`** (one sentence) |
| 2 | LOW | `count-c1.py:53` — `SRC = "corpus/evidence/sources-r55/"` | 1 line | Unreferenced name; the only occurrence is the definition. `COPIES` (`:63-95`) carries every copy path literally, and nothing in `checks/` or `controls/` reads `c1.SRC`. Selftest stays 44/0 with it removed. (Literal grep is the fallback proof: no LSP device is mounted in this session — `xd://lsp` answers "No such tool"; the mounted device list carries no language server, so no semantic-reference request could be made. A whole-constant removal of a module-level string with one occurrence is what a reference query would return.) | **delete** |
| 3 | LOW | `count-c1.py:341,345-346,390` — the `dup` flag | 5 lines (479→474 text lines) | Verdict-neutral. 150 randomised trials: `met` identical in 150/150; 11 named mutations: `met` identical in 11/11. Only delta is the `failed=` label on the corner *duplicate row displacing a scoped row while the row count stays 78*: frozen `matched,line,rows,status,votes` vs variant `matched,line,status,votes` — the row is already unmet through `matched`. The selftest's own duplicate/extra checks keep passing through the `rows != len(sc)` term (`checks/selftest-c1.py:127,129`): replay 44/0, 30 `evaluate()` outputs identical. | **delete** (accept losing one diagnostic label) |
| 4 | LOW | `count-c1.py:102` — `docs\.kernel\.org/7\.2/` alternative in `PIN72` | 1 regex arm | Inert by construction: a URL matching only this arm is admitted by `PIN72` and then dropped by `v72_paths()` (`:122-132`), whose two extraction patterns are `/v7\.2/`, `@v7\.2/` and `/plain/…?h=v7.2`. Measured on `SOURCES.md`@ENTER: exactly one such URL (`https://docs.kernel.org/7.2/admin-guide/cgroup-v2.html`), currently filtered-and-dropped. `--scope` output unchanged. | **delete** (removes a filter that advertises a pin it cannot turn into a path) |
| 5 | INFO | `checks/selftest-c1.py:8` — `import subprocess` | 1 line | `ruff check --no-cache --isolated --select F401,F811,F841,ARG002,B018` on the three C1 files: exactly one error, this import. Not used by the file. | proposal only; 1 line is below the re-pin cost |
| 6 | NONE | `count-c1.py:145` — `for sid in sorted(cited):` | 0 lines, 8 chars | Inert: `bmap` is a basename→set map queried by key, and scope order is driven by the entry line scan. `--scope` output identical under `PYTHONHASHSEED=0/7/12345` for the variant. | **no action** — not worth a line edit |

Variant B/C measured facts (all read from this seat's scratch):

- lines: frozen 479 text lines → B/C 474 (5 lines removed by candidates 2+3);
- scope: 78 rows, sha256 `00c145c8d6fc3a9fb7b43735e67cd7e93c13d6fca7b242f73a500e7ab607a489` for frozen, B and C —
  byte-identical to the pinned `evidence/c1-scope.txt`;
- selftest replay: `C1_SELFTEST pass=44 fail=0` for frozen, B and C; all 30 recorded `evaluate()` results identical;
- real ledger at `b8b7064c…`: all three print the same line and exit 1 —
  `C1=unmet scope=78 rows=78 matched=78 status_ok=78 line_ok=78 source_rows=ok pins=ok provenance=ok same=69 moved=7 changed=2 broken=0 holds=78 stale=0 voted=0 dissent=0 rev=b8b7064c… failed=votes`.

## Deletions refused (deleting these would harm an axis — this is the stopping point)

- **`controls/c1data.py:locate_all` (`:37-80`)** — a second, independent statement of "where did these lines go"
  (difflib-mapped) beside the counter's `derive()` (`:217-241`, strict). It reads like duplicated logic, but it is
  the *witness*: it is what makes the counter falsifiable on all 78 rows. Deleting it harms **A3**. Keep.
- **`controls/c1data.py:16-22 V73_SID` and the literal header at `:83`** — a builder-side transcription of the
  path→S-id map and of `count-c1.py:60 HEADER`. Merging them (render from `c1.COPIES`/`c1.HEADER`) would make the
  witness tautological on the header and source-id axes — the two places a wrong cell is most expensive. Keep; the
  duplication buys detection.
- **`count-c1.py --scope` (`:456-459`) and the pinned `evidence/c1-scope.txt`** — the mode is the only reproduction
  path for the pinned listing (`c1-scope-count.txt` and the contract's frozen 78 both cite it). Deleting the mode
  orphans a pin: harms **A3/A4**.
- **The per-round counter family** — 19 rounds carry a file named `count-c1.py` (round-31, 32–38, 42, 44–45, 48–55),
  10,171 lines in total, 479 of them this round's. Measured: of
  18 functions in round-55's counter, only 3 are byte-identical with round-54's (`git_reader`, `lane_root`,
  `split_cells`) while 5 share a name and have drifted (`evaluate`, `final_votes`, `git_lister`, `main`, `scope`).
  This is not copy-paste duplication that can be collapsed; each round's counter is pinned historical evidence with
  a distinct predicate. Delete nothing; if the family recurs, the *new* round should say so in its contract.
- **Micro-parameters** — `copies=` on `evaluate()` (exercised by the selftest), `--repo` (the only way to run
  against a clone), `parse_ledger`'s `header = HEADER` sentinel. One or two lines each; the re-pin cost exceeds the
  weight saved. Not worth an axis move.

## Preserved contract

P-C1 as written in the frozen counter docstring is unchanged under every candidate above: same SCOPE (78 unique
`(entry, path, lines)` keys, sha-pinned), same `derive()` status mapping, same `source_rows`/`pins`/`provenance`
arms, same vote arm (`MIN_VOTES=2`, `VOTERS` = the 16 frozen `Mo55Rc*` names). Candidates 1–4 change no counted
field and no verdict on the measured revision; candidate 3 changes one `failed=` label in a corner where the verdict
is already unmet.

## Scope-design observations (detection only, no widening proposed)

1. **70 tokens in the four entries are dropped by the extractor at ENTER, all for the same reason** — no v7.2-pinned
   `SOURCES.md` row cited by that entry names their path (`0 paths`). None were dropped by the ambiguity guard
   `count-c1.py:166` (`len(paths) != 1`), so the multi-path branch is unexercised and `next(iter(paths))` at `:168`
   is safe on this input. Most drops are correctly out of scope (earlyoom `kill.c`/`main.c`, corpus-local docs,
   `shokunin-watchdog.sh`).
2. **Exactly two Linux v7.2 line pointers fall outside the frozen token grammar**, and the `|Kconfig` arm cannot
   rescue them because it requires a *bare* `Kconfig:` token: `corpus/knowledge/system-pressure-r24.md:70`
   `init/Kconfig:730-731` and `:127` `init/Kconfig:743-760`. Both resolve to a v7.2 S-row (S093 names `init/Kconfig`),
   so under the predicate's prose they would be scoped; under the frozen extractor (authoritative: SCOPE is "every
   pointer the frozen extractor below finds") they are not, and scope stays 78. Recorded because the dead arm reads
   like coverage of exactly this case. **Not proposed to widen**: adding an extensionless-name alternative would move
   the frozen scope.
3. **The pinned at-data receipt carries a different revision than the ticket's measured one, but the same C1
   surface.** `evidence/c1-at-data.txt` records `rev=f70051dd…`; the ticket measures `b8b7064c…`. Both are round-55
   data commits and `git diff --stat f70051dd b8b7064c` over the whole C1 input set (`corpus/SOURCES.md`,
   `corpus/evidence/sources-r55/`, `count-c1.py`, `controls/c1data.py`, the four entries) is empty, so the receipt's
   field vector transports. This seat re-measured it at `b8b7064c` read-only and reproduced it field-for-field
   (`same=69 moved=7 changed=2`, `scope/matched/status_ok/line_ok=78`, `source_rows/pins/provenance=ok`,
   `voted=0 dissent=0`, `failed=votes`, exit 1).
4. **124 KiB of ignored bytecode sits inside the frozen wave dir** (6 `.pyc` under `round-55/`, `checks/`,
   `controls/`). They are git-ignored and regenerable, and currently newer than their sources (03:22:18 vs
   03:22:08), so nothing is stale today. Deleting them is safe but pointless — they return on the next import. The
   deletion-shaped fix is to run the counters with `PYTHONDONTWRITEBYTECODE=1` (or set it in the counter before the
   `importlib` loads at `:446-451`), which is an addition, not a deletion.

## Evidence (command → output → exit)

- `python3 .ufo/waves/round-55/count-c1.py b8b7064c2b54c8b6b22c288232a96c43fae1af47 --repo <lane>` →
  the `C1=unmet … failed=votes` line above → exit 1. Same output for `variant-b.py` and `variant-c.py` → exit 1.
- `python3 harness.py` (scratch) → `out.json` (743 lines): scope shas, trim, witness fidelity, 11-case matrix,
  150-trial sweep (`met_diffs: 0`, `failed_set_diffs: 17`, all of the duplicate-displaces-a-row class), selftest
  replay for three variants (`exit 0`, `pass=44 fail=0`, `selftest_lines_equal_A_vs_B: true`,
  `selftest_lines_equal_A_vs_C: true`, `selftest_evaluate_calls: 30`). Wall 78 s. exit 0.
- `python3 .ufo/waves/round-55/count-c1.py --scope | sha256sum` → `00c145c8d6fc…` = pinned `c1-scope.txt`; same
  under `PYTHONHASHSEED=0` and `12345`; same for `variant-b.py` under seeds 0/7/12345.
- `ruff check --no-cache --isolated --select F401,F811,F841,ARG002,B018 count-c1.py controls/c1data.py
  checks/selftest-c1.py` → 1 error (`selftest-c1.py:8` unused `subprocess`) → exit 1.
- `git diff --stat f70051dd b8b7064c -- <C1 input set>` → empty → exit 0.
- `git merge-base --is-ancestor f70051dd b8b7064c` → true.
- `sha256sum` of the four C1 artifacts vs `evidence/freeze-sha256.txt` → four matches.
- `xd://lsp` → `No such tool` (no language server mounted); semantic-reference proof unavailable this session, so
  the unused-name claims above rest on whole-file literal grep plus the selftest replay.

**Unverified / labelled:** candidate weights are physical lines removed (measured on scratch diffs); no candidate
was applied to the lane, so none has a re-pinned hash or a verifier replay. Candidate 5 has no behavioural test, only
static evidence. The scope-drop probe uses my own regex (`[A-Za-z0-9_.-/]+:<spec>` filtered to basenames that resolve
to one v7.2 path) to find tokens the frozen grammar misses; it is a superset-shaped probe, not the frozen counter,
and its result is exactly two rows. Scratch (harness, variants B/C, `out.json`) is deleted before yield per the seat
rules, so a re-run must rebuild the harness from the Method section: it imports `count-c1.py`, `checks/selftest-c1.py`
and `controls/c1data.py` read-only, applies the three textual variants named above, and compares `evaluate()`
outputs over the four surfaces listed.

## Tradeoffs

- Candidate 3 buys 5 lines and costs one `failed=` label on a corner case. If the round's readers grep `failed=rows`
  to separate "row accounting" from "row content", keep it; the verdict is unaffected either way.
- Candidate 1 is the only one with a design payoff beyond lines: it removes an arm that promises extensionless-file
  coverage it does not deliver. Deleting without the one-sentence `Limits` note would lose the knowledge instead of
  the weight, so the two moves belong together.
- Candidates 2 and 4 are cosmetic-to-small. Their honest justification is that both are *false signal* (an unused
  constant that looks like a root, a filter arm that cannot produce a path), not line count.
- Nothing here improves any axis at the cost of another; the next deletion (the `controls/` witness, the `--scope`
  mode, the round family) would damage A3/A4, so the walk stops here.

## Findings

1. **MED — `count-c1.py:99`, the `|Kconfig` token alternative is dead and lethal-if-live.** It selects nothing on the
   frozen entries (scope sha unchanged without it) and, if it ever selected a bare `Kconfig:<lines>` token, would
   force `source_rows=bad` (`:365`) plus a `line` failure (no `Kconfig` copy in `COPIES`) — an unmettable row. It
   also cannot reach the two real `init/Kconfig` pointers. Evidence:
   `count-c1.py:99`, `:63-95`, `:166`, `:365`; measured scope sha `00c145c8…`; probe rows
   `corpus/knowledge/system-pressure-r24.md:70,127`.
2. **LOW — `count-c1.py:53` `SRC` is an unused module constant.** Evidence: single occurrence in the file; 44/0
   selftest replay with it removed; `xd://lsp` unavailable (grep fallback recorded).
3. **LOW — `count-c1.py:341,345-346,390` the `dup` flag carries no verdict weight.** Evidence: 150/150 randomised
   trials and 11/11 named mutations agree on `met`; only the `failed=` label differs on the
   duplicate-displaces-a-scoped-row corner; selftest 44/0 with it removed.
4. **LOW — `count-c1.py:102` the `docs.kernel.org/7.2/` filter arm is inert** (admit-then-drop for its only live
   URL, `SOURCES.md`@ENTER). Evidence: `:102`, `:118-126`; one measured filtered-and-dropped URL; scope unchanged.
5. **INFO — `checks/selftest-c1.py:8` unused `import subprocess`** (sole ruff F-rule error in the C1 freeze set).
6. **INFO — the scope surface silently excludes every pointer whose v7.2 path has no `SOURCES.md` row cited by the
   entry (70 tokens) and two extensionless `init/Kconfig` pointers.** Both are consistent with the frozen extractor
   and the pinned 78; recorded so the theoretical-vs-measured scope difference is not rediscovered as a defect.
   Evidence: `count-c1.py:137-176`; probe rows `system-pressure-r24.md:70,127`.
7. **INFO — `evidence/c1-at-data.txt` is labelled `rev=f70051dd` while the round measures `b8b7064c`; the C1 input
   set is byte-identical between them** (`git diff --stat` empty), so the receipt transports; re-measured at
   `b8b7064c` with the same field vector. Evidence: `evidence/c1-at-data.txt:1`, `git diff --stat f70051dd b8b7064c`.

# ConnSibling — sibling overlap vs r39 gate-v2, count-c7, conform, gate-ancestry

Axes: sibling-overlap completeness (omission fails the seat); blast-radius honesty (a false "this breaks" harms no-harm); C3 depth (do not import a sibling walk that drops merges).

No tools installed.

## Census

- Lanes walked (23, mori excluded): audio, chousa, game-dev-2d, game-dev-3d, kagi, kaidoku, kake, kama, kasegi, kengaku, kotoba, kotodama, kumitate, lore, mado, revenger, souji, tabi, tameshi, tsukuroi, plus typo trees `mori-shokukin`, `tameshi-shokukin`, `kaidoku-sh2`.
- Exact basename walk, `.ufo` included, sandboxes included: **1,220,254 files, 0 hits** for `count-c7.py`, `conform.py`, `mori-sources-appendonly.py`, `gate-ancestry-r39.md`, or a filename containing `count-c7` / `gate-ancestry` / `mori-sources-appendonly`.
- Content scan of live `tools/`, `scripts/`, `verifiers/`, `corpus/knowledge/`, `corpus/lessons/` (3322 files, `*.py|sh|mjs|md|json`): **0 hits** for `mori-sources-appendonly`, `supersede_timing`, `superseded_as_of`, `stale_supersede`, `gate-ancestry`, `count-c7`, `P-C7`, `P-C8`, `P-C9`.
- Mori surface that would have to be called to break: `tools/mori-sources-appendonly.py:52-53` (only git verbs: rev-parse, log, show, `merge-base --is-ancestor`); timing line at `:403-405`. v2 vs v1 is stated at `:247-252`: full-history, edit vs first parent, supersede-as-of is ancestry not walk order; linear histories agree.

## Overlap table

| Path | What it is | Verdict |
|---|---|---|
| `kama-shokunin/tools/sources-append-only.py:1-20,59-69` | Pairwise `git show REV:PATH` of two revisions. Mutable set `{status, recheck, used-by}`. No `git log`, no `merge-base`. Frozen copy at `.ufo/waves/round-18/frozen/tools_sources-append-only.py` and `.ufo/waves/round-18/build/out/C2AppendOnly-2/sources-append-only.py` are pins of this file, not of mori's gate. | **Cousin, not an implementation of P-C9.** Does not read mori stdout. Gate-v2 does not break it. |
| `kumitate-shokunin/.ufo/waves/round-47/quality/q35-append-only.sh:1-25` | Same cell contract, `<lane> <base> <tip>` blob compare. Summary is `Q35 rewritten/removed`, not `supersede_timing`. Round-52 `build/*/…/q35-append-only.sh` copies are scratch checkouts of this script. | **Cousin.** Can be pointed at any repo's `SOURCES.md`, including mori, and still only diffs cells. v2 does not change cell rules, so it does not break. |
| `kotoba-shokunin/verifiers/check_sources_append_only.py:9-16,99-108` | Walks `rev-list --reverse --no-merges` and diffs each commit against `c^`. Permitted cells match (`:30`). Does not test "superseder descends from the edit." | **Closest cousin, inverted history filter.** `--no-merges` is the class P-C9 fixture C exists to kill (mori v2 uses `--full-history`, gate `:263-264`). Not a P-C9 implementation. Not a consumer. Importing this filter into mori would harm C3. |
| `kotoba-shokunin/.ufo/waves/round-54/falsify/W2RowCheckSourcesAppendOnly.md:1-9` | Attack report on the kotoba verifier (unpack bug on row removal). | **Not this work.** |
| `chousa-shokunin/.ufo/waves/round-32/controls/L1-design-v2/a-append-only.sh:1-11` | Filename says append-only; body is `research-gate.sh` (`RESEARCH_GATE: CLEAN\|DRIFT`). | **False friend.** Not a sources gate. v2 cannot break it. |
| `kotodama-shokunin/corpus/knowledge/verification/append-only-record-verification.md:1-3` | Close-digest / successor-row method for kotodama bookkeeping. No SOURCES walk, no `merge-base` on registry rows. | **Different surface.** |
| `kake-shokunin/.ufo/waves/round-45/w1/ConnectorSiblingOverlap.md:83` | Cites mori r39 `count-c7.py` and `tools/mori-sources-appendonly.py` as not kake's witness classes. | **Citation only.** |
| `kumitate-shokunin/.ufo/waves/round-52/w1/ConnOverlap.md:31` | Lists mori r39 C1–C3 and verdict "No" shared file. Round-49 `ConnSiblingOverlap.md:14,154` cites the r36 gate the same way. | **Citation only.** |
| kaidoku `.ufo/waves/round-22|23|24/**/count-c1.py` (and `count-c2.py`); kama `.ufo/waves/round-25` through `round-31` `count-c1.py` / `count-c2.py` | Other lanes' own claim counters. | **Name family only.** No `count-c7.py`, no `conform.py` anywhere in the 1,220,254-file walk. |
| `corpus/knowledge/gate-ancestry-r39.md` | Present only under `mori-shokunin` (indexed at `mori-shokunin/corpus/README.md:606`, `SOURCES.md` S227/S228). | **No sibling copy.** |

Every other `*append-only*` / `*AppendOnly*` basename under sibling `.ufo` trees (kagi CriticAppendOnly reports, mado/tabi/tameshi/tsukuroi review notes, kotoba census notes, kengaku `RevAppendOnly.md`) is a seat report, not a gate. Sandbox mirrors of those reports were not re-listed; they are copies.

## Proposed move

Do not unify the walks. Keep mori v2's `--full-history` + `merge-base --is-ancestor` (`tools/mori-sources-appendonly.py:247-252,263-264`) and do not treat kotoba's `--no-merges` parent diff, kama's two-rev diff, or kumitate q35 as prior art for P-C9 or as callers that v2 must stay compatible with. The shared fact worth recording is only the mutable-cell set `{status, recheck, used-by}` — the same set v1 already enforced — so a later "harmonize siblings" edit that ports `--no-merges` back into the mori gate would re-open fixture C and harm C3 while leaving C1/C2 untouched. Overlap axis improves by this classification; no other axis moves.

## Risks

- Point-in-time. A sibling seat can add a caller after this walk.
- `.ufo` markdown bodies were not byte-scanned (1.2M files). Executable and knowledge roots were. A prose parser of `supersede_timing` inside an old wave report would not execute, but it would be an unlisted citation. The two concurrent citations found by the earlier lane grep are in the table.
- q35's `<lane>` argument could be pointed at mori by a human. It still grades cells, not timing lines, so v2's non-linear verdict change does not change q35's exit.

## Verification

Re-run, read-only, from the fleet root. Expect empty stdout. Confirmed empty on this seat's walk of 1,220,254 files: no sibling file is named `count-c7.py`, `conform.py`, `mori-sources-appendonly.py`, or `gate-ancestry-r39.md`.

Do not run the mori gate's selftest from this seat (lane read-only; verification belongs to the wave owner). The contract's declared check remains `python3 tools/mori-sources-appendonly.py --selftest` → `pass=12 fail=0`.

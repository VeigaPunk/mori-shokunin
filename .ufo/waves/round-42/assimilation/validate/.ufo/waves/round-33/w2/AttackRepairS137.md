# AttackRepairS137 — falsification of the S137 repair row (round-33 §1)

Target: `corpus/lessons/round-33.md:62` — the row starting `| S137 |` in the "Round-32 repair" §1 table, under rule R-R. Base row: `SOURCES.md@7d382043:143`. Seat report: `.ufo/waves/round-33/w1/RepairS137.md`. Verdict under attack: **no defect that changes the row's conclusion found; two minor residual risks.** Overall: minor.

## Checks run and what held

**(a) "Supported on another page" pointers — all three verified.**

- `corpus/evidence/recheck-r33/S137-main-750a.src` exists at measured rev `62db24c` (blob `99601ddf`). `sha256sum` → `d24a26c97744458706a870ee3eb1ddcd5e5f05dda11fe22a71d6a4952028df3e`, identical to the sha256 recorded in S137's own observation cell at `7d382043` (`main.c@750a7c0d sha256 d24a…`), so the file is a committed copy of the page the source cell names (second URL, `raw.githubusercontent.com/…/750a7c0d…/main.c`).
- `:260` reads verbatim `fprintf(stderr, "Option -k is ignored since earlyoom v1.2\n");` (case `'k'`). `:201` reads `{ "kernel-oom", no_argument, NULL, LONG_OPT_USE_KERNEL_OOM },` inside `long_opt`. `:352` reads `"  --kernel-oom              use kernel OOM killer via /proc/sysrq-trigger\n"`. Line numbers and quoted text exact.
- `corpus/evidence/recheck-r32/S137.src` sha256 `b658df9d…` matches `RepairS137.md:10`; its commit record at `:331–344` states sha `750a7c0d…`, author `2026-02-02`, committer `2026-02-17`, subject "kill: option for triggering kernel oom killer" — carrying "returned … February 2026" and the delegation subject on the population page.

**(b) "Unsupported on every page the row names" — both clauses verified by grep.**

- `grep -n '1\.9' recheck-r32/S137.src` → no match (exit 1); same on `S137-main-750a.src` → no match. Neither copy contains "v1.9", "1.9.0", "binary", or "prints" (grepped `v1\.9\.0|1\.9\.0|binary|name the build|prints` → 0 hits in both). "a v1.9.0 binary prints that output" is unstated everywhere; the row's parenthetical "(the page is commit 750a7c0d, not v1.9.0)" is accurate.
- `grep -niE 'delegation|build'` → hits only in `S137.src:1410,1421` ("add build.sh", "static build" inside an unrelated commit message) and `:2026` (a compiler error line). None states "delegation claims must name the build". Unsupported claim holds; "lane rule, undeclared" is consistent with the seat report (`RepairS137.md:23`).

**(c) Middle column vs closure list and base teaches cell.**

- Closure `corpus/lessons/round-32-verifier-spotcheck.md:91` lists "v1.2 removal (needed for 'returned'); v1.9.0 ignored-option output; `--kernel-oom` spelling" — the repair row's middle column is verbatim-identical.
- Base teaches cell (`7d382043`, full row extracted, 1595 bytes): "The kernel-OOM delegation option left earlyoom in v1.2 and returned on master in February 2026, so a 1.9.0 binary prints 'Option -k is ignored since earlyoom v1.2' while current master grows a --kernel-oom long option (S016 documents it from the master README); delegation claims must name the build they hold for."
- Clause ledger: "left in v1.2" → middle column (v1.2 removal); "returned on master in February 2026" → population page (commit record, treated as carried); "1.9.0 binary prints …" → middle column; "--kernel-oom … grows" → middle column (spelling); "(S016 documents …)" → in-cell attribution, treated as non-clause (consistent with closure's "In-cell attribution" treatment); "delegation claims must name the build" → last column as unsupported. No teaches clause forgotten.
- Verdict "current → not current" is correct: at minimum the v1.9.0-output and build-naming clauses are unsupported on every named page, and the middle-column clauses are absent from the population page (`grep -c 'kernel-oom' recheck-r32/S137.src` → 0; `grep '1\.2'` → only match is the commit message quoting "Linux 5.17", i.e. no v1.2 statement; `grep -ni master` → 0).

**(d) Seat-report comparison.** `RepairS137.md:20-22` had marked the `-k`/`--kernel-oom` quotes "fetch-only … not a committed copy" and judged them unsupported. The integrated row promotes them to "supported on another page" — consistent, because wave-1 later committed the fetched bytes (`recheck-r33/S137-main-750a.src`, hash-identical to the seat's scratch fetch `RepairS137.md:12-13`). The seat's other dispositions (v1.9.0 unsupported, build-naming unsupported, committer-date ≠ merge-date) carry into the row correctly.

## Findings

- **F1 (minor): the `:260` quote does not state the clause it is cited under.** The clause is "v1.2 removal" of the kernel-OOM *delegation* option; the quote says only "Option -k is ignored since earlyoom v1.2". Nothing in `S137-main-750a.src` equates `-k` with kernel-OOM: the same commit maps `'k'` → ignored (`:257-260`) while `"kernel-oom"` → `LONG_OPT_USE_KERNEL_OOM` (`:201`). `-k` ≠ `--kernel-oom` in this very page; identifying the ignored `-k` as the removed kernel-OOM option's compatibility stub needs an unstated historical fact (the v0.6-era spelling). Verdict impact: none — under R-R the clause is still *not carried by the population page*; it would move from "supported on another page" to "unsupported on every page" without changing `not current`. Cited: `recheck-r33/S137-main-750a.src:201,257-260`; `round-33.md:62`.
- **F2 (minor): "returned **on master**" is accepted without a page naming the branch.** `recheck-r32/S137.src` contains no "master"/"default_branch" string (`grep -ni master` → 0). The row implicitly relies on the commits endpoint returning the default branch. Convention-consistent (other rows accept endpoint semantics), and "returned … February 2026" itself is carried by `:331-344`; flagging only because R-R's "quote states it" is literal.
- **F3 (minor, residual): "(S016 documents it from the master README)" is silently dropped as attribution.** Consistent with the closure's In-cell-attribution column, but if a judge counts it as an asserted fact about another page it is unsupported (S016 is not among S137's URLs; `RepairS137.md:22,25`). No row change needed; noted for the repair judge.

## Verification gaps

- Did not fetch live URLs (prohibited scope was only committed copies; the r33 copy's hash equality with the anchor substitutes).
- Did not re-derive whether `750a7c0d` predates/postdates tag v1.9.0; not needed for the row's claim.
- No tools installed or updated; pacman untouched. Scratch: `/fast/scratch/hyaku/mori-r33/AttackRepairS137/s137-row.txt`.

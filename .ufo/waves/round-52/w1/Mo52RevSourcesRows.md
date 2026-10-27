# Seat Mo52RevSourcesRows — SOURCES rows S497-S501 vs registry contract

- Reviewed revision: `8524904adb25e44f24d9f25aac7eae909625c18c` (round-52 data commit), as assigned. HEAD at review time is `075436b1346ca659afb8be7a46f0e67e4170aa83` (wave w1 spec commit); `git diff 8524904..HEAD -- corpus/SOURCES.md corpus/knowledge/overcommit-commit-limit-r52.md corpus/evidence/sources-r52/` is empty, so the rows reviewed are identical at HEAD.
- Lane repo: /home/vgpnk/Projects/shokunin/mori-shokunin (read-only access used; no mutation, no jj/git index changes).
- Scratch: /fast/scratch/hyaku/mori-r52/Mo52RevSourcesRows/ (removed on finish).
- No tool installs performed (all commands used pre-existing git/awk/grep/sed/curl); no pacman, no writes outside scratch and this report.

## Contract read

Contract section `SOURCES.md — where a shokunin learns`, CORPUS.md lines 64-155 (Contract v1, frozen): shape (id/source/kind/tier/scope/anchor/teaches/status/opened/recheck/used-by), rules 1-6, census commands, maintained parser note.

## Rows S497-S501 at 8524904 (excerpts from `git show 8524904:corpus/SOURCES.md`)

| row | kind | tier | scope | anchor (as written) | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|
| S497 | docs | A | three overcommit modes, mode-2 limit, per-mapping accounting, listed gaps at v7.2 | `overcommit-accounting.rst:7-28,33-37,45,54-64,83-84; tag v7.2; copy corpus/evidence/sources-r52/overcommit-accounting.rst.v7.2 sha256 767ab88153c4494e54fcf2db4e5bd01921d6bd8350f1596ada508cb5e4b4927f` | mined | 2026-10-26 | on-release | `corpus/knowledge/overcommit-commit-limit-r52.md` |
| S498 | docs | A | vm sysctls overcommit_memory/ratio/kbytes and the two reserves at v7.2 | `vm.rst:84-97,825-833,836-858,861-866,1029-1046; tag v7.2; copy corpus/evidence/sources-r52/vm.rst.v7.2 sha256 bf8ca0265fefc019250697b6ee47a0679709b2ee45f4d1893b3dfd95c1f8c1ce` | mined | 2026-10-26 | on-release | `corpus/knowledge/overcommit-commit-limit-r52.md` |
| S499 | code | A | vm_commit_limit(), vm_memory_committed(), __vm_enough_memory(), overcommit policy handler at v7.2 | `mm/util.c:781-786,806-834,901-1006; tag v7.2; copy corpus/evidence/sources-r52/util.c.v7.2 sha256 e702754c45bd7bd69e5da22a6505c9c1016eaafe6e883b746cc3cdbd413ebe7c` | mined | 2026-10-26 | on-release | `corpus/knowledge/overcommit-commit-limit-r52.md` |
| S500 | code | A | vm_acct_memory()/vm_unacct_memory() at v7.2 | `include/linux/mman.h:61-84; tag v7.2; copy corpus/evidence/sources-r52/mman.h.v7.2 sha256 d7bf787c910d9a7cbabee3a50c512ce3aad78d63659b0c968adca16b5916b058` | mined | 2026-10-26 | on-release | `corpus/knowledge/overcommit-commit-limit-r52.md` |
| S501 | code | A | MAP_NORESERVE handling in do_mmap(), boot-time reserve initialisers at v7.2 | `mm/mmap.c:546-558,1585-1619; tag v7.2; copy corpus/evidence/sources-r52/mmap.c.v7.2 sha256 449b858385c7ece0ff88a8b41893efadb70a437fb8585a296c4ef0461a4c1545` | mined | 2026-10-26 | on-release | `corpus/knowledge/overcommit-commit-limit-r52.md` |

- `teaches` is one sentence per row, each actionable ("Only mode 2 caps the committed total (swap plus a share of RAM, default half) and fails allocations instead of killing; modes 0 and 1 overcommit." etc.). No `|` inside any cell; no credential material; URLs are canonical raw.githubusercontent.com v7.2-tag paths.

## Checks performed (command → result)

1. `git -C mori-shokunin show 8524904:corpus/SOURCES.md | grep -n -A3 -B1 -E '^\| *S49[7-9] |^\| *S50[01] '` → rows at file lines 276-280, exactly S497-S501, in order, directly after S496.
2. Frozen census (contract lines 135-147) on `SOURCES.atdata.md` (extracted at 8524904):
   - rows = 274; malformed (NF≠13) = 0; dup ids = none; enum/tier-inflation violations = none.
   - tier histogram A=243 B=14 C=17 (sum 274); status histogram mined=224 queued=24 rejected=26 (sum 274).
   - mined used-by existence: 65 unique used-by paths extracted, all present in `git ls-tree -r --name-only 8524904` (no `missing-at-data:` lines).
3. `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori` → exit=0. Fresh output vs evidence/census-start.txt: identical W04 set (23 warnings, same IDs and order) apart from the transcript wrapper lines that the baseline file additionally contains (its first line `$ <command>` and its last line `exit=0`); no W04 entries reference S497-S501. Result: census unchanged from start; W04 count = 23.
4. Blob hashes: `git show 8524904:corpus/evidence/sources-r52/<f> | sha256sum` for all five copies matches exactly the sha256 recorded in each row's anchor cell (767ab881…, bf8ca026…, e702754c…, d7bf787c…, 449b8583…).
5. Anchor landing (numbered `cat -n` on the pinned copies): S498 (vm.rst 84-97, 825-833, 836-858, 861-866, 1029-1046), S499 (util.c 781-786, 806-834, 901-1006), S500 (mman.h 61-84), S501 (mmap.c 546-558, 1585-1619) all land on the quoted content. S497's ranges land on modes (7-28), sysctl/CommitLimit paragraphs (33-38), accounting rules (54-64) and To-Do/ptrace (83-85) — except line 45 (see Findings 1).
6. URL liveness: `curl -fsSL -w '%{http_code}'` → 200 for all five canonical URLs at tag v7.2.
7. used-by target exists at data commit (`git ls-tree 8524904 corpus/knowledge/overcommit-commit-limit-r52.md`), and the entry's provenance trio (`source: S497…S501`, `verified-at: 2026-10-26`, `recheck: on-release` with the curl+sha256 pin command) is consistent with the rows.

## Findings

1. **LOW** — S497 anchor cell cites `45` as a single anchor line, but in the pinned copy (sha256 767ab881…), line 45 is inside the C-stack-growth gotcha paragraph; the overcommit-relevant single line is 48 (`In mode 2 the MAP_NORESERVE flag is ignored.`), which is the line quoted by the entry's claim. The anchor's line list omits 48 and includes 45, so the anchor is not exact for the gotcha it supports. Fix (data correction, allowed): change `45` to `48` in S497's anchor cell (or `43-48`). File: corpus/SOURCES.md row S497.
2. No MED/HIGH findings. All other contract fields (kind enum, tier A scoped to v7.2 primary sources, scope, teaches one-sentence, status mined with existing used-by, opened 2026-10-26, recheck on-release) are conformant; census stable; blob hashes and URLs verified; no second-method duplication (entry points to rows; QUALITY.md untouched by this seat).

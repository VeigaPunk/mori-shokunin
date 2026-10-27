# Mo55Crit05 — C1 duplicate sources: S-id/path matching, basename collisions, pins, omitted lines

Seat: Mo55Crit05 (critic, leaf). Lane: mori-shokunin. Wave: round-55 w1.
Scope of this review: the C1 freshness claim only — duplicate/ambiguous sources, S-id ↔
source-path matching, basename collisions, source pins, and whether any cited line is
omitted from the frozen 78-row scope. No C1/C2 vote lines are emitted by this seat
(non-voter; per seat spec no line in this report begins with the vote keywords).

Frozen references (unchanged):
- Contract: `.ufo/waves/round-55/contract.md`
- Counter: `.ufo/waves/round-55/count-c1.py` (predicate = its docstring)
- Frozen scope: `.ufo/waves/round-55/evidence/c1-scope.txt` (count file confirms 78, exit 0)
- Ledger under test: `corpus/knowledge/kernel-v7.3-recheck-r55.md`
- Registry: `corpus/SOURCES.md`; entering tip `ca52426ea496bc6592e3e867cc9d28843e45f196`; measured data rev `b8b7064c2b54c8b6b22c288232a96c43fae1af47`.

Method: read-only re-derivation. I re-implemented the frozen extractor's resolution
logic in scratch (`probe.py`, `probe2.py`, `probe3.py` under
`/fast/scratch/hyaku/mori-r55/Mo55Crit05/`, removed before yield) and cross-checked it
against the counter's own output. No production files were modified.

## 1. Counter reproduction (command evidence)

Command: `python3 .ufo/waves/round-55/count-c1.py b8b7064c2b54c8b6b22c288232a96c43fae1af47`
Output: `C1=unmet scope=78 rows=78 matched=78 status_ok=78 line_ok=78 source_rows=ok pins=ok provenance=ok same=69 moved=7 changed=2 broken=0 holds=78 stale=0 voted=0 dissent=0 rev=b8b7064c2b54c8b6b22c288232a96c43fae1af47 failed=votes`
Exit: 1. Matches the assignment's data read exactly; sole failure mode is `votes`
(0 RECHECK voters bound at the time of measurement), which is out of this seat's scope.

Command: `python3 .ufo/waves/round-55/count-c1.py --scope` diffed against
`.ufo/waves/round-55/evidence/c1-scope.txt` → byte-identical (exit 0, `SCOPE-IDENTICAL`).
The frozen 78-row scope is exactly what the frozen extractor produces at the entering tip.

## 2. S-id ↔ source-path matching (result: clean)

The ledger's "v7.3 source" column uses S502, S516, S526–S534. For each of the 78 rows I
verified, against `corpus/SOURCES.md` at HEAD and at the data rev:
- the registry row exists with 11 cells;
- its URL set contains exactly `https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/<pointer-path>?h=v7.3`;
- status is `mined`; opened date ∈ {2026-10-26, 2026-10-27};
- used-by list includes `corpus/knowledge/kernel-v7.3-recheck-r55.md`.

Result: 0 mismatches across 78 rows. The S-id → v7.3 path bijection is:
S526 fs/proc/base.c, S527 mm/page_alloc.c, S516 mm/oom_kill.c, S528 include/trace/events/oom.h,
S529 Documentation/accounting/psi.rst, S530 kernel/sched/psi.c, S531 include/linux/psi_types.h,
S532 Documentation/admin-guide/kernel-parameters.txt, S533 Documentation/admin-guide/cgroup-v2.rst,
S502 Documentation/filesystems/proc.rst, S534 kernel/fork.c.
Ledger header `source:` line cites exactly these 11 S-ids, and `used_ids ⊆ cited` holds.
Row distribution per S-id sums to 78 (S530: 34, S516: 14, S529: 9, S533: 7, S526: 6,
S527/S528: 2 each, S502/S531/S532/S534: 1 each). Per entry: 13 + 14 + 51 = 78.

## 3. Duplicate sources (result: clean)

- Registry-wide scan for duplicate v7.3 cgit URLs (any two S-ids claiming the same v7.3
  bytes): 0 at HEAD, 0 at the data rev. No duplicate v7.3 authority for any of the 11 paths.
- v7.2 side: 15 URL groups are shared by multiple S-ids (e.g. mm/oom_kill.c v7.2 under
  S003/S476/S491; fs/proc/base.c v7.2 under S127/S148/S166/S476). These are same-path
  aliases; the extractor stores paths in a set (`bmap.setdefault(base, set()).add(p)`),
  so aliases collapse and cannot inject a wrong path.
- Ledger hash column: 78 unique hashes, no duplicates; each recomputes as
  `sha256("entry|path|spec")[:12]` from the frozen scope (0 mismatches of 78).

## 4. Basename collisions (result: no impact; one latent fragility)

The extractor resolves a token's path by basename through the S-ids cited in that entry,
and silently skips tokens whose basename maps to anything other than exactly one path
(`count-c1.py:166`). Per-entry basename maps at the entering tip:
- oom-tracepoints-r47.md: base.c, oom.h, oom_kill.c, page_alloc.c — each → 1 path.
- system-pressure-r24.md: Kconfig, cgroup-v2.rst, kernel-parameters.txt, psi.c, psi.rst,
  psi_types.h — each → 1 path.
- watchdog-identity-r31.md: array.c, binfmt_script.c, exec.c, kernel.rst, sched.h —
  each → 1 path (and the contract's claim holds: it cites v7.2 kernel S-ids but
  contributes 0 line-pointer rows — all its tokens are lane-internal or non-kernel).
- oom-victim-selection-r27.md: base.c, cgroup-v2.rst, fork.c, oom.h, oom_kill.c,
  proc.rst — each → 1 path. Note: in this entry `oom.h` resolves to
  `include/uapi/linux/oom.h` (via S127/S148), not `include/trace/events/oom.h`; the entry
  contains no `oom.h:…` token, so nothing resolves to a path outside COPIES.

Registry-wide at the entering tip, 3 basenames map to >1 v7.2 path: `core.c`
(block/partitions vs drivers/base), `errno.h` (3 arch paths), and `oom.h`
(include/trace/events vs include/uapi/linux). None of the four entries cites S-ids that
pull both sides of any of these into one entry, so 0 tokens were skipped due to
collision. This is a latent property of the frozen extractor, not a round-55 defect.

## 5. Pins (result: clean)

All 22 pinned copies in the counter's COPIES table (`count-c1.py:62-96`) hash-match:
- on the working tree (HEAD b8a70adf): 22/22 OK;
- at the measured data rev b8b7064c (git-show blobs): 22/22 OK.
Cross-check against `evidence/freeze-sha256.txt` shows the same digests for the 24
r55-fetched files. Four v7.2/v7.3 pairs are byte-identical (oom_kill.c 452f1348…,
oom.h 82f04ad4…, psi.rst 11c6b712…, psi_types.h 483269b2…), consistent with the ledger
marking every pointer into those files `same`.

## 6. Cited lines omitted from scope (result: none omitted that the predicate covers)

I re-ran the frozen extractor over all four entries at the entering tip and classified
every token it saw:
- 88 token instances resolved to exactly one path → 78 unique (entry, path, spec) rows
  (10 duplicate instances are prose repeats; the scope dedups by key). Diff against the
  frozen scope: identical (§1).
- 70 token instances were skipped, every one because its basename had no v7.2 registry
  URL among the entry's cited S-ids (`candidates=[]`). Two groups:
  (a) lane-internal cross-references (README.md, PROVINCE.md, shokunin-watchdog.sh,
      mori-census.sh, lessons/knowledge pointers) and third-party non-kernel sources
      (earlyoom, systemd, man-pages, omp) — outside C1's "Linux-v7.2 line pointer" scope;
  (b) ~13 Linux-v7.2 kernel pointers in system-pressure-r24.md carrying inline
      raw.githubusercontent.com `/v7.2/` URLs but no registry row — init/main.c:1011,1047,1445,
      kernel/cgroup/cgroup.c:4077-4091/:4127/:3970-4091/:5585-5589, include/linux/psi.h:39,
      kernel/time/sched_clock.c:48-50,242-243, include/linux/sched/clock.h:112-116,
      arch/x86/kernel/tsc.c:327-328,1544-1545, kernel/sched/clock.c:176,243,
      kernel/sched/sched.h:3492-3495/:3518-3521. The entry itself flags these as
      "no registry row" (system-pressure-r24.md:27,128,150,166).
Group (b) is a boundary of the frozen predicate (registry-mediated resolution), not an
execution defect: the contract froze the scope at exactly these 78 rows, the kill rules
cover only missing/extra/mismatched rows, and these pointers are not voteable rows. No
resolvable cited line was omitted from the frozen scope, and no row cites a path outside
COPIES (the counter's `bad_src` check confirms `source_rows=ok`).

Status tally independently confirmed from the ledger: 69 same / 7 moved / 2 changed,
matching the frozen contract. The 9 non-same rows are ledger lines 13, 19, 58, 66, 67,
68, 82, 83, 85.

## Findings

- INFO (positive evidence): S-id ↔ path matching exact for all 78 rows; 11-source
  bijection; provenance fields (mined, opened 2026-10-26/27, used-by) all satisfy the
  counter's checks. Evidence: `corpus/SOURCES.md:281,295,306-314`; counter output §1.
- INFO (positive evidence): no duplicate v7.3 sources registry-wide; no duplicate ledger
  hashes; 78 unique hashes recompute exactly. Evidence: §3; `evidence/c1-scope.txt`.
- INFO (positive evidence): 22/22 pins match at HEAD and at the measured data rev;
  four byte-identical v7.2/v7.3 pairs consistent with all-`same` statuses. Evidence: §5.
- LOW (latent, by design): frozen extractor silently skips basename-ambiguous tokens
  (`count-c1.py:166`); registry has 3 colliding v7.2 basenames (oom.h, core.c, errno.h).
  No round-55 impact — the four entries never cite both sides of a collision. Evidence: §4.
- LOW (predicate boundary, disclosed by the entry itself): ~13 inline-URL v7.2 kernel
  pointers in system-pressure-r24.md are outside the frozen 78 by registry-mediated
  design; they are not voteable rows and trigger no kill rule. Evidence:
  `corpus/knowledge/system-pressure-r24.md:27,128,150,166`; §6.

No C1-kill defects found in the duplicate-source / matching / collision / pin /
omission dimension. The unmet verdict at the data rev is attributable solely to
`failed=votes`, pending the RECHECK voters.

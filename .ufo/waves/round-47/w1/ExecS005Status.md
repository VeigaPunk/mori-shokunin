# ExecS005Status — wave w1 report (round 47)

Seat: ExecS005Status (leaf, read-only inspection). Lane: mori-shokunin.
Scope assigned: inspect SOURCES row S005 (oom.h at commit c03c1a14…, status per brief "queued"),
fetch that exact commit's file, diff against the v7.2 copy
`corpus/evidence/sources-r47/include_trace_events_oom.h`, report whether `mark_victim`'s
fields differ and whether S005's anchor line numbers (76, 82-105) still hold at v7.2; and run
`tools/mori-sources-appendonly.py 63eecf2738db96f46b0bd02b1b2dfd66787493d0 --round-base
2d85e33d14198d388fd3cda9cc15ec07e57e7a53`.

All paths below are relative to the lane root `/home/vgpnk/Projects/shokunin/mori-shokunin`
unless absolute. Host read-only; no git/jj mutation; no tools installed (nothing was needed).

---

## 1. S005 row (observed)

`corpus/SOURCES.md` line 11:

> | S005 | Linux OOM trace events — https://raw.githubusercontent.com/torvalds/linux/c03c1a14507dfaf8b856c2608f9ac216021fc222/include/trace/events/oom.h | code | A | Linux oom:mark_victim tracepoint field schema | include/trace/events/oom.h:76,82-105; Linux master commit c03c1a14507dfaf8b856c2608f9ac216021fc222 (2026-10-18) | The victim-mark tracepoint exposes PID, comm, UID, memory fields and oom_score_adj as a distinct event schema. | mined | 2026-10-19 | on-release | corpus/knowledge/oom-tracepoints-r47.md |

- Observed status is **mined**, not queued as the seat brief stated; used-by =
  `corpus/knowledge/oom-tracepoints-r47.md` (row is already referenced by the round-47 entry name).
- Anchor cell: `include/trace/events/oom.h:76,82-105`; commit c03c1a14507dfaf8b856c2608f9ac216021fc222 (2026-10-18).

## 2. Fetch of exact commit c03c1a14's oom.h

Command: `curl -fsSL --max-time 30 https://raw.githubusercontent.com/torvalds/linux/c03c1a14507dfaf8b856c2608f9ac216021fc222/include/trace/events/oom.h -o /tmp/oom_c03c1a14.h`
Exit 0. File: 223 lines.
sha256: `82f04ad4108ba9499b638fe298967f124269c0a2feb6ddbb14b1ade59c974e0d`

## 3. Diff vs the committed v7.2 copy

`diff -u /tmp/oom_c03c1a14.h corpus/evidence/sources-r47/include_trace_events_oom.h` → empty, exit 0.
sha256 of the v7.2 copy: `82f04ad4108ba9499b638fe298967f124269c0a2feb6ddbb14b1ade59c974e0d` — identical.
The two files are byte-identical (223 lines, same hash).

## 4. mark_victim field comparison (S005 scope)

No difference: the fetched c03c1a14 file and the v7.2 copy are the same bytes, so `mark_victim`
has the identical schema in both:

- `TRACE_EVENT(mark_victim, ...)` at line 76 in both.
- `TP_STRUCT__entry` fields (lines 82-90 in both): `pid` (int), `comm` (__string),
  `total_vm`, `anon_rss`, `file_rss`, `shmem_rss` (unsigned long), `uid` (uid_t),
  `pgtables` (unsigned long), `oom_score_adj` (short) — 9 fields, same order/types.
- `TP_fast_assign` lines 93-103 and `TP_printk` at line 105 identical.

**Verdict: S005's mark_victim schema is unchanged between c03c1a14 and v7.2.**

## 5. Anchor line numbers at v7.2

- Line 76 = `TRACE_EVENT(mark_victim,` — holds.
- Lines 82-105 = the entry field set (82-90), `TP_fast_assign` body (93-103) and the opening of
  `TP_printk` (105) — all hold.
- Since the files are byte-identical, the same anchors hold verbatim at c03c1a14.

**Verdict: S005 anchors (76, 82-105) hold at v7.2 (and at c03c1a14).**

## 6. mori-sources-appendonly.py run

Command (cwd = lane root, TMPDIR=`/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r47-ExecS005Status`):

```
python3 tools/mori-sources-appendonly.py 63eecf2738db96f46b0bd02b1b2dfd66787493d0 --round-base 2d85e33d14198d388fd3cda9cc15ec07e57e7a53
```

Exit code: **0** (with `--round-base`, main() returns 1 iff `round_changed` non-empty; it was empty).

Key output (freeze rev 63eecf2):
```
changed S041 superseded_by=S206
... (18 changed rows: S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193)
appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S041,S044,S051,S062,S064,S067,S069,S070,S071,S083,S084,S090,S093,S096,S097,S101,S124,S127,S128,S129,S131,S140,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193,S226,S229,S235] round_changed=[]
supersede_timing superseded_as_of=[<same 36 ids>] stale_supersede=[]
```

Interpretation (grounded in the tool's walk of SOURCES.md history to the given rev):
- The gate reports 18 historical append-only violations (rows edited vs first-parent tree) at the
  freeze rev, with no deletions and 36 supersede rows; `stale_supersede=[]`.
- `round_changed=[]` → no SOURCES row changed between the round base (2d85e33) and the freeze rev.
- Comparison run at the entering tip (`2d85e33d14198d388fd3cda9cc15ec07e57e7a53` with the same
  `--round-base`) prints the identical violation set and `round_changed=[]` → the 18 violations
  pre-date round 47; they are not introduced by this round.
- S005 is not among the changed/violation ids, so S005 is untouched per the gate.

## 7. Notes / risks

- Network fetch of the raw GitHub URL succeeded and resolved by full commit hash; the fetched bytes
  equal the committed v7.2 copy, so no off-tree content was relied on for the comparison.
- The seat brief described S005 status as "queued"; the current row says `mined` (used-by
  `oom-tracepoints-r47.md`). Flagged for the L1 — likely a post-brief update, not a conflict.
- No tools installed; no host state touched; only read-only git (invoked by the gate) and curl.
- Scratch used: `/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r47-ExecS005Status/` (TMPDIR for lane tool runs).

## 8. Evidence summary

| Check | Result |
| --- | --- |
| Fetch c03c1a14 oom.h (raw GitHub, full hash) | exit 0; 223 lines; sha256 82f04ad4…e0d |
| v7.2 committed copy sha256 | 82f04ad4108ba9499b638fe298967f124269c0a2feb6ddbb14b1ade59c974e0d (same) |
| `diff -u` fetched vs v7.2 copy | empty, exit 0 → byte-identical |
| mark_victim fields (9 field set, lines 82-90) | identical in both |
| Anchors 76 and 82-105 at v7.2 | hold verbatim |
| appendonly gate at freeze 63eecf2 | exit 0; appendonly_violations=18 (pre-round-47); deleted=[]; round_changed=[]; stale_supersede=[] |
| appendonly gate at entering tip 2d85e33 | identical output (violations pre-date round 47) |

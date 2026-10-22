# SrcProcRstOom — Linux 7.2 Documentation/filesystems/proc.rst: oom_adj / oom_score_adj / oom_score

Question: what does the kernel's own proc.rst document about the OOM badness score, the
-1000/+1000 `oom_score_adj` values, inheritance across fork, and the unprivileged-lowering rule,
plus the SOURCES row or anchor this file needs for C1.

Bottom line: this file already owns row **S082** at the same tag, so the binding rule gives an
**anchor addition to S082**, not an S127+ row. The fork-inheritance sentence is **not in proc.rst**;
it is in `kernel/fork.c` (observed below, cross-reference only). Consequence for C1: S082 cannot
count toward `new_rows_cited` (the counter requires ids >= S127).

## Gate block

- URL: https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/filesystems/proc.rst
- Access: 2026-10-22, ordinary `curl` only. First request at 2026-10-22T15:46:42Z returned
  `HTTP 429` ("rate-limited ... from your network", 313 bytes); a single retry after a 20 s pause
  returned `HTTP 200 bytes 107560`. Saved to scratch as `proc.rst.v7.2` (2495 lines).
- sha256: `e760f716f8278deefab17a63739033cadc7faee93663c49e76455afaaf40d126`
  (matches the `sha256 e760f716f8278dee` prefix already recorded in S082)
- Located quotes (verbatim, <=25 words each):

| # | lines | quote |
|---|---|---|
| Q1 | 1761-1763 | "The badness heuristic assigns a value to each candidate task ranging from 0 (never kill) to 1000 (always kill)" |
| Q2 | 1777-1778 | "The value of /proc/<pid>/oom_score_adj is added to the badness score before it is used to determine which task to kill." |
| Q3 | 1778-1779 | "Acceptable values range from -1000 (OOM_SCORE_ADJ_MIN) to +1000 (OOM_SCORE_ADJ_MAX)." |
| Q4 | 1782-1784 | "The lowest possible value, -1000, is equivalent to disabling oom killing entirely for that task since it will always report a badness score of 0." |
| Q5 | 1799-1800 | "The value of /proc/<pid>/oom_score_adj may be reduced no lower than the last value set by a CAP_SYS_RESOURCE process." |

## Findings (observed in proc.rst at tag v7.2)

- Section headings: `3.1 /proc/<pid>/oom_adj & /proc/<pid>/oom_score_adj` at :1755 (body 1758-1801);
  `3.2 /proc/<pid>/oom_score` at :1804 (body 1807-1812). TOC entries at :37-39.
- Badness score meaning (:1761-1766): 0 = never kill, 1000 = always kill; the number is roughly the
  task's proportional share of "allowed" memory estimated from current memory and swap use.
  "Allowed" is context-dependent (:1768-1775): cpuset mems, mempolicy nodes, the reached memcg
  memory/swap limit, or all allocatable resources for a system-wide OOM.
- `oom_score_adj` is **added after** the badness score (Q2, :1777-1778); acceptable range
  -1000 `OOM_SCORE_ADJ_MIN` .. +1000 `OOM_SCORE_ADJ_MAX` (Q3, :1778-1779); -1000 forces badness 0
  and so disables OOM killing for that task (Q4, :1782-1784).
- Worked polarisation examples: +500 "roughly equivalent to allowing the remainder of tasks ... to
  use at least 50% more memory"; -500 discounts half the task's allowed memory (:1786-1791).
- Legacy `oom_adj` (:1793-1797): range -16 `OOM_ADJUST_MIN` .. +15 `OOM_ADJUST_MAX`, special -17
  `OOM_DISABLE` disables OOM killing, value scaled linearly to `oom_score_adj`.
- Unprivileged-lowering rule (Q5, :1799-1801): the value may be reduced no lower than the last value
  set by a `CAP_SYS_RESOURCE` process; going lower requires `CAP_SYS_RESOURCE`.
- `/proc/<pid>/oom_score` (:1807-1812): "the exported value includes oom_score_adj so it is
  effectively in range [0,2000]" (:1811-1812). So a live `oom_score` read cannot be used as the bare
  badness number without subtracting the adjustment.
- Absence is source-bounded: `grep -n -i oom` over the fetched file returns only :37, :39, :1755,
  :1759, :1768, :1777, :1779, :1782, :1786, :1793, :1795, :1797, :1799, :1808, :1811. No other
  OOM text exists, so there is no `memory.oom.group` or earlyoom material in this file (those are
  other seats' sources, not this one).

## Absent from this source: inheritance across fork

proc.rst v7.2 documents no fork/child inheritance for `oom_score_adj`. The words do not appear:
`grep -n -i -E 'fork|inherit'` returns :284, :592, :599, :1034, :1633 (each about capabilities, VMAs,
thread-stack or map-inheritance) and `grep -n -i child` returns only the `/proc/<pid>/task/<tid>/children`
section (:44, :2014-2025). The claim must not be anchored on S082 or on this file. [INFERENCE] the
missing half of the sentence — that the pair is copied at fork — belongs to kernel source, not the
proc documentation; verified location below.

## Cross-reference (NOT my row, no SOURCES row exists yet)

- File: https://raw.githubusercontent.com/torvalds/linux/v7.2/kernel/fork.c, fetched 2026-10-22 with
  the same `curl`, `HTTP 200 bytes 85725`, sha256
  `359882ea981b58f5289293e5644f7c0085a8350e4f1937f39dcb94ae1cd0dd1d`, 3409 lines.
- `copy_signal`: :1768-1769 `sig->oom_score_adj = current->signal->oom_score_adj;`
  `sig->oom_score_adj_min = current->signal->oom_score_adj_min;`
- `copy_oom_score_adj` at :1949-1968, called from `copy_process` at :2558; it skips kernel threads
  (`if (!tsk->mm) return;`, :1953-1954) and skips thread/vfork clones
  (`if ((clone_flags & (CLONE_VM | CLONE_THREAD | CLONE_VFORK)) != CLONE_VM) return;`, :1957-1958),
  then re-copies the pair under `oom_adj_mutex` (:1960-1965) — the "in case they were changed after
  copy_signal" comment at :1962. `oom_score_adj_min` is the field behind the CAP_SYS_RESOURCE floor.
- `grep -n "kernel/fork\|fork\.c" corpus/SOURCES.md` returns nothing: `kernel/fork.c` is an unowned,
  new file. If a new S127+ row is wanted for C1's counter, this is a candidate anchor
  (`kernel/fork.c:1768-1769,1949-1968,2558`), but I did not mint it — row ownership is the planner's.

## Ready-to-paste: S082 row (anchor added, scope/teaches/used-by extended)

This source re-opens S082's exact URL at the exact tag, so the contract gives an anchor, not a new
row. Replace the whole S082 line with:

```markdown
| S082 | Linux proc.rst v7.2 — mountinfo layout and per-process OOM score files — https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/filesystems/proc.rst | docs | A | the textual mountinfo field layout plus the per-process `oom_adj`/`oom_score_adj`/`oom_score` semantics: badness-score meaning, adjustment range, the -1000 disable value, the legacy `oom_adj` scale and the CAP_SYS_RESOURCE floor; not fork inheritance, not 3.3 onward | mountinfo section3.5:1965-2002, field table:1973-1983; oom section3.1:1755-1801, badness:1761-1763, adj added:1777-1778, range:1778-1779, -1000 disables:1781-1784, legacy oom_adj:1793-1797, CAP_SYS_RESOURCE floor:1799-1801; oom_score section3.2:1804-1812, includes adj and 0..2000:1811-1812; tag v7.2; sha256 e760f716f8278deefab17a63739033cadc7faee93663c49e76455afaaf40d126 | Scan optional mountinfo fields to the separator, then read fstype, source and super options; the badness score is a proportional 0..1000 share of allowed memory, `oom_score_adj` is added after it, -1000 forces 0, and an unprivileged task cannot lower it below the CAP_SYS_RESOURCE floor, while exported `oom_score` already includes the adjustment and spans 0..2000. | mined | 2026-10-21 | on-release | corpus/lessons/round-23.md, corpus/knowledge/oom-victim-selection-r27.md |
```

Check before pasting: the row keeps 11 columns (`| id | source | kind | tier | scope | anchor |
teaches | status | opened | recheck | used-by |`), status stays `mined`, and `opened` stays
`2026-10-21` because that is when S082 was first opened; today's re-open is an anchor addition.

## Consequence for C1's counter

`count-c1.sh` counts only ids with `num >= 127` that are `mined` and name the entry in `used-by`
(`.ufo/waves/round-27/count-c1.sh:11-12,25-32`). S082 can be cited in the entry's body prose but
adding it to the entry's `source:` line earns nothing toward `new_rows_cited`. The three S127+ rows
must come from genuinely new files/URLs opened this round (the earlyoom option surface rows and
whatever the kernel-side seats mint); this seat's file is not one of them.

## Privacy and tooling

- Nothing written here copies a command line, uid, pid list, journal MESSAGE text, harness setting
  value or key, `/etc/default/earlyoom` value, or any `--prefer`/`--avoid`/`--ignore` expression.
  No host state was read for this seat; only public upstream bytes and the lane's SOURCES/counter.
- Tooling: no install or upgrade. Used the stock `curl` and the read/grep tools; scratch under
  `/fast/scratch/hyaku/mori-r27/SrcProcRstOom/`.

## Unresolved gaps

- Fork inheritance is unowned: needs an S127+ row (candidate `kernel/fork.c`, anchor above) or the
  man-pages seat's row; the knowledge entry must not attribute it to proc.rst/S082.
- `memory.oom.group` is not in proc.rst; another seat's source must carry it.
- Whether the planner prefers an S127+ row splitting the OOM half out of S082: the contract's
  re-open rule says anchor, and I followed it; a split would still need a citable new URL to count.

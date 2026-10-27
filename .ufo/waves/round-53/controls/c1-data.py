#!/usr/bin/env python3
"""Round 53 C1 data applier (L1 MoriR53). Builds the recheck ledger table, the SOURCES rows S502-S513 and,
for controls only, synthetic voter files. Usage:
  c1-data.py --print-table            print the ledger table derived from the frozen scope and the v7.3 copies
  c1-data.py --print-rows             print the SOURCES rows S502-S513
  c1-data.py <clone-dir> <parts>      apply comma-separated parts inside a throwaway clone (controls only):
      ledger    write corpus/knowledge/kernel-v7.3-recheck-r53.md (minimal prose + table)
      allheld   (with ledger) label every row held with its v7.2 quote
      rows      insert S502-S513 at the end of the Registry table of corpus/SOURCES.md
      votes     write synthetic RECHECK lines for Mo53Fr01 and Mo53Fr02 (feasibility witness only)
      v72copies overwrite the six changed v7.3 copies with the lane's committed v7.2 bytes
Status, quote and source cells are derived, never typed: status by the counter's rule, quote = the v7.2 quote
when held else the replacement below, source = the row for the claim's kernel path.
"""
import importlib.util
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
W = os.path.dirname(HERE)
LANE = os.path.dirname(os.path.dirname(os.path.dirname(W)))
spec = importlib.util.spec_from_file_location("count_c1", os.path.join(W, "count-c1.py"))
C = importlib.util.module_from_spec(spec)
spec.loader.exec_module(C)

SID = {
    "Documentation/filesystems/proc.rst": "S502",
    "mm/show_mem.c": "S503",
    "fs/proc/meminfo.c": "S504",
    "include/linux/mm_inline.h": "S505",
    "Documentation/mm/overcommit-accounting.rst": "S506",
    "Documentation/admin-guide/sysctl/vm.rst": "S507",
    "mm/util.c": "S508",
    "include/linux/mman.h": "S509",
    "mm/mmap.c": "S510",
}
# replacement quotes for the rows whose v7.2 quote is absent at v7.3 (located in the v7.3 copy, 6-25 words)
REPLACE = {
    "0fbd62f51ce8": "We honor MAP_NORESERVE if allowed to overcommit */ if (sysctl_overcommit_memory != "
                    "OVERCOMMIT_NEVER) vma_flags_set(&vma_flags, VMA_NORESERVE_BIT);",
    "d7a1dc88dcb3": "hugetlb applies strict overcommit unless MAP_NORESERVE */ if (file && is_file_hugepages(file)) "
                    "vma_flags_set(&vma_flags, VMA_NORESERVE_BIT);",
}
DISPOSITION = {}  # hash -> "changed"; every other row "holds"
LEDGER = C.LEDGER
R53 = "corpus/evidence/sources-r53/"
CG = C.CGIT
T73 = "tag v7.3 (091b06388b11, commit c03c1a14507d)"
ROWS = [
    ("S502", "Linux Documentation/filesystems/proc.rst at tag v7.3 — %sDocumentation/filesystems/proc.rst?h=v7.3" % CG,
     "docs", "A", "the /proc/meminfo field definitions at v7.3, for the v7.3 recheck of the round-51 MemAvailable claims",
     "%s; meminfo section lines 1043-1240 (MemAvailable 1127, CommitLimit 1221, Committed_AS 1239); sha256 bc178ff511e0; copy %sproc.rst.v7.3" % (T73, R53),
     "re-checks a v7.2-pinned meminfo field claim against the current release; v7.2 to v7.3 changes 3 lines, none in the meminfo definitions",
     LEDGER),
    ("S503", "Linux mm/show_mem.c at tag v7.3 — %smm/show_mem.c?h=v7.3" % CG, "code", "A",
     "si_mem_available at v7.3 (the MemAvailable estimate)",
     "%s; si_mem_available lines 33-73; sha256 c50205bc1997; copy %sshow_mem.c.v7.3" % (T73, R53),
     "shows the MemAvailable estimate body unchanged at v7.3; the release's edits there are an include, const nodemask parameters and printk units",
     LEDGER),
    ("S504", "Linux fs/proc/meminfo.c at tag v7.3 — %sfs/proc/meminfo.c?h=v7.3" % CG, "code", "A",
     "how /proc/meminfo prints its lines at v7.3",
     "%s; meminfo_proc_show from line 34 (CommitLimit and Committed_AS at 125-126); sha256 d6c5807421a6, byte-identical to v7.2; copy %smeminfo.c.v7.3" % (T73, R53),
     "proves the meminfo printer is byte-identical between v7.2 and v7.3, so a v7.2 line-format claim carries over",
     LEDGER),
    ("S505", "Linux include/linux/mm_inline.h at tag v7.3 — %sinclude/linux/mm_inline.h?h=v7.3" % CG, "code", "A",
     "which folios sit on the file LRU lists at v7.3",
     "%s; folio_is_file_lru at line 28; sha256 277e99e23ecc; copy %smm_inline.h.v7.3" % (T73, R53),
     "re-checks the file-LRU membership rule the MemAvailable estimate relies on; the v7.3 edit removes an unrelated uffd-wp helper",
     LEDGER),
    ("S506", "Linux Documentation/mm/overcommit-accounting.rst at tag v7.3 — %sDocumentation/mm/overcommit-accounting.rst?h=v7.3" % CG,
     "docs", "A", "the three overcommit modes and the mode-2 limit at v7.3",
     "%s; whole file lines 1-85; sha256 767ab88153c4, byte-identical to v7.2; copy %sovercommit-accounting.rst.v7.3" % (T73, R53),
     "proves the overcommit modes text did not change in v7.3, so the round-52 mode claims carry over word for word",
     LEDGER),
    ("S507", "Linux Documentation/admin-guide/sysctl/vm.rst at tag v7.3 — %sDocumentation/admin-guide/sysctl/vm.rst?h=v7.3" % CG,
     "docs", "A", "overcommit_memory, overcommit_ratio, overcommit_kbytes and the two reserves at v7.3",
     "%s; admin_reserve_kbytes 82-109, overcommit_kbytes 823, overcommit_memory 834, overcommit_ratio 859, user_reserve_kbytes 1106-1116; sha256 f81feb3dfca5; copy %svm.rst.v7.3" % (T73, R53),
     "re-checks the sysctl descriptions behind the commit ledger; v7.3 adds panic_on_unrecoverable_memory_failure and drops a mm/swap.c pointer",
     LEDGER),
    ("S508", "Linux mm/util.c at tag v7.3 — %smm/util.c?h=v7.3" % CG, "code", "A",
     "vm_commit_limit, __vm_enough_memory and the policy handler at v7.3",
     "%s; overcommit_policy_handler 806, vm_commit_limit 904-916, __vm_enough_memory 959-1003; sha256 4dfcce2b8fa8; copy %sutil.c.v7.3" % (T73, R53),
     "shows the commit limit and the mode-2 test unchanged at v7.3; the release's util.c edits sit in vm_mmap_pgoff and the shadow-stack helper",
     LEDGER),
    ("S509", "Linux include/linux/mman.h at tag v7.3 — %sinclude/linux/mman.h?h=v7.3" % CG, "code", "A",
     "vm_acct_memory and vm_unacct_memory at v7.3",
     "%s; vm_acct_memory 76, vm_unacct_memory 81; sha256 d7bf787c910d, byte-identical to v7.2; copy %smman.h.v7.3" % (T73, R53),
     "proves the commit charge helpers are byte-identical between v7.2 and v7.3",
     LEDGER),
    ("S510", "Linux mm/mmap.c at tag v7.3 — %smm/mmap.c?h=v7.3" % CG, "code", "A",
     "MAP_NORESERVE handling and the reserve initialisers at v7.3",
     "%s; MAP_NORESERVE block 563-571, init_user_reserve 1566, init_admin_reserve 1587; sha256 8e51fb1c10fe; copy %smmap.c.v7.3" % (T73, R53),
     "shows the MAP_NORESERVE rule kept under the v7.3 vma_flags_set spelling, which is why two round-52 quotes no longer match byte for byte",
     LEDGER),
    ("S511", "Linux mm/mm_init.c at tag v7.2 — %smm/mm_init.c?h=v7.2" % CG, "code", "A",
     "the vm_committed_as batch size by overcommit policy at v7.2 (the host kernel line)",
     "tag v7.2 (237a1c39e8df); mm_compute_batch lines 191-210, mm_compute_batch_init 226-233; sha256 ed691b24afbc; copy %smm_init.c.v7.2" % R53,
     "gives the mode-2 batch rule (0.4 percent of RAM per CPU, floor max(2 x CPUs, 32)) that sizes the commit counter's approximation band",
     "corpus/knowledge/commit-runway-read-r53.md"),
    ("S512", "Linux lib/percpu_counter.c at tag v7.2 — %slib/percpu_counter.c?h=v7.2" % CG, "code", "A",
     "how far a per-CPU counter's global count can lag its sum at v7.2",
     "tag v7.2 (237a1c39e8df); percpu_counter_add_batch lines 93-113 (SMP path); sha256 2c26e67751f9; copy %spercpu_counter.c.v7.2" % R53,
     "shows each CPU folds its local delta into the global count once it reaches the batch, which bounds the read error by batch per CPU",
     "corpus/knowledge/commit-runway-read-r53.md"),
    ("S513", "Linux include/linux/percpu_counter.h at tag v7.2 — %sinclude/linux/percpu_counter.h?h=v7.2" % CG, "code", "A",
     "percpu_counter_read_positive at v7.2 (the read the mode-2 test uses)",
     "tag v7.2 (237a1c39e8df); percpu_counter_read_positive lines 118-126 (SMP); sha256 4a107bc381b3; copy %spercpu_counter.h.v7.2" % R53,
     "shows the mode-2 test reads only the global count, never the per-CPU deltas, so the enforced value is approximate",
     "corpus/knowledge/commit-runway-read-r53.md"),
]


def row_line(r):
    sid, source, kind, tier, scope, anchor, teaches, used = r
    return "| %s | %s | %s | %s | %s | %s | %s | mined | 2026-10-26 | on-release | %s |" % (
        sid, source, kind, tier, scope, anchor, teaches, used)


def table_lines(lane, all_held=False):
    d = C.scope(C.git_reader(lane, C.ENTERING))
    norm = {}
    for path, (copy, _, _) in C.V73.items():
        with open(os.path.join(lane, copy), encoding="utf-8", errors="surrogateescape") as f:
            norm[path] = C.ws(f.read())
    out = ["| h | entry | status | source | quote | disposition |", "|---|---|---|---|---|---|"]
    for h, (entry, path, q72) in sorted(d.items(), key=lambda kv: (kv[1][0], kv[1][1], kv[0])):
        st = "held" if (all_held or q72 in norm[path]) else "absent"
        q = q72 if st == "held" else REPLACE[h]
        out.append("| %s | `%s` | %s | %s | `%s` | %s |" % (h, entry, st, SID[path], q.replace("|", "\\|"),
                                                          DISPOSITION.get(h, "holds")))
    return out


def apply(clone, parts):
    if "ledger" in parts:
        body = ["# Control ledger (round-53 C1 control; not lane data)", "",
                "source: " + ", ".join(sorted(set(SID.values()))), "verified-at: 2026-10-26",
                "recheck: on-release", "", "## Ledger", ""] + table_lines(clone, "allheld" in parts) + [""]
        with open(os.path.join(clone, LEDGER), "w") as f:
            f.write("\n".join(body))
    if "rows" in parts:
        p = os.path.join(clone, "corpus/SOURCES.md")
        lines = open(p).read().split("\n")
        start = lines.index("## Registry")
        last = max(i for i, l in enumerate(lines) if i > start and re.match(r"^ {0,3}\|\s*S[0-9]{3,}\s*\|", l)
                   and i < lines.index("## Paths"))
        lines[last + 1:last + 1] = [row_line(r) for r in ROWS]
        open(p, "w").write("\n".join(lines))
    if "votes" in parts:
        d = C.scope(C.git_reader(clone, C.ENTERING))
        os.makedirs(os.path.join(clone, C.VOTE_DIR), exist_ok=True)
        for v in ("Mo53Fr01", "Mo53Fr02"):
            with open(os.path.join(clone, C.VOTE_DIR, v + ".md"), "w") as f:
                f.write("# synthetic control votes (witness only)\n\n" + "\n".join(
                    "RECHECK %s %s" % (h, DISPOSITION.get(h, "holds")) for h in sorted(d)) + "\n")
    if "v72copies" in parts:
        src = {"proc.rst.v7.3": "corpus/evidence/sources-r51/proc.rst.v7.2",
               "show_mem.c.v7.3": "corpus/evidence/sources-r51/show_mem.c.v7.2",
               "mm_inline.h.v7.3": "corpus/evidence/sources-r51/mm_inline.h.v7.2",
               "vm.rst.v7.3": "corpus/evidence/sources-r52/vm.rst.v7.2",
               "util.c.v7.3": "corpus/evidence/sources-r52/util.c.v7.2",
               "mmap.c.v7.3": "corpus/evidence/sources-r52/mmap.c.v7.2"}
        for name, s in src.items():
            with open(os.path.join(clone, s), "rb") as f:
                b = f.read()
            with open(os.path.join(clone, R53, name), "wb") as f:
                f.write(b)


def main(argv):
    if argv == ["--print-table"]:
        print("\n".join(table_lines(LANE)))
        return 0
    if argv == ["--print-rows"]:
        print("\n".join(row_line(r) for r in ROWS))
        return 0
    if len(argv) != 2:
        print(__doc__, file=sys.stderr)
        return 2
    apply(os.path.abspath(argv[0]), set(argv[1].split(",")))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

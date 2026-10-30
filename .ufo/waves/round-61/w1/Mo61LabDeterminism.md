# Mo61LabDeterminism — selftest repeatability

**Finding:** The tested C1 and C2 selftests were deterministic across three distinct scratch directories each. For each counter, all three complete stdout streams were byte-identical; all cases passed. C2 was invoked with the requested `--floor 1`.

**Commands:** From `/home/vgpnk/Projects/shokunin/mori-shokunin`, with `TMPDIR=/fast/scratch/hyaku/mori-r61/Mo61LabDeterminism`, each iteration used its own directory `.../count-c1-1`, `.../count-c1-2`, `.../count-c1-3`, and likewise for C2:

```sh
python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-61/count-c1.py --selftest --scratch "$d"
python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-61/count-c2.py --selftest --floor 1 --scratch "$d"
```

The loop compared each full captured stdout against the prior run for the same counter. Exact comparison receipts: `count-c1.py BYTE_COMPARE=IDENTICAL`; `count-c2.py BYTE_COMPARE=IDENTICAL`.

**Three outputs (each listed output appeared identically on runs 1, 2, and 3):**

C1:
```text
case good: ok=True want=True pass failed=[]
case missing: ok=False want=False pass failed=['missing:tools/absent.py']
case thin: ok=False want=False pass failed=['thin:tools/h.py:owner']
case noselftest: ok=False want=False pass failed=['noselftest:tools/i.py']
case superseded-ok: ok=True want=True pass failed=[]
case unres: ok=False want=False pass failed=['missing:tools/nothere.py']
C1_SELFTEST pass=6 fail=0
```

C2:
```text
case good: ok=True want=True pass failed=[]
case quote-missing: ok=False want=False pass failed=['quote_missing:a.rst:5-7']
case row-missing: ok=False want=False pass failed=['rows_missing:a.rst:5-7', 'rows_ne_pointers']
case orphan: ok=False want=False pass failed=['rows_orphan:b.c:25', 'quote_words:b.c:25', 'rows_ne_pointers']
case small-span: ok=False want=False pass failed=['span_small:a.rst:5-7']
case dup-quote: ok=False want=False pass failed=['quote_dup:a.rst:9']
case not-mined: ok=False want=False pass failed=['rows_src:a.rst', 'rows_src:b.c', 'rows_src:c.txt', 'rows_src:d.h']
case usedby-miss: ok=False want=False pass failed=['rows_src:a.rst', 'rows_src:b.c', 'rows_src:c.txt', 'rows_src:d.h']
case tampered-copy: ok=False want=False pass failed=['copy_pin:a.rst', 'loc_bad:a.rst:5-7', 'loc_bad:a.rst:9', 'sources_floor']
case no-prov: ok=False want=False pass failed=['provenance']
C2_SELFTEST pass=10 fail=0
```

**Pointers:** C1 deterministic case list, scratch fixture creation and output formatting: `.ufo/waves/round-61/count-c1.py:150-190`. C2 synthetic data/cases, per-case print and tally: `.ufo/waves/round-61/count-c2.py:201-283`.

**Scope/evidence note:** Only these selftest executions were assessed; this does not assert determinism for live counter runs or other environments. Scratch root was removed by the run's exit trap after capturing outputs. No tools installed or project files changed outside this report.

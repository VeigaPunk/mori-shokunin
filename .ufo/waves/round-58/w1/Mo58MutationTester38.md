# Mo58MutationTester38 — frozen registry census

## Method and evidence

Read the frozen contract, `count-c1.py`, and `count-c2.py`; used committed `corpus/SOURCES.md` at `fe8801120a67c1a6b8899d7d0423839caa09e7d0` (not the current working-tree registry). Independent manual row/histogram command:

```sh
git -C /home/vgpnk/Projects/shokunin/mori-shokunin show fe8801120a67c1a6b8899d7d0423839caa09e7d0:corpus/SOURCES.md | python3 -c 'import sys,re,collections; r=[x.rstrip() for x in sys.stdin if re.match(r"\\|\\s*S\\d+\\s*\\|",x)]; print("rows",len(r)); print("tier",dict(sorted(collections.Counter(x.split("|")[4].strip() for x in r).items()))); print("status",dict(sorted(collections.Counter(x.split("|")[8].strip() for x in r).items())))'
```

Output:

```text
rows 322
tier {'A': 290, 'B': 14, 'C': 18}
status {'mined': 270, 'queued': 24, 'rejected': 28}
```

Round-start validator command:

```sh
TMPDIR=/fast/scratch/hyaku/mori-r58/Mo58MutationTester38 /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori
```

Output ended `mori ok /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md`, exit 0. It emitted W04 duplicate-URL warnings; no validation errors. It was run on current on-disk `SOURCES.md`, not the frozen bytes, so only the manual git-show census establishes the freeze-revision count/histograms. Disk guard reported `/fast/scratch/hyaku` 32% used / 551.1G free.

## Finding

No counterexample to the frozen contract's round-start total: independently counted 322 committed source rows, matching its stated 322. Manual histograms are A/B/C = 290/14/18 and mined/queued/rejected = 270/24/28. Bounded census only; no counter mutation or claim about the counter predicates.
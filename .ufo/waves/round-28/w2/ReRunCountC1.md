# ReRunCountC1 — wave 2 falsification of the round-28 C1 counter

Verdict: **breaks** — the C1 freshness claim at attack rev `f2de0eedcd60d2e354da75265ea6122bc3896073` is
`C1=unmet` (superseding row S147 absent); the counter itself is reproducible and its internals check out where
I hand-verified.

## Counter reruns (executed from /tmp, 2026-10-22 ~18:52Z)

`bash .ufo/waves/round-28/count-c1.sh 6ebd518f` →

```
row_identity=rows=144 changed=3 removed=0 bad=0
superseding=0/8 ids=none
fail S145 row_absent ... fail S152 row_absent   (all 8 rows absent)
readers_left=27
C1=unmet
EXIT=1
```

`bash .ufo/waves/round-28/count-c1.sh f2de0eedcd60d2e354da75265ea6122bc3896073` →

```
row_identity=rows=151 changed=0 removed=0 bad=0
superseding=7/8 ids=S096,S097,S127,S128,S129,S131,S140
fail S147 row_absent
readers_left=0
C1=unmet
EXIT=1
```

## Comparison with recorded evidence

- `evidence/c1-before-a1.txt` (measured 2026-10-22T18:06:33Z): my rerun output is **byte-identical line for
  line** — same `rows=144 changed=3`, same 8 `row_absent` fails, `readers_left=27`, `C1=unmet`, exit 1. Counter
  is deterministic and reproducible.
- `evidence/c1-before.txt` (pre-amendment counter, 17:55:46Z): same verdict, lacks per-row fails and
  `readers_left` — consistent with the A1 counter rewrite (contract.md:79-92).
- `evidence/c1-after*.txt`: **does not exist for round 28** (`find` over the lane; only rounds 17-27 have
  `c1-after*` files). The contract's declared after-state "C1=met, exit 0" (contract.md:31) has **no recorded
  evidence**, and at the attack rev it is not true: `C1=unmet`.

## Finding 1 (high): C1 unmet at attack rev — S147 row absent

`git show f2de0eed:corpus/SOURCES.md | grep -c ' S147 '` = 0. S145,S146,S148-S152 rows exist (SOURCES.md lines
151-157 at that rev); S147, the row meant to supersede S101, was never landed — matching wave-1 report list
(`w1/SupersedeS096/S097/S127/S128/S129/S131/S140.md`; no `SupersedeS101.md`). Until S147 lands, `superseding`
can reach at most 7/8 and C1 cannot be met.

## Finding 2 (medium): `readers_left=0` is honest here but the `tsukuroi` filter is fragile

Unfiltered grep of the old ids over the live readers (`SKILL.md PROVINCE.md corpus/README.md corpus/knowledge`)
at f2de0eed returns exactly one line — `corpus/knowledge/oom-victim-selection-r27.md:203`, which the counter's
`grep -v -E 'tsukuroi'` (count-c1.sh:81) silently drops. Hand-check: line 203 reads "Source ids are lane-local
and every bare id here is mori's: tsukuroi S119 is the same v7.2 `mm/oom_kill.c` bytes as mori S003 …; tsukuroi
S115, S118, S120 and S127 are `psi.rst`, `cgroup-v2.rst`, `oomd.conf.xml` and a row for mori's
`system-pressure-r24.md`, **not mori's rows of those numbers**." The dropped hit is a tsukuroi-lane id, not a
mori citation — `readers_left=0` is correct at this rev. Residual risk: the filter is whole-line; any future
reader line that mentions "tsukuroi" anywhere while citing a superseded mori id would be dropped unchecked.

## Hand-checks of rows the counter cannot see

1. **S096, S097, S101 restored byte-equal to first-published — verified stronger than the counter sees.**
   `check-row-identity.py` (frozen at df886be1) compares only non-mutable cells (status/recheck/used-by exempt)
   against each row's first commit (`--full-history --topo-order --reverse`). I ran it at `6ebd518f`: it names
   the three defect rows — `changed S096 cells=teaches`, `changed S097 cells=anchor,teaches`, `changed S101
   cells=teaches`. Then cell-diffed all 13 cells of each row at `f2de0eed` vs its first-published commit
   (S096/S097: `df4db54`; S101: `90ed9b7`): **zero differing cells in all three rows** — even mutable cells
   (status `mined`, used-by) are byte-identical to first publication. Restoration is genuine and total.
2. **S152 Gate sha256 verified against live content.** Gate line: `job-manager.ts` at commit 6962d5cd, access
   2026-10-22T17:59:30Z, sha256 `f8851470a8bd953f25ab659c0d0aac2ea8c34df9a433e154ec4127c7683b70bd`. I fetched
   the same URL 2026-10-22T18:55:41Z: `sha256sum /tmp/jm.ts` = `f8851470a8bd953f25ab659c0d0aac2ea8c34df9a433e15
   4ec4127c7683b70bd` — match. Located quote `job-manager.ts:305` "return Math.max(1, Math.floor(val…" is at
   line 305 of the fetched file. The counter only checks the Gate line's *format* (https + 64-hex + quote); the
   content is honest for this row.
3. **`changed=0` semantics** (counter can't express this): identity check counts only non-mutable-cell drift vs
   first publication, so `changed=0` at the attack rev certifies restoration of the three defect rows AND no
   drift in any of the other 148 rows — verified by direct run (`rows=151 changed=0 removed=0 bad=0`).

## Residual gaps (not verified by me, within time)

- Gate sha/quote content for S145, S146, S148-S151 — only format-checked by the counter (count-c1.sh:69).
- `used_by_not_citing` check (count-c1.sh:44-45) greps each used-by path for the new id's bytes anywhere in the
  file — presence, not citation context; I did not audit each citing line.
- `teaches_unchanged` (count-c1.sh:54) requires only that the new row's teaches differ textually; whether the
  new teaches actually repairs the defect (e.g., S146 cites the man-pages 6.20 tarball, S149 the real scaling)
  is outside the counter and outside my spot check except S152 above.
- The counter's hardcoded MAP (count-c1.sh:17) matches contract.md's eight pairs; it would not notice a
  contract amendment to the map.

## Tooling

None installed — git, python3, curl, sha256sum already present. RULES.md read
(/home/vgpnk/.omp/agent/RULES.md); no installs needed.

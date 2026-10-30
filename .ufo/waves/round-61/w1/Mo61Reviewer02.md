# Mo61Reviewer02 — C2 freeze re-derivation

Axes: freeze fidelity, pointer-set completeness against the frozen enumerator, control reproducibility. Recommendation only; no admission or integration.

## Findings by severity

No actionable mismatch in the assigned freeze/control/checklist comparison. C2 is **unmet**, not a landed freshness capability.

Executed from `/home/vgpnk/Projects/shokunin/mori-shokunin`:

```sh
env TMPDIR=/fast/scratch/hyaku/mori-r61/Mo61Reviewer02 PYTHONDONTWRITEBYTECODE=1 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-61/count-c2.py 7370a731abcafc4c803111de7c22cd6264d63be1 --scratch /fast/scratch/hyaku/mori-r61/Mo61Reviewer02
```

Actual stdout and exit:

```text
C2=unmet pointers=47 rows=0 same=0 moved=0 changed=0 quotes_ok=0 spans_ok=0 sources=0 failed=entry_absent rev=7370a731abcafc4c803111de7c22cd6264d63be1
rc=1
```

Committed control read with:

```sh
git -C /home/vgpnk/Projects/shokunin/mori-shokunin show 7370a731abcafc4c803111de7c22cd6264d63be1:.ufo/waves/round-61/evidence/control-c2-do-nothing.txt
```

```text
C2=unmet pointers=47 rows=0 same=0 moved=0 changed=0 quotes_ok=0 spans_ok=0 sources=0 failed=entry_absent rev=325f7e639916fcbc77fa2ec7475951a1b86bb1cb
rc=1
```

The two stdout lines are exactly equal after replacing their revision with `{REV}`; exit codes also agree. Independently loaded the counter **from `git show` at freeze**, executed its `enumerate_pointers`, `measure(repo, freeze, FLOOR_DEFAULT)`, and `fmt`, and compared to the committed receipt: `committed_control_equal_modulo_rev=True`. Frozen counter SHA256: `82d0fee6124685f8a50f93550f3665703a33dce644948958db642a77d5aec2d8`.

Canonical logic: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-61/count-c2.py:39-40,57-65` defines literal-name extraction and ordered deduplication; `:94-104` enumerates before returning on absent ledger; `:289-301` uses floor 40 by default and formats the result. Thus `entry_absent` alone is the actual early-return diagnostic; no downstream quote/source checks ran. This is compatible with the contract's unmet control, but does not assert `rows_missing` was exercised.

## Pointer-set receipt

Source entry: `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/knowledge/system-pressure-r24.md`, committed SHA256 `26b22ddf38cdd4da2d7846943089d0e4bf2a05db6a00f6556c41b046cf2976f5`. `git show` byte comparison confirms identical entry bytes at entering and freeze revisions. Read-only `git diff 325f7e639916fcbc77fa2ec7475951a1b86bb1cb 7370a731abcafc4c803111de7c22cd6264d63be1 -- corpus/knowledge/system-pressure-r24.md corpus/knowledge/psi-v73-recheck-r61.md` produced no output.

Compared all 47 ordered keys against Mo61ScoutAnchorMap-2's extracted checklist (`POINTER` records in its scratch `pointers.txt`, header `pointers=47 rev=325f7e...`; consulted through read/grep). Exact ordered match, no missing/orphan key. The scout also directly supplied the complete matching 47-key list and normalization caveats via peer message, naming its durable report `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-61/w1/Mo61ScoutAnchorMap.md`. Durable copy of the matching enumeration follows; numbers after `@` are representative source-entry line numbers, not target-copy locations.

```text
psi.rst:60-65 @19
psi.c:342-360 @19
psi.c:1268-1270 @21
psi.c:1372-1373 @23
psi.c:1379-1380 @23
psi.c:1712 @26
psi.c:1017 @32
psi.c:1540 @42
psi.c:1686 @42
psi.rst:36-38 @66
psi.c:1710-1721 @68
Kconfig:730-731 @70
psi.rst:40-43 @75
psi.c:1290-1296 @78
psi.rst:45-56 @81
psi.rst:57-59 @85
psi.c:1282-1288 @87
psi.c:1284-1288 @96
psi.c:160-164 @98
psi.c:1268 @99
psi.c:1269-1270 @100
psi.c:600-602 @101
psi.c:1273-1296 @106
psi.c:1032-1042 @107
psi.c:1364-1367 @109
psi_types.h:41-49 @110
psi.c:1717-1719 @113
psi.c:1260-1263 @116
psi.c:1257-1258 @120
psi.c:228-240 @121
psi.c:149-158 @123
psi.c:1553-1566 @124
psi.c:1711-1719 @126
kernel-parameters.txt:5505-5507 @127
Kconfig:743-760 @127
psi.rst:67-88 @132
psi.rst:102-104 @133
psi.c:167 @134
psi.c:1596-1598 @136
psi.rst:178-187 @142
cgroup-v2.rst:1066-1081 @143
psi.c:408-410 @154
psi.rst:70-88 @160
psi.c:845-857 @225
psi.c:551 @225
psi.c:1538-1550 @241
cgroup-v2.rst:1066-1087 @242
```

## Residual risk and verification gaps

- The 47-key equality is equality to the **frozen regex**, not proof of full semantic citation coverage. Comma shorthand tails are not expanded: entry `:19`, `:89`, `:110`, `:143` contain examples. Historical corrected-away anchors at `:241-242` are nevertheless enumerated. Do not silently add/remove these in the ledger's frozen key set.
- No positive ledger run, quote correctness, source-opening date, pin validation, later integration, runtime routing, saturation, or resume behavior was assessed; the assigned negative run returns before those C2 checks. No capability acquisition claim follows from this receipt.
- LSP unavailable: `read xd://lsp` returned `No such tool`; no server/status/references/definition/diagnostics device was mounted. Direct frozen-source inspection and literal checklist matching are fallback evidence, not semantic LSP proof.
- Disk guard printed `/fast/scratch/hyaku` 57% used, 345.4G free (`/tmp` 97.5G, `/var/tmp` 533.8G free), then timed out while listing top consumers after 30s. No heavy work or ENOSPC occurred; no clone, fixture repo, VCS mutation, production edit, or tool install/update was performed.

Self-evaluation: accuracy 4 (negative-path conclusions only), completeness 4 (compared scout extraction rather than its not-yet-published final report), clarity 4 (47-key receipt adds necessary length), actionability 4 (supports freeze/control decision, not ledger acceptance), conciseness 4 (full enumeration retained for durable evidence); overall 4.0. Improvement: pair this negative control with the separately assigned integrated-ledger review; no broader acceptance is implied. User-alignment self-check: findings stay within the requested freeze/control scope.

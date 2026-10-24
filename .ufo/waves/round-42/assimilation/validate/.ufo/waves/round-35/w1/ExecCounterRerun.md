measured 2026-10-23T08:54:17Z

# ExecCounterRerun — frozen counter reproducibility, MANIFEST freeze hash, independent oracle

Seat: MoriR35.ExecCounterRerun (leaf). Lane repo: /home/vgpnk/Projects/shokunin/mori-shokunin.
Scope: rerun frozen counter in a fresh clone, compare MANIFEST freeze hash, recompute oracle key set independently.

## Artifacts verified before any run

- `sha256sum .ufo/waves/round-35/count-c1.py` → `27b82d71f2f591df1833c8de793201475d8f01735b5ed4edd7b74e389ee18167`, matching `.ufo/waves/round-35/evidence/c1-freeze.txt:2`. Counter unchanged since freeze.
- `git -C /home/vgpnk/Projects/shokunin show 37b51a243302e8009c7067431e8a47f9a722fd14:MANIFEST.json | sha256sum` → `0b414b8a926f44b54f11fedbbc4f9a00ef2075659dcf1e52db5ff57395ae9952`, matching `evidence/c1-freeze.txt:6`. Freeze hash holds.
- Clone: `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone --no-hardlinks <lane> /fast/scratch/hyaku/mori-r35/ExecCounterRerun/clone` → rc=0. All revs the counter needs resolve in it as type `commit`: `dd76eb79ef4f6d39c9c26647a56d3fb607308f8f`, `f2d28711ee723c969b6c2008d32df498192f9e7b`, and the hard-coded `FIRST_PREV` `20e2255` (`count-c1.py:32`).

## Runs (frozen counter, `--repo <clone>`, fleet MANIFEST read from its default root)

Command shape: `timeout 300 python3 <lane>/.ufo/waves/round-35/count-c1.py <rev> --repo /fast/scratch/hyaku/mori-r35/ExecCounterRerun/clone`

| rev | run | exit | stdout lines | stderr bytes | stdout sha256 |
|---|---|---|---|---|---|
| dd76eb79 | 1 | 1 | 24 | 0 | 8633ae8ff78040f225c24eb753c1af608244c4300b56c67dd2efe271e168aa86 |
| dd76eb79 | 2 | 1 | 24 | 0 | 8633ae8ff78040f225c24eb753c1af608244c4300b56c67dd2efe271e168aa86 |
| f2d28711 | 1 | 1 | 24 | 0 | 19325c49eb5bd7219f827c91f41dda996e922944184d61e028d458d22b9d82ac |
| f2d28711 | 2 | 1 | 24 | 0 | 19325c49eb5bd7219f827c91f41dda996e922944184d61e028d458d22b9d82ac |

Both revs end in the same summary:
`label=P-C1 rev=<full> manifest_rev=37b51a243302 register='## Capabilities (round 12 demonstrations)' oracle=18 rows=5 matched=0 missing=18 bad=0 extra=5 mismatches=23 C1=unmet`

Diffs:
- dd76 run1 vs run2: identical (`diff` empty).
- f2d run1 vs run2: identical.
- dd76 vs f2d: differ only at line 24, the `rev=` field; lines 1–23 identical.
- The identical result across revs is structural, not cached: `git -C clone diff --quiet dd76eb79 f2d28711 -- SCORECARD.md` → rc=0, and `git diff --stat dd76eb79 f2d28711` shows f2d adds only round-35 files (contract.md, count-c1.py, 4 evidence files).

Output shape: 5 `row <name> extra` lines (the five round-12 data rows `source registry`, `live census`, `census self-test`, `silence oracle`, `drift pin`; the `Capability` header is dropped by `register_rows`), then 18 `row rounds[N].capabilities_added[M] missing` lines sorted.

## Determinism probes (same clone, no cache between runs)

- `PYTHONHASHSEED=0`, `=1`, `=12345` at dd76eb79: all rc=1 and identical sha `8633ae8f…`; also byte-identical to the unseeded run. No hash-order leakage.
- Full 40-hex revs instead of 8-hex at both revs: byte-identical to the abbreviated-rev outputs.
- Clone read-only: `git -C clone status --porcelain` → 0 lines after all runs.

## Cross-check against pre-data control receipt

`evidence/c1-before.txt` line 1 is a comment; lines 2–25 are the recorded dd76eb79 stdout. `cmp` of those 24 lines against my `out-dd76eb79-1.txt` → identical. Line 26 records `exit=1`, matching my exit. This independently reproduces the recorded control-1 baseline.

## Independent oracle recomputation

Script: `/fast/scratch/hyaku/mori-r35/ExecCounterRerun/oracle_indep.py` (80 lines, does not import count-c1.py; reads MANIFEST.json@37b51a24 via read-only `git show`, filters `lane=="mori"` and `admitted is True` and non-empty `capabilities_added`, emits `rounds[i].capabilities_added[j]`, then checks each entry commit exists in the clone).

Result: `mori_entries=23 admitted_with_caps=12 oracle_keys=18`, `unresolved_commits=0`.
Manifest structure (525 rounds total): 23 mori entries, 13 admitted, 12 admitted-with-caps, 1 admitted-with-no-caps (round 21, index 412), 1 non-admitted-with-caps (round 17, index 372). Those two edge entries are the discriminating cases: the oracle excludes both, and neither key appears in the counter output.
Per-entry capability counts: `[(12,1),(14,1),(15,1),(16,1),(18,3),(19,1),(22,1),(24,2),(25,2),(26,1),(28,2),(31,2)]` — sums to 18.

Set comparison: independent 18 keys vs the counter's 18 `missing` keys at dd76eb79 → `diff` empty (IDENTICAL); same vs f2d28711 → IDENTICAL.

## Reproducibility prerequisites and risks (non-blocking)

- `--repo <clone>` is not self-contained: the counter still reads MANIFEST.json and report bodies from the hard-coded fleet default at `count-c1.py:96` (`/home/vgpnk/Projects/shokunin`) unless `--fleet` is passed (`count-c1.py:100-101`). My runs used the lane clone for SCORECARD/tree/oracle commits and the fleet repo (read-only) for the manifest, which is the frozen invocation the contract cites. A runnable reproduction therefore requires both the lane clone and the fleet repo at 37b51a24; this is a portability caveat, not a wrong result.
- `FIRST_PREV` is a hard-coded abbreviation (`count-c1.py:32`); it resolves in the clone today but is a hidden dependency on that object remaining reachable.
- No time-dependence observed in outputs; no writes performed by the counter.

## Verdicts

VERDICT: counter reproducibility — no defect found (2/2 revs × 2 runs, identical repeats, exit 1, byte-identical to the recorded baseline)
VERDICT: MANIFEST.json@37b51a24 freeze hash — holds (0b414b8a… equals c1-freeze.txt)
VERDICT: independent oracle vs counter missing list — no defect found (18-key sets identical at dd76eb79 and f2d28711)

## Cleanup

No background processes started; no installs; all writes confined to /fast/scratch/hyaku/mori-r35/ExecCounterRerun/ and this report. No lane, fleet or jj state mutated.

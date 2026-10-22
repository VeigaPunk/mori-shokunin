agree — the frozen A3 gate caught all seven planted leak probes and passed both false-positive controls; the deliberate broad-URL-allowlist mutant was killed.

# Scope and detector
Used the frozen gate from `db1ec469` in the isolated clone `/fast/scratch/hyaku/mori-r30-w2/MutGateA3/sandbox`; `git rev-parse` returned `db1ec4694242a9c1acef03fef2852c7e943b1ed7`. Synthetic reports were committed in that clone at `cc9c66e747ea49a84aa5a3d455e387261e55f6b0` (the URL mutant control used the earlier report commit `6d5b4c8349303a2d3a975687a9c335b49b602a2e`). No lane source was changed.

Relevant frozen-gate behavior: the URL allowlist is at `check-blind-wave.sh:12-24`, path-entry parsing at `:27-52`, citation patterns at `:76-78` and their report at `:121-123`, heading/list parsing at `:112-131`, selftest-output detection at `:135-150`, missing/forbidden-list checks at `:156-165` (all paths relative to `.ufo/waves/round-30/`).

The per-probe invocation was:

```sh
if bash .ufo/waves/round-30/check-blind-wave.sh cc9c66e747ea49a84aa5a3d455e387261e55f6b0 .ufo/waves/round-30/w2 '^PROBE_NAME[.]md$'; then printf 'exit=0\n'; else rc=$?; printf 'exit=%s\n' "$rc"; fi
```

Each selector below replaced `PROBE_NAME`; output is the actual gate output (one report scanned per run).

| Probe / planted content | Output | Result |
|---|---|---|
| Lane script path, report `ProbeLaneScript.md:2` | `scanned=1; blind_violations=1; .ufo/waves/round-30/w2/ProbeLaneScript.md:2:writer-forbidden-opened-path; exit=1` | Caught |
| Lane fixture path, `ProbeLaneFixture.md:2` | `scanned=1; blind_violations=1; .ufo/waves/round-30/w2/ProbeLaneFixture.md:2:writer-forbidden-opened-path; exit=1` | Caught |
| Non-allowlisted raw GitHub lane-repo URL, `ProbeLaneRawURL.md:2` | `scanned=1; blind_violations=1; .ufo/waves/round-30/w2/ProbeLaneRawURL.md:2:writer-forbidden-opened-path; exit=1` | Caught |
| Fleet-root path, `ProbeFleetRoot.md:2` | `scanned=1; blind_violations=1; .ufo/waves/round-30/w2/ProbeFleetRoot.md:2:writer-forbidden-opened-path; exit=1` | Caught |
| Tool line citation, `ProbeToolCitation.md:5` | `scanned=1; blind_violations=1; .ufo/waves/round-30/w2/ProbeToolCitation.md:5:writer-tool-source-citation; exit=1` | Caught |
| Selftest marker line, `ProbeSelftestMarker.md:5` | `scanned=1; blind_violations=1; .ufo/waves/round-30/w2/ProbeSelftestMarker.md:5:writer-tool-run-output; exit=1` | Caught |
| Empty `## Files opened` list, `ProbeEmptyList.md:1-4` | `scanned=1; blind_violations=1; .ufo/waves/round-30/w2/ProbeEmptyList.md:1:writer-missing-files-opened-list; exit=1` | Caught as missing list |
| Benign prose after an allowed list entry, `ProbeProseFalsePositive.md:2-3` | `scanned=1; blind_violations=0; exit=0` | No false positive |
| Heading variant `## Opened Files` with an allowed entry, `ProbeHeadingVariant.md:1-2` | `scanned=1; blind_violations=0; exit=0` | No false positive |

# Mutation probe and restoration
Mutant: on the scratch copy only, broadened the raw GitHub allowlist at frozen `check-blind-wave.sh:16` from the named earlyoom raw host/path to `https://raw.githubusercontent.com/*`. Expected detector: the same raw-URL report must produce a forbidden-path violation. The identical report selector and commit were run with pristine, mutant, and restored script bytes:

- Pristine: `scanned=1; blind_violations=1; .ufo/waves/round-30/w2/ProbeLaneRawURL.md:2:writer-forbidden-opened-path; exit=1`.
- Mutant: `scanned=1; blind_violations=0; exit=0` — the mutant let the leak through, so the probe killed it.
- Restored: `scanned=1; blind_violations=1; .ufo/waves/round-30/w2/ProbeLaneRawURL.md:2:writer-forbidden-opened-path; exit=1`.

`sha256sum .ufo/waves/round-30/check-blind-wave.sh` before mutation: `a3c85d9d988ad98b3a8042015b972d2051cf08f884c76bc937aed533ee9f3e44`; mutated: `97388f6f1b4b17c6a9229182d3f806f8c9cdb847b5e02fa78b88608b1f75e794`; after restoration: `a3c85d9d988ad98b3a8042015b972d2051cf08f884c76bc937aed533ee9f3e44`. Thus the restored bytes match the recorded pre-mutation hash.

# Baseline and run notes
The exact pristine no-match baseline was `bash .ufo/waves/round-30/check-blind-wave.sh db1ec469 .ufo/waves/round-30/w1 '^ProbeLaneRawURL[.]md$'`: `scanned=0`, `blind_violations=0`, `exit=0`. An earlier broad baseline selector `'^Probe.*[.]md$'` selected the pre-existing `ProbeC1Cases.md` in `w1` and returned `scanned=1`, `blind_violations=1`, `.ufo/waves/round-30/w1/ProbeC1Cases.md:1:writer-missing-files-opened-list`, `exit=1`; that run is inconclusive and was not counted as a mutant kill. The exact selector then gave the clean baseline above.

The selftest-marker case is a planted report line, not an invocation of the gate's `--selftest` mode (`check-blind-wave.sh:168-232`). No tool was installed or updated.
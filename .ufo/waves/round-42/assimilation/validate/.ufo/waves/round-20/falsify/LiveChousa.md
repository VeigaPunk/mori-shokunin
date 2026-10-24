# LiveChousa — C2 falsify, lane chousa-shokunin

VERDICT: **HOLDS**

C2 scan accuracy on chousa survives the attack. The live tool run, the wave-1 manual ground truth, and the committed fleet snapshot agree on every compared field; zero differences required explanation. Exit code 1 is the tool's documented contract, not an error, and the committed snapshot recorded the same exit 1.

## 1. Command under test (run 2026-10-21 ~08:00:58 -03)

```
python3 /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-wave-settlement.py scan \
  --lane-root /home/vgpnk/Projects/shokunin/chousa-shokunin \
  --fleet-root /home/vgpnk/Projects/shokunin \
  --out /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-20/falsify/LiveChousa/scan.json
```

Exit code **1**; stdout payload written to `scan.json` (9849 bytes, mtime 08:00:58.747 -03). Read-only on the lane: no lane file mtime changed (§4).

Result: totals `members 136, present 120, missing 16, misrooted 0, stub 0, empty 0, unparsed 0, unsafe 0, waves 2, ignored_json 11, unreadable_json 0, states {partial:1, settled:1}, unique_dispatch_sha256 2, name_hinted_waves 0`.

## 2. Three-way agreement (per dispatch file and lane totals)

| field | live scan | GT (build/GtLaneChousa.md §1–§2, §5) | snapshot (evidence/c2-live-fleet.json:209-221) |
|---|---|---|---|
| dispatch files | round-25/build-dispatch.json, round-25/falsify-run.json | same 2 of 13 JSON | waves 2 |
| build sha256 / state | 218d4c6a…44dc / settled | same sha / settled | (lane aggregate only) |
| build counts | 68 members, 68 present, 0 missing | 68 / 68 / 0 | — |
| falsify sha256 / state | b43ec155…77d7 / partial | same sha / partial | — |
| falsify counts | 52 present, 0 empty, 16 missing | 52 / 0 / 16 | — |
| lane totals | 120 / 0 / 16, misrooted 0, stub 0 | same | members 136, present 120, missing 16, misrooted 0, empty 0, waves 2 |
| trailers | unparsed 0, unsafe 0 | 136 parsed / 0 | unparsed 0, unsafe 0 |
| misc | ignored 11, unreadable 0, name-hint 0 | 13 JSON, 11 ignored | unreadable_json 0 |
| exit | 1 | n/a (manual) | `"exit": 1` (line 209) |
| missing set | 16 names | identical 16 names (GT §5) | count 16 |

**Differences: none.** Nothing to attribute to live lane change or tool error.

## 3. Exit code 1 is contract, not tool error

`tools/mori-wave-settlement.py:366`: `rc = 0 if all(wave["state"] in ("settled", "no-spawn") for wave in waves) else 1`. chousa's falsify wave is `partial`, so 1 is the specified outcome; 2 is reserved for unreadable lane/out (`:672-674`, `:676-680`); `main` returns `scan_lane`'s rc (`:671`, `:682 sys.exit(main())`). The committed snapshot independently recorded `"exit": 1` for chousa (c2-live-fleet.json:209).

## 4. Independent re-derivation (not trusting the tool's self-report)

Using `/usr/bin/jq` (jq 1.8.2) against the dispatch files and `stat`:

- Trailer rule (last non-empty line = `^Report: write your scoped findings to \S+$`): falsify 68 match / 0 non-match; build 68 / 0 → unparsed 0 confirmed.
- Existence (xargs stat of all 136 trailer paths under the lane root): falsify 52 exist / 16 `No such file`; build 68 / 0 → present 120, missing 16 confirmed.
- Zero-byte present files: 0 in either wave → empty 0 confirmed.
- Sub-1000-byte present files: 0 → none can hold `STUB_CONTENTS` (15/16 bytes, tool :35) → stub 0 confirmed.
- Misrooted: the 16 missing paths stat'ed at `/home/vgpnk/Projects/shokunin/<rel>` → 16 `No such file` → misrooted 0 confirmed.
- JSON census: 13 `*.json` under `.ufo/waves`, 2 with top-level schema `ufo-swarm-wave-dispatch-v1` → ignored 11, unreadable 0 confirmed (matches GT §3).
- Missing-16 name set in my scan.json equals GT §5 exactly (FxCapR17/18/21/23, FxConnectSeparability, FxFrontierR12R13/14R15/16R17, FxMetaDirectory/Recheck/Root/Schedule, FxRegistryAppend, FxSkillCurrent, FxSrcFAIR, FxSrcProvO).

Freshness: dispatch mtimes 2026-10-21 02:58:00.243 (build) and 04:37:16.111 (falsify); snapshot c2-live-fleet.json mtime 07:46:53.060; `find chousa-shokunin/.ufo/waves -type f -newermt '2026-10-21 07:46:53'` → empty. No lane wave file changed between snapshot and my run, so live==snapshot is expected, and live==GT with identical dispatch sha256s closes the loop.

## 5. Findings by severity

None. No defect found in the tool's chousa output; no unexplained difference; no evidence of misclassification (missing≠dead honored: the 16 are `missing`, matching GT's [INFERENCE]-flagged contract reading).

## 6. Residual risk and verification gaps

- The committed snapshot stores lane aggregates only (no per-dispatch rows), so the per-file columns rest on the manual GT plus my independent re-derivation above — both agree with the tool.
- "No live lane change" is verified only under `chousa-shokunin/.ufo/waves` in the window 07:46:53→08:01 -03; the counted artifacts all live there.
- Two bash probes returned exit 1 from `grep -c` finding zero matches (expected counts 0); not tool errors.
- `mori-census.sh` not run (my item does not call for it). No tool installs or updates performed; no pacman transactions. Only writes: this report and `falsify/LiveChousa/scan.json`.

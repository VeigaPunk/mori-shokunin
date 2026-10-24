BROKEN: "C2 needs no C1 artifact" fails. "C1 needs no C2 artifact" HOLDS.
Scope: causal separability, C1 (drift freshness) vs C2 (per-seat settlement), round 20. Leaf seat, no subagents.

METHOD AND BOUNDS
- Grep/read on named files; sha256sum, stat, find; jq over dispatch JSON under .ufo/waves/ (report paths only); Python replica of the tool's discovery walk (paths and counts only); tool run on /tmp copies only (/tmp/sepcheck-r20). No lane file written. Census not run. Forbidden dirs untouched. No installs (python3 stdlib, /usr/bin/jq 1.8.2).
- Files changed during the review, so verdicts are pinned to these hashes:
  tools/mori-wave-settlement.py 203c716e (28880 B, 08:11:12); earlier e5c06dad (08:04:26)
  corpus/evidence/drift-classification-r20.json e3a923cc (18431 B, 08:11:23)
  corpus/evidence/baseline-r20-20261021T1051Z.json e528bc15 (07:54:21)
  .ufo/waves/round-20/evidence/c1-drift-entering.json 91397955 (07:22:34)
  .ufo/waves/round-20/evidence/c1-pin-probe-scratch.json 33027b82 (07:26:28)
  .ufo/waves/round-20/build/OracleHarness/c2-oracle.py 2a0da4c8 (07:46:29)
  .ufo/waves/round-20/frozen/c2-expected.json 09848069 (07:23:14)
  tools/mori-census.sh 87b8d680 (2026-10-20 17:39; equals census_sha256 in both C1 files)

CLAIM 1 - C1 needs no C2 artifact: HOLDS
1. The classification and the baseline name no mori-wave-settlement, c2-*.json, c2-oracle, OracleHarness or frozen/. Text only: classification:211 "not settlement evidence" and "FR3 frontier" (labels, not inputs). [INFERENCE] token classes come from census/fleet state in the reason fields, not from C2 output.
2. census_sha256 covers only the census script: census:282 (SELF), :379 (sha256sum "$SELF"), :2926. The tool's bytes appear in no C1 artifact.
3. The census never reads the lane's waves: LANE_ROOT only derives DEFAULT_ROOT (census:288-291, *-shokunin basename -> fleet parent); WAVES_DIR (:303) = /home/vgpnk/Projects/shokunin/.ufo/waves (baseline line 9); probe_waves reads its depth-1 directories (:866-876).
4. The counting command reads only the DRIFT capture and REG (contract:36-41).

CLAIM 2 - C2 needs no C1 artifact: BROKEN
A. Verdict via wave membership (observed). round-20/wave1-run.json (dispatch schema; a mixed C1/C2 wave) names 14 C1 seats as members: 12 Tok* reports, VolatileContract, C1Critic (round-20/build/). c2-live-mori.json (07:46:42): that wave is state "partial", present 70, stub 6, and the stubs include three C1 seats (TokPathAge, TokSilenceA, VolatileContract). The tool reads report bytes when size <= 16 (tool:230-232), so C1 seat output enters the C2 verdict. TokPathAge.md (53 lines) and VolatileContract.md (170 lines) now have full content, so the figure has moved with C1 progress (TokSilenceA not rechecked). wave2-run.json (falsify wave) lists CountC1.md and CriticC1Claim.md as members.
B. Counters via discovery (observed). The tool walks every regular *.json under <lane>/.ufo/waves/ (tool:113-122; contract:64-66). Non-dispatch JSON -> ignored_json (tool:334-335); unparseable -> unreadable_json (:327, :332). C1-lineage files under that root: round-20/evidence/c1-drift-entering.json (ignored); round-20/evidence/c1-pin-probe-scratch.json (C1 text pin output named .json -> unreadable); round-13/evidence/drift-classification.json (r13 register) and drift-retained-baseline.json (ignored); census-named round-13..19 JSON. Replica: 44 drift/census/baseline/register/pin-named files. c2-live-mori.json: ignored_json 472, unreadable_json 2; both named C1 files predate that scan (07:22, 07:26). The contract mandates these counters (contract:82-86).
C. Schema gate (latent). The verdict depends only on the schema string (tool:334). Fixtures built from copies of the real files (/tmp/sepcheck-r20):
   W0 wave only                  rc 0  waves 1  present 1  ignored 0  unreadable 0
   W1 + c1-drift-entering        rc 0  same verdict  ignored 1
   W2 + W1 + r13 register        rc 0  same verdict  ignored 2
   W3 + truncated C1 copy        rc 0  same verdict  ignored 0  unreadable 1
   W4 C1 copy with dispatch schema  rc 1  waves 2  states {settled 1, unavailable 1}
   No C1 file carries that schema (replica before 08:08: none of the 14 dispatch-schema files).
D. Oracle: HOLDS. c2-oracle.py reads only frozen/c2-expected.json (:393) and builds fixtures in a temp sandbox (:51, :160-164, :340-351). It names no census, baseline, register or C1 file. The 14 frozen cases cannot see A-C.

ANSWERS TO THE QUESTIONS ASKED
- Does drift-classification-r20.json or baseline-r20 depend on mori-wave-settlement.py? No.
- Does the tool or oracle read the census? Oracle: no. Tool: not the census script or census output; yes for census-named JSON under .ufo/waves (B).
- Baselines? Tool: not corpus/evidence/baseline-r10/r20; yes for round-13 drift-retained-baseline.json (B). Oracle: no.
- Register? Tool: not corpus/evidence/drift-classification-r20.json; yes for round-13 drift-classification.json and c1-drift-entering.json (B). Oracle: no.

CONTRACT SENTENCE (contract.md:108-109)
- "C1 ... does not need the C2 tool": HOLDS. "C2 needs no new baseline and no census change": HOLDS (census hash unchanged; no corpus reads).
- "Each is verifiable with the other reverted": BROKEN for live output (C1 JSON moves the counters; C1 seat reports move wave-1 counts). Holds only for the 14 sandboxed frozen cases.

SAME CHANNEL, NOT C1 (for the judge)
- round-20/falsify/SentinelTool/probe-20261021/{lane/.ufo/waves/round-1/dispatch.json, outside/secret.json} carry the dispatch schema, so a live scan counts them as waves. round-17/fixtures/seat/NonJsonlIgnored/other.json is unparseable.
- JSON files under .ufo/waves: 626 (replica, before 08:08) -> 683 (find, 08:09:07). Live counters are time-varying.

OPTIONS (not applied; judge decides)
1. Narrow C2 discovery (dispatch-named files, or exclude evidence/, build/, frozen/), or move C1 JSON out of .ufo/waves/. Rename c1-pin-probe-scratch.json (it is text).
2. Or keep the walk and state the live coupling in contract.md:108-109. Do not present wave-1's live figure as C2-only: 14 of its members are C1 seats.

GAPS
- Not run: the tool on the real lane, census, oracle, selftest. Live figures come from c2-live-mori.json (07:46:42) and the replica; replica equivalence rests on W0-W4 and tool:113-122, 319-335.
- [INFERENCE] the 07:46 unreadable pair is the two named files (mtime of the round-17 file not checked).
- Tool and classification changed during review; discovery and counter lines were re-checked in tool 203c716e.

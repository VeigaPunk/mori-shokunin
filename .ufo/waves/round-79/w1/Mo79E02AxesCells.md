# Mo79E02AxesCells — C2 data walk

## 1. Scope and inspected bytes

Produced candidate Last change cells and an insertion paragraph only; did not edit SCORECARD.md, MANIFEST.json, the counters, or other lane files. Axes named: coverage, operability, depth, freshness, calibration, adjacency. Calibration is the claimed move; no score, operability, or freshness move is claimed by this seat.

Read contract C2, SCORECARD.md lines 1–40 and 3924–3989 (round 78), QUALITY.md criteria 159/161/162/163, and SKILL.md registry lines 1290–1325 using the read tool. Read the complete six axes rows verbatim with:

```text
read /home/vgpnk/Projects/shokunin/mori-shokunin/SCORECARD.md:10-15:raw
```

Observed leading rounds were **47/51/51/28/50/19**, not the contract's descriptive before-state **47/47/49/28/50/19**. The frozen predicate itself is unaffected: it compares each axis to the latest admitted improved/harmed closure, not that descriptive list. No symbols were changed; no LSP tool is available in this seat's tool inventory.

## 2. Independent manifest derivation

Command executed (no counter import, no contract-derived numbers):

```sh
python3 -c 'import hashlib,json,pathlib,subprocess; p=pathlib.Path("/home/vgpnk/Projects/shokunin/MANIFEST.json"); b=p.read_bytes(); data=json.loads(b); axes=("coverage","operability","depth","freshness","calibration","adjacency"); rows=[r for r in data["rounds"] if r.get("lane")=="mori" and r.get("admitted") is True and isinstance(r.get("round"),int) and r["round"]<=78]; print("\n".join("{} {} {}".format(a,*max((r["round"],r["verdicts"][a]) for r in rows if r.get("verdicts",{}).get(a) in ("improved","harmed"))) for a in axes)); print("admitted_rows={}".format(len(rows))); print("manifest_sha256="+hashlib.sha256(b).hexdigest()); rev=subprocess.check_output(["git","-C","/home/vgpnk/Projects/shokunin","rev-parse","HEAD"],text=True).strip(); print("fleet_revision="+rev); committed=subprocess.check_output(["git","-C","/home/vgpnk/Projects/shokunin","show",rev+":MANIFEST.json"]); print("manifest_equals_revision="+str(b==committed).lower())'
```

Six-line table and provenance output (rc 0):

```text
coverage 56 improved
operability 78 improved
depth 76 improved
freshness 78 improved
calibration 78 improved
adjacency 19 improved
admitted_rows=46
manifest_sha256=86a82240bbb183b17811b9974de1cad83bd9c58a9b2f84a2a4b310a9d373f1b7
fleet_revision=37c313715318eea4a59d30ffae5f77c28301ec72
manifest_equals_revision=true
```

These maxima agree with the contract and counter. Independent derivation matters because the contract's numbers could have omitted an admitted row, included a rejected row, ignored a harmed verdict, or become stale against a changed fleet record; those are possible failure modes, not observed errors. The observed error is confined to the contract's descriptive current-round list for operability and depth. The equality line binds the manifest bytes actually read to the named fleet revision.

## 3. Initial counter observation

Command executed with scratch explicitly confined:

```sh
HYAKU_SCRATCH=/fast/scratch/hyaku/mori-r79/Mo79E02AxesCells python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-79/count-c2.py 84c6cbc3b47c536a504aaee329c77897d389935e
```

Output, rc 1 (predicate unmet, not setup failure):

```text
axis coverage cell=round_47_improved expect=round_56_improved state=mismatch
axis operability cell=round_51_improved expect=round_78_improved state=mismatch
axis depth cell=round_51_improved expect=round_76_improved state=mismatch
axis freshness cell=round_28_improved expect=round_78_improved state=mismatch
axis calibration cell=round_50_improved expect=round_78_improved state=mismatch
axis adjacency cell=round_19_improved expect=round_19_improved state=ok
C2=unmet axes=6 mismatches=5 errors=0 rows=46 through=78 rev=84c6cbc3b47c
```

## 4. Candidate cells and insertion paragraph

Also written to `.ufo/waves/round-79/w1/Mo79E02AxesCells-cells.md` for integration. Prepending the new clause retains the entire current cell, including its old leading clause; every existing clause after the first semicolon remains byte-for-byte. Adjacency remains unchanged (annotation is not cell text).

| axis | current cell | proposed cell |
|---|---|---|
| coverage | round 47 (improved, score held); round 26 (improved, score held) before the round-50 correction | round 56 (improved, score held); round 47 (improved, score held); round 26 (improved, score held) before the round-50 correction |
| operability | round 51 (improved, score held); round 47 (improved, score held); round 31 (improved, score held) before the round-50 correction; round-37 C2 re-attributed here (score held, 7) | round 78 (improved, score held); round 51 (improved, score held); round 47 (improved, score held); round 31 (improved, score held) before the round-50 correction; round-37 C2 re-attributed here (score held, 7) |
| depth | round 51 (improved, score held); round 50 (improved, score held); round 49 (improved, score held); round 31 (improved, score held) before the round-50 correction | round 76 (improved, score held); round 51 (improved, score held); round 50 (improved, score held); round 49 (improved, score held); round 31 (improved, score held) before the round-50 correction |
| freshness | round 28 (improved, score held); round-37 C2 is re-attributed to operability (round-38 axes-cell correction below) and round 38 claims no freshness move | round 78 (improved, score held); round 28 (improved, score held); round-37 C2 is re-attributed to operability (round-38 axes-cell correction below) and round 38 claims no freshness move |
| calibration | round 50 (improved, score held); round 49 (improved, score held); round 25 (improved, score held) before the round-50 correction; round-37 claim C1 closed the r36 measurement-discrimination defect and states no new number | round 78 (improved, score held); round 50 (improved, score held); round 49 (improved, score held); round 25 (improved, score held) before the round-50 correction; round-37 claim C1 closed the r36 measurement-discrimination defect and states no new number |
| adjacency | round 19 (improved, score held) | round 19 (improved, score held) |

Adjacency: **unchanged**.

Draft for insertion after the r50 correction (prospective integration text, not a claim that SCORECARD has already changed):

Round-79 correction (C2, calibration): at entering revision `84c6cbc3b47c536a504aaee329c77897d389935e`, 5 of 6 Last change cells disagreed with the latest admitted mori closures through round 78 in fleet `MANIFEST.json` at `37c313715318eea4a59d30ffae5f77c28301ec72`; adjacency alone was already right (round 19, improved). Coverage, operability, depth, freshness and calibration now lead with rounds 56, 78, 76, 78 and 78 respectively (all improved), retaining the full older cell text after a `;`; scores and Evidence pointers are unchanged. "Last change" here means the latest admitted closure grading the axis improved or harmed, not the latest score move.

## 5. Final entering-state control and cleanup

Final counter execution, after candidate writing, via `bash -c` with the following exact program:

```sh
S=/fast/scratch/hyaku/mori-r79/Mo79E02AxesCells; trap 'rm -rf -- "$S"; printf "scratch_cleanup_rc=%s\n" "$?"' EXIT; HYAKU_SCRATCH="$S" python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-79/count-c2.py 84c6cbc3b47c536a504aaee329c77897d389935e; rc=$?; printf 'counter_rc=%s\n' "$rc"; exit "$rc"
```

Output (shell rc 1):

```text
axis coverage cell=round_47_improved expect=round_56_improved state=mismatch
axis operability cell=round_51_improved expect=round_78_improved state=mismatch
axis depth cell=round_51_improved expect=round_76_improved state=mismatch
axis freshness cell=round_28_improved expect=round_78_improved state=mismatch
axis calibration cell=round_50_improved expect=round_78_improved state=mismatch
axis adjacency cell=round_19_improved expect=round_19_improved state=ok
C2=unmet axes=6 mismatches=5 errors=0 rows=46 through=78 rev=84c6cbc3b47c
counter_rc=1
scratch_cleanup_rc=0
```

This is the **entering-state control**, not an after-state result: proposed cells are not already present at the frozen entering revision. It does not prove anything about an unmeasured later revision or a concurrently edited working tree. No landed-state checks, builds, tests, linters, formatters, selftests, or fixture commits were run. L1 should integrate the five changed cells and paragraph, then run the frozen C2 counter against the landed revision; this seat does not assert that unrun result.

## 6. Own defects, limits, and handoff

1. Initial scratch setup used a bash tool `name` unnecessarily, creating a supervised finite service instead of an ordinary finite command. The tool reported pid 3646806 and later exit code 0. The setup command was `mkdir -p /fast/scratch/hyaku/mori-r79/Mo79E02AxesCells && ls -la /fast/scratch/hyaku/mori-r79/Mo79E02AxesCells && wc -c /home/vgpnk/Projects/shokunin/MANIFEST.json`; its listing/size output was not retained here and supports no findings. Subsequent calls omitted the service name. No deliberate background jobs or child agents were started; the tool automatically backgrounded two finite calls on an incoming message and delivered their completed results.
2. Initial scratch creation omitted an EXIT trap. Caught while preparing the final control; final command installed the required trap and removed the exclusive scratch directory with rc 0. No scratch tree is intentionally retained.
3. Initial response unnecessarily exposed verbose planning before action. Subsequent work used tools directly; no substantive data was inferred from that planning.
4. No tool installations, host changes, credentials, session material, mutating git commands, or external remediation. Only two assigned markdown deliverables were written. Counter output is scoped to the entering commit and live manifest bytes above; L1 owns integration and landed verification.

Self-evaluation: accuracy 4/5 (landed behavior intentionally unmeasured); completeness 5/5 (six cells, both requested controls, provenance and paragraph supplied); clarity 4/5 (long exact command is necessary but dense); actionability 5/5 (separate ready-to-integrate candidate file); conciseness 4/5 (table and control output duplicated as explicitly requested). Overall 4.4/5. Critical issues: none. Self-check: evidence supports the candidate and entering-state mismatch only, not a landed pass. Improvement: L1's post-integration counter supplies the missing landed-state evidence.

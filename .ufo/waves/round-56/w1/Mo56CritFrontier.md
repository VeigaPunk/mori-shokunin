# Mo56CritFrontier — frontier-step attack (round 56 w1)

seat: Mo56CritFrontier (mori lane, leaf critic; no subagents dispatched)
measured: freeze tip T = 8be2717b0809281d07dffe83dad424a4859e0747; entering tip E = 5b295eeebd87ebd610d8d39bfe2035742f740cfa; data commits c419fe6d, 6ced9da9; freeze commit 3f494b49; HEAD at acc62f54 (w1 dispatch commits, not measured)
scratch: /fast/scratch/hyaku/mori-r56/Mo56CritFrontier (removed at exit; cited bytes copied here)
convention: "frozen fix" = the round-55 lesson's routed-defect 1/2 fixes restated in the round-56 contract ("paste census-mode output (which prints mori rows N) or the counting command"; "receipts here stamp the measured revision themselves").

## (a) Mined-mistake class — verdict: RIGHT class; the alternative was already mined as C2 itself

The vote-emission format mistake was not available to mine as the frontier mistake, because the round already mined it — as claim C2. Evidence:

- contract.md "Frontier and routed defects": "Carried planned item: the voter final-output format rule is implemented as the dual-shape binder (C2), not as a seat-format rule."
- corpus/knowledge/vote-binding-r56.md "## The failure class" is the vote-emission mistake verbatim: round-55 C1 "unmet on its vote arm with every data arm green", all fifteen reporting RECHECK voters emitted structured JSON yields whose vote_lines quote the lines, frozen stripped-line binding read `voted=0` while the substring-binding C2 counter read `entailed=15` on the same bytes.
- The lesson (corpus/lessons/round-55-verifier-spotcheck.md, routed defect 3) carries the format rule + dispatch validator as the named carry-forward; the contract converts it into C2. Mining it again "instead" would double-count one defect in two instruments and would leave the census misstatement — the exact class QUALITY 152 now bars ("A census receipt is the command's captured bytes, not a retyped summary", corpus/QUALITY.md:1520) — with no cheap, binary, in-round handle.

Class fit, census misstatement vs vote-emission mistake:

- The frontier step's declared product is the census before→after pair (contract: "Start census receipt … End census must exit 0"). The census misstatement's frozen fix is one paste away and recurs every round; the vote-emission fix needed claim-grade machinery (tool + 16-case selftest + pinned counter + fixtures), which C2 supplies and the wave's C2 attack seats already falsify independently.
- Severity of the two mistakes is not the test — instrument fit is. The vote-emission mistake killed round-55 C1's vote arm; the census misstatement killed no verdict. But the frontier-mined-mistake slot is a discipline instrument, and the discipline class is the one with a frozen, checkable remedy.
- Caveat: right class chosen, wrong application — the round's own start receipt does not implement the frozen fix (item (c)). The class choice is sound; the execution repeats the mined defect.

## (b) Sourced-claim rule — verdict: HOLDS; citations load-bearing and accurate in both directions

Both rows opened this round: `git show 5b295eee:corpus/SOURCES.md | grep -c 'S544|S545'` → 0; rows first appear at data commit c419fe6d (corpus/SOURCES.md:324 S544, :325 S545), status `mined`, opened `2026-10-27`, used-by naming each entry and its tool.

C1 on S544 — load-bearing test (remove the citation, does the entry still stand?):

- The entry's header names S544 "grammar authority"; the section "The frozen grammar (S544)" grounds every grammar rule in writer-line citations: inline.sh:149 (launch `pgid=` + `driver=… attempt=…`), inline.sh:176 (complete `; hyaku-inline attempt=a`), inline.sh:182 (dead `; retry same round (…)`), shokunin-watchdog.sh:266 (launch bare `pgid=`), :405 (complete `; advancing to round=n+1`), :448 (dead), :241-249 (launch-fail ` :: reason`), :398 (wrap ` landed` / `; NOT respawning (fleet-wrap)`).
- Every cited line verified against the live fleet scripts (read-only): all eight are exact single-line matches (e.g. inline.sh:149 = `log "launch $lane round=$n pgid=$$ driver=hyaku-inline attempt=$a"`; shokunin-watchdog.sh:398 = `log "wrap $lane round=$n landed; NOT respawning (fleet-wrap)"`).
- Committed extract corpus/evidence/sources-r56/watchdog-log-grammar.txt sha256 = 38ba3e6b…417796, matching the S544 row pin exactly.
- Removal test: the measurement facts (live receipt 1728 lines / 0 malformed / 23 lanes; the Limits section) stand without S544, but the entry's central claim — "the probe grammar is frozen from the writer source", the row's teaches cell — collapses into log induction. The entry still stands as a probe manual; it falls as a sourced claim. Citation is load-bearing.
- Named limit (not a defect for this item): the cited writers are fleet-owned files that can move outside the lane; the pinned extract is the stable snapshot and matches today.

C2 on S545 — load-bearing test:

- The overclaim guard ("a scalar that merely *contains* a vote sentence ('the claim is RECHECK … holds today') is prose, not a vote") rests on three S545 citations: §1 line 251 "A JSON text is a serialized value."; §2 grammar line 308 `value = false / null / true / object / array / number / string`; §2 line 461 `string = quotation-mark *char quotation-mark`.
- All three verified against the committed copy corpus/evidence/sources-r56/rfc8259.txt by `grep -n` (251, 308, 461 exact); sha256 = 61a5378f…4cd2d7 matches the S545 row pin.
- Removal test: without S545 the two-channel rule still functions as a spec, but the entry's sentence "This is the RFC 8259 grammar reading" becomes false and the anchored binding is unjustified convention — the very overclaim posture the entry criticizes in the old substring counter. Citation is load-bearing.

Counter nexus re-measured at T (both pass, so the rule is enforced, not just asserted):

- `python3 .ufo/waves/round-56/count-c1.py 8be2717b… --repo …` → `C1=met selftest=ok fixtures=ok entry=ok row=ok norem=ok rev=8be2717b…` exit=0 (run from scratch, TMPDIR set).
- `python3 .ufo/waves/round-56/count-c2.py 8be2717b… --repo …` → `C2=met selftest=ok tally=ok control=ok contrast=voted0 entry=ok row=ok rev=8be2717b…` exit=0.

## (c) Census before→after command — verdict: NOT the frozen one (start receipt repeats the mined defect class)

Frozen fix required (lesson routed defect 1 + contract): paste census-mode output, which prints `mori rows N`, or paste the counting command; and (routed defect 2) the receipt must stamp the measured revision.

What is committed at .ufo/waves/round-56/evidence/census-start.txt:

- 25 lines: 23 W04 duplicate-url lines + `mori\tok\t…/corpus/SOURCES.md` + `exit=0`. It is validate-mode bytes only. `grep -n 'rows|316|rev|sha'` over the file → no match (exit 1). There is no row count and no revision stamp anywhere in the file, and no second census receipt exists under .ufo/waves/round-56/ (`grep -rn 'mori rows|rows 316|rows 318'` finds only seat drafts, no receipt bytes).
- The contract's parenthetical "(exit 0, 316 rows, 23 W04)" therefore embeds a number that appears nowhere in the receipt — a retyped summary, the exact QUALITY 152 class the round mined.
- The receipt cannot even substantiate 316 over 318: I diffed the receipt body (minus the `exit=0` append) against a live `sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori` at HEAD — byte-identical; and the W04 set over the entering-tip registry (316 rows) is the identical 23 lines (S544/S545 add no duplicate URLs). So the same bytes describe both the 316-row and the 318-row registry; the row count is indeterminate from the receipt.
- Provenance sharpens the doubt: census-start.txt was committed in c419fe6d — the same commit that added S544+S545 (registry 316→318; verified `git show <rev>:corpus/SOURCES.md | grep -c '^| S[0-9]'` = 316 at 5b295eee and d27d943a, 318 at c419fe6d/6ced9da9/3f494b49/8be2717b). A receipt committed in the same commit that moved the count, with no stamped revision, is indeterminate as evidence of the before-state.
- Stamp convention violated: sibling receipts carry measured revisions (c1-at-freeze `rev=3f494b49…`, c2-at-freeze `rev=3f494b49…`, c2-old-counter-voted0 `rev=5b295eee…`, controls.txt rev-stamped per line). census-start.txt has none, against the contract's own sentence "receipts here stamp the measured revision themselves".
- The conforming capture was one command away and remains available: `sources-census.sh census --root … mori` at HEAD prints `mori rows 318` plus tier/status histograms (ran live, exit=0); at E it would print `mori rows 316`.
- Partial compensation exists only at seat level: build-w1-spec.py directs Mo56ExecCensus/Mo56ExecRowsCensus to paste the counting commands and expect 318 at T. The committed artifact of record, however — the receipt the round-57 before→after line will cite — is non-conforming today, and the contract text repeats the retyped-summary pattern in the same line that announces the fix.

Smallest safe correction (data/evidence only; no counter, predicate, or kill-rule change proposed): re-capture the start receipt now — census-mode output at E (`mori rows 316`) plus the row-count awk over `git show 5b295eee…:corpus/SOURCES.md`, with `rev=5b295eeebd87ebd610d8d39bfe2035742f740cfa` and `exit=$?` appended; capture the end receipt the same way at the landed tip; cite the stamped revisions in the SCORECARD before→after row. If the L1 will not re-capture this round, route as a named item for round 57 with this paragraph as the record. The end-census exit condition itself is satisfiable (validate exits 0 with the 23 W04 set unchanged, verified live).

## Cross-checks run (evidence hygiene)

- Freeze pins: sha256 of contract.md/count-c1.py/count-c2.py/controls.py at T match .ufo/waves/round-56/evidence/freeze-sha256.txt (088761f3…, c4e58eed…, 4b350c77…, 5bf65ac0…); tools/mori-driver-liveness.py = 6b3dba74…, tools/mori-vote-bind.py = 8be1acdb… match the pinned tool shas.
- S545/S544 row pins match committed evidence copies (61a5378f…, 38ba3e6b…).
- Artifact under flag: while testing the receipt against the entering-tip registry I copied SOURCES.md into scratch and ran `validate --file`; that run floods E11 "missing used-by" because used-by cells resolve relative to the registry's directory — an artifact of the copy, not a registry defect. The live lane validate is clean (exit=0, 23 W04, byte-body identical to the committed receipt).
- No fleet/lane/jj mutation performed; all git use read-only (show/log/grep/rev-parse); no tools installed.

## Findings

- HIGH — .ufo/waves/round-56/evidence/census-start.txt: start-of-round census receipt carries no row count (no census-mode `mori rows N` line, no counting-command paste) and no measured-revision stamp, despite routed defect 1's frozen fix ("paste census-mode output … or the counting command") and routed defect 2's ("receipts here stamp the measured revision themselves"); committed in the same data commit (c419fe6d) that moved the registry 316→318 rows, so the before-state row count is indeterminate from the receipt. Item (c).
- MED — .ufo/waves/round-56/contract.md ("Frontier and routed defects"): the parenthetical "(exit 0, 316 rows, 23 W04)" asserts a row count that appears nowhere in the cited receipt — a retyped summary of exactly the class QUALITY 152 bars and the class this round mined; the "End census must exit 0" bar is satisfiable but the before→after row claim will again rest on retyped numbers unless the receipt is re-captured per the finding above. Item (c).
- LOW — corpus/SOURCES.md S544 row: cited writer scripts (scripts/hyaku/inline.sh, scripts/shokunin-watchdog.sh) are fleet-owned moving files outside the lane's pin control; all eight cited lines match today and the pinned extract (sha 38ba3e6b…) is the stable snapshot, but the row's anchor is live-fleet-dependent — a named limit, routed for awareness, no action required this round. Item (b).
- INFO — items (a) and (b) verdicts are clean: the mined class is the right class (the vote-emission mistake was already mined as the C2 claim substance per the contract's carried-planned-item sentence), and the sourced-claim rule holds — both entries rest on rows opened this round with load-bearing, verified-accurate citations in both removal directions.

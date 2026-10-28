# Mo59Scribe47 — C2 depth entry skeleton (draft only, not landed)

Seat: `Mo59Scribe47` (scribe, leaf — no subagents). Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin`.
Freeze revision: `60b3a76ad0524c8978cc51922940be1c8c388915`; entering revision `2b9f03975bfb6e508f35074ac8181ec8bf54e805`.
Disk guard before work: green (`/fast/scratch/hyaku` 27% used, 592.6G free). No tool installs or updates were made.

Read first (read-only): `.ufo/waves/round-59/contract.md`, `.ufo/waves/round-59/count-c1.py`,
`.ufo/waves/round-59/count-c2.py`, `tools/mori-settlement-scan.py` at R, `.ufo/waves/round-59/trees-c2/t03-*`,
`corpus/SOURCES.md` at R, `scripts/sources-census.sh`.

## Result

A 14-claim entry skeleton over 6 distinct committed artifacts (contract minimum: 10 claims / 3 files) in the
frozen claim grammar, with `line` and `offset` spans and sha256 pins computed from the artifacts **at R**, plus
6 proposed registry rows (`S553`–`S558`, one per cited artifact copy). Verified end-to-end against the frozen
counter in a throwaway sandbox repo: `C2=met … claims=14 files=6` (receipt below). Nothing was written to
`corpus/`, the registry, SCORECARD, LOG or the lane VCS.

## Artifacts pinned (bytes at R; R == HEAD for all six)

| artifact | copy (`corpus/evidence/sources-r59/`) | bytes | newlines | sha256 |
|---|---|---:|---:|---|
| `.ufo/waves/round-54/w1-results.json` | `w1-results-r54.json` | 264143 | 451 | `ea48a0cc07fa948c70d90103b589db0cdf7d48343aa689a3e56742c1cd59335f` |
| `.ufo/waves/round-55/w1-results.json` | `w1-results-r55.json` | 197729 | 391 | `2e5b0a0f94d1fa5b90b2804d370db87d25d5197fa65bc4f26441d939b8d9763b` |
| `.ufo/waves/round-56/w1-results.json` | `w1-results-r56.json` | 358591 | 391 | `19536201a689c954899a2e6decf322ef2c5f3d2ed9bc8ddb75229636b1e5d761` |
| `.ufo/waves/round-57/w1-results.json` | `w1-results-r57.json` | 159483 | 391 | `29e7a35df544315d3bb6ac2f0da96235342d77a1f8306ab25b8a27675669beb1` |
| `.ufo/waves/round-58/w1-results.json` | `w1-results-r58.json` | 180075 | 391 | `a57b660d9f41c55dc5d614444f60f1cf658d19a55a530c9788369e5fb7ec61fc` |
| `.ufo/waves/round-58/evidence/w1-settlement.json` | `w1-settlement-r58.json` | 230411 | 1 | `b259e73cdddef7ff8565a01c6d97f79da8b112aa6c7dbb97a8aa541b4f0b5588` |

Copy plan: `git show 60b3a76ad0524c8978cc51922940be1c8c388915:<artifact>` straight into the copy path
(byte-identical by construction; the counter's `tree` arm re-checks copy-vs-artifact equality at R).

## Claim map (14 claims, 6 files)

| claim | copy | span | pin |
|---|---|---|---|
| K1 | w1-results-r54.json | `line:5` ` "seats": 74,` | `ea48a0cc…59335f` |
| K2 | w1-results-r54.json | `line:446` `   "name": "Mo54ExecSelftestReceipts",` | `ea48a0cc…59335f` |
| K3 | w1-results-r55.json | `line:5` ` "seats": 64,` | `2e5b0a0f…d9763b` |
| K4 | w1-results-r55.json | `line:386` `   "name": "Mo55Simple02",` | `2e5b0a0f…d9763b` |
| K5 | w1-results-r56.json | `line:3` ` "round": 56,` | `19536201…1e5d761` |
| K6 | w1-results-r56.json | `line:9` `   "agent": "scout",` | `19536201…1e5d761` |
| K7 | w1-results-r57.json | `line:5` ` "seats": 64,` | `29e7a35d…669beb1` |
| K8 | w1-results-r57.json | `line:386` `   "name": "Mo57Simplifier64",` | `29e7a35d…669beb1` |
| K9 | w1-results-r58.json | `line:5` ` "seats": 64,` | `a57b660d…ec61fc` |
| K10 | w1-results-r58.json | `line:386` `   "name": "Mo58Simplifier64",` | `a57b660d…ec61fc` |
| K11 | w1-settlement-r58.json | `offset:79` `"schema":"mori-wave-settlement-v1"` | `b259e73c…0b5588` |
| K12 | w1-settlement-r58.json | `offset:1` `"ignored_json":1719` | `b259e73c…0b5588` |
| K13 | w1-settlement-r58.json | `offset:134` `"members":3153` | `b259e73c…0b5588` |
| K14 | w1-settlement-r58.json | `offset:312` `"waves":62` | `b259e73c…0b5588` |

Every derived statement in the claim prose was re-checked against parsed JSON: r54 seats 74 / 74 members,
`results[73].name == "Mo54ExecSelftestReceipts"`; r55 64/64, last `Mo55Simple02`; r56 round 56, lane `mori`,
wave `w1`, 64/64, `results[0] == (scout, Mo56ScoutLogGrammar)`; r57 64/64, last `Mo57Simplifier64`; r58 64/64,
last `Mo58Simplifier64`; settlement `totals.members == 3153 == Σ per-wave members`, 62 waves,
`states 36 settled + 26 partial`, every wave has `dispatch_path` + `dispatch_sha256`, and `ignored_json` is
absent from all five results files. Each offset quote was asserted byte-equal at its offset and unique in the file.

## Draft entry (verbatim — to land at `corpus/knowledge/wave-settlement-artifacts-r59.md`)

```markdown
source: S553, S554, S555, S556, S557, S558
verified-at: 2026-10-28
recheck: `python3 .ufo/waves/round-59/count-c2.py 60b3a76ad0524c8978cc51922940be1c8c388915 --scratch $TMPDIR`
coverage-map: Core — orchestrator `*-results.json` / settlement-evidence schema identity across rounds 54–58; deepens the existing wave-settlement surface, no frontier advance claimed

# Wave-settlement artifacts pin the seats/members contract of rounds 54–58

This entry pins the byte-level header and boundary lines of the five `w1-results.json` settlement artifacts plus the round-58 settlement evidence, so the round-59 `tools/mori-settlement-scan.py` verdict is judged against committed bytes rather than prose. Every claim below is a byte-exact span of the copy named in the claim; the copy is byte-equal to its `.ufo` artifact at the freeze revision.

Each `w1-results.json` object has the key set `lane`, `round`, `wave`, `seats`, `results`; each `results` member has the key set `agent`, `name`, `note`, `output`; member names are unique and every `agent` value is one of connector, critic, executor, mutation-tester, revenger, reviewer, scout, scribe, sentinel, simplifier. The seats/members counts below are the ones the scanner gate compares; the settlement evidence file is separate evidence about dispatch settlement, not a results file.

## Claims

- **K1** — Round-54 results declare 74 seats, and `results` carries exactly 74 member objects: the scanner's seats==members gate is satisfied on the declared header. Quote: ` "seats": 74,` (corpus/evidence/sources-r59/w1-results-r54.json:line:5; pin ea48a0cc07fa948c70d90103b589db0cdf7d48343aa689a3e56742c1cd59335f)
- **K2** — The 74th and final r54 member is named Mo54ExecSelftestReceipts, terminating the member list at the declared seat count. Quote: `   "name": "Mo54ExecSelftestReceipts",` (corpus/evidence/sources-r59/w1-results-r54.json:line:446; pin ea48a0cc07fa948c70d90103b589db0cdf7d48343aa689a3e56742c1cd59335f)
- **K3** — Round-55 results declare 64 seats and its `results` array carries exactly 64 members. Quote: ` "seats": 64,` (corpus/evidence/sources-r59/w1-results-r55.json:line:5; pin 2e5b0a0f94d1fa5b90b2804d370db87d25d5197fa65bc4f26441d939b8d9763b)
- **K4** — The 64th and final r55 member is named Mo55Simple02, terminating the member list at the declared seat count. Quote: `   "name": "Mo55Simple02",` (corpus/evidence/sources-r59/w1-results-r55.json:line:386; pin 2e5b0a0f94d1fa5b90b2804d370db87d25d5197fa65bc4f26441d939b8d9763b)
- **K5** — Round-56 results carry the round token 56 in their header; the wave object is `mori`/`w1` with 64 declared seats and 64 members. Quote: ` "round": 56,` (corpus/evidence/sources-r59/w1-results-r56.json:line:3; pin 19536201a689c954899a2e6decf322ef2c5f3d2ed9bc8ddb75229636b1e5d761)
- **K6** — Round-56's first member carries role `scout`, a role token inside the scanner's accepted enum. Quote: `   "agent": "scout",` (corpus/evidence/sources-r59/w1-results-r56.json:line:9; pin 19536201a689c954899a2e6decf322ef2c5f3d2ed9bc8ddb75229636b1e5d761)
- **K7** — Round-57 results declare 64 seats and its `results` array carries exactly 64 members. Quote: ` "seats": 64,` (corpus/evidence/sources-r59/w1-results-r57.json:line:5; pin 29e7a35df544315d3bb6ac2f0da96235342d77a1f8306ab25b8a27675669beb1)
- **K8** — The 64th and final r57 member is named Mo57Simplifier64, terminating the member list at the declared seat count. Quote: `   "name": "Mo57Simplifier64",` (corpus/evidence/sources-r59/w1-results-r57.json:line:386; pin 29e7a35df544315d3bb6ac2f0da96235342d77a1f8306ab25b8a27675669beb1)
- **K9** — Round-58 results declare 64 seats and its `results` array carries exactly 64 members. Quote: ` "seats": 64,` (corpus/evidence/sources-r59/w1-results-r58.json:line:5; pin a57b660d9f41c55dc5d614444f60f1cf658d19a55a530c9788369e5fb7ec61fc)
- **K10** — The 64th and final r58 member is named Mo58Simplifier64, terminating the member list at the declared seat count. Quote: `   "name": "Mo58Simplifier64",` (corpus/evidence/sources-r59/w1-results-r58.json:line:386; pin a57b660d9f41c55dc5d614444f60f1cf658d19a55a530c9788369e5fb7ec61fc)
- **K11** — The r58 settlement evidence names its own schema `mori-wave-settlement-v1`, the artifact family the depth entry pins. Quote: `"schema":"mori-wave-settlement-v1"` (corpus/evidence/sources-r59/w1-settlement-r58.json:offset:79; pin b259e73cdddef7ff8565a01c6d97f79da8b112aa6c7dbb97a8aa541b4f0b5588)
- **K12** — The settlement evidence counts 1719 ignored non-object JSON inputs, an accounting scalar the results-file gate does not read. Quote: `"ignored_json":1719` (corpus/evidence/sources-r59/w1-settlement-r58.json:offset:1; pin b259e73cdddef7ff8565a01c6d97f79da8b112aa6c7dbb97a8aa541b4f0b5588)
- **K13** — The settlement evidence totals 3153 dispatch members over the 62 waves it inventories (36 settled, 26 partial). Quote: `"members":3153` (corpus/evidence/sources-r59/w1-settlement-r58.json:offset:134; pin b259e73cdddef7ff8565a01c6d97f79da8b112aa6c7dbb97a8aa541b4f0b5588)
- **K14** — Every inventoried wave carries its own dispatch_path and dispatch_sha256, so settlement is per-dispatch rather than per-lane. Quote: `"waves":62` (corpus/evidence/sources-r59/w1-settlement-r58.json:offset:312; pin b259e73cdddef7ff8565a01c6d97f79da8b112aa6c7dbb97a8aa541b4f0b5588)

## Boundary

The artifacts are orchestrator-written settlement records. The claims above establish only the declared header values, the member-list boundary names, and the settlement-evidence scalar fields; they do not establish report quality, lane health, provider state, or that any agent actually ran. The round-53 results file is out of scope for this entry: it is the counter's schema-drift control and fails the scan on `report_file` extra keys.
```

## Proposed registry rows (verbatim; insert **inside** `## Registry`, after S552)

```markdown
| S553 | mori round-54 wave settlement results — `.ufo/waves/round-54/w1-results.json` (copy `corpus/evidence/sources-r59/w1-results-r54.json`) | own-work | A | the r54 `w1-results.json` header and member-list boundary only; not report quality or lane health | copy sha256 ea48a0cc07fa948c70d90103b589db0cdf7d48343aa689a3e56742c1cd59335f; seats line 5, final member name line 446 | The r54 settlement artifact declares 74 seats over exactly 74 named members; the seats==members gate binds on committed bytes. | mined | 2026-10-28 | 90d | corpus/knowledge/wave-settlement-artifacts-r59.md |
| S554 | mori round-55 wave settlement results — `.ufo/waves/round-55/w1-results.json` (copy `corpus/evidence/sources-r59/w1-results-r55.json`) | own-work | A | the r55 `w1-results.json` header and member-list boundary only; not report quality or lane health | copy sha256 2e5b0a0f94d1fa5b90b2804d370db87d25d5197fa65bc4f26441d939b8d9763b; seats line 5, final member name line 386 | The r55 artifact declares 64 seats over exactly 64 named members, so the gate is satisfiable at the 64-seat band. | mined | 2026-10-28 | 90d | corpus/knowledge/wave-settlement-artifacts-r59.md |
| S555 | mori round-56 wave settlement results — `.ufo/waves/round-56/w1-results.json` (copy `corpus/evidence/sources-r59/w1-results-r56.json`) | own-work | A | the r56 `w1-results.json` round token, role enum sample and member boundary; not report quality | copy sha256 19536201a689c954899a2e6decf322ef2c5f3d2ed9bc8ddb75229636b1e5d761; round line 3, first member agent line 9 | The r56 artifact keys its header by round 56 and opens with a scout member, showing the role enum is artifact-carried, not positional. | mined | 2026-10-28 | 90d | corpus/knowledge/wave-settlement-artifacts-r59.md |
| S556 | mori round-57 wave settlement results — `.ufo/waves/round-57/w1-results.json` (copy `corpus/evidence/sources-r59/w1-results-r57.json`) | own-work | A | the r57 `w1-results.json` header and member-list boundary only; not report quality or lane health | copy sha256 29e7a35df544315d3bb6ac2f0da96235342d77a1f8306ab25b8a27675669beb1; seats line 5, final member name line 386 | The r57 artifact declares 64 seats over exactly 64 named members terminated by Mo57Simplifier64. | mined | 2026-10-28 | 90d | corpus/knowledge/wave-settlement-artifacts-r59.md |
| S557 | mori round-58 wave settlement results — `.ufo/waves/round-58/w1-results.json` (copy `corpus/evidence/sources-r59/w1-results-r58.json`) | own-work | A | the r58 `w1-results.json` header and member-list boundary only; not report quality or lane health | copy sha256 a57b660d9f41c55dc5d614444f60f1cf658d19a55a530c9788369e5fb7ec61fc; seats line 5, final member name line 386 | The r58 artifact declares 64 seats over exactly 64 named members terminated by Mo58Simplifier64. | mined | 2026-10-28 | 90d | corpus/knowledge/wave-settlement-artifacts-r59.md |
| S558 | mori round-58 wave settlement evidence — `.ufo/waves/round-58/evidence/w1-settlement.json` (copy `corpus/evidence/sources-r59/w1-settlement-r58.json`) | own-work | A | the r58 settlement-evidence scalar header only (schema name, ignored-JSON count, member total, wave count); not a results file and not an agent-execution proof | copy sha256 b259e73cdddef7ff8565a01c6d97f79da8b112aa6c7dbb97a8aa541b4f0b5588; schema offset 79, ignored_json offset 1, members offset 134, waves offset 312 | The settlement evidence self-identifies as mori-wave-settlement-v1 and reports 1719 ignored JSON files, 3153 members and 62 waves as separate accounting from the results-file gate. | mined | 2026-10-28 | 90d | corpus/knowledge/wave-settlement-artifacts-r59.md |
```

Row shape checks: 11 cells each (`id|source|kind|tier|scope|anchor|teaches|status|opened|recheck|used-by`),
`status=mined`, `used-by` exactly the entry path (counter compares `cells[10] != ENTRY`), kind `own-work`,
tier `A`, recheck `90d`, opened `2026-10-28`.

## Verification (all read-only on the lane; sandbox under scratch)

1. **Baseline at R** (the draft is additive, not overlapping):
   `python3 .ufo/waves/round-59/count-c2.py 60b3a76… --scratch <scratch>/c2run` → rc=1
   `C2=unmet selftest=ok scan=ok drift=ok trees=ok entry=bad rows=bad pins=bad tree=bad claims=0 files=0 rev=60b3a76ad0524c8978cc51922940be1c8c388915 failed=copy_absent:corpus/evidence/sources-r59/w1-results-r54.json,…,copy_absent:corpus/evidence/sources-r59/w1-settlement-r58.json,entry_absent,tree`
   Note: `tools/mori-settlement-scan.py` **is already present at R** and hashes to the frozen PIN
   (`4c04bf2170b0484192dd157ee04851e8243e030c54046c5e8806d46eea5ac9a9`); the wave's remaining C2 arms are
   entry + copies + rows + pins + tree, and `failed=` names exactly those.
2. **Frozen entry arm on the draft** (`import` of `count-c2.py`, `eval_entry(<materialized root>)`):
   `ok=True stats={'claims': 14, 'files': 6} reasons=[]`.
3. **End-to-end in a throwaway sandbox repo** (`git archive R | tar -x` → `git init` → commit base
   `c40c234`, add 6 copies + entry + 6 rows → commit `fa571512142049379c6b83f2483cd80699cd691b`):
   `python3 .ufo/waves/round-59/count-c2.py fa57151… --repo <sandbox>` → rc=0
   `C2=met selftest=ok scan=ok drift=ok trees=ok entry=ok rows=ok pins=ok tree=ok claims=14 files=6 rev=fa571512142049379c6b83f2483cd80699cd691b`
4. **Counter-level negative control** (same sandbox, one pin corrupted in K9/K10's family):
   commit `94bee6d22517319486bf4a4faa4a88cb6c8837c5` → rc=1
   `C2=unmet selftest=ok scan=ok drift=ok trees=ok entry=ok rows=ok pins=bad tree=ok claims=14 files=6 rev=94bee6d… failed=pins`
5. **Entry-level controls** (mutations of the draft, `eval_entry` on a copied root):
   wrong line number (`line:446`→`line:447`) → `reasons=['span:2']`;
   stale pin on the r56 family → `reasons=['pin:5','pin:6']`;
   frontmatter stripped → `reasons=['frontmatter:source','frontmatter:verified-at','frontmatter:recheck','frontmatter:coverage-map','rows:no_source_ids']`;
   quote shortened to two bytes → `reasons=['span:short=10']`.
6. **Counter selftest**: `python3 .ufo/waves/round-59/count-c2.py --selftest` → `C2_SELFTEST pass=9 fail=0` (matches the contract).
7. **Census**: `scripts/sources-census.sh validate --file <sandbox>/corpus/SOURCES.md --today 2026-10-28` →
   exit 0, 25 findings, all `W04` (pre-existing same-URL-across-scopes warnings), **zero findings for S553–S558**
   (`grep -E 'S55[3-8]'` → empty).
8. **Scanner semantics cross-check** (`tools/mori-settlement-scan.py` at R): `MEMBER_KEYS = {name, agent, output, note}`,
   `ROLES = (scout, reviewer, critic, connector, sentinel, executor, mutation-tester, revenger, simplifier, scribe)`,
   `seats != len(results)` → `seats_mismatch`; the r53 drift control fails with `member[0..N]:extra_keys=report_file`,
   `verdict SETTLEMENT_SCAN_FAIL` — matching the entry's Boundary paragraph.

## Findings / handoff risks

1. **E12 trap on row placement.** Appending the six rows at end of `corpus/SOURCES.md` (a natural shortcut) produces
   6× `E12 … row outside Registry section` per copy (observed: 12 findings after a double append). The rows MUST be
   inserted inside the `## Registry` section (currently lines 3–333; last data row `S552` at line 332, next heading
   `## Paths` at line 334).
2. **SID numbering depends on the S552 reconciliation.** `S552` is the round-58 duplicate-source defect; the contract
   requires an appended reconciliation row for it. If that reconciliation consumes `S553`, the six rows here shift to
   `S554`–`S559`, and both the entry frontmatter `source:` line and nothing else need renumbering (claims/pins are
   unaffected). Sequencer decision, not made here.
3. **The tool is already landed at R.** C2's do-nothing arm at R therefore fails on `copy_absent`/`entry_absent`, not
   `tool_absent` — the contract's "Before" sentence (`failed=tool_absent`) does not describe R as it now stands. The
   draft's evidence quotes the counter's actual R output above; the contract text itself is frozen and was not edited.
4. **`line:` vs `offset:` risk.** All `line:` spans are full lines of a 1-space/3-space-indented pretty-printed JSON, so
   a future re-serialisation of an artifact would move them; that is exactly what the pin protects against (any byte
   change flips `pins=bad`), and the counter's `tree` arm additionally requires copy==artifact.
5. **Two claims per results file share one pin** (K1/K2, K3/K4, K5/K6, K7/K8, K9/K10). The counter's `distinct` rule is
   on K ids only, so this is legal; a pin change surfaces as two `pin:` reasons (observed in control 5).
6. **Census E11 needs the entry on disk.** The rows' `used-by` resolves only once the entry is committed
   (`E11 … missing used-by` otherwise). In the scratch-only root, all 367 E11 findings were pre-existing rows
   whose targets were absent from the partial tree — none were S553–S558.
7. Not verified, not claimed: the round-59 lesson Gate pair (≥1 admit / ≥1 reject) required by contract §2b is a
   separate artifact and was not drafted here; nothing in this report asserts axis score movement.

## Out of scope (untouched)

`corpus/` (entry and copies not written), `corpus/SOURCES.md` (rows not inserted), `tools/`, `SCORECARD.md`, `LOG.md`,
fleet/sibling repos, lane VCS (no commits, no jj ops, no worktrees). No files in `~/.local/bin` or any PATH dir.
Sandbox git operations ran only with `git -C` inside `/fast/scratch/hyaku/mori-r59/Mo59Scribe47/…`; the assertion
`git rev-parse --show-toplevel` printed the sandbox path before any commit.

## Observed lane state at report time (not mine, not evaluated)

The lane working tree changed under this seat during the wave (siblings landing the same claim). At report time
`git -C … status --porcelain` shows `M corpus/SOURCES.md` (+8 lines, rows `S553`–`S559`), untracked
`corpus/knowledge/wave-settlement-artifacts-r59.md` (6207 bytes), and untracked `corpus/evidence/sources-r59/`
with **7** copies (`w1-results-r53.json` plus the six in the frozen `ARTIFACTS` map). None of these paths were
written by this seat; every write here went to `/fast/scratch/hyaku/mori-r59/Mo59Scribe47/` or to this report.
That landing is a separate artifact: it is not merged with, and was not used to validate, the draft above. The
draft's facts (pins, spans, counts) were computed from `git show <R>:<artifact>` bytes, which the working-tree
changes do not alter.

## Scratch / receipts

Scratch root `/fast/scratch/hyaku/mori-r59/Mo59Scribe47/` (created with `mkdir -p`, `TMPDIR` set there, `--scratch`
passed to every counter invocation). Receipts copied into this report before cleanup: baseline C2 line (item 1),
met line (item 3, rev `fa57151`), negative-control line (item 4, rev `94bee6d`), selftest line (item 6), census exit
code and code histogram (item 7). Scratch (including the 400 MB sandbox tree and its clone) was removed after writing
this report; nothing under `/tmp` was used as evidence.

# MoriR16.HistoricalCorrections — round 16

Scope: map the round-15 non-author closure queue onto the round-16 lesson, QUALITY and SKILL, and report active contradictions. Leaf seat. Read-only except this report. No builds, tests, gates, smoke runs, commits or installs. External reads were `curl` piped straight into `grep -cF`; nothing was written outside this file.

Snapshot: read 2026-10-20 while the round-16 wave was in flight. `git status` showed modified `LOG.md`, `PROVINCE.md`, `SCORECARD.md`, `corpus/QUALITY.md`, `corpus/SOURCES.md`, and untracked `.ufo/waves/round-16/`. Line numbers are as read; they will drift as the wave lands.

Source queue: `corpus/lessons/round-15-verifier-spotcheck.md` (non-author closure, committed `b83edc6`; decision `admitted: true`, bounded to the declared finite-fixture scope; M4–M6 procedural violations disclosed).

## 1. Mapping: closure item → current state → target

| # | Closure item | Verified current state | Target | Status |
|---|---|---|---|---|
| 1 | M4: append a correction assigning L1 responsibility for the omitted exact-id / no-broadcast restriction; carry it into future contexts | Forward fix present: `wave1-spec.json` and `wave1-dispatch.json` each contain the `agent://all` prohibition (2 hits each). QUALITY 37 (uncommitted) records the dispatcher defect. Retrospective correction NOT present: `corpus/lessons/round-15.md:22` M4 row is unchanged and has no appended block. | `round-15.md` append-only correction block; `round-16.md#M1` | Forward: landed statically. Retrospective: **OPEN** |
| 2 | Add the omitted outside-lane `/tmp` write (`build/HarnessBuild.md:248–267`) to the procedural-debt disposition | Verified at `.ufo/waves/round-15/build/HarnessBuild.md:256–257` (`--pin-fixtures /tmp/mori-r15-expected-probe-final.json`; `PINNED /tmp/...`). `round-15.md` M5 names only `RegistryFrontier.md:63–72`; the HarnessBuild instance is absent from the lesson. | `round-15.md` correction block; `round-16.md#M2`; QUALITY 38 | Rule landed (QUALITY 38, uncommitted). Round-15 disposition: **OPEN** |
| 3 | Append a correction separating "implementing a selftest" from "permission to execute it"; preserve the historical report | Verified: `HarnessBuild.md` honesty note (~lines 301–307) justifies earlier `--selftest` runs as "explicitly required" by the assignment. `round-15.md` M6 has no correction. | `round-15.md` correction block; `round-16.md#M3`; QUALITY 39 | Rule landed (QUALITY 39, uncommitted). Round-15 disposition: **OPEN** |
| 4 | Correct active registry prose: `SKILL.md:134` says `--no-frozen-control` "requires the hidden `--selftest-child`" | **Still present.** `SKILL.md` is unmodified in `git status`. Delivered gate parser (`tools/mori-round15-regressions.py:2310–2319`) defines only `--census --fixtures --output --frozen --expected --pin-fixtures --case --timeout --selftest`; both former flags are refused (`evidence/control-bypass-refused.json`, rc 2, "unrecognized arguments"). `build/SkillInterface.md:88` is historical and should stay. SkillRegistry is assigned in `wave1-spec.json`. QUALITY 40 (uncommitted) is the sweep rule. | `SKILL.md:134` | **ACTIVE CONTRADICTION** (owner in flight) |
| 5 | Carry the old drift-pin debt; no re-pin | Consistent. `evidence/drift-current.json` records `"exit": 1` for `corpus/evidence/baseline-r10-20261015T2231Z.json`. `SKILL.md:196–216` says no re-pin. QUALITY 41 (uncommitted) codifies it. Minor wording issue in C5 below. | QUALITY 41 | Landed (uncommitted); no contradiction in the pin itself |

Stale status wording that the closure did not list but that follows from it (the admission at `b83edc6` supersedes these):

- `corpus/lessons/round-15.md:34`, `:142`, `:165`: "admit/reject sampling is pending closure", "pending independent non-author closure", "remains pending".
- `SCORECARD.md:846` (round-15 section, "C1 verified by the lane, pending non-author closure") and `:874` (calibration cell, "outside closure pending"). `SCORECARD.md:689` and `:752`-era text belong to earlier rounds and are historical; leave them.
- `LOG.md` round-15 "Final measurement" block (~lines 985–988): "Current outside closure is still required." No LOG entry records the `b83edc6` admission decision. `RULES.md` requires every change to append a LOG entry.

## 2. Active contradictions (ranked)

**C1 — HIGH, active. `SKILL.md:134`.** The row says `--no-frozen-control` "is selftest-internal and requires the hidden `--selftest-child`". The delivered gate has neither flag. A reader following the row looks for a flag that does not exist, and the row misstates the control rule that HarnessBuild F2 and the r15 selftest receipt now enforce (the pinned frozen control always runs). Owner: SkillRegistry (already assigned). Suggested replacement for the clause:
> `--selftest` runs the normal gate, including the pinned frozen control; the former `--no-frozen-control` and `--selftest-child` are removed and refused (argparse rc 2; `.ufo/waves/round-15/evidence/control-bypass-refused.json`).

**C2 — MEDIUM, active. Stale "pending" status after admission.** `round-15.md:34,142,165`, `SCORECARD.md:846,874`, and `LOG.md` ~985–988 still say the outside closure is pending. The closure at `b83edc6` returned `admitted: true` at scope. Fix by append-only correction (Section 3, drafts A, C, D). Do not rewrite the historical text.

**C3 — MEDIUM, active (in-flight QUALITY text). QUALITY 38 attribution.** Criterion 38 says "round 16 omitted a `/tmp` expected-probe write" (precedent `round-15.md:23`). The only `/tmp` expected-probe pin write found in the tree is round-15 `HarnessBuild.md:256–257`. Round-16 build files found so far contain only negated statements ("no /tmp use": `build/PackKernelUser.md:44`, `build/Quality.md:26`). Either a round-16 instance exists and must be cited at file:line, or the attribution must point to round-15 `HarnessBuild.md:256–257`. Re-check when the wave settles. Criterion 38 is uncommitted, so correct it in place before commit (no errata needed).

**C4 — MEDIUM, dependency. Dangling lesson pointers.** QUALITY 37–41 cite `corpus/lessons/round-16.md#M1–M5`, and criterion 42 cites `corpus/lessons/round-16.md`. That file does not exist (`corpus/lessons/` holds rounds 12–15 only). QUALITY admission rule 9 ("every path... resolves at the carrying commit") fails unless `round-16.md` lands in the same commit as QUALITY. Do not commit QUALITY without it.

**C5 — LOW, wording. SCORECARD round-15 "next steered-round plan"** says to "retain the reasoned drift re-pin as separate freshness debt until an actual semantic review is assigned." That reads like a planned re-pin. The closure and QUALITY 41 allow a re-pin only as a recorded, semantically reviewed act, never to silence red. Suggested wording: "No re-pin is planned; any future re-pin requires an assigned semantic review (QUALITY 41)."

**Checked and NOT a contradiction:**
- `SKILL.md:30` (capture failure vs positives). Full sentence: "nonzero query rc, stderr, timeout or malformed JSON makes both aggregate and positive evidence unavailable. A semantic record failure in a successfully parsed capture makes raw aggregate/split tokens `unavailable`, never zero, but may retain individually qualified r15 positive evidence." This matches the r15 knowledge note row 8 and the capture-boundary receipts. An earlier truncated read looked contradictory; the full text is consistent.
- "fail-loud on positive validated records" (r14 `journal-alarm-routing-r14.md:221`). Superseded by the explicit correction in `journal-positive-evidence-r15.md`. Not repeated in active SKILL/PROVINCE/README text; `QUALITY.md:83` quotes it only as the superseded phrasing.
- QUALITY 37/38/39/40/41 line pointers to `round-15.md:22`, `:23`, `:24`, `:42` all resolve (M4, M5, M6 rows; the "Re-pin ... rejected" row).
- Round-15 fleet report `.ufo/reports/round-15/mori.md` exists in the parent repo (18303 bytes, 2026-10-20 05:35). Commit `1ccac09` resolves there. `b83edc6` resolves in `mori-shokunin`.

## 3. Append-only correction drafts (for owners; none applied by this seat)

**A — `corpus/lessons/round-15.md`, append after the last line (owner: Lesson scribe):**
```
## Corrections appended round 16 (append-only; original text preserved)
- Status. The non-author closure `corpus/lessons/round-15-verifier-spotcheck.md` (commit b83edc6) admitted C1 at its measured scope (`admitted: true`). The "pending closure" wording at lines 34, 142 and 165 is superseded by that closure.
- M4 (line 22). The omitted exact-id / no-broadcast restriction is the dispatching L1's responsibility. Round-16 contexts carry it (static repair, not a tested preventive control). See QUALITY 37 and round-16.md#M1.
- M5 (line 23). A further outside-lane write is disclosed: `.ufo/waves/round-15/build/HarnessBuild.md:256–257` (`--pin-fixtures /tmp/mori-r15-expected-probe-final.json`). It is a temporary probe output, not durable evidence. See QUALITY 38.
- M6 (line 24). The honesty note at `build/HarnessBuild.md` ~301–307 treated an assignment's implementation request as permission to run selftests. It was not. Writing a selftest is not permission to execute it (QUALITY 39). The admissible verification is the post-integration run.
```

**B — `SKILL.md:134` (owner: SkillRegistry):** replace the "requires the hidden `--selftest-child`" clause with the C1 wording above. Leave `build/SkillInterface.md` unchanged.

**C — `SCORECARD.md` round-15 section, append (owner: Registry scribe):**
```
Correction (round 16, append-only): outside closure b83edc6 admitted C1 at its declared bounded scope (`admitted: true`). The "pending non-author closure" sentence and the calibration cell's "outside closure pending" are superseded. Procedural debt M4–M6 stays disclosed. No score changed.
```

**D — `LOG.md`, append a round-16 entry (owner: L1):** record the `b83edc6` closure decision (admitted at scope, M4–M6 disclosed, five queued items and their landing status from Section 1). Note that the round-15 "closure still required" line is superseded.

**E — `corpus/QUALITY.md` criterion 38 (owner: Quality scribe, uncommitted):** change "round 16 omitted a `/tmp` expected-probe write" to the cited round-15 location, unless a round-16 instance is evidenced at file:line.

## 4. Verification performed (read-only)

- Read `corpus/lessons/round-15-verifier-spotcheck.md`, `round-15.md`, `QUALITY.md`, `SKILL.md`, `SCORECARD.md` (round-15 section), `LOG.md` (round-15 and round-16 entries), the `build/` files named in the closure, and round-16 `wave1-spec.json`, `wave1-dispatch.json`, `swarm-registry.json`, and `build/Quality.md`.
- Delivered gate flags checked by reading `tools/mori-round15-regressions.py:2310–2319`. Receipts read: `control-bypass-refused.json`, `drift-current.json` (exit 1).
- Primary-source presence checks (`curl -fsSL … | grep -cF`, 2026-10-20; count 1 each):
  - S014 `journalctl.html`: "Journal entries permit non-unique fields within the same log entry."
  - S015 `systemd.journal-fields.html`: "Fields prefixed with an underscore are trusted fields"; "User fields are fields that are directly passed from clients"
  - S038 `service.c` @ `cf8ebfc6…`: `[SERVICE_FAILURE_OOM_KILL]`
  - `journalctl.html` (QUALITY 42): "The format of the cursor is private and subject to change."
  - These are presence checks only. I did not re-check the `"oom-kill"` value, the 6588–6602 line range, or any digest.
- Not checked: round-15 `HarnessBuild` task text ("No execution") and the r15 closure's census and gate measurements. I did not run them, per contract.

## 5. Tooling

No installs or updates. Used only `git`, `grep`, `sed`, `ls`, and `curl` (read-only, piped). No credential, database, or omp CLI access.

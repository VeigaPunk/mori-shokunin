# ScribeScorecard — round 47 wave w2 report

Seat: ScribeScorecard (leaf scribe). Assignment: draft the `SCORECARD.md` "## Round 47" section for
the mori-shokunin lane — claims C1/C2 with axis, held score, before→after values copied from the round-47
evidence receipts, counting commands, the measured commit `68d66ca53d89be5c34a62f46af7c37449d9f9b63`,
and a capabilities row "registry pin reconciler v2" (evidence: selftest + v2 junk receipts). No score
change is claimed.

## Behavior (observed evidence)

All reads were read-only; no lane tool was executed by this seat, no production file was edited, and no
tool was installed or updated (no tooling authorization event).

- Read (verbatim): the round-47 contract (`.ufo/waves/round-47/contract.md`), the five before/after
  receipts `evidence/control-c1-donothing.txt`, `evidence/after-c1-v1-frozen.txt`,
  `evidence/after-c1-v2.txt`, `evidence/control-c2-donothing.txt`, `evidence/after-c2.txt`, the control
  receipts `evidence/control-c1-{deleted,moved,truncated}.txt` and
  `evidence/control-c2-{donothing,staged,three}-at-freeze.txt`, the selftest receipt
  `evidence/selftest-pin-check.txt`, all nine `evidence/v2/` junk receipts and eight
  `evidence/v1-junk/` receipts (tails), `corpus/lessons/round-47.md`, the w1 seat reports
  (incl. `w1/ScribeScorecardLog.md`, `w1/CritC1Predicate.md`, `w1/RevPinCheckCode.md`), and the current
  `SCORECARD.md` tail.
- Read-only git (no mutation of jj state, git index, fleet repo, or any tracked file):
  - `git log --oneline --all -- tools/mori-pin-check.py` → freeze `63eecf27` carries v1 (sha256
    `e3ef425a…`), commit `af2250d8` lands v2 (sha256 at T `9832e38c…`); landing commit `68d66ca5`
    ("round-47: after-receipts at af2250d8 (P-C1 frozen v1 met, v2 met, P-C2 met), v1/v2 junk receipts,
    w1 results") parents `af2250d8`.
  - `git show --stat 68d66ca` → T adds only the after-receipts, v1/v2 junk receipts and w1 result
    files; the measured files' trees are identical at `af2250d8` and T.
  - `git diff 68d66ca -- SCORECARD.md` → the working tree already contains an **uncommitted** "## Round
    47" section appended after round 46 (drafted outside this seat). This report's Draft below supersedes
    it with receipt-verified values and the measured commit `68d66ca`.
  - `git ls-tree 68d66ca corpus/knowledge/` → `corpus/knowledge/oom-tracepoints-r47.md` present at T;
    `git show T:corpus/SOURCES.md` → S475 present as a mined tier-A code row naming v7.2 and
    include/trace/events/oom.h, used-by `corpus/knowledge/oom-tracepoints-r47.md`.

## Before → after values (copied verbatim from the receipts)

| Receipt | Verbatim values (final lines) | rc |
|---|---|---|
| `evidence/control-c1-donothing.txt` (entering `2d85e33`) | `PIN_CHECK=unmet tally_pins=26 digest_pins=5 mismatches=1 unparsed=0 no_command=0 dropped=0`; sole mismatch `SKILL.md:912` `MORI_SOURCES_APPENDONLY_SELFTEST` pinned `pass=15 fail=0`, observed `pass=22 fail=0` | 1 |
| `evidence/after-c1-v1-frozen.txt` (at `af2250d8`, frozen v1) | `PIN_CHECK=met tally_pins=28 digest_pins=5 mismatches=0 unparsed=0 no_command=0 dropped=0`; pin line 938 observes `PIN_CHECK_SELFTEST pass=34 fail=0` | 0 |
| `evidence/after-c1-v2.txt` (at `af2250d8`, v2) | `PIN_CHECK=met tally_pins=28 digest_pins=5 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0`; pin line 938 observes `PIN_CHECK_SELFTEST pass=34 fail=0` | 0 |
| `evidence/control-c2-donothing.txt` (entering `2d85e33`) | `C2=unmet events=0 rows=0 name_mismatch=0 field_mismatch=0 callsite_mismatch=0 pin_mismatch=4 source_row=bad provenance=bad failed=entry_absent,pins,source_row` | 1 |
| `evidence/after-c2.txt` (at `af2250d8`) | `C2=met events=8 rows=8 name_mismatch=0 field_mismatch=0 callsite_mismatch=0 pin_mismatch=0 source_row=ok provenance=ok` | 0 |

Controls (all stay unmet, rc 1): C1 deleted `dropped=1`; C1 moved `mismatches=1`; C1 truncated
`mismatches=1`; C2 at-freeze do-nothing `failed=entry_absent,source_row`; C2 staged byte-exact
`failed=provenance,source_row,table`; C2 "three tracepoints" table `events=8 rows=3 name_mismatch=5
failed=name_mismatch,source_row`.

## Findings

1. C1 before/after values in the receipts match the contract's before/after targets exactly; the frozen
   v1 (`e3ef425a…`) scores `PIN_CHECK=met` at the measured tip, rc 0.
2. v1 false-green contrast: `evidence/v1-junk/` shows the frozen v1 scores `PIN_CHECK=met` on five junk
   edits that keep the stale `pass=15` pin (`skill-v2-oldcopy`, `skill-v3-fakeecho`,
   `skill-v4-weakened`, `skill-v7-entrycopy`, `skill-v8-hide+dup`), rc 0 each; `skill-v5-renameprefix`,
   `skill-v6-deleted` and `skill-v0-frozen` stay unmet.
3. v2 hardened contrast: `evidence/v2/` shows v2 scores all seven junk variants unmet — `no_command=1`
   for oldcopy/fakeecho/entrycopy, `mismatches=1` for weaken/renameprefix, `dropped=1` for deleted,
   `unparsed=1 no_command=1` for hide+dup — and `skill-v0-frozen` unmet, `skill-v1-honest` met.
4. Selftest tallies: `evidence/selftest-pin-check.txt` (frozen v1 instrument) → `PIN_CHECK_SELFTEST
   pass=22 fail=0`, rc 0; the v2 tool's selftest prints `pass=34 fail=0` as observed inside both after
   receipts' pin rows (line 938). Both facts are recorded; the capability row below cites the v2 tally
   as observed in the after receipts.
5. C2: entering `C2=unmet failed=entry_absent,pins,source_row` → measured `C2=met events=8 rows=8` with
   all mismatch/row/provenance counters zero; at-freeze controls isolate the failure classes.
6. The measured commit for the section is `68d66ca`; the after-receipts were executed at `af2250d8`,
   whose tree equals T for every measured file (receipts committed at T).

## Draft — SCORECARD.md "## Round 47" section (fenced, ready for L1 integration)

```markdown
## Round 47 — registry pins re-measured from committed bytes (C1) and the v7.2 OOM tracepoint catalogue (C2)

L1 MoriR47, attempt 1. Entering tip `2d85e33d14198d388fd3cda9cc15ec07e57e7a53`; freeze `63eecf2738db96f46b0bd02b1b2dfd66787493d0`
(`.ufo/waves/round-47/contract.md`, both counters and the controls committed before any seat; frozen instrument
`tools/mori-pin-check.py` sha256 `e3ef425abde30974faf53a894f96650af11570d2125a5bf621395f6ab0d903e1`). Scores entering:
coverage 6, operability 7, depth 5, freshness 5, calibration 5, adjacency 6; both claims work a lowest (tied 5) axis.
No score change is claimed by the lane; the non-author closure rules.

Measured commit `68d66ca53d89be5c34a62f46af7c37449d9f9b63` (landed tip); the after-receipts were executed at
`af2250d8`, whose tree equals T for every measured file.

| Claim | Axis (held) | Counting command | Before (entering `2d85e33`) | After (measured at T) | Verdict proposed for the closure |
|---|---|---|---|---|---|
| C1 SKILL.md registry self-test pins reproduce from committed bytes | calibration 5 | `python3 <git show 63eecf27:tools/mori-pin-check.py> --rev R --min-tally-pins 26 --baseline-rev 2d85e33d…` | `PIN_CHECK=unmet tally_pins=26 digest_pins=5 mismatches=1 unparsed=0 no_command=0 dropped=0` (`SKILL.md:912` pinned `pass=15 fail=0`, tool prints `pass=22 fail=0`), rc 1 — `evidence/control-c1-donothing.txt` | `PIN_CHECK=met tally_pins=28 digest_pins=5 mismatches=0 unparsed=0 no_command=0 dropped=0`, rc 0 — `evidence/after-c1-v1-frozen.txt` | met under the frozen predicate, **with a disclosed limit**: wave 1 showed the frozen v1 also turns green on five junk edits (`evidence/v1-junk/`); the landed tip also passes the hardened v2 — `PIN_CHECK=met tally_pins=28 digest_pins=5 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0`, rc 0 (`evidence/after-c1-v2.txt`) — which scores every junk variant unmet (`evidence/v2/`) |
| C2 OOM tracepoint catalogue entry (FR13) | depth 5 | `python3 .ufo/waves/round-47/count-c2.py R` | `C2=unmet events=0 rows=0 name_mismatch=0 field_mismatch=0 callsite_mismatch=0 pin_mismatch=4 source_row=bad provenance=bad failed=entry_absent,pins,source_row`, rc 1 — `evidence/control-c2-donothing.txt` | `C2=met events=8 rows=8 name_mismatch=0 field_mismatch=0 callsite_mismatch=0 pin_mismatch=0 source_row=ok provenance=ok`, rc 0 — `evidence/after-c2.txt` | met; limits: prose and lifecycle claims are not counted, and a used-by survivor / indented-row miss are recorded (`corpus/lessons/round-47.md` M5) |

Controls that skip the work stay unmet (each scored with the frozen counter before data): C1 do-nothing
(`evidence/control-c1-donothing.txt`), deleted row (`dropped=1`, `evidence/control-c1-deleted.txt`), moved-cell
(`mismatches=1`, `evidence/control-c1-moved.txt`) and truncated pin (`mismatches=1`, `evidence/control-c1-truncated.txt`);
C2 do-nothing (`failed=entry_absent,pins,source_row`), the staged entry byte-exact
(`failed=provenance,source_row,table`) and the staged "three tracepoints" claim as a table
(`name_mismatch=5`), re-scored at the freeze commit (`evidence/control-c2-*-at-freeze.txt`).

### capabilities: first demonstrated round 47

| Capability | What it can now do | Evidence | First-working round |
|---|---|---|---|
| registry pin reconciler (v2) | re-run every tally and digest pin in SKILL.md's self-test cells from a `git archive` export of a revision and refuse rebinding, inline code, `.scratch` paths, weakened pins, stale echoes, duplicate or hidden rows | `python3 tools/mori-pin-check.py --selftest` → `PIN_CHECK_SELFTEST pass=34 fail=0` (observed in `evidence/after-c1-v1-frozen.txt:33` and `evidence/after-c1-v2.txt:33`); `evidence/after-c1-v2.txt`; `evidence/v2/` vs `evidence/v1-junk/` | 47 |
```

## Out-of-scope items

Applying the draft to `SCORECARD.md` (the working tree currently holds an uncommitted round-47 section,
written outside this seat), the `LOG.md` round-47 entry, and the closure verdict are L1 integration
surfaces, not this seat's. This seat wrote only its own report.

## Artifact paths (Report: trailer — relative to /home/vgpnk/Projects/shokunin/mori-shokunin)

Report: .ufo/waves/round-47/w2/ScribeScorecard.md

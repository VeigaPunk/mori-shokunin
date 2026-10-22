# ReviewA2SpecVsTool — spec-vs-tool review of the ten A2 rules

Seat: MoriR28.ReviewA2SpecVsTool (leaf; no subagents). Round 28 wave 1.
Tool reviewed: `tools/mori-oom-killers.py` at rev `6ebd518f10e53057da926353d99442d51267ccaf`, 824 lines.
Rule text: `.ufo/waves/round-27/contract.md:47-58` (frozen table A2-01..A2-10) and `.ufo/waves/round-26/contract.md:152-200` (amendment A2).
Method: `git clone --no-hardlinks` of the lane into my sandbox, detached at `6ebd518f`; every repro run as
`python3 -I -B <sandbox>/tools/mori-oom-killers.py --inputs <file>` (never `--selftest`, never against a lane case
file). 22 invented inputs under `/fast/scratch/hyaku/mori-r28/MoriR28.ReviewA2SpecVsTool/repro/`; all journal text
invented, no host values. No lane writes; this report is the only lane file I touched.

## Result table

| Rule | Tool lines (6ebd518f) | Divergence from rule text | Repro (sandbox) |
|---|---|---|---|
| A2-01 | `:120-121` marker, `:377-378` detect in-scope, `:391` scope_complete | none found | `r01` suppressed-in-scope → scope_complete false, KILLERS_UNKNOWN exit 2; `r01b` same line for another unit → scope_complete true, QUIET |
| A2-02 | `:196-212` state map (`:212` other→unavailable), `:452-453` unknown, `:432-435` acted | letter-level collisions (2): (a) unavailable state + earlier boot send → KILLER_ACTED not UNKNOWN — licensed by A2-06's "not active" wording at r26 contract :175-179, collide in blind-case space; (b) `LoadState=not-found` + `ActiveState=failed` → state `absent` not `unavailable` (LoadState checked first `:201`) | `r02` failed+send → state `unavailable`, earlier 1, ACTED exit 1; `r02b` failed+quiet → UNKNOWN exit 2; `r09b` not-found+failed → state `absent`, ACTED |
| A2-03 | `:118` prefix, `:375-376` count, `:423-425` null when actions null | none found; caveat: field is null for every non-active state, so a blind case pinning a count on an inactive unit mismatches by design | `r03` in-scope group line → process_group_lines 1; `r03b` inactive → null, group line not counted as send (earlier 1 from the sigterm line) |
| A2-04 | `:115` prefix, `:373-374` flag, `:383-387` move sigterm+sigkill only, `:329` treats escalation as send for earlier | ambiguity, likely breach of "never positive evidence": `escalating to SIGKILL after ` stays in `actions.escalations` and feeds `acted` (`:433`) inside a dry-run invocation; the tool's own earlier-invocation counter (`:329`) classes escalation among send lines, so the same line is a send in one rule and evidence in another | `r04` dryrun + 2 sends + escalation → dryrun_send_lines 2, escalations 1, ACTED exit 1; `r04b` dryrun + sends only → QUIET |
| A2-05 | `:215-218` parse, `:279-287` missing-or-0 → unbounded scoped set, `:391` scope_complete | none found | `r05` aetm absent → scope_complete false, send still counted → ACTED exit 1; `r07` uses aetm=0, same unbounded path |
| A2-06 | `:309-332` earlier split/count, `:435` evidence for non-active, `:480` report | none on stated shapes; mechanism boundary: attribution inside `earlier` keys only on version lines — a segment whose version line was rate-limited away merges into the previous segment and inherits its dryrun flag (both directions). Consistent with "split at each version line" but a suppressed delimiter silently folds invocations | `r06` inactive + send → earlier 1, ACTED exit 1; `r06b` active + earlier send → earlier 1 reported, QUIET exit 0 (no verdict change) |
| A2-07 | `:313-332` per-invocation dry-run split inside `earlier` only; `:373-374`+`:383-387` single `dryrun` flag over all of `scoped` | **breach**: the split never runs on `scoped`; any `dryrun mode enabled` anywhere in scope zeroes sigterm/sigkill of every segment in scope. One dry-run invocation zeroes another invocation's real sends whenever 2+ version lines fall in scope — aetm=0 (unbounded) or two version lines inside a bounded scope | `r07` aetm=0, send, version, dryrun, send → dryrun_send_lines 2, sigterm 0, UNKNOWN exit 2 (rule: real send stands → ACTED); `r07b` bounded, scope_complete true → QUIET exit 0 (rule: ACTED) |
| A2-08 | `:413-420` journal null → counts null, `:445-448` unknown, `:434` oomd evidence precedes unknown | no breach of the frozen law: frozen `c30` (`cases.json:709-718`) pins null journal + `oomd_notices>0` → ACTED, so "for any earlyoom state" binds the earlyoom state value, not other positive evidence. Blind-writer trap: pinning UNKNOWN with journal null + notices>0 mismatches by design | `r08` journal null + notices 1 → ACTED exit 1 (c30 shape); `r08b` notices 0 → UNKNOWN exit 2; `r08c` null show + null journal + notices 2 → ACTED |
| A2-09 | `:201-202` not-found→absent, `:403-411` non-active actions null, `:435` earlier sends acted | none found | `r09` not-found + send this boot → state `absent`, earlier 1, ACTED exit 1 |
| A2-10 | `:289-300` bounded branch: stamp-less → unplaced, skipped, scope incomplete (`:391`); holes: `:287` unbounded keeps every record, `:310-312` stamp-less falls into `earlier` | **breach, two shapes**: (a) unbounded scope (aetm missing/0): `scoped = list(journal)` keeps stamp-less records and the send-count loop counts them — record is counted, not "left uncounted"; (b) stamp-less records are excluded from `scoped` by identity (`:311`) and land in `earlier`, inflating `earlier_invocation_send_lines`; for a non-active unit that alone yields ACTED | `r10` bounded: stamp-less + junk-stamp sends uncounted, scope_complete false, oomd notice → ACTED (positive evidence stands — but earlier_invocation_send_lines shows the hole: 2); `r10b` aetm=0 + stamp-less send → sigterm 1, ACTED; `r10c` inactive + stamp-less send → earlier 1 → ACTED (rule: uncounted → QUIET/UNKNOWN) |

## Detail on the two breaches

### A2-07 — dry-run is not per-invocation inside `scoped`

The amendment (r26 contract :180-181) adopted the wave-2 fix: "dry-run is now applied per earlier invocation (split
at each version line), so one dry-run invocation no longer zeroes the real sends of another." The implementation
splits only the `earlier` list (`:320-330`); the scoped loop sets one boolean `dryrun` (`:373-374`) and the zeroing
at `:384-387` wipes sigterm+sigkill of *every* segment in scope. Minimal bounded repro (`r07b`, scope_complete
true — the most innocent-looking shape a blind writer can build):

```json
{"earlyoom_show": "LoadState=loaded\nActiveState=active\nUnitFileState=enabled\nActiveEnterTimestampMonotonic=1000000",
 "oomd_show": "LoadState=loaded\nActiveState=active\nUnitFileState=enabled\nActiveEnterTimestampMonotonic=100",
 "earlyoom_journal": [
  {"MESSAGE": "earlyoom 1.9.0", "__MONOTONIC_TIMESTAMP": 2000000},
  {"MESSAGE": "sending SIGTERM to process 1234 (bigproc), oom_score 100", "__MONOTONIC_TIMESTAMP": 2500000},
  {"MESSAGE": "earlyoom 1.9.0", "__MONOTONIC_TIMESTAMP": 3000000},
  {"MESSAGE": "dryrun mode enabled", "__MONOTONIC_TIMESTAMP": 3500000},
  {"MESSAGE": "sending SIGTERM to process 5678 (bigproc), oom_score 100", "__MONOTONIC_TIMESTAMP": 4000000}],
 "oomd_notices": 0}
```

Observed: `sigterm 0, dryrun_send_lines 2, KILLERS_QUIET exit 0`. Rule letter: the first send is a real send of a
non-dry-run invocation → positive evidence → `KILLER_ACTED exit 1`. The `r07` variant (aetm `0`, unbounded scope)
produces `KILLERS_UNKNOWN exit 2` on the same journal — still not ACTED.

### A2-10 — "left uncounted" only holds in the bounded branch

The superseded setup-error rule was replaced by "left uncounted and makes the scope incomplete" (r26 contract
:186-187). The tool implements exactly that inside `scope_known` (`:291-298`), but:

- `scoped = list(journal)` (`:287`) when aetm is missing/0 carries stamp-less records straight into the counting
  loop → `r10b`: sigterm 1, KILLER_ACTED on a record that is not countable.
- `earlier = [e for e in journal if id(e) not in scoped_ids]` (`:312`) — a stamp-less record is not in `scoped`,
  so it is swept into the earlier-invocation bucket and counted at `:329-330`. `r10c` (inactive unit): a lone
  stamp-less send yields `earlier_invocation_send_lines 1` → `KILLER_ACTED exit 1`; under the rule letter the
  record is left uncounted and the shape reads quiet/unknown.

The bounded branch itself is correct: `r10` shows the stamp-less and junk-stamp sends uncounted, scope_complete
false, and the oomd notice still producing ACTED — "positive evidence elsewhere still stands" holds.

## Verdict-ordering note for the L1

`acted` is computed before `unknown` is even consulted (`:432-436` vs `:438-458`): any positive evidence —
oomd notices, earlier sends — overrides every unknown trigger including null reads. That is frozen `c30`/`c29`
behaviour and consistent with the contract's "positive evidence stands" clause; the same ordering is what produces
the A2-02 collision in `r02` and the A2-08 trap above. Blind cases that pin UNKNOWN on top of positive evidence
will all mismatch the same way — this is a spec-reading pitfall, not a tool defect.

## Residual risk / gaps

- Escalation-vs-send vocabulary (A2-04) is genuinely ambiguous in the amendment; I flag rather than decide.
- Segment merge on a lost version line (A2-06) cannot distinguish "new invocation" from "same invocation"; noted
  as mechanism, no rule breach demonstrated.
- All probes are `--inputs` on invented JSON; the live collection path and A1c readability probe are out of scope
  per the r27 contract.
- Only rev `6ebd518f` was exercised; later tool edits in this wave are unreviewed here.

## Tooling

- python3 3.14.8 (host, stdlib only — no installs), git 2.56.0 (clone/checkout inside my scratch dir only).
- No packages installed or upgraded; pacman untouched per bounds.

Report: `.ufo/waves/round-28/w1/ReviewA2SpecVsTool.md`

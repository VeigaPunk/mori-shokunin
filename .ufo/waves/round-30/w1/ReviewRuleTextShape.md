# ReviewRuleTextShape — screening of `.ufo/waves/round-30/rule-text.md` before the case freeze

Seat: MoriR30.ReviewRuleTextShape (reviewer, leaf — no subagents used). Date: 2026-10-22.

Method and compliance: I read exactly one lane file, `.ufo/waves/round-30/rule-text.md` (114 lines,
verbatim extract at lane 58b61681a0e3f3b821a17d38a4e713ccd9921615). I did not open the tool, any case
file (frozen or draft), or any detector/evidence file. Every derivation below cites rule-text.md line
numbers only (`rule-text.md:NN`). No git/jj commands run. No tooling installed (operator directive
2026-10-19: nothing needed). This report is my only write in the lane.

## The question

Disputed shape: earlyoom `ActiveState=active`; `ActiveEnterTimestampMonotonic` absent or `0`; at least
two `earlyoom <version>` lines in the journal; at least one real send line (`sending SIGTERM to
process ` / `sending SIGKILL to process `) before the last version line; no send lines after the last
version line. What does the rule text alone force for verdict, exit, and the five named earlyoom fields?

Conditioning assumptions (the shape as given leaves these open; each changes specific fields if violated):

- the journal read is not `null` and every record has a numeric `__MONOTONIC_TIMESTAMP`
  (else `rule-text.md:112`, `rule-text.md:114`);
- no `Suppressed N messages from earlyoom.service` line in scope (else `rule-text.md:67-68`, `105`);
- `oomd_notices` is `0` — a value `>0` forces `KILLER_ACTED` via `rule-text.md:44-45` regardless of the
  earlyoom fork below, and a `null` oomd read forces `KILLERS_UNKNOWN` via `rule-text.md:46`;
- the send lines are real: no `dryrun mode enabled` line in the invocation that logged them
  (else `rule-text.md:75-76`, `108`);
- the version lines match the grammar, so `grammar` is `verified-1.9.0` (`rule-text.md:29`, `38`).

## Result table

| Field | Value from the text alone | Status | Deciding lines |
|---|---|---|---|
| `verdict` | `KILLER_ACTED` or `KILLERS_UNKNOWN` — Finding F1 | **unclear** | 25-26, 29, 44-48, 82-83, 84-88, 109, 110, 111 |
| `exit` | `1` or `2`, tracking `verdict`; `0` excluded — Finding F1 | **unclear** | 44, 46, 49-51 |
| `earlyoom.state` | `active` | decided | 37-38, 71-72, 106 |
| `earlyoom.scope_complete` | `false` | decided | 82-83, 109 |
| `earlyoom.actions.sigterm` | count of real SIGTERM send lines `N`, or `0` — Finding F3 | **unclear** | 32, 40-41, 44, 76, 108, 110 |
| `earlyoom.actions.sigkill` | `0` if the disputed sends are all SIGTERM; otherwise forks like `sigterm` | decided iff SIGTERM-only sends; else **unclear** | 32, 33, 41 |
| `earlyoom.earlier_invocation_send_lines` | `N`, or `0` — Finding F2 | **unclear** | 29, 82-83, 84-85, 110 |

Also decidable from the text (not asked, listed because the freeze needs them): `grammar` =
`verified-1.9.0` (29, 38); `actions` is a non-null object (49-51 reserves `actions: null` for an
inactive or absent killer); `dryrun` = `false` (36; no dry-run line in the shape); `version` = the
version string on the last version line (29: that line starts the current invocation).

## F1 (high — blocks a text-grounded freeze): the verdict forks on whether earlier-invocation sends count as positive evidence inside an unbounded scope

The text gives two mechanisms that agree in bounded cases and disagree here:

- M1 (scope): journal lines with `__MONOTONIC_TIMESTAMP` >= `ActiveEnterTimestampMonotonic`, current
  boot (25-26). With the property absent or `0`, every line of the boot passes the filter.
- M2 (invocation): an `earlyoom <version>` line is "the first line of an invocation" (29), so the sends
  before the last version line belong to earlier invocations, not the current one.

Reading A1 — `KILLER_ACTED`, exit 1:

- the sends pass M1 (25-26 with the property absent/0), and verdict 1 fires on "any earlyoom
  `sending SIG…to process` or escalation line in scope" (44);
- "Positive evidence stands even when the scope is incomplete" (45) is written for exactly the
  evidence-plus-`scope_complete:false` combination this shape produces;
- A2-06's "reported without a verdict change for an active one" (87-88, 110) stays literally true: the
  `earlier_invocation_send_lines` field does not change the verdict — the lines count through the
  ordinary in-scope send counters instead (32: "one action each");
- A2-07 (111) only has content if real sends of non-current invocations land in the main counters;
  under exclusive routing (reading A2) "one dry-run invocation does not zero another invocation's real
  sends" would protect lines that were never in the counter to begin with.

Reading A2 — `KILLERS_UNKNOWN`, exit 2:

- line 29 fixes invocation membership: the disputed sends are not lines of the current invocation;
  A2-06 routes them to `earlier_invocation_send_lines` (84-85, 110);
- for an active earlyoom that count is "reported but does not change the verdict" (87-88, 110) — read
  unqualified, the lines cannot surface as positive evidence anywhere, so `sigterm` stays 0 (this
  reading must treat A2-06's routing as exclusive; note A6 shows the drafters mark exclusions
  explicitly when they mean them — 75-76 says "`sigterm`/`sigkill` stay 0", A2-06 says nothing of the sort);
- no positive evidence remains, `scope_complete` is false by A2-05 (82-83, 109), and verdict 2's clause
  "earlyoom active but `scope_complete` false" fires (46-47) -> `KILLERS_UNKNOWN`, exit 2 (46).

Why the text cannot adjudicate: A2-06 was written against bounded shapes — its motivating anchors are
the stop-without-restart case and frozen `c02` (86-88). In a bounded boot the earlier sends are outside
the scope under either counting, so both readings agree there, and no sentence in the text says which
reading governs once A2-05 makes the scope unbounded and therefore sends-inclusive. A2-05 itself
(82-83) only sets `scope_complete`; it is silent on counting and verdict.

Reachable combinations: (`KILLER_ACTED`, `sigterm`=N, field=0) [invocation read as AEM-delimited],
(`KILLER_ACTED`, `sigterm`=N, field=N) [invocation read as version-delimited, additive counting],
(`KILLERS_UNKNOWN`, `sigterm`=0, field=N) [version-delimited, exclusive routing]. (`KILLERS_UNKNOWN`
with field=0) is unreachable: if nothing lies outside the current invocation, the sends are
current-invocation lines and count somewhere.

Excluded outcome: `KILLERS_QUIET`, exit 0. It requires "otherwise" (49-51); an active earlyoom with
`scope_complete` false always satisfies verdict 2's clause (46-47) when no positive evidence exists,
and any positive evidence gives verdict 1. The text as written cannot produce QUIET for this shape.

Freeze consequence: whatever the r30 blind row pins for this shape is a policy choice between A1 and
A2, not something a blind writer can derive from the rule text. Either the text gets a one-line erratum
before the freeze stating which reading governs when the scope is unbounded, or the counter must not
claim text-grounding for that row.

## F2 (high): `earlier_invocation_send_lines` — "outside the current invocation" has two delimiters in the text

- Reading B1 (version-delimited, favored): line 29 states invocation boundaries at the grammar level;
  the AEM is introduced only as the scope bound (25-26). The disputed sends precede the last version
  line, hence are "send and escalation lines of this boot outside the current invocation" (84-85, 110)
  -> field = N >= 1.
- Reading B2 (AEM-delimited): 82-83 says the missing/0 property "leaves the invocation unbounded" —
  read as delimitation, the current invocation spans the whole boot, no line is outside it, the field
  stays 0, and the sends are current-invocation lines (this reading forces verdict reading A1).

B1 is the stronger reading, but B2 is textually available, and the field is one of the observable
outputs the blind row must pin, so it inherits F1's freeze problem.

## F3 (medium): `actions.sigterm` / `actions.sigkill` co-fork with the verdict

- If all disputed sends are `sending SIGTERM to process ` lines: `sigkill` = 0 under every reading
  (32 routes SIGTERM sends to the sigterm action only; escalations count in `escalations`, 33 and 41,
  never in `sigkill`). Decided.
- `sigterm` (and `sigkill`, if a real SIGKILL send precedes the last version line): N under both
  ACTED readings, 0 under the UNKNOWN reading — the same A1/A2 fork as F1, so these fields cannot be
  pinned independently of the verdict.

## F4 (medium): the text excludes QUIET for this shape, but line 88 anchors writers toward it

Lines 87-88: "For an active earlyoom it is reported but does not change the verdict, because frozen
`c02` pins `KILLERS_QUIET` for that shape". The text never says whether c02's
`ActiveEnterTimestampMonotonic` is present or 0/absent. A blind writer who reads "that shape" as this
disputed shape will freeze `KILLERS_QUIET` — an outcome the text's own A2-05 plus verdict 2 make
unreachable (46-47 with 82-83, 109). Before the freeze, either state that c02's shape is the bounded
one, or expect QUIET-pinning errors in the blind writers' derivations.

## F5 (low): the superseded malformed-timestamp rule is still stated as live text

Lines 77-78 still instruct that a journal record without a numeric `__MONOTONIC_TIMESTAMP` "is a setup
error: `KILLERS_UNKNOWN`, exit 2". Lines 95-97 say that rule "is superseded", and A2-10 (114) is the
operative row (uncounted, scope incomplete, positive evidence elsewhere still stands). A writer
grepping for "malformed" or reading top-down can freeze exit-2 setup-error expectations that the text
itself withdraws. Any r30 blind-gate key should treat 95-97 and 114 as controlling. Outside the
disputed shape, but the same writers produce the other rows.

## F6 (info): fields the text does decide, with deciding lines

- `earlyoom.state` = `active`: the enum is at 37-38; A2-02 maps only "an `ActiveState` other than
  `active` or `inactive`" to `unavailable` (71-72, 106), so `ActiveState=active` maps to state
  `active`. Unique.
- `earlyoom.scope_complete` = `false`: 82-83 covers both "missing or `0`" explicitly; 109 is the table
  form. Note the base definition at 39-40 would call the version line "inside the scope" here (every
  line is); 82-83 records that this is a deliberate override ("before this, a version line alone set it
  true"). Unique — and the only field where two sentences point opposite ways with the winner named.
- Exit pairing when decided: verdict 1 -> exit 1 (44), verdict 2 -> exit 2 (46); setup errors also exit
  2 (52-53), so exit alone never disambiguates UNKNOWN-by-scope from UNKNOWN-by-null-read — a frozen
  row can pin (verdict, exit) pairs only, never the fired clause.
- A1c (69-70) is live-mode-only and cannot constrain frozen inputs-object cases; unreadable-journal
  behavior in the frozen file can only be pinned through `null` inputs plus A2-08 (112).

## Residual risk and verification gaps

- I did not run the tool or read any case file (bounds and assignment): which of A1/A2 the
  implementation actually takes is unknown to me, and is exactly what the frozen blind row will pin.
  [INFERENCE] Even if the implementation already resolves the fork, the rule text is the writers' only
  input, so F1-F4 stand regardless of what the code does.
- The count N (and any `sigkill` fork) depends on the exact send lines the fixture uses; I derived
  per-line rules, not a total, because the shape says "send line(s)" without fixing the signal mix.
- All conditioning assumptions are listed at the top; a fixture that violates any of them (suppressed
  line, null read, oomd notices > 0, dry-run flag) changes specific fields as cited per line.

No tool installs or updates were made (directive of 2026-10-19 recorded: none needed).

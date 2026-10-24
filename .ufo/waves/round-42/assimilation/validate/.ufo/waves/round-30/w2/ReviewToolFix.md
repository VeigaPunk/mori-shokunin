# ReviewToolFix — round-30 wave-2 falsify: judged tool fix 7aa77484

**Verdict: agree** — the fix at `7aa77484` implements exactly what round-29 rulings Judge11–13 declared tool
errors, complies with the round-30 rule text and the contract's fix bounds, is general logic rather than a
special-case for the three cases, keeps `actions: null` for every non-active unit, and the four older
self-tests pass at the measured tip `ad0f0474` (run by me from committed bytes, in a sandbox clone).

## Method and material

- Worked from committed bytes only. Lane tree was `713be294` (= `ad0f0474` + one wave-2 dispatch commit; two
  untracked scratch paths only). Sandbox clone of the lane at `ad0f04745ced2194e58c22a0d6b38131bee3e230`
  under `/fast/scratch/hyaku/mori-r30-w2/ReviewToolFix/lane`; all runs there; no lane writes, no subagents,
  no installs (none needed — recorded under Tooling below).
- Diff identity: `git show 7aa77484:.ufo/waves/round-30/evidence/fix-tool.diff` and the working-tree evidence
  file both sha256 `7eb603cf36826860cd03a5d49fc2b0383ee581ab6a2211ef2c387a1356f039db`. The tool is identical
  from `7aa77484` to `ad0f0474` (`git diff 7aa77484 ad0f0474 -- tools/mori-oom-killers.py` empty).
- Sources: the diff; round-29 rulings `.ufo/waves/round-29/w2/Judge11.md`, `Judge12.md`, `Judge13.md`;
  `.ufo/waves/round-30/rule-text.md` (extract of round-26 contract + amendment A2 table A2-01…A2-10); fixed
  reader source `tools/mori-oom-killers.py` at tip (scoping ~275–311, state map `unit_state` 191–211,
  verdict assembly 440–500); round-30 contract clauses at `:5-11` (C2), `:96-102` (mismatch judging), `:178-190`
  (fix bounds, declared `a66751b1` 2026-10-22T18:00:36-03:00, i.e. before the fix).

## Clause check — each hunk against the rulings and the text

**Hunk 1 (scope computed for non-active units; new `scope_bounded`).** Base computed the scope only when
`earlyoom_state == "active"`; the fix keeps that path (`earlyoom_state == "active" and (aetm is None or
aetm == 0)` → unbounded) and adds a general elif: any unit with a numeric nonzero
`ActiveEnterTimestampMonotonic` and a present `ActiveState` gets entries stamped ≥ the stamp placed in
scope (`scope_known` true only when actually `active`). This is the prerequisite for the version/grammar
rulings of all three judges: Judge11 (inactive, version at the boundary; `.ufo/waves/round-29/w2/Judge11.md`
lines 20–22), Judge12 (failed, version at the boundary; table rows 1–3), Judge13 (absent/not-found) — all
citing rule-text scope ≥ boundary and "`earlyoom <version>` → version". Sending evidence is not dropped
(malformed-stamp handling, `unplaced`, unchanged). The `ActiveState is not None` guard keeps the verdict
rule "a show text that lacks ActiveState" (Judge11's show is `not-found` with `ActiveState=inactive`
present; verified in the source: `unit_state` returns `unavailable` only when `ActiveState` is missing from
otherwise-readable text — my P7 probe).

**Hunk 2 (non-active branch no longer nulls version/grammar).** Removes `version = None` and
`grammar = GRAMMAR_UNVERIFIED`; keeps `thresholds = None`, `scope_complete = False`, `actions = None`,
`dryrun = False`. Implements Judge11's ruling rows (version "1.9.0", grammar "verified-1.9.0",
`.ufo/waves/round-29/w2/Judge11.md:20-21`) and the same rows in Judge12/Judge13. `actions: null` is kept —
the rule text requirement "An inactive or absent killer reports `actions: null` … never zero counts" holds
in every one of my 11 non-active probes (below).

**Hunk 3 (the nulling of `dryrun_send_lines`/`process_group_lines` is conditional).** Base zeroed nothing —
it *nulled* these counters whenever `actions` was null, which the judges ruled wrong for readable bounded
cases (Judge11 "tool error" on both fields; Judge12 same; Judge13 same). The fix keeps the nulling exactly
when the counters are genuinely unavailable: `journal is None` (A2-08), `earlyoom_show is None` (unreadable
show), or `not scope_bounded` (no retained nonzero boundary). Every judge-decided case has a readable show,
a journal, and a nonzero stamp, so all three get counts; every unbounded/unreadable probe of mine gets null.

**Hunk 4 (`acted` gains in-scope last-invocation sends for non-active units).** Base had
`earlyoom_state != "active" and earlier_send_lines` only; with hunk 1, sends of the *last* invocation now
land in `counts` instead of `earlier_send_lines`, so `counts["sigterm"]/["sigkill"]/["escalations"]`
must count as positive evidence or Judge12's `KILLER_ACTED` pin would regress. It does. Rule-faithful:
verdict rule 1 is "any earlyoom `sending SIG…to process` or escalation line in scope"; the fix counts
sends and escalations only, correctly *not* `kill_failed`/`low_memory_warnings` (my P2/P4b: quiet) and
correctly *not* dryrun-routed sends (A2-04/A2-07, my P1a/P1b: dry sends never evidence, pre-boundary real
send still acts). The active-unit path is untouched (`earlyoom_state != "active"` guard), so condition (2)
"may not turn any `KILLER_ACTED` of an older file into another verdict" is respected, and
`c2-differential.py` reports `acted_lost=0` over all 126 inputs and I ran it (below).

## Not a special-case for the three cases

No hunk mentions a state name except the pre-existing `active`/`inactive` classification, and no threshold,
state string, or case id is special-cased — the gate is the physical condition "readable show, present
`ActiveState`, retained nonzero stamp". I ran 12 invented probes through `tools/mori-oom-killers.py
--inputs` at the tip (shapes the three judged cases do not cover); all behaved per the rule text:
- P1a inactive, bounded, dry-run invocation + 1 dry send in scope → `KILLERS_QUIET` exit 0,
  `dryrun_send_lines=1`, `actions` null, version "1.9.0", grammar "verified-1.9.0" (A2-04 kept).
- P1b same + real send before the boundary → `KILLER_ACTED` exit 1, `earlier_invocation_send_lines=1`,
  dry sends still not evidence.
- P2 inactive, bounded, thresholds + `kill failed:` + low-memory lines only, no sends → `KILLERS_QUIET`,
  `thresholds` null (hunk 2 keeps it null for non-active), counters kept at 0.
- P3 inactive with stamp `0` (unbounded) → sends still found via `earlier_invocation_send_lines=1` →
  `KILLER_ACTED`; `dryrun_send_lines`/`process_group_lines` null (hunk-3 condition), version null.
  Evidence is not dropped on the unbounded path (no dead code path in hunks 3–4).
- P4a absent (`not-found`) with an escalation in scope → `KILLER_ACTED` (hunk 4 includes escalations, as
  the rule text does). P4b absent with only process-group/kill-failed/low-memory lines → `KILLERS_QUIET`,
  `process_group_lines=1` recorded but not positive evidence (verdict rule 1 lists sends/escalations only).
- P5 inactive with the stamp *property missing* → unbounded → counters null, send counted as earlier, acted.
- P6 inactive bounded with a journald `Suppressed …` notice in scope → quiet, `scope_complete` false, no crash.
- P7 show lacking `ActiveState` → `state` unavailable, **not** bounded (hunk-1 guard), counters null, send
  counted as earlier evidence, acted — the "show text that lacks ActiveState" verdict rule stays intact.
- P8 inactive bounded with one malformed-stamp record beside a valid in-scope send → `KILLER_ACTED`,
  `earlier_invocation_send_lines=0`, counters kept, `scope_complete` false (A2-10 generalized).
- P10 `ActiveState=reloading` (unavailable-but-named, beyond Judge12's `failed`) → bounded, `KILLER_ACTED`,
  version "1.9.0", `actions` null — the logic generalizes; it is not a `failed`-only carve-out.
- P11 inactive, bounded, version line of an earlier invocation + in-scope send → acted, version null —
  version is taken only from the last invocation, no boot-wide backfill.
- P9 active regression guard → unchanged: `actions` object with `sigterm:1`, `scope_complete` true,
  thresholds object, `KILLER_ACTED`.

Honest saturation note: P10 is an invented non-active *unreadable* shape (`reloading`); the contract's
differential bound (non-`active` readable ActiveState, `_a2.json` scope) was exercised only on the two older
cases `a2-02-earlyoom-activestate-deactivating` (ActiveState=deactivating) and
`a2-06-inactive-earlier-invocation-sends-acted`. My probes generalize the class by construction; that is an
inference from shared code shape, additionally supported (not proven) by the freeze-blindness of the r30 file.

## Determinism, no leakage, freeze-blindness

- The changed code path is deterministic: a journal entry maps to output fields only via stamp comparisons
  against the stamp from `earlyoom_show` and prefix matches; no unbounded loop with side effects, no dict
  iteration order feeding outputs, no time/env input (`read_inputs` is pure; verified by reuse of one pure
  function behind `--selftest`, `--inputs`, live mode, docstring at `tools/mori-oom-killers.py:238-247`,
  and identical selftest results across my runs).
- **Privacy invariant: output holds no message text.** No hunk touches `_entry_text`/`decode_message` or the
  redaction, so `MESSAGE` text still never enters state; the result carries exactly the contracted fields
  (`state`, `version`, `grammar`, `thresholds`, `scope_complete`, `actions`, `dryrun`,
  `dryrun_send_lines`, `process_group_lines`, `earlier_invocation_send_lines`, oomd pair, verdict). In
  particular no process name, uid, command line, or `--prefer/--avoid` expression appears: my probes fed
  realistic raw message text ("sending SIGTERM to process chrome", "killing whole process group 1234",
  "kill failed: Operation not permitted") and the printed output contained none of it — fields only. Also:
  version "1.9.0" and the counts are already in the schema; the version string is not message text capture.
  No host values were involved anywhere in this check.
- `read_inputs` is already pure per its docstring; the fix adds no I/O, no subprocess, no unit/journal
  change (read-only contract kept).
- The round-30 blind file is accepted by both tools: `MORI_OOM_KILLERS_SELFTEST: PASS 8/8`, exit 0, on the
  entering-tip blob `58b61681` (receipt `evidence/c2-freeze-selftest-base.txt`, run by the author at the
  freeze `db1ec469`) and on the changed tool (receipt `c2-freeze-selftest-fixed.txt`) — receipts include
  timestamps and sha256; both at commit `7aa77484`. The blind case file pins only four fields (contract :85)
  and all eight of its cases are `ActiveState=active`, so author-blindness (no writer saw the diff) is
  structurally plausible [INFERENCE]; the pins themselves are untouched by the diff (my differential: no
  `cases-a2-r30.json` case changed output at all).

## Differential — I ran the author's committed harness myself

`python3 -I -B lane/.ufo/waves/round-30/c2-differential.py 7aa77484` (the committed script, which reads
entering-tip blob `58b61681` vs blob at `7aa77484` over all 94 older + 32 blind = 126 case inputs):

    changed cases-a2.json a2-02-earlyoom-activestate-deactivating   ActiveState=deactivating exit 2->2 …
    changed cases-a2.json a2-06-inactive-earlier-invocation-sends-acted ActiveState=inactive exit 1->1 …
    changed cases-a2-r29.json r29-a2-10-inactive-lone-missing-stamp ActiveState=inactive exit 0->0 …
    changed cases-a2-r29.json r29-a2-10-failed-stamped-positive     ActiveState=failed    exit 1->1 …
    changed cases-a2-r29.json r29-a2-10-not-found-earlier-stamped-positive ActiveState=inactive exit 1->1 …
    inputs=126 changed=5 older_changed=2 older_disallowed=0 acted_lost=0

The allowed set is exactly "readable show, ActiveState not active"; `older_disallowed=0` and
`acted_lost=0`. The author's receipt `.ufo/waves/round-30/evidence/c2-differential.txt` (that receipt lands
at `2ec25cc`, i.e. *after* `7aa77484` — the commit body of `7aa77484` embeds the same summary "126 inputs,
5 changed, older 2 both non-active readable, KILLER_ACTED lost 0") matches my run on those five cases; this
file `0` lines at `7aa77484` is a cosmetic ordering nit only, since the full-output field changes are what
carry the check.

## Older self-tests at the measured tip (run by me)

From the sandbox clone at `ad0f0474`, `python3 tools/mori-oom-killers.py --selftest --cases …`:

| file | result | exit |
|---|---|---|
| `cases.json` | `PASS 32/32` | 0 |
| `cases-supplementary.json` | `PASS 32/32` | 0 |
| `cases-a2.json` | `PASS 30/30` | 0 |
| `cases-a2-r29.json` | `PASS 24/24` | 0 |

(round-30 blind file for reference: `cases-a2-r30.json` `PASS 8/8`, exit 0.) The base (parent-of-fix) tool
run on the *same committed* `cases-a2-r29.json` at the measured tip reproduces exactly the judged residual:
`FAIL 21/24`, failing precisely

    r29-a2-10-inactive-lone-missing-stamp        version/grammar/dryrun_send_lines/process_group_lines
    r29-a2-10-failed-stamped-positive            version/grammar/dryrun_send_lines/process_group_lines/earlier_invocation_send_lines
    r29-a2-10-not-found-earlier-stamped-positive version/grammar/dryrun_send_lines/process_group_lines

— each field exactly as ruled tool error by Judge11 (version, grammar, dryrun, process-group; verdict,
exit, earlier count already right), Judge12 (five fields), Judge13 (four fields; its fixed earlier count
already matched base-then). Base passes the other three files (32/32, 32/32, 30/30) and the blind r30 file
(8/8), so the fix's changed set is exactly the judged set.

## Findings

**F1 (minor, no action needed): receipt/commit ordering.** The judged-fix commit `7aa77484` embeds a
differential summary in its body, but its own `evidence/c2-differential.txt` is written by the next commit
`2ec25cc` (the file has 0 lines when shown at `7aa77484`). The round-30 contract requires "Receipt:
`evidence/c2-differential.txt`" alongside the residual-fix frame (`.ufo/waves/round-30/contract.md:190`), and
the landing-receipt orderigma is dealt with by the separate count-c2 gate — no contract condition reads the
differential receipt at the fix commit itself; `2ec25cc` is the stopping point of the same session. Cosmetic.
I verified the substance myself (differential run above), so no severity beyond "cosmetic ordering".

**F2 (observation, not a ruling violation):** for a *non-active* unit with a retained nonzero stamp whose
last invocation logs `dryrun mode enabled`, the output `dryrun` boolean stays `false` while
`dryrun_send_lines` counts the sends (my P1a). The rule text and all three rulings either leave `dryrun`
unpinned for non-active units or treat the flag through `dryrun_send_lines` only (A2-04, A2-07); the frozen
files pin `dryrun` only for active units. Behavior is unchanged from the base tool for the flag itself
(hunk 2 keeps `dryrun = False`). No defect; noted so the choice is visible.

**No defect found.** No hunk contradicts a ruling, the rule text, or a frozen case; the fix is general
(judged-class logic, not per-case); `actions: null` is kept for non-active units in every probe; the four
older self-tests pass at the measured tip; the blindness gate byte-identity holds; and the differential
loses no positive verdict and touches only permitted cases.

## Residual risk and verification gaps

- The scope-restore for non-active units rests on systemd retaining `ActiveEnterTimestampMonotonic` across
  a deactivation (the S157 fact in `corpus/lessons/round-30.md:6-11`); I did not re-verify S157 against the
  upstream doc this run — the three judges accepted the same premise, and the frozen entries S156–S160 carry
  the excerpts.
- My P10 (`reloading`) and P11 (version-line-outside-boundary) shapes are not pinned by any frozen case
  (none exists); their correctness is judged from the rule text + shared code path,
  [INFERENCE] for the unpinned output fields, though the verdict behaviors follow directly
  from the verdict rule.
- I did not re-run the round-30 `count-c1.sh`/`count-c2.sh` gates (out of my assignment; other seats cover
  them — the author's own C2-after receipt reports `blind_violations=1`, a gate-parser false positive on
  prose, per `.ufo/waves/round-30/evidence/c2-after.txt` and the lesson).
- No tool installs or updates were performed this run (none needed: python3, git, coreutils sufficed).

`Report:` .ufo/waves/round-30/w2/ReviewToolFix.md

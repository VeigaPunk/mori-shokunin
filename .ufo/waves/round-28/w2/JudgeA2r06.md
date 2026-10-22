# JudgeA2r06 — A2-06 pin rulings at f2de0ee

Verdict: **holds** — all three A2-06 cases' pinned values follow from the rule text; no `tool error`, `case error`, or `unclear text` ruling needed; no L1 tool change after the freeze.

Rule text attacked: `.ufo/waves/round-27/contract.md:54` (A2-06) and adopted form `.ufo/waves/round-26/contract.md:175-179`, with scope at round-26 :78-79 and verdicts at :97-103.

## Verification run (this seat)

- `bash .ufo/waves/round-28/count-c2.sh f2de0ee…` → `C2=met`, `freeze_commit=d21b8bd`, `cases_changed_since_freeze=0`, `a2_A2-06=cases=3 distinct=3 field=3`, `a2_selftest=PASS 30/30`, `a2_rule_checks=ok`. Matches freeze evidence `.ufo/waves/round-28/evidence/c2-freeze-selftest.txt` (PASS 30/30, exit 0, first tool run).
- `tool_blob_at_freeze=3fb78bbc…` == `tool_blob` at f2de0ee → tool unchanged since the case freeze; `git log -1` shows f2de0ee is the lane tip and `git status --porcelain` on the tool/cases is clean, so no post-freeze L1 tool edit exists to check.
- Reproduced on a temp extract of f2de0ee (`git archive` → /fast/scratch/hyaku/mori-r28-w2/JudgeA2r06/): `--selftest --cases cases-a2.json` → `PASS 30/30` exit 0; `--inputs` per A2-06 case → verdict, exit, and every `expect.fields` pin matched the pinned value exactly (39/39 field pins across the three cases).

## Per-case rulings

**a2-06-active-earlier-invocation-sends-quiet** (pins KILLERS_QUIET/0, `earlier_invocation_send_lines`=2): sends at 12.1M/12.2M < AETM 64M → outside the current invocation (round-26 :78-79) → count 2; active earlyoom → "reported without a verdict change" (A2-06; round-26 :178-179) → QUIET via rule 3 (round-26 :102). Version line at exactly 64M is ≥ AETM → `scope_complete`=true (:92-94); thresholds 12.5/12.5/6.25/6.25 from the current-invocation grammar lines (:83-85); all-zero actions and `dryrun`=false consistent with grammar rules. All 16 pins follow.

**a2-06-inactive-earlier-invocation-sends-acted** (pins KILLER_ACTED/1, `earlier_invocation_send_lines`=3, `actions`=null): `ActiveState=inactive` → "not active" → non-zero count is positive evidence (A-06; round-26 :176-177, "a stop without restart no longer reads quiet" — the why cites :177-178, the bullet text lands on :176-178). `actions: null` pins the rule-3 shape (round-26 :102-103). KILLER_ACTED correctly wins over the UNKNOWN list because rule 2 is conditioned on "**no** positive evidence" (:97-100). All 5 pins follow.

**a2-06-active-earlier-and-current-send-acted** (pins KILLER_ACTED/1, `earlier_invocation_send_lines`=1, `sigkill`=1): SIGKILL send at 8.1M ≥ AETM 8M → in-scope positive evidence (:97) → ACTED; earlier send at 3.05M → count 1 reported alongside per A2-06's active branch (:178-179). Separates the two counters as the why claims. All 18 pins follow.

## Residual notes (not rulings)

- Wording gap: A2-06 (round-27 :54) says "send lines"; the adopted text (round-26 :176) says "send and escalation lines". No A2-06 case pins an out-of-scope `escalating to SIGKILL` line, so no pin is contradicted; [INFERENCE] escalation-in-earlier-invocation coverage is untested — width note, not an error.
- No A2-06 case exercises `earlier_invocation_send_lines` combined with an unbounded/unscoped current invocation (A2-05 × A2-06) — again coverage width, not a pin defect.

No installs needed; used system `git`, `python3`, `tar` only.

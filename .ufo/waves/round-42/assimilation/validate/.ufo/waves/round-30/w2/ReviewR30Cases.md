# ReviewR30Cases — wave-2 falsify seat: the 8 frozen C2.3 cases vs rule text

**Verdict (one line):** `unclear text` on the `verdict`/`exit` pins of all 8 cases (a literal timestamp-scope reading of the rule text yields `KILLER_ACTED`/exit 1, contradicting the pinned `KILLERS_UNKNOWN`/exit 2); every other pinned field is decided by the text and correct; all 8 cases satisfy the C2.3 shape; no case errors found.

## Scope and method

- Judged the 8 frozen cases of
  `tools/fixtures/mori-oom-killers/cases-a2-r30.json` against `rule-text.md` only (task instruction; I did not read the tool). Rule text read with line numbers (`.ufo/waves/round-30/rule-text.md:1-114`).
- Verified shape per case with a Python check over the committed JSON (8 cases; each: `ActiveState=active`; stamp absent or `0`; ≥2 version lines; ≥1 send/escalation line all before the *last* version line; numeric non-decreasing timestamps; `LoadState=loaded`; `oomd_notices=0`; no `dryrun mode enabled` line; pins ⊆ {verdict, exit, state, scope_complete, sigterm, sigkill, earlier_invocation_send_lines}).
- Freeze identity: `git log --diff-filter=A` → `db1ec469` adds the file; `git log --format=%H -- <file>` lists only `db1ec469` (never modified after freeze); worktree `git hash-object` = `a05863cc` = `HEAD:<file>` blob.
- No tool installs were needed/run this seat; no tool run performed (text-decidedness judging only).

## Per-case findings (all 8, same disputed shape)

Each case: earlyoom `active` with stamp absent or `0`; N send/escalation lines before the final version line; nothing after. Expected fields, all cases:

| Field | Expected | Ruling | Rule-text citation |
|---|---|---|---|
| `earlyoom.scope_complete` | false | **decided** | `rule-text.md:82-83` (missing/0 stamp → unbounded → incomplete), `rule-text.md:109` (A2-05) |
| `earlyoom.state` | "active" | **decided** | `rule-text.md:37` (state values); input `ActiveState=active`; `rule-text.md:71-72` maps only non-active/active states to other values |
| `earlyoom.actions.sigterm` / `sigkill` | 0 | **decided** | `rule-text.md:84-86,110` (A2-06: sends of this boot outside the current invocation go to `earlier_invocation_send_lines`, not to actions); `rule-text.md:29` + `:111` (A2-07: invocation split at each version line) — no send follows the final version line |
| `earlyoom.earlier_invocation_send_lines` | 1 or 2 | **decided** | `rule-text.md:84-85,110` (counts send *and escalation* lines outside the current invocation); count = lines before the last version line, verified per case below |
| `verdict` / `exit` | `KILLERS_UNKNOWN` / 2 | **unclear text** | see below |

Case-by-case earlier-send counts (all match pinned integers):

1. `r30-disputed-missing-stamp-one-send` (a): 1 SIGTERM before last version → `earlier=1` ✓; `sigterm=0` ✓; stamp absent → `scope_complete=false` ✓.
2. `r30-disputed-missing-stamp-two-sends-warning` (a): 2 SIGTERM before last version → `earlier=2` ✓; `sigterm=0` ✓. The post-version `low memory!` line is a warning (`rule-text.md:35`), not positive evidence (`rule-text.md:44` only lists sends/escalations), so it does not force `KILLER_ACTED` ✓.
3. `r30-disputed-escalation` (b): 1 SIGTERM + 1 escalation before last version → `earlier=2` ✓ (escalation counts per `rule-text.md:85`); `sigterm=0`, `sigkill=0` ✓; stamp `0` → `scope_complete=false` ✓.
4. `r30-disputed-sigkill` (b): 1 SIGKILL before last version → `earlier=1` ✓; `sigterm=0`, `sigkill=0` ✓.
5. `r30-disputed-absent-clock` (c): 2 sends (SIGTERM, SIGKILL) before the last of 3 version lines → `earlier=2` ✓; `sigterm=0` ✓.
6. `r30-disputed-zero-clock` (c): 1 SIGTERM before last of 3 version lines → `earlier=1` ✓; `sigterm=0` ✓.
7. `r30-disputed-zero-stamp-kill-failed` (d): 1 SIGTERM before last version → `earlier=1` ✓; the `kill failed:` line (`rule-text.md:34`) is not a send/escalation, correctly excluded from the earlier count ✓; `sigterm=0` ✓.
8. `r30-disputed-absent-stamp-ordered` (d): 1 SIGTERM before last version → `earlier=1` ✓; `sigterm=0` ✓.

## The `verdict`/`exit` pins: unclear text (all 8)

Two readings of the rule text conflict on this exact shape:

- **Literal timestamp-scope reading → `KILLER_ACTED`/exit 1.** `rule-text.md:25-26` defines scope purely as a timestamp predicate: earlyoom lines with `__MONOTONIC_TIMESTAMP ≥ ActiveEnterTimestampMonotonic`. With the stamp missing or `0`, `rule-text.md:82-83`/`:109` leave the invocation "unbounded", so every journal line satisfies the predicate — including the pre-restart sends. `rule-text.md:44-45` then reads: any `sending SIG…to process`/escalation line **in scope** → `KILLER_ACTED`, exit 1, and positive evidence stands even when the scope is incomplete.
- **Invocation-partition reading → `KILLERS_UNKNOWN`/exit 2.** `rule-text.md:84-88`/`:110` (A2-06) commit sends of this boot outside the current invocation to `earlier_invocation_send_lines` and state that for an *active* earlyoom they are "reported but does not change the verdict". Excluding them from positive evidence, `rule-text.md:46-48` yields `KILLERS_UNKNOWN`, exit 2 (active + `scope_complete` false).

The rule text does not reconcile the two: line 25-26's scope predicate is unconditional in timestamp, while A2-06's "outside the current invocation" carve-out silently overrides it for the verdict without amending the scope definition. The contract itself concedes the ambiguity: `.ufo/waves/round-30/contract.md` A2 ("Disclosed, uncounted"): *"the rule text does not decide the disputed shape uniquely (ReviewRuleTextShape F1–F2: a literal scope reading gives `KILLER_ACTED`)"*, and *"the counted after-value is agreement of four blind writers and the tool, not a proof that the text decides the shape"*.

**Ruling:** per the mismatch-judging trichotomy (tool error / case error / unclear text), the `verdict`/`exit` pins of all 8 cases are **unclear text** — not case errors (the values are internally consistent and match the adopted A2-06 reading, and every mandatory pin `sigterm`/`earlier_invocation_send_lines` is text-decided), and not tool errors (no tool run performed this seat; a tool-verdict check is a separate seat's job). This matches the contract's own disclosure and therefore does not *itself* contradict C2.3's counted value, but it means the 8 cases do **not** independently prove the text decides the disputed shape — they encode agreement.

## Residual risk / verification gaps

- The `sigterm`/`sigkill`/`earlier_invocation_send_lines` pins are only "decided" because the A2-07 invocation split (`rule-text.md:111`) and A2-06 field (`:84-86,110`) are part of the rule text; a reader who rejected those amendments would also find the action-count pins unclear (the fields would then be undefined for the unbounded shape).
- I did not run the tool (out of seat scope per the task and bounds); the "agreement of writers and tool" claim for these pins must be checked by the tool-running seats.
- No case errors found: no pin outside the allowed set, no value inconsistent with the decided readings, no shape violation. All 8 pass the C2.3 shape (≥6 required; 4 distinct authors a–d present).

## Tooling record (operator directive 2026-10-19)

No tools installed or updated this seat; only read-only `git` (log/rev-parse/hash-object) and `python3` (stdlib `json`) used inside the lane / on the committed blob. No pacman transactions.

Final one-line verdict: **`unclear text` on all 8 cases' `verdict`/`exit` pins (literal scope reading gives `KILLER_ACTED`); all other pins decided and correct; C2.3 shape holds on all 8; no case errors.**

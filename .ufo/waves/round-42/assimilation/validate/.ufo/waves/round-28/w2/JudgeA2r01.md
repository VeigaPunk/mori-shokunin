# JudgeA2r01 — A2-01 amendment rulings

Verdict: **holds** — attacked rule A2-01 (`Suppressed N messages from earlyoom.service` in scope ⇒ `scope_complete` false) across its three blind cases at `f2de0eed`; every pinned value follows from the rule text, zero failing cases to rule, and the tool was not changed after the freeze.

## Scope of attack

- Rule text: `.ufo/waves/round-27/contract.md:49` (A2-01 row), adopted as A1b in `.ufo/waves/round-26/contract.md:158-159`; scope/verdict definitions `.ufo/waves/round-26/contract.md:78-106`.
- Cases: `tools/fixtures/mori-oom-killers/cases-a2.json` at `f2de0eedcd60d2e354da75265ea6122bc3896073` (blob `7ba553d4`), 30 cases total, 3 with `"rule": "A2-01"`.
- Freeze selftest: `.ufo/waves/round-28/evidence/c2-freeze-selftest.txt:3` — `PASS 30/30`, exit 0, run at freeze commit `d21b8bd3`.

## Do pinned values follow from the rule text?

**`a2-01-suppressed-in-scope-active-quiet`** — yes. Journal: version line `earlyoom 1.9.0` @42000000 (= `ActiveEnterTimestampMonotonic`, in scope per `:78-79` `__MONOTONIC_TIMESTAMP >=`), `Suppressed 42 messages from earlyoom.service` @42001234 (≥ boundary ⇒ in scope). A2-01 fires ⇒ `scope_complete: false` pinned, superseding the `:92-93` version-line default — consistent, since the rule exists precisely to override that default. No send/escalation line, `oomd_notices` 0 ⇒ no positive evidence (`:97`); earlyoom `active` with `scope_complete` false ⇒ `KILLERS_UNKNOWN` exit 2 (`:99-100`). `state: active` (`:90`), `version: 1.9.0` (`:82`), `dryrun: false` (no `dryrun mode enabled` line, `:89`), `oomd.state: inactive`, `notices 0` — all direct. `grammar`/`thresholds` correctly unpinned: the in-scope `Suppressed` line is a non-earlyoom-grammar line, so pinning `verified-1.9.0` would have been wrong.

**`a2-01-suppressed-before-scope-start`** — yes, and it is the load-bearing boundary case. `Suppressed 17 messages from earlyoom.service` @73499999 is one microsecond below `ActiveEnterTimestampMonotonic=73500000` ⇒ out of scope (`:78-79`), so the rule's `in scope` qualifier does not fire. The version line @73500000 is in scope ⇒ `scope_complete: true` (`:92-93`), `version: 1.9.0`, `grammar: verified-1.9.0` (`:91`: every in-scope line is a grammar line; the out-of-scope suppressed line cannot taint it). No positive evidence ⇒ `KILLERS_QUIET` exit 0 (`:102`). `thresholds: null` (`:91`, no threshold lines). Negative test of A2-01: passes only because the rule carries `in scope`.

**`a2-01-suppressed-in-scope-with-action`** — yes. `Suppressed 3 messages` @88000050 in scope ⇒ `scope_complete: false` (A2-01). The `sending SIGTERM to process <pid> "<invented-name>"` line @88000100 matches the send prefix `:85` ⇒ `actions.sigterm: 1`, `sigkill: 0`. Positive evidence ⇒ `KILLER_ACTED` exit 1 per `:97-98` — "Positive evidence stands even when the scope is incomplete" is exactly the pinned interplay: the rule degrades the scope flag, not the verdict. `oomd.state: active`, `notices 0` direct. `grammar` unpinned as above.

All three cases pin the suppressed-line unit qualifier literally (`from earlyoom.service`), matching the rule's wording — no case relaxes it to another unit name, so nothing in scope of this ruling tests a looser match. [INFERENCE: the writers' `why` texts cite `round-26/contract.md:158-159` for the rule and `:78-79` for scope; both citations check out against the committed text.]

## Rulings on failing cases

None. Freeze selftest `PASS 30/30` (`c2-freeze-selftest.txt:3`); no A2-01 case failed, so no `tool error` / `case error` / `unclear text` ruling is required. As a spot check I ran `python3 -I -B tools/mori-oom-killers.py --inputs` from a `git archive` extract of `f2de0eed` on all three A2-01 inputs (seat scratch `/fast/scratch/hyaku/mori-r28-w2/JudgeA2r01/`): verdicts/exits `KILLERS_UNKNOWN/2`, `KILLERS_QUIET/0`, `KILLER_ACTED/1`, every pinned field matched.

## Post-freeze tool change check

None exists. `git rev-parse` shows `tools/mori-oom-killers.py` is the same blob `3fb78bbc` at `d21b8bd3` (freeze) and `f2de0eed` (attack rev); `cases-a2.json` is the same blob `7ba553d4` at both. `git log d21b8bd3..f2de0eed -- tools/mori-oom-killers.py tools/fixtures/mori-oom-killers/` lists zero commits. The "turned no KILLER_ACTED into anything else on either case file" condition is vacuously satisfied — there is no diff to check.

## Residual risk / gaps

- Cases test `Suppressed` only with the exact `earlyoom.service` unit name and only relative to `ActiveEnterTimestampMonotonic`; a suppressed line at the same timestamp *after* an out-of-scope send line, or a `Suppressed … <other>.service` decoy, is unpinned (out of A2-01's literal text anyway).
- `grammar` on a suppressed-in-scope quiet case is unpinned by design; if the grammar rule itself were buggy, these cases would not see it — a different rule's cases cover that.

## Tooling record

No installs; used system `git`, `python3`, `tar` (all preinstalled). No pacman transactions attempted (host pause noted). Lane untouched: all reads via `git show`/`rev-parse`; extract ran under `/fast/scratch/hyaku/mori-r28-w2/JudgeA2r01/`.

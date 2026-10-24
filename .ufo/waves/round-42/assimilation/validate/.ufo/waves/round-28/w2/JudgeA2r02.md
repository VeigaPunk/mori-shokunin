holds — A2-02 (non-steady earlyoom `ActiveState` → `unavailable` + `KILLERS_UNKNOWN`): all 3 pinned cases follow from the rule text, tool output matches at f2de0ee, no post-freeze tool change, no failing cases to rule on.

# Scope

Amendment-A2 judge for rule A2-02 only. Sources read:

- Rule text: `.ufo/waves/round-27/contract.md:50` (frozen row A2-02); adopted wording
  `.ufo/waves/round-26/contract.md:162-163` ("an `ActiveState` other than `active` or `inactive`
  (failed, activating, deactivating, reloading, maintenance) maps to state `unavailable` and
  `KILLERS_UNKNOWN` (X5, X6)").
- Cases: `tools/fixtures/mori-oom-killers/cases-a2.json` at f2de0ee (bytes identical to freeze
  commit d21b8bd; `git log --reverse` shows d21b8bd is its only commit).
- Selftest evidence: `.ufo/waves/round-28/evidence/c2-freeze-selftest.txt:3` — PASS 30/30, exit=0.
- Tool: extracted via `git archive f2de0ee` to `/fast/scratch/hyaku/mori-r28-w2/judge-a2r02/`
  (lane never touched).

# Verification

- `git merge-base --is-ancestor d21b8bd f2de0ee` → yes; `git diff d21b8bd..f2de0ee --
  tools/mori-oom-killers.py tools/fixtures/mori-oom-killers/` → empty. No post-freeze tool or
  case change exists, so the regression audit is vacuous.
- Temp extract of f2de0ee: `python3 -I -B tools/mori-oom-killers.py --selftest --cases
  tools/fixtures/mori-oom-killers/cases-a2.json` → `MORI_OOM_KILLERS_SELFTEST: PASS 30/30`,
  exit 0; on the round-26 file `cases.json` → `PASS 32/32`, exit 0. No KILLER_ACTED expectation
  flips on either file (selftest would fail otherwise).
- `--inputs` run per A2-02 case; every pinned value reproduced exactly (see below).

# Per-case pin audit

Case 1 `a2-02-earlyoom-activestate-failed` (ActiveState=failed, AETM=0):
- `earlyoom.state: unavailable` — follows r26:162-163 / r27:50.
- `verdict KILLERS_UNKNOWN`, `exit 2` — follows r26:99. No positive evidence under r26:97: the
  `kill failed: ` line is a failed kill, not `sending SIG…to process` or an escalation;
  `oomd_notices` 0.
- `earlyoom.scope_complete: false` — follows r27:53 (A2-05): `ActiveEnterTimestampMonotonic=0`
  leaves the invocation unbounded. Consistent, though the pin rests on A2-05 not A2-02.
- `oomd.state: inactive`, `oomd.notices_this_boot: 0` — direct mapping of `ActiveState=inactive`
  and `oomd_notices` 0. All reproduced by `--inputs` (exit 2).

Case 2 `a2-02-earlyoom-activestate-deactivating` (ActiveState=deactivating, AETM=41880003,
oomd active):
- `earlyoom.state: unavailable`, `verdict KILLERS_UNKNOWN`, `exit 2` — follow r26:162-163 and
  r26:99; journal holds only threshold/status lines, no positive evidence under r26:97.
- `oomd.state: active`, `oomd.notices_this_boot: 0` — direct mappings. All reproduced (exit 2).

Case 3 `a2-02-earlyoom-activestate-activating-empty-journal` (ActiveState=activating, AETM=0,
journal `[]`):
- `earlyoom.state: unavailable`, `verdict KILLERS_UNKNOWN`, `exit 2` — follow r26:162-163 / r26:99;
  empty journal means no positive evidence. Empty `[]` is a successful read, not `null`
  (r26:73), so it does not trigger the null-read UNKNOWN clause; the verdict here comes from the
  state mapping alone — a correct and non-trivial distinction.
- `earlyoom.scope_complete: false` — follows r26:92-93 (no version line in scope) and r27:53
  (AETM=0 unbounded).
- `oomd.state: inactive`, `oomd.notices_this_boot: 0` — direct mappings. All reproduced (exit 2).

# Rulings

None. No failing cases exist (PASS 30/30 at both the freeze and the attack revision), so no
`tool error` / `case error` / `unclear text` ruling was required. All three cases' pinned values
follow from the rule text; the only unpinned-derivation note is that `scope_complete: false` in
cases 1 and 3 follows from A2-05 (r27:53) and r26:92-93, not from A2-02 itself — consistent and
correct, not a defect.

# Observations (not defects)

- Tool reports `earlyoom.grammar: "unverified"` and `scope_complete: false` in case 2 even
  though a version line sits at AETM. r26:92-93 makes a version line in scope a *necessary*
  condition for `scope_complete` true, not sufficient; treating a deactivating unit's scope as
  incomplete is defensible and the field is unpinned here. [INFERENCE]
- Case `why` fields cite the correct contract lines; spot-checked against r26:162-163, r26:99,
  r27:50.

# Residual risk / verification gaps

- I did not independently diff the tool's rule dispatch code; verification is behavioral
  (`--inputs` + selftest) plus the zero-diff tool provenance check. A latent divergence reachable
  only through input shapes outside the frozen cases is possible but out of A2-02 scope.
- `why` texts are truncated in my read (768-byte cap); the first ~700 bytes of each were verified
  against cited lines.

# Tooling

No installs. Used `git` (read-only archive/diff/log), `python3 -I -B` on the extracted tool.
Host pacman transactions paused per bounds; nothing needed installing.

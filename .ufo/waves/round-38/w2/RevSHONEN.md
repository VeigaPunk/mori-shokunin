# RevSHONEN — SHONEN.md seed fidelity and non-author `[x]` support (mori round 38, wave 2)

Scope: `mori-shokunin/SHONEN.md` vs the canonical seed in `../PROTOCOL.md` ("File contract per
shokunin repo", seed block at `PROTOCOL.md:439-448`), marks conformance, and which box a fresh
non-author verifier could check against this round's evidence. Detection only; no marks written.

## Verdict: PASS

- Seed diff = exactly the `<name>` line (allowed substitution; `<name>` = repo directory name
  `mori-shokunin`, per `PROTOCOL.md:432`).
- No mark on any box → no mark without a pointer.
- No `[x]` exists → no `[x]` without a named non-author verifier.

## Seed diff (mechanical)

Method: `sed -n '441,448p' PROTOCOL.md | sed 's/^    //' > /tmp/seed; diff -u /tmp/seed SHONEN.md`.

```
-# <name> — Promotion checklist
+# mori-shokunin — Promotion checklist
```

All other seven lines byte-identical (`cmp` reports first divergence at char 3 of line 1 — the
`<name>` substitution only). `mori-shokunin` equals the repo directory name; the file is otherwise
the canonical seed: 4 boxes, all `[ ]`, no evidence lines, no added/removed boxes, no prose.
`SHONEN.md` is unchanged this round — absent from `git diff --name-only e37dcc6..f725f307`.

## Current marks

| box | mark | pointer | canonical-form compliant |
|---|---|---|---|
| SKILL.md decision tables / error patterns / checklists / cited sources | `[ ]` | — | yes |
| end-to-end domain task executed and logged in `LOG.md` | `[ ]` | — | yes |
| instructions executable without oral context | `[ ]` | — | yes |
| no cross-domain bleed (`PROVINCE.md` still accurate) | `[ ]` | — | yes |

All four boxes are bare `[ ]` — the mint state. Conforms to "marks are confined to the box
character plus one indented evidence line per box" (`PROTOCOL.md:432`): there are none.

## Which box a non-author can check, with evidence

Gate rule under test (`PROTOCOL.md:63-66`): `[x]` requires a reviewer who did not author the
round's changes — a fresh lane or integrator review; **a subagent the lane dispatched is still the
lane**. I am `MoriR38.RevSHONEN`, a seat of the MoriR38 lane — my executions below prove the checks
are mechanical and reproducible, but cannot themselves count as the non-author check. The verifier
must be a sibling lane or the integrator.

### Box 3 — instructions executable by an agent without oral context — CHECKABLE NOW (primary)

Every printed command of the round ran verbatim from the lane root and reproduced its claimed
output, no oral context needed:

- `python3 .ufo/waves/round-38/count-c4.py f725f3076972e6e70595b5ac8279be524a111ff8` → `C4=met`,
  exit 0; negatives `witness-token-entry`/`witness-dangling-row`/`witness-summary-only-live`
  each `rejected`; checks `anchors`/`capability`/`live_rows`/`named_row_drift`/`drift_kill` PASS.
- `python3 .ufo/waves/round-38/conform.py f725f3076972e6e70595b5ac8279be524a111ff8
  --counter .ufo/waves/round-38/count-c1.py --counter .ufo/waves/round-38/count-c4.py` →
  `CONFORM=met`, exit 0; six checks PASS.
- `python3 tools/mori-sources-appendonly.py f725f3076972e6e70595b5ac8279be524a111ff8
  --round-base f10a320d` → `supersede_timing superseded_as_of=[S041,S044,S051,S062,S064,S069,
  S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] stale_supersede=[]`.
- `python3 tools/mori-sources-appendonly.py --selftest` →
  `MORI_SOURCES_APPENDONLY_SELFTEST pass=9 fail=0`, exit 0.

Receipts carry literal `command:` lines (routed debt 6 landed):
`.ufo/waves/round-38/evidence/c4-after.txt`, `c4-before.txt`, `c5-after.txt`, `gate-after.txt`,
`gate-selftest-after.txt`, `c1-before-rerun-memo.txt`, `c1-before-rerun-summary.txt` — a verifier
copies the line and runs it.

### Box 1 — SKILL.md contains real decision tables, error patterns, checklists, cited sources — CHECKABLE

- `SKILL.md:11` `## Decision table` (8 intent rows with correct surface / never / expected output);
  `SKILL.md:23` `## Error patterns` (~18 observation→reading rows); `SKILL.md:149`
  `## Checklist (executable)`; `SKILL.md:156` `## Gates` registry incl. the r38 row
  `SOURCES append-only timing (r38)` naming command `python3 tools/mori-sources-appendonly.py
  <rev> --round-base REV` and selftest `pass=9`.
- Cited sources: kernel/systemd upstream URLs (`oom_kill.c`, `oomd-util.c`, systemd catalog
  entries — `SKILL.md` error-pattern rows) and resolvable repo paths (`corpus/knowledge/*`,
  `tools/*`). Selftest above resolves the newest gate row end-to-end.

### Box 2 — end-to-end task executed and logged in LOG.md — CHECKABLE (freshest logging owed)

- `LOG.md` carries logged end-to-end rounds with receipts (e.g., `LOG.md:2109` Round 36,
  `LOG.md:2139` Round 37); `LOG.md:2186` is the round-37 correction appended this round naming the
  round-38 S069/S226 timed-supersede work.
- Gap: `grep -c '^## Round 38' LOG.md` → **0** — no `## Round 38` entry yet (round in flight).
  The box's "at least one" bar is met by prior entries; the newest evidence lands with the entry.
- `.ufo/reports/round-38/` does not exist yet — the `SHONEN`-heading assessment the contract
  requires of the lane report is still owed.

### Box 4 — no cross-domain bleed (PROVINCE.md still accurate) — PARTIAL; verifier must weigh recorded debt

- No-bleed half is provable: `git diff --name-only e37dcc6..f725f307` touches only lane files
  (`LOG.md`, `SCORECARD.md`, `SKILL.md`, `corpus/*`, `tools/mori-sources-appendonly.py`,
  `.ufo/*`); no sibling repo or fleet file touched.
- "Still accurate" half is contested by the lane's own record: `PROVINCE.md:386` ("Round-30
  correction") explicitly leaves open "sixteen `tools/` files and six fixture directories are not
  named here" and "the census citation `tools/mori-census.sh:211-212,282` at `:94` has drifted
  (the default now sits near `:237`, `:321`)". A non-author should not write `[x]` on box 4
  without resolving or explicitly scoping past that self-recorded stale-pointer debt.
  `PROVINCE.md` last changed at `af42101` (round 30).

## Residual risk / verification gaps

- The one-named-checkable-box answer: **box 3** (commands reproduce as printed); boxes 1 and 2 are
  also checkable with the pointers above. Box 4 carries an open accuracy objection the lane itself
  recorded — not wave-2's to resolve.
- All my command runs are same-lane seat executions; per `PROTOCOL.md:65` they establish
  reproducibility, not `[x]`.
- Round-38 LOG entry and lane report (with `SHONEN` heading) not yet landed — expected mid-round;
  flagged, not scored.

## Commands actually run

| command | result |
|---|---|
| `sed -n '441,448p' PROTOCOL.md | sed 's/^    //'` → `diff -u` vs `SHONEN.md` | 1-line diff (name) |
| `python3 .ufo/waves/round-38/count-c4.py f725f307…` | `C4=met` exit 0 |
| `python3 .ufo/waves/round-38/conform.py f725f307… --counter count-c1.py --counter count-c4.py` | `CONFORM=met` exit 0 |
| `python3 tools/mori-sources-appendonly.py f725f307… --round-base f10a320d` | `stale_supersede=[]` |
| `python3 tools/mori-sources-appendonly.py --selftest` | `pass=9 fail=0` |
| `git merge-base --is-ancestor f725f307… HEAD` | exit 0 (ancestor) |
| `git log --oneline -2` | `f725f30` tip, `daa1d4d` parent |
| `git log -1 -- PROVINCE.md` / `git diff --name-only e37dcc6..f725f307` | `af42101`; lane-files-only |
| `grep -c '^## Round 38' LOG.md` | 0 |

Tooling: none installed (python3/git/sed present; pacman untouched).

Report: .ufo/waves/round-38/w2/RevSHONEN.md

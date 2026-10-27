# Mo56RevSHONEN — SHONEN.md four-box check at freeze tip 8be2717b

Scope: resolve every cited pointer in `SHONEN.md` at
`8be2717b0809281d07dffe83dad424a4859e0747`, verify the round-56 instruments are
eligible pointers, propose the exact `[~]` line updates for round 56.
Vote-line protocol: this report contains no vote items.

## Method (all commands from lane root unless noted; TMPDIR was the seat scratch)

- `git rev-parse HEAD` → `acc62f54fb0f53b47b428594dc27365150cbd76b` (three wave-spec
  commits after the freeze tip; working tree carries uncommitted L1 integration
  drafts of `LOG.md`, `SCORECARD.md`, `SHONEN.md`).
- `git show 8be2717b:SHONEN.md` → 8 lines, four `[~]` boxes, all citing round-54
  pointers (SHONEN.md was last committed at round-54 integration `f111d4b0`;
  `git log --oneline -3 -- SHONEN.md`).

## Box-by-box pointer resolution at 8be2717b

### Box 1 — SKILL real content

Cited: `SKILL.md:1211`, `SKILL.md:1178`, `corpus/QUALITY.md:1479-1514`.

- `git show 8be2717b:SKILL.md | sed -n '1211p'` →
  `## Round54 — hardware memory-failure kills, and the v7.3 recheck of the remaining v7.2 rows`.
  Section heading; the decision table + error patterns follow in the section. Resolves.
- `sed -n '1178p'` →
  `## Round53 — the commit ledger as a runway read, and the v7.3 recheck`; the
  `### Commit runway by mode` table is at 1180ff. Resolves (heading-line convention,
  same as 1211).
- `corpus/QUALITY.md` at freeze: item 148 starts at line 1479; items 149, 150, 151
  start at 1497, 1509, 1511; **item 151 runs through line 1518** (blank) with item
  152 at 1520. The cited range `1479-1514` clips item 151 mid-sentence (its last
  ~4 lines, the `Shown able to fail`/`Not covered` arms, fall outside). Item 152
  was added at round-55 integration `a27ec482` (`git log -S` confirms), so the
  "(QUALITY 148-151; added at round 54)" parenthetical stays accurate; only the
  endpoint is off → `1479-1518`. DEFECT (see Findings F1).

### Box 2 — end-to-end domain task in LOG.md

- `git show 8be2717b:LOG.md` → `## Round 54` at line 2890 names C1 v7.3 recheck
  (31/31 status/line/quote, 31 voted) and C2 hardware memory-failure entry
  (21 located, 6 sources, 21 entailed). Resolves.
- `.ufo/waves/round-54/evidence/c1-at-landed.txt` →
  `C1=met scope=31 rows=31 matched=31 status_ok=31 line_ok=31 quote_ok=31 … voted=31 dissent=0 rev=f111d4b0…`, `exit=0`.
- `.ufo/waves/round-54/evidence/c2-at-landed.txt` →
  `C2=met claims=21 located=21 … entailed=21 dissent=0 rev=f111d4b0…`, `exit=0`. Both exist and contain the claimed content.

### Box 3 — executable instructions

- Round-54 receipts at freeze:
  `selftests/mori-pin-check.txt` → `PIN_CHECK_SELFTEST pass=125 fail=0`, exit 0;
  `mori-unlanded-check.txt` → `UNLANDED_SELFTEST pass=17 fail=0`, exit 0;
  `mori-commit-runway.txt` → `MORI_COMMIT_RUNWAY_SELFTEST: PASS 31/31`, exit 0.
  All three resolve.
- Re-run this seat (worktree tools are blob-identical to freeze:
  `git rev-parse 8be2717b:tools/<t>.py` == HEAD == `git hash-object` for all five tools):
  - `python3 tools/mori-pin-check.py --selftest` → `PIN_CHECK_SELFTEST pass=125 fail=0`, exit 0.
  - `python3 tools/mori-unlanded-check.py --selftest` → `UNLANDED_SELFTEST pass=17 fail=0`, exit 0.
  - `python3 -I -B tools/mori-commit-runway.py --selftest` → `PASS 31/31`, exit 0.

### Box 4 — no cross-domain bleed

- `git show 8be2717b:PROVINCE.md` → `## Round-54 appended scope notes` at line 458
  with the Boundaries note (no injection/unpoisoning, no `vm.memory_failure_*`
  writes; EDAC/rasdaemon/MCE is tsukuroi-adjacent host ground). Resolves.
- `corpus/knowledge/memory-failure-kills-r54.md` `## Boundaries` at line 81:
  no poison injection (`MADV_HWPOISON`, hwpoison-inject debugfs), no unpoisoning,
  no memory-failure sysctl writes; corrected-error accounting not held. Matches
  the box text.

## Round-56 instrument eligibility

- `python3 tools/mori-driver-liveness.py --selftest` →
  `DRIVER_LIVENESS_SELFTEST pass=13 fail=0 skipped=0`, exit 0 (this seat).
- `python3 tools/mori-vote-bind.py --selftest` →
  `VOTE_BIND_SELFTEST pass=16 fail=0`, exit 0 (this seat; matches
  `evidence/selftest-vote-bind.txt` at freeze).
- Frozen counters re-run read-only this seat:
  - `python3 .ufo/waves/round-56/count-c1.py 8be2717b…` →
    `C1=met selftest=ok fixtures=ok entry=ok row=ok norem=ok rev=8be2717b…`, exit 0.
  - `python3 .ufo/waves/round-56/count-c1.py acc62f54…` → same `C1=met`, exit 0.
  - `python3 .ufo/waves/round-56/count-c2.py 8be2717b…` →
    `C2=met selftest=ok tally=ok control=ok contrast=voted0 entry=ok row=ok rev=8be2717b…`, exit 0.
  - `python3 .ufo/waves/round-56/count-c2.py acc62f54…` → same `C2=met`, exit 0.
- Evidence files present at `8be2717b` (`git ls-tree .ufo/waves/round-56/evidence/`):
  `c1-at-freeze.txt`, `c2-at-freeze.txt`, `c2-old-counter-voted0.txt`,
  `census-start.txt`, `controls.txt`, `driver-liveness-live.txt`,
  `freeze-sha256.txt`, `selftest-c1-counter.txt`, `selftest-c2-counter.txt`,
  `selftest-vote-bind.txt`, `tally-r55.txt`. The worktree draft's cited files all exist.
- `tally-r55.txt` → `TALLY rows=78 agree=78 double=68 single=10 zero=0 dissent=0
  voters=16 bound_voters=15`, exit 0; `c2-old-counter-voted0.txt` → frozen r55 C1
  counter `voted=0 … failed=votes`, exit 1 (contrast confirmed).
- Knowledge entries: `corpus/knowledge/driver-liveness-r56.md` section is titled
  `## Limits (named before data)` (log-shape facts only; `*.round` state values
  never read; driver-authored lines are not authenticated). `vote-binding-r56.md`
  also `## Limits (named before data)` — first bullet: the binder proves a captured
  output *carried* a vote line, not who authored it (the "carriage, not
  authorship" claim in the draft is accurate; the heading name in the draft is
  not — see F2).
- Source rows: `corpus/SOURCES.md:324` S544 (own-work driver-line grammar, extract
  sha `38ba3e6b…`), `:325` S545 (RFC 8259, copy sha `61a5378f…`); both name the
  entries and tools, matching `freeze-sha256.txt` pins.
- Scope basis for an unchanged PROVINCE: `PROVINCE.md:6` owns "shokunin watchdog
  liveness (pid, start time, log…)" and `:22` names `.ufo/state/*.round` vs
  launch-ledger comparison; `corpus/README.md:345` (FR5 row) names the
  `.ufo/watchdog.log` launch/complete second-liveness-source ground this round
  claimed. The new probe reads log lines and `*.round` *shapes* only
  (`state_dir` in `driver-liveness-live.txt` reports file-type counts, never
  values) — a subset of already-owned ground; no appended PROVINCE note is needed.
- Worktree `LOG.md` (uncommitted L1 draft) has `## Round 56` at line 2950 naming
  C1 FR5 driver-liveness and C2 dual-shape vote binder — the box-2 `LOG.md`
  pointer resolves once the L1 commits it.

## Review of the uncommitted worktree draft (the L1's draft `SHONEN.md`)

The draft boxes 2–4 are directionally right but carry three pointer defects:

- F2 (LOW): box 4 cites `corpus/knowledge/driver-liveness-r56.md` "Boundaries";
  the entry's section is `## Limits (named before data)`. Cite `## Limits`.
- F3 (LOW): box 4 cites "kumitate settlement semantics untouched (wave connector
  check)". No connector-check artifact exists in `evidence/` or the wave
  directory; `w1-spec.json` defines connector seats but nothing named "wave
  connector check". The resolvable pointers are `corpus/README.md:343` (FR3:
  mori reports filesystem shape, kumitate owns orchestration/result semantics)
  and `:345` (FR5 ground claimed).
- F4 (LOW): box 2 cites `c1-at-freeze.txt`/`c2-at-freeze.txt` — both stamp
  `rev=3f494b49` (the freeze commit), not `8be2717b` (the freeze *tip* where the
  receipts landed) and not the eventual landed commit. This is the QUALITY-148
  stage-name class: honest naming, but the citation should either name the
  stamped rev or cite `*-at-landed` receipts produced at integration. Both
  counters re-verified `met` at `8be2717b` and `acc62f54` by this seat, so an
  at-landed receipt will print `met`.

## Proposed `[~]` lines for round 56

Exact replacement lines (integrator may drop the editorial notes in parentheses
it prefers; every pointer below was resolved by this seat):

```markdown
- [~] SKILL.md contains real decision tables, error patterns, checklists, cited sources — `SKILL.md:1211` (Round54 hardware-memory-failure table and error patterns), `SKILL.md:1178` (Round53 commit-runway table); `corpus/QUALITY.md:1479-1518` (QUALITY 148-151; added at round 54); `corpus/SOURCES.md:324-325` (S544 watchdog-log grammar, S545 RFC 8259; added at round 56)
- [~] At least one end-to-end domain task executed and logged in LOG.md — `LOG.md` Round56 (C1 FR5 driver-liveness probe; C2 dual-shape vote binder re-binding the round-55 tally); `.ufo/waves/round-56/evidence/c1-at-freeze.txt`, `c2-at-freeze.txt` (stamp `rev=3f494b49`; counters re-verified met at `8be2717b`/`acc62f54`), `driver-liveness-live.txt`, `tally-r55.txt`
- [~] Instructions executable by an agent without oral context — `python3 tools/mori-driver-liveness.py --selftest` (13/13), `python3 tools/mori-vote-bind.py --selftest` (16/16), `python3 tools/mori-pin-check.py --selftest` (125/125); round-56 receipts `.ufo/waves/round-56/evidence/selftest-vote-bind.txt`, `selftest-c1-counter.txt`, `selftest-c2-counter.txt`, `controls.txt`; round-54 receipts `.ufo/waves/round-54/evidence/selftests/mori-pin-check.txt`
- [~] No cross-domain bleed (PROVINCE.md still accurate) — `corpus/knowledge/driver-liveness-r56.md` `## Limits` (log-shape facts only, no health verdict, `*.round` state values never read); `corpus/knowledge/vote-binding-r56.md` `## Limits` (binding proves carriage, not authorship); `corpus/README.md:343,345` (FR3 kumitate owns settlement semantics; FR5 watchdog-log second-source ground); no appended PROVINCE note — read-only log-shape probe inside owns-scope watchdog liveness (`PROVINCE.md:6,22`)
```

Alternative for box 2 if the L1 produces `*-at-landed.txt` receipts at the
integration commit (preferred under the QUALITY-148 pattern): cite
`evidence/c1-at-landed.txt`, `c2-at-landed.txt` instead of the at-freeze pair.

## Observations (not defects; for the record)

- `controls.txt` `do-nothing-c2` PASS detail ends `…rev=5b295eee…` with no
  `failed=` visible: `controls.py:92` truncates `verdict[:110]`, and c2's longer
  field names push `failed=tool_absent` past column 110. The PASS decision
  evaluates the untruncated string (`want = "unmet" in verdict and "tool_absent"
  in verdict`), so the control is genuine; only the printed detail is clipped.
  c1's shorter field names keep `failed=tool_absent` visible.
- No verbatim `DRIVER_LIVENESS_SELFTEST` receipt file exists in `evidence/` —
  unlike `selftest-vote-bind.txt` and the two counter selftest receipts, the
  driver selftest survives only as the `selftest=ok` arm inside
  `c1-at-freeze.txt`. Asymmetric; the proposed box-3 line cites the receipts
  that exist rather than implying one that does not.
- The driver probe's top-level `verdict` field (`DRIVER_LIVENESS_OK` /
  `DRIVER_LIVENESS_UNAVAILABLE`) is a probe-availability report, not a per-lane
  health verdict — the selftest arm `t_no_health_verdict` asserts exactly those
  two values and the norem counter arm passes. Consistent with the claim; noted
  because the field name alone could misread as a verdict.

## UNVERIFIED / limits

- No LSP server applicable; all checks are byte-level `git show`/`ls-tree` plus
  direct tool runs (read-only).
- The box-2 `LOG.md` Round56 pointer is verified against the uncommitted
  worktree draft (line 2950); it resolves only when the L1 commits it.
- `w1-spec.json` connector seats were not re-run; the FR3/FR5 boundary is cited
  from committed `corpus/README.md` rows, not from a connector artifact.
- No tools installed; no report-receipt generation attempted (frozen items and
  L1-owned files untouched; only this report was written).

## Findings

- **MED** — `SHONEN.md` box 1 (at `8be2717b`, line 5): `corpus/QUALITY.md:1479-1514`
  truncates item 151, which runs to line 1518 (item 152 starts 1520). Correct
  range `1479-1518`; fixed in the proposed line above.
- **LOW** — worktree draft `SHONEN.md` box 4: cites `driver-liveness-r56.md`
  "Boundaries"; the entry's section is `## Limits (named before data)`
  (`corpus/knowledge/driver-liveness-r56.md:54` at `8be2717b`).
- **LOW** — worktree draft `SHONEN.md` box 4: "(wave connector check)" names no
  resolvable artifact; replace with `corpus/README.md:343,345` (FR3/FR5 rows).
- **LOW** — `evidence/c1-at-freeze.txt`, `c2-at-freeze.txt` stamp `rev=3f494b49`,
  not the freeze tip `8be2717b` where they were committed; a box-2 citation
  should name the stamped rev or use at-landed receipts (QUALITY-148 class;
  counters verified met at `8be2717b` and `acc62f54`).
- **LOW** — `.ufo/waves/round-56/controls/controls.py:92` `verdict[:110]` clips
  `failed=tool_absent` from the `do-nothing-c2` receipt detail (PASS logic is on
  the full string; observational only).
- **LOW** — no verbatim driver-selftest receipt in `evidence/` (asymmetry vs
  `selftest-vote-bind.txt`); box 3 should cite `c1-at-freeze.txt`'s `selftest=ok`
  arm or a receipt the L1 adds.

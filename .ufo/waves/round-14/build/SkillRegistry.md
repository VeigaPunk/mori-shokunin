# SkillRegistry — round 14

Seat: `MoriR14.SkillRegistry` (executor, leaf). Owned file: `SKILL.md` only.
Assignment: register the existing r13 regression gate and the new r14 gate under the full
PROTOCOL §Gate registry fields, remove false unregistered descriptions if present, keep self-test
commands actual with tallies pending rather than invented, and correct the journal
decision/error-pattern descriptions (OOM critical/DRIFT, fleet vs non-fleet routing, unknown
metadata, no absolute-trust/unique-kill overclaims). SHONEN.md and PROVINCE.md untouched.

No build, test, lint, format, smoke or gate/selftest command was executed (lane contract; L1 owns
post-integration verification). No tool was installed or updated. No commit, push, sibling-file,
MANIFEST/SHONEN or protected-verifier write was made. No delegation or background job was used.

## Axes named

- **coverage** — both verdict-producing gates now have a registry row, so a later reader can find
  and re-run them instead of reading them as unregistered harnesses.
- **calibration** — severities, owners and `unknown` classes are stated with their limits
  (notice ≠ unique victim, non-fleet = no marker, client-set IDs, unmeasured ≠ zero); no tally is
  asserted that this seat did not measure.

## Files changed

### 1. `SKILL.md` — Gates registry table (`:67-75`)

Added two rows using all eight PROTOCOL §Gate standard fields (name, kind, entry, verdict map,
self-test command and spelling, pinned values, write scope, owner):

- `r13 regressions` (`:74`) — entry `python3 tools/mori-round13-regressions.py --output <dir>`
  (`--census`/`--oracle` default to the repo `tools/*.sh`; `--frozen-dir` default
  `.ufo/waves/round-13/frozen`). Verdict map `0 clean · 1 failed · 2 could-not-evaluate`
  (usage/setup, unreadable target, `snapshot_tampered`, unbuildable requested mutation), matching
  the migrated file's own header `:119-125` where the old code 3 was folded into 2. Self-test
  spelling `python3 tools/mori-round13-regressions.py --selftest` with the r14-migration intent
  (real gate run over an isolated fixture asserting exit + stable expected id); tally explicitly
  **pending L1 measurement**. Pinned values: `.ufo/waves/round-13/frozen/inputs.json` digests, with
  the same-directory independence limitation stated, plus in-script expected ids; evidence names
  the measured revision and dirty flag. Write scope: `<dir>` only.
- `r14 regressions` (`:75`) — entry `python3 tools/mori-round14-regressions.py --output <dir>`
  (`--census` default `tools/mori-census.sh`; `--frozen` red-control default
  `.ufo/waves/round-14/frozen/mori-census.sh`). Verdict map `0 clean · 1 failed (claim failed, or
  the frozen control did not reproduce the defect) · 2 could-not-evaluate (usage/setup/pin,
  snapshot_tampered)`, read from the delivered docstring. Self-test `--selftest` (parsers plus the
  real gate over isolated fixtures, red rc1 / tamper rc2); tally **pending L1 measurement**. Pinned
  values: in-script `PINNED_SHA256` for the frozen census.

Updated the census row's self-test cell (`:71`) from the unqualified `91 cases measured at r13` to
`91 cases measured at r13 bytes; r14 tally pending L1 measurement` — the r14 repair changes the
census bytes, so the old tally is not the delivered gate's tally.

### 2. `SKILL.md` — Gate prose (`:79-108`)

- Journal-arm paragraph: keeps the twelve-query bound attribution at the r13 bytes and adds that the
  restored `OOM_KILL_JOURNAL` crit is one global alarm with four separate never-summed arms, not an
  authenticated or unique-victim count.
- New `**Regression gates (r14).**` paragraph (`:90-108`) describes both gates, their evidence tree,
  the frozen r13 census bytes pinned `39abda0a…`, the r14 gate's claim surface, and states that
  neither gate replaces the production census nor proves universal forgery resistance; tallies stay
  unstated until L1 measures delivered bytes.

### 3. `SKILL.md` — Decision table kill row (`:17`)

Names the structured surfaces (`UNIT_RESULT=oom-kill`, user `UNIT_RESULT=signal`), the single global
`OOM_KILL_JOURNAL` crit/DRIFT with its four counters, fleet `UNIT_FAILURE_JOURNAL` info vs non-fleet
`UNIT_FAILURE_OUT_OF_SCOPE` info `owner=tsukuroi`, unclassifiable
`UNIT_FAILURE_UNATTRIBUTED_JOURNAL` info `owner=unresolved`, and user
SIGKILL/`UNIT_RESULT=signal` `KILL_SIGNAL_JOURNAL` warn. The `Never` cell now says a notice is never
a unique victim. Raw pipes inside the cell were removed (`scope=user or scope=system`) so the table
still has the same five separators as its header (checked by pipe count: `:15-20` = 5 each).

### 4. `SKILL.md` — Error patterns (`:28-36`)

- `Positive cgroup oom_kill` (`:28`): added that the counter covers only the selected cgroup and is
  not a substitute for the journal `OOM_KILL_JOURNAL` alarm.
- `journal class counts` (`:30`): added the unit-SIGKILL and unit-failed catalog ids, the
  validated-field classes, multi-boot unavailability, and `drift=` = warning/critical FINDING
  lines, not records or kills.
- New `positive OOM notice … / UNIT_RESULT=oom-kill` row (`:31`): one global crit, four counters,
  explicit unknown arms (`*_unit_oom_result_unknown`), event-not-victim and client-set-ID limits.
- New `fleet vs non-fleet unit failure` row (`:32`): INFO on both sides; exactly one valid subject
  field independent of scope; `classification_rule=unit-name-token` over the five historical
  tokens; non-fleet means no marker; no emitter-field fallback; system id is new fleet-only
  semantics, not a silent reuse.
- New `unit subject absent, malformed, or ambiguous` row (`:33`):
  `UNIT_FAILURE_UNATTRIBUTED_JOURNAL`/`_SYSTEM`, info, `owner=unresolved`,
  `reason=subject-metadata-unknown`; both fields present is unknown even when identical.
- New `user UNIT_RESULT=signal` row (`:34`): one warn line with separate `process_sigkill` and
  `unit_signal` counters; generic `signal` is not signal-9 proof; system scope keeps no such warn;
  other signals / no retained record stay unknown.
- New `JOURNAL_CLASSES_UNMEASURED` row (`:35`): retired text heuristics vs unimplemented structured
  field vs possible no-retained-record, replacing any categorical "no structured field" reading.
- `a kill needs PID / uid / cgroup / time` (`:36`): added that the OOM alarm and the result-subtype
  are alarms, not victim attribution.

### 5. `SKILL.md` — bounded verdict-contract scope (`:154-169`) and routing payload (`:189-197`)

Per the L1 correction, the Round 13 paragraph is retitled `(bounded D01/D02 repair)` and now states
that only audit D01/D02's named long-history membership and BANANA/final-roll mechanisms are
repaired; arbitrary tally corruption, aggregate/registry-count vacuity and adaptive output forgery
remain outside the demonstrated repair, so it is neither full audit closure nor universal-forgery
resistance. The F01 whole-function transplant and reconstructed F02 prefix shim are named as bounded
mutation witnesses, not original-byte restorations.

The new `Journal routing payload (r14)` paragraph makes `UNIT_FAILURE_OUT_OF_SCOPE` the Tier-1
pointer (`owner=tsukuroi`, info, validated count, no echoed unit text, no Tier-2 instruction) and
`UNIT_FAILURE_UNATTRIBUTED_JOURNAL` information-only with `owner=unresolved`, and says the OOM crit
is an operator-visible alarm, not a remediation order.

## Exact retained evidence

All commands below were executed by this seat (read-only). Nothing was re-run for confirmation.

1. Gate registry before edit: `grep -n '## Gates' SKILL.md` → `61`; table (`:64-68` before edits)
   listed census, drift pin, silence oracle only — this is the r13 spotcheck's conformance defect
   (`corpus/lessons/round-13-verifier-spotcheck.md`: "`tools/mori-round13-regressions.py` is a
   committed verdict-producing checker ... but SKILL.md:64–68 registers only census, drift pin and
   silence oracle").
2. r13 harness declared state, read from delivered bytes: header `:4` `REGISTERED GATE (registry
   home: this lane's SKILL.md; row `r13 regressions`)`; `:119` `Exit codes (declared registry map:
   0 clean · 1 failed · 2 could-not-evaluate)`; `:216` CLI `--census`, `--oracle`, `--output`
   (required), `--baseline`, `--mutation`, `--shonen`, `--frozen-dir`, `--timeout`, `--jobs`,
   `--seed`, `--nonce`, `--keep-fixtures`, `--selftest`.
3. r14 gate declared state, read from `tools/mori-round14-regressions.py:1-90`: `Exit 0` every
   claim satisfied and frozen control reproduced the defects; `Exit 1` claim failed or control did
   not reproduce; `Exit 2` usage/setup/pin; defaults `DEFAULT_CENSUS=tools/mori-census.sh`,
   `DEFAULT_FROZEN=.ufo/waves/round-14/frozen/mori-census.sh` (`:102-104`).
4. Pinned frozen digest: `sha256sum .ufo/waves/round-14/frozen/mori-census.sh` →
   `39abda0a67028575d888d9157b8548dec0b4944c3d8c165691e88ab657fc3985`, byte-identical to the r13
   delivered census named in the r13 spotcheck table. Production census at read time:
   `47ef93bc…` then `3ff941c8…` mid-flight (see Risks).
5. Delivered census interface, read from `tools/mori-census.sh`: one global alarm
   `emit_finding OOM_KILL_JOURNAL crit ... counters user_notice/system_notice/user_unit_oom/
   system_unit_oom ... never summed` (`:1320`); user warn line `KILL_SIGNAL_JOURNAL warn ...
   process_sigkill=$ps unit_signal=$us ... never summed` (`:1346`); unattributed ids
   `UNIT_FAILURE_UNATTRIBUTED_JOURNAL` / `_SYSTEM` with `owner=unresolved
   reason=subject-metadata-unknown` (`:1277,:1279`); `FLEET_UNIT_TOKENS='shokunin|ufo-sighting|
   tmux-spawn|the-tick|fleet'` and `classification_rule=unit-name-token` in the header
   (`:920-1000`); `JOURNAL_CLASSES_UNMEASURED` reason split at `:1163`.
6. Canonical L1 interface: `.ufo/waves/round-14/scoped-counter-contract.json` `.l1_interface_ruling`
   — one OOM crit with four counters, info both routing sides, `UNIT_FAILURE_UNATTRIBUTED_JOURNAL`
   info `owner=unresolved`, exactly one valid subject field (both present = unknown even when
   identical), token rule without exhaustive-membership claim, drift counts warning/critical lines.
7. Table integrity after edits: `grep`-based content review plus a pipe-count check (`awk` over
   `^\|` lines) — decision rows 5 pipes, error rows 3, gate rows 9, owner rows 5, i.e. consistent
   with each header. The two `scope=user|system` cell texts were rewritten to
   `scope=user or scope=system` and the id suffix form.
8. `git status --porcelain` before my edit showed sibling-owned modifications
   (`LOG.md`, `PROVINCE.md`, `SCORECARD.md`, `corpus/*`, `tools/mori-census.sh`,
   `tools/mori-round13-regressions.py`, new r14 files). This seat added only `SKILL.md`; no
   `tools/` bytes were touched.

## Measured vs pending (no invented tally)

- Measured: registry-field facts above, digests, CLI spellings, delivered finding ids/fields.
- **Pending L1 measurement:** census `--selftest` tally on the r14 census bytes; r13 gate
  `--selftest` tally on the migrated harness bytes; r14 gate `--selftest` tally. The r13 spotcheck
  recorded 91 census cases at the r13 bytes; that number is retained with its revision attribution
  only. The earlier "24 checks at `80bd58a`" r13-harness selftest is not carried into the row.

## Risks and open items

1. **Both harnesses were in flight when read.** `tools/mori-round13-regressions.py` was modified
   (header migrated, exit 3 folded into 2, selftest strengthening not yet visible at the time of my
   last read: `def selftest` at `:1976` still pure and `GATE not-registered` strings remained at
   `:1956,:1970,:2115`). The registry row states the migration target the parent named (real
   isolated self-invocation with exit + stable id). If HarnessMigration's delivered `--selftest`
   stays helper-only, the row overstates the delivered bytes and L1 should treat it as a routed
   conformance defect. Likewise `tools/mori-census.sh` changed twice while I inspected it
   (interface header + global alarm present; all six scoped counts and the r14 split read as
   described).
2. **Frozen-digest independence (r13 gate).** `inputs.json` sits beside the frozen files it
   digests, so a coordinated edit is not detected; the registry row says so rather than claiming
   the PROTOCOL G6 independence property. The r14 gate pins its red-control digest in-script.
3. **`corpus/knowledge/journal-alarm-routing-r14.md` landed during this seat's run** (untracked at
   final read). Its rulings match the SKILL text: one global `OOM_KILL_JOURNAL` critical per census
   (`:12`), fleet `UNIT_FAILURE_JOURNAL` INFO "the historical fleet severity, not WARN" (`:107`),
   non-fleet INFO with tsukuroi owner (`:113`), unattributed INFO for absent/ambiguous/dual-presence
   subject metadata (`:116,:212-214`), one user-scope `KILL_SIGNAL_JOURNAL` WARN with two separate
   counters (`:191-197,:294`), and no unique-victim/authenticity claim (`:66,:223,:278`). Citations
   at SKILL `:30` and `:35` therefore resolve; this is a filename/consistency check, not a
   behavioral gate run.
4. **No claim of audit closure.** The registry rows describe gate mechanics; the emitted red/green
   evidence is L1's to measure, and the verdict-contract paragraph explicitly bounds D01/D02.

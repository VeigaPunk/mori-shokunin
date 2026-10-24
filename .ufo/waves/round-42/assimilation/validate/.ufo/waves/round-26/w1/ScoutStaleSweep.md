# Scout stale sweep — C1 completeness attack (round 26, wave 1)

Seat: `MoriR26.ScoutStaleSweep`. Date: 2026-10-22. Lane HEAD `5e5e86f`; contract `28b0494`;
entering tip `248408f5`. Working tree clean for tracked files (only untracked `.scratch/` and
`.ufo/waves/round-26/w1/`). This seat wrote nothing except this report; it ran no pacman
transaction, started/stopped no unit, and used no browser or bot-challenge workaround.

## Host capture (read-only, run 2026-10-22)

```text
$ uname -r
7.2.11-arch1-1
$ systemctl --version | head -1
systemd 262 (262-1-arch)
$ systemctl is-active earlyoom.service
active
$ systemctl is-enabled earlyoom.service
enabled
$ systemctl show earlyoom.service -p ActiveState,UnitFileState,ActiveEnterTimestamp
ActiveState=active
UnitFileState=enabled
ActiveEnterTimestamp=Thu 2026-10-22 04:55:44 -03
$ systemctl is-active systemd-oomd.service
inactive
$ systemctl is-enabled systemd-oomd.service
disabled
$ systemctl show systemd-oomd.service -p ActiveState,UnitFileState,ActiveEnterTimestamp
ActiveState=inactive
UnitFileState=disabled
ActiveEnterTimestamp=
$ pacman -Q earlyoom systemd          # query only, no transaction
earlyoom 1.9.0-1
systemd 262-1
$ uptime -s
2026-10-22 04:55:40
```

Counts only (no journal `MESSAGE` text emitted):

- earlyoom journal lines this boot: `13`; one version line reads `earlyoom 1.9.0`; two
  threshold lines present.
- systemd-oomd notice records (`d989611b…`): `0` system, `0` user; also `0`/`0` without `-b`.

## Method and limitations

- Fixed-string and regex sweeps over all 34 files in `corpus/knowledge/`, plus
  `corpus/README.md`, `SKILL.md`, `PROVINCE.md`, `SCORECARD.md` (round-26 section
  `:1588-1604` and whole-file `earlyoom|oomd|systemd` hits), and lane-root `README.md`,
  `AGENTS.md`, `MINT.md`, `SHONEN.md`, `LOG.md`; repeated over the whole lane excluding
  `.ufo/` and `corpus/evidence/`. Dated receipts skipped as instructed.
- C1 count at HEAD: `stale_present=4` — matches the declared before-value.
- The `lsp` device is not present in this seat's tool set; markdown corpus text has no
  language-server definition/reference graph. Findings rest on committed text plus the live
  read-only commands above, with fixed-string counts for coverage.
- Inclusion rule: a statement counts as stale when it asserts or implies a *current* host
  state and a 2026-10-22 command contradicts it. `verified-at` snapshots and explicit
  historical corrections are dated records, not claims.

## A. Frozen C1 phrases (covered)

| Id | Path:line | Text (short) | Host now | Verdict |
|---|---|---|---|---|
| F1 | `corpus/knowledge/userspace-oom-killers-r12.md:6` | `On this host both services are inactive` | earlyoom active; oomd inactive | stale, frozen |
| F2 | `corpus/knowledge/userspace-oom-killers-r12.md:14` | `` `systemctl is-active earlyoom.service` → `inactive` `` | `active` | stale, frozen |
| F3 | `corpus/knowledge/userspace-oom-killers-r12.md:18` | `Both service units are inactive` | earlyoom active | stale, frozen |
| F4 | `corpus/README.md:34` | `inactive on this host` | earlyoom active | stale, frozen |

## B. Additional contradicted present-tense statements, NOT in the frozen list (6)

| # | Path:line | Text (short) | Contradicting command and output | Why not covered |
|---|---|---|---|---|
| 1 | `corpus/knowledge/userspace-oom-killers-r12.md:3` | recheck expected outputs `…; inactive; inactive; 0; 0` | `systemctl is-active earlyoom.service` → `active` | recipe annotation; second `inactive` is the earlyoom slot; frozen list has no line-3 phrase |
| 2 | `corpus/knowledge/userspace-oom-killers-r12.md:14` | `` `systemctl is-enabled earlyoom.service` → `not-found` `` | `systemctl is-enabled earlyoom.service` → `enabled` | F2 freezes only the `is-active` value |
| 3 | `corpus/knowledge/userspace-oom-killers-r12.md:18` | `earlyoom's service unit is not found` | `systemctl is-enabled earlyoom.service` → `enabled` | F3 freezes only `Both service units are inactive` |
| 4 | `corpus/knowledge/journal-alarm-routing-r14.md:67-68` | `host systemd 261 equivalence is not established` | `systemctl --version` → `systemd 262 (262-1-arch)` | different file; C1 never touches r14 |
| 5 | `corpus/knowledge/journal-alarm-routing-r14.md:290` | `matches host systemd 261` | same | different file; open-unknown list still names 261 |
| 6 | `corpus/knowledge/journal-alarm-routing-r14.md:342` | `host systemd is 261` | same | different file; plain present tense |

Notes on B:

- B2 and B3 sit on lines that a wholesale dated rewrite of F2/F3 would probably remove, but
  C1's counting command does not require it. A minimal phrase-only rewrite leaves both.
- B1 is outside the rewritten lines entirely: the `recheck:` header's own expected values
  become self-contradictory (a re-run now prints `active`), so the note is no longer
  reproducible from its own recipe.
- B4-B6 are the only present-tense host systemd-version claims found; all say 261 while the
  installed version is 262. r14 was verified 2026-10-20, the same day as the recorded
  261.2-1 → 262-1 upgrade (`corpus/knowledge/journal-cursor-window-r16.md:144`), so these
  were already time-sensitive when written.

## C. Dated records and matching statements (fine, not stale)

| Path:line | Text (short) | Status |
|---|---|---|
| `corpus/knowledge/userspace-oom-killers-r12.md:2` | `verified-at: 2026-10-19 (… host kernel 7.2.3-arch1-3, systemd 261 (261.2-1-arch))` | dated snapshot; kernel/systemd differ today, correctly dated |
| `corpus/knowledge/oom-kill-counter-kernel-only-r12.md:2` | same `verified-at` line | dated snapshot |
| `corpus/knowledge/kernel-oom-line-attribution-r12.md:2` | same `verified-at` line | dated snapshot |
| `corpus/knowledge/kill-classes-by-message-id-r12.md:2` | same `verified-at` line | dated snapshot |
| `corpus/knowledge/verdict-machine-r6.md:178,271` | `Linux 7.2.3-arch1-3` | round-6 measured environment; dated by round-6 receipts |
| `corpus/knowledge/journal-cursor-window-r16.md:140-146` | `historical 261.2-1 … not today's current-version claim`; records `261.2-1→262-1` | explicit historical correction |
| `corpus/README.md:363,375-376` | `historical 261.2-1, not today's 262-1` | explicit historical framing |
| `corpus/README.md:41` | r16 provenance `host systemd 261.2-1 --help/man checks only` | describes the r16 measurement; dated by round, disambiguated at `:363,375`; weakest framing, not a live claim |
| `corpus/knowledge/journal-positive-evidence-r15.md:322` | `the host may run a different systemd version` | hedged; no claim |
| `corpus/knowledge/system-pressure-r24.md:2` | `kernel 7.2.11-arch1-1 …` | matches `uname -r` |
| `corpus/knowledge/userspace-oom-killers-r12.md:24` | `Historical activity while either service was inactive…` | historical scope; fine |
| `corpus/knowledge/userspace-oom-killers-r12.md:15` | zero `d989611b…` notices | re-measured `0`/`0`; holds |
| `corpus/lessons/round-12.md:105` | `inactive → unavailable (inactive)` | dated round-12 admission row; outside the named sweep |
| `corpus/lessons/round-16-verifier-spotcheck.md:219-222` | `the lesson records host 261.2-1 from version lookups` | dated round-16 defect record about the r16 note; quotes the historical value, no current claim |
| `LOG.md:1823` | round-26 declaration quoting the defect | dated ledger record |

## D. Conditional rules and source pins (not host-state claims)

- `SKILL.md:30`: `an inactive oomd/earlyoom is unavailable (inactive), never 0` — conditional
  rule. Its link `oomd-util.c … v261` is a source pin, not a host version.
- `PROVINCE.md:53` and `corpus/README.md:341`: `Inactive killers are unavailable, not zero`
  — conditional boundary, no host claim.
- `corpus/knowledge/userspace-oom-killers-r12.md:8` dates the readings (`2026-10-19
  availability snapshot only`), `:21` is a conditional inference, `:27` is a rule.
- Source pins at `userspace-oom-killers-r12.md:6,11`, `oom-kill-counter-kernel-only-r12.md:13`
  and `corpus/SOURCES.md` S011 pin oomd code at v261. Not contradicted (v261 code does behave
  as described), but [INFERENCE] host-equivalence with installed 262 is not established by
  those rows; r12 also cites the 262 man page (S007), so the gap is narrower than it looks.

## Totals

- **Contradicted present-tense statements: 10**, in 3 files.
  - killer/systemd-oomd host state: 7 (F1-F4 plus B1-B3).
  - host systemd version 261: 3 (B4-B6).
  - host kernel version: 0 present-tense claims; every 7.2.3 mention is a dated record.
- Frozen by C1: 4. **Not covered by C1: 6.**
- Conservative core, if a reviewer discounts the recheck annotation (B1) and the
  open-unknown reference (B5): 4 unfrozen, 8 total. The reportable range is 8-10; the
  six-statement gap in section B is the actionable number.
- C1 can pass while 6 stale statements remain: [INFERENCE] from the contract's exact
  phrase counting at `:73-77` and its declared after-value (four phrases absent plus entry
  existence). `journal-alarm-routing-r14.md` is not referenced by C1 at all.
- Status: `corpus/knowledge/userspace-oom-killers-r26.md` is absent at HEAD
  (`git cat-file -e HEAD:…` exits 128), as expected during wave 1.

## Recommendations for the integration owner (hygiene, not counted)

1. Extend the frozen list with the B phrases, or count with a regex over
   `inactive|not-found|not found|host systemd (is )?261` and require the still-true oomd
   values (`inactive`, `disabled`) to remain as a positive control.
2. Rewrite `userspace-oom-killers-r12.md` as one dated record: keep oomd's still-true
   `inactive`/`disabled`, date the earlyoom values, cite the r26 entry, and correct the
   `recheck:` expected outputs to `active; enabled` (or stop pinning expected outputs).
3. Add the r16-style historical correction to `journal-alarm-routing-r14.md:67,290,342`
   (or replace 261 with 262 and state the note's measurement date). This file is invisible
   to C1.
4. After F4 is removed, make `corpus/README.md:34` state the current split (earlyoom active
   and enabled, systemd-oomd inactive and disabled) and cite the r26 entry; keep the
   `unavailable (inactive)` rule scoped to the inactive killer only.

## Remaining unknowns

- Whether sibling lanes repeat these claims: outside the named sweep; whole-repo grep adds
  only dated lesson references (`corpus/lessons/round-12.md:105`;
  `round-16-verifier-spotcheck.md:219-222`, which quotes the historical 261.2-1 wording) and
  no new host-state claim; `corpus/lessons/round-13.md:42` and `round-14.md:70,73` are
  used-by metadata rows only.
- Whether oomd v262 changed the xattr/D-Bus paths described from v261: not checked this
  seat; flagged above as source-version skew.
- No tool installs or upgrades were needed; nothing was written outside this report.

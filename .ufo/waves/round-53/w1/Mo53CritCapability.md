# Mo53CritCapability — C2 attacked as a capability/coverage move

Scope: does the C2 commit-ledger tool satisfy AXES §Capabilities (runs and verifies in the
round), does PROVINCE.md at `2a4213bf` name the surface, does the SCORECARD capabilities
register already cover it, and is the move frontier→core or new ground. Counters/predicates
are frozen; findings below are data-scope items for the L1's integration, not counter changes.

Seat scratch: `/fast/scratch/hyaku/mori-r53/Mo53CritCapability/` (removed on finish; nothing
cited lives only there — every command below is reproducible read-only).

## 1. Does the capability run and verify in the round? — YES (axis requirement met)

`AXES.md:61-64`: a row enters only through a round that *demonstrates the capability running*.
Receipt and independent spot-run agree:

- `$ cat .ufo/waves/round-53/evidence/c2-at-data.txt` →
  `C2=met tool=present selftest=pass n=23 fixtures=80 agree=80 disagree=0 registry=ok live=ok
  rev=2a4213bf…`, `exit=0`. The `live=ok` leg already ran the tool on this host's defaults.
- Independent live run (read-only, from my scratch):
  `cd /fast/scratch/hyaku/mori-r53/Mo53CritCapability && python3 -I -B
  /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-commit-runway.py` →
  `{"verdict": "COMMIT_HEURISTIC", "mode": 0, "commit_limit_kb": 47583772,
  "committed_as_kb": 38570540, "headroom_kb": 9013232, "limit_recomputed_kb": 47583772,
  "limit_consistent": true, "cpus_present": 32, "single_request_cap_kb": 63444672,
  "schema": "mori-commit-runway-v1", …}`, `exit=0`. Capability executes on the host.
- Registry arm: `SKILL.md:1208` carries a table row naming `tools/mori-commit-runway.py` and
  `--selftest`; the counter's registry check (`count-c2.py:351-355`) reads `registry=ok`.
  `git show 2a4213bf --stat` confirms the data commit lands tool + 23-case fixtures + SKILL
  `## Round53` section (`SKILL.md:1178`).

P-C2's own text (`count-c2.py:9-18`) requires only: regular file, selftest ≥12, 80 fixture
agreements vs REF, the SKILL row, and the live leg. **It does not check PROVINCE.md or
SCORECARD.md** — so both gaps below are outside the frozen predicate: the claim can verify
`met` with the capability unnamed in the province and absent from the register.

## 2. Does PROVINCE.md at `2a4213bf` name the commit-ledger surface? — NO

`git diff 20edafa5 2a4213bf -- PROVINCE.md` → 0 lines (byte-unchanged at the data commit);
working tree identical today (`git diff 2a4213bf -- PROVINCE.md` empty).

`grep -ni 'commit\|CommitLimit\|Committed_AS\|overcommit\|runway' PROVINCE.md` hits only:
- `:10` owns: "resource runway (disk on the fleet root and `/tmp`, memory pressure)" —
  category-level only;
- `:26` Core "Resource runway" bullet — enumerates exactly `SURFACE disk` + `SURFACE cgroup`
  (df targets, device-write average, memory PSI/fill/avail, scope high-watermark). The
  commit-ledger read (`/proc/meminfo` CommitLimit/Committed_AS, five `/proc/sys/vm` files,
  `/sys/devices/system/cpu/present`) is **not in that enumeration**;
- `:294-355` round-25 scope notes — job-runway (harness `async.maxJobs`), a different surface;
- FR1–FR15 (`:44-57`, `:321`): no frontier row covers the commit ledger. FR8 (alert thresholds)
  and FR12 (PSI) are the nearest; neither is this.

So PROVINCE names the *category* (resource runway, mori ground — the contract's `:62` wording
is literally true) but not the *surface*. The lane's own precedent for a new read-only probe is
an appended scope-note block (`:236-290` round 24, `:294-355` round 25, `:357-371` round 26):
a Core bullet + "Owns-scope extension (append-only)" sentence + boundary bullets + admission
state. The round-30 correction (`:395-399`) even records that un-named tools are a known-open
item — but those are non-claim tools; every *capability* surface got a scope note. C2 is a
capability claim on mori ground with no such note.

**What should change:** no existing line needs editing (the append-only convention at `:274-278`,
`:345-349`, `:395-399` exists precisely so sibling line pointers never move). The smallest safe
correction is one appended block after `:400`, drafted:

```markdown
## Round-53 appended scope notes (2026-10-26)

- **Core, commit-ledger runway read (new ground on the resource-runway surface, admitted round
  53):** `tools/mori-commit-runway.py` reads `/proc/meminfo` CommitLimit and Committed_AS, five
  `/proc/sys/vm` files and `/sys/devices/system/cpu/present` and reports one JSON object
  (`schema: mori-commit-runway-v1`) with a mode-aware verdict (`COMMIT_OK`,
  `COMMIT_HEURISTIC`, `COMMIT_UNLIMITED`, `COMMIT_LOW`, `COMMIT_UNKNOWN`). Under mode 2 the
  LOW threshold is the per-CPU committed-counter error band (`batch × present CPUs × page`),
  an upper bound from the batch rule, not a measured deviation. Knowledge:
  `corpus/knowledge/commit-runway-read-r53.md` (S511–S513 at v7.2).
- **Owns-scope extension (append-only; `PROVINCE.md:6-10` left byte-unchanged):** the owned
  read-only probe list gains a fifth resource class — the kernel commit ledger — under the
  existing "resource runway" surface. The header sentence is not rewritten.
- **Boundaries:** `COMMIT_LOW` is "inside the counter's own error band", never a calibrated
  alarm — FR8 stays open. No cgroup-level commit accounting exists to read; mode-0/1 verdicts
  describe the heuristic, not enforcement. Not a census surface: no `SURFACE` row, no finding
  id, no DRIFT verdict, no baseline re-pin. Overcommit sysctl *configuration* stays with
  tsukuroi/operator; mori reads and reports only.
- **Admission state:** tool, fixtures and SKILL row landed at `2a4213bf`; selftest
  `MORI_COMMIT_RUNWAY_SELFTEST: PASS 23/23`; live host run `COMMIT_HEURISTIC` exit 0.
  Admitted by the round-53 non-author closure. No frontier row is closed.
```

## 3. Does the SCORECARD capabilities register already cover it? — NO (no duplicate authority)

The live register is `SCORECARD.md:1951-1989` (round-35 rewrite; keyed by fleet `MANIFEST.json`
`rounds[i].capabilities_added[j]`, rows entering at closure). Full row list: source registry (12),
typed journal alarm (14), partial positive journal alarms (15), exact-start journal window (16),
retention gate / freeze-order / dispatch-ledger (18), content-review gate (19), retention
reconcile (22), one-shot system pressure + routed-check (24), job-runway + routed-r24 (25),
userspace-OOM read (26), SOURCES repair + A2 cases (28), blind-writer gate + watchdog identity
(31). Plus pre-MANIFEST rows (`:641-645`): live census, census self-test, silence oracle,
drift pin. **No row reads the kernel commit ledger**; the closest are `one-shot system pressure
read` (PSI, different files and verdict semantics) and `harness background-job runway read`
(OMP cap, not kernel memory). No duplicate authority, no identity change, no false provenance.

Timing precedent (`git log -- SCORECARD.md`): round-51 and round-52 rows landed in *integration*
commits (`70e68cdd`, `2f245af7`), not the data commit — consistent with the register being keyed
to MANIFEST closure rows. So the missing row is **expected at this point in the round but is a
hard requirement for integration**: the contract declares C2 "a coverage move with a capability
row" (`contract.md:14`), and `AXES.md:62-64` + `SCORECARD.md:1953-1956` make the row enter
through this round's demonstration. The L1's integration must (a) add the row to the round-53
SCORECARD section and (b) carry `capabilities_added` in the MANIFEST entry so the register can
key it — otherwise the capability is demonstrated but never enters the repertoire.

## 4. Frontier→core, or new ground? — NEW GROUND on an owned surface

No frontier row (FR1–FR15) ever named the commit ledger, so there is no FR to advance and no
frontier→core promotion. What actually happened, per the counter's own description
(`count-c2.py:4-5`): "The round moves that surface **from knowledge into a read-only tool**" —
round-52 C2 admitted the knowledge (`corpus/knowledge/overcommit-commit-limit-r52.md`,
`SCORECARD.md:2737-2747`), round-53 C2 operationalizes it. The closest precedent is round-25's
job-runway: new ground under the owned "resource runway" surface, declared Core by appended
scope note in the same round. Round 53 skipped the declaration step.

## Verdict

- **Runs-and-verifies axis: PASS** — `C2=met` at data + independent live run, `COMMIT_HEURISTIC`
  exit 0, registry ok.
- **PROVINCE surface naming: GAP (fixable)** — commit ledger/CommitLimit absent everywhere in
  PROVINCE at `2a4213bf`; per the round-24/25/26 convention it needs the appended scope-note
  block drafted in §2 at integration. Not counter-blocked.
- **SCORECARD register: PENDING (must not be dropped)** — no covering row exists and none is
  due until integration, but the claim is a declared capability move, so the row + MANIFEST key
  are owed at closure. Track it.
- **Move class: new ground** under the owned resource-runway surface (knowledge→tool), not
  frontier→core; the scope note should keep FR8 open (band ≠ calibrated alarm) and name the
  boundaries the contract's named limits already concede.
- **Contract wording:** `contract.md:62` "PROVINCE names resource runway as mori ground" is true
  only at category level; the Core bullet's enumeration (`PROVINCE.md:26`) excludes this read.
  Harmless, but the report should not lean on it as if the surface were already enumerated.

None of these blocks `C2=met` — the frozen predicate never reads PROVINCE or SCORECARD. They
are integration-stage corrections the L1 can land in the same commit as the wave results.

## Findings

| # | Severity | File:line | Finding |
|---|---|---|---|
| F1 | MED | `PROVINCE.md:10` owns, `:26` Core bullet, FR1–FR15 `:44-57`/`:321` | Commit-ledger/CommitLimit surface unnamed anywhere in PROVINCE at `2a4213bf`; every prior capability surface (r24 pressure, r25 job-runway, r26 oom-killers) got an appended Core scope note. Fix: appended round-53 scope-note block (draft §2), no line edits. |
| F2 | LOW | `SCORECARD.md:1951-1989` (capabilities register) | No register row covers `mori-commit-runway.py`; contract declares "a capability row" (`contract.md:14`). Row + MANIFEST `capabilities_added` key are owed at integration/closure — flag so the demonstrated capability isn't dropped from the repertoire. |
| F3 | LOW | `contract.md:62` vs `PROVINCE.md:26` | "PROVINCE names resource runway as mori ground" holds only at category level; the Core bullet enumerates disk/cgroup surfaces that exclude the commit ledger. Report wording should not treat the surface as pre-enumerated. |
| F4 | INFO | `count-c2.py:9-18` | Named counter limit (not a fix request): P-C2 never checks PROVINCE/SCORECARD, so an unnamed-in-province capability still verifies `met`. Route to round 54 if the lane wants claim predicates to check surface naming; F1/F2 correct it this round by convention. |

Report: .ufo/waves/round-53/w1/Mo53CritCapability.md

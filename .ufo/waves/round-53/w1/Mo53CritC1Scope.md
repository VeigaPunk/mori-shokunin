# Mo53CritC1Scope — C1 scope and axis attack

Seat task: enumerate every lane artefact at `2a4213bf8da72f7cd78189baa5bb9be825dca1df` that pins
kernel v7.2-or-older bytes under an on-release or release-triggered recheck, say which the round
leaves unrechecked, and judge whether `freshness` is the honest axis. All `git show`/`git grep`
calls are read-only against the lane at that rev; fetches used git.kernel.org cgit (`?h=v7.2`,
`?h=v7.3`), each under 100 KB. Scratch: `/fast/scratch/hyaku/mori-r53/Mo53CritC1Scope/` (removed
at exit; cited bytes are quoted below).

## 1. The release-triggered inventory at the data commit

The assigned sweep `git grep -E 'recheck:.*(on-release|kernel release)' <rev> -- corpus/knowledge`
plus a wider `^recheck:.*release` pass returns the full trigger population. Each entry classified
by what its trigger binds to and whether its trigger fired when v7.3 was tagged:

| entry | trigger wording | kernel v7.2 bytes pinned? | fired at v7.3 tag? | in scope D? | actually drifted? |
|---|---|---|---|---|---|
| `memavailable-estimate-r51.md` | `on-release` | yes (proc.rst, show_mem.c, meminfo.c, mm_inline.h + 2014 patch) | yes | yes (21-row table) | measured by ledger |
| `overcommit-commit-limit-r52.md` | `on-release` | yes (overcommit-accounting.rst, vm.rst, util.c, mman.h, mmap.c) | yes | yes (28-row table) | measured: 2 rows `changed` |
| `oom-tracepoints-r47.md` | `on-release` | yes (`include/trace/events/oom.h` at v7.2) | yes | **no — named exclusion** | no: v7.3 copy byte-identical to committed `sources-r47/include_trace_events_oom.h` |
| `quota-observability-r48.md` | two `on-release` rows | yes (`include/uapi/asm-generic/errno.h`, arch mips+sparc `errno.h` at v7.2) | yes | **no — NOT named in ledger exclusions** | no: all three v7.3 files byte-identical to `sources-r48/` copies |
| `oom-victim-selection-r27.md` | "on a kernel release re-open `fs/proc/base.c` `proc_oom_score` and `mm/oom_kill.c` `oom_badness`" | yes (S003 oom_kill.c, S148 base.c at v7.2) | yes | **no — NOT named** | no claim drift: oom_kill.c byte-identical (`sources-r47`/`sources-r50` copies equal, both match v7.3); base.c diff is only `task->fs`→`task->real_fs` in root/pwd getters, `proc_oom_score` at same line (583) with identical region |
| `system-pressure-r24.md` | "on a kernel release, re-open S090 and S091" | yes (psi.rst, psi.c at v7.2; no committed copies) | yes | **no — NOT named** | psi.rst byte-identical; psi.c one hunk `delta < 0`→`delta <= 0` at line 1023 in the IRQ accumulator — cited items (`psi_proc_init`, `psi_disabled`, `EOPNOTSUPP`, trigger-window writes) untouched |
| `watchdog-identity-r31.md` | "on a procps-ng, kernel or man-pages release, or a change to `scripts/shokunin-watchdog.sh`" | yes (S163 sched.h, S164 exec.c, S165 binfmt_script.c, S167 array.c, S173 kernel.rst at v7.2) | yes | **no — NOT named** | no claim drift: 4 of 5 files diff but cited regions untouched — array.c is the same `fs`→`real_fs` rename in umask read, kernel.rst only *adds* `syscall_user_dispatch`, exec.c is futex/exec-mm plumbing, sched.h sched-stats fields + the `real_fs` member; TASK_COMM_LEN/binfmt argv/stat-state claims intact |
| `disk-write-rate-r33.md` | `on-release` BUT conditional: "re-open when the host kernel moves past 7.2 or sysstat past 12.8.0" | yes (S180–S190) | **no** — host still 7.2.11-arch1-1 (`uname -r`), so its own condition has not fired | n/a | deferred by its own wording, correctly |
| `conform-scope-r40.md` | bare `on-release` | no — pins Python docs (S229) | n/a (not kernel bytes) | n/a | — |
| `source-drift-r36.md` | bare `on-release` | no — pins fleet CORPUS.md + the drift tool itself | n/a | n/a | — |
| `kernel-v7.3-recheck-r53.md` | `on-release` forward-looking | pins v7.3 | next tag | the ledger itself | — |
| `commit-runway-read-r53.md` (C2's new entry) | `on-release` — "at the next tag fetch the three paths" | **yes — lands pinned to v7.2** (S511 mm_init.c, S512 percpu_counter.c, S513 percpu_counter.h) | fired the day before it landed | n/a (new claim) | no claim drift: `mm_compute_batch` body byte-identical across the 213-line mm_init.c diff; both percpu_counter files byte-identical |

Adjacent, not kernel-triggered: `oom-memcg-stat-r50.md` (`90d`, v7.2-pinned; ledger names it),
`kernel-oom-line-attribution-r12.md` / `oom-kill-counter-kernel-only-r12.md` (v7.2 URLs in recheck
lines but no release word), `harness-job-capacity-r25.md` ("on an omp release"),
`earlyoom-invocation-scope-r30.md` / `userspace-oom-killers-r26.md` (earlyoom/systemd triggers only).
SOURCES.md registry column: many rows carry `on-release` (S003, S005, S006, S019, S020, S033…);
the ledger excludes "the anchors of rows S492–S501 … they stay true for v7.2". S005 is special —
see §3.

## 2. What the round leaves unrechecked

- Named in the ledger's own Boundaries (honest): `oom-tracepoints-r47.md`, `oom-memcg-stat-r50.md`,
  "prose outside the two tables", S492–S501 anchors.
- **Not named anywhere: `quota-observability-r48.md`, `oom-victim-selection-r27.md`,
  `system-pressure-r24.md`, `watchdog-identity-r31.md`.** All four carry kernel-release triggers
  that fired when v7.3 was tagged; none appears in the contract scope, the named limits, or the
  ledger's Boundaries list. The backlog the round discharges is therefore understated: the reader
  learns of one skipped kernel entry, not five (r47 + four unnamed; r33's trigger is
  host-worded and unfired, so it is not owed).
- Good news for the lane: my independent v7.3 diffs show **zero latent claim drift** in all four
  skipped entries (every diff is in uncited code), so the scope gap is a coverage/calibration
  defect, not a stale-claim incident. Cost of discharge was low: r47's file was already provable
  from a committed pin (see §3) and the other three needed ≤ 5 small cgit fetches each.

## 3. The S005 corner: one recheck was already half-done

`SOURCES.md` S005 pins `include/trace/events/oom.h` at master `c03c1a14507dfaf8b856c2608f9ac216021fc222`,
"byte-identical" to the v7.2 copy. `evidence/sweeps.txt` records `refs/tags/v7.3^{}` →
`c03c1a14507dfaf8b856c2608f9ac216021fc222`. So the r47 entry's central file was already pinned
byte-identical to v7.3 by S005 — the sweep premise "the lane holds no v7.3 recheck … 0 `v7.3`
hits" is literally true only as a string match: the lane already held v7.3 *bytes* under a
commit-shaped pin it did not recognize as the tag. A ledger row for r47 could have been written
with zero network. This is a small honesty wrinkle in the premise, not an error in the ledger.

## 4. C2's new entry is pinned to an already-superseded tag

`commit-runway-read-r53.md` lands v7.2 copies (S511–S513) the day after v7.3 was tagged and C1
was justified by "the release trigger has fired and nothing answered it". Its `on-release`
recheck points at "the next tag", so its first scheduled recheck arrives one release late
relative to the freshest surface at authoring time. Harmless today — I verified
`mm_compute_batch` (whole function body), `percpu_counter_add_batch` and
`percpu_counter_read_positive` are byte-identical at v7.3 — but it is the same staleness C1
exists to fix, created in the same round. Data is correctable: repinning S511–S513 at v7.3 costs
three cgit fetches and zero claim edits.

## 5. Axis verdict: freshness is honest — with one caveat

AXES.md: **freshness** = "Drift detection — skill claims re-verified against live surfaces; stale
items flagged or fixed." C1 is precisely that: located-quote claims re-verified against the newly
tagged v7.3 surface, with a `holds`/`changed` disposition per row and a durable re-runnable
ledger. This is not depth (the entry adds no new mechanism knowledge beyond the already-known
`VMA_NORESERVE_BIT` respelling, which is a *drift finding*, not new detail), not operability
(the ledger is not an executable tool; count-c1.py is the instrument, not the artifact), and not
calibration — though see below. The axis assignment is honest.

Caveat — freshness credit is proportional to the fired-trigger backlog discharged. The ledger's
"Not rechecked here" names one kernel entry and omits four. Since dispositions verified clean
anyway, the deficit is in how completely the move answers "which pinned claims does v7.3 leave
stale?" — a freshness-completeness question, not an axis mislabel. This also has a small
calibration overtone (understating the backlog), insufficient to relabel the claim.

## Findings

- **MED** — scope: four kernel-release-triggered v7.2-pinned entries are left unrechecked and are
  absent from both the contract scope and the ledger's Boundaries list:
  `corpus/knowledge/quota-observability-r48.md` (recheck lines 10–11),
  `corpus/knowledge/oom-victim-selection-r27.md` (recheck line 3),
  `corpus/knowledge/system-pressure-r24.md` (recheck line 3),
  `corpus/knowledge/watchdog-identity-r31.md` (recheck line 3). All four verified drift-free at
  v7.3 by my diffs; the defect is the incomplete disclosure of the backlog (Boundaries,
  `corpus/knowledge/kernel-v7.3-recheck-r53.md:107`), not stale claims. Route to round 54 or land
  a Boundaries line naming them.
- **LOW** — `corpus/knowledge/commit-runway-read-r53.md` (S511–S513): new claim pinned to v7.2
  bytes while v7.3 is the tagged live surface; `mm_compute_batch` is byte-identical at v7.3
  (verified), so repinning is a free correctness improvement — data-correctable per contract.
- **LOW** — premise wording: "0 `v7.3` hits" in `evidence/sweeps.txt` misses that S005 already
  pins `include/trace/events/oom.h` byte-identical at commit `c03c1a14…` = `v7.3^{}`; the lane
  held v7.3 bytes for one pinned file without a recheck record. Affects narrative precision only.
- **LOW** — `disk-write-rate-r33.md`'s `on-release` is conditioned on the *host* kernel, not the
  tag: with host at 7.2.11 the entry's own recheck never fires no matter how many tags upstream
  makes. Not in C1 scope by that wording, but the entry's tag-pinned bytes can silently stale;
  worth a named limit somewhere (round-54 routing).
- Axis verdict: **freshness is the honest axis** for C1 (drift re-verification is exactly what the
  ledger is); the residual is completeness of the discharged backlog, not mislabelling.

Counter/verification evidence used above: `python3 .ufo/waves/round-53/count-c1.py
2a4213bf8da72f7cd78189baa5bb9be825dca1df` → `C1=unmet scope=46 rows=46 matched=46 status_ok=46
quote_ok=46 source_rows=ok pins=ok provenance=ok held=44 absent=2 holds=46 changed=0 voted=0
dissent=0 … failed=votes`, exit 1 (reproduced; matches `evidence/c1-at-data.txt`).
Byte comparisons: `cmp`/`diff` of committed `sources-r47/r48/r50/r53` copies and cgit `?h=v7.3`
fetches — same/diff results as tabled in §1; `uname -r` → `7.2.11-arch1-1`. UNVERIFIED: nothing —
all cited diffs were computed locally.

Report: .ufo/waves/round-53/w1/Mo53CritC1Scope.md

# Mo53CritC2Semantics — attack on the reading of tools/mori-commit-runway.py and commit-runway-read-r53.md

Seat: semantics critic for claim C2. Review revision: `2a4213bf8da72f7cd78189baa5bb9be825dca1df` (data commit;
entering freeze `f4da3fd400fa88a6db8ea544a4f7045c15d2410e`). All tool runs below used the **committed** bytes
extracted by `git archive 2a4213bf … tools/mori-commit-runway.py tools/fixtures/mori-commit-runway/cases.json`
into my scratch; kernel quotes are from the lane's pinned copies under `corpus/evidence/sources-r52/` and
`corpus/evidence/sources-r53/`. Scratch: `/fast/scratch/hyaku/mori-r53/Mo53CritC2Semantics/` (removed on finish;
the one fetched artifact's hash is recorded below).

## Wave-state observation (context, not a finding against the data)

The working tree currently carries an **uncommitted** delta to `tools/mori-commit-runway.py` (+159 lines of
hostile-input guards), `tools/fixtures/mori-commit-runway/cases.json` (+3 UNKNOWN cases), `SKILL.md` and the
entry, citing wave seats `Mo53SentC2ReadOnly`, `Mo53SentC2Hostile`, `Mo53ScoutRunwayTools` (observed
`git status --porcelain` → ` M` on those four files; `git diff` read; committed bytes still 316 lines,
sha256 `80cb169650bf…`). I reviewed the committed rev as assigned. The patch does not touch any line my
findings concern. One consequence for the L1's integration ledger (not a counter defect): the patched tool
returns `COMMIT_UNKNOWN` where the frozen REF would compute a verdict for three input shapes (a 30-digit
MemTotal, an overlapping CPU list, a CPU list naming >65536 CPUs). The counter's 80 counted fixtures never
produce those shapes (seeded CPU lists are always ascending/disjoint, ≤256 CPUs, digits-only fields), so
`agree=80` is unaffected — but tool and REF now diverge on a class of inputs REF parses; worth one named-limit
line if the patch lands.

## Assigned questions, verdicts

### 1. Does `COMMIT_LOW` mislead? — Mostly no; one LOW-severity gap on the JSON surface.

Checked the kernel model against the pinned bytes:

- `corpus/evidence/sources-r52/util.c.v7.2:982-983`: `if (!cap_sys_admin) allowed -= sysctl_admin_reserve_kbytes
  >> (PAGE_SHIFT - 10);` — root keeps the admin reserve, as the entry's "do not mean" column says.
- Same file, :988-991: `if (mm) { long reserve = sysctl_user_reserve_kbytes >> (PAGE_SHIFT - 10); allowed -=
  min_t(long, mm->total_vm / 32, reserve); }` — the user reserve is per process, applies to every caller with an
  mm (root included), and the full sysctl value is the worst case for a large process, as the docstring says.
- The band direction: `percpu_counter_read_positive` (S513 copy :118-126) returns the global count only; local
  deltas sit in (−batch, +batch) per present CPU (`percpu_counter_add_batch` fold at S512 copy :93-113 resets the
  local to ~0). The kernel test `read_positive < allowed` can therefore refuse early only when the unfused
  deltas sum negative — bounded by `ncpu·(batch−1)`, and the tool uses `ncpu·batch`, i.e. `usable_kb <= band_kb`
  is conservative by under one page per CPU. Correct direction; COMMIT_OK ⇒ every caller class passes (the tool's
  `usable` subtracts both reserves at maxima; the kernel subtracts less or none).
- Verified live: crafted mode-2 input (8 GiB, 32 CPUs, `usable_kb == band_kb == 32768`) → `COMMIT_LOW`, exit 1,
  `inside_band` finding. Matches the frozen edge rule.

The misleading surface is the **JSON `notes` string**, not the verdict: docstring line 32-33 names the worst
case, entry table row and SKILL row 1187 say "non-root allocation may already be refused" — but the emitted note
says only `usable_kb counts the full user reserve (worst case)`. A consumer that reads only JSON sees `COMMIT_LOW`
plus `usable_kb ≤ band` and can read it as "no room", while a CAP_SYS_ADMIN caller still has `admin_reserve`
room (8 MiB default) — a documented but JSON-invisible qualifier. Direction is safe (false-positive only).
The mode-2 note is not a REF-compared field, so it is freely correctable. Severity LOW. Fenced replacement
(tool docstring :31-38 and the note at :192-193 of the committed file):

```text
docstring line ~33 — replace:
   ``usable_kb`` = headroom_kb - reserve_kb, the room a large non-root allocation has before the test
   fails.
with:
   ``usable_kb`` = headroom_kb - reserve_kb, the room the strictest caller (non-root, process large enough
   that min(total_vm/32, user_reserve) = user_reserve) has before the test fails; CAP_SYS_ADMIN callers keep
   the admin reserve, smaller processes keep part of the user reserve, so usable_kb under-reads their room.

note string line ~192 — replace:
   "mode 2 (never): enforced; usable_kb counts the full user reserve (worst case) and band_kb "
   "is the per-CPU approximation bound, not a measured deviation"
with:
   "mode 2 (never): enforced; usable_kb is the strictest caller's room (full user reserve plus the admin "
   "reserve a CAP_SYS_ADMIN caller keeps); band_kb is the per-CPU approximation bound, not a measured "
   "deviation; COMMIT_LOW is inside-band, not a calibrated alarm"
```

### 2. Does mode 0's `single_request_cap_kb` match `__vm_enough_memory`? — Yes.

`util.c.v7.2:972-975` (identical in `util.c.v7.3`): `if (sysctl_overcommit_memory == OVERCOMMIT_GUESS) { if
(pages > totalram_pages() + total_swap_pages) goto error; return 0; }` — **strictly greater**: a request of
exactly `totalram + swap` pages passes the check. The tool's `(ram_pages + swap_pages) * page_kb` is the
largest page-aligned request that passes, and `MemTotal`/`SwapTotal` kB are `totalram_pages()`/`total_swap_pages`
in page units, so the figure is exact (live host printed `single_request_cap_kb: 63444672` =
(31721796 + 31722876) kB). No hugetlb subtraction — matching the kernel, which uses `totalram_pages()` unreduced
here (unlike `vm_commit_limit`, which subtracts `hugetlb_total_pages()`, and the tool mirrors that too).

Two residue nits (both LOW, wording only):
- The note `"only a single request above RAM + swap is refused"` reads ambiguously — it is a *per-request* cap
  refused however many times it is attempted, and it is the only check this commit test applies in mode 0 (other
  limits — RLIMIT_AS, VMA count — still apply and are outside this reading). Suggested wording in the fenced
  block below.
- `enforced: false` in mode 0 means "CommitLimit not enforced" while the single-request cap *is* enforced. The
  field is REF-frozen (REF emits `mode == 2`); the docstring can fix the gloss without touching the schema:

```text
docstring — after the ``enforced: true`` line for mode 2, or in the field list, clarify:
   ``enforced`` reports whether CommitLimit is enforced (mode 2 only); mode 0 still enforces the
   single-request cap reported as ``single_request_cap_kb``, and mode 1 enforces nothing.
note string for mode 0 — replace:
   "mode 0 (guess): only a single request above RAM + swap is refused; CommitLimit is printed, not enforced"
with:
   "mode 0 (guess): the only commit check refuses each request larger than RAM + swap "
   "(single_request_cap_kb); CommitLimit is printed, not enforced"
```

### 3. Is negative `headroom_kb` in mode 0 safe to print? — Yes.

Reproduced on the frozen host numbers (Committed_AS 60169456 > CommitLimit 47583772, mode 0): exit 0,
`COMMIT_HEURISTIC`, `headroom_kb: -12585684`, and the `over_limit_not_enforced` finding carrying the value. The
truthful negative plus the finding is safer than clamping to 0 or nulling (which would also break REF agreement).
Entry "do not mean" column and SKILL row 1184 both preempt the exhaustion misreading. No defect.

### 4. Would a mori operator read any field as advice to change a sysctl? — No.

Every emitted string is descriptive; the only imperative-shaped artifact is exit 1, mapped `1 → failed` in the
registry — and that vocabulary is convention-wide (`PRESSURE_HIGH`, `KILLER_ACTED`, `RUNWAY_CLAMPED` all map
1 → failed), not a COMMIT_LOW-specific slip. The entry's boundary line ("Choosing an overcommit mode, a ratio or
a reserve is the operator's; OS-state triage is tsukuroi's") and the repeated "not a calibrated alarm" disclaim
it. `limit_mismatch` is explicitly framed as "the reading of the inputs is off, not the kernel's" — the one
direction that could invite a sysctl "fix" is already inverted. No defect.

### 5. Is `coverage` the honest axis, or is this operability? — Coverage, and the counter reads it correctly.

The move is a *capability* move: the commit ledger (CommitLimit, Committed_AS, the five vm sysctls, the CPU
present list) was admitted knowledge in round 52 with zero readers under `tools/` at `20edafa5`; C2 gives the
surface a reader. That is exactly what the coverage axis measures — a governed surface the lane can now read.
Operability would assert the tool is *used*, calibrated or wired into the fleet's operating loop; nothing in
P-C2 asserts that (the registry `kind: gate` says "host-surface verdict; not a census or fleet-admission gate",
and no other tool consumes the JSON). The counter's fixtures/selftest are gates on the capability's correctness,
not operability evidence. Axis assignment is honest; if the report wants the sharpest phrasing: coverage gained
a read; operability gains nothing yet (an uncalibrated verdict with no consumer changes no workflow) — that is
a strength of the claim, not a hidden inflation.

### Additional finding: the "v7.3 copy" the boundary section cites is not in the lane

`commit-runway-read-r53.md` boundary bullet (:49-50) asserts `mm_compute_batch` "in the v7.3 copy differs only
by its line number". The lane pins `corpus/evidence/sources-r53/mm_init.c.v7.2` only — no `mm_init.c.v7.3`
exists (verified: `git ls-files`, `ls corpus/evidence/sources-r53/`). I fetched the missing artifact myself:
`https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/mm/mm_init.c?h=v7.3` → 2693 lines,
sha256 `678410005f881a64…` (full hash in evidence below); `mm_compute_batch` and `mm_compute_batch_notifier` are
**byte-identical** to the v7.2 copy (`awk` extract + `diff` → IDENTICAL), sitting at line 195 vs 191. The
substantive claim is true — but it cites an unpinned artifact in a lane whose evidence discipline is committed
copies with sha256 pins (S502-S510 all pin `*.v7.3`). Two acceptable corrections (data is L1-editable):

```text
Either — pin it:
   add corpus/evidence/sources-r53/mm_init.c.v7.3
   (sha256 678410005f881a64…, cgit plain/mm/mm_init.c?h=v7.3, fetched 2026-10-26)
   and extend the boundary bullet to name the pinned copy.

Or — reword corpus/knowledge/commit-runway-read-r53.md lines 49-50:
   - v7.2 bytes, the host's kernel line (7.2.11); mm_compute_batch was compared against mm/mm_init.c at
     v7.3 (cgit, 2026-10-26) during this round: the function and its notifier are unchanged, differing only
     in line numbers (195 vs 191); the v7.3 bytes are not pinned — the recheck rule below re-fetches them.
```

(If pinning, note C1's D-scope is the nine r51/r52-cited paths; mm_init.c is outside it, so no ledger row is
required — the pin is a provenance nicety, and the rewording alone is sufficient if the L1 prefers minimal
data churn.)

## Evidence

| # | command | result |
|---|---|---|
| 1 | `git archive 2a4213bf … | tar -x` in scratch; `python3 -I -B tools/mori-commit-runway.py --selftest` | `PASS 23/23`, `MATCHER: rejected 23/23`, exit 0 — matches committed SKILL row text |
| 2 | `python3 -I -B tools/mori-commit-runway.py` (live, committed bytes) | `COMMIT_HEURISTIC` exit 0; mode 0; `limit_consistent: true` (recomputed 47583772 = printed); `single_request_cap_kb 63444672`; headroom positive today (`Committed_AS 35632816`) |
| 3 | committed tool on crafted mode-2 fixture (usable == band == 32768) | `COMMIT_LOW` exit 1, `inside_band` finding |
| 4 | committed tool on the entry's mode-0-over-limit numbers | `COMMIT_HEURISTIC` exit 0, `headroom_kb: -12585684`, `over_limit_not_enforced` |
| 5 | `util.c.v7.2` :972-975, :982-991, :904-915 | GUESS check strictly `>`; admin reserve only `!cap_sys_admin`; user reserve `min(total_vm/32, reserve)` for any mm; `vm_commit_limit` formula matches the tool's recompute |
| 6 | `mm_init.c.v7.2` :191-233 | batch = `max(min(ram_pages/nr/256, INT_MAX), max(2*nr, 32))` with `nr = num_present_cpus()`; memory-hotplug notifier recomputes on MEM_ONLINE/OFFLINE (entry's boundary claim verified) |
| 7 | `percpu_counter.c.v7.2` :93-113, :171-186, :266-286 + `percpu_counter.h.v7.2` :118-126 | fold resets local to ~0 (bound < batch per CPU at rest); sum iterates online|dying; dead-CPU deltas folded at hotplug (entry's claim verified); read_positive clamps at 0 |
| 8 | `mman.h.v7.2` :76-78 | `vm_acct_memory` uses `vm_committed_as_batch` — the per-mode batch |
| 9 | `curl cgit plain/mm/mm_init.c?h=v7.3` → sha256 `678410005f881a640a8c94b3f9b1f2f…` (full: `678410005f881a64`…, 2693 lines) | `mm_compute_batch` and notifier byte-identical to the v7.2 copy (lines 195/216 vs 191/212); **no `*.v7.3` mm_init.c is pinned in the lane** |
| 10 | `git status --porcelain` + `git diff` | uncommitted L1 integration patch in flight on the four C2 files (hostile-input guards, +3 fixture cases, SKILL/entry text); committed bytes reviewed; patch does not touch finding lines |
| 11 | SKILL.md :1184-1189 decision table, registry row :1208, peer registry rows | non-root qualifier and "not a calibrated alarm" present in prose; `1 → failed` is registry-wide convention |

Hand-arithmetic check of the fixture note: `(7930449*50//100 + 7930719)*4 = 47583772` ✔ equals the printed and
recomputed limit on the live host.

Full sha256 of the fetched v7.3 `mm/mm_init.c`: run `sha256sum` on the cgit body; first 16 hex digits
`678410005f881a64` (recorded; body removed with scratch — the URL and tag make it reproducible).

## Verdict

The reading is semantically sound: `COMMIT_LOW` is the correct conservative bound (never misses the strictest
caller's refusal; can only over-warn), `single_request_cap_kb` matches the kernel's strict `>` test, negative
mode-0 headroom is honest and flagged, and no field invites sysctl action. `coverage` is the honest axis. Two
data-level corrections proposed (unpinned "v7.3 copy" provenance claim; JSON notes missing the caller
qualifier); neither requires touching frozen counters, predicates or REF-compared fields.

## Findings

- **MED** — `corpus/knowledge/commit-runway-read-r53.md:49-50`: cites a "v7.3 copy" of `mm_init.c` that is not
  pinned anywhere in the lane (only `sources-r53/mm_init.c.v7.2` exists); the claim itself verified true
  (identical function, line-number shift 191→195). Fix: pin `corpus/evidence/sources-r53/mm_init.c.v7.3`
  (sha256 `678410005f881a64…`, cgit `?h=v7.3`) or apply the fenced rewording above.
- **LOW** — `tools/mori-commit-runway.py:192-193` (committed note string) and docstring :31-38: `COMMIT_LOW`'s
  JSON `notes` omit that `usable_kb` models the *strictest* caller (non-root, maximal user reserve); root keeps
  `admin_reserve_kbytes` and smaller processes keep part of the user reserve, so the number under-reads their
  room. Prose docs carry the qualifier; the emitted JSON does not. Fenced replacement in §1.
- **LOW** — `tools/mori-commit-runway.py` docstring/mode-0 note: `enforced: false` in mode 0 can be read as
  "no check is enforced" while the single-request cap *is* enforced there; and the note's "only a single
  request above RAM + swap is refused" is ambiguous (per-request cap, repeatedly applied). Field semantics are
  REF-frozen; docstring/note wording fix only. Fenced replacement in §2.
- **LOW** — observation for the L1's integration ledger (not against the committed data): the in-flight
  worktree patch makes the tool stricter than frozen REF on three malformed-input classes (giant digit strings,
  overlapping CPU lists, >65536 CPUs). No counted fixture produces those shapes, so `agree=80` is unaffected;
  record it as a named limit if the patch lands.

Report: .ufo/waves/round-53/w1/Mo53CritC2Semantics.md

# Mo53ScribeSkill — `## Round53` in SKILL.md vs the committed tool, entry and recheck ledger

Seat: Mo53ScribeSkill (leaf, no subagents). Lane: mori-shokunin. Data revision under review:
`2a4213bf8da72f7cd78189baa5bb9be825dca1df` (lane HEAD at read time `95cf78eef71979f9b740ef6bc3c5299b6beff86e`;
the three artifacts are byte-identical between the two, see §0). Scratch `/fast/scratch/hyaku/mori-r53/Mo53ScribeSkill/`,
removed at the end of this seat.

Subject: SKILL.md `## Round53` (lines 1178–1208 at 2a4213) against `tools/mori-commit-runway.py`,
`corpus/knowledge/commit-runway-read-r53.md`, `corpus/knowledge/kernel-v7.3-recheck-r53.md`, and the
PROTOCOL §Gate standard `Registry` schema.

This seat reviewed and drafted only. I wrote exactly one file: this report. No product code, no cache verbatim,
no SKILL/corpus/tool edit, no git mutation, no pacman.

## 0. Revision hygiene (why committed bytes, not the worktree)

The worktree moved while I read: `git status --porcelain` at 22:4x showed

```
 M SKILL.md
 M corpus/knowledge/commit-runway-read-r53.md
 M tools/fixtures/mori-commit-runway/cases.json
 M tools/mori-commit-runway.py
?? .ufo/waves/round-53/evidence/selftests/
?? .ufo/waves/round-53/w1.ready
?? .ufo/waves/round-53/w1.ready.dispatched
?? .ufo/waves/round-53/w1/
```

and the live worktree already carries (a) a tool hardening patch citing sentinel seats (`Mo53SentC2ReadOnly`,
`Mo53SentC2Hostile`: regular-file-only reads, 1 MiB cap, 20-digit numbers, ascending/disjoint CPU list,
`--page-kb ≤ 1024`, 5 built-in hostile-input checks, `PASS 31/31` over 26 cases) and (b) an entry rewrite of the
host paragraph (lines 44–47: two `Committed_AS` readings, one above the limit, one below). Those are the L1's
integration in progress, not the bytes the round is scored on. Every finding below is stated against the committed
bytes at 2a4213; I note where an uncommitted revision appears to answer it.

Verification that the reviewed bytes are the scored bytes:

```
$ for f in SKILL.md tools/mori-commit-runway.py tools/fixtures/mori-commit-runway/cases.json \
    corpus/knowledge/commit-runway-read-r53.md corpus/knowledge/kernel-v7.3-recheck-r53.md; do
    git diff --quiet 2a4213bf 95cf78ee -- "$f" && echo "$f: unchanged" || echo "$f: CHANGED"; done
SKILL.md: unchanged
tools/mori-commit-runway.py: unchanged
tools/fixtures/mori-commit-runway/cases.json: unchanged
corpus/knowledge/commit-runway-read-r53.md: unchanged
corpus/knowledge/kernel-v7.3-recheck-r53.md: unchanged
```

Worktree hashes at read time (for the record; not the reviewed bytes):
`SKILL.md f7875b4c…`, `commit-runway-read-r53.md e11fc2d0…`, `mori-commit-runway.py 82924be7…`.
Committed tool copy used for every run below: `git show 2a4213b:tools/mori-commit-runway.py`,
sha256 `80cb169650bf02578439703bc006173aab7b759ff9cf57337611b27164676156`, run from
`/fast/scratch/hyaku/mori-r53/Mo53ScribeSkill/committed/` with the committed `cases.json` next to it.

## 1. Commands run and their outputs

Scratch discipline: `mkdir -p /fast/scratch/hyaku/mori-r53/Mo53ScribeSkill/{tmp,m2,…}`,
`export TMPDIR=/fast/scratch/hyaku/mori-r53/Mo53ScribeSkill/tmp`; every fixture written under that root; no
network fetch (the three kernel paths are already committed as S511–S513 copies); no write to the lane or the fleet
root.

| # | command (cwd = scratch unless the path is absolute) | output | exit |
|---|---|---|---|
| 1 | `python3 -I -B tools/mori-commit-runway.py --selftest` (committed copy) | `MATCHER: rejected 23/23 corrupted expectations` / `MORI_COMMIT_RUNWAY_SELFTEST: PASS 23/23` | 0 |
| 2 | `python3 -I -B tools/mori-commit-runway.py` (committed copy, host defaults) | `{"commit_limit_kb": 47583772, "committed_as_kb": 35405020, "cpus_present": 32, "enforced": false, "findings": [], "headroom_kb": 12178752, "limit_consistent": true, "limit_recomputed_kb": 47583772, "mode": 0, … "single_request_cap_kb": 63444672, "verdict": "COMMIT_HEURISTIC"}` | 0 |
| 3 | `python3 -I -B tools/mori-commit-runway.py --meminfo m2/meminfo --vm-dir m2/vm --cpu-present /sys/devices/system/cpu/present --page-kb 4` (`m2/vm/overcommit_memory` = `2`, rest copied from `/proc/sys/vm`, `m2/meminfo` copied from `/proc/meminfo`; **read-only experiment, no sysctl written**) | `mode 2 band_kb 123904 batch_pages 968 usable_kb 11694372 reserve_kb 139264 COMMIT_OK`, `limit_consistent true` | 0 |
| 4 | `python3 -I -B tools/mori-commit-runway.py --cases tools/fixtures/mori-commit-runway/cases.json` (no `--selftest`) | a live read (`COMMIT_HEURISTIC mode 0 47583772`) — `--cases` silently ignored | 0 |
| 5 | `python3 -I -B tools/mori-commit-runway.py --selftest --meminfo /nonexistent` | `PASS 23/23` — `--meminfo` silently ignored in selftest mode | 0 |
| 6 | quote check: every backticked span of the entry's `## Claims` table searched in the S511/S512/S513 copy under `corpus/evidence/sources-r53/` and the S499 copy `corpus/evidence/sources-r52/util.c.v7.2`, whitespace collapsed | `OK S511`×3, `OK S512`×1, `OK S513`×1, `OK S499`×3 — 8/8 located | 0 |
| 7 | `sed -n '/mm_compute_batch/,/^}/p' corpus/evidence/sources-r53/mm_init.c.v7.2` | the function plus `mm_compute_batch_notifier` (MEM_ONLINE/MEM_OFFLINE only) and `mm_compute_batch_init` (`hotplug_memory_notifier`) | 0 |
| 8 | `grep -n 'hotplug\|notifier' mm_init.c.v7.2` / `grep -n 'percpu_counter_cpu_dead' percpu_counter.c.v7.2` | `212 static int __meminit mm_compute_batch_notifier …`, `229 hotplug_memory_notifier(…)`; `266 percpu_counter_cpu_dead`, `403 cpuhp_setup_state_nocalls(… percpu_counter_cpu_dead)` | 0 |
| 9 | `grep -n 'vm_acct_memory\|vm_unacct_memory' sources-r53/mman.h.v7.3` | `76 static inline void vm_acct_memory(long pages)` … `83 vm_acct_memory(-pages);` | 0 |
| 10 | `grep -n 'vm_acct_memory\|vm_unacct_memory\|percpu_counter_read_positive' sources-r52/util.c.v7.2` | `964 vm_acct_memory(pages);`, `983 allowed -= sysctl_admin_reserve_kbytes …`, `989 long reserve = sysctl_user_reserve_kbytes …`, `994 if (percpu_counter_read_positive(&vm_committed_as) < allowed)`, `1000 vm_unacct_memory(pages);` | 0 |
| 11 | `git ls-files \| grep -i mm_init` | `corpus/evidence/sources-r53/mm_init.c.v7.2` only — no v7.3 copy in the lane | 0 |
| 12 | `python3 -c 'import json;…'` over committed `cases.json` | 23 cases, ids and expected verdicts listed; `host-mode0-over-limit` expects `over_limit_not_enforced` | 0 |
| 13 | `/proc` reads for the live comparison | `overcommit_memory 0`, `overcommit_ratio 50`, `admin_reserve_kbytes 8192`, `user_reserve_kbytes 131072`; `MemTotal 31721796 kB`, `SwapTotal 31722876 kB`, `CommitLimit 47583772 kB`, `Committed_AS 38513360 kB` (first read) / `35405020` (later read); `/sys/devices/system/cpu/present` = `0-31` | 0 |

Tooling: nothing installed. Host reads only; no sysctl, no cgroup, no OOM, no journal vacuum, no kernel-log
message text.

## 2. Row-by-row truth check of the `## Round53` section (SKILL.md 1178–1208 at 2a4213)

### 2.1 Decision table (1182–1189)

| SKILL line | claim | verdict | ground |
|---|---|---|---|
| 1184 | `COMMIT_HEURISTIC` (mode 0), exit 0; only a single request above RAM + swap is refused (`single_request_cap_kb`); `over_limit_not_enforced` when `Committed_AS` exceeds `CommitLimit` | **true** | `util.c.v7.2:973` `if (pages > totalram_pages() + total_swap_pages)`, tool 178/195; live exit 0 |
| 1185 | `COMMIT_UNLIMITED` (mode 1), exit 0; the commit test always passes | **true** | `util.c.v7.2:969-971` (`OVERCOMMIT_ALWAYS` → `return 0`) |
| 1186 | `COMMIT_OK` (mode 2), exit 0; `usable_kb` (limit − committed − admin and user reserves) above `band_kb` | **true, wording weak** | tool 185–193; the "do not read as" cell speaks of "room for any allocation of `usable_kb`" — the real caution is the strict `<` at `util.c.v7.2:994` (a request that lands exactly on the limit is refused), plus the signed band. See finding F1/F3 and draft D2 |
| 1187 | `COMMIT_LOW` (mode 2), exit 1; `usable_kb ≤ band_kb`; "inside the per-CPU counter's error band a non-root allocation may already be refused" | **the inequality is true, the explanation is not** | tool 187; the refusal-with-room story needs the read **above** the exact sum (pending negative deltas), while the entry calls the read a **lag** — see F1 |
| 1188 | `COMMIT_UNKNOWN`, exit 2; an input missing, unreadable or malformed, or the mode outside 0–2 (`notes`) | **true but incomplete** | tool 136–153 and the `--page-kb` power-of-two refusal (tool 308 in the committed copy) also produce `COMMIT_UNKNOWN`; usage error covered in the registry row, not here — F4 |
| 1189 | `limit_mismatch`: recomputed `vm_commit_limit()` differs from printed `CommitLimit`; inputs misread (page size, Hugetlb) | **true** | tool 157–167 recomputes `(ram − hugetlb) × ratio / 100 + swap` pages; `util.c.v7.2:904-916` is the same arithmetic; live `limit_consistent true` at the host's 4 KiB page |

### 2.2 Error patterns (1191–1195)

| SKILL line | claim | verdict |
|---|---|---|
| 1193 | Reading `Committed_AS > CommitLimit` under mode 0 as exhaustion | **true** (`util.c.v7.2:969-975`: mode 0 never compares the two) |
| 1194 | Subtracting only `admin_reserve_kbytes`: a non-root process also loses up to `user_reserve_kbytes` | **true** (`util.c.v7.2:982-992`: admin reserve when `!cap_sys_admin`, then `min(mm->total_vm/32, user_reserve)`); the bullet cites a bare `vm.rst`, not the S row that carries it (S507) — F5 |
| 1195 | Treating `Committed_AS` as the enforced value: it is the exact sum; the test reads the global count | **true** (`util.c.v7.2:937-940` sum; `:994` the global read) |

### 2.3 Release recheck rule (1197–1202)

The `held`/`absent` derivation matches `count-c1.py` line for line (counter: `derived = "held" if q72 in
norm[path] else "absent"`, whitespace collapsed, v7.3 committed copy). The sentence says "re-read **every** claim
row", while the frozen scope D is "every row that cites a v7.2 **file**" — 46 of 49; the three rows citing the 2014
patch cannot be re-read at a tag (contract C1, `evidence/c1-scope.txt`). Precision defect — F6, draft D5. The rule
also omits the counter's other requirement (a `held` row's new text must equal the old text), which the ledger entry
states in its own words.

### 2.4 Registry row (1204–1208) against PROTOCOL §Gate standard `Registry`

PROTOCOL.md §Gate, `Registry` bullet: "Row fields: name, `gate|probe`, entry command, verdict map (code → class),
self-test command and spelling, pinned-value path, write scope, owner." The row has eight columns in exactly that
order:

| required field | row cell | resolves |
|---|---|---|
| name | `commit runway (r53, C2)` | yes |
| `gate|probe` | `gate (host-surface verdict; not a census or fleet-admission gate)` | yes — the parenthetical is prose, the token is `gate` |
| entry command | `python3 -I -B tools/mori-commit-runway.py [--meminfo PATH] [--vm-dir DIR] [--cpu-present PATH] [--page-kb N] [--selftest [--cases FILE]]`, defaults and read-only scope | yes; flag names match tool 297–302 |
| verdict map (code → class) | `0 → clean (COMMIT_OK, COMMIT_HEURISTIC, COMMIT_UNLIMITED) · 1 → failed (COMMIT_LOW) · 2 → could-not-evaluate (COMMIT_UNKNOWN, usage error)` | yes, and the classes are PROTOCOL's own (`clean | failed | could-not-evaluate`, line 381) |
| self-test command and spelling | `--selftest` → `MORI_COMMIT_RUNWAY_SELFTEST: PASS 23/23` (also prints `MATCHER: rejected 23/23 corrupted expectations`) | **exact**: run 1 reproduces both strings, in that order, 23/23 |
| pinned-value path | `tools/fixtures/mori-commit-runway/cases.json` (23 cases) | path exists with 23 cases; but no digest pins it — F2 |
| write scope | `none (selftest: a temporary directory under $TMPDIR)` | true (`tempfile.mkdtemp` at tool 254, `shutil.rmtree` in `finally`) |
| owner | `mori` | yes |

Verdict: **registry row complete (8/8 fields), spelling verified**. Two wording notes (F2, F4), no missing field.

### 2.5 Pointer resolution

| pointer in the section | resolves to | state |
|---|---|---|
| `corpus/knowledge/commit-runway-read-r53.md` | the entry | exists |
| `corpus/knowledge/kernel-v7.3-recheck-r53.md` | the recheck ledger | exists (111 lines, table header `h, entry, status, source, quote, disposition`) |
| `memavailable-estimate-r51.md` | round-51 entry | exists |
| `tools/mori-commit-runway.py` | the tool | exists, executable, `python3 -I -B` safe |
| `.ufo/waves/round-53/count-c1.py` | the C1 counter | exists |
| S511–S513 | `corpus/SOURCES.md:290-292`, all `opened 2026-10-26`, each naming its committed v7.2 copy | exists |
| S499 | `corpus/SOURCES.md:278`, `used-by` already lists `corpus/knowledge/commit-runway-read-r53.md` | exists |
| S497 | `corpus/SOURCES.md:276` | exists |
| `tools/fixtures/mori-commit-runway/cases.json` | committed fixture, 23 cases | exists |
| entry `source:` lines: `corpus/evidence/sources-r53/{mm_init.c,percpu_counter.c,percpu_counter.h}.v7.2` | all three | exist, and each is the file the quote check matched |

One pointer **does not** resolve: the entry's Boundary "`mm_compute_batch` in the v7.3 copy" — `git ls-files` has
only `mm_init.c.v7.2` (run 11; grep over the whole lane finds the phrase "v7.3 copy" nowhere else). F7.

## 3. Findings

Each finding names committed file and line at 2a4213, then the observation, then the draft that would fix it.
Severities: HIGH = a claim a reader would act on wrongly and no pointer corrects; MED = a claim true in form but
wrong or ungrounded in a way that changes the reading; LOW = precision, resolvability, or durability.

### F1 (MED) — the counter's error is signed, the entry and the decision table call it a lag

Files: `corpus/knowledge/commit-runway-read-r53.md:14-18` (committed), `SKILL.md:1187`.

The entry says the mode-2 test "reads only the global part of a per-CPU counter, which **lags the sum** by less than
one batch per CPU" (line 14) and then "there, a non-root allocation **may already be refused** although the printed
numbers still show room" (line 18). Those two statements need opposite signs of the error:

* A lag (read < exact sum) makes the test **more permissive**: with printed room `allowed − sum > 0` we get
  `read ≤ sum < allowed`, and `util.c.v7.2:994` (`read < allowed`) passes. A lag can never produce a refusal while
  room shows.
* A refusal while room shows requires read ≥ allowed > sum, i.e. the read **above** the exact sum. That is possible:
  each CPU's local delta is signed (`percpu_counter.c.v7.2:100` `if (unlikely(abs(count + amount) >= batch))` folds
  either sign; `mman.h.v7.3:76-84` reaches it through `vm_unacct_memory` → `vm_acct_memory(-pages)`), so pending
  negative deltas put the global count above the exact sum.

Consequence for a reader: the band is a two-sided bound (|read − sum| < batch × CPUs), and inside it a request can
be **accepted past the limit** as readily as refused. The tool's docstring (lines 33–40 of the committed copy) is
sign-neutral and correct; only the entry sentence and the SKILL cell carry the one-sided story. The verdict
(`COMMIT_LOW` iff `usable_kb ≤ band_kb`) is frozen and unaffected — this is a data/wording defect, not a counter
defect.

### F2 (LOW) — the registry row's "pinned values" cell names a fixture nothing pins

File: `SKILL.md:1208` (pinned-values cell). `cases.json` is named as the pinned value, but its bytes carry no
digest: `evidence/freeze-sha256.txt` (33 lines) predates the data commit and lists neither the tool nor the fixture;
`evidence/c2-at-data.txt` records the counter line only. The C2 counter's selftest arm requires exit 0 and
`PASS n/n` with n ≥ 12 (its docstring, `count-c2.py:12`), so a later trim of `cases.json` to 12 trivial cases
would keep that arm green; the independent arm is the 64 generated + 16 frozen fixtures compared against REF, not
the file. Nothing to change in the frozen counter — the row should say which arm is the real pin.

### F3 (MED) — the band can understate after a CPU hot-add, and no line says so

Files: entry `Boundaries` (committed lines 51–55), SKILL error-pattern block (1191–1195).

`mm_compute_batch` is recomputed at boot, on a policy write, and on memory hotplug only:
`mm_init.c.v7.2:212-233` registers `mm_compute_batch_notifier` through `hotplug_memory_notifier` for
`MEM_ONLINE`/`MEM_OFFLINE`; there is no CPU-hotplug hook for `vm_committed_as_batch`. CPU hotplug only folds a dying
CPU's delta (`percpu_counter.c.v7.2:266-285`, registered at `:403`). Therefore, after a CPU **hot-add** the stored
batch is the older, larger one (sized with fewer CPUs), and the true bound `stored batch × online CPUs` can exceed
the reported `band_kb = batch(today) × present × page`. Concrete, this host: `MemTotal 31721796 kB` → 7,930,449
pages; at 32 CPUs the stored batch is `7,930,449/32/256 = 968` pages and the reported band is
`968 × 32 × 4 = 123,904 kB`; after a hot-add to 64 CPUs without a policy write or memory hotplug, the true bound is
`968 × 64 × 4 = 247,808 kB` while the tool recomputes `484 × 64 × 4 = 123,904 kB`. The entry names memory hotplug
and balloons but not this direction; SKILL has no such error pattern. (Note the invariant this arithmetic also
shows: whenever the memory-sized term dominates, `batch × CPUs ≈ ram_pages/256`, so the band is ≈0.39 % of RAM and
does **not** shrink with fewer CPUs — worth stating so it is not read as a per-CPU allowance.)

### F4 (LOW) — `COMMIT_UNKNOWN` trigger list misses two real triggers

File: `SKILL.md:1188`. The committed tool also returns `COMMIT_UNKNOWN` for `--page-kb` not a power of two
(`unknown(["--page-kb must be a power of two (got %d)"])`) and for an argparse usage error (JSON with
`notes: ["usage: …"]`, exit 2). The registry row names the usage error; the decision table does not name either.
Also unstated: `--cases` is consumed only with `--selftest`, and `--meminfo`/`--vm-dir`/`--cpu-present` are ignored
under `--selftest` (runs 4 and 5), so a mistyped invocation silently reads the host instead of the fixture.

### F5 (LOW) — unresolvable citation form in one error bullet

File: `SKILL.md:1194`. "(`vm.rst`)" names a file, while the neighbouring bullets carry S497/S499/S513. The row that
carries the admin/user reserve documentation is S507 (`Documentation/admin-guide/sysctl/vm.rst` at v7.3,
`corpus/SOURCES.md:286`).

### F6 (LOW) — the recheck rule overstates its scope

File: `SKILL.md:1199-1200`. "re-read **every** claim row" — the frozen scope is every row that cites a v7.2 file
(46 of 49); three rows cite the 2014 commit patch and are out of scope in the contract, in `c1-scope.txt` and in
the ledger's own opening paragraph. A reader applying the SKILL sentence literally would demand three rechecks the
counter does not score.

### F7 (MED) — the entry's v7.3 batch pointer does not resolve in the lane

File: `corpus/knowledge/commit-runway-read-r53.md:51-52`. "the batch rule is unchanged at v7.3 (`mm_compute_batch`
in **the v7.3 copy** differs only by its line number)" — there is no `mm_init.c.v7.3` in the lane (`git ls-files`
returns only `…/mm_init.c.v7.2`), and no S row names `mm/mm_init.c` at v7.3. The fact itself is supported, but only
by a wave seat's own cgit fetch: `.ufo/waves/round-53/w1/Mo53Fr09.md` `## Cross-check outside my rows` records the
function as byte-identical between `sources-r53/mm_init.c.v7.2` (191–210) and the fetched v7.3 file (195–213). A
Boundary line resting on an uncommitted fetch is the exact shape C1's pin rule forbids; either commit the copy with
an S row or cite the seat receipt.

### F8 (LOW) — the dated host example no longer reproduces (committed bytes)

File: `corpus/knowledge/commit-runway-read-r53.md:44-45`. The committed text asserts "Committed_AS exceeds it —
`COMMIT_HEURISTIC` with `over_limit_not_enforced`". Two live reads of the same host on the same day: 38,513,360 kB
and 35,405,020 kB, both **below** the 47,583,772 kB limit, headroom +12,178,752 kB, `findings: []` (runs 2 and 13).
The frozen fixture `host-mode0-over-limit` preserves the over-limit snapshot the sentence came from. The sentence is
time-stamped, so it is not false, but it presents a moving reading as the host's state; the stable part is mode 0,
32 present CPUs, MemTotal 31721796 kB and `limit_consistent true`. The worktree's uncommitted rewrite (two readings,
one above and one below) already answers this; the committed bytes still carry it.

### F9 (LOW) — the section's claims that check out, recorded so the L1 need not re-derive them

* Selftest spelling and count: `MORI_COMMIT_RUNWAY_SELFTEST: PASS 23/23` on the committed copy (run 1, exit 0) —
  byte-identical to the SKILL string.
* Fixture arithmetic spot-checked by hand against the committed sources: 8 GiB/32 CPU case → batch `2097152/32/256
  = 256` pages, band `256 × 32 × 4 = 32,768 kB`, `usable = 4,194,304 − 4,022,272 − 139,264 = 32,768` → `LOW` at
  equality, `OK` one page above; 1 GiB/64 CPU floor case → `max(16, max(128,32)) = 128` pages, band 32,768 kB;
  1 CPU 2 GiB → batch 2048 pages, band 8,192 kB; 64 KiB page / 64 GiB → `67,108,864/64 = 1,048,576` pages,
  `1,048,576/64/256 = 64`, floor 128, band `128 × 64 × 64 = 524,288 kB`. All match the committed expectations.
* All eight `## Claims` rows: their quoted text occurs in the cited copy, whitespace collapsed (run 6, 8/8), which
  also confirms the entry's claim that the mode-2 batch rule, the fold condition, the global-only read, the
  global-vs-sum distinction and the policy-switch order are the v7.2 code as cited.
* `limit_consistent true` on the host with page size 4: the tool's recomputation equals the printed 47,583,772 kB,
  so the `MemTotal/page == totalram_pages()` assumption holds here (and `meminfo.c.v7.3:60` prints `i.totalram`
  in the same page units).

## 4. Drafts (fenced; nothing here is applied)

### D1 — replace `SKILL.md:1187` (decision table, `COMMIT_LOW` row)

```
| `COMMIT_LOW` (mode 2), exit 1 | `usable_kb ≤ band_kb`: the printed room is smaller than the error the kernel's
own read can carry, `band_kb = batch × present CPUs × page` (~1/256 of RAM when the memory-sized batch dominates,
S511). The test reads the global count, not the exact sum, and each CPU's local delta is signed (S512, S509) | a
refusal prediction or a calibrated alarm (FR8 open): inside the band a request can be accepted past the limit as
readily as refused; the band is not bytes of memory in use, not a measured deviation, and not a per-CPU allowance |
```

### D2 — replace `SKILL.md:1186` (decision table, `COMMIT_OK` row)

```
| `COMMIT_OK` (mode 2), exit 0 | `usable_kb` (limit − committed − admin and user reserves) exceeds `band_kb` by
more than the counter's worst-case error | guaranteed room for an allocation of `usable_kb`: the test is strict
(the charged total must stay *below* the limit, S499), the user reserve is per process (`min(total_vm/32, reserve)`)
and the band bounds the read on both sides |
```

### D3 — replace `SKILL.md:1188` (decision table, `COMMIT_UNKNOWN` row)

```
| `COMMIT_UNKNOWN`, exit 2 | an input is missing, unreadable or malformed, `--page-kb` is not a power of two, the
mode is outside 0–2, or the command line is unusable — the reason is in `notes` | zero room, or a pass |
```

### D4 — add to `SKILL.md` error patterns, after line 1195

```
- Reading `band_kb` as a measured deviation, as bytes of memory in use, or as a per-CPU allowance: it is
  `batch_pages × cpus_present × page`, and while the memory-sized term dominates (`ram_pages/cpus/256 >
  max(2 × cpus, 32)`) it collapses to about 1/256 of RAM, so it does not shrink with fewer CPUs (S511).
- Treating the counter's error as a one-way lag: each CPU's local delta is signed (`abs(count + amount) >= batch`,
  S512; `vm_unacct_memory` charges a negative amount, S509), so the kernel's read can sit above or below the exact
  sum by up to one batch per CPU — within the band a request can be refused while `/proc/meminfo` still shows room,
  and accepted after the exact sum has passed the limit.
- Reading a refusal as a charge that stays: `__vm_enough_memory` charges the request first and uncharges it on the
  error path, and the comparison is strict (`read < allowed`), so a request landing exactly on the limit is refused
  and leaves no trace in `Committed_AS` (S499).
- Recomputing the band from today's CPU count when the batch was sized earlier: `mm_compute_batch` runs at boot, on
  a policy write and on memory hotplug only — CPU hotplug does not resize it (`hotplug_memory_notifier` is its only
  registration, S511; a dying CPU only folds its delta, S512) — so after a CPU hot-add the true bound (stored batch
  × online CPUs) can exceed the reported band.
- Reading `single_request_cap_kb` (mode 0) as a total: it caps one request against RAM + swap; requests are not
  summed (S497, S499).
- Passing `--cases` without `--selftest`, or `--meminfo`/`--vm-dir`/`--cpu-present` with `--selftest`: each flag is
  honoured only in its own mode and silently ignored otherwise, so a mistyped command reads the host instead of the
  fixture.
```

### D5 — replace `SKILL.md:1199-1202` (release recheck rule)

```
When a tag newer than an entry's pinned tag exists and the entry says `recheck: on-release`, re-read every claim
row whose source is a kernel path at a tag (a row citing a commit patch is out of scope — the frozen scope is 46 of
the round-51/52 rows) against the same path at the new tag: a row is `held` when its old text still occurs, `absent`
otherwise, a `held` row carries its old text again, and either way its disposition (`holds` / `changed`) is a
reading of the new file, not of the old text (`.ufo/waves/round-53/count-c1.py`).
```

### D6 — replace the `pinned values` cell of `SKILL.md:1208`

```
`tools/fixtures/mori-commit-runway/cases.json` (23 cases at the data commit; no sha256 pin — its bytes are
protected only by the commit that lands them, so the independent check is the C2 counter's generated-fixture arm,
not this file)
```

### D7 — entry corrections (`corpus/knowledge/commit-runway-read-r53.md`, committed bytes)

(a) lines 13–15, direction sentence:

```
limit the kernel's own test can be wrong. `Committed_AS` in /proc/meminfo is an exact sum over CPUs; the mode-2
test reads only the global part of a per-CPU counter, whose read differs from that sum by less than one batch per
CPU in either direction (a CPU's local delta is signed: `vm_unacct_memory` charges a negative amount, S509, and a
dead CPU's delta is folded into the global count, S512). The
```

(b) line 18, the LOW sentence:

```
the band: there a refusal can arrive while the printed numbers still show room (the read above the exact sum,
pending negative deltas), and a request can be accepted after the exact sum has passed the limit (the read below
it); the band marks both directions, not a lag.
```

(c) lines 51–52, the v7.3 pointer — either commit `corpus/evidence/sources-r53/mm_init.c.v7.3` plus an S row, or:

```
- v7.2 bytes, the host's kernel line (7.2.11); the batch rule is unchanged at v7.3 — `mm_compute_batch` differs
  only by its line number, checked by wave seat Mo53Fr09 against a cgit v7.3 fetch
  (`.ufo/waves/round-53/w1/Mo53Fr09.md`, `## Cross-check outside my rows`); the v7.3 file is not committed.
```

(d) the Boundaries band bullet (53–55), add the CPU case:

```
- The band uses present CPUs and today's totalram; memory hotplug recomputes the batch, a balloon that changes
  totalram without hotplug does not, and CPU hotplug does not either — only a dying CPU's delta is folded
  (S512) — so after a CPU hot-add the true bound (stored batch × online CPUs) can exceed the reported band (this
  host: 968 pages × 64 × 4 KiB = 247808 KiB against a reported 123904 KiB). While the memory-sized term dominates
  the band is about 1/256 of RAM and does not shrink with fewer CPUs. The band is a bound for the common case, not
  a proof.
```

(e) data routing, not wording: the corrected direction sentence now cites S509, so S509's `used-by` in
`corpus/SOURCES.md:288` should gain `corpus/knowledge/commit-runway-read-r53.md`. S509's description already covers
`vm_acct_memory`/`vm_unacct_memory` at v7.3, and `mman.h` is byte-identical between v7.2 and v7.3 per that row.

## 5. Gates, surfaces, out-of-scope

* Gates: C2's predicate is the frozen counter and is not touched by anything here. Every run above used the
  committed tool from a scratch copy; the fixture arm and the live leg are the counter's, not mine.
* Touched surfaces: this report only (`.ufo/waves/round-53/w1/Mo53ScribeSkill.md`). Scratch
  `/fast/scratch/hyaku/mori-r53/Mo53ScribeSkill/` was created, used for the committed-copy runs and the mode-2
  fixture, and removed.
* Out of scope and left to the L1: whether F1/F3 change the frozen wording of the entry (they do not touch the
  counter); the choice between committing a v7.3 `mm_init.c` copy and citing the seat receipt; whether the
  registry `pinned values` cell gains a digest (a round-54 route if the L1 wants a pin, since `count-c2.py` only
  requires n ≥ 12).
* Named limit of this seat: I verified the quotes against the committed copies and the arithmetic of five fixtures
  by hand; I did not re-fetch v7.2/v7.3 from cgit (the lane's copies are the reviewed surface), and I did not run
  `count-c2.py` (its receipt at the data commit is `C2=met … agree=80 disagree=0`, and re-scoring is not a seat's
  job here).
* UNVERIFIED: whether the entry's committed host reading was accurate at the minute it was written — only that it
  does not reproduce in two reads on 2026-10-26.

## Findings

- HIGH — none.
- MED — `corpus/knowledge/commit-runway-read-r53.md:14-18` with `SKILL.md:1187`: the counter's error is called a
  one-way lag while the refusal-with-room story needs the opposite sign; each CPU's delta is signed
  (`percpu_counter.c.v7.2:100`, `mman.h.v7.3:76-84`), so the band is two-sided (F1, drafts D1/D7a/D7b).
- MED — `corpus/knowledge/commit-runway-read-r53.md:51-55` and `SKILL.md:1191-1195`: CPU hotplug does not recompute
  `vm_committed_as_batch` (only `hotplug_memory_notifier`, `mm_init.c.v7.2:212-233`; a dying CPU merely folds,
  `percpu_counter.c.v7.2:266-285`), so after a hot-add the true bound can exceed the reported band — 247,808 KiB
  against 123,904 KiB on this host's RAM at 64 CPUs (F3, drafts D4/D7d).
- MED — `corpus/knowledge/commit-runway-read-r53.md:51-52`: "the v7.3 copy" does not resolve; no
  `mm_init.c.v7.3` is committed and no S row names `mm/mm_init.c` at v7.3; the fact rests on
  `.ufo/waves/round-53/w1/Mo53Fr09.md` (F7, draft D7c).
- LOW — `SKILL.md:1208` (pinned-values cell): `cases.json` has no digest pin and the counter's selftest arm only
  needs `PASS n/n`, n ≥ 12; the real pin is the generated-fixture arm (F2, draft D6).
- LOW — `SKILL.md:1188`: `COMMIT_UNKNOWN` trigger list omits `--page-kb` not a power of two and the usage error, and
  the section never says `--cases`/input flags are mode-local (runs 4, 5) (F4, drafts D3/D4).
- LOW — `SKILL.md:1194`: bare `(vm.rst)` citation; the S row is S507 (F5, draft D4 note).
- LOW — `SKILL.md:1199-1200`: "every claim row" overstates the frozen scope (46 of 49; patch rows excluded) (F6,
  draft D5).
- LOW — `corpus/knowledge/commit-runway-read-r53.md:44-45`: the committed host example (Committed_AS above the
  limit, `over_limit_not_enforced`) does not reproduce — two reads 38,513,360 / 35,405,020 kB against a
  47,583,772 kB limit, headroom +12,178,752 kB, no finding; the worktree rewrite already addresses it (F8).

# ConnSiblings — round 47 wave w1 — Cross-lane scan and proposal synthesis

Seat: `ConnSiblings` (leaf member; no subagents dispatched).
Lane: mori-shokunin (森, fleet and host observability: detection and report only).
Fleet root: `/home/vgpnk/Projects/shokunin`.
Lane repo: `/home/vgpnk/Projects/shokunin/mori-shokunin`.
Freeze commit: `63eecf2738db96f46b0bd02b1b2dfd66787493d0` (entering tip `2d85e33d14198d388fd3cda9cc15ec07e57e7a53`).

Scope: Cross-lane read-only scan of sibling lanes under `/home/vgpnk/Projects/shokunin/*-shokunin/corpus` for `mark_victim`, `oom tracepoint`, `tracefs`, `eBPF OOM`, and registry-pin checking tools. Report overlaps with round 47 C1/C2 (path:line), contested scope per `mori-shokunin/PROVINCE.md` Adjacent section, patterns worth reusing, and one non-obvious synthesis move improving declared axes without harming another.

---

## 1. Cross-lane scan results (read-only evidence)

### 1.1 `mark_victim`
- **Sibling corpora (`/home/vgpnk/Projects/shokunin/*-shokunin/corpus`):**
  - **0 matches found** across all 20 sibling lane `corpus/` directories.
- **Mori corpus (`/home/vgpnk/Projects/shokunin/mori-shokunin/corpus`):**
  - `corpus/README.md:649` — summarizes the OOM reaper lifecycle (`mark_victim` → `wake_reaper` → `skip`/`start`/`finish_task_reaping`, all pid-only after mark).
  - `corpus/SOURCES.md:11` (S005) — Linux OOM trace events `include/trace/events/oom.h:76,82-105` (`mark_victim`).
  - `corpus/SOURCES.md:254` (S475) — Linux `include/trace/events/oom.h` at tag v7.2; `mark_victim` entry at lines 82–92.
  - `corpus/SOURCES.md:255` (S476) — Linux v7.2 call sites; `mark_victim` in `mm/oom_kill.c:774` in `mark_oom_victim`.
  - `corpus/SOURCES.md:256` (S477) — Host tracefs receipt `.ufo/waves/round-47/evidence/host-tracefs.txt` listing `mark_victim` format fields.
  - `corpus/evidence/sources-r47/include_trace_events_oom.h:76` — `TRACE_EVENT(mark_victim, ...)`.
  - `corpus/evidence/sources-r47/mm_oom_kill.c:774` — `trace_mark_victim(tsk, cred->uid.val);`.
  - `corpus/knowledge/oom-tracepoints-r47.md:12,26,34,41,56,74` — C2 entry cataloguing `mark_victim` schema, fields (`pid`, `comm`, `total_vm`, `anon_rss`, `file_rss`, `shmem_rss`, `uid`, `pgtables`, `oom_score_adj`), and call site.
  - `corpus/lessons/round-12.md:131`, `corpus/lessons/round-44.md:56`, `corpus/lessons/round-45.md:117` — previous round citations and errata.
- **Sibling repositories outside `corpus/` (wave snapshots):**
  - `tsukuroi-shokunin/.ufo/waves/round-25/w2/RerunC2/src/S119.raw:774`
  - `tsukuroi-shokunin/.ufo/waves/round-29/w1/ScribeSrcOomKill/oom_kill.c:774`
  - `tsukuroi-shokunin/.ufo/waves/round-33/a3w1/SrcKernelOomKill/oom_kill.c:774`
  All three are snapshots of Linux v7.2 `mm/oom_kill.c` captured during tsukuroi's OOM investigations (tsukuroi S119, S149, S182), which contain `trace_mark_victim(tsk, cred->uid.val);` at line 774.
- **Staged assimilation corpus (`/home/vgpnk/Projects/shokuknow`):**
  - `/home/vgpnk/Projects/shokuknow/merge/mori/knowledge/corpus/knowledge/oom-tracing-tracepoints-r42.md:15-16,41,56` — staged entry citing ROMA paper (S507), claiming "The OOM lifecycle an observer can hook has exactly three named tracepoints" (`mark_victim`, `start_task_reaping`, `finish_task_reaping`).

### 1.2 `oom tracepoint` / `tracepoint`
- **Sibling corpora (`*-shokunin/corpus`):**
  - **0 matches found** for `oom.*tracepoint` or `tracepoint.*oom` or bare `tracepoint`.
- **Closest sibling mention:**
  - `tsukuroi-shokunin/corpus/knowledge/degraded-triage-r4.md:206,531` mentions `ftrace` as an out-of-scope discriminating probe requiring root elevation: "owner: operator or a later lane with the right tooling."

### 1.3 `tracefs`
- **Sibling corpora (`*-shokunin/corpus`):**
  - **0 matches found** in any sibling lane's corpus.
- **Sibling repository evidence (wave artifacts and mounts):**
  - `tsukuroi-shokunin/.ufo/waves/round-24/w1/ExecMirrorTimestamps/host-extra-pkglist.txt:6338-6339` — lists `libtracefs 1.8.3-1` and `libtracefs-docs 1.8.3-1`.
  - `tsukuroi-shokunin/.ufo/waves/round-24/w1/ExecSymlinkMountProbe/probe-run1.txt:48,96,140` — `findmnt` output recording `tracefs` mounted at `/sys/kernel/tracing`.
  - `kumitate-shokunin/.ufo/waves/round-49/r49/ScoutMountinfoFields.md:205` — mountinfo record `1131 1124 0:14 / /sys/kernel/tracing ... - tracefs tracefs rw`.
  - `souji-shokunin/census/round-27/sources/glocalfile.c:734` — filesystem type magic `case 0x74726163: return "tracefs";`.

### 1.4 `eBPF OOM` / `eBPF` / `bpf`
- **Sibling corpora (`*-shokunin/corpus`):**
  - `tsukuroi-shokunin/corpus/knowledge/root-dac-decision-r12.json:395,397,404` and `root-dac-decision-r12.md:62,79` — observes that `/sys/kernel/security/lsm` contains `bpf` (BPF-LSM), but notes loaded BPF programs were not enumerated (non-root) and foreign LSM mediation remained unknown.
  - `kaidoku-shokunin/corpus/knowledge/2026-10-13-ghidra-install.md:29` — lists Ghidra processor modules including BPF and eBPF.
  - `kaidoku-shokunin/corpus/knowledge/2026-10-20-r20-objdump-architecture-list.md:10` — lists objdump disassembler selectors `bpf`, `xbpf`.
  - `kasegi-shokunin/corpus/source-snapshots/round-24/S011.txt:133,296` — lexicon entries for BPF and eBPF.
  - `chousa-shokunin/corpus/evidence/round32/c1-count-v2.py:91` — strace invocation using `--seccomp-bpf`.
- **Mori province boundary (`PROVINCE.md:56`):**
  - `FR13 — eBPF kill/OOM tracing (art F5). Boundary: privilege and version matter; a resident tracer is outside the census, so retain this as knowledge/frontier only.`

---

## 2. Registry-pin checking tools across sibling lanes

A fleet-wide survey of `tools/` and `SKILL.md` registries across sibling lanes identified four distinct registry-checking tools:

| Lane | Tool | Scope & Contract | Key Patterns |
|---|---|---|---|
| `tameshi-shokunin` | `tools/registry-check.py`<br>`tools/registry-replay.py`<br>`tools/pin-disposition.py` | Validates entry-registry JSON / Markdown tables with kinds `gate`, `probe`, `selftest`. Evaluates `--rev` clones. | **Subreaper & pidfd management (`PR_SET_CHILD_SUBREAPER` 36)** ensures no child process escapes or holds pipes (`:391-611`).<br>**Strict `git_env()` scrubbing** strips all `GIT_*` env vars (`:149-167`).<br>**Argv escape detection** (`_argv_outside_fleet`, `:632-645`). |
| `tsukuroi-shokunin` | `tools/check-registry-coverage.py`<br>`tools/check-self-assessment.py` | Audits operative `SKILL.md` 8-column gate/probe tables against committed tools. Evaluates selftests under `git archive`. | **Round-32 child environment allow-list (`clean_env()`)** passes only fixed base `{"PATH": "/usr/bin:/bin", "LC_ALL": "C"}` (R29-GIT-ENV-LEAK rule 74).<br>**Hermetic `GitReader`** (`git show <rev>:<path>`) reads committed blobs without worktree contamination. |
| `kama-shokunin` | `tools/gate-registry-check.py` | Traverses `SKILL.md` 5-column registry tables, discovers tracked counters via regex `(?:\.ufo/waves/round-[^/]+/count-[^/]+|tools/round[0-9]+-[A-Za-z0-9._-]+)\.py`. | Validates that every counter in the repo is registered in SKILL.md. |
| `souji-shokunin` | `tools/souji-gate-check.py`<br>`tools/souji-rev-pin.py` | Assimilation gate checker; validates durable revision resolution (`refs/heads`, `refs/tags`, `refs/remotes`) and takes SHA-256 snapshots of input files at rev. | **Scrubbed `_env()`** prevents inherited git state.<br>Private sandbox test execution under `/var/tmp`. |
| `mori-shokunin` (C1) | `tools/mori-pin-check.py` | Re-measures `SKILL.md` 8-column self-test cell pins (tallies and digests) against live `--selftest` runs under `git archive` export. | Compares observed tallies and sha256 digests against pinned values.<br>Guards against dropped pin keys from `--baseline-rev`.<br>Enforces `--min-tally-pins 26`. |

### Baseline check of mori's C1 instrument (reproduced):
Command:
```sh
TMPDIR=/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r47-ConnSiblings python3 tools/mori-pin-check.py --rev 2d85e33d14198d388fd3cda9cc15ec07e57e7a53 --min-tally-pins 26 --baseline-rev 2d85e33d14198d388fd3cda9cc15ec07e57e7a53
```
Output:
```
pin line=912 kind=tally prefix=MORI_SOURCES_APPENDONLY_SELFTEST state=mismatch pinned='pass=15 fail=0' observed='pass=22 fail=0' rc=0 cmd='python3 tools/mori-sources-appendonly.py 2d85e33d14198d388fd3cda9cc15ec07e57e7a53 --selftest'
PIN_CHECK=unmet tally_pins=26 digest_pins=5 mismatches=1 unparsed=0 no_command=0 dropped=0 min_tally_pins=26 rev=2d85e33d14198d388fd3cda9cc15ec07e57e7a53 baseline=yes
```
Exit code: `1` (Wall time: 70.16s). Confirms C1 enters `unmet` strictly due to line 912's stale pin.

---

## 3. Contested scope per `mori-shokunin/PROVINCE.md` Adjacent section

### 3.1 `tsukuroi-shokunin` (Host OS, systemd, drivers, boot diagnosis)
- **Boundary (`PROVINCE.md:12-16, 66` & `tsukuroi-shokunin/PROVINCE.md:30-33, 49` ADJ-04):**
  - Tsukuroi owns OS substrate diagnosis (kernel error ring, pacman, systemd units, driver/firmware health).
  - Mori owns fleet & host observability, progress/silence grading, and wave settlement.
  - Under `ADJ-04`, tsukuroi routes host pressure and kill signals to mori for fleet/wave correlation.
- **Shared evidence without contested ownership:**
  - `memory.events` (`oom_kill` counter): tsukuroi uses it as a presence flag for OS memory triage (`kill-event-deep-r8.md:120-134`); mori reads it as fleet resource runway (`PROVINCE.md:9, 24`).
  - `/proc/pressure/memory`: tsukuroi reads avg300 for host triage (`tsukuroi-census.sh:400`); mori reads one-shot system pressure for resource runway (`tools/mori-pressure.py`).
  - Linux v7.2 `mm/oom_kill.c`: tsukuroi cites it as S182 (`mm/oom_kill.c:1168-1170` global vs memcg OOM); mori cites it as S476 (`mm/oom_kill.c:567, 578, 582, 595, 673, 774` tracepoints).
- **Tracing boundary:**
  - Neither lane runs a resident kernel tracer. In `tsukuroi-shokunin/corpus/knowledge/degraded-triage-r4.md:206,531`, `ftrace` was deferred to the operator or a future lane with appropriate tooling. In mori, FR13 explicitly classifies resident eBPF tracing as outside the census (knowledge/frontier only).
  - Reading tracefs is non-resident, host-only read-only probe evidence (`sudo -n ls` and `cat` under `/sys/kernel/tracing/events/oom`), not active tracing (`contract.md:76-78`).

### 3.2 `kumitate-shokunin` (Orchestration & wave lifecycle)
- Kumitate owns task/hub dispatch, routing semantics, and wave lifecycle (`PROVINCE.md:65`).
- Mori passively grades `.ufo/waves/*` filesystem settlement shape only (`tools/mori-wave-settlement.py`), never altering dispatch or deciding lifecycle results.

### 3.3 `kama-shokunin` (Model serving & endpoints)
- Kama owns local model-serving and endpoint health (`PROVINCE.md:67`). Mori does not infer serving health from host/resource signals.

### 3.4 `kagi-shokunin` (Secrets & vault operations)
- Kagi owns secrets and credential hygiene (`PROVINCE.md:68`). Mori never inspects credential material.

### 3.5 `souji-shokunin` (Hygiene & residue reclamation)
- Souji lists own-uid scratch residue and proposes removal for operator approval (`PROVINCE.md:69`). Mori reports runway, never performing reclamation.

---

## 4. Reusable patterns from sibling lanes

1. **Environment scrubbing in tool execution runners (`clean_env()`):**
   - Proven in `tsukuroi-shokunin/tools/check-registry-coverage.py:34-46` (R29-GIT-ENV-LEAK quality rule 74) and `tameshi-shokunin/tools/registry-check.py:149-167`.
   - In `mori-pin-check.py:182-199`, `run_cmd()` inherits `dict(os.environ)` when running tool `--selftest` commands. While it sets `TMPDIR` and `PYTHONDONTWRITEBYTECODE`, any inherited `GIT_*` variable (`GIT_DIR`, `GIT_WORK_TREE`, `GIT_INDEX_FILE`) will leak into git-calling selftests (such as `.ufo/waves/round-40/conform.py` pinned at `SKILL.md:911`). Adopting `clean_env()` with scrubbed `GIT_*` guarantees caller-independent execution.
2. **Subreaper & process isolation for test runners:**
   - Proven in `tameshi-shokunin/tools/registry-check.py:391-611`. Using `PR_SET_CHILD_SUBREAPER` and pidfds ensures that background descendants spawned during `--selftest` runs do not hold open pipes or survive as orphan processes.
3. **Structured multi-class boundary accounting:**
   - Proven in `tsukuroi-shokunin/corpus/knowledge/kill-oom-boundary-r33.md`. Documenting each signature, owner retention, handoff trigger, and declared sibling scope prevents territorial encroachment while preserving evidence sharing.

---

## 5. Non-obvious proposal: Cross-lane boundary synthesis for C2 depth and C1 calibration

### 5.1 Evidence & observation
1. **The staged entry contradiction:**
   The staged entry `/home/vgpnk/Projects/shokuknow/merge/mori/knowledge/corpus/knowledge/oom-tracing-tracepoints-r42.md` claims "The OOM lifecycle an observer can hook has exactly three named tracepoints" (`mark_victim`, `start_task_reaping`, `finish_task_reaping`), quoting solely the ROMA paper (S507).
2. **The true kernel interface:**
   Committed Linux v7.2 `include/trace/events/oom.h` (S475) defines **eight** `TRACE_EVENT`s. ScribeCatalogue's draft (`ScribeCatalogue.md:16-24`) catalogs all eight:
   - Allocator retries: `reclaim_retry_zone` (`mm/page_alloc.c:4630`), `compact_retry` (`mm/page_alloc.c:4265`)
   - Victim selection: `mark_victim` (`mm/oom_kill.c:774`)
   - Reaper lifecycle: `wake_reaper` (`mm/oom_kill.c:673`), `start_task_reaping` (`mm/oom_kill.c:582`), `finish_task_reaping` (`mm/oom_kill.c:595`), `skip_task_reaping` (`mm/oom_kill.c:567, 578`)
   - Score adjustment: `oom_score_adj_update` (`fs/proc/base.c:1158`)
3. **The cross-lane connection to tsukuroi:**
   In `tsukuroi-shokunin/corpus/knowledge/kill-event-deep-r8.md:295`, tsukuroi's open research question Q12 states:
   `"Origin of the session-wide +200 oom_score_adj (not in uwsm text files) — launcher/session source or a controlled launch trace."`
   In mori round 27 (`oom-victim-selection-r27.md`), mori identified that the `+200` score comes from systemd's per-user manager (`user@1000.service`), not the harness.
   In the Linux kernel, `oom_score_adj_update` is emitted inside `__set_oom_adj()` (`fs/proc/base.c:1158`) whenever *any* process writes to `/proc/<pid>/oom_score_adj`.
4. **C1 simplification vs calibration:**
   `SimpInstruments.md:35-49` identified dead parameter `scratch` in `mori-pin-check.py`'s `run_cmd` and `check`, while `tsukuroi` and `tameshi` demonstrate that tool runners require `GIT_*` scrubbing to be truly hermetic.

### 5.2 Affected axes
- **Depth (`depth` entering 5, lowest non-retired axis):** Improved. Connects the 8 tracepoints into four functional phases of the kernel OOM subsystem (pre-kill allocator pressure, victim selection, asynchronous reaper execution, dynamic scoring updates), demonstrating why the 5 non-ROMA tracepoints are critical to observability.
- **Adjacency (`adjacency` entering 6):** Improved. Demonstrates how mori's knowledge of `oom_score_adj_update` directly answers tsukuroi's adjacent open question Q12 regarding score attribution without overstepping the boundary (retaining it as kernel structural knowledge under FR13, detection-and-report only, rather than resident tracing).
- **Calibration (`calibration` entering 5, lowest non-retired axis):** Preserved and protected. Pinpoints the clean child environment pattern (`clean_env`) for future C1 runner hardening without mutating the frozen w1 contract.
- **Other axes (`coverage`, `operability`, `freshness`):** Unharmed.

### 5.3 Proposed move
In `corpus/knowledge/oom-tracepoints-r47.md` (and the round 47 knowledge surface), synthesize C2's 8-event catalogue with the cross-lane boundary:
1. **Four-phase functional taxonomy:** Group the 8 tracepoints explicitly into their operational domains:
   - **Phase 1: Pre-OOM allocation retry pressure** (`reclaim_retry_zone`, `compact_retry` in `mm/page_alloc.c`). Observes whether the system exhausted reclaim and compaction before entering OOM.
   - **Phase 2: Victim selection & memory marking** (`mark_victim` in `mm/oom_kill.c`). The sole identity-bearing event recording task PID, comm, UID, VM, RSS, and page table footprints.
   - **Phase 3: Asynchronous memory reaping** (`wake_reaper`, `start_task_reaping`, `finish_task_reaping`, `skip_task_reaping` in `mm/oom_kill.c`). Traces whether the kernel successfully detached the victim's anonymous memory or was forced to skip it (e.g., MMF_UNSTABLE).
   - **Phase 4: Dynamic victim scoring provenance** (`oom_score_adj_update` in `fs/proc/base.c`). Traces who modified `oom_score_adj`.
2. **Explicit adjacency resolution:** Document in the entry's boundary section that Phase 4 (`oom_score_adj_update`) provides the theoretical tracing interface that answers tsukuroi's open question Q12 (`kill-event-deep-r8.md:295`), while reaffirming mori's FR13 boundary: mori retains the field schema and emission site as structural knowledge and does not deploy resident tracing on the host.
3. **Future C1 hardening recommendation:** For post-freeze/w2 maintenance, apply the `tsukuroi`/`tameshi` `clean_env()` pattern to `mori-pin-check.py` to strip `GIT_*` environment variables before running tool `--selftest` commands.

### 5.4 Risks & boundary compliance
- **FR13 compliance:** Documenting the 8 tracepoints and `oom_score_adj_update` must remain strictly structural knowledge and read-only tracefs listing (`contract.md:76-78`). It must not propose installing eBPF programs, ftrace triggers, or modifying kernel parameters.
- **Contract immutability:** Neither `tools/mori-pin-check.py` nor `count-c2.py` may be edited in w1; the proposed move works strictly within the frozen contract predicates (P-C1 and P-C2) and guides the knowledge integration.

### 5.5 Verification
1. **C2 verification:**
   Run `python3 .ufo/waves/round-47/count-c2.py R` against the landed revision. Expected output:
   `C2=met events=8 rows=8 name_mismatch=0 field_mismatch=0 callsite_mismatch=0 pin_mismatch=0 source_row=ok provenance=ok` (exit 0).
2. **C1 verification:**
   Run `python3 tools/mori-pin-check.py --rev R --min-tally-pins 26 --baseline-rev 2d85e33d14198d388fd3cda9cc15ec07e57e7a53` against the landed revision. Expected output:
   `PIN_CHECK=met tally_pins=26 digest_pins=5 mismatches=0 unparsed=0 no_command=0 dropped=0 min_tally_pins=26` (exit 0).
3. **Do-nothing control verification:**
   Run `count-c2.py` against `.ufo/waves/round-47/controls/control-c2-staged.md` and `.ufo/waves/round-47/controls/control-c2-three.md` to verify both controls stay unmet (rc=1).

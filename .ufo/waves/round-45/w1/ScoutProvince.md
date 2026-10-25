# ScoutProvince — PROVINCE / QUALITY fit check (round 45, wave 1)

Scope: does the round's assimilation theme fit mori's province, do the two packaged
entries belong to another lane, and which QUALITY criteria does the theme violate
as drafted. Leaf seat: read-only; nothing edited outside this file.

Measured revision: `3ad8faaa637ae466c61f9427fea1c208bf49ea82` (round-45 freeze commit;
entering tip per contract `554ff416459c92f0dea9762f834a556df2990187`).
Read: `PROVINCE.md`, `corpus/QUALITY.md`, `.ufo/waves/round-45/contract.md`,
`.ufo/waves/round-45/w1-spec.json`, `tools/mori-census.sh`,
`tools/mori-silence-cases.sh`, and the staged entries under
`/home/vgpnk/Projects/shokuknow/merge/mori/knowledge/corpus/knowledge/`:
`who-sets-the-scope-cap-r45.md`, `cap-control-wording-r52.md`,
`cgroup-surface-two-levels-r49.md`, `selftest-cannot-tell-levels-r49.md`.

Confidence: high on the code facts (line-quoted, re-read at HEAD); high on the
PROVINCE/QUALITY quotes; the live counter reading is an observation without a
baseline and is not used as a claim (see §1.3).

## Verdicts

1. **Theme is in province.** It is a wording/measurement-scope correction to mori's
   *own* census row and *own* selftest — a read-only observation surface. PROVINCE
   lines 6–10, 24 and 26 own the `memory.events` read; lines 12–18 only forbid
   *owning OS state* and *remediation*, which the theme does not do.
2. **Both packaged entries are correctly refused.** `who-sets-the-scope-cap-r45.md`
   is runner-configuration semantics (kumitate/operator), and
   `cap-control-wording-r52.md` is a throttle-vs-kill tuning recommendation for that
   same runner — neither is a host record mori reads. Reason + flip condition below.
3. **The theme as drafted violates QUALITY #2/#9 (no locator), #25/#34 (the
   "service's own `memory.events`" clause is contradicted by the code), and risks
   #14/#61/#12.** The admitted entry must cite `tools/mori-census.sh:1862`,
   `:1705-1712`, `:3252-3254` at its own revision, and must state the level **per
   branch** of the read.

---

## 1. The theme and PROVINCE fit

### 1.1 The lines that make a host-observability *reading* in-province

> **Domain:** fleet & host observability (森) — whether the fleet, its waves and
> its host are alive and progressing.
> — `PROVINCE.md:3-4`

> **Owns (read-only probes):** shokunin watchdog liveness (pid, start time, log
> freshness, lane counters); `.ufo/waves/*` settlement state (registry + results
> pair); kill/OOM-related catalog-ID records and signal-11 coredump records from
> independently labeled user/system journals, plus cgroup `memory.events` and the explicit same-boot journal window after a retained anchor;
> resource runway (disk on the fleet root and `/tmp`, memory pressure); lane silence grading (silent / progressing / progressing-weak).
> — `PROVINCE.md:6-10`

> `SURFACE cgroup` retains selected-scope kernel memory-event counters, not a replacement for all journal alarms.
> — `PROVINCE.md:24` (Core, Kill/OOM classes row)

> **Resource runway** — `SURFACE disk` and `SURFACE cgroup`: default `df -P` targets `$ROOT` and `/tmp`, since-boot device-write average, memory PSI/fill/avail, and scope high-watermark.
> — `PROVINCE.md:26`

The probe list is explicitly *read-only*, and the same census file this theme
corrects is named in Core twice (the selected-scope counters at :24, the resource
runway at :26). A rule about **how mori's own emitted row names the level it read**
is therefore a rule about an owned surface, not an expansion. The round-24
precedent states the read-only shape without qualification:

> Read-only: the probe opens the PSI files read-only, registers no PSI trigger,
> writes nothing to `/proc`, `/sys` or a cgroup, and changes no service or package.
> — `PROVINCE.md:250-251`

and the contrast with a resident instrument is stated for FR13:

> a resident tracer is outside the census, so retain this as knowledge/frontier only.
> — `PROVINCE.md:56`

The theme's proposed work is exactly (a) a level/scope token in the emitted row and
(b) three distinct fixture files for three distinct env paths. Both are edits to
`tools/mori-census.sh` / `tools/mori-silence-cases.sh` — read-only w.r.t. the host.
**No PROVINCE amendment is required**; if the L1 wants the level-naming rule
recorded as a standing statement, it belongs in an append-only round-45 note (the
convention already used at `PROVINCE.md:274` and `:345`), not a rewrite of
`PROVINCE.md:6-10`.

### 1.2 The lines that make remediation / host mutation out of province

> **Refuses:** dispatch and orchestration mechanism (→ kumitate); OS package,
> systemd unit, driver/firmware and boot state (→ tsukuroi) — mori reads journal
> and cgroup events as fleet evidence and reports them, never owning OS state;
> endpoint and model-serving health (→ kama); credential material (→ kagi).
> **Detection and report only — never remediation.**
> — `PROVINCE.md:12-16`

> **Out of province → report, never absorb.**
> — `PROVINCE.md:18`

Same boundary stated per item:

> Boundary: `df` capacity percentages cannot detect quota exhaustion; observe and report only, never change quota state.
> — `PROVINCE.md:45` (FR2)

> Boundary: inactive killers are unavailable, not zero; `memory.events oom_kill` does not cover every userspace kill; never enable or tune a killer.
> — `PROVINCE.md:53` (FR10)

> Boundary: a PSI trigger watcher is resident, not a one-shot census probe; system CPU `full=0` is not evidence of no stall.
> — `PROVINCE.md:55` (FR12)

> Kernel-visible mechanism observations do not transfer quota configuration,
> cause or reclamation authority: tsukuroi/operator own configuration/diagnosis, souji
> proposes eligible residue handling, and operator approval owns reclamation.
> — `PROVINCE.md:228-230` (round-23 note)

**Consequence for the theme:** naming a cgroup level is a *reading* rule and stays
inside `PROVINCE.md:16`. The moment the entry tells anyone to set `MemoryHigh=`,
change `MemoryMax=`, or re-target the census at the service instead of the slice,
it crosses `:16`/`:18` into configuration advice — the exact defect that refuses
`cap-control-wording-r52.md` (§2.2). The entry should state the level, not the
policy.

### 1.3 The two theme pins, verified at HEAD

**(a) The census row carries two levels and names neither level+scope pair.**
`tools/mori-census.sh:1862`:

```
emit_surface cgroup "$st" "cmd=$cmd; oom_kill=$oom_kill oom=${oom:-?} high=${high:-?} max=${max:-?} current=${cur:-?}; local_oom_kill=${service_oom_kill:-unavailable} psi_some_avg10=...
```

Read sites `:1705-1712`:

```
LOCAL_EVENTS=${MORI_CGROUP_LOCAL_EVENTS:-${CGROUP_EVENTS%.events}.events.local}
SERVICE_EVENTS=${MORI_CGROUP_SERVICE_EVENTS:-/sys/fs/cgroup/user.slice/user-$(id -u).slice/user@$(id -u).service/memory.events}
service_oom_kill=''
if [ -r "$LOCAL_EVENTS" ]; then
  service_oom_kill=$(cgroup_field "$LOCAL_EVENTS" oom_kill)
elif [ -r "$SERVICE_EVENTS" ]; then
  service_oom_kill=$(cgroup_field "$SERVICE_EVENTS" oom_kill)
fi
```

Precise statement (narrower than the staged entry's): `oom_kill` is the selected
slice's **hierarchical** `memory.events`; `local_oom_kill` is the slice's
**non-hierarchical** `memory.events.local` when that file is readable, and the
**service's hierarchical** `memory.events` only in the fallback branch. The row
names the counter (`oom_kill`, `local_oom_kill`) but not the level+scope pair, and in
the fallback branch the `local_` token is not local at all.

**(b) The selftest pins all three level paths to one fixture file.**
`tools/mori-census.sh:3252-3254` (inside `sut_env`):

```
MORI_CGROUP_EVENTS="$FX/cgroup/memory.events"
MORI_CGROUP_SERVICE_EVENTS="$FX/cgroup/memory.events"
MORI_CGROUP_LOCAL_EVENTS="$FX/cgroup/memory.events"
```

`tools/mori-silence-cases.sh:518-520` repeats the same three-way pin. The only
OOM-positive case writes that one file with `oom_kill 1` and all three env paths
read it (`:3905-3908`), so the case cannot distinguish slice-hierarchical from
slice-local from service-hierarchical. **Verified: no selftest case can tell the
levels apart.** (Adjacent, not my claim: the `CGROUP_OOM_KILL` finding at `:1844`
prints `path=${LOCAL_EVENTS}` even when the value came from `SERVICE_EVENTS` — that
is `ScoutCensusBytes`' item.)

**Live observation, no baseline — not a claim.** One read at 2026-10-25 of the
host's user slice returned `oom_kill 539` (hierarchical) and `oom_kill 0`
(`memory.events.local`); the mount line has no `memory_localevents`, so
`memory.events` is hierarchical on this host. That shows the level distinction is
material, but the counters are cumulative and I did **not** read the cgroup
instance/boot baseline, so per **QUALITY #12** (`corpus/QUALITY.md:23`: "No
cumulative counter is read without its baseline") this must not be reported as a
kill count, current load, or a census finding.

---

## 2. The two packaged entries the round proposes to refuse

Both live under
`/home/vgpnk/Projects/shokuknow/merge/mori/knowledge/corpus/knowledge/` and are
staged by `MERGE-REPORT.md:52` and `:96`. Both carry `coverage-map: FR1`, and both
are own-work entries whose subject is the *kumitate* runner's per-scope
configuration, not a host surface mori probes.

### 2.1 `who-sets-the-scope-cap-r45.md`

**One-line reason:** it answers *who configured* the runner's per-scope cap — a
kumitate/operator configuration fact — not a host record mori reads; admitting it
makes mori the holder of another lane's runner semantics.

The entry itself reaches that conclusion:

> It does not license remediation: the runner belongs to the kumitate lane.
> — `who-sets-the-scope-cap-r45.md:52`

PROVINCE/QUALITY lines that justify refusal:

> **Refuses:** dispatch and orchestration mechanism (→ kumitate); …
> — `PROVINCE.md:12`

> | kumitate | Owns OMP task/hub orchestration and wave plan/run/record/collect semantics; …
> — `PROVINCE.md:65`

> **Detection and report only — never remediation.** / **Out of province → report, never absorb.**
> — `PROVINCE.md:16,18`

> 25. A claim is admitted at the scope it was measured; narrowing is an explicit correction, not a silent edit.
> — `corpus/QUALITY.md:50`

The `coverage-map: FR1` is a scope overclaim under #25: FR1 is *event-time
attribution and fleet correlation*, whose own boundary says

> a host record alone does not prove a fleet-caused kill.
> — `PROVINCE.md:44`

whereas this entry's subject is a default value in another lane's launcher. It also
fails #2 (measured anchor): its `recheck` is
`` `grep -c 'cap-run-' …` -> many (ran 2026-10-24) `` (`:7`) — "many" is not a
measured anchor, and the quoted runner block (`:17`) carries no `path:line`.

**Flip condition (what would have to change for the lane to admit it):** either
(i) recast the subject as a **host record** mori already reads — e.g. quote a kernel
OOM record's `oom_memcg=…/app.slice/cap-run-….scope` with its journal path, boot,
timestamp and receipt, and claim only "the killed scope's name has the runner's
`cap-run-<pid>-<ms>-<hex>` shape" (an observation under FR1's boundary, not "who set
the cap"); **or** (ii) kumitate's PROVINCE cedes runner-configuration reading to
mori and the operator records that assignment, in which case the owner's statement —
not the campaign's `file://` note — must be the source row.

### 2.2 `cap-control-wording-r52.md`

**One-line reason:** it teaches a throttle-vs-kill **design choice** for that same
runner (add `MemoryHigh=`), which is configuration advice to another lane; mori
reports counters, it does not tune another lane's cgroup.

The entry says so in its own limits:

> It does not choose for the owner. Adding `MemoryHigh=` to the runner changes
> what the fleet's kills mean, and that is the kumitate lane's decision.
> — `cap-control-wording-r52.md:37-38`

PROVINCE/QUALITY lines that justify refusal:

> **Detection and report only — never remediation.** / **Out of province → report, never absorb.**
> — `PROVINCE.md:16,18`

> Boundary: … observe and report only, never change quota state. — `PROVINCE.md:45`
> Boundary: … never enable or tune a killer. — `PROVINCE.md:53`
> Kernel-visible mechanism observations do not transfer quota configuration,
> cause or reclamation authority: tsukuroi/operator own configuration/diagnosis…
> — `PROVINCE.md:228-230`

> | tsukuroi | Owns host OS, package, systemd-unit, driver, firmware, and boot diagnosis. …
> — `PROVINCE.md:66`

QUALITY also bites on the entry's form: "the throttle-then-kill shape … is the
manual's recommendation, and … what a working engineer's write-up calls safe"
(`:31-33`) is an opinion/advice claim and must be marked as such, not presented as
mori measurement:

> 1. Every claim falsifiable or marked opinion. — `corpus/QUALITY.md:3`

and the entry's opening runner fact —

> The runner sets two properties on its scope — `MemoryMax=` at the `--mem` value
> and `MemorySwapMax=0` — and no third.
> — `cap-control-wording-r52.md:13-14`

— has **no source row**: its sources are the systemd manual (S602) and a tier-C
article (S604), neither of which is the runner. That is #2 ("Every claim carries a
source: a measured anchor …", `corpus/QUALITY.md:4`).

**Flip condition:** either (i) recast as a **reading rule for mori's own row** — what
a nonzero `high`/`max` counter in `memory.events` means versus `oom_kill`
(throttle/reclaim vs kill), quoted from the manual with a locator and grounded on
the increment site, with no "add `MemoryHigh=`" advice; **or** (ii) the owner
(kumitate/operator) changes the runner, and an entry records only the observed
post-change counter shape as fleet evidence, routed to kumitate (`PROVINCE.md:18`),
not absorbed as mori knowledge.

### 2.3 The refusals must be recorded, not just decided

> 5. A rejection is kept, not silently dropped. — `corpus/QUALITY.md:7`

The round's own `ScribeLesson` item requires ">= 1 admit and >= 1 reject … each with
reason and flip condition"; that satisfies #5 only if the Gate text is actually
landed in `corpus/lessons/round-45.md`. Both rows, if their source rows are kept for
provenance, also owe #60:

> 60. Rejected source rows still need a located quote of at most 25 words in Gate,
> or an explicit unavailable screening-only limitation with the access attempts;
> never imply an unopened body was read.
> — `corpus/QUALITY.md:207-209`

Both entries *have* located quotes ≤ 25 words (the `systemd-run …` line and the
`Memory usage may go above the limit …` sentence), so #60 is satisfiable — it is not
a reason to refuse, just a condition on how the rejection is recorded.

---

## 3. QUALITY criteria the theme would violate as drafted

"As drafted" = the two staged theme entries
`cgroup-surface-two-levels-r49.md` (+ `selftest-cannot-tell-levels-r49.md`), whose
`file://` own-work sources the round already says it will not adopt. Each defect is
also a requirement on the replacement entry `census-cgroup-levels-r45.md`.

| # | Criterion (line) | Defect in the staged draft | Required in the admitted entry |
|---|---|---|---|
| 1 | **2** — measured anchor (`QUALITY.md:4`) | Sources are `file:///…/round12/.deepresearch/notes/r12-census-two-levels.txt` (`:4`); quotes carry **no lane line number**; `recheck` is a presence test (`grep -c 'local_oom_kill=' … -> present`, `:6`). | Cite `tools/mori-census.sh:1862` (row) and `:3252-3254` (selftest) at the entry's revision, plus the read sites `:1705-1712`. |
| 2 | **9** — every pointer resolves at the carrying commit (`QUALITY.md:17`) | No `path:line` pointer exists at all; the `file://` notes are not committed lane evidence. | Each pointer names the lane file, line, and the entry's rev; the digest of the opened source is carried. |
| 3 | **25** — claim admitted at the scope measured (`QUALITY.md:50`) | `cgroup-surface-two-levels-r49.md:17-18` says "`local_oom_kill` comes from the **service's** own `memory.events`". The code prefers `${CGROUP_EVENTS%.events}.events.local` (the **slice's** local file, `:1705,1708-1709`); the service file is only the `elif` fallback (`:1710-1711`). The claim is wrong **and** wider than the code. | State: slice-hierarchical (`oom_kill`), slice-local (`local_oom_kill` when readable), service-hierarchical **only** in the fallback branch. |
| 4 | **34** — class wording names the counted unit and its validation scope (`QUALITY.md:82`) | `local_oom_kill` token does not name the cgroup whose local value it is, and the fallback makes the same token hierarchical. | Emit or document the level+scope per branch (a token or a `path=` that is the file actually read); never rename a hierarchical value "local". |
| 5 | **14** — counter semantics cite the increment site, not only documentation wording (`QUALITY.md:27`) | The theme's support is the kernel doc definition alone. The lane already holds the increment site and its own warning: "The documentation phrase is broader than the increment site: cite the implementation, not the description alone." (`corpus/knowledge/oom-kill-counter-kernel-only-r12.md:12`; S004 `mm/memcontrol.c:4965-4966`). | Cite both: the doc quote for the hierarchical/local distinction **and** the increment-site row the lane already holds. |
| 6 | **3** — observation, inference, unknown separate (`QUALITY.md:5`) | Observation ("nothing in the row says which is which", `:19`) and inference ("The level-pairing clause is therefore not a new requirement", `:19-21`) are blended. "No selftest case can distinguish" is a universal negative needing its enumeration. | Label the inference; enumerate the three pins and the single fixture. |
| 7 | **8** — a cannot-fail claim enumerates the channels tested (`QUALITY.md:15`) | "no selftest case can distinguish the slice's counters from the service's" (`selftest-cannot-tell-levels-r49.md:18`) is a cannot-fail claim. | Enumerate the three env paths and the one file; name what is *not* tested (only one OOM case exists). |
| 8 | **36** — a fixture observation names its case id and pack (`QUALITY.md:91`) | If the entry cites the OOM case (`:3905-3908`), a fixture vector could read as live. | Name the case (`cgroup-oom`) and the fixture builder; never print a fixture vector as live load. |
| 9 | **61** — reader transport is not source bytes (`QUALITY.md:212`) | The kernel quotes must come from the opened bytes, not a rendered projection. | Quote from `.ufo/waves/round-45/assimilation/opened/cgroup-v2.rst.src` and carry its sha256 (`a9433bb0…`) + `wc -w` per quote. |
| 10 | **12** — cumulative counter needs its baseline (`QUALITY.md:23`) | Not in the draft, but the theme makes live level values tempting (my own 539/0 observation). | Any live `memory.events`/`.local` value is printed with boot and cgroup-instance anchor, or is not printed as a claim. |

The sharpest single violation is **#3/#4**: the staged entry's own example sentence
("the service's own `memory.events`") is contradicted by the code it is quoting. The
replacement entry must fix that sentence or it imports the defect into the corpus.

---

## 4. Residuals / unknowns

- `[UNKNOWN]` Whether the service's own `memory.events.local` also differs from its
  hierarchical file on this host — not read; not needed for the fit check.
- `[UNKNOWN]` The cgroup-instance creation time for the live counters I sampled, so
  the 539/0 split has **no baseline** and is not a claim (QUALITY #12).
- `[INFERENCE]` Refusing `who-sets…` and `cap-control…` costs the round nothing it
  claims: the admitted theme entry does not cite either, and `sources-census` rows
  for them are not part of the append set described in `ExecAssimCensus`.
- No PROVINCE line needs to move. If the L1 wants the level-naming rule durable,
  append a round-45 note; do not rewrite `PROVINCE.md:6-10` (the lane's own
  append-only convention at `:274` and `:345`).

## 5. Copy-paste for the L1

`corpus/lessons/round-45.md` → `## Gate` (rejects, reason + flip):

```markdown
- **reject** `corpus/knowledge/who-sets-the-scope-cap-r45.md` — the subject is the
  kumitate/operator runner's `MemoryMax=` configuration (`PROVINCE.md:12,65`), not a
  host record mori reads; `coverage-map: FR1` is a scope overclaim (`QUALITY.md:50`;
  FR1 boundary `PROVINCE.md:44`) and the `recheck` ("-> many") is not a measured
  anchor (`QUALITY.md:4`). Flip: recast as the `oom_memcg=` scope-name observation
  with journal path/boot/timestamp/receipt, claiming only the record's shape; or
  kumitate cedes runner-configuration reading and the operator records it.
- **reject** `corpus/knowledge/cap-control-wording-r52.md` — a throttle-vs-kill
  tuning recommendation for another lane's runner (`PROVINCE.md:16,18,45,53,228-230`;
  `tsukuroi` owns systemd-unit diagnosis at `:66`); it is advice, not a reading, and
  its runner claim (`:13-14`) has no source row (`QUALITY.md:4`). Flip: recast as a
  reading rule for mori's own `high`/`max` vs `oom_kill` counters with a locator and
  the increment site; or record only the owner's post-change counter shape, routed
  to kumitate.
```

`corpus/knowledge/census-cgroup-levels-r45.md` → level/scope sentence (in-province,
narrower than the staged draft):

```markdown
The `cgroup` row reads two levels of the same counter family: `oom_kill` is the
selected slice's **hierarchical** `memory.events` (`tools/mori-census.sh:1690`),
while `local_oom_kill` is the slice's **non-hierarchical** `memory.events.local`
when that file is readable (`:1705,1708-1709`) and the **service's hierarchical**
`memory.events` only in the fallback branch (`:1710-1711`). The row names the
counter but not the level+scope pair; in the fallback branch the `local_` token is
not local. Read-only: no `/proc`, `/sys` or cgroup write is made.
```

Optional PROVINCE append (only if the L1 wants it durable):

```markdown
## Round-45 appended scope note (2026-10-25)

- **Core wording, level-naming (no scope expansion):** the `SURFACE cgroup` row's
  memory-event counters are read hierarchically (`memory.events`) and locally
  (`memory.events.local`); the row states which level+scope each value came from.
  The selftest pins three distinct fixture files to the three env paths. Read-only;
  no remediation, no configuration change, no `PROVINCE.md:6-10` rewrite.
```

## Commands run (rc in place)

```
git -C …/mori-shokunin rev-parse HEAD            -> 3ad8faaa637ae466c61f9427fea1c208bf49ea82 (0)
grep -E '^cgroup2 ' /proc/mounts                  -> cgroup2 … memory_recursiveprot,memory_hugetlb_accounting (0; no memory_localevents)
grep -n "MORI_CGROUP_…EVENTS\|cgroup/memory.events" tools/mori-census.sh (0)
grep -n … tools/mori-silence-cases.sh             (0; pins at :518-520)
sed -n '1703,1714p;1862p;3250,3256p;3896,3916p' tools/mori-census.sh (0)
grep -n "^2\. Every claim\|^9\. Every path\|^14\.\|^25\.\|^34\.\|^36\.\|^60\.\|^61\." corpus/QUALITY.md (0)
for f in slice/memory.events slice/memory.events.local user@1000.service/memory.events; do … done  (0; 539 / 0 / 539, no baseline)
```

No package or tool install was performed (pacman paused host-wide; nothing needed).

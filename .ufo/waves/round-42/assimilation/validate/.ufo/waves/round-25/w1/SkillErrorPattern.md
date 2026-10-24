# SkillErrorPattern — round 25, claim C2 (SKILL.md error-pattern block for the harness job-cap refusal)

Seat: `MoriR25.SkillErrorPattern` (scribe). Leaf seat: no subagents, no background jobs.
Surface: `/home/vgpnk/Projects/shokunin/mori-shokunin/SKILL.md`. Claim C2
(`.ufo/waves/round-25/contract.md:38-92`).

**This seat produced no product edit.** `SKILL.md` is untouched (see §6). The assignment is
"draft … one SKILL.md error-pattern block … in your report only", so the block below is a
**proposal for the L1 to paste**, written to match the file's existing idiom. Everything in it is
cited; nothing is asserted without a pointer.

---

## 1. What the observed text is, and where it comes from

The observed text is upstream's own fixed string, not a fleet message:

```
Background job limit reached (100). Wait for running jobs to finish or cancel one.
```

* Upstream source, oh-my-pi **v18.12.6** = commit `45c35e40c46166dc726ccc52f5d27f40f2449f99`:
  `packages/coding-agent/src/async/job-manager.ts:371-373` throws it from `register()` —
  `` throw new Error(`Background job limit reached (${maxRunningJobs}). Wait for running jobs to finish or cancel one.`) ``
  (the source string occurs once; `grep -c 'limit reached' job-manager.ts` → 1).
* Installed binary `~/.local/bin/omp` (256,702,432 bytes, sha256
  `85d9daf3a05fc76e8cd425ae1904eb576af8d21cc85fcf4690742626e07ccfa4`) carries the same template at
  **byte 160033342** (`throw new Error(\`Background job limit reached (${o}). …\`)`) and the split
  string-table fragments at byte 95794256.
* A lane reading a transcript usually sees it **wrapped**: the task tool composes
  `Failed to start background task job{s}: <agentId>: <message>`
  (`packages/coding-agent/src/task/index.ts:1220-1230`, upstream tag). The fixed inner sentence is
  upstream's; the wrapper is the tool's.

**The number in the text is the effective cap, not the operator's setting.** The effective cap of a
shipped session is `max(1, floor(min(100, base)))`:

| Piece | Upstream | Binary |
|---|---|---|
| clamp `Math.min(100, cfgAsyncMaxJobs.get(settings))` at the one shipped manager construction | `packages/coding-agent/src/sdk.ts:2282-2286` | byte 164406766 (`maxRunningJobs: () => Math.min(100, XPe.get(R))`) |
| getter `Math.max(1, Math.floor(value ?? DEFAULT_MAX_RUNNING_JOBS))` | `job-manager.ts:331-335` | byte 160032730 (`get #R()`) |
| module fallback `const DEFAULT_MAX_RUNNING_JOBS = 15;` (unreachable in a shipped session — the shipped construction always passes a function) | `job-manager.ts:43` | byte 160031518 (`var v = 15;`) |
| setting `async.maxJobs`, `type: "number"`, `default: 100` | `packages/coding-agent/src/tools/settings.ts:941-946`; `docs/settings.md:623` | byte 155231590 |

On this host the operator's OMP settings file carries `async:` / `  maxJobs: 200`, so the effective
cap is **100** and the text reads `(100)` — the configured 200 is clamped before the manager sees it.
The lane's own committed live run agrees: `.ufo/waves/round-25/evidence/runway-live-run.json` →
`configured 200`, `clamp {found, 100, sites 1}`, `effective 100`, `verdict RUNWAY_CLAMPED`, exit 1.

**What counts against the cap** (the count rule has no type filter):

* `job-manager.ts:343` and `:367` — `if (job.status === "running" && !job.queued) activeCount++;`
  over **every** job the manager holds; `AsyncJobType = "bash" | "task" | "eval"` (`job-manager.ts:48`).
  So a background **shell** job draws on the same runway as a subagent seat.
* A **queued** (parked) task job does not hold a slot until it starts: it registers `queued: true`
  (`task/index.ts:1565`) and `markRunning()` clears the flag when it actually begins
  (`task/index.ts:1490`; `job-manager.ts:416-417`).
* A bash job registers **without** the queued flag (`tools/bash.ts:882`), so it counts from
  registration. The manager is the root session's and is inherited by children and nested
  subagents (`sdk.ts:2315`, `sdk.ts:2521-2528`), so the population is the whole session tree.

**Not every call errors at the cap.** The bash and eval auto-background branches check `atCapacity`
first and **fall through to direct foreground execution** (`tools/bash.ts:1220-1229`,
`tools/eval.ts:536`). The paths that actually raise the error are the ones that register without a
pre-check: the task spawn path (`task/index.ts:1407`, caught at `:1210-1219`) and an explicit
`async: true` bash call (`tools/bash.ts:1188-1192` → `:882`).

---

## 2. Independent re-derivation of the refusal census (read-only, no private content reported)

The sibling seat `MoriR25.RefusalCensus` counted the same surface with its own script. To avoid
restating its numbers I re-derived the census with a separate one-pass scan over `~/.omp` at
**2026-10-22T10:50:22Z**, matching the strict form `Background job limit reached \((\d+)\)` and
**excluding the three round-25 seat transcripts that quote the string in their own prose**
(`MoriR25.SkillErrorPattern`, `MoriR25.RefusalCensus`, `MoriR25.SrcRejections`):

```
files_with_hits 544   occurrences 20928   bytes_read 4505314531
caps {'100': 20928}
```

**Every occurrence on this host carries the number 100.** The only non-100 occurrences anywhere
under `~/.omp` are in those three round-25 seat transcripts, where a seat wrote the literal string
`(1)` / `(15)` while reasoning about the number — self-contamination, not a harness emission. That
matches the sibling's tiered result (its `harness` and `toolresult` tiers are 100-only; its single
`15` sits in the `prose` tier).

Per the round-25 bounds, only counts, timestamps and the fixed error text are reported here; no
transcript message content is reproduced.

---

## 3. The proposed SKILL.md block (paste-ready)

Placement: a new subsection under the existing round sections, i.e. after the
`## Round24 — one-shot system pressure read (C2)` section that ends at `SKILL.md:641`, following the
same `Condition | Report as | Never infer` idiom the round-24 decision table uses (`SKILL.md:621-641`).
Proposed text:

```markdown
### Harness background-job cap refusal (r25)

The fixed text `Background job limit reached (100). Wait for running jobs to finish or cancel one.`
is upstream's own message from the async job manager's registration path
(`job-manager.ts:371-373` at v18.12.6; installed `omp` byte 160033342), wrapped by the task tool as
`Failed to start background task job{s}: <agentId>: <message>` (`task/index.ts:1220-1230`).

| Condition | Report as | Never infer |
|---|---|---|
| the fixed sentence appears in a transcript or tool result | a harness **registration refusal** at the session's running-job cap; the number is the **effective** cap at that instant, `max(1, floor(min(100, async.maxJobs)))` — the clamp is compiled into the binary (`sdk.ts:2284`, byte 164406766), so `(100)` is the clamp, not the operator's configured value | that the operator configured 100 (this host's the operator's OMP settings file says 200 and the clamp reduces it to 100); that the cap is still 100 now — it is re-read at every check (`job-manager.ts:331-335`); that the refused work ran — `register()` throws before the job exists (`task/index.ts:1210-1219`, `results: []` at `:1229`) |
| a bash or eval call was made while the cap was full | nothing — the auto-background branch checks `atCapacity` first and runs in the foreground instead (`tools/bash.ts:1220-1229`, `tools/eval.ts:536`) | that the cap was not reached; that the call was backgrounded |
| a `task` spawn or an explicit `async: true` bash was refused | one refused registration; a batch can partially start, so refusals and starts coexist in one result | that the wave is dead — a refusal creates no job; that the count was this wave's own seats: the population is every **running, non-queued** job in the session tree — bash, task and eval alike (`job-manager.ts:343,367`, `:48`; `tools/bash.ts:882`) — and a parked (queued) task job counts only after `markRunning()` (`task/index.ts:1565,1490`) |
| mori must state the cap | `python3 -I -B tools/mori-job-runway.py` → one JSON object (`schema: mori-job-runway-v1`) with `configured {state,value}`, `clamp {state,value,sites}`, `setting_default {state,value,sites}`, `effective`, and `verdict` ∈ `RUNWAY_CLAMPED` (exit 1) / `RUNWAY_AS_CONFIGURED` (exit 0) / `RUNWAY_DEFAULT` (exit 0) / `RUNWAY_UNKNOWN` (exit 2) | that the session was at capacity — the tool reports the **cap**, never a running-job count, and the live count is not readable from outside the session (`contract.md:83-84`); that an absent or unreadable clamp means "no clamp" (it is `RUNWAY_UNKNOWN`); that the file's `async.maxJobs` is the value the session resolved — the runtime settings stack has project and overlay layers the tool does not read (`corpus/knowledge/harness-job-capacity-r25.md` F13) |

**mori never acts on this text.** It does not edit the operator's OMP settings file or any other OMP
setting, it does not cancel or kill a running job, and it does not split, shrink or re-dispatch a
wave. mori is detection and report only (`SKILL.md:9`, `SKILL.md:139-147`, `PROVINCE.md:12-18`).
Dispatch and wave shape are kumitate's (`PROVINCE.md:65`); writes under `~/.omp` are the operator's
(`kama-shokunin/PROVINCE.md:45-47`); the harness-side remedy the message itself names — let running
jobs finish, or cancel one — is the operator's, and mori reports the refusal as evidence, not as a
work order.

**A refusal is not repairable by raising the setting.** `async.maxJobs` above 100 cannot lift this
cap: the clamp is compiled into the binary (`sdk.ts:2284`), so a configured 200 already means an
effective 100. Only the operator can change the installed binary or the harness build.
```

### 3a. Compact alternative — one row for the existing `## Error patterns` table

`SKILL.md:23-45` holds a two-column `| Observation | Reading |` table. If the L1 prefers the block
to live there instead of as its own subsection, this single row carries the same content in the
table's own idiom:

```markdown
| `Background job limit reached (100). Wait for running jobs to finish or cancel one.` | upstream's fixed refusal from the async job manager's registration path, not a fleet message: the session's running-job cap was full at that instant and the number is the **effective** cap `max(1, floor(min(100, async.maxJobs)))` — compiled clamp, so `(100)` is the clamp even where the operator configured 200; the population is every running, non-queued job in the session tree (bash, task and eval alike), so a refusal says nothing about this wave's own seats, and a refused seat never ran. Read the cap with `python3 -I -B tools/mori-job-runway.py` (`RUNWAY_CLAMPED` / `RUNWAY_AS_CONFIGURED` / `RUNWAY_DEFAULT` / `RUNWAY_UNKNOWN`); it reports a cap, never a running-job count. mori edits no setting, cancels no job and re-dispatches no wave — writes under `~/.omp` are the operator's (`kama-shokunin/PROVINCE.md:45-47`), wave shape is kumitate's (`PROVINCE.md:65`) |
```

I recommend the **subsection** (3) over the table row (3a): the round-24 precedent put its reading
table in its own section (`SKILL.md:611-641`), and this row carries four distinct readings plus a
never-do list, which does not fit one table cell without losing the "Never infer" column.

---

## 4. Remediation ownership — the brief's routing vs. what `PROVINCE.md` Adjacent actually says

The item brief asks for "operator; tsukuroi for host config — check `PROVINCE.md` Adjacent". I checked
it and report the conflict verbatim for the canonical judge.

**What `PROVINCE.md` Adjacent actually says** (`mori-shokunin/PROVINCE.md:59-70`):

* row `kumitate` (`:65`) — "Owns OMP task/hub orchestration and wave plan/run/record/collect
  semantics; mori passively grades `.ufo/waves/*` filesystem settlement state."
* row `tsukuroi` (`:66`) — "Owns host OS, package, systemd-unit, driver, firmware, and boot
  diagnosis. It was the only sibling hit in R12Connector's corpus search for `systemd-oomd`,
  `earlyoom`, `memory.events`, and `MESSAGE_ID`; this is adjacent host diagnosis, not contested
  fleet ownership."

**Conflict.** The file at issue is the operator's OMP settings file — OMP **harness** configuration, which
is none of tsukuroi's declared surfaces (host OS, packages, systemd units, drivers, firmware,
boot). The harness's own contract — task batch, agent hub, agent discovery — is kumitate's
(`kumitate-shokunin/PROVINCE.md:19`), and kumitate already treats that same file as the global OMP
config authority (`kumitate-shokunin/SKILL.md:288`). Write ownership under `~/.omp` is the
**operator's** (`kama-shokunin/PROVINCE.md:45-47`: "kama never writes to `~/.config`, `~/.omp`, or
systemd units. Those are operator-owned"). The tiering matches mori's own routing table
(`SKILL.md:342-356`): Tier-1 diagnosis by a read-only domain specialist, Tier-2 actuation by the
operator for host mutations.

**So the routing this seat writes into the block is:**

| Layer | Owner | Basis |
|---|---|---|
| Tier 1 — read the cap, say what the refusal means | `mori` (`tools/mori-job-runway.py`) | this lane's contract C2 (`contract.md:38-92`) |
| Tier 1 — diagnose the harness contract (task batch, agent hub, how a session spawns seats) | `kumitate` | `PROVINCE.md:65`; `kumitate-shokunin/PROVINCE.md:19` |
| Tier 1 — host substrate, **only** if the remedy turns out to be host-side (a systemd unit, a cgroup limit, boot) | `tsukuroi` | `PROVINCE.md:66` — this cap is **not** host substrate, so tsukuroi is not on the path for `async.maxJobs` itself |
| Tier 2 — change the setting or the installed binary; cancel a running job | `operator` | `kama-shokunin/PROVINCE.md:45-47`; `SKILL.md:350-354` |
| Tier 2 — change wave shape / re-dispatch | `kumitate` (automated orchestration actions) | `SKILL.md:350-354`; `PROVINCE.md:65` |

**Two [INFERENCE]-marked consequences for the L1 to rule on:**

1. **[INFERENCE]** No config edit can lift a `(100)` refusal on omp 18.12.6 — the clamp is compiled
   in (`sdk.ts:2284`). The only operator levers are the installed binary/harness build, or the
   harness-side remedy the message names (finish or cancel running jobs). If the L1's intent was
   "the operator can raise `async.maxJobs`", that intent is void above 100.
2. **[INFERENCE]** tsukuroi stays off the path for this finding unless the operator's chosen remedy
   is host-side. Routing it to tsukuroi "for host config" would place the OMP harness settings file
   under a lane that declares only host substrate — the exact "absorb another lane's domain"
   failure `PROVINCE.md:18` forbids.

---

## 5. Facts the block rests on — every one cited

| # | Fact used in the block | Pointer |
|---|---|---|
| F1 | the fixed refusal string, thrown by `register()` | `job-manager.ts:371-373` @ `45c35e40c46166dc726ccc52f5d27f40f2449f99`; binary byte 160033342 |
| F2 | the number is the effective cap = `max(1, floor(min(100, base)))` | `sdk.ts:2282-2286`; `job-manager.ts:331-335`; binary bytes 164406766 / 160032730 |
| F3 | the count rule: running and not queued, no type filter | `job-manager.ts:343`, `:367`, type union `:48` |
| F4 | bash jobs count from registration; task jobs count only after `markRunning()` | `tools/bash.ts:882`; `task/index.ts:1565`, `:1490`; `job-manager.ts:416-417` |
| F5 | the manager is the root's and children inherit it | `sdk.ts:2315`, `:2521-2528` |
| F6 | bash/eval degrade to foreground at the cap; task spawn and explicit `async: true` bash do not | `tools/bash.ts:1220-1229`, `tools/eval.ts:536`; `task/index.ts:1407`; `tools/bash.ts:1188-1192` |
| F7 | the task tool's wrapper text | `task/index.ts:1220-1230`; upstream prose on the shared population and the "default and maximum 100" ceiling at `docs/tools/eval.md:258` |
| F8 | the setting default is 100 and the docs state no maximum | `tools/settings.ts:941-946`; `docs/settings.md:623` |
| F9 | the tool's verdicts, exit codes and JSON shape | `contract.md:68-75`; `tools/mori-job-runway.py:105-108` (`RUNWAY_UNKNOWN`/`RUNWAY_CLAMPED`/`RUNWAY_AS_CONFIGURED`/`RUNWAY_DEFAULT`) |
| F10 | the tool reports a cap, never a running-job count | `contract.md:83-84`; `corpus/knowledge/harness-job-capacity-r25.md` (Limits, F13) |
| F11 | this host: configured 200 → effective 100, verdict `RUNWAY_CLAMPED`, exit 1 | `.ufo/waves/round-25/evidence/runway-live-run.json`; re-run by this seat, same JSON, exit 1 |
| F12 | every refusal on this host carries 100 | this seat's scan, §2; sibling `RefusalCensus.md` tiers `harness` / `harness_error` |
| F13 | mori never remediates; dispatch is kumitate's; `~/.omp` writes are the operator's | `SKILL.md:9`, `:139-147`, `:342-356`; `PROVINCE.md:12-18`, `:65`; `kama-shokunin/PROVINCE.md:45-47` |

Lane-internal sources already carrying these facts, which the block can lean on instead of
re-deriving: `corpus/knowledge/harness-job-capacity-r25.md` (F1–F13 and its Decision table) and
`corpus/SOURCES.md` rows **S098** (job-manager), **S099** (sdk clamp), **S100** (settings schema),
**S101** (settings reference), **S102** (installed binary), **S103** (eval docs), **S112** (bash.ts),
**S113** (eval.ts).

---

## 6. Touched surfaces, gates, out-of-scope

**Files written by this seat:** exactly one — this report,
`.ufo/waves/round-25/w1/SkillErrorPattern.md`. `SKILL.md` was **not** edited: the bounds say a seat
writes only its own report file, and the item says to draft the block "in your report only". The
L1 pastes §3 (or §3a) if the block is admitted.

**Gates exercised by this seat (read-only):**

| Command | Result |
|---|---|
| `python3 -I -B tools/mori-job-runway.py --selftest` | `MORI_JOB_RUNWAY_SELFTEST: PASS 21/21`, exit 0 |
| `python3 -I -B tools/mori-job-runway.py` | `RUNWAY_CLAMPED`, `effective 100`, exit 1 (matches the committed evidence file) |
| `python3 -I -B tools/mori-job-runway.py --config /tmp/cfg_ok.yml` (`async:` / `maxJobs: 50`) | `RUNWAY_AS_CONFIGURED`, exit 0 |
| `python3 -I -B tools/mori-job-runway.py --config /tmp/nope.yml` (absent) | `RUNWAY_DEFAULT`, exit 0 |
| `python3 -I -B tools/mori-job-runway.py --config /tmp/cfg_ok.yml --binary /tmp/notabin` | `RUNWAY_UNKNOWN`, exit 2 |
| refusal census over `~/.omp` (read-only, strict regex) | 20,928 occurrences across 544 files, all `(100)` (§2) |
| byte reads of `~/.local/bin/omp` (`re`/`mmap` over the file; no execution) | clamp ×1 @164406766, throw ×1 @160033342, setting id ×1 @155231590 |

**Out of scope / not done by this seat:**

* No edit to `SKILL.md`, `PROVINCE.md`, the knowledge entry, `SOURCES.md` or the tool.
* No lane commit, no jj command anywhere, no `git` write of any kind; the only git reads were
  `git log --oneline`, `git status --short`, `git diff --stat` inside the lane repo.
* `omp` was never run; the operator's OMP settings file, `~/.omp/agent/mcp.json` and OMP settings were
  read only, never edited.
* No tool installed or upgraded (no `pacman`, `uv tool`, `cargo` or `npm` transaction). Interpreter:
  system `python3`; upstream bytes fetched over HTTPS with `curl` from
  `raw.githubusercontent.com` at the pinned commit `45c35e40c46166dc726ccc52f5d27f40f2449f99`
  (fetched to `/tmp`, read-only use).

---

## 7. Findings

**F1 — the brief's remediation routing does not match `PROVINCE.md` Adjacent (needs an L1 ruling).**
"operator; tsukuroi for host config" would put the OMP harness settings file under a lane that
declares host OS/packages/systemd/drivers/firmware/boot only (`PROVINCE.md:66`). The harness
contract is kumitate's (`PROVINCE.md:65`, `kumitate-shokunin/PROVINCE.md:19`) and `~/.omp` writes are
the operator's (`kama-shokunin/PROVINCE.md:45-47`). The block above routes accordingly and keeps
tsukuroi on the path only for a host-side remedy. **Reported, not silently corrected.**

**F2 — no configuration edit can lift a `(100)` refusal on this binary.** The clamp
`Math.min(100, cfgAsyncMaxJobs.get(settings))` is compiled in (`sdk.ts:2284`, byte 164406766), so the
configured 200 is already reduced to 100 and any larger configured value would be too. A block that
implied "raise `async.maxJobs` to fix the refusal" would be wrong on this host. [INFERENCE] applied to
the two cited sources; the sources themselves are direct.

**F3 — the same cap has two observable behaviours, and the block must not conflate them.** A bash or
eval call at the cap runs in the foreground with no error (`tools/bash.ts:1220-1229`,
`tools/eval.ts:536`); only unguarded registrations raise it. So "no refusal seen" does **not** mean
"the cap was not reached", and "a refusal seen" does not mean every background call failed.

**F4 — the number in the text is a cap, not a count.** `(100)` is the effective cap; the running-job
count is not in the message and is not readable from outside the session
(`contract.md:83-84`). The block's wording keeps "the cap was full" and "100 jobs were running"
apart, and the tool's `effective` field is labelled as a cap.

**F5 — a refusal creates no seat and consumes no runway.** `register()` throws before the job
exists; the task tool catches it per seat and returns `results: []`
(`task/index.ts:1210-1219`, `results: []` at `:1229`). A refusal is therefore *not* evidence that a seat ran, and *not*
evidence that a seat died — the two must not be collapsed in the error-pattern row.

**F6 — self-contamination is real in this round's own transcripts and must be excluded from any
census.** Three round-25 seat transcripts contain the literal `(1)` and `(15)` strings because seats
quoted the refusal while reasoning about its number. Excluding them, all 20,928 occurrences under
`~/.omp` carry 100. Any future census should exclude seat transcripts by seat id before quoting a
number distribution.

**F7 — the block should cite the lane's own knowledge entry, not re-derive it.**
`corpus/knowledge/harness-job-capacity-r25.md` already carries F1–F13, its Decision table and its
Limits; `corpus/SOURCES.md` carries S098–S103 and S112–S113. The block above cites upstream for the
mechanism and the lane sources for the host reading; if the L1 admits it, adding one pointer line
(`corpus/knowledge/harness-job-capacity-r25.md`) keeps the SKILL.md from becoming a second source of
truth for the cap.

**F8 — an observed gap in the sibling census worth noting.** `RefusalCensus.md` scopes itself to
`~/.omp/agent/sessions` with a file-mtime window; this seat's scan covered the whole of `~/.omp`
(including session `.log` and `.md` artifacts) and found the same 100-only distribution with a
larger occurrence count (20,928 vs the sibling's 20,323 tier-`all` figure at its earlier instant).
The difference is scope and instant, not disagreement; the sibling's own tiering is the more
conservative and better-cited instrument for the harness-tier claim.

---

## 8. Artifacts

| Artifact | Path |
|---|---|
| this report | `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-25/w1/SkillErrorPattern.md` |
| proposed SKILL.md block (paste-ready) | §3 of this report (subsection) and §3a (single error-patterns-table row) |
| lane tool the block names | `tools/mori-job-runway.py` (committed; `MORI_JOB_RUNWAY_SELFTEST: PASS 21/21`) |
| committed live-run evidence | `.ufo/waves/round-25/evidence/runway-live-run.json`, `.ufo/waves/round-25/evidence/runway-live-run.meta` |
| knowledge entry the block leans on | `corpus/knowledge/harness-job-capacity-r25.md` |
| source rows | `corpus/SOURCES.md` S098–S103, S112, S113 |
| upstream refs (tag `v18.12.6` = `45c35e40c46166dc726ccc52f5d27f40f2449f99`) | `packages/coding-agent/src/async/job-manager.ts`, `packages/coding-agent/src/sdk.ts`, `packages/coding-agent/src/task/index.ts`, `packages/coding-agent/src/tools/{bash,eval,settings}.ts`, `docs/settings.md`, `docs/tools/eval.md` |
| installed binary (read as bytes only) | `~/.local/bin/omp`, sha256 `85d9daf3a05fc76e8cd425ae1904eb576af8d21cc85fcf4690742626e07ccfa4` |

Report: `.ufo/waves/round-25/w1/SkillErrorPattern.md`

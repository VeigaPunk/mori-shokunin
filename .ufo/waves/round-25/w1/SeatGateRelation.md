# SeatGateRelation — what the hyaku seat gate enforces, and why a grant still gets refused

Seat: `MoriR25.SeatGateRelation` (wave 1, round 25, leaf scout). Question: the current cap of
`scripts/hyaku/wave-slot.sh` (85?), where it comes from, what it counts, and why a granted wave can
still be refused by the harness ceiling of 100. Read-only: every command below reads files or git
objects; nothing in the fleet, the gate state dir, `config.yml`, or the omp binary was written.
No tools installed or upgraded.

Confidence markers: **[observed]** = command output or file bytes below; **[inference]** = labelled
reasoning, not a run.

---

## 1. Answer in brief

- The gate enforces **85 seats**, read from the state file `~/.local/state/shokunin-hyaku/wave-cap`
  (3 bytes, `85\n`, mtime `2026-10-22 05:30:46 -03:00` = `08:30:46Z`). **[observed]**
- Precedence: `HYAKU_WAVE_CAP` env → `$STATE/wave-cap` → **compiled-in default 200**
  (`scripts/hyaku/wave-slot.sh:30-32`, `:33-38`, `:40`). **[observed]**
- It counts `live agents (JSONL tails under one session tree) + ledger reservations granted in the
  last 120 s + the requested seats`, and grants when that sum is `<=` cap **and** MemAvailable is at
  least 6144 MB (`wave-slot.sh:20-21`, `:48-53`, `:61-67`, `:79-80`). **[observed]**
- The harness ceiling is **100 jobs per top-level session**, compiled into the binary as
  `maxRunningJobs: () => Math.min(100, XPe.get(R))`, so `async.maxJobs: 200` in
  `~/.omp/agent/config.yml:245` cannot raise it. **[observed]**
- A grant is a *forecast about agents*; admission is a *hard count of running, non-queued jobs* in
  the same process — including backgrounded `bash` jobs and async `eval` jobs, which create no
  transcript seat at all. That gap is why grants were refused in full on this host at 08:26Z
  (`PHASE3.md:180`). **[observed + mechanism from binary]**
- Ledger for 2026-10-22: **4 grants, max seats 41**, seats sum 151, four distinct lanes. **[observed]**

---

## 2. The gate as landed (`scripts/hyaku/wave-slot.sh`)

State and knobs:

| Line | Content |
|---|---|
| `:19` | `STATE=${HYAKU_STATE:-$HOME/.local/state/shokunin-hyaku}` |
| `:20` | `PENDING=${HYAKU_WAVE_PENDING:-120}` (reservation window, seconds) |
| `:21` | `MIN_AVAIL_MB=${HYAKU_WAVE_MIN_AVAIL_MB:-6144}` |
| `:22` | `LEDGER="$STATE/wave-slots"`, `LOCK="$STATE/wave-slots.lock"` |

Cap selection, `configured_cap()` (`:28-46`):

- `:30-32` — `HYAKU_WAVE_CAP` set → source `environment`.
- `:33-38` — else `$STATE/wave-cap` must contain exactly one line, source `state`.
- `:40` — else `value=200`, source `default`.
- `CAP_SOURCE` is carried into `status` and the grant/timeout lines only through `status`
  (`:98-102`); the grant line prints `cap=$CAP` without the source (`:83`).

What the machine currently has **[observed]**:

```
$ od -An -c ~/.local/state/shokunin-hyaku/wave-cap
   8   5  \n
$ stat -c 'mtime=%y' ~/.local/state/shokunin-hyaku/wave-cap
mtime=2026-10-22 05:30:46.218375402 -0300
```

`HYAKU_WAVE_CAP` is read only by `wave-slot.sh:30-31`; the only other reference in the fleet is
`wave-slot-selftest.sh:187`, which sets it in a temporary env. No launcher exports it
(`grep -rn HYAKU_WAVE_CAP /home/vgpnk/Projects/shokunin/scripts` → the two lines above). So absent an
export in the L1's own shell — not observable from this seat — **the gate uses 85**. **[observed;
the L1 shell env is the residual unknown]**

Provenance of 85 **[observed]**: `.ufo/waves/hyaku/PHASE3.md:182` (checkpoint `2026-10-22T08:30:00Z`)
records the change 200 → 85 and the reason: "wave-live counts agents only, while the harness limit
also counts background shell jobs (L1 gate waits, timers); 85 leaves room so that a grant is admitted
and Main's closures can still spawn. Same threshold as `await-capacity.sh`'s default." That default is
visible in `scripts/hyaku/await-capacity.sh:8` (`thr=${2:-85}`).

History is *not* retained: `wave-cap` is a single line, and `events.log` records only one cap event,
`events.log:360` (`2026-10-21T12:40:47-03:00 operator-policy wave-cap 240->320`). The 320 → 200 step
and the 200 → 85 step exist only as the rendered `status` rows `PHASE3.md:128` (`cap=200 (state)`,
08:02:30Z) and `PHASE3.md:188` (`cap=85 (state)`, 08:33Z). **[observed]**

Latent hazard **[inference]**: the built-in default is still 200 (`:40`). If `wave-cap` is ever
removed, the gate silently reverts to a target twice the harness ceiling — the exact configuration
that produced the 08:26Z refusals.

Grant arithmetic, `acquire` (`:71-89`):

| Line | Meaning |
|---|---|
| `:76` | exclusive `flock` on `$LOCK` |
| `:77` | `configured_cap` re-read **every** loop iteration |
| `:78` | `a=$(live)` — live agent estimate (section 3) |
| `:79` | `used=$((a + p + seats))`, `p=$(pending)`, `m=$(mem_avail_mb)` |
| `:80` | grant iff `fits_cap "$used" "$CAP"` **and** `m >= MIN_AVAIL_MB` |
| `:81` | append `<epoch> <seats> <lane> <wave>` to `$LEDGER` |
| `:83` | print `granted lane=… wave=… seats=… live=… pending=… cap=…`, exit 0 |
| `:87-88` | on deadline: `timeout … mem_avail_mb=… min=…`, exit 3; else `sleep 20` |

`fits_cap` (`:48-53`) compares decimal strings by length then lexicographically, which is `used <= cap`
for nonnegative integers and avoids shell integer overflow; equality **is** a grant. **[observed]**

`pending` (`:67`) sums seats of ledger rows whose epoch is `>= now-120`. Rows otherwise never expire
from the file: only `release` deletes them (`:94`, an awk filter + rewrite). Nothing logs releases —
`grep -n 'grant\|release\|wave-slot' events.log` returns no gate lines at all. So the ledger is
"grant rows not yet released", not a complete grant history. **[observed]**

`session_dir` (`:55-59`) resolves `$HYAKU_SESSION_DIR`, else the path in `$STATE/live-session-dir`,
else dies. Current contents **[observed]**:

```
$ cat ~/.local/state/shokunin-hyaku/live-session-dir
/home/vgpnk/.omp/agent/sessions/-Projects-shokunin/2026-10-22T07-55-56-355Z_01a1629c-0c43-7754-9701-07270d148a3a
```

That is Main's top-level session. The parent `-Projects-shokunin/` holds six top-level sessions; only
this one is walked. The other session dated today (`2026-10-22T07-36-10-599Z_…`) has a JSONL last
written `04:54:46 -03:00` and 2 nested JSONLs — dormant now, but structurally outside the walk. **[observed]**

---

## 3. What `live()` actually measures (`scripts/hyaku/wave-live.py`)

`live()` (`wave-slot.sh:61-65`) = `wave-live.py` output + `MANUAL_RESERVE` (default 0, `:20`). The
helper emits exactly one decimal integer (`wave-live.py:180-193`) and describes itself as "a snapshot
estimate, not a scheduler/process liveness oracle" (`:19`).

Rules that matter for the seat number **[observed]**:

- Bounded read: at most 256 KiB + 1 boundary byte per JSONL (`:28`, `:138-139`); `.md` bodies are
  never read (`:7`); symlinked directories are not followed (`:33-47`), files opened `O_NOFOLLOW`
  (`:24-25`).
- Verdict is taken from the JSONL tail in **reverse append order** (`:82-129`):
  - `session_exit` closes the run (`:97`); `custom`/`session_exit` closes it (`:103`);
  - assistant `stopReason` `error` or `aborted` closes it (`:115-118`);
  - assistant `stopReason` `stop` closes it **only** if a nonempty regular `.md` exists strictly
    newer than the message (`:119`, `:66-80`);
  - `custom`/`tool_execution_start` opens it (`:105`); any `custom_message` opens it (`:121`);
  - bookkeeping types `model_usage, credential_pin, session, model_change, thinking_level_change,
    compaction, branch_summary, session_info, label` are skipped (`:123-124`);
  - anything else, including malformed JSON, counts **active** (fail-closed).
- A file that is appended to during inspection is counted active regardless of verdict (`:147-153`).
- Recursive walk: 30 JSONLs at the session root, 544 in nested subagent directories, 572 total at
  first read — each *active* one is one seat (`:157-178`). Unreadable subtrees count 1 rather than 0
  (`:174`).

Readings taken today **[observed]**:

```
$ python3 scripts/hyaku/wave-live.py "$(cat …/live-session-dir)"
73          # ts=1792663159 = 2026-10-22T06:59:19-03:00
63          # ts=1792663310 = 2026-10-22T07:01:50-03:00
```

Thus the gate's notion of "live" is **agent transcripts only**. It cannot see: backgrounded `bash`
jobs, async `eval` jobs, foreground tool work, subagent-internal jobs, jobs of other top-level
sessions, and the harness's own running-job count. **[observed from code; the exclusions follow from
what is scanned]**

Consequence at the second reading: `used = 63 + 0 + seats`, cap 85 → **22 free seats**. At the first
reading `73 + 34 = 107 > 85` → every wave was refused, which matches the four L1s parked in
`proc://` as "Waiting for seat gate grant" / "Waiting for remaining build seats". **[observed]**

---

## 4. The harness ceiling: 100 jobs per top-level session

Byte reads of the installed binary (`/home/vgpnk/.local/bin/omp`, 256,702,432 bytes, `omp/18.12.6`
per the embedded `18.12.6` version string) **[observed]**:

1. Clamp — exactly one site, at byte offset 164406766:

   ```js
   const Ui = !u.parentTaskPrefix ? new Xm({
     maxRunningJobs: () => Math.min(100, XPe.get(R))
   }) : undefined;
   ```

   Reproduce with:
   `python3 -c "import re;d=open('/home/vgpnk/.local/bin/omp','rb').read();print([m.group(1) for m in re.finditer(rb'maxRunningJobs:\s*\(\)\s*=>\s*Math\.min\(\s*(\d+)\s*,\s*[\w$]+\.get\([\w$]+\)\s*\)', d)])"`
   → `[b'100']`, 1 site.

2. Setting — one site:

   ```js
   var XPe = h({ id: "async.maxJobs", protocolDefault: ["rpc"], type: "number", default: 100 });
   ```

   and the config sets `async.maxJobs: 200` (`~/.omp/agent/config.yml:245`, file mtime
   `2026-10-22 05:01:04 -03:00`). Effective ceiling = `min(100, 200)` = **100**.

3. Enforcement — class `Xm` (`packages/coding-agent/src/async/job-manager.ts` in the bytecode),
   `register()` at offset ~160033359:

   ```js
   let r = 0;
   for (const u of this.#e.values()) if (u.status === "running" && !u.queued) r++;
   const o = this.#R;
   if (r >= o) throw new Error(`Background job limit reached (${o}). Wait for running jobs to finish or cancel one.`);
   ```

   `get #R()` = `Math.max(1, Math.floor(t ?? 15))` — the `15` fallback is not reached here because the
   clamp always supplies a number. `get atCapacity` uses the same predicate.

4. Who registers jobs with that manager **[observed]**:
   - `"task"` — the `task` tool's per-agent runner (`register("task", P, …)` at 164179343, options
     `{ id, agentId, queued: true, … }` at 164183991, `markRunning()` when the run actually starts);
   - `"bash"` — the background-command runner (`register("bash", …)` at 161053249); the tool only
     backgrounds automatically when `!Y.atCapacity` (161061588), so foreground shell work runs inline
     and registers nothing;
   - `"eval"` — async eval (`register("eval", …)` at 163907062 and 164233930); inline eval bypasses the
     manager when the feature flag is off **or** `atCapacity` (164233375).

5. Scope of the counter: one manager per top-level session (`!u.parentTaskPrefix`); a subagent session
   has `asyncJobManager === undefined` and the code paths throw
   `"Async job manager unavailable for this session."` (161060785) / `"agent() needs the session's
   async job manager; unavailable here"` (164034300). So the counter is **session-global**, which the
   fleet record states independently: `PHASE3.md:167` "The job counter is session-global, so seats'
   shell jobs also advance it."

---

## 5. Why a granted wave can still be refused

Mechanism, each piece anchored:

**(a) The gate counts agents; the ceiling counts jobs.** Backgrounded `bash` jobs and async `eval`
jobs occupy slots in `Xm` but write no agent JSONL, so `wave-live.py` scores them zero. L1 seat-gate
wait loops (`wave-slot.sh:88 sleep 20`) and freeze timers are exactly such jobs; `PHASE3.md:182`
names this as the reason 85 was chosen and `PHASE3.md:167` as the reason timers advance the counter.

**(b) 120 s reservation window vs. transcript lag.** A wave's jobs register immediately at the
`task` call, but the transcripts that `live()` scores appear later. The only cover for that gap is
`pending` (`:67`), which forgets a reservation 120 s after its grant. Two waves granted more than
120 s apart are therefore measured against transcripts that may not yet exist. **[observed code;
lag inference]**

**(c) Scope mismatch.** The gate sums one number globally over Main's session tree; the ceiling is
per top-level session/process. Jobs of another session are invisible to `live()` and do not consume
this session's 100 — the gate can neither predict a refusal in a busy sibling session nor account for
one. **[observed from code + session layout]**

**Fleet proof, same host, same day** **[observed]**: `PHASE3.md:180` (checkpoint 08:26Z) — "Four L1
build waves were granted by the seat gate (cap 200, live 127–138), then refused in full by the task
tool with `Background job limit reached (100)`, 0 spawned: KaidokuR25 37 seats, KotodamaR51 36 seats,
TsukuroiR24 40 seats, KakeR28 38 seats. The process admits a task call only while fewer than 100
background jobs run; earlier waves pushed the count above 100." `PHASE3.md:181` records the config
read (200) versus the enforced 100. The 85 cap at `PHASE3.md:182` is the repair.

**Live corroboration of the divergence** **[observed]**, `2026-10-22T07:01:50-03:00`:

| Measure | Value | Source |
|---|---|---|
| Gate live estimate | 63 | `wave-live.py` over the live session dir |
| Gate pending (120 s) | 0 | `awk` over `wave-slots` |
| Gate cap | 85 | `wave-cap` |
| Harness running jobs | 58 `[task]` + 1 `[service]` = 59 | `proc://` listing, same minute |

63 ≠ 59: the two numbers answer different questions (active-looking transcripts vs. non-queued
running jobs) and neither is authoritative for the other. The four L1s waiting in `proc://` are the
gate refusing at `63 + seats > 85`.

**Own-wave arithmetic** **[observed]**: `.ufo/waves/round-25/wave1-attempts.json` records the grant
text `granted lane=mori wave=r25-w1 seats=34 live=50 pending=0 cap=85` and ledger line
`1792663083 34 mori r25-w1`; `50 + 0 + 34 = 84 <= 85` — one seat of margin. The corresponding row is
the last line of `wave-slots`, and the wave produced 34 started jobs, no refusal.

---

## 6. Ledger counts for 2026-10-22

Command (read-only):

```
lo=$(date -d '2026-10-22 00:00:00' +%s); hi=$(date -d '2026-10-23 00:00:00' +%s)
awk -v lo="$lo" -v hi="$hi" '$1>=lo && $1<hi {n++; s+=$2; if($2+0>mx)mx=$2+0; l[$3]++}
  END {printf "GRANTS=%d SEATS_SUM=%d MAX_SEATS=%d LANES=%d\n", n, s, mx, length(l)}' \
  ~/.local/state/shokunin-hyaku/wave-slots
```

Output **[observed]**:

```
                    epoch  local (-03:00)        seats  lane       wave
               1792661550  2026-10-22T06:32:30      40   kama       r25a2-build
               1792661896  2026-10-22T06:38:16      36   kotoba     r49-build
               1792662386  2026-10-22T06:46:26      41   kotodama   r51a3-falsify
               1792663083  2026-10-22T06:58:03      34   mori       r25-w1
GRANTS=4 SEATS_SUM=151 MAX_SEATS=41 LANES=4
```

Whole file: 20 rows, 16 dated 2026-10-21, 4 dated 2026-10-22 (659 bytes, mtime
`2026-10-22 06:58:56 -03:00` — a `touch` from a later gate invocation, `wave-slot.sh:23`, not an append).

Caveat **[observed]**: `release` (`:94`) deletes rows and nothing logs releases, so 4 is the count of
**surviving** grant rows for the day, a lower bound on grants. All four rows are still present, i.e.
none of today's four waves released its slot. At `07:01:50 -03:00` the 120 s pending sum was 0.

---

## 7. Unresolved / out of scope

- Whether the L1 shells export `HYAKU_WAVE_CAP` is not observable from this seat; the state source is
  what `configured_cap` uses by default.
- Why the binary clamps at 100 while the setting default is 100 and the host config says 200 is a
  compiled decision (`Math.min(100, …)`); no config or project-level override reaches it. The binary is
  authoritative here; upstream intent is the C2 tool's problem, not this seat's.
- The harness's live running-job count is visible only inside a session (`proc://`), never to the gate.
- The 320 → 200 cap step has no recorded event anywhere read.

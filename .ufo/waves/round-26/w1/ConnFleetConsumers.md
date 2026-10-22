# ConnFleetConsumers — who consumes the C2 verdict, and how earlyoom relates to the fleet memory gate

Seat: `MoriR26.ConnFleetConsumers` (connector, leaf). Round 26, wave 1. Date 2026-10-22.
Mode: detection and report only. No fleet script change is proposed. No lane, fleet or sibling
file was written except this report. Scratch: `/fast/scratch/hyaku/mori-r26/MoriR26.ConnFleetConsumers/`.
Installs or updates: none.

## Answer in brief

1. The fleet runs exactly one scripted memory gate: the MemAvailable floor in
   `scripts/hyaku/wave-slot.sh` (6144 MiB by default). It is an admission check. It runs only
   when an L1 asks for a wave grant, and it never looks at running seats or at swap.
2. On this host, earlyoom's SIGTERM limit (mem avail ≤ 10% of `MemAvailable + AnonPages`
   **and** swap free ≤ 10%) always sits below the gate floor. Measured in memory level, the gate
   floor is crossed first, every time. earlyoom cannot fire while MemAvailable ≥ 6144 MiB unless
   user mem total is ≥ 61440 MiB, about twice this host's RAM.
3. A fleet run can still be killed by earlyoom, because crossing the floor only holds *future*
   grants. In the previous boot, earlyoom sent 39 kill signals; 26 of them came after the floor
   was committed, and 6 fell inside a window of heavy lane activity. At every logged warning,
   MemAvailable was between 158 and 2467 MiB, below the floor, so the gate would already have been
   refusing grants. It could not stop seats that were already running.
4. No script reads any mori tool verdict. The people who use the C2 verdict are Main, through the
   "memory stall" drop-back trip and its after-crash diagnosis, and tsukuroi, through its MP4
   action. The verdict covers the current boot only. On this boot it would read quiet, even though
   the previous boot had 39 actions.

## Evidence

### E1. The fleet gate (`scripts/hyaku/wave-slot.sh`, read-only)

- Floor, default: `MIN_AVAIL_MB=${HYAKU_WAVE_MIN_AVAIL_MB:-6144}` (`scripts/hyaku/wave-slot.sh:21`).
- Reading: `mem_avail_mb() { awk '/^MemAvailable:/ {print int($2 / 1024)}' /proc/meminfo; }`
  (`scripts/hyaku/wave-slot.sh:68`). It reads MemAvailable only, never SwapFree or AnonPages.
- Use: a grant needs both `fits_cap` and `[ "$m" -ge "$MIN_AVAIL_MB" ]` (`scripts/hyaku/wave-slot.sh:80`).
  On failure the gate retries every 20 s until a timeout (`scripts/hyaku/wave-slot.sh:87-88`).
  Nothing in the script runs after `granted` (`:83-84`), and `release` does not read memory (`:91-96`).
- Why it exists: "A grant also waits while MemAvailable < MIN_AVAIL_MB (a seat workload spike
  stalled memory at 20% PSI full)." (`scripts/hyaku/wave-slot.sh:8-9`). PSI is named in the comment
  but is not read anywhere in the script.
- Landed: `git -C /home/vgpnk/Projects/shokunin log -S'MIN_AVAIL_MB' -- scripts/hyaku/wave-slot.sh`
  → `cc57d9a 2026-10-21 03:09:19 -0300 ops(hyaku): corrected job-cap finding, wave target 200 with memory floor, …`.
- Incident that caused it: `.ufo/waves/hyaku/PHASE2.md:500-503`: "One reading showed 29/30 GB used,
  0 available, 22 GB swap, PSI `full avg10=19.95`; a minute later MemAvailable was 25 GB".
- Other memory checks: no other script in `scripts/hyaku/` reads memory. A grep of
  `scripts/` for `MIN_AVAIL|mem_avail|MemAvailable|earlyoom|oomd|psi` matches only
  `wave-slot.sh` and `wave-slot-selftest.sh:177`, which sets the floor to `0`.
  The only other memory "gate" is a judgment trip, with no number attached:
  "Drop-back trips stay in force: >20% dead seats in a wave, refusal of Main's own dispatches at
  the job cap, or a memory stall." (`.ufo/waves/hyaku/PHASE3.md:159`).
- PHASE3, last 200 lines (`:291-490`): no memory sample, no OOM entry, and no mention of earlyoom.
  Gate figures appear only as `live_estimate`/`cap` (for example `:350`, `:485`).
- Kumitate: the corpus has no memory-gate entry (`git -C kumitate-shokunin grep -i -E 'earlyoom|oomd|MIN_AVAIL|mem_avail|MemAvailable|wave-slot|PSI' HEAD -- corpus`
  → only unrelated substring hits plus `corpus/lessons/round-38-verifier-spotcheck.md:193` about the
  ledger). The only memory figure is in a gate receipt: `live=70 pending=33 cap=85 mem_avail_mb=23052 min=6144`
  (`kumitate-shokunin/.ufo/waves/round-39/evidence/seat-gate.txt:18`).
- Tsukuroi (sibling, at `157ee255`; cited, not absorbed): there is no fleet gate. The MP4 action reads "the
  operator must check for the running userspace killer (earlyoom is active and enabled on this
  host) before deciding what a second killer would do" (`memory-pressure-r25.md:216-218`).
  The entry also says "No row below concludes that nothing watches memory before the kernel." (`:42`).

### E2. earlyoom 1.9.0 limits (primary source, fetched 2026-10-22 by curl)

| URL | sha256 |
|---|---|
| https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/main.c | `08656b0bc90c85f23738661456b25c97af908bc5e2cfea78e0a69697b5f9d0e4` |
| https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/kill.c | `b32e0fad65e298235102f98aff37e02c94400b544d454cb57192ae697b100bf3` |
| https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/meminfo.c | `526e512c89c58cb0b1db2ae98ea62d287cdc1516846be80c9173bdc4bf0edfeb` |
| https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/MANPAGE.md | `cc48b02e79255ae27bad9b2c49364fcae1b6b5eb20fe8e83ecef432f360dfeda` |

Each digest is byte-identical to the L1 copy in `/fast/scratch/hyaku/mori-r26/` (`sha256sum`).

Quotes (verbatim):
- MANPAGE.md:20-21: "If **both** memory **and** swap (if any) are below 10%, it will kill the largest process (highest `oom_score`)."
- MANPAGE.md:31: "set available memory minimum to PERCENT of `user mem total` (default 10 %)."
- MANPAGE.md:34: "(`MemAvailable`+`AnonPages` as reported in `/proc/meminfo`)."
- meminfo.c:112: "m.UserMemTotalKiB = m.MemAvailableKiB + m.AnonPagesKiB;"
- main.c:502: "else if (m->MemAvailablePercent <= args->mem_term_percent && m->SwapFreePercent <= args->swap_term_percent)"
- main.c:472-473: "const unsigned min_sleep = 100;" / "const unsigned max_sleep = 1000;"
- kill.c:457: "/* find process with the largest oom_score */" (the default when `--sort-by-rss` is not set).

The percentage denominator is therefore **user mem total**, not MemTotal, and it is recomputed on
every poll. The man page says "below" (`:20`, `:41`), but the code uses `<=` (`main.c:500-502`).
The contract wording, which uses `<=`, matches the code.

### E3. Host numbers (read-only, 2026-10-22)

- `grep -E '^(MemTotal|MemAvailable|SwapTotal|SwapFree):' /proc/meminfo` → `MemTotal 31721800 kB`,
  `MemAvailable 22393316 kB`, `SwapTotal 31722876 kB`, `SwapFree 29157320 kB`.
- Current invocation, from the earlyoom unit journal (`journalctl -q -b -u earlyoom.service -o cat`;
  these are the version and threshold lines only):
  `earlyoom 1.9.0`; `mem total: 30978 MiB, user mem total: 28862 MiB, swap total: 30979 MiB`;
  `sending SIGTERM when mem avail <= 10.00% and swap free <= 10.00%,`;
  `SIGKILL when mem avail <=  5.00% and swap free <=  5.00%`.
- Unit: `ActiveState=active`, `UnitFileState=enabled`, start_time `Thu 2026-10-22 04:55:44 -03`;
  `systemd 262 (262-1-arch)`.
- Flag names only (the values are not copied): the unit command line carries 2 `--avoid` and
  1 `--prefer`, and no `--sort-by-rss`, `--ignore-root-user` or `--kernel-oom` was found in the
  unit command line or in `/etc/default/earlyoom`. Victim choice is therefore by largest
  `oom_score` (`kill.c:457`).

### E4. Threshold relation (arithmetic over E1 to E3)

| Quantity | Value on this host |
|---|---|
| Gate floor | 6144 MiB MemAvailable; swap not read |
| earlyoom SIGTERM, memory leg, at start (10% × 28862 MiB) | ≈ 2886 MiB |
| earlyoom SIGTERM, memory leg, at the logged firings (10% × 23470…26833 MiB) | ≈ 2347…2683 MiB |
| earlyoom SIGTERM, swap leg (10% × 30979 MiB) | ≤ 3098 MiB swap free, i.e. ≥ 27.9 GiB swap used |
| earlyoom SIGKILL (5% / 5%) | ≈ 1443 MiB mem and ≤ 1549 MiB swap free |
| Gate floor as a share of user mem total at start | 6144 / 28862 = 21.3% (19.8% of MemTotal) |
| Gate floor ÷ SIGTERM memory leg at start | ≈ 2.1× |
| Poll interval | gate: 20 s, and only while an `acquire` waits; earlyoom: 100–1000 ms, always |

For earlyoom to fire with MemAvailable ≥ 6144 MiB, user mem total would have to be ≥ 61440 MiB. This
host's MemTotal is 30978 MiB, so the memory leg can never be met above the floor.

### E5. What earlyoom actually did (journal, counts and memory numbers only)

`journalctl --list-boots`: boot −1 ran from 2026-10-20 09:57:09 to 2026-10-22 04:54:50 -03, and
boot 0 started at 2026-10-22 04:55:41 -03.

| Boot | earlyoom `sending SIG… to process` | SIGTERM-limit / SIGKILL-limit warnings | kernel `Out of memory: Killed` |
|---|---|---|---|
| −4, −3, −2 | 0 | 0 / 0 | 0 |
| −1 | 39 (38 SIGTERM, 1 SIGKILL; 0 escalations, 0 failed kills) | 39 / 1 | 1 (at 2026-10-22T03:54:59-03:00) |
| 0 (current) | 0 | 0 / 0 | 0 |

The per-boot loop was `journalctl -q -b $b -u earlyoom.service -o cat | grep -c -E 'sending SIG(TERM|KILL) to process'`,
with matching `grep -c` runs for the other columns. Boot 0 also has 0 systemd-oomd `d989611b…` notices.

The boot −1 actions, measured against the floor commit (`journalctl -o short-unix` and awk):
`before_floor_commit=13 after_floor_commit=26 before_2026-10-21T13:10:51=19 window_10-21_0300-0415=8 of_which_after_floor=6`.
- Action times, in 10-minute buckets: 2026-10-20 13:50–17:50 (10 actions), 19:50 (1);
  2026-10-21 03:00–04:00 (8); 2026-10-22 03:10 (20, within about 6 s, with swap free 0 MiB).
- Memory at the warning lines (the earlyoom `mem avail: … swap free: …` stats line, numbers only):
  MemAvailable min 158, max 2467 MiB; swap free max 3091 MiB. All are below the 6144 MiB floor.
- Fleet activity in the 2026-10-21 03:00–04:15 -03 window (`git -C <lane> log --all --since/--until | wc -l`):
  kumitate 84, souji 61, kama 46, tameshi 41, kake 33, mori 32, kagi 29, mado 24, kaidoku 4,
  kengaku 1. A fleet campaign was running while 6 post-floor kills happened.
- 2026-10-22 02:30–03:20 -03: 0 lane commits in any lane. Of the 39 victims, 1 was the harness
  binary: a SIGTERM at 2026-10-22T03:16:05-03:00. The names were sorted in memory into
  "harness" or "other"; no name was copied.
- Current oom_score ranking (`/proc/*/oom_score`, sorted; names reduced to harness or other):
  the largest omp process ranks 2nd at 847, behind one other process at 866. omp also has the
  largest RSS on the host, 2913 MiB (`ps -eo rss=,comm= --sort=-rss`).

## Contradictions (stated, not smoothed)

- K1. `.ufo/waves/hyaku/PHASE2.md:729`, at the 2026-10-21 13:10 -03 resume: "Host at resume:
  MemAvailable 26 GB, memory/CPU PSI ~0, no OOM in the journal." By then the same boot's earlyoom
  journal already held 19 kill actions (E5). The statement is true only for kernel OOM kills (the
  one kernel kill in that boot came later, at 2026-10-22 03:54:59). [INFERENCE] The check counted
  kernel-scope lines only. This is exactly the blind spot C2 closes.
- K2. `PHASE2.md:500-501` reads the recovery from "0 available" to "25 GB" a minute later as "a
  transient seat workload spike". The earlyoom actions at 2026-10-21 03:46:49 and 04:04:43 -03
  bracket a "~03:5x" reading (`PHASE2.md:493`). [INFERENCE] The recovery may have come from an
  earlyoom kill rather than from the spike ending. The ledger timestamp is too coarse to decide.
- K3. The `wave-slot.sh:8-9` comment justifies the floor by "20% PSI full", but the gate does not
  read PSI, and earlyoom 1.9.0 does not read PSI either (its limits are MemAvailable and SwapFree,
  `main.c:500-502`). Neither mechanism measures the signal that caused the incident.

## Who consumes the C2 verdict

- Machine consumers: none. `rg -l -F -e mori-job-runway -e mori-oom-killers -e KILLER_ACTED` over
  `scripts/`, `.ufo/waves/hyaku/`, `templates/` and the root `*.md` finds only `PHASE3.md`, which
  records `mori-job-runway` as a ledger fact (`:424`). Kumitate and tsukuroi have no hits under
  `corpus`/`tools`.
- People who use it:
  - Main, for the "memory stall" drop-back trip (`PHASE3.md:159`) and for after-crash diagnosis
    (K1).
  - Tsukuroi's MP4 action, before any second killer is enabled (`memory-pressure-r25.md:216-218`).
  - Closure seats that rule on dead-seat counts (`PHASE3.md:405`, the ">20% of a wave's seats
    dead" sentinel).
- Scope effect: the contract limits the verdict to the current boot and invocation
  (`contract.md:78-79`). Boot 0 has 0 actions, so [INFERENCE] the live verdict today would be
  `KILLERS_QUIET`. The 39 boot −1 actions, including the one harness SIGTERM, are invisible to it.
  A consumer reading `KILLERS_QUIET` as "earlyoom never touched the fleet" would be wrong.

## Proposed move (one, bounded)

Put one line in `corpus/knowledge/userspace-oom-killers-r26.md` that ties earlyoom to the fleet
gate and bounds the C2 verdict's scope. Nothing changes in the contract, the tool or fleet
scripts. Ready to paste:

```text
Fleet gate relation (2026-10-22): the seat gate's 6144 MiB MemAvailable floor (scripts/hyaku/wave-slot.sh:21, :80) always trips before earlyoom's SIGTERM limit here (about 2.4–2.9 GiB plus swap free ≤ 10%), but it only holds new grants, so earlyoom can still kill already-granted seats: the previous boot logged 39 earlyoom kills, 26 after the floor landed, and the tool's verdict covers only the current boot.
```

If the L1 wants it shorter (fewer than 40 words):

```text
The fleet seat gate's 6144 MiB floor trips before earlyoom's 10%/10% SIGTERM limit, but it guards only new grants; earlyoom killed 26 times after the floor landed (previous boot), and the C2 verdict covers the current boot only.
```

Affected axes:
- Adjacency improves: the line ties the FR10 entry to a fleet surface, citing it without absorbing it.
- Calibration improves: it blocks reading `KILLERS_QUIET` as "never killed".
- C1 freshness is unchanged: the line adds no stale phrase, and the four frozen phrases are untouched.
- C2 coverage is unchanged: no interface or case change.

No harm is expected to privacy (counts, MiB figures, a commit hash and dates only) or to the
retention scan.

## Risks

- R1. The counts are from the live journal on 2026-10-22 and can change if the journal is rotated
  or vacuumed. The entry line should cite a committed capture that reproduces E5, not this report.
- R2. "Always trips before" depends on host RAM (≤ 61440 MiB user mem total) and on the default
  `-m 10`. The unit carries `-m` twice (flag-name count only, values not read here). If a configured
  `-m` value differs from 10, the E4 arithmetic must use the thresholds from the invocation's
  journal line, which currently reads 10.00/10.00/5.00/5.00 (E3).
- R3. "26 after the floor landed" counts from the commit time. It does not show the floor was in
  force in a running session at each kill (the session could have run older script bytes).
  Phrase it as "after the floor was committed" if a reviewer objects.
- R4. The harness-victim count comes from victim names sorted in memory. If the privacy reviewer
  rules even that category off-limits, drop that clause; the proposed line does not use it.

## Verification for the L1 (not run by this seat as a pass)

```sh
grep -n -E 'MIN_AVAIL_MB=|mem_avail_mb\(\)|-ge "\$MIN_AVAIL_MB"|sleep 20' /home/vgpnk/Projects/shokunin/scripts/hyaku/wave-slot.sh
git -C /home/vgpnk/Projects/shokunin log --format='%h %ad' --date=iso -S'MIN_AVAIL_MB' -- scripts/hyaku/wave-slot.sh
journalctl -q -b -1 -u earlyoom.service -o cat --no-pager | grep -c -E 'sending SIG(TERM|KILL) to process'   # expect 39
journalctl -q -b -1 -u earlyoom.service -o short-unix --no-pager | grep -E 'sending SIG(TERM|KILL) to process' | awk -v g="$(date -d '2026-10-21 03:09:19 -0300' +%s)" 'int($1)>=g{n++} END{print n}'   # expect 26
journalctl -q -b -u earlyoom.service -o cat --no-pager | grep -E '^ *(user mem total|mem total|sending SIGTERM when|SIGKILL when)'
```

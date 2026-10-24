# DraftSkillFr10 — SKILL.md draft for FR10 userspace OOM killers (round 26, wave 1)

Seat: `MoriR26.DraftSkillFr10` (scribe, leaf; no subagents, no background jobs). Date: 2026-10-22.
Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin`. Scratch: `/fast/scratch/hyaku/mori-r26/DraftSkillFr10/`.

**Mode: draft only.** No product file was edited. The only file written in the lane is this report
(`.ufo/waves/round-26/w1/DraftSkillFr10.md`). No `jj` command was run at the fleet root; no
`git add/commit/stash/checkout/switch/reset/pull/push` was run in the lane; only read-only `git`
(`log`, `show`, `rev-parse`, `cat-file`, `diff-filter=A`, `merge-base`) and ordinary reads.

Lane tip while writing: `21386b9` ("round-26: supplementary cases updated to case-seat tip da9af118").
Earlier tips seen: `5e5e86f`, `b4473ed`, `825f988`, `278f02e`, `99338de`, `c2fdd92`, `5b10649`.

---

## 1. What I read (provenance)

| Input | Location | Note |
|---|---|---|
| round-26 claim contract | `.ufo/waves/round-26/contract.md` — C2 interface at `:48-119`, amendments A1 at `:126-150`, A2 at `:152-172` | binding CLI, grammar, states, verdict/exit map, frozen case file, selftest string |
| lane SKILL.md house style | `SKILL.md:11-21` (`## Decision table`, 4 columns Intent / Correct surface / Never / Expected output); `SKILL.md:23-45` (`## Error patterns`, 2 columns Observation / Reading); `SKILL.md:162-184` (`## Gates` registry, 8 columns); `SKILL.md:520`, `:584`, `:639-642` (round-local registries, same 8 columns) | the registry format is `name \| kind \| entry \| verdict map \| self-test \| pinned values \| write scope \| owner` |
| fleet gate standard | `/home/vgpnk/Projects/shokunin/PROTOCOL.md:375-403` | `0` = clean, `1` = failed; every other code declared and mapped onto `clean \| failed \| could-not-evaluate`; a tool that cannot fail is a **probe**; self-test spelling is lane-owned but must be registered |
| C2 tool (landed) · C2 frozen cases | `tools/mori-oom-killers.py` (blob `44dac3fd…` at `21386b9`; first commit `c2fdd92`) · `tools/fixtures/mori-oom-killers/cases.json` (blob `5b4dcee7…`; first commit `5b10649`, a strict ancestor of `c2fdd92`; 32 cases, `schema: mori-oom-killers-cases-v1`) | verdicts, exits, output fields, live collection |
| C2 committed receipts | `.ufo/waves/round-26/evidence/c2-selftest.txt`, `.ufo/waves/round-26/evidence/c2-live-run.txt`; counters `.ufo/waves/round-26/count-c1.sh`, `count-c2.sh` | the counted after-values |
| round-25 tools | `tools/mori-routed-r24.py` (commit `e54b644`, +`e06d4a0`), `tools/mori-job-runway.py` (commit `09f55b6`, +`9a3d511` A2, +`fbecc59`, +`d3b7af2`) | read `--help`, docstrings and code; runs in §4.4 |
| routed defects R1 · R3 · R5 | `corpus/lessons/round-25-verifier-spotcheck.md:174-179` (R1, job-runway false numbers), `:182-185` (R3, the round-25 SKILL block — **not** my item), `:189-193` (R5, registry conformance) | R1 detail: `corpus/knowledge/harness-job-capacity-r25.md:211`, `.ufo/waves/round-25/w2/ReviewRunwayCode.md:40-53`, `CriticHarnessOverclaim.md:41-88` |
| upstream earlyoom v1.9.0 · upstream systemd v262 | `https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/{main.c,kill.c,meminfo.c,README.md,MANPAGE.md}` and `https://raw.githubusercontent.com/systemd/systemd/v262/{catalog/systemd.catalog.in,src/oom/oomd-util.c}`, fetched 2026-10-22 | sha256 and line use in §7 |
| stale FR10 statement | `corpus/knowledge/userspace-oom-killers-r12.md` (`## Claim` at `:6`, `## Evidence` at `:11-15`, `## Observed` at `:18`) and `corpus/README.md:34` | the four frozen phrases in `.ufo/waves/round-26/c1-phrases.txt` |
| sibling adjacency (cite, never absorb) | `tsukuroi-shokunin@157ee255:corpus/knowledge/memory-pressure-r25.md` | says the capture never read earlyoom; mori owns the fleet-facing evidence rule |
| sibling wave-1 reviews I relied on | `.ufo/waves/round-26/w1/ReviewContractGrammar.md:77-140` (grammar verdicts, action-relevant messages the contract misses), `ReviewOomdV262Facts.md:31-100` (v262 oomd facts), `ReviewScopeClock.md:56-123` (scope clock, S1/S2), `SrcEarlyoomReadme.md:79-92` (`--kernel-oom` absent from v1.9.0), `HostCapture.md` (host capture) | cited where I repeat a finding |

### Host facts (read-only, this host, 2026-10-22)

| Fact | Value | Command |
|---|---|---|
| `earlyoom.service` | `LoadState=loaded`, `ActiveState=active`, `UnitFileState=enabled`, `ActiveEnterTimestampMonotonic=19964362`; `ExecStart` start time `2026-10-22 04:55:44 -03` | `systemctl show earlyoom.service -p LoadState,ActiveState,UnitFileState,ActiveEnterTimestampMonotonic` |
| `systemd-oomd.service` | `LoadState=loaded`, `ActiveState=inactive`, `UnitFileState=disabled` | `systemctl show systemd-oomd.service -p …` |
| versions | earlyoom `1.9.0` (`earlyoom 1.9.0-1`), systemd `262 (262-1-arch)`, kernel `7.2.11-arch1-1` | `earlyoom --version` (prints the banner), `systemctl --version`, `uname -r` |
| earlyoom journal this boot | 13 entries; version line at monotonic `19981126`, both threshold lines at `19981234` (same microsecond — the two lines are two entries, not one); **0** `sending SIG… to process` lines, **0** escalations, **0** `kill failed:`, **0** low-memory warnings, **0** dry-run, 6 periodic `mem avail:` report lines | `journalctl -q -b -u earlyoom.service -o json --output-fields=MESSAGE` (classes counted in-process; no MESSAGE text reproduced here) |
| oomd notices · kernel OOM summaries | **0** in the current boot, both | `journalctl -q -b MESSAGE_ID=d989611b15e44c9dbf31e3c81256e4ed -o json --output-fields=MESSAGE_ID \| wc -l` · `journalctl -k -b -q --grep='^oom-kill:constraint=' -o json --output-fields=_BOOT_ID \| wc -l` |
| earlyoom thresholds in force | SIGTERM `10.00%` mem / `10.00%` swap; SIGKILL `5.00%` mem / `5.00%` swap | parsed from earlyoom's own startup lines (below) |

Privacy: no process name, command line, uid, `--avoid`/`--prefer` expression or `/etc/default/earlyoom`
value is reproduced in this report. Journal `MESSAGE` text appears only as the three fixed-format lines
the grammar pins (version line and the two threshold lines), which the contract itself admits as
output; the two threshold lines carry percentages only.

---
## 2. (a) Decision rows — "Did a userspace killer act?"

### 2.1 Placement

**Primary:** a new round-scoped section at the end of `SKILL.md`, after the round-25 block
(`SKILL.md:644-673`), titled `## Round26 — userspace OOM killers (C1/C2)`, containing the condition
table in §2.2 and the registry additions in §4.

**Alternative (L1's call):** one row in the lane-wide `## Decision table` (`SKILL.md:13-21`) plus the
round-scoped detail table. The round-24 precedent chose the round-scoped table only
(`.ufo/waves/round-24/w1/DraftSkillTable.md` §3.2, same reason: the top table's 4 columns cannot carry
condition → report-as → never-infer rules).

### 2.2 The decision table (ready to paste)

```markdown
## Round26 — userspace OOM killers (C1/C2)

`python3 -I -B tools/mori-oom-killers.py` reads what this host's two **userspace** OOM killers
(earlyoom, `systemd-oomd`) are set to do and whether they have acted. It is detection and report
only: it starts, stops or configures nothing, and it never prints journal `MESSAGE` text, a process
name, a command line, a uid or an `--avoid`/`--prefer` expression. Host/unit diagnosis and any
killer tuning stay operator-owned (`PROVINCE.md:53`, FR10).

Grounded in `corpus/knowledge/userspace-oom-killers-r26.md` (the 2026-10-22 host record that
supersedes the 2026-10-19 reading in `corpus/knowledge/userspace-oom-killers-r12.md`) and in the
earlyoom v1.9.0 message grammar at tag `v1.9.0`. The tool is the Core surface; this table is the
reading rule.

### Did a userspace killer act?

| Condition | Report as | Never infer |
|---|---|---|
| earlyoom is `active` and its unit journal (current boot) holds a `sending SIGTERM to process ` or `sending SIGKILL to process ` line, or an `escalating to SIGKILL after ` line, **inside the current invocation's scope** | `KILLER_ACTED` (exit 1); `earlyoom.actions.sigterm` / `.sigkill` / `.escalations` counted | that a process died — the line is earlyoom's own log of a signal it sent ([kill.c:627](https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/kill.c), [kill.c:318](https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/kill.c)); that the count is a victim count (it is a count of log lines); that the killed process belonged to the fleet |
| earlyoom is `active` and reports `dryrun` mode (`dryrun mode enabled`, [main.c:295](https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/main.c)) | `earlyoom.dryrun_send_lines` counts the send lines; `sigterm`/`sigkill` stay 0 and are never positive evidence | that nothing was signalled — dry-run sends no signal; that a dry-run line means a kill happened |
| earlyoom is `inactive` or its unit is `not-found` | `earlyoom.state` is `inactive` or `absent`; `earlyoom.actions` is **null** (unavailable), never zero counts | that the killer made no kills — an unavailable killer is not a killer that did nothing; that the host is healthy on the memory plane |
| earlyoom is in a non-steady state (`failed`, `activating`, `deactivating`, `reloading`, `maintenance`, `refreshing`) | `earlyoom.state` is `unavailable`; verdict `KILLERS_UNKNOWN` (exit 2) | that the unit is idle — an earlier invocation may have acted, so the state is not readable as active or inactive |
| earlyoom is `active` but its `ActiveEnterTimestampMonotonic` is missing or 0, or the invocation's version line is not in scope | `scope_complete: false`, verdict `KILLERS_UNKNOWN` (exit 2) | that the scope was empty because nothing happened — an unbounded scope is unknown, not quiet |
| an earlyoom `sending … to process` line falls **before** the current invocation's `ActiveEnterTimestampMonotonic` (an earlier invocation in the same boot) | `earlyoom.earlier_invocation_send_lines` reports the count; for an `active` unit it is not a verdict input (frozen case `c02`), for a unit that is not `active` it is positive evidence → `KILLER_ACTED` | that a restarted earlyoom never killed anything — the earlier invocation's sends are still sends; that `scope_complete: true` means the whole boot was checked |
| `systemd-oomd.service` notices with catalog `MESSAGE_ID` `d989611b15e44c9dbf31e3c81256e4ed` exist in the current boot | `oomd.notices_this_boot` > 0 → `KILLER_ACTED` (exit 1); the count is of journal **notices**, one per killed unit | that the notice names a unique victim — the catalog entry is "one or more processes in the unit @UNIT@" ([systemd.catalog.in:884-885](https://raw.githubusercontent.com/systemd/systemd/v262/catalog/systemd.catalog.in)); that oomd acted on the fleet |
| the kernel wrote an `oom-kill:constraint=` summary (system journal, `journalctl -k`) | kernel-side OOM evidence, reported by the existing kernel attribution path (`corpus/knowledge/kernel-oom-line-attribution-r12.md`) | that earlyoom or oomd caused it — earlyoom v1.9.0 has **no** `--kernel-oom` delegation option (its `-k` is ignored since v1.2, [main.c:245-246](https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/main.c); the option list at [main.c:180-192](https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/main.c) has no `kernel-oom`), so an earlyoom kill never produces a kernel OOM record |
| a needed read failed (unit show unreadable, journal unreadable, notice count unavailable) | the affected field is `null` / the state is `unavailable`; verdict `KILLERS_UNKNOWN` (exit 2) | that the killers were quiet — an unreadable surface is unknown, not zero |
| everything readable, no positive evidence anywhere | `KILLERS_QUIET` (exit 0) | that no memory kill happened in this boot — quiet means "no positive evidence from the killers that could be read", and it names the unavailable ones |
```

### 2.3 Row coverage check

earlyoom active/inactive → rows 1, 3, 4 · journal `sending SIG… to process` lines → rows 1, 2, 6 ·
oomd notices → row 7 · kernel OOM lines → row 8 · unavailable-not-zero → rows 3, 4, 5, 9, 10.

---

## 3. (b) Error patterns

### 3.1 Placement

**Primary:** a new `### Error patterns (userspace OOM killers)` subsection inside the round-26
section, using the lane's 2-column `Observation | Reading` shape from `SKILL.md:25-45`.

**Alternative:** append the three rows to the lane-wide `## Error patterns` table (`SKILL.md:23-45`).
The round-24 precedent put its reading rules in its own round-scoped table instead; I recommend the
round-scoped subsection, because the three rules below are specific to the FR10 surfaces and would
otherwise sit next to lane-wide contracts.

### 3.2 The error-pattern rows (ready to paste)

```markdown
### Error patterns (userspace OOM killers)

| Observation | Reading |
|---|---|
| earlyoom's thresholds read from `/etc/default/earlyoom`, from the unit file, or from the upstream defaults | the thresholds in force are the ones earlyoom printed at startup: `sending SIGTERM when mem avail <= <a>% and swap free <= <b>%,` ([main.c:414](https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/main.c)) and `SIGKILL when mem avail <= <c>% and swap free <= <d>%` ([main.c:416](https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/main.c)), read from the unit's journal. The packaged default file is only the argument source (`EnvironmentFile=-/etc/default/earlyoom`, `ExecStart=/usr/bin/earlyoom $EARLYOOM_ARGS`, `/usr/lib/systemd/system/earlyoom.service:6-7`); the built-in defaults are 10 % with `PERCENT/2` for the kill threshold ([MANPAGE.md:31,45,56-57](https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/MANPAGE.md)). **Never** treat the config file or the documented default as the running configuration — the running values are the printed ones; and never copy the file's values or the `--avoid`/`--prefer` expressions into a report |
| `oom_kill=0` (cgroup `memory.events` or `/proc/vmstat`) read as "no memory kills" while earlyoom is `active` | that counter moves only at the **kernel** victim site ([oom_kill.c:935-936 v7.2](https://raw.githubusercontent.com/torvalds/linux/v7.2/mm/oom_kill.c)); earlyoom signals in userspace and never increments it, and systemd-oomd kills through `cgroup.kill`/`kill()` and records `user.oomd_ooms`/`user.oomd_kill` xattrs instead ([oomd-util.c:269-306 v262](https://raw.githubusercontent.com/systemd/systemd/v262/src/oom/oomd-util.c)). With earlyoom active, `oom_kill=0` says only "no **kernel** OOM kills"; the userspace killers' own evidence is earlyoom's journal send lines and the `d989611b…` oomd notices. `corpus/knowledge/oom-kill-counter-kernel-only-r12.md`, `userspace-oom-killers-r12.md` |
| earlyoom journal lines counted from a whole-boot query (`journalctl -b -u earlyoom.service` with no invocation bound) | earlyoom's log lines belong to **one invocation**; the scope is the lines whose `__MONOTONIC_TIMESTAMP` is at or after the unit's `ActiveEnterTimestampMonotonic`. A restart inside one boot gives a new `ActiveEnter`, so the previous invocation's send lines fall below the bound and a whole-boot count attributes an old kill to the running instance (`earlyoom.earlier_invocation_send_lines`; `.ufo/waves/round-26/w1/ReviewScopeClock.md:56-69`). The bound is comparable within a boot because both clocks are `CLOCK_MONOTONIC` |
```

### 3.3 Coverage check

thresholds from the config file → row 1 · `oom_kill=0` while earlyoom is active → row 2 ·
lines from a previous invocation → row 3.

---

## 4. (c) Gate-registry rows (three tools)

Format: the 8-column house shape `name | kind | entry | verdict map | self-test | pinned values |
write scope | owner` (`SKILL.md:162`, `:520`, `:584`, `:639-642`).

`kind` follows `PROTOCOL.md:377-378`: a **gate** is a committed, re-runnable verdict script that
compares surfaces against expected values persisted in its own repo; a tool that cannot fail is a
**probe**. All three tools below can fail (exit 1), so all three are gates. The two round-25 tools
were never registered (`corpus/lessons/round-25-verifier-spotcheck.md:189`, R5).

### 4.1 `tools/mori-oom-killers.py` (new, round 26, C2)

```markdown
| userspace OOM killers (r26, C2) | gate (host-surface verdict over two units; not a census or fleet-admission gate) | `python3 -I -B tools/mori-oom-killers.py [--inputs FILE \| --selftest \| --dump-inputs] [--cases FILE]` — no arguments collects the inputs live (`systemctl show` of the two units' `LoadState,ActiveState,UnitFileState,ActiveEnterTimestampMonotonic`; the earlyoom unit journal of the current boot; the `d989611b15e44c9dbf31e3c81256e4ed` notice line count) and runs the same pure reader; `--inputs FILE` runs the reader on one JSON inputs object; `--dump-inputs` prints the live inputs with every non-version/threshold `MESSAGE` replaced by its grammar class | 0 → clean (`KILLERS_QUIET`) · 1 → failed (`KILLER_ACTED`) · 2 → could-not-evaluate (`KILLERS_UNKNOWN`: a needed read is null, an active earlyoom has an incomplete scope or an unverified grammar, a show text lacks `ActiveState`, or a setup/internal error — an uncaught exception never exits 1) | `python3 -I -B tools/mori-oom-killers.py --selftest` → `MORI_OOM_KILLERS_SELFTEST: PASS 32/32` over `tools/fixtures/mori-oom-killers/cases.json` (32 cases, `schema: mori-oom-killers-cases-v1`, frozen in `5b10649` before the tool's first commit `c2fdd92`; `count-c2.sh` reports `freeze_order=ok`, `cases_changed_since_freeze=0`) | result `schema: mori-oom-killers-v1`; `earlyoom` {`state` (`active`/`inactive`/`absent`/`unavailable`), `version`, `grammar` (`verified-1.9.0`/`unverified`), `thresholds`, `scope_complete`, `actions`, `dryrun`, `dryrun_send_lines`, `process_group_lines`, `earlier_invocation_send_lines`}, `oomd` {`state`, `notices_this_boot`}, `verdict`; the earlyoom grammar is pinned to tag `v1.9.0` (`main.c:161,295,414,416,519,523`; `kill.c:318,627,654`); `actions` is null for an inactive or absent killer, never zero counts | none live — stdout only; reads `systemctl show` and `journalctl` (two `journalctl` reads, one for the unit journal and one for the notice count); no unit, journal, package or network change; the output carries states, numbers, the version string and counts — never `MESSAGE` text, a process name, a command line, a uid or an `--avoid`/`--prefer` expression | mori |
```

### 4.2 `tools/mori-routed-r24.py` (round 25, C1) — the R5 row

```markdown
| routed round-24 items (r25, C1) | gate (committed-bytes consistency gate over the lane's own round-24 evidence; not a fleet-admission gate) | `python3 -I -B tools/mori-routed-r24.py --repo REPO --rev REV [--rerun]` — every predicate reads git objects only (`cat-file`, `ls-tree`, `archive`, `merge-base`) at REV; the working tree is never consulted; `--rerun` additionally re-executes the named revision's `mori-pressure.py --selftest` from a temporary extract and reports byte equality | 0 → clean (`status: held`: all four counted items D1, D2, D3, D5 held **and** the D4 hygiene row held) · 1 → failed (any counted item red, or the D4 hygiene row red) · 2 → could-not-evaluate (the repository path is not a directory, the revision does not resolve to a commit, or a git call fails) | none built in — the tool has no `--selftest`; able-to-fail evidence is the round-25 wave-2 mutation reports (`.ufo/waves/round-25/w2/MutRoutedD1.md`, `MutRoutedD2.md`, `MutRoutedD3D5.md`, `MutRoutedHygiene.md`). **A committed self-test is still owed** (routed defect R5) | result `schema: mori-routed-r24-v1`; `items: 4`; per-item rows `{id, held, reasons[], detail}` for D1 (stale gate evidence), D2 (correction sweep in `corpus/knowledge/system-pressure-r24.md`), D3 (lesson count drift), D5 (`## Axes` table against the pinned base `28b79d3d`); D4 is a reported hygiene row, not a counted item; D3's case count is pinned to `4f05dd5a` (7 supplementary cases) | read-only git object reads over the measured repo; a temporary extract only for `--rerun`; **known limits**: D1 compares the recorded body with a constant, so only `--rerun` detects a forged PASS; D5 reads the Score and Last-change columns by position, never by header name; D2 does not scan heading lines for the stale phrases; D3 holds while the uncorrected `PASS 6/6` line remains; an unreadable pinned baseline exits 1, not 2; a promisor clone can have objects fetched into it (no `GIT_NO_LAZY_FETCH`); a `--repo` below the repository top level changes the result. `corpus/lessons/round-25-verifier-spotcheck.md:189-193` | mori |
```

### 4.3 `tools/mori-job-runway.py` (round 25, C2) — the R5 row

```markdown
| harness background-job runway (r25, C2) | gate (reads the operator's harness configuration and the installed binary; not a census or fleet-admission gate) | `python3 -I -B tools/mori-job-runway.py [--config PATH] [--binary PATH] [--selftest] [--cases PATH]` — `--config` defaults to `~/.omp/agent/config.yml`, `--binary` to the real path of `omp` on `PATH`; the tool reads one settings file and one binary and never runs `omp` | 0 → clean (`RUNWAY_AS_CONFIGURED` when the configured value equals the effective cap, `RUNWAY_DEFAULT` when no `maxJobs` is configured) · 1 → failed (`RUNWAY_CLAMPED`: the effective cap differs from the configured value) · 2 → could-not-evaluate (`RUNWAY_UNKNOWN`: the effective cap could not be derived, or a usage error) | `python3 -I -B tools/mori-job-runway.py --selftest` → `MORI_JOB_RUNWAY_SELFTEST: PASS 21/21` over `tools/fixtures/mori-job-runway/cases.json` (21 frozen cases); a co-evolved `tools/fixtures/mori-job-runway/supplementary-cases.json` (24 cases) is **not** counted; `--selftest --cases ""` silently runs the frozen cases instead of failing | result `schema: mori-job-runway-v1`; `configured {state,value}`, `clamp {state,value,sites}`, `setting_default {state,value,sites}`, `effective`, `verdict`; the clamp is `max(1, min(clamp, base))`; the configured value is read from a block-style `async:` → `maxJobs:` child only | read-only: one settings file and one binary are read; the only writes are the `--selftest` temporary files; the operator's settings file is never edited and its values are never printed in a report. **Known false-number limit (routed defect R1, still open)**: the rule-1 line grammar reads only the block-style `async:` → `maxJobs:` form, so a YAML/JSON form that omp's own parser reads as `maxJobs: 50` (a flow mapping `{async: {maxJobs: 50}}`, a JSON file, a flow or tagged child, an anchored or escaped `async` header, an indented root) is reported as `configured {absent, null}` → `effective 100` → `RUNWAY_DEFAULT`, exit 0 — a **false number**, and a file omp's parser refuses can still be reported as `set 50`, exit 0; `--selftest --cases ""` silently runs the frozen cases; an uncaught exception exits 1, the `RUNWAY_CLAMPED` code. `corpus/lessons/round-25-verifier-spotcheck.md:174-179`; `corpus/knowledge/harness-job-capacity-r25.md:211` | mori |
```

### 4.4 Truthful inputs / verdicts / exits — what I actually ran

`tools/mori-routed-r24.py`:

| Command | Result |
|---|---|
| `--help` | `usage: mori-routed-r24.py [-h] --repo REPO --rev REV [--rerun]` — **no `--selftest`** |
| `--repo <lane> --rev HEAD` | exit **0**, `"held":4,"items":4,"mismatches":0`, `"status":"held"`, D4 hygiene `held:true` |
| `--repo <lane>/tools --rev HEAD` | exit **1** — a `--repo` below the top level changes the result (measured) |
| `--repo /nonexistent --rev HEAD` · `--repo . --rev deadbeef` | exit **2** (both) |
| `--repo <shallow depth-1 clone> --rev HEAD` | exit **1** — an unreadable pinned baseline gives exit 1, not 2 (measured) |

`tools/mori-job-runway.py`:

| Command | Result |
|---|---|
| `--help` | `--config`, `--binary`, `--selftest`, `--cases` |
| `--selftest` | `MORI_JOB_RUNWAY_SELFTEST: PASS 21/21`, exit **0** (21 frozen cases; 24 supplementary, not counted) |
| `--selftest --cases ""` | `MORI_JOB_RUNWAY_SELFTEST: PASS 21/21`, exit **0** — the empty path silently falls back to the frozen cases (measured) |
| block-style `async:` / `maxJobs: 50` | `configured {set, 50}` → `effective 50` → `RUNWAY_AS_CONFIGURED`, exit **0** |
| flow root `{async: {maxJobs: 50}}` · JSON form `{"async": {"maxJobs": 50}}` | `configured {absent, null}` → `effective 100` → `RUNWAY_DEFAULT`, exit **0** — the false number of R1 (both measured) |
| anchored header `&a async:` · escaped header `"\x61sync":` · indented root · flow child `{maxJobs: 50}` · tagged child `!!str maxJobs: 50` · `&a maxJobs: 50` · `"max\u004aobs": 50` | all `configured {absent, null}` → `effective 100` → `RUNWAY_DEFAULT`, exit **0** (measured, seven forms) |
| quoted header `"async":` · inline `async: {maxJobs: 50}` | `configured {malformed, null}` → `RUNWAY_UNKNOWN`, exit **2** (the A2 abstention; these two are *not* false numbers) |
| stray deeper line under `maxJobs` (`     extra: 1`) · `async:#c` header | `configured {set, 50}` → `RUNWAY_AS_CONFIGURED`, exit **0** for files omp's parser refuses (measured) |
| non-integer `maxJobs: abc` | `configured {malformed, null}` → `RUNWAY_UNKNOWN`, exit **2** |
| 4301-digit `maxJobs` value | uncaught exception, exit **1** (the `RUNWAY_CLAMPED` code), no JSON (measured) |

`tools/mori-oom-killers.py`:

| Command | Result |
|---|---|
| `--help` | `--inputs FILE`, `--selftest`, `--dump-inputs`, `--cases FILE` |
| `--selftest` | `MORI_OOM_KILLERS_SELFTEST: PASS 32/32`, exit **0** |
| `--selftest --cases /nonexistent.json` | exit **2**, `verdict: KILLERS_UNKNOWN`, `error:` field, JSON still printed |
| live (no arguments) | `KILLERS_QUIET`, exit **0**; `earlyoom` active, `version 1.9.0`, `grammar verified-1.9.0`, `scope_complete true`, thresholds 10.00/10.00/5.00/5.00, all action counts 0; `oomd` inactive, `notices_this_boot 0` |
| `--inputs`, SIGTERM action line in scope | `KILLER_ACTED`, exit **1** |
| `--inputs`, inactive earlyoom, readable oomd | `KILLERS_QUIET`, exit **0**, `earlyoom.actions: null` (unavailable, not zero) |
| `--inputs`, absent earlyoom, null notice count · `--inputs`, all reads null | `KILLERS_UNKNOWN`, exit **2** (both) |
| `--inputs`, send line **before** the invocation bound | `KILLERS_QUIET`, exit **0**, `earlier_invocation_send_lines: 1`, `scope_complete: true` |
| `--inputs`, inactive unit with a send line this boot | `KILLER_ACTED`, exit **1** |

---

## 5. Out of scope for this seat (handoff to the integration owner)

1. **The r26 knowledge entry** `corpus/knowledge/userspace-oom-killers-r26.md` — another seat's
   (`DraftEntryR26`). My tables cite it as the grounding entry; it does not exist in the lane yet
   (`corpus/knowledge/` has no `*-r26.md` at `21386b9`), so the SKILL.md text must land with it.
2. **The four stale statements** in `corpus/knowledge/userspace-oom-killers-r12.md` and
   `corpus/README.md:34` — `DraftR12Corrections`' item. (Note: the r12 file shows an uncommitted
   working-tree edit in `git status` at my write time; it is not mine — I wrote only this report.)
3. **The round-25 SKILL block rows 1-4** (routed R3) — `DraftHygieneKnowledge`'s item.
4. **`corpus/SOURCES.md` rows** for the sources opened this round — the source seats' items; the
   registry rows above cite upstream URLs and line numbers inline instead of S-ids, because the S-id
   numbering is the owner's.
5. **`SCORECARD.md`** — the capabilities row and the round-26 Axes rows are not mine.
6. **The tool and the frozen cases** — `BuildOomKillersTool` / `WriteOomKillersCases`; landed, not mine.

---

## 6. Conflicts and open decisions for the canonical judge

**Conflict 1 — exit 1 is "failed" fleet-wide, but `KILLER_ACTED` is a finding, not a broken gate.**
`PROTOCOL.md:379-384` fixes `0` = clean, `1` = failed. The C2 contract fixes `KILLER_ACTED` at exit 1
(`.ufo/waves/round-26/contract.md:97-98`). The lane precedent (`mori-pressure.py`, `PRESSURE_HIGH` at
exit 1) reads exit 1 as "the gate fired its alarm". The registry rows above follow that precedent and
say so in the verdict-map cell; the judge may prefer the words "finding fired" to "failed".

**Conflict 2 — `RUNWAY_CLAMPED` at exit 1 is likewise a finding** (the effective cap is below the
configured value — a statement about the harness, not a gate failure). Same reading as Conflict 1.

**Conflict 3 — `KILLERS_QUIET` at exit 0 is not a health statement.** Exit 0 can mean "no positive
evidence from the killers that could be read", including the case where a killer is inactive
(`actions: null`). The verdict map says `clean`, which the outer interface requires, but the decision
table row 9 says in words that quiet is not "no kill happened". That split is deliberate; a reader
who takes exit 0 as a health verdict will misread it.

**Conflict 4 — the R1 false-number limit is still open, and the row says so.** `mori-job-runway.py`
can report `effective 100` / `RUNWAY_DEFAULT` / exit 0 for a configuration omp's parser reads as
`maxJobs: 50`, and can report `set 50` for a file omp's parser refuses. R1 asks for the abstention and
for the probe corpus to be committed as fixtures. The registry row carries the limit as a "known
limits" clause rather than hiding it. If the L1 prefers to register the tool as a **probe** until R1
lands, the `kind` cell and the verdict map change and nothing else does.

**Conflict 5 — the round-25 tools were never registered, so this is an addition, not a correction.**
`SKILL.md` has no registry row for either round-25 tool (the round-25 block at `SKILL.md:644-673` is a
reading table only). R5 asks for the rows. I placed all three rows in one new round-26 table; the
L1 may prefer two round-25 rows inside the round-25 section and one round-26 row in the new section.
The row text is unchanged either way.

**Conflict 6 — `--kernel-oom` is absent from earlyoom 1.9.0.** The r12 entry's earlyoom clause says
"only `--kernel-oom` delegates to the kernel OOM killer" and cites the README at upstream master
(`S016`). At tag `v1.9.0` there is no such option: the long-option list (`main.c:180-192`) has no
`kernel-oom`, `-k` prints "Option -k is ignored since earlyoom v1.2" (`main.c:245-246`), and the
v1.9.0 README's "Why not trigger the kernel oom killer?" section says earlyoom does not use
`/proc/sysrq-trigger` (`README.md:65-68`). The option exists on upstream master
(`main-now.c:202`, `README-now.md:69`), so the r12 sentence is true of master and false of the
installed 1.9.0. Decision-table row 7 is written to the v1.9.0 fact; the r12 clause itself is
`DraftR12Corrections`'/`SrcEarlyoomReadme`'s item.

---

## 7. Sources opened (ordinary fetch, 2026-10-22)

| File | URL | sha256 | Lines used |
|---|---|---|---|
| earlyoom `main.c` (tag v1.9.0) | `https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/main.c` | `08656b0bc90c85f23738661456b25c97af908bc5e2cfea78e0a69697b5f9d0e4` (552 lines) | `161` version line; `180-192` option table; `245-246` `-k` ignored; `295` dry-run; `414`, `416` threshold lines; `519`, `523` low-memory warnings |
| earlyoom `kill.c` (tag v1.9.0) | `https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/kill.c` | `b32e0fad65e298235102f98aff37e02c94400b544d454cb57192ae697b100bf3` (666 lines) | `318` escalation; `617-629` send line (signal name ∈ {SIGTERM, SIGKILL, `0 (no-op signal)`}); `654` `kill failed:` |
| earlyoom `meminfo.c` (tag v1.9.0) | `https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/meminfo.c` | `526e512c89c58cb0b1db2ae98ea62d287cdc1516846be80c9173bdc4bf0edfeb` (286 lines) | `279` the periodic `mem avail:` report line (not a grammar line) |
| earlyoom `README.md` (tag v1.9.0) | `https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/README.md` | `23411dbfd8b409d433f984a5d6677830e86a383ec76935fc1e1d675e6b4374dd` (427 lines) | `55-56` act rule; `65-68` "does not use sysrq-trigger"; `148-149` "every action is logged to stderr"; `234-238` defaults; `383` v1.2 removed the kernel-oom option |
| earlyoom `MANPAGE.md` (tag v1.9.0) | `https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/MANPAGE.md` | `cc48b02e79255ae27bad9b2c49364fcae1b6b5eb20fe8e83ecef432f360dfeda` (288 lines) | `31`, `45`, `56-57` defaults (10 %, kill = PERCENT/2) |
| earlyoom `main.c` · `README.md` (upstream master) | `https://raw.githubusercontent.com/rfjakob/earlyoom/master/{main.c,README.md}` | `baeb78a6e45037ba17901b6897b780f3997687db61d23c7811b424fa99264370` · `b2a34e354d122fd756672a1a4014ec5382144e41451291c9d84fd6458c30826c` | `main-now.c:202` `--kernel-oom` long option exists on master; `README-now.md:69` mentions it |
| systemd `catalog/systemd.catalog.in` (tag v262) | `https://raw.githubusercontent.com/systemd/systemd/v262/catalog/systemd.catalog.in` | `e53707db7e6963b284e504dc17f36a4d5a2bdb4bd8a9611b2cf95c075ad86592` | `604` kernel-OOM unit notice `fe6faa94…`; `884-885` oomd notice `d989611b…` |
| systemd `src/oom/oomd-util.c` (tag v262) | `https://raw.githubusercontent.com/systemd/systemd/v262/src/oom/oomd-util.c` | `2e94450aa337dd7d2062f2730e46e22ac00fc2c3195c11654047ddcaba487e7a` | `269-271` `user.oomd_ooms` before the kill; `274`, `280`, `289` kill paths; `305-308` `user.oomd_kill` after the kill |

No browser, no bot challenge, no access control was used; every fetch above is a plain `curl` of a
public raw URL.

---

## 8. Tooling record

**No install or upgrade was performed** by this seat. The work needed only repository reads, read-only
`git`, ordinary `curl` fetches of public upstream files, `journalctl`/`systemctl` reads on this host,
and the pre-existing `python3` (3.14.8) / `git` (2.56.0) / `jq` / `sha256sum` / `curl` toolchain.
No `pacman` transaction was run — the round-wide pacman freeze is untouched — and no host service was
started, stopped, enabled or restarted. The `git clone --depth 1` I made lives in scratch
(`/fast/scratch/hyaku/mori-r26/DraftSkillFr10/shallow`), never in the lane.

## 9. Deliverables

(a) decision rows "Did a userspace killer act?" → §2.2 (paste-ready table), §2.3 (coverage).
(b) error patterns (thresholds from the config file; `oom_kill=0` while earlyoom is active; lines from
a previous invocation) → §3.2 (paste-ready rows), §3.3 (coverage).
(c) gate-registry rows for `tools/mori-oom-killers.py`, `tools/mori-routed-r24.py`,
`tools/mori-job-runway.py` → §4.1-§4.3 (paste-ready rows), §4.4 (measured inputs/verdicts/exits).
Grounding → §1 (provenance), §7 (sources, sha256), inline citations in every row. Conflicts → §6, six
items, open. Handoffs → §5, six items, open. All three drafts are unlanded.

No file in the lane repo other than this report was created or modified.

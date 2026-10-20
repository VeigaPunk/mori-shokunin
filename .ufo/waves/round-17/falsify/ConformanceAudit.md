# ConformanceAudit — round 17 wave 2 falsification of wave-1 build seat reports

Seat: `MoriR17.ConformanceAudit-4` (leaf member; no subagent dispatch).
Date: 2026-10-20. Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin` (entering tip `24526ea`).
Advisory only. I do not judge admission; L1 `MoriR17` owns the verdict.

## Attacked scope (stated exactly)

- Attacked: all 71 files under `.ufo/waves/round-17/build/` (`*.md`, `*.json`, `*.txt`). Each was
  swept by regex for eight conduct classes (tool install, `/tmp`, background job, live journal,
  fleet-root write, lane jj/git mutation, credential or transcript-field display, network). Hits
  were filtered for negation (`no`, `not`, `none`, `never`, `forbidden`), then every non-negated
  hit was read in context. About 25 reports were read in full or in the cited ranges.
- Not attacked: transcript files, `/var/log/pacman.log`, journals, lane op logs, credential files.
  Host and transcript facts below are cited from the wave-1 reports or from `corpus/lessons/round-17.md`.
  I did not re-observe them. Each such claim is marked as cited or `[INFERENCE]`.
- No blanket pass is claimed. Categories with zero observed violations are listed in §5 with the
  exact sweep that found nothing.

## Method and tool record (no installs)

- Tools used: `read`, `glob`, `grep`, and stdlib Python through `eval` over the local report files
  only (regex sweeps and line counts). No command was run in the lane, the fleet root, a clone, or a
  transcript store. No `/tmp` write. No background job. No journal query. No network fetch.
- Tool installs or upgrades by this seat: **none**.
- Credential files and credential values: not opened and not read. Where a report quotes a
  credential-adjacent field name, I cite the path and line only.

## 1. Violations disclosed or observed, by seat and path:line

Status key. **D** = disclosed by the seat itself. **L1** = recorded by the L1 lesson. **C** = cited
from another report. **I** = my inference from report text (not verified by me).

| ID | Sev | Seat (report) | Path:line | Conduct | Status |
|---|---|---|---|---|---|
| V1 | high | `MoriR17.ReviewSkillRows-5` (`ReviewSkillRows.md`) | `:37-38` | Lane jj reads run as `jj -R <lane> status`, `jj -R <lane> diff --stat`, `jj -R <lane> diff --git`, without `--ignore-working-copy`. L1 says this snapshotted the lane working-copy commit, creating op `45a25744584d` at 15:55:07. The branch did not move. | L1 (`corpus/lessons/round-17.md:73`, M8). The seat's own text says "successful reads" (`:37-38`). |
| V2 | high | `MoriR17.JjGate-5` (`JjGate.md`) | `:296-314` | Before the L1 guard, ad hoc jj and git writes ran in `.scratch/exp/repo`, `.scratch/exp2/lane`, `.scratch/exp3/lane`: `jj git init --colocate`, `jj commit`, `jj metaedit --update-author`, `jj bookmark set master`, all without `-R`. Two gate runs (`out-entering`, first `out-c2`) also ran `jj git init --colocate` with no `-R` on follow-up calls (`:312-314`). | D |
| V3 | high | `MoriR17.SentinelTranscripts-5` (`SentinelTranscripts.md`) | `:29-33` | A lane grep (`credential_pin\|errorMessage\|stopReason`, gitignore off) matched the lane-resident copy `.ufo/interactive-sessions/20261015T050057Z/*.jsonl`. The seat displayed one `credential_pin` record line and "content lines". Values were not copied, per the seat. The copy remains in the lane (`:195-201`, F11). | D (also L1 M9, `round-17.md:74`) |
| V4 | high | host; actor not a round-17 seat (`PacmanActorTrace.md`, `PacmanTxnToday.md`) | `PacmanActorTrace.md:12-13, 36-44, 109-112`; `PacmanTxnToday.md:79-82, 18-20` | `pacman -Syu` at `/var/log/pacman.log:2462` (09:15:30, 448 actions, incl. boot-chain packages). PacmanActorTrace attributes it to one OMP bash tool call in session `-Documents-nvhelpme`, by identical stream content and a shared systemd invocation UUID. PacmanTxnToday places it after the host-pause ruling, which it dates to no later than 05:35:41. The 13:23:08 `pacman -U zcode` (`:3161`) was run by `yay` as `vgpnk`; no OMP log ran it (`PacmanActorTrace.md:14-17`). | C (cited, not re-observed). Contested: `OverlapTsukuroi.md:93-94, 109-111` says the operator-scope pause "was not operative (13 operator pacman runs)" and "both statements are true in their scopes". The seat behind the OMP call is `[INFERENCE]` (`PacmanActorTrace.md:109-110`). |
| V5 | medium | `MoriR17.JjGate-5` | `JjGate.md:16, 324-328` | One mistaken shell redirection wrote a 237-byte `/tmp/does-not-exist`, removed after capture. | D |
| V6 | medium | `MoriR17.CensusJj-5` (`CensusJj.md`) | `:105` (run listed as "entering file, before edits"); `:118-119` | This run used `TMPDIR="$PWD/.scratch"` on the entering census. `CensusGitSites.md:353-357` states the entering file's selftest uses absolute `mktemp -d /tmp/mori-census-selftest.XXXXXX` and ignores `TMPDIR`. So that run wrote a transient `/tmp` directory, removed by the trap (`CensusGitSites.md:360`). The seat checked `/tmp` only for the post-fix run (`:118-119`). | I (the run is cited at `:105`; the `/tmp` write follows from `CensusGitSites.md:353-357`; not disclosed by the seat) |
| V7 | medium | `MoriR17.MisrootSweep-5` (`MisrootSweep.md`) | `:81-82, 231-233`; mutant runs `:113-134` | (a) The selftest runs `git init/add/commit` in a throwaway sandbox under `TMPDIR`. `wave1-context.txt` (line 5) says "never git add/commit… anywhere" and reserves git/jj writes to "the JjGate executor's gate… inside sandboxes it creates". (b) Four mutated copies of the tool were written under `.scratch` and run (`:113-134`). The wave allows an executor "only its own item's selftest". | D (both). The seat's "no VCS mutation" statement (`:231`) is narrower than the rule. |
| V8 | medium | `MoriR17.SessionExitCorrelation-5` (`SessionExitCorrelation.md`) | `:29-31`; results `:36-41`; method `:33-34` | Reads `customType == "session_exit"` records and reports values of `data.reason` and `data.kind` (`normal`/`dispose`). Those are outside the allowlist (`customType` only). The contract says `custom` records are "skipped unread". The seat also ran a full-file parse (`:33-34`). | D ("data.reason, data.kind only", `:31`). Compare the seat's own claim at `:128`: "no … non-allowlisted field was read or printed". |
| V9 | medium | `MoriR17.OmpRetryConfig-5` (`OmpRetryConfig.md`) | `:7` (claim); `:151-160` | Reports text values of `retryRecovery.note` and `retryRecovery.recovery` (`:158-160`) and model strings from `model_change` records (`:151-157`). Those are beyond the permitted "retryRecovery key shape" and beyond the `message.model` allowlist. It also read line ranges of `~/.omp/agent/config.yml` (`:36-52`). No credential line appears in the report, but raw config lines (`:94-209`) were read. | D (partly: "canned note/recovery values"). |
| V10 | medium | `MoriR17.DeadSeatCrossCheck-5` (`DeadSeatCrossCheck.md`) | snippet `:46-47`; claim `:136` | The snippet calls `json.loads` on every line of every file, including `credential_pin` lines. The report states those records were "skipped unread". Parse-then-discard is a read into memory, so the claim is not accurate. The snippet does not print field values. | I (claim vs snippet text; no output of credential content observed) |
| V11 | medium-low | `MoriR17.PacmanActorTrace-5` (`PacmanActorTrace.md`) | `:37-40, 74-76` (content heads); `:95-99` (`~/.bash_history`); `:97-98` (`wtmp`); `:100-102, 149-152` (`sudo -n`) | Printed heads of OMP session tool logs (`125.bash.log`, `59235`) under `~/.omp/agent/sessions`. The seat is not assigned transcripts, but this is the transcript store. It read shell history and login records, and ran privileged `sudo -n` reads of `/var/log` and `/etc/sudoers*`. Read-only, no install, no journal query (`:3-5`). | D (reads listed in `:131-155`). Scope ruling needed. |
| V12 | medium-low | `MoriR17.SentinelJjSandbox-5` (`SentinelJjSandbox.md`) | `:202-204` (lane jj call); `:32` (raw `cat` of user jj config); `:54-55` (its own claim that "even a read such as `jj log` snapshots the lane") | Ran `jj config path --repo -R <lane>` against the live lane without `--ignore-working-copy`. `JjEnvFacts.md:62-67` says that command uses the forcing loader, which creates config-id and directories when they are missing, and `JjEnvFacts.md:155` calls running it "forbidden". The seat's only evidence of no write is an mtime comparison (`:203`). V1 shows mtime-level evidence can miss an operation. | D ("this was the only jj command", `:204`). |
| V13 | low-medium | `MoriR17.RetryRecoveryShape-5` (`RetryRecoveryShape.md`) | `:63-64, 78` | Reports the value histogram of `attempt` and the min/max range of `supersededBy.timestamp`. The seat's own rule is "key shape" and "cardinality only" (`:22-26`). Numeric value ranges go beyond that. | D (`:26` states cardinality only). |
| V14 | low | `MoriR17.ReviewCarryForward-5` (unnamed; `ReviewCarryForward.md`), `MoriR17.ReviewC1Metric-5`, `MoriR17.ReviewC2Metric-5`, `MoriR17.CriticFrontier-5` | `ReviewCarryForward.md:29-31`; `ReviewC1Metric.md:77`; `ReviewC2Metric.md:53`; `CriticFrontier.md:161` (fleet root) | `git status` run without `GIT_OPTIONAL_LOCKS=0`, against the lane, worktree clones and the fleet root. Read-only in intent. `[INFERENCE]`: plain `git status` can refresh `.git/index`. Compare `FleetRootUntracked.md:12`, which sets the env. | I |
| V15 | low | several (see §4) | see §4 | Network fetches: `CriticFrontier.md:130,169`; `JjEnvFacts.md:167-168, 177-192` (includes a crates.io tarball, storage path not stated); `SentinelJjSandbox.md:205` (stdout only); `SrcZaiErrorCodes.md:13-14`; `SrcRfc6585.md:20`; `SrcGitSymbolicRef.md:10`; `SrcPacmanLog.md:7-8`. The wave context I read has no network clause, so these are not violations on their face. | I (listed for L1; `JjEnvFacts` crate output location is `[UNKNOWN]`) |

Host-level events cited in the reports and not attributed to a round-17 seat:
- `pacman -Sw --cachedir /tmp/pkgcheck …` at 08:20:52 (`/var/log/pacman.log:2461`), which writes to `/tmp`. Actor unknown. Cited at `PacmanTxnToday.md:38, 99, 128-129` and `OverlapTsukuroi.md:38`. The seat rule against `/tmp` applies to seats, so this is out of scope for them.
- `pacman -U zcode` at 13:23:08 (`:3161`), run by `yay` (see V4).

## 2. Historical round-16 disclosures re-cited in round-17 reports

These are round-16 conduct, cited as evidence. They are not round-17 seat conduct. Listed so L1 can
separate them from V1–V15.

- Background job `bg_2667`, `/tmp/.probe_null`, `/tmp/.x`, live system-journal probes: `MisrootR16Facts.md:38-46`, `:165-167`; `R16LessonM7.md:25, 32, 40, 47-50, 65`; `LessonMistakesDraft.md:13, 22`; `QualityCriteriaDraft.md:41`. Covered by L1 lesson M2 and M7.
- Fleet-root write of `MoriR16.Lesson` (847 bytes): `MisrootR16Facts.md:9, 24, 48`; `LessonMistakesDraft.md:12`; L1 lesson M1 (`round-17.md:66`).
- Breach ledger M7–M30 (`/tmp` writes, background jobs, live journal queries, `curl` to files): `ReviewSeatBreachDetect.md:46-53`.

## 3. Compliance claims versus observation, by seat

| Seat (report) | Claimed compliance | Observation | Verdict |
|---|---|---|---|
| `ReviewSkillRows-5` | "No VCS mutations were performed" (`:41`) | Lane jj reads without the ignore flag; L1 records a working-copy snapshot op (`:37-38`; L1 M8) | Mismatch (V1) |
| `JjGate-5` | "all git/jj writes were fixture commits inside throw-away sandbox repos the gate creates" (`:17-19`) | Pre-guard ad hoc writes outside the gate (`:296-314`, self-disclosed) | Mismatch (V2) |
| `JjGate-5` | "No probe outputs, downloads or scratch were written to /tmp" (`:326-328`) | Accidental `/tmp` file (`:324-325`, disclosed) | Mismatch, disclosed (V5) |
| `SentinelTranscripts-5` | "I printed no content, errorMessage text, usage, credential, hash, or responseId value" (`:26`) | Displayed one `credential_pin` line and content lines (`:29-33`) | Mismatch, disclosed (V3) |
| `SentinelTranscripts-5` | "credential_pin lines skipped by raw prefix before parsing" (`:21`) | Consistent with `:21`; the displayed line (`:31`) was a separate, earlier grep | Consistent with its own method; V3 stands |
| `SessionExitCorrelation-5` | "no … non-allowlisted field was read or printed" (`:128`) | `data.reason` and `data.kind` read and reported (`:29-31`, `:38-41`) | Mismatch, disclosed in `:31` (V8) |
| `OmpRetryConfig-5` | "field-limited … no content read" (`:5-7`) | `retryRecovery` text values and `model_change` strings reported (`:151-160`) | Partial mismatch (V9) |
| `DeadSeatCrossCheck-5` | "credential_pin … skipped unread" (`:136`) | Snippet `json.loads` every line (`:46-47`) | Mismatch (V10) |
| `MisrootSweep-5` | "No VCS mutation in the lane, fleet root, or my clone" (`:231`) | True for those three locations. Sandbox `git init/add/commit` is outside the gate exception (V7) | Narrow claim, rule deviation |
| `CensusJj-5` | "no `/tmp` selftest directory survives" (`:16-17`) | Consistent for the fixed run; the `:105` run wrote `/tmp` transiently by code (V6) | Unclaimed transient write |
| `SentinelJjSandbox-5` | "this was the only jj command, and it should not be repeated" (`:204`) | Accepted as the only lane jj call; compliance rests on mtime only (`:203`) | Partial (V12) |
| `PacmanActorTrace-5` | "No journal query… No VCS mutation… No tool installed" (`:3-5`) | Consistent for those; session content displayed and `sudo -n` reads (`:37-40, 100-102`) | Consistent for the claims; scope issue (V11) |
| `TranscriptShapes-5`, `CriticHarm-5`, `CriticC1-5`, `SeatNaming-5`, `TranscriptTailBounds-5`, `ReviewC1Contract-5`, `RevengerOmpTerminal-5` | Field allowlist followed; counts only | Read the allowlisted fields as cited. Reported values are counts, class names, provider/model strings and `customType` | Consistent with the claim; I did not open transcripts to verify |

## 4. Network and external fetches (listed for completeness)

`curl` or `read` of external URLs by source and critic seats: `SrcRfc6585.md:20`;
`SrcZaiErrorCodes.md:13-14`; `SrcGitSymbolicRef.md:10`; `SrcPacmanLog.md:7-8`;
`CriticFrontier.md:130,169`; `JjEnvFacts.md:167-168, 177-192`; `SentinelJjSandbox.md:205`;
`KnowledgeSeatTerminal.md:24` (recheck command only, not run). Most write to stdout or to
`/dev/null` (`SrcZaiErrorCodes.md:13`). The `JjEnvFacts` crate download storage path is not stated.

## 5. Categories with no observed violation (exact sweep)

- **Tool installs or upgrades (round-17 seats):** no `pacman -S/-U/-R/-Sy/-Syu/-Sw`, `uv tool`,
  `pip install`, `npm -g`, `cargo install`, `apt`, `npx`, `uvx`, `brew`, `go install`, `snap`,
  `flatpak`, `docker` run by a round-17 seat. The only `pacman` text is host-log citation. Every seat
  that mentions installs states "none". `RevengerOmpTerminal.md:37` shows `go` missing (exit 127), not installed.
- **Background jobs:** no `bg_N`, `nohup`, `disown`, or unattended `&` in a round-17 seat command. The
  matches are negated or are r16 citations (§2).
- **Live journal calls:** none by round-17 seats. `journalctl --version` appears only as a receipt
  citation (`ProvinceFrontier.md:43, 223, 233, 277`, from `.ufo/waves/round-16/runtime-versions.json`).
  `systemctl --version` (`ProvinceFrontier.md:28, 242`) is not a journal query. `journalctl` appears in
  `CensusGitSites.md:290, 361, 464` and `JjGate.md:71, 106, 112` only as stub or override names.
- **Fleet-root writes:** none by round-17 seats. Every fleet-root path in the sweep is a read
  (`MisrootSweep.md:140-143` and `FleetRootUntracked.md`). `MisrootSweep` ran its tool with `--fleet-root` read-only.
- **Lane git mutations (add, commit, stash, checkout, switch, reset, pull, push):** none against the
  lane. Sandbox writes are V7 and V2.
- **Selftests:** run inside own clone with `TMPDIR` set: `SeatGate.md:113`, `SeatTool.md:70`,
  `ContextCheck17.md:65`, `CensusJj.md:109`, `MisrootSweep.md:72`. The census selftest was not run
  where not permitted (`CensusConsumers.md:51`).
- **jj with the ignore flag:** `HelperFailureWindows.md:22-29` uses `--ignore-working-copy` on every jj call.

## 6. Findings that bear on L1 admission (not verdicts)

1. **V1 and V2 are the two confirmed lane-jj-discipline violations.** V1 is recorded by L1 (M8).
   V2 is self-disclosed. Neither moved the lane branch. L1 must decide whether either affects C2
   evidence. The C2 gate runs in gate-created sandboxes (`JjGate.md:81-95`), so V2 does not
   contaminate the measured C2 receipts on the face of the report, but its experiments were not
   reproduced under the gate.
2. **V3 is a credential-class display.** The seat says no values were copied. The lane still holds
   the transcript copy (`SentinelTranscripts.md:195-201`). L1 M9 records it.
3. **V4 is a host-level pause violation whose attribution is contested.** Tsukuroi's "pause not
   operative for operator" claim (`OverlapTsukuroi.md:93-94`) is the counter-observation. It does not
   change that a full upgrade ran after the ruling. The seat behind it is `[INFERENCE]`.
4. **V6 is an undisclosed transient `/tmp` write.** It is inferred from code, not from an observed
   directory. It was cleaned by the trap, and it sits in a run the seat did describe.
5. **V7 and V8–V12 are rule-scope deviations** under the field-allowlist and sandbox clauses of
   `wave1-context.txt`. Each is self-disclosed or cited. They need an L1 ruling, not a re-run.

## 7. Limits

- I did not re-observe any host log, journal, op log, or transcript. Items cited from reports are
  marked as cited.
- Regex sweeps and negation filters can miss a violation phrased without the listed verbs. Coverage
  is "pattern sweep + reads of the cited ranges", not a full read of every report.
- The seat-to-file mapping uses the `Seat:` header where present. Twelve reports carry no seat id,
  so they are identified by file stem (`ContextCheck17`, `JjEnvFacts`, `ReviewCarryForward`,
  `ReviewC1Metric`, `ReviewC2Metric`, `SrcPacmanLog`, `SrcRfc6585`, `SrcGitSymbolicRef`,
  `LiveLaneHeadVsBranch`, `FleetRootUntracked`, `SkillRegistry`, `PacmanTxnToday`).
- This report is advisory. No judgment of any claim, no edit to any report, no edit to the lane, the
  fleet root, a clone, or a sibling file.

## Trailer

Scope: round-17 build seat reports (71 files), read-only.
Tool installs/updates by this seat: none.

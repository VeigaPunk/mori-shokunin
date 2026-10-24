# Round 27 wave 2 — privacy sweep of the landed diff (ReviewPrivacyLanded)

Seat: MoriR27.ReviewPrivacyLanded, 2026-10-22. Scope: every file in
`git -C <lane> diff --name-only fc09f96c 5f00fd045c137b7e3835506d69946cfd9d010eb5` (56 files, saved with the full
7,606-line diff under `/fast/scratch/hyaku/mori-r27/ReviewPrivacyLanded/`). Searched classes: uid digits in unit
names, uid numbers, pids, command lines, journal `MESSAGE` text, `/etc/default/earlyoom` and
`--prefer`/`--avoid`/`--ignore` values, OMP settings values, session ids and session-store paths. Method: class
greps over all 56 paths at the tip rev, plus an added-lines-only (`^+`) pass over the whole diff so inherited
lines are separated from what this round introduced, plus full reads of the four committed evidence files, the
five committed scripts, and the four wave JSON files. No value of any forbidden class is reproduced in this
report; locations only. Round-27 privacy clause: `.ufo/waves/round-27/contract.md:38-40`.

## Retention gate (frozen scan)

Command (as assigned, run from the lane root), at both revs:

```
python3 -I -B tools/mori-retention-gate.py scan --repo <lane> --rev <rev> \
  --policy .ufo/waves/round-18/frozen/c1-policy.json \
  --allowlist corpus/evidence/retention-allowlist.json
```

- Landed tip `5f00fd045c…`: `"metric": 4`, `"routed": 0`, `"warnings": []`, `"non_author": 5`, exit 1.
- Entering tip `fc09f96c…`: `"metric": 4`, `"routed": 0`, `"warnings": []`, `"non_author": 5`, exit 1.
- The unallowlisted set is byte-identical at both revs: 4 lines, all classes R2/R5/R6/R8, all in the single file
  `.ufo/waves/round-20/falsify/NoHarmRun/rg/.ufo/waves/round-18/frozen/c1-policy.json` (the round-20 no-harm
  clone of the policy file). Nothing the round added is unallowlisted.
- Verdict: **metric 4 at the tip = base 4 at `fc09f96c`; the contract's no-harm ceiling is met**
  (`.ufo/waves/round-27/contract.md:63-66`). The exit code 1 is the scan's report-findings behaviour at base
  too, not a round regression. `non_author` is 5 at both revs, unchanged.

## Findings by severity

### High

None. No file added by this round carries a value in any searched class.

### Medium

None.

### Low

1. **Inherited uid-digit unit name inside a changed file — `corpus/knowledge/userspace-oom-killers-r26.md:144`.**
   The line embeds the operator's uid digits in `user@<uid>.service` and `user-<uid>.slice` unit names (redacted
   here as `user@UID.service`, `user-UID.slice`). It is **not this round's addition**: the class pattern matches
   the same single line at the entering tip (`git grep -c` at `fc09f96c` on this file → 1; at the tip → 1), and
   zero added diff lines match the pattern. It predates round 27 and is covered by the round's own disposition:
   the lint is prospective because 358 lines in 118 tracked files carry the pattern from earlier rounds, and
   "whether to rewrite those files or their history stays with the operator" (`corpus/lessons/round-27.md:50-54`,
   M3); the new lint that would catch future instances is `corpus/QUALITY.md:380` with the dispatch-side rule at
   `:382`. Report-back only; no action available to a seat.

2. **Host provenance digests of two system-unit files — `.ufo/waves/round-27/w1/HostUnitOomAdjust.md:28` and `:78`.**
   Each cites a `FragmentPath` (`/usr/lib/systemd/system/earlyoom.service`, `/usr/lib/systemd/system/user@.service`)
   with its sha256. These are digests of distro unit files, not of the operator's earlyoom environment file, whose
   digest the seat's own privacy plan explicitly withheld (`CriticPrivacyPlan` table: "low-entropy digest of a
   settings file — withheld, differs=yes/no only"); the committed report honours that: the env-file check is
   recorded as "the host file differs from the packaged one on all three tests (mtime, size, checksum)" with no
   digest (`HostUnitOomAdjust.md:153`). Not in a forbidden class; recorded so the L1 knows host-file digests are
   in the round's committed bytes by design. Lines `:171-173` are digests of public upstream sources (gate
   blocks) — unremarkable.

3. **Two host drop-in filenames and one drop-in setting disclosed — `.ufo/waves/round-27/w1/HostUnitOomAdjust.md:79-80`.**
   The report names two `user@.service` drop-in files on this host (one under `/usr/lib/systemd/system/...`,
   one under `/etc/systemd/system/...`) and states the `/etc` one "contains only `TimeoutStopSec=5s`". This is
   host configuration fingerprinting outside the sweep's forbidden classes (not a uid, pid, command line,
   journal text, earlyoom value, OMP settings value or session id). Deliberate, value is a systemd knob, and the
   report checks neither drop-in touches OOM. Informational.

## Clean-class evidence (what was searched and what came back)

| Class | Tip-wide hits in the 56 files | Added by this round | Note |
|---|---|---|---|
| uid digits in unit names | 1 line (`userspace-oom-killers-r26.md:144`, inherited, finding 1) | 0 | every other occurrence in the round's files is the literal placeholder form `user-UID.slice` / `user@UID.service` (e.g. the redacted cgroup path in `HostUnitOomAdjust.md`, where the seat pasted `sed -E 's/[0-9]+/N/g' /proc/self/cgroup` output) |
| uid numbers (`uid=`/`uid:` forms) | 0 | 0 | only `uid 0` / `_UID=0` root constants in upstream-doc citations (`ReviewEntryOomdFacts.md`, `SrcKillCSelection.md`) |
| pids | 0 real values | 0 | all hits are upstream code placeholders (`%d`, `pid <= 2`, `PID 1`), count statements ("`distinct_victim_pids=39`" is a count, not a list), or `/proc/<pid>/` path templates; added-lines check for `(pid\|PID\|MainPID\|_PID)[= :][0-9]{2,}` → 0 |
| command lines | 0 | 0 | `HostUnitOomAdjust.md` records commands unexpanded ("`$(id -u)` stays literal; no `set -x`"); the only `cmdline "` strings are the upstream earlyoom send-line format literal (public source) and the dispatch prompt's grammar placeholder |
| journal `MESSAGE` text | 0 host text | 0 | the only `MESSAGE=` context added is the upstream `logs-show.c` citation in a `source:` line; the capture scripts read `MESSAGE` in memory and print aggregates only (`boot-send-classes.py:4,32-41`); `ScoutDeadSeatCorrelation.md` carries a cause class and timestamp with the session id explicitly omitted |
| `/etc/default/earlyoom` and `--prefer`/`--avoid`/`--ignore` values | 0 host values | 0 | every quoted `EARLYOOM_ARGS`/flag expression is upstream bytes (v1.9.0 `earlyoom.default:5`, README example, Arch PKGBUILD presence-only statement in `CriticC1Novelty.md`); host side is presence-only ("**none literal** — the argv is the binary plus the environment expansion", `HostUnitOomAdjust.md`) |
| OMP settings values | 0 | 0 | the committed entry and SKILL name "the operator's OMP settings file" only (7 mentions in `harness-job-capacity-r25.md`, none with a value; the applied text says "sets a value above the clamp" without the value); the redaction placeholder `«OMP-SETTINGS-VALUE»` appears only as a placeholder in 4 drafted old→new lines in `.ufo/waves/round-27/w1/ReviewR3SkillRows.md`; no model/route identifiers in any added line |
| session ids / session-store paths | 0 | 0 | zero UUID-shaped or `sess_`/store-path hits; `CriticPrivacyPlan.md:147` writes the generic pattern `session-N.scope` (a raw-digit `session-[0-9]+\.scope` count in that file is 0); `SKILL.md` tmux rows carry count shapes only (`sessions=N relevant=R foreign=F`) |

## Per-area verification notes

- **Evidence files** (`.ufo/waves/round-27/evidence/`): `boot-send-classes.txt` and `oom-score-classes.txt`
  carry only counts, class labels, score/RSS min-median-max, adj-value histograms and UTC hour histograms —
  matching their scripts' printed promises (`boot-send-classes.py:4-5`, `oom-score-classes.py:4`). No pid, no
  name outside the fixed class list, no uid, no command line. `c1-before.txt` / `c2-before.txt` are counter
  outputs. The `uid_class={'operator': 39}` label is a class label, not a uid number.
- **Wave JSONs**: key inventories — `wave1-dispatch.json` (`context`, `tasks[]{agent,name,solutionSpace,task}`),
  `wave1-run.json` (`compaction.*`, `counts.*`, `policy.*`, `registry.members.<Seat>.{agentId,item,kind,role}`,
  `registry.path/reportDir/schema`, `taskCall`, `wave`), `wave1-spec.json` (`items[]{name,prompt,role}`,
  `maxLanes`, `reportDir`), `w1/swarm-registry.json` (`members…`, timestamps, `schema`). `agentId` values are
  seat agent names; `policy.*` values are lane wave-policy numbers with `policy.source: "config"`; no session
  ids, no model or route values anywhere. Corroboration: the frozen scan's R-class flagged the round-25 run
  JSONs but no round-27 JSON.
- **Scripts** (`check-row-identity.py`, `count-c1.sh`, `count-c2.sh`, both evidence scripts): the only absolute
  paths are lane paths (`/home/vgpnk/Projects/shokunin/mori-shokunin`) and journalctl invocations; no host
  values hardcoded.
- **Round-26 backfill files** (`OperabilityNoHarm.md`, `ReopenS116S117.md`, `ReopenS118S119.md`,
  `ReviewEntryOomdFacts.md`): the M1/M3 redactions hold at the tip — zero real-digit unit-name or pid hits in
  any of them; `ReviewEntryOomdFacts.md` states its host reads printed "key names and no values", and its one
  pid-class statement is the corrected wording "no pid is stored" about oomd's counters.
- **QUALITY 80-82**: the committed criteria include the prospective lint
  (`corpus/QUALITY.md:380`: `grep -nE 'user-[0-9]{3,}\.slice|user@[0-9]{3,}\.service|\bpid[ =:]*[0-9]{3,}|\buid[ =:]+[0-9]{3,}' <files>`
  before committing, redact host-value hits) and the dispatch rule ("a dispatch prompt never asks a seat to list
  unit names, pids or uids", `:382`). This sweep applied both patterns plus the wider class set above, and
  confirms the round's additions pass.

## Residual risk

- The frozen policy calls its own classes "a recall floor, not a privacy proof"
  (`corpus/lessons/round-27.md:50-52`); classes outside its grammar (host drop-in names, unit-file digests,
  finding 2-3) pass it by construction and were caught here only by manual reading.
- The sweep is pattern-class based plus targeted full reads; it is not a semantic read of all 7,606 diff lines.
  Prose that mentions no digit can still name a host fact; findings 2-3 are exactly that shape.
- The inherited uid line (finding 1) remains in the tree; per M3 the rewrite decision is the operator's.

## Verification gaps

- None blocking. Every searched class is reported with its count; the one ambiguity class (bare digit runs that
  could be uids/pids) was resolved by raw-byte counts (`grep -c` on unmasked patterns) rather than inference.
- I did not re-run the wave-1 sources or the C1 counter; out of scope for this seat.

## Tooling record

No tool installed or upgraded; the sweep used preinstalled git, grep, sed, awk, python3 (stdlib only). No pacman,
uv or binary downloads. Scratch artifacts (changed-file list, full diff, HostUnitOomAdjust extract) are under
`/fast/scratch/hyaku/mori-r27/ReviewPrivacyLanded/`.

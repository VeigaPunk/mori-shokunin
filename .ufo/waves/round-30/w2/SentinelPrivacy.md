# SentinelPrivacy — privacy and retention attack on round 30 (ad0f047)

**Verdict: agree with the number, disagree that it means much, and one defect found.** The retention metric at
`ad0f047` is **4**, equal to the base at `58b61681`, with **zero new population hits** and **zero new allowlist
rows** — but the frozen gate has **measured recall 0** on every host-specific class this round's surface introduces,
and the command exits **1** at both revisions, so neither "4" nor exit 0 alone can carry a privacy claim here.

Severity: **MEDIUM** (measurement validity of the only counted privacy instrument), **LOW** on the committed bytes
(reading sweep found no host value). Nothing I found is exploitable by a reader of the repo; the exposure is that
the lane's own clearance story would not have caught one.

## Axes

1. Does the frozen metric rise? 2. Does the metric see what round 30 exposed (unit timestamps, send lines, unit
   names, journal fields, earlyoom args)? 3. Did the committed bytes copy a host value? 4. Is any clearance claim
   fabricated?

## A. The measured metric (item as assigned)

```
$ cd /home/vgpnk/Projects/shokunin/mori-shokunin && python3 -I -B tools/mori-retention-gate.py scan \
    --repo /home/vgpnk/Projects/shokunin/mori-shokunin --rev ad0f04745ced2194e58c22a0d6b38131bee3e230 \
    --policy .ufo/waves/round-18/frozen/c1-policy.json --allowlist corpus/evidence/retention-allowlist.json
metric 4  routed 0  non_author 5  finding RETENTION_FINDINGS  warnings 0   exit 1
unallowlisted: .ufo/waves/round-20/falsify/NoHarmRun/rg/.ufo/waves/round-18/frozen/c1-policy.json
               lines 8 (R2), 11 (R5), 12 (R6), 14 (R8)
```

Same command at the base, compared as sets: **base hits 113, tip hits 113, added 0, removed 0, base metric 4,
tip metric 4, exit 1 at both.** Round 30 changed no tracked blob that the policy matches, and the allowlist file is
untouched in the range. So the assigned claim ("base is 4, must not rise") **holds exactly**.

Metric semantics, from the committed gate: `metric = len(unallowlisted_hits)` over non-`non_author` paths
(`tools/mori-retention-gate.py:267`), and `exit_code = 1` whenever that is non-zero (`:288`). The 4 are a
round-20 falsify scratch copy of the frozen policy itself (repo-internal regexes, no private value), inherited
since round 20, `routed 0`. They are not a round-30 regression and this round did not clean them.

## B. F1 (MEDIUM) — the metric is blind to round 30's entire exposed surface

The frozen classes are R1–R9: session-name/UUID prefixes, session-store paths, numbered tool-output names, personal
`Documents` paths, shell history, the privileged-config file name [L1 redaction: retention class R6], operator config files/keys, routing-table key names, session-record
field names (`.ufo/waves/round-18/frozen/c1-policy.json:7-15`). The policy says so itself: "Regex classes are a
recall floor, not a privacy proof" (`:29`).

Round 30's new surface is exactly the other thing: unit names, `ActiveEnterTimestampMonotonic` values, earlyoom
send lines carrying process id/uid/cmdline, journald suppression text, `/etc/default/earlyoom` arguments. **Probe,
measured in a sandbox clone at base `58b61681`** (`/fast/scratch/hyaku/mori-r30-w2/MoriR30.SentinelPrivacy/repo`,
commit `cdf378b`, one synthetic file, invented values only):

```
metric 4  finding RETENTION_FINDINGS    probe hits: []      # exit 1, same 4 inherited hits
```

The probe file held five lines, one per bounded class (a unit with a numeric active-enter stamp; a send line with a
process id, a uid and a cmdline; the per-uid user-manager unit and the per-uid slice in digit form; a journald
suppression line naming a unit; an `EARLYOOM_ARGS=` assignment). **Recall 0/5; metric unmoved at 4.** The
`RetentionBase` seat measured the same blindness for one of these tokens and reported it honestly
(`.ufo/waves/round-30/w1/RetentionBase.md:62-66`), so this is known-in-writing, not concealed.

**Exploit path.** A seat copies one real line out of `systemctl show earlyoom.service` or the earlyoom journal into
the entry, lesson, or SKILL row. The retention gate prints `metric 4` — identical to base — and the round's
no-harm condition ("not above 4") passes on a file that now carries a unit name, a timestamp, a process id and a
cmdline. Nothing in the counted path fails; only the reading sweep stands between that and the corpus. Round 30
stayed clean by author discipline (`## Not claimed`: "No host read"; `corpus/knowledge/earlyoom-invocation-scope-r30.md:123`),
not by instrument.

**Smallest remediation.** Do not edit the frozen round-18 policy (it is pinned by snapshot sha256 in
`tools/mori-retention-gate.py:27-30`). Add a second frozen policy `c1-policy-r31.json` with three classes —
(a) a unit property assignment carrying digits, (b) a per-uid manager/slice token in digit form, (c) an
earlyoom/journal field key followed by a non-zero literal — and run both in the counted condition, or make the
reading sweep a counted condition with a committed, adjudicated receipt per file class. Either keeps the existing
frozen metric intact and adds the classes the round actually touches.

## C. F2 (LOW) — one host-session-shaped token added, as instruction text

`user@<uid>`-form user-manager unit name appears three times as an **example instruction** for a leak-probe task:
`.ufo/waves/round-30/wave1-spec.json:50`, `.ufo/waves/round-30/wave1-dispatch.json:55`,
`.ufo/waves/round-30/wave1-run.json:292` ("create one synthetic file containing an upstream-source-like line such
as …"). I do not reproduce the literal here, per the lane rule on this host's user-session unit names. This is a
surface mention with no host content — adjudication rule (a) — and the gate scores it 0 (see F1). Keep or paraphrase
to a generic `<unit>` form if a stricter line is wanted; no other action justified.

## D. F3 (LOW, inherited) — the metric's floor is a policy copy, and one pre-existing host value

- The 4 unallowlisted hits are the round-20 `NoHarmRun/rg` scratch copy of the frozen policy
  (`.ufo/waves/round-20/falsify/NoHarmRun/rg/.ufo/waves/round-18/frozen/c1-policy.json:8,11,12,14`). They make
  `exit 1` structural at every tip, which is why the lane's own records say "floor4→4" and "rc1"
  (`SCORECARD.md:1345,1399`) rather than pretending a clean run.
- `SKILL.md:742` carries a host-specific `oom_score_adj_min` value. It is **present at `58b61681` and unchanged**
  (`git show 58b61681:SKILL.md | grep -c` → 1, same at `ad0f047`) — inherited, not this round's; not reproduced here.
  It is outside F1's classes too, so it survived every round's metric.

## E. What I cleared by reading, and how

Range: `git diff --stat 58b61681 ad0f047` → 73 files, +9726/−28.

Read in full: `corpus/evidence/sources-r30/S156.txt`–`S160.txt` (all five; upstream source only — systemd v262 and
the earlyoom patch, no host bytes), `corpus/knowledge/earlyoom-invocation-scope-r30.md`,
`corpus/lessons/round-30.md`, `.ufo/waves/round-30/evidence/*.txt` (census, gate, C1/C2 before/after, differential,
freeze selftests), `.ufo/waves/round-30/w1/RetentionBase.md`, the `SKILL.md` / `corpus/SOURCES.md` / `corpus/QUALITY.md`
additions, and the head of `tools/fixtures/mori-oom-killers/cases-a2-r30.json`.

Pattern sweep over all 73 changed files (revision-pinned `git grep`):

| class | result |
|---|---|
| unit-property values (`Monotonic=`, `User=`, `Group=`) | 38 occurrences, **all `=0`**; no `User=`/`Group=` at all |
| journal record fields with values (`__PID`, `_UID`, `MainPID`, `_EXE`, `_CMDLINE`, `__CURSOR`) | 0 |
| `MESSAGE=` content | only inside the synthetic fixture (see below) |
| process id / uid literals | fixture only, invented and small; percentages are earlyoom's published 10 %/5 % defaults |
| unit names | `earlyoom.service` (public), `systemd.service` (doc), per-uid template without digits, generic slice; plus F2 |
| `/etc/default/earlyoom` | 15 path mentions, **no values**; the only `EARLYOOM_ARGS` value in range is upstream's shipped default in the pre-existing S151 text (`corpus/SOURCES.md:137,157`) |
| `sudo`, `/proc/*` reads | 0 |
| host-observing commands (`systemctl`/`journalctl`/`ps`/`pgrep` as a run line in any report) | **0** — no seat ran one, consistent with "No host read" |
| OMP: session-store paths [L1 redaction: retention class R2], config-file keys, routing keys, session-record fields | 0 new (gate set identical; added-line sweep clean) |
| 10+-digit literals | 7, all accounted for: PRNG seeds in pre-existing `LOG.md:342-343` / `SCORECARD.md:264`, upstream commit times, and an oh-my-pi commit sha fragment in pre-existing S152 — **no boot id, no monotonic stamp, no epoch from this host** |

Fixture: `tools/fixtures/mori-oom-killers/cases-a2-r30.json` — invented process ids, standard first-user uids,
`fixture-process-*`/`worker`/`renderer` names, `cmdline "worker"`, round monotonic stamps (`100000`…). Synthetic per
adjudication rule (b); no host line.

Reading-sweep residual: the 35 wave-1 reports (~8 000 lines) were pattern-swept, not line-read end to end.
"[INFERENCE] a host value hidden there without one of the tokens above would be missed by both me and the gate" —
the token set covers every class named in my bounds, but it is a floor like the policy's.

## F. F4 (INFO, outside my surface) — a cited tip receipt does not exist at the tip

`SCORECARD.md:1824-1825` cites `.ufo/waves/round-30/evidence/tip-retention.txt` (with `tip-c1.txt`,
`tip-c2.txt`); `git cat-file -e ad0f047:.ufo/waves/round-30/evidence/tip-retention.txt` fails — all three are
absent from the evidence tree at the measured tip, and the SCORECARD text calls them the receipts-only last batch.
The retention claim itself is true (I re-measured 4), so this is provenance ordering, not a false claim. Flagging
for R1/tip-receipt seats; I did not chase it.

## G. Limits of this report

Not a clearance and not "clean": the metric is inherited-clean only, the instrument is blind to this round's
surface (measured), and my sweep is a recall floor. Nothing here authorises a privacy claim for round 30 or any
later round. No host unit, journal, process or setting was read or touched; the only execution was the gate (read-only
`git cat-file`/`ls-tree`) and two sandbox clones under my scratch dir. No writes outside
`.ufo/waves/round-30/w2/SentinelPrivacy.md` and `/fast/scratch/hyaku/mori-r30-w2/MoriR30.SentinelPrivacy/`.

No tools were installed or updated; none were needed (python3 and git already present).

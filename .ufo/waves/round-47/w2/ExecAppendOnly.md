# ExecAppendOnly — w2 report (round 47)

Seat: ExecAppendOnly (leaf). Lane: mori-shokunin. Task: run the SOURCES.md
rule-2 append-only gate at T with round base E; confirm `round_changed=[]`; diff
row S005 between E and T and confirm only status/used-by changed (rule 2).

Commands were run from `/home/vgpnk/Projects/shokunin/mori-shokunin` with
`TMPDIR=/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r47w2-ExecAppendOnly`.
No tool installs were needed (python3 present); nothing installed.

## 1. Append-only gate at T with round base E

Command:

```
python3 tools/mori-sources-appendonly.py 68d66ca53d89be5c34a62f46af7c37449d9f9b63 --round-base 2d85e33d14198d388fd3cda9cc15ec07e57e7a53
```

Output (key lines; full stdout captured):

```
P-C12: ... (predicate text)
changed S041 superseded_by=S206
changed S044 superseded_by=S207
changed S051 superseded_by=S208
changed S062 superseded_by=S209
changed S064 superseded_by=S210
changed S069 superseded_by=S226
changed S179 superseded_by=S211
changed S180 superseded_by=S212
changed S181 superseded_by=S213
changed S182 superseded_by=S201
changed S183 superseded_by=S214
changed S184 superseded_by=S215
changed S185 superseded_by=S216
changed S186 superseded_by=S217
changed S188 superseded_by=S218
changed S189 superseded_by=S219
changed S190 superseded_by=S220
changed S193 superseded_by=S202
appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S041,S044,S051,S062,S064,S067,S069,S070,S071,S083,S084,S090,S093,S096,S097,S101,S124,S127,S128,S129,S131,S140,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193,S226,S229,S235] round_changed=[]
supersede_timing superseded_as_of=[S041,S044,S051,S062,S064,S067,S069,S070,S071,S083,S084,S090,S093,S096,S097,S101,S124,S127,S128,S129,S131,S140,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193,S226,S229,S235] stale_supersede=[]
```

Exit code: **0**.

Verdict: **`round_changed=[]` confirmed** (and `deleted=[]` in the round too;
the 18 `ids` / 36 `superseded` are pre-round history-wide findings, not round
changes — the round-window check is `round_changed`, which is empty, and the
tool exits 0 when `--round-base` is set and `round_changed` is empty).

## 2. S005 row diff E → T

```
git show 2d85e33d14198d388fd3cda9cc15ec07e57e7a53:corpus/SOURCES.md | grep '^| S005 '
git show 68d66ca53d89be5c34a62f46af7c37449d9f9b63:corpus/SOURCES.md | grep '^| S005 '
```

@ E (2d85e33d):

```
| S005 | Linux OOM trace events — https://raw.githubusercontent.com/torvalds/linux/c03c1a14507dfaf8b856c2608f9ac216021fc222/include/trace/events/oom.h | code | A | Linux oom:mark_victim tracepoint field schema | include/trace/events/oom.h:76,82-105; Linux master commit c03c1a14507dfaf8b856c2608f9ac216021fc222 (2026-10-18) | The victim-mark tracepoint exposes PID, comm, UID, memory fields and oom_score_adj as a distinct event schema. | queued | 2026-10-19 | on-release | — |
```

@ T (68d66ca5):

```
| S005 | Linux OOM trace events — https://raw.githubusercontent.com/torvalds/linux/c03c1a14507dfaf8b856c2608f9ac216021fc222/include/trace/events/oom.h | code | A | Linux oom:mark_victim tracepoint field schema | include/trace/events/oom.h:76,82-105; Linux master commit c03c1a14507dfaf8b856c2608f9ac216021fc222 (2026-10-18) | The victim-mark tracepoint exposes PID, comm, UID, memory fields and oom_score_adj as a distinct event schema. | mined | 2026-10-19 | on-release | corpus/knowledge/oom-tracepoints-r47.md |
```

Column-by-column (header at T: id | source | kind | tier | scope | anchor | teaches |
status | opened | recheck | used-by):

| column | E | T | changed? |
|---|---|---|---|
| id | S005 | S005 | no |
| source | identical | identical | no |
| kind | code | code | no |
| tier | A | A | no |
| scope | identical | identical | no |
| anchor | identical | identical | no |
| teaches | identical | identical | no |
| status | queued | mined | **yes** |
| opened | 2026-10-19 | 2026-10-19 | no |
| recheck | on-release | on-release | no |
| used-by | — | corpus/knowledge/oom-tracepoints-r47.md | **yes** |

Verdict: **rule 2 holds** — exactly the two mutable columns `status` and
`used-by` changed (both in the tool's MUTABLE set); all nine immutable cells are
byte-identical. The used-by change names the new C2 entry
`corpus/knowledge/oom-tracepoints-r47.md`, consistent with the round's claim.

## Evidence / risks

- Evidence: exact command + output + exit code above; no files were mutated
  (run `git log`/`git show` read-only over corpus/SOURCES.md; TMPDIR confined to
  scratch).
- Risk: the gate's history-wide `ids=18`/`superseded=36` findings are pre-round
  and out of scope for this seat's check (round-window signal is
  `round_changed=[``, which passed). The S005 diff is a two-revision blob
  comparison, not a working-tree read.
- Blockers: none. No tools installed (python3 available; no pacman/uv/npm
  action needed).

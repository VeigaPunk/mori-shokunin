# Mo56CritRegistry — attack on new registry rows S544 and S545

Seat scope: attack the two new registry rows only. Freeze tip under test:
`8be2717b0809281d07dffe83dad424a4859e0747`. All reads read-only; scratch
`/fast/scratch/hyaku/mori-r56/Mo56CritRegistry/` (removed at exit). No vote
items in this wave; this report carries no vote-shaped lines.

## 1. S544 tier A — argued both ways, verdict

Row (corpus/SOURCES.md:324, verified at freeze tip):

```
| S544 | shokunin driver launch-log grammar — scripts/hyaku/inline.sh and scripts/shokunin-watchdog.sh in the fleet repo | own-work | A | the .ufo/watchdog.log line grammar under the hyaku-inline and legacy daemon drivers | inline.sh launch 149, complete 176, dead 182; shokunin-watchdog.sh launch 266, complete 405, dead 448; extract corpus/evidence/sources-r56/watchdog-log-grammar.txt, sha256 38ba3e6b…417796 | The writer source per launch/complete/dead/wrap line shape; the probe grammar is frozen from it | mined | 2026-10-27 | on-release | corpus/knowledge/driver-liveness-r56.md, tools/mori-driver-liveness.py |
```

### Argument that tier A is NOT defensible

1. The own-work tier rule as briefed to this seat: "the lane's own re-runnable
   gate output". The two writer scripts are the hyaku dispatcher fleet's
   infrastructure, not the lane's output, and they are not a gate the lane can
   run — mori can only read them. The lane's own re-runnable gate output is
   `tools/mori-driver-liveness.py` plus its selftest and the 9 frozen fixtures;
   S544 does not cite that as its source (it names the tool only in used-by,
   as a consumer).
2. Kind taxonomy: by the registry's own vocabulary, two shell scripts are
   `code` (cf. S003 mm/oom_kill.c code, S013 catalog code, S534 kernel/fork.c
   code at tag v7.3). Nothing in the nature of the artifact is "own-work";
   the novelty is only that the code is local and re-verifiable read-only,
   which argues for `code` with a local path anchor, tier A.
3. Precedent S200 (`fleet MANIFEST.json rounds ledger`, fleet commit
   37b51a24) shows the registry does not treat fleet bytes as automatically
   own-work: that fleet artifact was classified `dataset`. "Fleet-internal"
   and "own-work" are distinct axes in this registry's practice.
4. Drift exposure without a pin: the located line numbers are asserted
   against the moving fleet worktree. Fleet commits land frequently
   (`5f4fa8d8` on 2026-10-25 touched the same watchdog path). Unlike S003
   (tag v7.2), S013 (commit pin), S200 (fleet commit pin), S533/S534 (tag
   v7.3), S544 pins no fleet revision. If `inline.sh` is edited, the anchor's
   line numbers silently detach while the extract sha256 still verifies —
   a half-stale anchor.

### Argument that tier A IS defensible

1. Direct precedent S474 (`mori AXES calibration criterion —
   /home/vgpnk/Projects/shokunin/AXES.md`, own-work, tier A, anchor
   `AXES.md:15`, mined 2026-10-25): the registry has already admitted a
   fleet-repo path as kind own-work, tier A. The own-work axis in practice
   discriminates "authored by the shokunin fleet itself" from external
   authorities (docs/spec/code/tool/community/paper/book/dataset), not
   "lane-internal" from "fleet-internal". S544's source is fleet-authored,
   same as AXES.md.
2. S034 (the lane's own census receipt) and S488 (host capture) show own-work
   rows are re-verifiable artifacts; S544's anchor is exactly located and the
   extract pins the bytes, so the row is re-verifiable read-only by any seat —
   which this seat did below (all six line numbers reproduce exactly).
3. The taught claim is "the probe grammar is frozen from the writer source".
   For that claim the writer source is the primary authority; tier A is the
   tier for primary authorities with located anchors.
4. Counter point 3 above is weak: S200's `dataset` kind reflects that a
   rounds ledger is a dataset, not a ruling that fleet bytes can never be
   own-work; S474 is the direct kind ruling and it is own-work.

### Verdict

Tier A is **defensible**. The strongest counterexample available from local
evidence (S200, kind taxonomy) does not defeat it because S474 is the
on-point precedent: a fleet-repo file classified own-work, tier A, with a
located anchor. The narrow reading of the tier rule ("the lane's own
re-runnable gate output") is contradicted by the registry's own usage.
The classification is contestable registry semantics, not a factual error;
it does not touch the C1 kill list. Residual weaknesses are routed below as
LOW findings (unpinned fleet revision for located line numbers).

## 2. S544 anchor — located line range or prose?

**Located.** Six line numbers across two files plus a byte-pinned extract.
Verified against the live fleet worktree (all exact):

```
$ grep -n 'launch\|complete\|dead' scripts/hyaku/inline.sh
149:  log "launch $lane round=$n pgid=$$ driver=hyaku-inline attempt=$a"
176:  log "complete $lane round=$n; hyaku-inline attempt=$(claim "$lane" attempt)"
182:  log "lane-dead-no-report $lane round=$n; retry same round (hyaku-inline attempt=$a: $why)"
$ grep -n 'launch\|complete\|dead' scripts/shokunin-watchdog.sh
266:  log "launch $lane round=$n pgid=$pid"
405:      log "complete $lane round=$n; advancing to round=$((n+1))"
448:        log "lane-dead-no-report $lane round=$n; retry same round"
$ sha256sum corpus/evidence/sources-r56/watchdog-log-grammar.txt
38ba3e6b309e17d3d8038e8986e274bb363ac893d1c325fe145a95882a417796
```

(exit 0; extract digest matches the row's pinned sha256).

Caveat: the located line numbers are **not pinned to a fleet revision** (see
Findings F2). The extract carries the byte pin.

## 3. S545 — does it duplicate an existing row?

No. Searched the registry for `rfc 8259`, `json.org`, `ECMA-404` and
`json standard` — the only hit is S545 itself. Related but non-duplicative:

- S062 / S209 — RFC 8785 JSON Canonicalization Scheme (JCS): a different
  document (canonical serialization for hashing, Informational) with its own
  located anchors; scope is key collation/number text for hashing, not the
  §-level grammar of a JSON string scalar.
- S063 — Python `json` module documentation (rejected, tier C): CPython
  call-contract scope, not the JSON grammar.

No duplicate. S545 is admissible as the first JSON-grammar row.

## 4. used-by path existence at freeze tip 8be2717b

```
$ for p in corpus/knowledge/driver-liveness-r56.md tools/mori-driver-liveness.py \
           corpus/knowledge/vote-binding-r56.md tools/mori-vote-bind.py \
           corpus/evidence/sources-r56/watchdog-log-grammar.txt \
           corpus/evidence/sources-r56/rfc8259.txt; do
    git cat-file -e 8be2717b0809281d07dffe83dad424a4859e0747:"$p" && echo "EXISTS  $p" || echo "MISSING $p"; done
EXISTS  corpus/knowledge/driver-liveness-r56.md
EXISTS  tools/mori-driver-liveness.py
EXISTS  tools/mori-driver-liveness.py
EXISTS  corpus/knowledge/vote-binding-r56.md
EXISTS  tools/mori-vote-bind.py
EXISTS  corpus/evidence/sources-r56/watchdog-log-grammar.txt
EXISTS  corpus/evidence/sources-r56/rfc8259.txt
```

(exit 0). All four used-by paths and both anchor artifacts exist at the
freeze tip. No phantom used-by.

Both extract/copy sha256 pins verify against the freeze-tip blobs:
`38ba3e6b…` (watchdog-log-grammar.txt) and `61a5378f…` (rfc8259.txt).

## 5. Counter confirmation at freeze tip

```
$ python3 .ufo/waves/round-56/count-c1.py 8be2717b0809281d07dffe83dad424a4859e0747
C1=met selftest=ok fixtures=ok entry=ok row=ok norem=ok rev=8be2717b0809281d07dffe83dad424a4859e0747
exit=0
$ python3 .ufo/waves/round-56/count-c2.py 8be2717b0809281d07dffe83dad424a4859e0747
C2=met selftest=ok tally=ok control=ok contrast=voted0 entry=ok row=ok rev=8be2717b0809281d07dffe83dad424a4859e0747
exit=0
```

Both row-mining arms pass: the counters' `row=ok` confirms S544/S545 carry
status `mined`, opened `2026-10-27`, and used-by naming the entries.

## 6. S545 anchor line check (extra)

The row's anchor quotes and line numbers were checked against the committed
copy (899 lines, sha256 matches):

- line 251 = "A JSON text is a serialized value." ✓ (text exact)
- line 308 = "value = false / null / true / object / array / number / string" ✓
- line 461 = "string = quotation-mark *char quotation-mark" ✓

Section labels in the anchor prose are wrong on all three points (see
Findings F3): line 251 sits in §2 JSON Grammar (header line 246), line 308 in
§3 Values (header line 296), line 461 in §7 Strings (header line 424). The
located line numbers — the load-bearing part of the anchor — are correct.

## Findings

- **F1 (MED)** — `corpus/SOURCES.md:324` (S544, `teaches` cell). The cell
  claims the row is "the writer source per launch/complete/dead/wrap line
  shape", but the anchor locates only launch/complete/dead line numbers and
  the byte-pinned extract (`watchdog-log-grammar.txt`, 6 lines) contains no
  `wrap` and no `launch-fail` line. The wrap writer source does exist
  (`shokunin-watchdog.sh:398`, verified: `log "wrap $lane round=$n landed;
  NOT respawning (fleet-wrap)"`, and 22 wrap lines in the live
  `.ufo/watchdog.log`) and launch-fail at `:241-249`, but the row does not
  locate them. The teaches cell overclaims the located coverage. Does not
  kill C1 (counter `row=ok` passes; kill list unaffected). Smallest safe
  correction: append-only registry correction naming watchdog.sh:398 and
  :241-249 and extending the extract with the wrap and launch-fail writer
  lines, or narrow the teaches cell — round 57 routed item; frozen cells are
  not edited this round.

- **F2 (LOW)** — `corpus/SOURCES.md:324` (S544, anchor cell). Located line
  numbers are asserted against the unpinned fleet worktree; no fleet revision
  is named (contrast S003 tag v7.2, S013 commit pin, S200 fleet commit
  37b51a24, S533/S534 tag v7.3). The extract sha256 pins the bytes, so the
  anchor degrades gracefully, but the six line numbers can drift silently on
  the next fleet edit of either script. Smallest safe correction: round 57
  appends a fleet commit pin to the anchor (or to a correction record) at the
  next registry touch.

- **F3 (LOW)** — `corpus/SOURCES.md:325` (S545, anchor cell). Section labels
  are misattributed on all three located lines: "section 1 line 251" is §2
  JSON Grammar; "section 2 grammar lines 308 and 461" are §3 Values (line 308)
  and §7 Strings (line 461). The quoted text and line numbers are exact;
  only the prose section names are wrong. Smallest safe correction: round 57
  correction record; no located value changes.

- **F4 (INFO, no defect)** — S544 tier A adjudicated defensible on local
  precedent S474 (`/home/vgpnk/Projects/shokunin/AXES.md`, own-work, tier A);
  no duplicate exists for S545; all used-by and anchor paths exist at the
  freeze tip; both frozen counters run `met` at `8be2717b` with exit 0.

# Round 28, wave 1 — SupersedeS129 (seat MoriR28.SupersedeS129)

Claim: C1 (freshness). Carried teaches defect M2 of row S129 (routed by
`.ufo/waves/round-27/w2/ReopenS129.md`, and by the round-27 closure's routed-defect list at
`corpus/lessons/round-27-verifier-spotcheck.md:150`). This report gives the L1 one ready-to-paste
superseding row **S150**, the Gate lines, the QUALITY 77 sweep list, and the measurements run on a
sandbox clone. The lane was not written except this file. Scratch:
`/fast/scratch/hyaku/mori-r28/MoriR28.SupersedeS129/`.

## 0. Result in one paragraph

S129's row was first published at `126e192d1fa92675bbaabdcfa7fa1b389f01791c` and is byte-identical at
the entering tip `6ebd518f` (sha256 of the row line `2c3141c9…b849` at both; the row-identity check at
the tip does not list S129 — `changed=3` is only S096, S097, S101). So S129 needs **no restore**: the
defect is a wording defect in the `teaches` cell as first published (M2: an unflagged derivation, plus
L1 and L2 wordings in the same cell), and under QUALITY 81 the correction must be a new superseding row.
The source was re-opened today by `curl` (HTTP 200 both; sha256 identical to the row's recorded digests —
bytes unchanged since the 2026-10-22T15:46:34Z fetch). The recommended row **S150** opens
`supersedes S129 — `, fixes M2/L1/L2, and is accepted by the round-28 counter's own detection logic
(prints `1 S129`). It adds one new census warning (W04, same URL across scopes) because its scope is
corrected; a scope-identical variant is measured as the zero-new-warning alternative.

## 1. First-published row and the row at the tip

First publication (the assignment's command, run read-only in the lane):

```
$ git -C /home/vgpnk/Projects/shokunin/mori-shokunin log --reverse --format=%H -S'| S129 |' -- corpus/SOURCES.md | head -1
126e192d1fa92675bbaabdcfa7fa1b389f01791c
```

`126e192d` is "round-27: C1 entry oom-victim-selection-r27, SOURCES S127-S132 and used-by anchors…"
(2026-10-22 12:58:23 -0300). Its parent has 0 occurrences of the row. The pickaxe lists only this one
commit — the row was never edited in place.

First-published row (`git show 126e192d:corpus/SOURCES.md`, line 135):

```
| S129 | systemd v262 `OOMScoreAdjust=` and `DefaultOOMScoreAdjust=` manual pages — https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd.exec.xml ; https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd-system.conf.xml | docs | A | systemd 262 release documentation of the OOM score adjustment only: the per-unit range and its stated effects, the per-unit default of the managing manager's own level, the manager-wide default and its unset/inherit reading, the unprivileged-user-manager default of manager value plus 100, and the statement that the manager's own value is never rewritten; not this host's unit values, user-manager state or fleet process scores, not the kernel's `oom_score` computation or `proc(5)` wording, not earlyoom's or systemd-oomd's victim choice, not the privilege rule on lowering the value (kernel doc, separate row) | man/systemd.exec.xml:1293 (term), :1295-1296 (executed processes), :1296-1297 (range -1000..1000), :1299-1300 (unset => manager's level, normally 0), :1302-1305 (OOMPolicy cross-ref), :4934-4938 (EXIT_OOM_ADJUST = 206, "problems during process invocation" at :4890-4891); man/systemd-system.conf.xml:301 (term), :303-304 (processes run by the manager), :304-305 (unset => fork inherits manager value), :305-307 (unprivileged user manager => manager value plus 100), :307-308 (global default for the per-unit setting), :310-311 (manager process keeps its own value), :313 (v250), :49-55 (system.conf vs user.conf read by the two managers); tag v262 = commit 8cc40e0c5e9234bf45084751ac53b1fbfe70b492 (annotated tag 1f7dffaf714cc4488159c498b7a17cf34c5a96d5, tagger 2026-09-22T13:12:43Z); systemd.exec.xml 343,315 B sha256 44b89bffce737aff803966c207329e9fe2d28ad07709a4bb8e0edf6a4ec0d844; systemd-system.conf.xml 49,977 B sha256 161359987affadc8e4a533bc9117bbbd98053cb807808b623eb24794b49b0c58; HTTP 200 both, 2026-10-22T15:46:34Z | The per-unit score is an integer in -1000..1000 applied to a unit's executed processes; unset means the managing manager's own level (normally 0 for the system manager), and for an unprivileged user manager the manager-wide default is that manager's value plus 100, so user units inherit manager+100 unless they set the value; the setting never changes the manager's own score. | mined | 2026-10-22 | on-release | corpus/knowledge/oom-victim-selection-r27.md |
```

Row at the entering tip `6ebd518f` (`git show 6ebd518f:corpus/SOURCES.md`, line 135): byte-identical
(sha256 of the row line identical, `cmp` in scratch).

Cells that differ: **none.** Every cell (source, kind, tier, scope, anchor, teaches, status, opened,
recheck, used-by) is byte-identical between first publication and the tip. Therefore S129 is not in the
row-identity check's `changed` set; its fix is a superseding row only (contract's fixed id for S129 is
S150), and S129's row must stay in the registry (`removed=0` is part of the C1 check).

## 2. The source re-opened today, and every claim checked against the bytes

All fetches: ordinary `curl -sS -L` GETs, no redirect tricks, no challenge. Access times UTC.

| URL | accessed | result | SHA-256 of fetched bytes |
|---|---|---|---|
| https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd.exec.xml | 2026-10-22T17:58:56Z | HTTP 200, 343,315 B, 5,308 lines | `44b89bffce737aff803966c207329e9fe2d28ad07709a4bb8e0edf6a4ec0d844` |
| https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd-system.conf.xml | 2026-10-22T17:58:56Z | HTTP 200, 49,977 B, 919 lines | `161359987affadc8e4a533bc9117bbbd98053cb807808b623eb24794b49b0c58` |

Both digests equal the row's recorded sha256 values — the bytes are unchanged. Tag/commit re-verified:
`git ls-remote` → `refs/tags/v262` = `1f7dffaf…` (annotated tag object), `refs/tags/v262^{}` =
`8cc40e0c…` (commit); GitHub API (18:01:05Z / 18:01:08Z) → object type `tag`, `tagger.date`
2026-09-22T13:12:43Z, `verification.verified` true.

Statement-by-statement verification of what the corrected row (S150) asserts (line numbers in the
fetched bytes):

1. "the per-unit score is an integer in -1000..1000 applied to a unit's executed processes" — holds:
   exec.xml `:1293` term; `:1295-1296` "Sets the adjustment value … for / executed processes."; `:1296-1297`
   "Takes an integer between -1000 … and 1000".
2. "an unset per-unit `OOMScoreAdjust=` takes the OOM score adjustment level of the service manager
   itself, normally at 0, and the page names no manager type" — holds: exec.xml `:1299-1300`, "If not
   specified, defaults to the OOM score adjustment level of the service manager itself, which is normally
   at 0." "Names no manager type": `grep -ni 'system manager'` in exec.xml hits only lines 3367, 4185,
   4208 — none in 1293-1305, 4890-4891 or 4934-4938; in conf.xml hits 110, 113, 382, 605, 662, 678,
   784, 785 — none in 301-313.
3. "the manager-wide `DefaultOOMScoreAdjust=` configures the default OOM score adjustments of processes
   run by the service manager and defaults to unset, so forked-off processes inherit the service
   manager's own value" — holds: conf.xml `:303-305`.
4. "except that for a service manager run for an unprivileged user it defaults to the manager's value
   plus 100" — holds: conf.xml `:305-307`.
5. "that setting may be used to pick a global default for the per-unit `OOMScoreAdjust=` setting" —
   holds: conf.xml `:307-308` "This may be used to pick a global default for the per-unit
   `<varname>OOMScoreAdjust=</varname>` setting." (the "may be used" hedge is exactly why the old row's
   "so user units inherit manager+100" was a derivation, not a byte reading).
6. "`DefaultOOMScoreAdjust=` has no effect on the manager process's own value" — holds: conf.xml
   `:310-311`.
7. The per-unit page never references the manager-wide setting: `grep -c 'DefaultOOMScoreAdjust'`
   exec.xml = 0 — so the two pages genuinely do not reconcile the per-unit unset default with the
   manager-wide default.
8. `[INFERENCE] What a unit of a user manager inherits when it sets no OOMScoreAdjust= is not stated by
   either page` — supported by 2 and 5 (the execution of 4 on per-unit defaults is not stated).
9. Anchor lines: exec.xml `:1293`, `:1295-1296`, `:1296-1297`, `:1299-1300`, `:1302-1305`
   (OOMPolicy cross-ref), `:4934-4938` (EXIT_OOM_ADJUST = 206), `:4890-4891` ("problems during process
   invocation" sits on line 4891); conf.xml `:301`, `:303-304`, `:304-305`, `:305-307`, `:307-308`,
   `:310-311`, `:313` (v250 include), `:49-55` (system.conf vs user.conf read by the two managers) — all
   hold in the fresh fetch.

Not re-observable: the original fetch timestamp `2026-10-22T15:46:34Z`; byte identity is established by
today's sha256 equality.

## 3. Ready-to-paste row

**Recommended (S150, scope corrected — the assignment's "scope and anchor corrected").** Insert after the
S144 row (`corpus/SOURCES.md:150`, last row of `## Registry` before the blank line). Id 150 is the
contract-fixed id for S129 (the counter requires id > 144; S150 qualifies).

```text
| S150 | systemd v262 `OOMScoreAdjust=` and `DefaultOOMScoreAdjust=` manual pages — https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd.exec.xml ; https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd-system.conf.xml | docs | A | systemd 262 release documentation of the OOM score adjustment only: the per-unit range and its stated effects, the per-unit unset default of the service manager's own level (the page names no manager type), the manager-wide default and its unset/inherit reading, the unprivileged-user-manager branch of manager value plus 100, and the statement that `DefaultOOMScoreAdjust=` leaves the manager process's own value unchanged; not the value a unit inherits when it sets no `OOMScoreAdjust=`, not this host's unit values, user-manager state or fleet process scores, not the kernel's `oom_score` computation or `proc(5)` wording, not earlyoom's or systemd-oomd's victim choice, not the privilege rule on lowering the value (kernel doc, separate row) | man/systemd.exec.xml:1293 (term), :1295-1296 (executed processes), :1296-1297 (range -1000..1000), :1299-1300 (unset => the service manager's own level, normally at 0, no manager type named), :1302-1305 (OOMPolicy cross-ref), :4934-4938 (EXIT_OOM_ADJUST = 206, "problems during process invocation" at :4890-4891); man/systemd-system.conf.xml:301 (term), :303-304 (processes run by the manager), :304-305 (unset => fork inherits manager value), :305-307 (unprivileged user manager => manager value plus 100), :307-308 (the manager-wide setting may be used to pick a global default for the per-unit setting), :310-311 (`DefaultOOMScoreAdjust=` leaves the manager process's own value unchanged), :313 (v250), :49-55 (system.conf vs user.conf read by the two managers); tag v262 = commit 8cc40e0c5e9234bf45084751ac53b1fbfe70b492 (annotated tag 1f7dffaf714cc4488159c498b7a17cf34c5a96d5, tagger 2026-09-22T13:12:43Z); systemd.exec.xml 343,315 B sha256 44b89bffce737aff803966c207329e9fe2d28ad07709a4bb8e0edf6a4ec0d844; systemd-system.conf.xml 49,977 B sha256 161359987affadc8e4a533bc9117bbbd98053cb807808b623eb24794b49b0c58; HTTP 200 both, re-opened 2026-10-22T17:58:56Z (bytes unchanged since the 2026-10-22T15:46:34Z fetch) | supersedes S129 — the old row's clause "so user units inherit manager+100 unless they set the value" was a derivation presented as a reading of the bytes, and it conflicts with the row's own anchor systemd.exec.xml:1299-1300 without saying so; the old row also narrowed "normally 0 for the system manager" and left "the setting never changes the manager's own score" ambiguous between the per-unit and the manager-wide setting. Corrected: the per-unit score is an integer in -1000..1000 applied to a unit's executed processes; an unset per-unit `OOMScoreAdjust=` takes the OOM score adjustment level of the service manager itself, normally at 0, and the page names no manager type (systemd.exec.xml:1299-1300); the manager-wide `DefaultOOMScoreAdjust=` configures the default OOM score adjustments of processes run by the service manager and defaults to unset, so forked-off processes inherit the service manager's own value (systemd-system.conf.xml:303-305), except that for a service manager run for an unprivileged user it defaults to the manager's value plus 100 (systemd-system.conf.xml:305-307); that setting may be used to pick a global default for the per-unit `OOMScoreAdjust=` setting (systemd-system.conf.xml:307-308), and `DefaultOOMScoreAdjust=` has no effect on the manager process's own value (systemd-system.conf.xml:310-311). [INFERENCE] What a unit of a user manager inherits when it sets no `OOMScoreAdjust=` is not stated by either page: systemd.exec.xml:1299-1300 gives the service manager's own level and systemd-system.conf.xml:305-308 only says the manager-wide setting may be used as a global default, and the two pages do not reconcile each other. | mined | 2026-10-22 | on-release | corpus/knowledge/oom-victim-selection-r27.md, SKILL.md, corpus/lessons/round-27.md, corpus/lessons/round-27-verifier-spotcheck.md |
```

Cell notes: `teaches` opens exactly `supersedes S129 — ` (em dash U+2014, one space after — matches
the counter's regex and the S133/S143 precedent). `status` is `mined`, `opened` `2026-10-22`,
`recheck` `on-release` (S129's own convention), `used-by` is the set of files that cite S129 today
(§5), excluding `corpus/SOURCES.md` itself (registry-internal; 0 of 144 rows list it). No cell contains a
`|` (13 fields, checked).

Alternative (variant B, census-clean): the same row but with the `scope` cell byte-identical to S129's
published scope. Measured consequence: no new census line at all (see §4). Recommended is variant A
because the assignment asks for a corrected scope and the scope wording "the statement that the manager's
own value is never rewritten" is itself the L2 ambiguity the row fixes.

## 4. Gate lines (round-28 lesson `## Gate`)

Per the contract's C1 Gate shape (URL, access time, located quote ≤25 words verbatim, admit/kind/mined):

| Row | URL | Accessed | Located quote (verbatim, ≤25 words) | Decision |
|---|---|---|---|---|
| S150 | https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd.exec.xml (with https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd-system.conf.xml) | 2026-10-22T17:58:56Z | `systemd.exec.xml:1299-1300` "If not specified, defaults to the OOM score adjustment level of the service manager itself, which is normally at 0." (20 words) | admit, A, mined (MoriR28.SupersedeS129) |
| S150 (supporting) | https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd-system.conf.xml | 2026-10-22T17:58:56Z | `:305-306` "if the service manager is run for an unprivileged user, in which case this defaults to the service manager's OOM adjustment value plus 100" (24 words) | admit, A, mined (MoriR28.SupersedeS129) |

Both quotes are verbatim in the fetched bytes (whitespace-folded across the wrap; ASCII apostrophe in
"manager's").

## 5. QUALITY 77 sweep: every place in the lane whose prose states the defective wording

The defective wording = M2's unflagged derivation ("so user units inherit manager+100 unless they set the
value") and the same cell's L1 narrowing ("normally 0 for the system manager") and L2 ambiguity ("the
setting never changes the manager's own score"). Line numbers at the entering tip `6ebd518f`.

Live surfaces to correct (the round-28 sweep must make these carry the corrected wording / cite S150):

1. `corpus/SOURCES.md:135` — S129's own row (teaches cell). Immutable under QUALITY 81; the correction is
   S150, not an in-place edit. S129 stays in the registry.
2. `corpus/knowledge/oom-victim-selection-r27.md:86-87` — "Every process a user unit starts, and
   everything those processes start, inherits 200 unless something writes a new value." (ReopenS129
   dependent statement D2: unsupported as a bytes claim; the 200 is host-observed, the per-unit rule for
   user units is the M2 inference).
3. `corpus/knowledge/oom-victim-selection-r27.md:166` — decision table "most likely it inherits the user
   manager's default for its units (100 + 100, Fact 3)" (D3).
4. `SKILL.md:730` — "(manager 100, children 100 more)" (D4).
5. `corpus/README.md:36` — "the fleet's `oom_score_adj` 200 traced to systemd's per-user manager (100 +
   100) and not the harness".
6. `PROVINCE.md:376` — "where the fleet's `oom_score_adj` 200 comes from (systemd's per-user manager, not
   the harness)".
7. `corpus/knowledge/oom-victim-selection-r27.md:200` — "the `systemd.exec` default quoted at
   `kill-event-deep-r8.md:142` describes the system manager" — the M1 wording still standing at the tip
   (entry `:78` was narrowed in wave 2, `:200` was not). S150's teaches corrects the same point.
8. Citation updates (no wording defect, but S129 references should name S150 after the sweep):
   `corpus/knowledge/oom-victim-selection-r27.md:1` (source line), `:72` (heading), `:78` (manual-sentence
   reference), `SKILL.md:722` (grounding list), `corpus/SOURCES.md:136` (S130 row's "the manual sentence is
   row S129" — note S130's scope cell is immutable; only a lesson note or a new row can carry the pointer).

Records (keep as history; log old→new in the round-28 lesson, per the lane's S090/S143 precedent):

9. `corpus/lessons/round-27.md:15-17, 71, 127`
10. `corpus/lessons/round-27-verifier-spotcheck.md:119, 133, 150`
11. `.ufo/waves/round-27/w1/SrcSystemdExecOomScoreAdjust.md:56 (F3), 59 (F6), 61 (F8), 66-70 (consequence), 94`
12. `.ufo/waves/round-27/w1/ConnSiblingOverlap.md:83-88`
13. `.ufo/waves/round-27/w1/SrcSystemdUserService.md:45, 68-69`
14. `.ufo/waves/round-27/w2/ReopenS129.md` (the finding itself)

## 6. Falsifications run (sandbox clone, lane untouched)

Sandbox `git clone --no-hardlinks` at `6ebd518f`; S150 inserted after S144 and committed; the round-28
counter's detection block, the row-identity check (copy with `LANE` repointed at the sandbox), and the
fleet census were run there.

1. Counter detection (the python block of `.ufo/waves/round-28/count-c1.sh`, owed list
   `S096 S097 S101 S127 S128 S129 S131 S140`, `MAX_OLD=144`): prints `1 S129` — S150 is counted as the
   superseding row for S129.
2. Row-identity check at the sandbox commit: `rows=145 changed=3 removed=0 bad=0` (the `changed=3` are
   S096/S097/S101, owned by other seats; S129 not changed; S150 new). Exit 1 only because the other
   seats' restores are not yet applied.
3. Census `sources-census.sh validate` (with the row present): variant A adds one new warning line
   `W04 S150 duplicate url …/systemd.exec.xml across scopes`; exit 0 (warnings do not change status).
   Variant B (scope identical to S129's) adds zero new findings; exit 0. No E-codes either way; no E11
   (all used-by paths exist).
4. `cmp`: S129's row line is byte-identical between 126e192d and 6ebd518f.

## 7. Findings for the L1

- **MEDIUM — S129's defect is first-published content, not an in-place edit.** The row was never edited;
  the M2 derivation (with L1/L2) is in the publishes cell as first published. The C1 fix for S129 is
  therefore the superseding row S150 + the QUALITY 77 prose sweep; S129's row stays in the registry
  (removed=0).
- **MEDIUM — the sweep must also touch the derived 200 prose.** Entry :86-87, :166, SKILL.md:730, README
  :36, PROVINCE :376 state the inheritance chain as fact; ReopenS129 flagged the per-unit rule as the M2
  inference. The corrected wording belongs in these live surfaces.
- **LOW — the M1 wording survives at entry:200.** The wave-2 fix narrowed entry :78 but not :200
  ("describes the system manager"); S150's teaches carries the correction, the prose sweep should too.
- **LOW — one new census warning with the corrected scope.** Variant A adds `W04 S150` (same URL across
  scopes). Variant B (scope identical to S129's) is census-silent; choose B if the lane wants a
  byte-identical census output.
- **NOTE — S130's scope cell is immutable** and keeps "the manual sentence is row S129"; the L1 should
  log this pointer in the round-28 lesson (a scope edit would violate QUALITY 81).
- **NOTE — the round-28 lesson will cite S150 (and S129).** Add `corpus/lessons/round-28.md` to S150's
  used-by once it exists (it is currently untracked in the working tree); listing it before it is
  committed would trip the census E11 check.

## 8. Bounds, tools, installs

- Lane writes: this file only. No `git add/commit/…` in the lane; only read-only `git log/show/grep/
  ls-remote`; no jj command ran; no unit/process touched; no harness settings or MCP files read or
  written; no OMP settings value, session id or session-store path appears.
- Fetches: ordinary `curl -sS -L` GETs, HTTP 200, no challenge, no bot bypass. GitHub API calls for the
  tag record. Counts, states, versions and digests only.
- Tools: `curl`, `sha256sum`, `python3 -I -B`, `git` (read-only), `grep`/`awk`/`sed` on scratch copies.
  Installed or upgraded: **nothing** (host pacman transactions are paused; no uv/npm/cargo ran).
- Privacy: no uid, pid, `user-<digits>.slice`, `user@<digits>.service`, unit names of this host's user
  session, journal MESSAGE text, or `/etc/default/earlyoom` values; no fixture was written.

## 9. Artifact paths

- Report: `.ufo/waves/round-28/w1/SupersedeS129.md` (this file).
- Scratch: `/fast/scratch/hyaku/mori-r28/MoriR28.SupersedeS129/` — fetched `systemd.exec.xml` /
  `systemd-system.conf.xml`, `api-tag-v262.json`, `api-tagobj-v262.json`, `draft-row.txt`,
  `row-final.txt`, `row-variantB.txt`, sandbox clone, census builders.

# Draft — C1 replacement text for the four frozen stale statements (round 26, wave 1)

Seat: `MoriR26.DraftR12Corrections` (scribe). Claim drafted: C1 (freshness) — replacement wording only.
No lane file was edited, no commit, no ref update, no `jj` run, no unit started/stopped/enabled/disabled.
Scratch for this seat: `/fast/scratch/hyaku/mori-r26/DraftR12Corrections/`.

## 1. Host reading this draft is based on (read-only, 2026-10-22)

Commands and outputs, run from the lane root at 2026-10-22 (local time -03):

```
$ systemctl is-active earlyoom.service
active
$ systemctl is-enabled earlyoom.service
enabled
$ systemctl show earlyoom.service -p LoadState -p ActiveState -p UnitFileState -p ActiveEnterTimestamp
LoadState=loaded
ActiveState=active
UnitFileState=enabled
ActiveEnterTimestamp=Thu 2026-10-22 04:55:44 -03
$ systemctl is-active systemd-oomd.service
inactive
$ systemctl is-enabled systemd-oomd.service
disabled
$ systemctl show systemd-oomd.service -p LoadState -p ActiveState -p UnitFileState
LoadState=loaded
ActiveState=inactive
UnitFileState=disabled
$ systemctl --version | head -1
systemd 262 (262-1-arch)
$ pacman -Q earlyoom
earlyoom 1.9.0-1
$ uname -r
7.2.11-arch1-1
```

All of the above are read-only queries (`is-active`, `is-enabled`, `show`, `--version`, `pacman -Q`).
No `pacman` transaction was run.

## 2. Targets, byte-exact

Line identity, from `awk`/`sha256sum` over the working-tree files (byte length of the line without the
newline; sha256 of the same bytes):

| Target | file | line | bytes | sha256 |
|---|---|---|---|---|
| F1 | `corpus/knowledge/userspace-oom-killers-r12.md` | 6 | 528 | `3e3b84aaa5184c4e2d7a330cee08289fed004416903c978799e72913159f90bc` |
| F2 | `corpus/knowledge/userspace-oom-killers-r12.md` | 14 | 236 | `9084eec66a53d04fd0206a49236b633cb16662578ee8104a85fb36a8e4860039` |
| F3 | `corpus/knowledge/userspace-oom-killers-r12.md` | 18 | 310 | `212c4f86aa8b28f47b632614fe16161818c48a322bf476bcf3ee67dc440d59bc` |
| F4 | `corpus/README.md` | 34 | 286 | `3377962df010a589a911a50dd1d11e5f0e29c3c33341bcd979e47ee29be6a154` |
| FR10 row | `corpus/README.md` | 341 | 248 | `6a6c2c2376e7e218f209f9c87b459052f28746f19a919a6e71c8b9f92aedccf6` |
| FR10 row | `PROVINCE.md` | 53 | 290 | `abad027bae9057ebb81a3f378d426c6f30ac701c3db993bc221518a526b601b2` |

Each frozen phrase occurs exactly once in its file, at the line above (verified with
`grep -n -F` on all four phrases across `corpus/knowledge/userspace-oom-killers-r12.md`,
`corpus/README.md`, `PROVINCE.md`).

## 3. Replacement pairs (old line → new line, byte-exact old)

### 3.1 F1 — `corpus/knowledge/userspace-oom-killers-r12.md:6` (`## Claim` paragraph)

OLD:

```
systemd-oomd v261 records its cgroup kills in `user.oomd_ooms` (one per oomd kill attempt) and `user.oomd_kill` (number of PIDs killed), emits D-Bus `Killed(path, reason)`, and has the catalog notice `d989611b…`. These userspace kill paths do not increment the kernel OOM counters. earlyoom normally sends SIGTERM and then SIGKILL and logs its own actions; only `--kernel-oom` delegates to the kernel OOM killer. On this host both services are inactive, so a probe must render `unavailable (inactive)`, never a zero-kill result.
```

NEW:

```
systemd-oomd v261 records its cgroup kills in `user.oomd_ooms` (one per oomd kill attempt) and `user.oomd_kill` (number of PIDs killed), emits D-Bus `Killed(path, reason)`, and has the catalog notice `d989611b…`. These userspace kill paths do not increment the kernel OOM counters. earlyoom normally sends SIGTERM and then SIGKILL and logs its own actions; only `--kernel-oom` delegates to the kernel OOM killer. On 2026-10-19 this host had both userspace OOM killer services inactive, so a killer that cannot be observed had to render `unavailable`, never a zero-kill result. On 2026-10-22 earlyoom was active and enabled and systemd-oomd was inactive and disabled; `corpus/knowledge/userspace-oom-killers-r26.md` is the superseding host-state record.
```

### 3.2 F2 — `corpus/knowledge/userspace-oom-killers-r12.md:14` (Evidence bullet)

OLD:

```
- Host state: `systemctl is-active systemd-oomd.service` → `inactive`; `systemctl is-enabled systemd-oomd.service` → `disabled`; `systemctl is-active earlyoom.service` → `inactive`; `systemctl is-enabled earlyoom.service` → `not-found`.
```

NEW:

```
- Host state: on 2026-10-19 `systemctl is-active systemd-oomd.service` → `inactive` and `systemctl is-enabled systemd-oomd.service` → `disabled`, while `systemctl is-active earlyoom.service` returned `inactive` and `systemctl is-enabled earlyoom.service` returned `not-found`; on 2026-10-22 `systemctl is-active earlyoom.service` → `active` and `systemctl is-enabled earlyoom.service` → `enabled`, with `systemctl is-active systemd-oomd.service` → `inactive` and `systemctl is-enabled systemd-oomd.service` → `disabled` (earlyoom 1.9.0, systemd 262), per the superseding entry `corpus/knowledge/userspace-oom-killers-r26.md`.
```

Note for the L1: the 2026-10-19 earlyoom readings are rendered with "returned" instead of the
arrow form on purpose. The arrow form for earlyoom is the frozen phrase F2
(`` `systemctl is-active earlyoom.service` → `inactive` ``), so keeping the arrow there would leave
F2 standing in the file and `stale_present` would stay 1.

### 3.3 F3 — `corpus/knowledge/userspace-oom-killers-r12.md:18` (`## Observed` paragraph)

OLD:

```
The v261 source writes the two cgroup xattrs around oomd's kill operation and emits the D-Bus signal. Both service units are inactive; oomd is disabled and earlyoom's service unit is not found. The host has zero retained d989611b notices in each queried journal scope; that is not a historical-kill conclusion.
```

NEW:

```
The v261 source writes the two cgroup xattrs around oomd's kill operation and emits the D-Bus signal. On 2026-10-19 both service units were inactive, oomd was disabled and earlyoom's service unit was not found. On 2026-10-22 earlyoom was active and enabled and systemd-oomd was inactive and disabled; `corpus/knowledge/userspace-oom-killers-r26.md` is the superseding record for that reading. The 2026-10-19 queries found zero retained d989611b notices in each queried journal scope; that is not a historical-kill conclusion.
```

### 3.4 F4 — `corpus/README.md:34` (coverage-map row)

OLD:

```
| `knowledge/userspace-oom-killers-r12.md` | systemd-oomd (`user.oomd_ooms`/`user.oomd_kill` xattrs, D-Bus `Killed`, `d989611b…`) and earlyoom kill paths; inactive on this host → `unavailable (inactive)`, never 0; OS/unit state is tsukuroi's | S002, S003, S007, S011, S012, S013, S016 |
```

NEW:

```
| `knowledge/userspace-oom-killers-r12.md` | systemd-oomd (`user.oomd_ooms`/`user.oomd_kill` xattrs, D-Bus `Killed`, `d989611b…`) and earlyoom kill paths; on 2026-10-19 both killer services were inactive here → `unavailable (inactive)`, never 0; the 2026-10-22 reading (earlyoom active and enabled, systemd-oomd inactive and disabled) is `knowledge/userspace-oom-killers-r26.md`; OS/unit state is tsukuroi's | S002, S003, S007, S011, S012, S013, S016 |
```

## 4. FR10 rows: do they need a pointer?

Judgment: **yes, a pointer; no, not a rewrite of the rule.** Neither FR10 row contains any of the
four frozen phrases (`grep -n -F` over `corpus/README.md` and `PROVINCE.md` matched only
`corpus/README.md:34`), so they are not counted by the C1 grep. But both rows are the only place
that points a reader at the r12 entry as the FR10 evidence, and QUALITY 77
(`corpus/QUALITY.md` tail) asks that every place that states the corrected fact carries the
corrected wording. The rule text itself ("inactive killers are unavailable, not zero") stays
true on 2026-10-22 — systemd-oomd is still inactive — so only the pointer and the dated host
state change.

### 4.1 `corpus/README.md:341` (FR10 row)

OLD:

```
| FR10 | Userspace OOM killers (systemd-oomd and earlyoom) | `knowledge/userspace-oom-killers-r12.md:10-15` | Inactive killers are unavailable, not zero; `memory.events oom_kill` does not cover every userspace kill; never enable or tune a killer. |
```

NEW:

```
| FR10 | Userspace OOM killers (systemd-oomd and earlyoom) | `knowledge/userspace-oom-killers-r12.md:10-15`; `knowledge/userspace-oom-killers-r26.md` | Inactive killers are unavailable, not zero; `memory.events oom_kill` does not cover every userspace kill; never enable or tune a killer. Host state is dated per entry: 2026-10-19 both services were inactive; 2026-10-22 earlyoom was active and enabled and systemd-oomd inactive and disabled (`knowledge/userspace-oom-killers-r26.md`). |
```

### 4.2 `PROVINCE.md:53` (FR10 bullet)

OLD:

```
- **FR10 — Userspace OOM killers (systemd-oomd and earlyoom)** (art F1). First evidence: `corpus/knowledge/userspace-oom-killers-r12.md:10-15`. Boundary: inactive killers are unavailable, not zero; `memory.events oom_kill` does not cover every userspace kill; never enable or tune a killer.
```

NEW:

```
- **FR10 — Userspace OOM killers (systemd-oomd and earlyoom)** (art F1). First evidence: `corpus/knowledge/userspace-oom-killers-r12.md:10-15`. Current host-state record: `corpus/knowledge/userspace-oom-killers-r26.md` — on 2026-10-19 both services were inactive; on 2026-10-22 earlyoom was active and enabled and systemd-oomd was inactive and disabled. Boundary: inactive killers are unavailable, not zero; `memory.events oom_kill` does not cover every userspace kill; never enable or tune a killer.
```

## 5. `superseded-in-part-by:` header line

Finding: **the corpus does not use such a header.**

- `grep -rn -i -e 'superseded-in-part-by' -e 'superseded-by' -e 'updated-by' corpus/ PROVINCE.md SKILL.md`
  → no match in this lane.
- The sibling lane has no such header either at the cited commit:
  `git -C ../tsukuroi-shokunin grep -n -i -e 'superseded-in-part-by' -e 'superseded-by:' 157ee255 -- corpus`
  → no match.
- The convention this corpus actually uses for supersession is in-body prose, not a header field.
  Examples: `corpus/knowledge/silence-cutover-r3.md:16-20` ("supersedes: `corpus/knowledge/…` …"),
  `corpus/knowledge/drift-repin-r20.md:82` ("Supersedes sections2–3's …"),
  `corpus/knowledge/journal-cursor-window-r16.md:121-125` and `:140-144` ("The original
  `verified-at` statement … is superseded for the **round-16 observation time**").
- The r12 entry's own frontmatter is three lines only — `source:` (line 1), `verified-at:` (line 2),
  `recheck:` (line 3) — then a blank line and `## Claim` (line 5).

So: the corpus-idiomatic home for the supersession sentence is the entry's own prose, and the best
home is the `Adjacent` paragraph at `corpus/knowledge/userspace-oom-killers-r12.md:8`, which already
carries the "2026-10-19 availability snapshot only" scope statement. Proposed one-line change
(line 8, old → new):

OLD:

```
Adjacent: `tsukuroi-shokunin/corpus/knowledge/oom-event-plane.md:344–346,353–367` owns host/service-state diagnosis and documents read-only detection surfaces. The `systemctl` readings here are a 2026-10-19 availability snapshot only; mori's claim is the fleet-facing rule `unavailable (inactive)`, not an OS/unit diagnosis.
```

NEW:

```
Adjacent: `tsukuroi-shokunin/corpus/knowledge/oom-event-plane.md:344–346,353–367` owns host/service-state diagnosis and documents read-only detection surfaces. The `systemctl` readings here are a 2026-10-19 availability snapshot only; mori's claim is the fleet-facing rule `unavailable (inactive)`, not an OS/unit diagnosis. Superseded in part on 2026-10-22 by `corpus/knowledge/userspace-oom-killers-r26.md`, which records earlyoom active and enabled and systemd-oomd inactive and disabled.
```

If the L1 decides to introduce a machine-readable header field anyway, this is the one-line form to
use, placed as line 4 of the entry (right after the `recheck:` line, before the blank line):

```
superseded-in-part-by: corpus/knowledge/userspace-oom-killers-r26.md (2026-10-22 host reading; earlyoom active and enabled, systemd-oomd inactive and disabled)
```

Warning for the L1: under QUALITY 77 a header is a banner. A `superseded-in-part-by:` line **plus**
the four rewrites in §3 is fine; the header **instead of** the rewrites leaves the contradicted
sentences standing and is a defect. If the header form is chosen, §3.1–§3.4 must still land in the
same commit.

## 6. Sweep candidates outside the four frozen phrases (flagged, not claimed by C1)

These are places that restate the 2026-10-19 host state. C1 does not count them
("Not claimed by C1: any statement about other entries, any host-wide unit census, any kill
history"), so they are the L1's call. Each is dated already, so none of them leaves a *present-tense*
stale sentence standing; I list them so the sweep decision is explicit.

| Place | What it says | Recommendation |
|---|---|---|
| `corpus/knowledge/userspace-oom-killers-r12.md:2` | `verified-at: 2026-10-19 (lane base 20e2255; host kernel 7.2.3-arch1-3, systemd 261 (261.2-1-arch))` | Keep as the 2026-10-19 verification stamp; the r26 entry carries the 2026-10-22 reading. Optionally append `; host state superseded by corpus/knowledge/userspace-oom-killers-r26.md`. |
| `corpus/knowledge/userspace-oom-killers-r12.md:21` | "A detector that cannot observe an inactive killer must report unavailable, not a healthy zero." | Keep — rule, not host state. |
| `corpus/knowledge/userspace-oom-killers-r12.md:24` | "Historical activity while either service was inactive is not inferred." | Keep — dated scope statement. |
| `corpus/knowledge/userspace-oom-killers-r12.md:27` | "keep inactive service state as `unavailable (inactive)`, never `0` kills" | Keep — rule, still true on 2026-10-22 for systemd-oomd. |
| `corpus/lessons/round-12.md:105` | "inactive → `unavailable (inactive)`; tsukuroi overlap cited, OS state deferred" | Lesson row for round 12; dated history. Optional pointer to the r26 entry. |
| `corpus/evidence/drift-r12-20261019T2204Z-classification.md:53` | `systemctl is-active systemd-oomd.service earlyoom.service; systemctl is-enabled systemd-oomd.service` → `inactive`, `inactive`, `disabled` | Dated 2026-10-19 receipt. Recommend leaving the receipt bytes alone and citing it from the r26 entry as the 2026-10-19 reading. |
| `corpus/README.md` coverage map | no row for `knowledge/userspace-oom-killers-r26.md` | The L1 must add the r26 row; the §3.4 text above is the r12 row that stays. |

## 7. Gates and checks I ran

1. Frozen-phrase clearance of my own new lines, run over
   `/fast/scratch/hyaku/mori-r26/DraftR12Corrections/new-lines.txt` with a fixed-string search for
   all four frozen phrases against all six drafted lines: **no hit** (`ALL CLEAN`). The first draft
   of §3.2 did hit F2 (the arrow form for the 2026-10-19 earlyoom reading) and was reworded to
   "returned"; the final text above is the checked one.
2. Defensive re-check of the same six lines for the substring `inactive on this host` and for
   `Both service units are inactive`: no hit (the §3.1 wording is "this host had both userspace OOM
   killer services inactive", the §3.3 wording is "both service units were inactive").
3. No trailing whitespace in any drafted line; each drafted line keeps its file's existing shape
   (one line per entry, table rows keep their column counts: README coverage map 3 columns, README
   FR10 row 4 columns).
4. Not run here (the L1's job at the landed revision): the contract's counting command over
   committed bytes. It must print `stale_present=0` and `r26_entry=present` after the rewrites land.

## 8. Tooling

Nothing installed, upgraded or changed. Tools used: `read`, `grep`, `bash` (read-only
`systemctl`/`pacman -Q`/`awk`/`sha256sum`/`grep`/`git show`-free reads), and `python3` for the
fixed-string clearance check on scratch files only. No `pacman -S/-Sy/-Syu/-U/-R`, no service
start/stop/enable/disable, no `jj`, no commit, no network fetch.

## 9. Artifact paths

- This report: `.ufo/waves/round-26/w1/DraftR12Corrections.md` (lane root
  `/home/vgpnk/Projects/shokunin/mori-shokunin`).
- Scratch drafts and the clearance check input:
  `/fast/scratch/hyaku/mori-r26/DraftR12Corrections/new-lines.txt`.
- Read-only sources used for the host reading and the conventions: `corpus/QUALITY.md` (tail),
  `corpus/README.md`, `corpus/knowledge/userspace-oom-killers-r12.md`, `PROVINCE.md`,
  `corpus/knowledge/silence-cutover-r3.md`, `corpus/knowledge/drift-repin-r20.md`,
  `corpus/knowledge/journal-cursor-window-r16.md`.

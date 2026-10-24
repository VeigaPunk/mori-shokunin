# ConnSiblingOverlap — round 28, wave 1 (connector, leaf)

Seat: MoriR28.ConnSiblingOverlap. Lane HEAD read: `079a47c` (mori), tsukuroi `a99d9e8`, kumitate `fae386a`
(`git log --oneline -1` in each). Scan finished 2026-10-22T18:02:19Z (`date -u +%FT%TZ`). Read-only: no lane,
sibling or fleet file was written except this report. Tools installed or updated: none.

## 1. Result in one paragraph

No sibling lane holds a SOURCES row with any upstream URL of S096, S097, S101, S127, S128, S129, S131 or S140, so
there is no shared row and no row-wording conflict for C1. There are three real cross-lane effects, all through
mori's knowledge entry `oom-victim-selection-r27.md` and tsukuroi's kill-plane entries rather than through rows:
(a) mori's outbound correction of tsukuroi at `oom-victim-selection-r27.md:199-201` rests on the claim that
round-27 ReopenS129 found unsupported (M1), and S150, which supersedes S129, will make that contradiction
visible inside mori; (b) tsukuroi has recorded mori's answer to its open question Q12 for a later round, so the
grounding mori gives that answer now decides what tsukuroi will absorb; (c) S151 (superseding S131) moves into
distribution packaging, which is tsukuroi's ground. C2 has no sibling overlap: no lane has earlyoom case
fixtures or an earlyoom journal parser. One scope rule for the case writers' `why` text follows from tsukuroi's
register.

## 2. Evidence — exact-URL sweep (C1)

- Sibling registries scanned: 20 (`ls -d *-shokunin/corpus/SOURCES.md` lists 21 including mori). The
  directories `mori-shokukin`, `tameshi-shokukin` and `kaidoku-sh2` hold no SOURCES.md (`fd -t f SOURCES.md` empty).
- The pattern set does match mori's own rows (sanity counts in mori SOURCES: `52b1364ba0b1` 1, `proc_pressure` 2,
  `docs/settings\.md` 2, `fs/proc/base\.c` 1, `proc_pid_oom_score` 1, `systemd\.exec\.xml` 1,
  `earlyoom/git/trees` 1, `6962d5cd2ef` 2).
- Over the 20 sibling SOURCES files, every one of the twelve URL tokens (`52b1364ba0b1`, `proc_pressure`,
  `docs/settings\.md`, `fs/proc/base\.c`, `uapi/linux/oom\.h`, `kernel/fork\.c`, `proc_pid_oom_score`,
  `systemd\.exec\.xml`, `systemd-system\.conf`, `earlyoom/git/trees`, `earlyoom\.default`, `6962d5cd2ef`) returned
  0 hits. No sibling SOURCES contains `rfjakob` at all.
- Over every file of every sibling lane (not only SOURCES), the same set returned one file:
  `tsukuroi-shokunin/SKILL.md:2309`, which lists systemd v262 `man/systemd-system.conf.xml` among the files opened
  for its round-25 memory-pressure rows. That use is for the memory-pressure defaults (SKILL.md:2307 names
  `DefaultMemoryPressureLimit=`, `DefaultMemoryPressureDurationSec=`, `MemoryPressureThresholdSec=`); tsukuroi has
  no `OOMScoreAdjust`/`DefaultOOMScoreAdjust` text in SKILL.md, `memory-pressure-r25.md/.json` or its round-25
  lesson (rg, 0 hits). It is the same file as S129's second URL but a different section: no conflict.
- Same repository, different files (adjacent, not shared rows):
  - tsukuroi `corpus/SOURCES.md:121-125,144` hold Linux v7.2 `psi.rst`, `psi.c`, `psi.h`, `cgroup-v2.rst` and
    `mm/oom_kill.c`. Its `psi.rst` digest `11c6b712…` equals mori S143's anchor `11c6b7129103b454`
    (`mori corpus/SOURCES.md:149`); its `oom_kill.c` digest `452f1348…` equals mori S003, as mori's entry already
    states (`oom-victim-selection-r27.md:202-203`). These agree with mori's corrections; none is among the eight.
  - kumitate `corpus/SOURCES.md:14-16,37,144` hold oh-my-pi `main`-branch docs (`docs/tools/task.md`,
    `agent-hub.md`, `task-agent-discovery.md`, `mcp-config.md`), not `docs/settings.md` and not commit `6962d5cd`.
    No sibling file contains `maxJobs`, `maxRunningJobs`, `6962d5cd` or `45c35e40` (rg over all sibling lanes,
    0 hits), so mori PROVINCE.md:338-340 ("its OMP contract entry still has no `async.maxJobs` row") still holds.
  - souji, kama and tameshi hold man7 pages (`proc_pid_fd`, `proc_pid_stat`, `ld.so`, `prctl`, …), none an OOM page.
- Sibling citations of mori's eight ids: none. The only `S127` hit in tsukuroi beside mori text is tsukuroi's own
  S127 (`tsukuroi-shokunin/corpus/SOURCES.md:133`, a blob-pinned row for mori's `system-pressure-r24.md`).

## 3. Shared evidence and whether the wording conflicts, row by row

| mori row (new id) | sibling text that meets it | conflict? |
|---|---|---|
| S096 (S145) | none on IRQ pressure. tsukuroi cites mori `system-pressure-r24.md` by blob at `4f05dd5a`, sections Scope, F2, F9 system half, F10 (`tsukuroi corpus/SOURCES.md:133`) | none; a blob pin does not move when mori's rows change |
| S097 (S146) | none; tsukuroi uses `psi.rst` as the format authority, the same choice S097 records | agrees |
| S101 (S147) | lessons in kagi, kaidoku, kama, kumitate, mado, souji, tameshi and tsukuroi quote the observed refusal `Background job limit reached (100)` (for example `kumitate corpus/lessons/round-37-verifier-spotcheck.md:14`) | none; observed text, not a docs-versus-code reading |
| S127 (S148) | tsukuroi `oom-event-plane.md:116,349`, `kill-event-deep-r8.md:147,260` say the +200 band is scanned or chosen first | already disputed by mori (`SKILL.md:740`, entry :195-197); S148's F3/F4 narrowing and S149's F5 pointer to S003 `mm/oom_kill.c:232-234` strengthen mori's side. tsukuroi S119 is the same bytes as S003 |
| S128 (S149) | none | none |
| S129 (S150) | tsukuroi `kill-event-deep-r8.md:142` quotes the manual, "the OOM score adjustment level of the service manager itself"; Q12 at `:295` leaves the +200 origin open | **yes, through mori's entry** (section 4) |
| S131 (S151) | tsukuroi has no earlyoom packaging row (no `PKGBUILD`/`EARLYOOM_ARGS`/`default/earlyoom` hit about earlyoom); `tools/check-boot-chain.py:74,82` lists earlyoom as an installed package only | none in wording; **scope** (section 5) |
| S140 (S152) | kumitate `corpus/lessons/round-41.md:100-104` (own-work read of the omp 18.12.6 binary): the limit error is thrown in job registration before any job record exists | none; agrees with mori S098. Mechanism semantics are kumitate's (mori PROVINCE.md:335-344) |

The in-place edits being reversed by restoration (computed from committed bytes; first-published commits `df4db54a`
for S096 and S097, `90ed9b77` for S101; `check-row-identity.py HEAD` prints `changed S096 cells=teaches`,
`changed S097 cells=anchor,teaches`, `changed S101 cells=teaches`, `rows=144 changed=3 removed=0 bad=0`):
restoring S096 brings back "an absent irq file is a build-configuration fact"; restoring S101 brings back "docs and
code disagree for values above 100". No sibling cites either first-published sentence, so restoration harms no
sibling. Both re-exposed sentences are cause or contradiction claims, so the superseding rows must retract them.

## 4. Contradiction to name: mori's outbound correction of tsukuroi versus S150

- ReopenS129 M1 (`.ufo/waves/round-27/w2/ReopenS129.md:19-24`): "the systemd.exec(5) default describes the system
  manager" is unsupported; `systemd.exec.xml:1299-1300` names no manager type. The seat noted that the HEAD entry
  repeats it at `:201-203` "about a tsukuroi file this seat did not open".
- That sentence is still at the mori HEAD entry, `oom-victim-selection-r27.md:199-201`: "the `systemd.exec` default
  quoted at `kill-event-deep-r8.md:142` describes the system manager". Fact 3 at `:78` was narrowed in wave 2
  ("names no manager type"), but the Adjacency paragraph was not. The entry now contradicts itself.
- What tsukuroi wrote at `kill-event-deep-r8.md:142` is a correct quotation of the manual. Mori's correction of it is
  the M1 claim.
- ReopenS129 M2 (`:26-31`): S129's "so user units inherit manager+100 unless they set the value" is a derivation.
  Read literally, `systemd.exec.xml:1299-1300` gives the manager's own level (100 for a user manager), not 200.
  S150 will mark that chain [INFERENCE].
- Second-order effect: tsukuroi's register records, for a later round, that mori "answers the lane's open question
  Q12" (`tsukuroi corpus/knowledge/adjacency-mori-oom-r27.md:34`). If the answer reaches tsukuroi through S129 or
  through the `:199-201` sentence, tsukuroi will absorb a claim mori itself has marked inference or unsupported.
  The part of the answer that rests on bytes is S130: the code `src/core/main.c:3063`
  (`saturate_add(a, 100, OOM_SCORE_ADJ_MAX)`, cited at entry :76-77) plus the host read in wave-1
  HostUnitOomAdjust (entry :78).

## 5. Contested scope to name in mori's report

1. **S150 versus tsukuroi Q12:** the +200 origin is mori's answer only as far as S130 code plus the dated host read
   carry it. The manual reading is an inference and goes no further than that. The host's unit OOM settings stay
   with tsukuroi and the operator (mori PROVINCE.md:383).
2. **S151 and distribution packaging:** ReopenS131 F2 (`ReopenS131.md:47-59`) moves the S131 teaches toward "a
   distribution packaging change (on Arch, S126 PKGBUILD:22 appends an --avoid option)". Package content and
   package-backup file state are tsukuroi's (tsukuroi PROVINCE.md:7-14; mori PROVINCE.md:12-15). S151 may state
   what the upstream tag and the PKGBUILD bytes ship. It must not state what this host's `/etc/default/earlyoom`
   holds (F2 already marks that [INFERENCE]), and it must not copy the appended expression's value (privacy bound).
3. **S145 and kernel/boot diagnosis:** S096's current wording lists the cases an absent irq file is "consistent
   with" (no IRQ time accounting at build, PSI disabled at boot, a kernel older than 6.1). Keep it as a list of
   consistent cases. Naming which cause holds on a host is tsukuroi's (mori PROVINCE.md:246-248: "no cause is
   inferred … kernel and boot configuration diagnosis belongs to tsukuroi"). The first-published "build-configuration
   fact" reading broke that rule.
4. **S152 and the harness mechanism:** keep S152 to the clamp site's history. ReopenS140 Low-1
   (`ReopenS140.md:137-143`) shows the floor moved to the job-manager getter in the same commit. What the manager
   counts and enforces is kumitate's (mori PROVINCE.md:335-339).
5. **C2 case text:** earlyoom and systemd-oomd unit state as host diagnosis is tsukuroi's (mori
   PROVINCE.md:369-371; tsukuroi PROVINCE.md:180). Case `why` text should state the rule on invented inputs, never
   this host's state. Two tsukuroi register rows bear on wording: OV4 (`adjacency-mori-oom-r27.md:17`; tsukuroi
   `memory-pressure-r25.md:387`). Under it, a case `why` must not say systemd-oomd monitors nothing at `auto`
   without the `kill`-ancestor and `OOMRules=` qualifiers. OV5 (`:18`): earlyoom 1.9.0 has no `--kernel-oom`
   (mori S114, S137), so no case may expect kernel counters from an earlyoom input. None of the ten A2 rules
   (`.ufo/waves/round-27/contract.md:49-58`) needs either claim.
6. **Bare-id collision:** tsukuroi already has an S145 (`tsukuroi corpus/SOURCES.md:151`, Linux `module-signing.rst`)
   and its own S125/S127. A sibling citation of mori's S145–S152 needs the lane name. The entry's existing rule
   ("every bare id here is mori's", `oom-victim-selection-r27.md:202`) covers mori's side.

## 6. Proposed move (one, bounded)

Ground the +200 answer on S130 and keep it off S150. When S150 lands, also log in the round-28 lesson that the
entry's Adjacency sentence at `oom-victim-selection-r27.md:199-201` is superseded. This needs no edit to the entry
and no edit outside C1's file scope; the contract's C1 is `corpus/SOURCES.md` plus the lesson `## Gate`
(`contract.md:12,20-22`).

- In S150 (the drafting seat owns the cell): apply M2 and L1/L2 as ReopenS129 wrote them. Do not let S150 carry
  "user units default to 200"; say S130 carries it (code `main.c:3063` and the dated host read).
- Text for the round-28 lesson, under the S150 Gate row or a corrections block:

```text
Cross-lane note (S150): `oom-victim-selection-r27.md:199-201` says the systemd.exec default quoted at
tsukuroi `kill-event-deep-r8.md:142` "describes the system manager". ReopenS129 M1 found that unsupported:
systemd.exec.xml:1299-1300 names no manager type, and tsukuroi's line quotes it correctly. Superseded by
S150. The +200 origin offered to tsukuroi for its Q12 rests on S130 (src/core/main.c:3063) and the
round-27 host read, not on the manual. The entry text is unchanged this round (C1 touches SOURCES only);
an append-only entry correction is routed to the next round.
```

- Text for mori's round-28 report, section on adjacency:

```text
Sibling overlap (C1/C2): no sibling SOURCES row shares an upstream URL with S096, S097, S101, S127,
S128, S129, S131 or S140 (20 sibling registries; ConnSiblingOverlap). Contested scope named, not absorbed:
the +200 origin answer to tsukuroi Q12 rests on S130, not S150; S151 states upstream and PKGBUILD bytes
only, never this host's packaged file (tsukuroi owns package state); S145 lists consistent causes and
diagnoses none (tsukuroi owns kernel and boot diagnosis); S152 stays clamp-site history (kumitate owns
the job-manager mechanism). C2 case text states rules on invented inputs, never host unit state.
```

Affected axes: freshness (C1) improves, because the superseding rows stop the outside check finding an internal
contradiction at `:199-201`. Adjacency is held, not harmed: tsukuroi gets an answer that rests on bytes. Calibration
improves, because an inference stays marked across the lane boundary. No axis is harmed: no row id, cell or counter
input changes, and `count-c1.sh` reads only SOURCES and the lesson Gate [INFERENCE from `contract.md:20-22`; the
counter was not run].

## 7. Risks

- The note leaves the entry's wrong sentence in place for another round. Mitigation: it is logged and dated in the
  lesson. Editing the entry now would widen C1 beyond its declared file.
- If the S150 drafting seat keeps the M2 chain as fact, the contradiction gets worse: the row would say 200 while
  the manual sentence it anchors says the manager's own level.
- S151: copying the PKGBUILD's appended expression into the row would breach the privacy bound, because it is very
  likely this host's value [INFERENCE; the host file is never read].
- The tsukuroi pins cited here are at tsukuroi `a99d9e8`; a later tsukuroi commit can move these line numbers.

## 8. Verification for the L1 (not run by this seat)

- `rg -c -e 52b1364ba0b1 -e proc_pressure -e 'docs/settings\.md' -e 'fs/proc/base\.c' -e proc_pid_oom_score -e 'systemd\.exec\.xml' -e 'earlyoom/git/trees' -e 6962d5cd2ef /home/vgpnk/Projects/shokunin/*-shokunin/corpus/SOURCES.md`:
  only `mori-shokunin` should be non-zero (re-run of this seat's sweep).
- `git -C /home/vgpnk/Projects/shokunin/mori-shokunin show <tip>:corpus/knowledge/oom-victim-selection-r27.md | sed -n 199,201p`:
  the sentence should be unchanged, and the lesson should carry the cross-lane note.
- The S150 teaches cell should contain `[INFERENCE]` before the manager-plus-100 chain, and should not contain
  "inherit manager+100 unless".
- The S151 cell should not contain the PKGBUILD's appended option value (`rg -n -- '--avoid ' ` on the row prints
  only the option name, with no expression after it).
- `bash .ufo/waves/round-28/count-c1.sh <tip>`: the move should not change its output.

# AttackPreservation — round 16 critic (wave1)

Seat `MoriR16.AttackPreservation`, critic. Read time 2026-10-20T08:49Z–08:53Z (UTC).
Changes may have been in flight; every quote below is from the working tree
at that read time. Advisory author-lane evidence. It is **not** outside
verification.

Axes attacked: **freshness** (old r10 drift pin), **coverage/calibration**
(universal event coverage), **calibration/discernment** (outside verification),
**operability/adjacency** (identity of the r15 alarm tokens).

## Disclosure of commands run (no journal reads, no tests)

There were no `journalctl` invocations. I ran no census, gate, selftest,
fixture, wrapper, build or formatter, started no background job, and wrote
nothing outside this report. I ran these read-only commands: `git status/log/diff`,
`grep`/`sed` on repo files, `zcat` of local man pages
(`journalctl.1.gz`, `journald.conf.5.gz`), `date -u`, `ls`, and two host-state
reads: `pacman -Q systemd` (→ `systemd 261.2-1`) and `id -Gn` (filtered: only
`wheel` of systemd-journal/wheel/adm). These two are not journal queries. They are
disclosed here because of the L1 clarification and sent to `MoriR16.Lesson`.
Nothing in this report is admissible as verification.

## Verdict summary

| # | Counterexample | Severity | Impacted axes | Smallest safe correction |
|---|---|---|---|---|
| P1 | A green new tool or r16 gate gets read as freshness progress, or as repair of the red r10 pin | guarded (no active defect) | freshness | Keep the current wording. Prove preservation with byte-equal pins, not with a `--drift` re-run |
| P2 | Same token names, different authority: window `positive_*` versus census `positive_*` | **defect (doc), fixable** | operability, calibration, adjacency | One sentence in SKILL/knowledge: different domain and salvage policy; not comparable to census tokens and not a substitute for them |
| P3 | Knowledge note says the census "already reports" a false-unavailable window | **defect (doc), fixable** | calibration, adjacency | Strike the census clause |
| P4 | README says `-q`-hidden **partial** reads "stay unavailable" | **defect (doc), fixable** | coverage, calibration | Reword: a partial read where the anchor is readable is not detected; an OK window may be partial |
| P5 | FR11 identity drift: README keeps "New-since-pin … kill counts … pin-scoped", PROVINCE renames to "new-since-anchor" | **defect (doc), fixable** | calibration, depth | One FR11 title. "anchor", not "pin". "notice/record subsets", not "kill counts" |
| P6 | Before→after metric is tautological at capability absence | tradeoff (already disclosed) | coverage, calibration | Report the case count as capability acquisition, never as N defects repaired |
| P7 | Author-lane reviewers or a green gate get read as outside verification | guarded | calibration, discernment | Keep the "author-lane, not outside" text. Do not use "independently persisted" for L1-owned hashes |
| P8 | Docs opened at systemd 262 are applied to host 261.2 behaviour | tradeoff (disclosed) | depth, calibration | Keep the existing [UNKNOWN]. No behavioural claim about the host binary from v262 text |

## P1 — new tool success ≠ old red drift pin (freshness)

**Counterexample.** The committed r15 `drift-current.json` (exit 1) lists
`+FINDING:JOURNAL_CLASSES_UNMEASURED`, `-FINDING:KILL_SIGNAL_JOURNAL`,
`-FINDING:SEGFAULT_JOURNAL`, `+SURFACE:journal.system`, `+SURFACE:journal.user`
among its tokens. A reader could assume that a journal-window tool "measuring journal
classes" or "observing kill signals" reconciles these tokens. It cannot:

- `--drift` compares only the census's normalized output against
  `corpus/evidence/baseline-r10-20261015T2231Z.json` (that baseline contains
  no `cursor` token: `grep -c cursor` → 0). r16 makes no census cutover, so the
  window cannot change one drift byte.
- `JOURNAL_CLASSES_UNMEASURED` names
  `kernel_victim_text,gpf_text,other_signals,uncataloged_unit_failure`
  (`tools/mori-census.sh:1335`). The window's four predicates (kernel OOM
  notice, unit OOM, unit signal, process SIGKILL) measure **none** of those
  classes. `other_signals`/segfault lineage stays unmeasured.
- The window output is not covered by any drift pin. Its only regression net
  is the r16 fixture gate, so it adds **no** freshness instrument.

**Evidence that this is currently guarded.** SCORECARD r16 draft: "The old r10 drift baseline is
preserved without re-pin; its existing red status is not made green by this
separate capability." SKILL "Window probe (r16)": "changes no alarm, drift
verdict or positive token. The r10 drift pin stays red". QUALITY 41 rejects
green inference from a sibling check. The r15 verifier routed item 5: "a green C1
fixture gate is not a full freshness pass".

**Residual risk.** If L1 re-runs `--drift` this round, host churn can change
the red token set. That delta must not be attributed to r16, in either direction.
**Correction:** show preservation statically. Compare the delivered
`tools/mori-census.sh`, silence oracle, r13/r14/r15 gates and frozen
controls byte-for-byte against `frozen/entering-capability.json`
`production_pins` (census `f1f8d1b6…`, the same digest as the r15 drift receipt's
`sha256_start`). Cite the committed r15 drift receipt unchanged. Freshness stays
**unchanged**, never "improved", for this round.

QUALITY 41 says "until a recorded re-pin with its reason". The r15 verifier
standard is stricter: "a separately reasoned **semantic review** justifies any re-pin".
The verifier's wording should prevail, or QUALITY 41 should cite it. That way
a trivially-reasoned re-pin does not qualify.

## P2 — identity collision: `positive_*` in window versus census (defect)

**Counterexample (static, from committed census selftest).** Take the
input `{valid fe6faa94 record} + {array-valued MESSAGE_ID sibling}` in one
scope. The census yields `kernel_oom_notice=unavailable:record-invalid`,
`positive_kernel_oom=1` and `FINDING OOM_KILL_JOURNAL severity=crit …
alarm_basis=validated-positive-records` (`tools/mori-census.sh:3499-3510`).
The same holds for a foreign-boot sibling: `positive_unit_oom=1`, crit
(`:3512-3521`). This is the r15 admitted behaviour (commit `26f6589`, "retain
valid positive alarms beside unavailable class totals"). Under the r16
interface, a foreign-boot or malformed later record makes the **whole window**
rc2 `UNAVAILABLE` with "no numeric positive totals". So identical
evidence gives a census crit alarm with `positive_kernel_oom=1`, and a window
with no `positive_kernel_oom` at all.

The query domains also differ. The census uses `-b` plus a server-side
`MESSAGE_ID=<id>` match per class (`:1190`, `:1293`), so it covers the whole current boot.
The window uses an unfiltered `--cursor=` read classified client-side, so it covers only
records after the anchor.

**Why it matters.** SKILL says the window counts "reuse the r15 predicates".
That is true per record. But the salvage policy and the domain differ while
the field names are byte-identical. All four names are also in census
`DRIFT_COUNTER_KEYS` (`:2516`), where magnitudes are masked. If anyone later
consumes window output inside the census, the masked count-only change reads
`none` by construction, and r15 positive retention would silently regress.
Today there is no cutover, so this is a latent identity hazard, not a live regression.

**Smallest correction (doc only; the field names are fixed by contract).** Add
one sentence to SKILL "Window probe (r16)" and to knowledge §4: *window
`positive_*` are after-anchor, whole-window-refusing subsets and are a
separate identity from census `positive_*`/`user_positive_*`. They are not
comparable, not summable, and they neither supersede nor feed the r15 alarm
retention.* Renaming to `window_positive_*` would be cleaner, but it is a
contract change, so that is L1's call.

## P3 — false census linkage in knowledge note (defect)

`corpus/knowledge/journal-cursor-window-r16.md:72` ([INFERENCE] section) says
"A false unavailable is a coverage loss **that the census already reports as
`unavailable`**." The census never invokes the window, and SKILL says it "adds no
`SURFACE` or `FINDING` row". So a window unavailable result is reported only on the
probe's own stdout. The sentence invents an alarm-integration path, which is the
conflation that WindowAlarmBoundary is meant to reject. **Correction:** strike the clause, so it reads
"A false unavailable is a coverage loss reported only by the probe's own rc2
`MORI_JOURNAL_WINDOW_UNAVAILABLE`."

## P4 — "partial reads stay unavailable" overclaims (defect)

`corpus/README.md` (new knowledge row) says "… `-q`-hidden
inaccessible-journal **partial** reads stay unavailable or [UNKNOWN]."

**Counterexample.** Local `journalctl(1)` (systemd 261.2) `-q`: "Suppresses …
any warning messages regarding inaccessible system journals when run as a
normal user." Local man: "by default, only root and users who are members of
a few special groups are granted access to the system journal and the
journals of other users." The knowledge note (line 65) correctly argues only the
**fully** inaccessible case: no anchor record, so unavailable. In a partial case,
the file holding the anchor is readable, but some file holding later same-scope
records is not readable or is skipped. That yields a valid first record,
same-boot later records, empty stderr (suppressed) and rc0. The result is
`MORI_JOURNAL_WINDOW_OK` with fewer records. Nothing in the contract detects it. How
often this happens on this host is [UNKNOWN]: it depends on per-file ACLs and on the
user's journal group membership. `id -Gn` showed `wheel` only. Wheel access to the system
journal comes from distro ACLs [INFERENCE], so it is not measured here.

**Correction.** README row: replace "partial reads stay unavailable or
[UNKNOWN]" with "a partial read in which the anchor stays readable is not detected
(stderr is suppressed by `-q`): an OK window may be partial — [UNKNOWN]". The
knowledge note's "No completeness" and "Stderr silence is not an access
proof" already support this. Only the README cell overstates it.

## P5 — FR11 identity drift across indexes (defect)

- PROVINCE (draft): "**FR11 — Remaining new-since-anchor journal semantics**".
- README frontier row (draft): "| FR11 | **New-since-pin journal kill counts**
  via cursors | … Cursor queries stay read-only and **pin-scoped**."

Two titles for one frontier ID create a duplicate authority. In this
repo, "pin" already means the r10 drift baseline. "since-pin"/"pin-scoped" invites
reading the window as anchored on, or reconciling, the drift pin (P1). "kill counts"
contradicts every r16 non-claim: the window counts records and catalog-ID notice
subsets, not kills or victims (`kill-classes-by-message-id-r12.md`: "notice ≠ kill").
**Correction:** align the README FR11 title and boundary with PROVINCE.
Use "new-since-anchor"/"anchor-scoped", and "record/notice subsets", not
"kill counts". The historical wording can stay in the LOG history.

## P6 — capability-absence metric (tradeoff, disclosed)

`frozen/entering-capability.json`: `capability_present: false` (`git
cat-file -e … tools/mori-journal-window.py` → 128). Every finite case fails
"before" by construction, so N→0 measures that the tool was acquired and conforms
to the author-written packs. It does not repair N defects. SCORECARD and SKILL
already say "Absence is capability red, not a historical production bug."
**Keep** that wording. Never report the before count beside r15's behavioural
34→0 as if the two were the same kind of metric.

## P7 — outside verification (guarded)

The wave contract says reports "are advisory author-lane evidence, never outside
verification". SCORECARD: "dispatched author-lane seats are not outside
verification". The ten `Review*`, eight `Attack*` and two sentinel seats are
all dispatched under L1 `MoriR16`, and pack authors coordinate wants with
`WindowHarness`. A green r16 gate is therefore author self-consistency. Outside closure
remains pending, as it did for r15 (`round-15-verifier-spotcheck.md:11-18`:
admission is "not a retroactive waiver"). The r15 outside admission covers r15
C1 only and must not be cited as covering r16.

**Minor wording risk.** SCORECARD says "independently persisted input hashes".
If L1 persists them, they are separately persisted but not independent. Say
"persisted by L1 before runs", and reserve "independent" for the outside
verifier. The LOG phrase "independently of the production census" means
"separately" and is fine.

## P8 — source version (tradeoff)

LOG and knowledge cite systemd **262** man pages. The host runs **261.2-1** (`pacman -Q`).
Knowledge §[UNKNOWN] already says host seek behaviour is "Not measured". The tradeoff
is acceptable only while no claim about host-binary behaviour rests on
v262-only text. Local 261.2 `man journalctl` was checked for `-q` and the private
cursor format, and both match the cited quotes.

## Checked and found consistent (no action)

- SKILL "Window probe (r16)": no census call, no SURFACE/FINDING, r10 pin
  stays red. PROVINCE: "no census cutover". LOG: "The old red r10 pin is
  unchanged."
- QUALITY 42's cursor quote "The format of the cursor is private and subject
  to change." is present at local `journalctl.1` line 723. The QUALITY 41
  source quote matches `lessons/round-15.md:42`.
- The knowledge note keeps "No completeness … nor that no event occurred". Zero is
  "not that nothing happened". The rate-limit/retention docs are explicitly not
  opened. For the record: local `journald.conf(5)` states that messages beyond
  `RateLimitBurst=` "are dropped", so an OK window is not universal coverage.
- The catalog-id hint `d9b373ed55a64e6c8e2e7d70a0fce472` in the spec is wrong.
  Census bytes use `d9b373ed55a64feb8242e02dbe79a49c` (19 occurrences). Several
  pack seats and ReviewFixtures already flag it. If the window tool used the hint,
  every unit positive would be a silent 0 inside an OK window, which would
  be a preservation break of the r15 predicate identity. L1 should confirm that the delivered tool
  uses the census bytes.
- `tools/mori-journal-window.py` was absent at read time (08:52:45Z), so no
  tool code was reviewed.

## Impacted-axes rollup

freshness: unchanged, and must not be claimed (P1). calibration: at risk from
P2/P3/P4/P5 wording until corrected. coverage: bounded capability only (P4, P6).
adjacency: P2/P3 must not imply alarm integration. discernment: P7 guarded.
Nothing here establishes an axis harm on committed bytes. All defects are in
uncommitted draft docs and can be fixed with one-line edits by their owners
(README → FrontierIndex; knowledge → Knowledge; SKILL → SkillRegistry; QUALITY → Quality).

Tools installed or updated: none.

## Owner dispositions (static re-read 2026-10-20T08:54:19Z, working tree)

- **P2 is fixed in SKILL.md:135** (SkillRegistry), which says "separate after-anchor identity … not comparable with, and does not substitute for, the census whole-boot `positive_*` or the r15 alarm retention". It is also fixed in knowledge §4, line 57 (Knowledge).
- **P3 is fixed** in knowledge line 71: "A false refusal is a coverage loss, reported only by the probe's rc2." The census clause is gone.
- **P4 is fixed** in `corpus/README.md:41`: "partial reads are not detected — an OK window may be partial — [UNKNOWN]".
- **P5 is fixed in substance** at `corpus/README.md:342`: "New-since-anchor journal record/notice subsets via cursors", "anchor-scoped", "not kill counts". No `pin` is left in the active FR11 cells. One minor residual remains: the README title and the PROVINCE title ("Remaining new-since-anchor journal semantics", `PROVINCE.md:54`) still differ in wording. They no longer conflict, so I raise no blocker.
- **P1, P6, P7 and P8 need no owner edit.** The open recommendations are for L1: a static byte-pin preservation check instead of a `--drift` re-run, QUALITY 41 aligned with the verifier's "semantic review" standard, "persisted by L1" instead of "independently persisted", and confirmation that the delivered tool uses the census unit-failure ID.
- I confirmed each fix only by reading text. Nothing was executed.

# ConnectCorpusFinal — final cross-file contradiction sweep (round 23, corpus → registry → scorecard)

**Seat:** `MadoR22-2.ConnectCorpusFinal` (connector, leaf member — no subagent dispatch).
**Lane:** `/home/vgpnk/Projects/shokunin/mori-shokunin` (mori-shokunin).
**Scope:** cross-file contradiction sweep among the new knowledge note, the SKILL registry,
the README frontier/Core surfaces, SCORECARD, lesson23 and the immutable original
contract/amendment. Corpus ↔ registry ↔ scorecard consistency only; no code, no frozen
bytes, no production change.
**Deliverable:** this file only. `falsify/ConnectCorpusFinal.md` (lane-relative path; absolute
`/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/falsify/ConnectCorpusFinal.md`).

## Method and bounds honored

Read-only text reads plus read-only git plumbing (`git status --short`, `git rev-parse HEAD`).
Read: `corpus/knowledge/quota-surface-r23.md`, `corpus/knowledge/retention-reconciliation-r22.md`,
`corpus/lessons/round-23.md`, `corpus/lessons/round-12.md:48`, `corpus/README.md`,
`corpus/QUALITY.md`, `corpus/SOURCES.md`, `SKILL.md`, `PROVINCE.md`, `SCORECARD.md`, `README.md`,
`LOG.md:1524-1542`, `tools/mori-quota-surface.py` (static source only), the immutable
`.ufo/waves/round-23/contract.md` and `preseal-amendment.md`, sealed receipts under
`.ufo/waves/round-23/frozen/` and `.ufo/waves/round-23/evidence/`, and wave-cache peer reports
under `.ufo/waves/round-23/build/` (attributed below).

Not done, by bound: **no live host read** of any kind (no `/proc/self/mountinfo`, no `stat`, no
`/sys/fs/btrfs`, no quota command, no `df`); **no session transcript read** (no `.ufo/interactive-sessions`,
no `~/.omp`); no VCS mutation (`git add/commit/push`, `jj`); no writes outside this report; no
production/frozen/oracle/case/rule byte touched; no build, test, lint, formatter, gate or selftest
executed; no delegation. **Tool installs: none** — no pacman/uv/npx/cargo transaction was run and
none was needed (markdown and JSON reading only); the host-wide pacman pause was untouched.
One disclosure: a single `find -name SOURCES.md` enumerated worktree *paths* under
`.ufo/worktrees/`; no worktree file was opened, read or searched, and no `.git`/`.jj`/`.scratch`
content was read.

## Result in one line

The **r23 documentation cutover landed in three of five corpus/registry surfaces**
(`SKILL.md`, `corpus/knowledge/quota-surface-r23.md`, `corpus/lessons/round-23.md`, plus the
`corpus/knowledge/retention-reconciliation-r22.md` alias cutover) but **did not land in the two
surfaces that carry the frontier/Core state the round claims to advance** —
`PROVINCE.md` FR2 and `corpus/README.md` FR2 are byte-unchanged and no round-23 knowledge-index
row exists — so the contract's declared move "FR2 frontier → bounded core" is **undocumented in
the frontier registries**, and SCORECARD still advertises the pre-amendment source range
S077–S084 while the landed registry, lesson and knowledge note carry ten rows S077–S086.

## Axes

| axis | this round's declared move | what the sweep can move |
|---|---|---|
| coverage (held 6) | FR2 quota visibility, frontier → bounded core | whether the advance is *recorded* in the registries that hold frontier state |
| calibration (held 5) | `raw_unallowlisted` removal, schema v2 | whether the alias removal is consistently documented across corpus/registry |
| freshness (held 5) | r23 evidence ↔ docs coherence | whether landed docs match the sealed/measured state |
| disc/adjacency (held 6) | tsukuroi/operator ownership of quota configuration | whether the ownership fence is visible in the refusal document |

## Findings

### F1 — The FR2 advance is recorded in no frontier/Core registry (highest consequence)

**Evidence (byte-exact, read-only):**

- `PROVINCE.md:45` — FR2 row, unchanged:
  `- **FR2 — Quota/EDQUOT observability** (state F2). First evidence: corpus/knowledge/audit-r11.md:218-222. Boundary: df capacity percentages cannot detect quota exhaustion; observe and report only, never change quota state.`
- `corpus/README.md:333` — FR2 row, unchanged:
  `| FR2 | Quota/EDQUOT observability | knowledge/audit-r11.md:218-222 | df capacity percentages cannot detect quota exhaustion; observe and report only, never change quota state. |`
- `PROVINCE.md` Core section (`:20-40`) lists no quota probe; `PROVINCE.md` "Owns (read-only probes)" (`:7-11`) does not mention kernel-visible quota-mechanism state; the file's last appended round section is `## Round22 own-evidence accounting boundary` (`:197`) — **there is no `Round-23` section** (grep count for `Round-23|round-23|quota-mechanism` in `PROVINCE.md` and `corpus/README.md` = **0** each).
- `corpus/README.md` ends at `## Round22 calibration of existing retention ground (not expansion)`; the round-20/21/22 idiom (`:401-402`, `:409-420`) has **no round-23 section** and **no index row for `knowledge/quota-surface-r23.md`** (the r22 note *is* indexed at `:420`).
- `SKILL.md:586` (registry row `quota surface (r23)`) and `SKILL.md:588` (`For quota visibility, read corpus/knowledge/quota-surface-r23.md (S077–S086)`) — the pointer landed in SKILL only.
- `SKILL.md` contains **zero** occurrences of `FR2`; the only `FR2` mention anywhere outside PROVINCE/corpus-README is `corpus/knowledge/quota-surface-r23.md:7`.

**Why it is a contradiction, not a nit.** The wave-1 connector already fixed this as a landing
obligation, not an optional extra: `build/ConnMoriCorpus.md` E5 — "Both say only '`df` capacity
percentages cannot detect quota exhaustion; observe and report only, never change quota state'.
**Any C2 text that says 'quota observability' unqualified contradicts the row it is supposed to
advance. The narrowing must land in these rows (append-only), not replace the boundary sentence**" —
and its verification item 8.3 prescribes exactly this check. The province drafter encoded it as
nine copy-pasteable blocks in `build/DraftProvince.md` (A `PROVINCE.md` EOF append; B1 owns-list;
B2 new Core bullet; B3 FR2 row; B4 Refuses-paragraph quota-configuration carve-out to tsukuroi;
B5 adjacency row; C `corpus/README.md:333`; D coverage-map + `## Round-23 coverage additions`;
plus an append-only fallback). Running that seat's own verification today:

```
$ grep -n 'quota' corpus/README.md PROVINCE.md SKILL.md
corpus/README.md:333:| FR2 | Quota/EDQUOT observability | knowledge/audit-r11.md:218-222 | ...
PROVINCE.md:45:- **FR2 — Quota/EDQUOT observability** (state F2). First evidence: ...
SKILL.md:411/- :412/... (historical), :566 Round23 section, :586 quota row, :588 pointer, :596-602 limits
```

The new pointer and the first-hand anchors appear in **SKILL.md only**; the two FR2 rows still
carry only the audit-r11 anchor. Meanwhile the shipped capability exists
(`tools/mori-quota-surface.py`, 65.1 KB, default `FLEET_ROOT = "/home/vgpnk/Projects/shokunin"`,
`DEFAULT_PATHS = (FLEET_ROOT, "/tmp")`).

**Affected axes:** coverage (the declared frontier→core move is unrecorded where frontier state
lives), adjacency (the `Refuses:` paragraph in `PROVINCE.md:12-15` still refuses OS/driver state
to tsukuroi without the quota *configuration* carve-out, while the shipped probe reads
`/sys/fs/btrfs` kernel state), calibration (registry prose and capability now disagree on what
FR2 now covers).

**Proposed move (one bounded, append-only, parent-owned):** land the drafted province/README
narrowing as drafted — never as a rewrite of the FR2 sentence:
1. `PROVINCE.md` EOF: `## Round-23 appended scope notes (2026-10-21)` (DraftProvince block A) — bounded
   Core advance, input fence, no-cause/no-remediation fence, explicit FR2 **remainder** list
   (per-user/group/project limits and usage and therefore any exhaustion/EDQUOT verdict; EDQUOT
   event attribution; ext superblock quota features; NFS/server-side and overlay/fuse quota;
   enable/disable/remount races; "a qgroups directory is not a limit"), tsukuroi/operator
   adjacency, no census cutover, measurement state.
2. `PROVINCE.md` Core bullet + `Owns (read-only probes)` addition + `Refuses:` quota-configuration
   carve-out + `Adjacent` tsukuroi row (blocks B1–B5) — with the Core row marked as measured,
   not "measurement pending" (the probe has now landed and been measured: 29/30, see F5).
3. `corpus/README.md:333` FR2 row narrowed append-only + `## Round-23 coverage additions` table
   with the `knowledge/quota-surface-r23.md` row (blocks C–D), keeping the round-20/21/22 idiom.

**Risks:** (a) the drafted text was written before the measurement — landing it verbatim would
import "measurement pending" and the pre-amendment wording; it must be re-pointed at the landed
tool and the 29/30 result. (b) Block B4/B5 cites tsukuroi-side lines
(`../tsukuroi-shokunin/PROVINCE.md:3-4,23,41-42,59-60`) whose target revision has since moved
(`build/DraftProvince.md` finding 3) — those cross-lane citations must be re-verified before
landing, and cross-lane files must not be edited. (c) FR2's `state F2` must not change and no
frontier row may be closed (`build/ConnMoriCorpus.md` §7.6; contract forbids promotion).

**Verification (owner: L1/parent; not run by this seat):**
- `grep -n 'quota' corpus/README.md PROVINCE.md SKILL.md` → the FR2 rows in all three now show the
  new pointer **and** the unchanged retained sentence "observe and report only, never change
  quota state" (the `ConnMoriCorpus.md` §8.3 check, currently failing on two of three files).
- `grep -rn 'visibly|visible enablement|quota-mechanism|Quota-mechanism' corpus/README.md PROVINCE.md SKILL.md` → non-empty (currently 0).
- `grep -c 'FR2' SKILL.md` → non-zero (currently 0).
- `git diff --stat <base> HEAD -- corpus/knowledge/audit-r11.md corpus/knowledge/observability-surfaces-r2.md corpus/knowledge/surfaces-r8.md corpus/knowledge/observability-census-r1.md tools/mori-census.sh` → empty (history untouched by the narrowing).
- `grep -n 'quota-surface-r23' corpus/README.md` → one index/coverage row.

### F2 — SCORECARD advertises a stale source range (S077–S084 vs the landed S077–S086)

**Evidence.** `SCORECARD.md:1423`: `| C2 FR2 quota-surface probe (capability; sourced S077–S084) | coverage 6→6 | ... |`.
But: `corpus/SOURCES.md:83-92` carries **ten** mined rows S077–S086, each `used-by` =
`corpus/lessons/round-23.md, corpus/knowledge/quota-surface-r23.md`; `corpus/knowledge/quota-surface-r23.md:1`
(header) says `source: S077–S086 in corpus/SOURCES.md`; `corpus/lessons/round-23.md` Gate opens
"All source rows S077–S086"; `SKILL.md:588` says "(S077–S086)"; `.ufo/waves/round-23/evidence/source-accounting.json`
records `before_rows: 76 → after_rows: 86`, `new_ids: [S077…S086]`; `corpus/SOURCES.md:132`
("Bounded search 14") states ten rows included, "Two extra code sources close escaping/tmpfs-emission gaps".

**Why it matters.** S085 (`fs/proc_namespace.c` — per-mount field emission and path escaping) and
S086 (`mm/shmem.c` — active tmpfs quota token emission) are load-bearing for shipped behavior:
the tool decodes exactly `\040 \011 \012 \134` (`tools/mori-quota-surface.py:233,291`) and accepts
only the four documented hardlimit keys (`:222-225`), and rejects an arbitrary `_hardlimit` suffix
(self-test arm `tmpfs-arbitrary-hardlimit-ignored`, `:1114-1116`). A reader auditing SCORECARD
would conclude those behaviors are unsourced or absent.

**Affected axes:** freshness (scorecard ≠ landed registry), calibration (a claim row that
under-declares its own evidence base).

**Proposed move:** amend the SCORECARD C2 row's source cell to name the landed range and the two
later rows — e.g. `sourced S077–S086 (S077–S084 forward-assigned at 4dc80c1; S085/S086 admitted
round 23 to close escaping/tmpfs-emission gaps)` — and, at landing, add the measured result line
(see F5). SCORECARD is a living ledger; the immutable `contract.md` keeps its original
"S077–S084" wording (that is history and must not be rewritten).

**Risks:** editing a scorecard row is a ledger edit; it must not restate the C2 target as achieved
(see F5) and must not alter any held score.

**Verification:** `grep -n 'S077' SCORECARD.md` → the amended cell; `grep -n 'S077–S08[0-9]' corpus/SOURCES.md`
→ ten rows; the scorecard's held-score line unchanged (`coverage6/operability7/depth5/freshness5/adjacency6`).

### F3 — The new knowledge note carries no pointer to the sealed contradiction that makes its own `recheck` instruction fail

**Evidence.** `corpus/knowledge/quota-surface-r23.md:3` (header) — `recheck: open S077–S086 at pinned
v7.2, compare raw hashes; run the sealed round23 oracles against the explicitly selected committed
tools, never infer a current host state from the documentary table`. But the sealed oracle state is
`.ufo/waves/round-23/evidence/frozen-contradiction.json`: `seal: 22772c10f6e3c1d8d3fe1b72083a6194e9f4e687`,
`measured_revision: 5729e7ff889875d27ab0ead4385db551572892a9`, `original_population_result: {pass: 29, total: 30, primary_pass: 26, primary_total: 27, supplemental_pass: 3, supplemental_total: 3}`,
case `CaseEscapedSpace` (sha256 `8340738a…`), disposition "Strict C2 target unprovable, not admitted".
The note's decision table itself is *correct* on the disputed rule ("Refuse ambiguous duplicate
covering points or inconsistent chosen-parent topology instead of claiming disabled for a hidden
nested mount"), and the shipped tool obeys it (`ambiguous_overmount`, `fstype=null`,
`device_check=not_checked`, `quota_option_keys=[]`, `btrfs_qgroups_mode=null`).

**The contradiction to state, not smooth:** the sealed expectation for that case (exit 1
`QUOTA_ENABLED`, xfs `usrquota` at `/srv/my data`) contradicts the sealed parent-ID rule (selected
mount id 43, parent id 33, longest strictly-shorter cover `/srv` id 42). The rule is right and the
expected row is wrong; both bytes stay unchanged. The note is the durable corpus reference and it
currently gives a reader no way to know that its own recheck instruction terminates in a red case —
that discovery lives only in `evidence/frozen-contradiction.json`, `corpus/lessons/round-23.md`
("Frozen rule versus inconsistent expected topology") and `evidence/parent-strict-target-disposition.txt`.

**Affected axes:** freshness, calibration (a re-checker following the note verbatim would attribute
the red to the note's own rule).

**Proposed move (append-only, note-side, one paragraph):** add to the note a short "Known sealed
case contradiction" paragraph naming `CaseEscapedSpace`, the sealed rule, the measured 29/30 with
primary 26/27 and supplemental 3/3, the disposition file, and the explicit statement that the
note's rule is the authority and the frozen expected row is the inconsistent artifact — with no
suggestion to repair, exclude, relabel or re-score it. Also state that the strict C2 target is
**unprovable**, so a future reader does not read the note as a claim of 30/30.

**Risks:** the paragraph must not become a result claim, must not restate any expected byte as
correct, and must not imply that the co-evolved public-selftest arm `escaped-mount-point`
(fixture input corrected to explicit `259:2`, `evidence/quota-selftest-corrected.json`,
`arms: 49`) is the same case — `corpus/lessons/round-23.md` is explicit that they are different
arms. Two different arms with the same name must not be conflated in the note.

**Verification:** `grep -n 'CaseEscapedSpace' corpus/knowledge/quota-surface-r23.md` → one pointer;
the note still contains no `30/30` or "all cases pass" phrasing; the note's rule sentence is
byte-unchanged.

### F4 — Corpus exit-code vocabulary (M25) is still unscoped against the shipped probe

**Evidence.** `corpus/lessons/round-12.md:48` (M25): "A setup abort never borrows a verdict code
(exit 2) and is neither a case PASS nor FAIL." The shipped probe gives exit 2 to **both**
`QUOTA_SETUP` (setup error) and `QUOTA_STATE_UNKNOWN` (a verdict). `build/ConnMoriCorpus.md` C-1
already adjudicated this: the contradiction is real *as written text*; the required fix is that the
C2 note "scopes M25 to the harness, cites the journal-window precedent, and says `finding_id`
(plus the JSON `exit_code`) is the only discriminator", and "C2 does not discharge D21/M25".
The landed note satisfies only the last part ("Read finding_id, not exit code alone.",
`corpus/knowledge/quota-surface-r23.md`, Exit and evidence vocabulary) — it **never cites
`lessons/round-12.md`/M25 or the journal-window precedent** (`SKILL.md:125` and `:137`:
`rc2 MORI_JOURNAL_WINDOW_UNAVAILABLE` / `rc2 MORI_JOURNAL_WINDOW_SETUP`; "Neither code is a DRIFT,
severity or alarm").

**Affected axes:** calibration (two corpus texts with the same exit code read differently),
adjacency (the same rc2 convention already exists in the lane's other probe).

**Proposed move:** in the same appended paragraph as F3, or a second short paragraph, scope M25 to
the case harness, cite `corpus/lessons/round-12.md:48` and `SKILL.md:125,137`, and state that the
probe's rc2 is neither a DRIFT, severity nor alarm. Do **not** claim D21/M25 are discharged.

**Risks:** the note must not claim M25 is satisfied by the probe; and `audit-r11.md:218-222`
("No closure is claimed for … quota observability …") stays byte-unchanged — the note may narrow
scope, not clear it (the note's header does cite `audit-r11.md:95-99,168,218-222`, which is
correct and should stay).

**Verification:** `grep -n 'M25\|round-12' corpus/knowledge/quota-surface-r23.md` → the scoping
sentence; `git diff` shows `corpus/knowledge/audit-r11.md` untouched.

### F5 — SCORECARD holds a target, the corpus holds a measurement: the r23 result is unrecorded in the score ledger

**Evidence.** `SCORECARD.md:1413-1427` is the Round23 declaration and ends "Targets, not results."
No `29/30`, `26/26`, `CaseEscapedSpace` or `unprovable` string appears anywhere in SCORECARD.md
(grep: none). Meanwhile `corpus/lessons/round-23.md` records "First exercised counterexample after
integration" (C1 26/26, C2 5/30, real control code 2 `input_unavailable`), the second run
"29/30 retains CaseEscapedSpace red", and the strict-C2-unprovable disposition;
`.ufo/waves/round-23/evidence/frozen-contradiction.json` carries the same; `evidence/measure4/`
holds the C1 receipts; `evidence/quota-selftest-corrected.json` records `arms: 49`, exit 0,
`QUOTA_SELFTEST_OK`, measured at `f3dc07c0bf423cc1947d0ffa91afa9ce236fbe3c`.

**Affected axes:** freshness (the ledger shows a declaration while the corpus shows a measurement),
calibration (a reader may take "sealed independent fixture cases capability_absent → all match" as
achieved).

**Proposed move:** at landing, append a Round23 **result** block to SCORECARD (the file's existing
idiom — see the r22 results table above the declaration) that states, without smoothing: C1
original 26/26 with the supplementary guards green and the alias 8→0; C2 primary 26/27 with the
sealed `CaseEscapedSpace` red and the strict C2 target **unprovable at 29/30**; the frozen real
control as a dated observation; the driver exit 1 as expected from that strict red; the co-evolved
public-selftest 49/49 with its separate fixture-input correction; the four unallowlisted hits,
permission RED 11/12, two unknown dispositions, blocked baseline acceptance and
`privacy_clearance=false` all unchanged; no score change, no clearance, no promotion, no r24.

**Risks:** writing "C2 29/30" without the "strict target unprovable" qualifier would read as
admission of the claim; writing the driver exit 1 without naming the frozen-contradiction source
would read as an implementation failure. Both would be false. Also: probe visibility is never
clearance/health/admission.

**Verification:** `grep -n '29/30\|unprovable\|26/26' SCORECARD.md` → the new result block;
held-score line unchanged; `grep -c 'r24' SCORECARD.md` unchanged.

### F6 — `SKILL.md:411-412` still asserts as fact what the new note retracts (pointer is 180 lines away)

**Evidence.** `SKILL.md:411-412`: "The fleet's *actually reported* disk failures are **quota**
events (`EDQUOT`, "disk-quota pressure") — a capacity-percent probe cannot see them, and the quota
numbers are unreadable on this host." `build/ConnMoriCorpus.md` C-2 already flagged this as "real;
wording risk" — "The empirical EDQUOT sentence has no receipt". The new note contradicts the
categorical half: "The historical census selftest's `Disk quota exceeded` abort is **evidence of
a failed write, not an identified filesystem/mechanism/cause** (`audit-r11.md` anchors above)."
`SKILL.md:596-602` does carry a caveat ("The old `:411` statement about fleet failures is dated
historical evidence, not a universal current failure diagnosis") — but it sits in the Round23
section, ~180 lines below the sentence it qualifies, and the sentence itself has no inline pointer.

**Affected axes:** calibration (two documents in the same repo, same lane, different claim strength
about the same event), freshness.

**Proposed move (optional, smallest form):** append one clause at `SKILL.md:411-412` — e.g. "— dated
historical evidence (r23: a `Disk quota exceeded` abort is a failed write, not an identified
mechanism or cause; see `corpus/knowledge/quota-surface-r23.md`)" — instead of editing the
historical wording. Do **not** delete or rewrite the original sentence; it is evidence.

**Risks:** SKILL.md is the operational registry; an edit there is visible to every lane reader.
Append-only keeps the historical claim intact while removing the ambiguity. If the parent prefers
zero SKILL edits in this round, the caveat already at `:596-602` is a defensible floor — record the
choice rather than leaving it implicit.

**Verification:** `grep -n 'actually reported' SKILL.md` shows the original sentence plus the
pointer; `grep -n 'not an identified filesystem/mechanism/cause' SKILL.md` or the knowledge note
still resolves the contradiction.

### F7 — The landed knowledge note's decision table omits scored behaviors it does not name

**Evidence.** The sealed case corpus scores 17 distinct basis tokens
(`grep -rho '"basis": *"[^"]*"' .ufo/waves/round-23/frozen/quota-cases/` → `xfs_noquota_option` ×6,
`xfs_quota_option` ×5, `tmpfs_quota_option` ×3, `ext_quota_option_unverified` ×3,
`btrfs_qgroups_dir_absent` ×3, `xfs_conflicting_quota_options` ×2, `unsupported_fstype` ×2,
`tmpfs_quota_options_absent` ×2, `ext_quota_superblock_unobservable` ×2, `btrfs_qgroups_enabled` ×2,
`btrfs_device_unmapped` ×2, `ambiguous_overmount` ×2, `xfs_quota_options_absent`, `no_covering_mount`,
`device_mismatch`, `btrfs_qgroups_enabled_unavailable`, `btrfs_qgroups_disabled`). The shipped tool
implements all of them (`tools/mori-quota-surface.py:437,498,510,521` and the classification table),
and the frozen real control adds `btrfs_subvolume_skipped` (`frozen/c2-expected-real.json`).
The note's table names none of these tokens; it describes them in prose and omits, in particular:
the XFS **mixed enforced/noenforce precedence** (sealed `CaseXfsMixedEnforce`; amendment: "Mixed
enforced/noenforce means SOME quota-type enforcement flag is set, not all"), the `device_check`
vocabulary (`match` / `mismatch` / `not_checked` / `btrfs_subvolume_skipped`), and the `ext_*`
basis split (`ext_quota_option_unverified` vs `ext_quota_superblock_unobservable`).
`SKILL.md:602` and the note promise "Fixed per-path basis tokens", but the durable corpus reference
does not carry them.

**Affected axes:** calibration (the note is the durable reference a future re-checker reads), depth.

**Proposed move:** extend the note's decision table with the **missing rows only** — mixed XFS
precedence, the ext basis split, `no_covering_mount`, and the `device_check` vocabulary — using the
token spellings already in the sealed cases and the tool. Do not re-list what the table already
covers, and do not restate any frozen expectation as a rule.

**Risks:** a token list that drifts from the tool is worse than none; the added rows must be
transcribed from the tool's own string constants (`grep -n` on `tools/mori-quota-surface.py`) and
checked against the sealed case tokens. Do not introduce a token the tool does not emit.

**Verification:** `diff <(grep -rho '"basis": *"[^"]*"' frozen/quota-cases/ | sort -u)` against the
token list in the note → every scored token appears in the note; `grep -c 'basis' tools/mori-quota-surface.py`
unchanged.

## Contradictions preserved (not smoothed, not resolved here)

1. **Frozen `CaseEscapedSpace`**: the sealed expected row (exit 1 `QUOTA_ENABLED`, xfs `usrquota`
   at `/srv/my data`) contradicts the sealed parent-ID rule (selected id 43, parent id 33, longest
   strictly-shorter cover `/srv` id 42 ⇒ `ambiguous_overmount`). Rule authority, expected bytes and
   the red case all stay unchanged; no special-casing, exclusion, relabelling or rewriting. Strict
   C2 target remains **unprovable at 29/30** (primary 26/27, supplemental 3/3).
2. **C1 calibration**: original 26/26 with the supplementary code-bound/output guards green and the
   misleading alias 8→0; the r22 oracle/real/refinement checks still read the removed key and run
   only at their bound revision `da40bb20f81da125d798f73cd1653655be1255ca`. Original26 denominator
   stays distinct from the supplementary guards.
3. **Open debt unchanged**: four unallowlisted retention hits (raw 95 / allowlisted 86 / non-author 5),
   original permission control RED 11/12, two unknown dispositions, baseline acceptance blocked,
   `privacy_clearance=false`. Probe visibility/accounting consistency is **not** clearance, health or
   admission, and no r24.
4. **Quota selftest vs frozen case**: the co-evolved public-selftest arm `escaped-mount-point`
   (fixture input corrected to explicit `259:2`; `evidence/quota-selftest-corrected.json`, 49/49) is
   **not** the frozen `CaseEscapedSpace` and must never be used to claim the frozen topology case
   was fixed or that its expected value changed.
5. **The immutable original `contract.md` / `preseal-amendment.md`** keep their original wording
   (including "sourced: S077–S084" and the original ext/btrfs rows). Where the landed corpus has
   moved past them (S085/S086, ext→unknown, btrfs enabled-first, mode never read in real mode), the
   amendment and the source rows govern; the original stays byte-unchanged as history.

## False positives checked and dismissed (so no later round "fixes" a correct anchor)

- `SKILL.md:556` ("Field caveats … `raw_unallowlisted` …") is the **historical r22 section**,
  explicitly superseded by the r23 section at `:566-575` ("The round22 registry/field caveats above
  are historical v1"). Not a contradiction.
- `corpus/knowledge/retention-reconciliation-r22.md:27,35` (old alias described) is historical
  schema-v1 prose, and the same file's `## Round23 API correction — schema-v2 clean cutover`
  section states the removal, the retained 4-vs-9 populations, absolute `--repo "$PWD"`, and that
  r22's driver does not stage a historical tool from `--revision`. The amendment's mandatory docs
  cutover for the r22 note **has landed**. Not a contradiction.
- `corpus/SOURCES.md:83-92` status `mined` / `used-by` naming both r23 notes is the intended
  registry state (rows are mined; the note exists and cites them). Not a contradiction.
- `corpus/lessons/round-23.md` M-citations to `QUALITY70` (population identity, `corpus/QUALITY.md:282`)
  and `QUALITY55` (acceptance examples derived by applying the frozen rule, `corpus/QUALITY.md:176`)
  resolve to real criteria. Not a contradiction — but note that criterion 55 is exactly what the
  `CaseEscapedSpace` expectation violates, which is why the lesson keeps the rule and reports the
  red instead of repairing the expectation.
- `SKILL.md:411-412`'s "the quota numbers are unreadable on this host" remains true after r23: the
  probe reports mechanism state, never per-ID limits or usage. Only the mechanism-attribution half
  of that bullet is retracted (F6).

## What I did not do (and why)

- No live host read, no quota command, no `df`, no mountinfo/sysfs read — the wave reserves live
  host reads to `RerunPinnedDriver`, and this item names none. The frozen real control was read as a
  **file**, not re-observed.
- No build, test, lint, formatter, gate, selftest or driver invocation: this item authorizes none.
  The oracle/selftest numbers cited above are quoted from the sealed receipts, not re-measured.
- No edits to `PROVINCE.md`, `corpus/README.md`, `SKILL.md`, `SCORECARD.md`, the notes, lessons,
  frozen bytes or tools — this seat is read-only and the parent integrates.
- No delegation (leaf member), no `agent://all`, no peer traffic beyond this report.

## Handoff for L1 (ordered, all parent-owned)

1. **F1** — land the DraftProvince blocks A–D (re-pointed at the landed tool and the 29/30
   measurement); this is the move that makes the declared coverage axis real in the registries that
   hold frontier state.
2. **F2** — amend the SCORECARD C2 row's source range to S077–S086.
3. **F5** — append the Round23 result block to SCORECARD with the unprovable-C2 qualifier.
4. **F3 + F4** — one appended paragraph in `corpus/knowledge/quota-surface-r23.md` (known sealed
   contradiction + M25 scoping + the two missing vocabulary rows of F7), with no change to the
   note's rule sentences, no restatement of frozen expectations, and no conflation of the
   co-evolved selftest arm with the frozen case.
5. **F6** — optional single-clause pointer at `SKILL.md:411`; if skipped, record the choice.

None of the five changes alters a frozen byte, a case, a rule, an oracle, a denominator or a held
score; all are append-only or ledger-text edits, and all are verifiable by the greps quoted above.

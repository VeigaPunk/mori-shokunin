# w2 / RevLesson — review of `corpus/lessons/round-47.md` at T

Seat: RevLesson (leaf, reviewer). 2026-10-25. Lane repo `/home/vgpnk/Projects/shokunin/mori-shokunin`.
Target: `corpus/lessons/round-47.md` at T = `68d66ca53d89be5c34a62f46af7c37449d9f9b63` (80 lines; worktree
copy byte-equal to T, `diff` empty). Every cited evidence file opened at T via `git show T:<path>`
(extracted to `.scratch/r47w2-RevLesson/t/`); E/F bytes extracted likewise. Live network re-checks run
by this seat: `git ls-remote` tag peel, raw oom.h fetch, ROMA PDF fetch + pdftotext. No lane tool was
re-run (scoring is other seats' work); no repo/jj/git mutation; no tools installed.

## Verdict summary

The lesson is overwhelmingly supported: every SOURCES-row claim, every count, every receipt path I
opened matches its cited evidence, and all three "shown able to fail" fixes (M1, M2, M3) have
committed red receipts that show the claimed failure. Four findings, none fatal: one routed summary
misstates its cited report (F1), M4's seat attribution is stated as fact but is only inferable (F2),
M5's "Recorded as named limits of P-C2" overstates where the limits are recorded (F3), and the
spot-check citation is imprecise (F4).

## Findings by severity

### F1 — breaks (medium) · lesson lines 76–77: routed ExecPinTiming summary contradicts its citation

Lesson: "`w1/ExecPinTiming.md`: one bound command (`count-c3.py` mutant) **varies which two arms fail
across runs**; its pinned tally line `C3_SELFTEST pass=17 fail=2` is stable."

The cited report says the opposite about the arms — `w1/ExecPinTiming.md` §3: "Difference is confined
to the two `FAIL` arm **detail lines** … The verdict line `C3_SELFTEST pass=17 fail=2`, **both FAIL
arm names, and rc=1 are identical across rounds**." What varies is only the throwaway fixture-repo
hash printed inside the detail lines (`7a3d0cc…`/`df73cc01…` in round 1 vs `054ac3c3…` twice in
round 2). The failing-arm identity does not vary.

- Reproducer: read `.ufo/waves/round-47/w1/ExecPinTiming.md` §3 (Determinism), sentence quoted above.
- Verdict: **breaks** as written. The stable-tally half of the sentence holds.
- Fix: reword to "…varies the debug detail (throwaway fixture hash) in the two failing arms' lines
  across runs; the failing arm names, the verdict line `C3_SELFTEST pass=17 fail=2` and rc are stable."

### F2 — attribution stated as fact without committed evidence (minor) · lesson line 67 (M4 evidence)

Lesson: "Seat **MutPinSemanticCell** edited the tracked `tools/mori-pin-check.py` (deleted
`bound = []`) …"

What is well-evidenced (three committed witnesses, all at T): the working-tree tool was mutated at
2026-10-25 16:43:57 to sha256 `104cf3dd…` with `bound = []` removed from `pin_commands`, crashed runs
with `NameError: name 'bound' is not defined`, and was restored to the frozen `e3ef425a…`
(`w1/LabPinStability.md` run2 + Ambient finding; `w1/ExecPinTiming.md` "Note on instrument bytes";
`w1/ExecC1Controls.md` §1 drift table).

What is **not** evidenced: the seat name. All three witnesses say "a sibling wave seat" /
"another in-flight seat" and name nobody. No `w1/MutPinSemanticCell.md` report exists in the tree;
`w1-results.json` for MutPinSemanticCell reads `"output": null` with note "orchestrator kernel
restarted mid-wave; seat output was delivered to the orchestrator session but not retained — read the
seat report file in the wave dir" (no such file exists). The attribution is a plausible inference
(the seat exists in `w1-spec.json`/`w1-dispatch.json` as a mutation-tester; the mutation window falls
inside the wave), but the lesson states it as observed fact.

- Verdict: mutation/restoration **holds**; named-seat attribution **breaks** as stated fact — mark it
  inferred, e.g. "attributed to MutPinSemanticCell (wave-spec mutation-tester; its output was not
  retained, `w1-results.json`); the committed witnesses name no seat".

### F3 — "Recorded as named limits of P-C2" overstates the record (minor) · lesson line 68 (M5 fix)

The frozen contract's P-C2 **Named limits** (`.ufo/waves/round-47/contract.md`) name only: no prose
check, no lifecycle-ordering check, no host-kernel check. The three successor-counter needs M5 lists
(used-by arm, 0–3-space row matching, one-path-per-cell) appear in **no** committed artifact labelled
"named limits of P-C2": a grep over the T tree (excluding `.scratch/`) for `used-by arm` /
`one-path-per-cell` hits only the M5 row itself and `w1/MutC2Source.md`'s mutant table.

- Verdict: **breaks** if read as "the contract records them"; holds only if read as "this row records
  them". Fix: "Recorded here as successor-counter requirements (the frozen contract's Named limits do
  not carry them)."
- Note: M5's fix honestly says "Not fixed", so the able-to-fail red-receipt rule does not apply to it;
  its three evidence citations all verify (see §Verified).

### F4 — spot-check citation imprecise (minor) · lesson line 57

"No non-author spot-check of this round's gate decisions exists yet; the hyaku closure session is the
outside check (**LEARNING.md**)." The absence claim holds (no spot-check seat in `w1-spec.json`/
`w1-results.json`; `corpus/lessons/` at T has only `round-46.md`, `round-46-verifier-spotcheck.md`,
`round-47.md`). But LEARNING.md (fleet root, 88 lines) contains **zero** occurrences of "hyaku" or
"closure session"; it documents the outside spot-check practice (`## Discernment is checked from
outside`: each round a non-author spot-checks ≥1 admit + ≥1 reject). The "hyaku closure" role is
defined in `scripts/hyaku/closure-prompt.md:1` ("You are the hyaku non-author integrator of record
(the protocol lane's closure role)"). Substance holds; cite both files or drop "hyaku" from the
LEARNING.md attribution.

## Verified claims (evidence opened; all hold)

Class vocabulary: M1 `number-drift`, M2 `survivor`, M3 `attribution`, M4 `scope`, M5 `survivor` — all
five in the CORPUS.md mistakes.md §5 vocabulary. Table shape conforms (class · evidence · captured-by
· fix).

**Header (lines 3–6).** Contract, both frozen instruments, controls and v7.2 copies all committed in
freeze `63eecf27` (`git show --stat`: contract.md, count-c2.py, 10 controls, 13 evidence files, 4
source copies, tools/mori-pin-check.py — 25 files). Frozen sha256s reproduce: `git show
63eecf27:tools/mori-pin-check.py | sha256` → `e3ef425abde30974…` (= contract.md:14); count-c2.py
in-script `PINS` equal the four committed copies' sha256s I computed (`82f04ad4…`, `452f1348…`,
`439ae8ec…`, `cef1a2cf…`).

**S475 (line 14).** Live `git ls-remote https://github.com/torvalds/linux 'refs/tags/v7.2*'` →
`refs/tags/v7.2^{}` = `8d3ae59288f1e7d58d76558a6ee96d533bc5019f` ✓ (annotated tag; peel matches).
Live fetch of the raw URL → sha256 `82f04ad4…`, byte-equal to the committed copy (`diff -q` empty).
Quote at oom.h:76–77 exact (`TRACE_EVENT(mark_victim,` / `TP_PROTO(struct task_struct *task, uid_t
uid),`); `grep -c '^TRACE_EVENT('` → 8 ✓. Corroborated by `w1/ExecLiveRefetch.md` (all four copies
live-matched) and `w1/ScribeRowS475.md` §1.

**S476 (line 15).** Committed copy `mm_oom_kill.c`: line 774 = `trace_mark_victim(tsk,
cred->uid.val);` inside `mark_oom_victim` (def :751) ✓; line 582 = `trace_start_task_reaping(tsk->pid);`
inside `oom_reap_task_mm` (def :562) ✓. S003-overlap note ✓: S003 row (SOURCES.md:9) carries the same
oom_kill.c URL with anchors `:447,935-936,945` only. page_alloc/base attributions also check out
(`should_compact_retry` def :4202 → call :4265; `should_reclaim_retry` def :4581 → call :4630;
`__set_oom_adj` def :1106 → call :1158).

**S477 (line 16).** Receipt `evidence/host-tracefs.txt` (2026-10-25T16:37:38-03:00, kernel
7.2.11-arch1-1): `mark_victim/format` carries `field:uid_t uid;	offset:48;	size:4;	signed:0;` ✓;
`sudo -n cat …/events/oom/enable` → `0`, rc=0 ✓; eight event dirs listed ✓.

**S478 (line 17).** Re-downloaded the publisher PDF myself with a browser UA → sha256
`1603404dd25b3a0dff93f2dcb23c75b671d4e2d78da3cce8f461e87ebde6add2` ✓ (= row and lesson `1603404d…6add2`);
`pdftotext` → 1405 lines; lines 139–141 contain exactly the claimed quote with "such as" ✓; printed
p. 3016 §I ✓ (per `w1/ScoutROMA.md` §2, quote block). CC BY 4.0 ✓ (Crossref license + PDF footer,
ScoutROMA §1). Page-count error in staged S507 ("4 pages" vs 14) documented in ScoutROMA §4 ✓.

**S005 change (lines 21–23).** `diff` E→T `corpus/SOURCES.md` = exactly 6 lines: S005 row
(`queued`→`mined`, `—`→`corpus/knowledge/oom-tracepoints-r47.md`) + appended S475–S478. Rule 2
compliant and completely logged ✓. Byte-identity claim ✓: `w1/ExecS005Status.md` §2–3 (c03c1a14
fetch sha256 `82f04ad4…` = v7.2 copy, `diff` empty); anchors `:76,82-105` hold ✓ (§5). The
`after-appendonly.txt` `appendonly_violations=18` is pre-round-47 history, not a contradiction:
`ExecS005Status.md` §6 shows `round_changed=[]` at both E and F.

**Collision check (lines 29–32).** `assimilation/reg-ids` = 247 lines, `staged-ids` = 136,
`collisions` = exactly `S471 S472 S473 S474` ✓. Guard proof ✓: `w1/ExecCollisionGuard.md` §1 —
0–3-space pattern catches the indented `  | S002 |` (nonempty collisions), column-zero pattern
misses it (empty, false green), exact commands and outputs in the report.

**Renumber (lines 33–35).** Staged rows read in `/home/vgpnk/Projects/shokuknow/merge/mori/SOURCES.append.md`
(read-only): staged S475 = Aliyun XXL-JOB workflow docs, S476 = Alibaba Cloud multi-step transaction
docs, S477 = `xfs_quota(8)` — all unrelated to OOM ✓ ("collide by number only"). Staged S507 = ROMA
full text (the DOI) ✓. "No other staged row is appended" ✓ (SOURCES diff adds only S475–S478).

**Admit S478 (lines 36–38).** Registry row (SOURCES.md:257): opened 2026-10-25, located quote,
`recheck` `180d`, `used-by` exactly `corpus/knowledge/oom-tracepoints-r47.md` ✓; all four new rows'
used-by name exactly that entry ✓.

**Reject staged entry (lines 39–43).** Staged
`knowledge/corpus/knowledge/oom-tracing-tracepoints-r42.md`: title "…is three named tracepoints",
Claim "exactly three named tracepoints" ✓; its own quoted sentence says "such as" ✓; refuted by eight
`TRACE_EVENT`s ✓. LSM-hook remedy + overhead figures present in staged S501/S507 teaches for
re-proposal ✓.

**Reject S501 (lines 44–46).** Staged S501 = ROMA abstract-level record ("not the full text
(paywalled)"); lane S262 (SOURCES.md:243) = same document, same abstract-level scope ✓;
`MERGE-REPORT.md:111` is exactly the `S501 → S262` "source the lane already holds" row ✓;
`w1/ScoutStagedTheme.md` §4.3 concurs ✓ (returned, as the lesson's "if returned" anticipates).

**Quarantine slice (lines 47–50).** `assimilation/quarantine-slice` = 3 rows `S244`, `S262`, `S268`,
each with the prose class "the cited source could not be fetched, so no quote was checked" ✓.

**considerthese (lines 51–53).** `considerthese/2026-10-25.md` lines 44–46 = suggestion 1, text
matches ("Add a registry pin check … list any mismatch by line number") ✓; implemented as
`tools/mori-pin-check.py` + QUALITY 123 (QUALITY.md:1028, cites the suggestion and lesson M1/M2) ✓;
`w1/ScoutConsider.md` carries the trail (§1: no earlier implementation; §2 adoptions) ✓.

**M1 (line 64).** `w1/RevPinHistory.md` E1: `265a955c` bytes print `pass=15 fail=0`, `d72ac167` bytes
print `pass=22 fail=0` (both re-run from extracted bytes); E3: pin written once at `265a955c`
(line 889), never updated, `SKILL.md:912` at E carries it; E4 reproduces the do-nothing receipt.
Red receipt ✓: `evidence/control-c1-donothing.txt` — `pin line=912 … state=mismatch pinned='pass=15
fail=0' observed='pass=22 fail=0'`, `PIN_CHECK=unmet … mismatches=1`, rc=1, at `--rev 2d85e33` —
exactly "red at 2d85e33 (mismatches=1, line 912)". Green ✓: `evidence/after-c1-v1-frozen.txt` —
frozen v1 at af2250d8, line 912 `state=match pinned='pass=22 fail=0'`, `PIN_CHECK=met … mismatches=0`,
rc=0; SKILL.md:912 at T reads `pass=22 fail=0` ✓. Captured-by ✓: QUALITY 40 (QUALITY.md:102) exists;
"nothing ran it on registry cells" grounded by ScoutConsider §1.2 (count-repins never re-ran anything,
did not cover :912).

**M2 (line 65).** All cited reports opened: `w1/CritC1Predicate.md` (v2/v3/v7/v8 MET — FALSE GREEN;
v4 weakened `pass=22` MET; receipts abridged) ✓; `w1/SentPinExec.md` F3 (digest paths escape the
tree, `../../../etc/passwd.txt` probe) ✓; `w1/RevPinCheckCode.md` M1 (compat echo wins, `seen[-1]`),
M3 (fenced tables read), L1 (entry column hard-coded `cells[2]`) ✓. Committed red state ✓: the five
junk control files at `controls/c1-junk/` diff against the freeze SKILL.md exactly as described
(v2 `.scratch` rebind, v3 `python3 -c` echo, v4 `pass=22` without `fail=0`, v7 entry-cell rebind, v8
lowercased-token hide + duplicate echo — all keep `pass=15`); `evidence/v1-junk/` shows v2/v3/v4/v7/v8
`PIN_CHECK=met` (false greens) with v1-honest met and v0/v5/v6 unmet; `evidence/v2/` shows all seven
junk variants `unmet` and v1-honest `met` ✓. "v2 selftest 34/34 adds twelve arms" ✓ (v1 selftest 22
per RevPinCheckCode; 34 pinned and observed at SKILL.md:938 in both after-receipts). "P-C1 stays
scored by the frozen v1 bytes" ✓ (after-c1-v1-frozen.txt).

**M3 (line 66).** Staged entry "exactly three" ✓; S478 sentence "such as" ✓; header eight ✓. Fix
QUALITY 124 ✓ (QUALITY.md:1041, cites lesson M3, "Shown able to fail" names the control). Red
receipt ✓: `evidence/control-c2-three-at-freeze.txt` — frozen counter at F with
`--entry controls/control-c2-three.md` (the staged claim as a 3-row table, opened) →
`name_mismatch=5`, rc=1 ✓ (8 events − 3 rows).

**M4 (line 67).** Mutation/restoration evidence ✓ (three witnesses, §F2 above); frozen sha
`e3ef425a…` recomputed ✓; while-mutated `104cf3dd…` recorded in `w1/ExecPinTiming.md` and
`w1/ExecC1Controls.md` §1 ✓. Quoted context text ✓: `w1-spec.json` contains "Write ONLY your own
report file (plus scratch under /home/vgpnk/Project…". "Next wave contexts tell mutation seats to
`cp` the target into `.scratch/<seat>/`" ✓ — observed in this wave's own w2 assignment. Seat-name
attribution: see F2.

**M5 (line 68).** `w1/MutC2Source.md` (b): mutant "Skip used-by check" → `C2_SELFTEST pass=13 fail=0`
exit 0, "Survived; coverage finding" ✓; pristine/restored sha `fc77b933…` = contract pin ✓.
`w1/RevCountC2Code.md`: 4-space-indented S475 row → `sources_row` returns None (reproducer in
report) ✓. `w1/CritC2Predicate.md` V4: correct path + bogus `mm/vmscan.c` citation in the same cell
→ `C2=met` (undetected) ✓. "Not fixed" is honest; no red receipt claimed, none needed. Wording issue:
see F3.

**Routed RevContract (lines 72–75).** Both receipts exist and say exactly what the lesson claims:
`evidence/control-c2-donothing.txt` (at E) → `failed=entry_absent,pins,source_row`, rc=1;
`evidence/control-c2-donothing-at-freeze.txt` (at F) → `failed=entry_absent,source_row`, rc=1 ✓.
"Both receipts exist; no contract change" ✓.

**Routed ExecPinTiming (lines 76–77).** Stable-tally half ✓ (`C3_SELFTEST pass=17 fail=2` identical
across rounds, per the cited report). Arm-variation half: see F1 (breaks).

**Routed ConnCrossClaim (lines 78–80).** `w1/ConnCrossClaim.md` §6.2 recommends exactly not
registering `count-c2.py` in SKILL.md ✓. `w1/ExecRegistryAudit.md` §1: auditor at freeze →
`REGISTRY=unmet … unregistered=2` (both instruments fail with "no row names …") — the auditor does
require every instrument row ✓. Kept registered ✓: SKILL.md at T carries both rows ("registry pin
reconciler (r47, C1)", "r47 tracepoint catalogue (C2)"); `evidence/after-registry.txt` →
`registered=2 unregistered=0 … REGISTRY=met`, rc=0 ✓.

**Knowledge entry (C2 surface, cited via used-by).** `corpus/knowledge/oom-tracepoints-r47.md` opens
with `source:` (citing S475…S005) / `verified-at: 2026-10-25` / `recheck:` ✓; header first cell
`tracepoint`, 8 rows ✓ — consistent with every row that cites it.

## Residual risk and verification gaps

- I did not re-run `count-c2.py` or `mori-pin-check.py` at T (scoring seats own the live runs); the
  C1/C2 green receipts I checked are measured at af2250d8, whose tree-equals-T property for measured
  files I did not independently verify byte-for-byte (assignment states it; the SOURCES.md and
  SKILL.md diffs I ran E→T are consistent with it).
- The v1/v2 junk matrix was verified from the committed control files and both receipt sets, not
  re-executed by me.
- S478's pdftotext line numbers were re-verified from my own live download; the printed-page (3016)
  and §I attributions rest on ScoutROMA's extraction (consistent with my lines 139–141 landing in
  the Introduction paragraph).
- Line 27's "nothing written there" (shokuknow package) is a process claim; corroborated only by
  package mtimes (all 2026-10-24T23:33, pre-wave) — not independently provable.
- Minor observation outside the lesson: `w1/ScoutROMA.md` §6 abbreviates the PDF sha256 as
  `1603404d…eadd2` (typo for `…6add2`; the full hash elsewhere in that report and in the registry
  row is correct). No lesson text is affected.

Scratch: `/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r47w2-RevLesson/` (extracted T/E/F
bytes, live fetches). Only this report file written in the lane tree.

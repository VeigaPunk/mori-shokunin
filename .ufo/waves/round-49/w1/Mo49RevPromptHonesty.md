# Mo49RevPromptHonesty — plan-vs-contract conformance review (mori round 49, wave w1)

Seat: `Mo49RevPromptHonesty`, reviewer, leaf (no subagents, no dispatch).
Scope: round prompt `/home/vgpnk/Projects/shokunin/.ufo/prompts/mori-round-49.md` §2 (lines 9-40), §2b
(42-78), §4 (99-130), §6 run-7 (141-165) and §9/§10 (420-541), against the frozen plan:
`/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-49/contract.md` (frozen at
`0df17b7b4e667dd0aaaef0adc7d7d9973e6aa115`) and the wave-1 seat plan generated from the frozen
`build-w1-spec.py` (`.ufo/waves/round-49/w1-spec.json`, 49 items; untracked at review time).
Review snapshot: 2026-10-25T21:58:34-03:00, lane tip `0df17b7b` (= freeze), remote `refs/heads/master`
= `0df17b7b`. Wave 1 was still in flight and the L1 had begun integrating data into the working tree
(`M corpus/SOURCES.md`, `?? corpus/knowledge/journal-reach-r49.md`), so the frozen bytes reviewed here are
the freeze commit, not the working tree. Nothing in the lane was written except this report and
`.scratch/r49-Mo49RevPromptHonesty/`. No tool was installed; `pacman` was not invoked.

Frozen-byte integrity (read-only):

```
$ cd /home/vgpnk/Projects/shokunin/mori-shokunin && sha256sum -c .ufo/waves/round-49/evidence/freeze-sha256.txt
# 0 lines not ": OK"        (31 hashed files, all match)
$ git show -s --format='%h %ai %ci' 0df17b7b
0df17b7b 2026-10-25 20:30:53 -0300 2026-10-25 21:36:32 -0300
$ git ls-remote origin refs/heads/master
0df17b7b4e667dd0aaaef0adc7d7d9973e6aa115	refs/heads/master
$ stat -c '%y %n' .ufo/waves/round-49/w1.ready .ufo/waves/round-49/w1.ready.dispatched
2026-10-25 21:36:48 …/w1.ready
2026-10-25 21:48:31 …/w1.ready.dispatched
```

## Checks that pass (verified against frozen bytes)

| Prompt item | Verdict | Evidence |
|---|---|---|
| 1-3 claims, distinct axes (§2:11-15) | PASS — 2 claims | `contract.md:16` (C1 calibration), `:67` (C2 depth); no third claim (`:118` "not claims") |
| at least one claim on the lowest non-retired axis (§2:15-17) | PASS — both | `contract.md:10-12` names depth/freshness/calibration tied at 5; `SCORECARD.md:10-15` Axes table reads coverage 6, operability 7, depth 5, freshness 5, calibration 5, adjacency 6 |
| causal separability (§2:20-21) | PASS at plan level | `contract.md:112-116`; `count-c1.py:53-57` imports only round-48's counter, `count-c2.py` is standalone (no cross-import); C1 touches `tools/`+`SKILL.md`, C2 touches `corpus/knowledge/`+SOURCES rows+copies |
| controls built and scored before data (§9:426-432) | PASS for the declared set | freeze commit `0df17b7b` is the first round-49 commit and precedes `w1.ready` (21:36:48) and dispatch (21:48:31); receipts `evidence/control-c1-*.txt` all end `rev=b3e3453d…`; `control-c2-donothing.txt` `failed=entry_absent,pins` |
| controls none may reach `met` | PASS except the declared witness (see F3) | `stub-always-met` `junk_met=18`, `stub-always-unmet` `honest_unmet=8 real=unmet`, `stub-filename-sniffer` `junk_met=18`, `surface-fixes` `junk_met=1`, `r11-only` `junk_met=7`, all exit 1 |
| one mined mistake with class·evidence·captured-by·fix (§2b item 3) | PASS at plan level | `w1-spec.json` item `Mo49ScribeMistakes` requires all four cells and a receipt per fix; `contract.md:130-132` names the two classes |
| ≥1 sourced claim citing a row opened this round (§2b item 4) | PASS | rows S485-S488 in the working-tree `corpus/SOURCES.md:264-267` are `mined`, `opened 2026-10-25`, `used-by corpus/knowledge/journal-reach-r49.md`; S486 `teaches` opens `supersedes S351 —` |
| one theme, 1-3 entries (§10:454-464) | PASS — 1 entry | `contract.md:69-74`; `w1-spec.json` items `Mo49ScribeEntryA`, `Mo49ScribeEntryB` |
| id collision check, 0-3-space pattern (§10:470-493) | PASS on the lists | `assimilation/{reg-ids,staged-ids,collisions}` committed at freeze; `collisions` = S471-S484 (14); S516/S532/S560 absent from `reg-ids` |
| renumber by document | PASS at plan level | `w1-spec.json` item `Mo49ExecCensusMirror` gives `S516→S485, S560→S487, S532→S486, own-work→S488` with a URL check per staged row |
| append only rows the admitted entry cites (§10:452-453) | PASS | the landed block is exactly S485-S488, the four ids the entry's `source:` lines name (`corpus/knowledge/journal-reach-r49.md:3-6`) |
| considerthese, one unimplemented proposal (§10:534-541) | PASS | `considerthese/2026-10-25.md:50-52` lists suggestion 3 under "proposals only, not acted on"; `w1-spec.json` items `Mo49ExecFlaggedFixed` (measurement + counting command) and `Mo49ScribeQuality` (QUALITY criterion citing `considerthese 2026-10-25 #3`) |
| C1 predicate = counter code | PASS on the variant set | `contract.md:24-32` vs `count-c1.py:10-13`, `:206-219`, `:248-280`, `:224-246`, `:298-305`: 18 junk (J1-J8+N1-N10), 7 honest (H1-H7), `real`+`real-opaque`, opaque `sha256`-prefix names, hash-ordered submissions, fixture-only N10/H5, crash/timeout → `error` |
| C2 predicate = counter code | PASS on every P-C2 clause | `contract.md:85-93` vs `count-c2.py:29-34` (floors), `:36-45` (four copies+sha), `:59-90` (normalise/header/rows), `:99-194` (pins, mined/opened/used-by, 6-25 words, unique, normalised location, ≥3 sources, provenance) |
| selftests reproduce | PASS | `count-c1.py --selftest` → `C1_SELFTEST pass=44 fail=0` (rc 0); `count-c2.py --selftest` → `C2_SELFTEST pass=26 fail=0`, matching `evidence/selftest-c1.txt:45`, `evidence/selftest-c2.txt:27`, `contract.md:162` |
| census gate at round start | PASS, receipt thin (see F11) | `evidence/census-start.txt` 21 lines = 20 `W04` + one `ok`, matching `contract.md:120-121`; my re-run `sources-census.sh validate --root … mori` exits 0 with 22 lines (adds `W04 S486`, the new row) |

## Findings — detail

### F1 — HIGH — the wave plan pins `C1_SELFTEST pass=42` while the frozen counter prints 44
`/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-49/build-w1-spec.py:103` (frozen) writes
into item `Mo49ScribeSkillRows`: gate rows "with pins `C1_SELFTEST pass=42 fail=0`, `C2_SELFTEST
pass=26 fail=0` (verify by running them)". The frozen instrument prints 44:
`TMPDIR=.scratch/r49-Mo49RevPromptHonesty python3 .ufo/waves/round-49/count-c1.py --selftest` → tail
`PASS lane_head_unchanged` / `C1_SELFTEST pass=44 fail=0`, rc 0; `evidence/selftest-c1.txt:45` and
`contract.md:162` both say 44. A scribe following the literal pin would land a false registry pin in the
round whose C1 claim is exactly about false pins; the same cell is then re-read by the reconciler
(`count-c1.py` `real` arm), so the false pin can also turn the C1 target `unmet`. Mitigation observed: the
seat was told to verify, did, and pinned 44 (`w1/Mo49ScribeSkillRows.md:35-41`). The plan text is still
wrong and would fail if the instruction were followed as written — a `number-drift` row for `## Mistakes`.

### F2 — MED — wave 1 is below the run-7 attack-share line (9/49 = 18.4%)
Prompt §6 run-7: "m_flash roles carry the majority of **every wave** (…); attack share (≥25%) is met with
reviewer/critic/mutation-tester/labrat seats" (`/home/vgpnk/Projects/shokunin/.ufo/prompts/mori-round-49.md:158-162`).
`w1-spec.json` roles: executor 16, scribe 14, scout 4, connector 4, critic 4, reviewer 3, mutation-tester 2,
sentinel 1, simplifier 1 = 49 seats. Attack seats (reviewer+critic+mutation-tester+labrat) = 9 = 18.4%;
flash-role seats (executor/scribe/labrat/sonic/simplifier) = 31 = 63.3% (majority PASS). If the 25% line is
read per wave, wave 1 fails; if it is read over the round, `contract.md:136-139` states no arithmetic and
no wave-2 mix, so the plan does not show how the round reaches 25% within the 64-100 total. Wave 2 must
carry ≥21 attack seats (for a 32-seat w2) to clear 25% at 81 total.

### F3 — MED — the C1 target is reached at freeze by a pre-existing tool, and §9's rule is disclosed rather than applied
`contract.md:49-57` says controls are "each scored with this counter before data, committed; none may reach
`met`", then lists `controls/tool-r48-merged-witness.py`, whose receipt
`evidence/control-c1-tool-r48-merged-witness.txt:29` is exactly `C1=met junk_met=0 honest_unmet=0 real=met
errors=0 variants=26`, exit 0 (`contract.md:153` repeats it). Prompt §9 (`…round-49.md:426-432`) requires
the cheapest control that skips the claimed work to be built and, if it meets the target, "the counter or
target is wrong — fix it before data". The contract discloses (`:155-161`) but does not fix: the witness
bytes are round-48 seat output, and the round-49 K-class rules (K2-K8, `contract.md:60-65`) are outside the
predicate. Consequence: landing the witness unchanged at `tools/mori-pin-check.py` reaches P-C1 with none
of wave 1's independent v4 work, so P-C1 measures mostly the new counter, not the claimed tool improvement.
It is a disclosed weakness, not concealment — the closure should read C1's improvement as "counter +
selftest arms + false-red audit", not "v4 tool".

### F4 — MED — C2's cheapest-skip control was not built; the claim cells are only counted, not tested
`count-c2.py:136` accepts any claim cell of ≥5 words; the quote/row/pin arms are the real gate. A table of
ten genuine quotes with arbitrary claim text therefore prints `C2=met`. Prompt §9 (`…:426-432`) requires
building that cheapest control and committing the receipt before data; the contract instead names it as a
limit (`contract.md:106-110`). No receipt scores a "real quotes, bogus claims" control. Wave-2 reviewers
re-opening rows around their quotes is the only defence, and it is human/seat review, not the predicate.

### F5 — MED — the contract points at a 0-3-space guard proof that is not in `assimilation/`, and no wave item was briefed to produce it
`contract.md:122-123`: "Collision check, 0-3-space guard proof and the quarantine slice are in
`assimilation/`". At the freeze commit that directory holds only `collisions`, `quarantine-slice`,
`reg-ids`, `staged-ids` (`git show --stat 0df17b7b`; `ls .ufo/waves/round-49/assimilation`). Prompt §10
(`…:486-493`) requires the guard to be proven once with a scratch indented-row registry before the first
append. `w1-spec.json` item `Mo49ExecCensusMirror` briefs only a re-run on the live files; the seat went
beyond the brief and proved it (`w1/Mo49ExecCensusMirror.md:335-347`: column-zero pattern `collisions=0`
=false green, 0-3-space pattern `collisions=1 -> S485`), with receipts under
`.scratch/r49-Mo49ExecCensusMirror/receipts/`. Unless the L1 copies that proof into a committed wave
artifact, the contract's pointer is false and §10's proof is only in uncommitted scratch.

### F6 — MED — the scratch mirror gate was proven with synthetic rows, not the actual append block
Prompt §10 (`…:494-513`) gates the first registry append on a scratch mirror built from the real append
block and the admitted entry. The only mirror receipt is
`.ufo/waves/round-49/assimilation/validate-output.txt` (untracked, 21:55): it ends
`file ok …/assimilation/validate/corpus/SOURCES.md`; the four rows it validated are
`.scratch/r49-Mo49ExecCensusMirror/fixtures/rows-ok.md`, and `diff` of those rows against the landed
`corpus/SOURCES.md:264-267` prints `differ` (e.g. the fixture's S488 source cell starts
`own-work: this host's journal reach, read read-only…`, which does **not** contain the counter's
`own-work: host-journal-reach` key). No receipt validates the real block before the append; the plan names
no step that does. (The post-append census I ran exits 0, 22 lines, but that is after the append and is not
the §10 gate.)

### F7 — MED — S351's flip says "no MESSAGE grep" unqualified; the frozen receipt and the successor row qualify it
`contract.md:80-83` says "this claim is that flip — … no MESSAGE grep". The flip cell itself
(`corpus/SOURCES.md:248`) reads "the public --vacuum-size= sentence plus a committed read-only disk-usage
receipt, and no MESSAGE grep". The frozen receipt contains a MESSAGE regex at lines 95-97:
`$ journalctl -b 0 -u systemd-journald --no-pager -q -g 'Journal .* is .*max'`, and `journalctl(1)` defines
`-g/--grep=` as filtering on the `MESSAGE=` field (`-g` text in the committed `journalctl.1.html`). The
landed successor row narrows the clause to "with no kernel-message grep" (`corpus/SOURCES.md:265`), while
S351's flip text is append-only and stays unqualified. The landed entry itself does not quote the `-g`
lines (its S488 rows are `--disk-usage`, `--system`/`--user`, the drop-in, and `--list-boots`), so the
entry's evidence is clean; the overclaim is the successor row's `teaches` against the flip as written. The
Gate must record which reading it applies (`w1/Mo49ScribeLessonGate.md:173-181,264-266` already flags it).

### F8 — LOW — P-C1's "every run with `--min-tally-pins 26 --baseline-rev 2d85e33d…`" is false for N10/H5
`contract.md:29` states the flags for every run. `count-c1.py:269` passes the fixture jobs with
`--min-tally-pins 1` and the fixture's commit 0 as baseline (`fixture_variant`, `:174-210`). The contract
notes the fixture repository at `:31-32` but not the changed flags: the predicate sentence and the counter
are not the same sentence for two of the 27 runs.

### F9 — LOW — the "staged entry byte-exact" control label has no real staged entry behind it
`contract.md:102` lists "staged entry byte-exact" among the selftest controls. The arm is
`no_table_unmet`, fed a two-line synthetic `# staged` entry (`count-c2.py:289-291`), not a copied staged
file from `/home/vgpnk/Projects/shokuknow/merge/mori/knowledge/…`. No receipt scores an actual staged entry
against the counter; the label overstates what was run.

### F10 — LOW — `contract.md:7-8` cites `.ufo/waves/round-49/disposition.md`, which does not exist
`ls` errors (`No such file or directory`) and `git ls-tree -r --name-only 0df17b7b .ufo/waves/round-49`
matches no disposition path. `w1-spec.json` item `Mo49ScribeDisposition` only drafts its text for the L1.
If the L1 does not land the file, the contract's round-48 spot-check pointer dangles.

### F11 — LOW — the census-start receipt carries no command and no exit code
`evidence/census-start.txt` has 21 output lines and ends `mori ok …/corpus/SOURCES.md`; unlike every
`evidence/control-c1-*.txt`, it has no `exit=` line. `contract.md:121` asserts "exit 0" from outside the
receipt, and prompt §2b (`…:54-56`) asks the report to paste each census output **and its exit code**. My
re-run is exit 0 (22 lines), so the value is true; the receipt is just not self-evidencing.

### F12 — LOW — the round-shape sentence allows a total above 100
`contract.md:138-139`: "Two v1 waves … Total within 64-100". Wave 1 has 49 items (`w1-spec.json`), the v1
band is 32-64, so wave 2 must be ≤51 to keep the total ≤100; the contract states no such bound. A full-band
wave 2 (64) would total 113, outside run-7's ceiling (`…:148-152`).

### F13 — LOW — no plan artifact carries the §4 report sections in order
Prompt §4 (`…:99-130`) requires Work performed → Landed changes → Before → after measurements → Sources &
frontier → Trend verdicts → SHONEN, and §6 item 6 adds a Stale-lane line and tool installs. Neither
`contract.md` nor `w1-spec.json` assigns or sketches them (the spec's scribe items cover SCORECARD, LOG,
SKILL, README, QUALITY, lesson, disposition only). The L1 must build the report from the prompt; a missing
**Sources & frontier** or **Trend verdicts** section is a logged conformance defect under the §4 marker
rule, not a marker failure.

### F14 — LOW — integration markers remain in the Gate and QUALITY drafts
Prompt §2b requires the lesson `## Gate` to record URL, access date and a ≤25-word located quote for every
new row. `w1-spec.json` item `Mo49ScribeLessonGate` deliberately leaves each quote as `[from ScribeRow*]`
and item `Mo49ScribeQuality` leaves `<command from ExecFlaggedFixed>`; the Gate draft still shows the
markers at `w1/Mo49ScribeLessonGate.md:71-74`. If the L1 appends them unfilled, §2b item 1 fails.

### F15 — LOW — both target strings omit the trailing `rev=<R>` token the counters always print
`contract.md:25` and `:99-100` state target lines ending at `variants=26` / `provenance=ok`;
`count-c1.py:304-305` appends ` rev=%s` and `count-c2.py:188-189` does the same. The receipts include the token, so
the intended reading is a prefix match; a closure that greps the whole line literally would fail a
successful run.

### F16 — LOW — the freeze's ordering is provable only from the committer date (jj author-time inheritance)
`git show -s --format='%h %ai %ci'`: `0df17b7b` author 2026-10-25 20:30:53 (= parent `b3e3453d`'s committer
time), committer 21:36:32. The "freeze before any wave seat runs" claim (`contract.md:5-6`) holds by
committer date against `w1.ready` 21:36:48, not by author date. Prompt §6 item 3's rule "report author date
at or after the lane tip it cites" inherits the same jj behaviour; the L1 should check the report against the
committer date.

### F17 — LOW — "rewritten as one entry" (contract) vs "reject as an entry" (spec/Gate draft)
`contract.md:71-74` says the three staged entries are "rewritten as one entry `corpus/knowledge/journal-reach-r49.md`".
`w1-spec.json` item `Mo49ScribeLessonGate` and the Gate draft instead reject **all five** staged entries as
entries (`w1/Mo49ScribeLessonGate.md:111-115`) and admit one newly written entry plus the four rows
(`:135`). Prompt §10 (`…:465-469`) asks the Gate for ≥1 admit and ≥1 reject "from the assimilation set";
as drafted, the admits from the set are the rows S485-S487 while every staged entry is refused. That can
be compliant, but the L1 must pick one reading and say it, or the closure's admit spot-check has no admitted
*entry* to check against the contract's own "rewritten" wording.

## Residual risk and verification gaps

- I did not run either full counter (`--tool … --rev …` / `count-c2.py R`): each takes ~10 minutes and
  changes data-time state; only `--selftest` (44/26, rc 0) and the census were re-run. Every claim about
  the C1/C2 result lines in this report is quoted from committed receipts, not re-derived.
- `contract.md:153`'s "selftest 65/65" for `tool-r48-merged-witness.py` has no committed receipt:
  **UNVERIFIED** (also flagged at `w1/Mo49ScribeScorecard.md:172`). `contract.md:159-161`'s H5 first-draft
  narrative likewise has no receipt: **UNVERIFIED**.
- The wave-1 seat reports and the landed data (`corpus/SOURCES.md:264-267`,
  `corpus/knowledge/journal-reach-r49.md`) were uncommitted at review time; their citations are observed
  working-tree state, not frozen bytes, and the L1 may still change them.
- I reviewed the plan and the frozen instruments, not the taxonomies of every seat report; the Gate's own
  findings (`w1/Mo49ScribeLessonGate.md`) and the S351 scout's (`w1/Mo49ScoutS351.md:77-78`) overlap F5,
  F7 and F14 and should not be counted as independent confirmation of this report.
- Not checked: whether wave 2 is sized ≤51 (not yet built), and whether the eventual report follows §4
  order (not yet written).

## Findings

- **HIGH** — `build-w1-spec.py:103` / item `Mo49ScribeSkillRows` pins `C1_SELFTEST pass=42 fail=0`; the frozen counter prints 44 (`count-c1.py --selftest`, `evidence/selftest-c1.txt:45`, `contract.md:162`).
- **MED** — `w1-spec.json` wave 1 has 9/49 attack seats (18.4%) against prompt §6 run-7's ≥25% line (`…mori-round-49.md:161`); no wave-2/round arithmetic in `contract.md:136-139`.
- **MED** — `contract.md:49-57` says no control may reach `met`, yet `controls/tool-r48-merged-witness.py` reaches the C1 target at freeze (`evidence/control-c1-tool-r48-merged-witness.txt:29`, `contract.md:153`); §9 (`…:426-432`) says a control that meets the target means the target is wrong.
- **MED** — C2's cheapest-skip control (real quotes, arbitrary claims) is not built; `count-c2.py:136` only requires ≥5-word claim cells; `contract.md:106-110` names it a limit instead.
- **MED** — `contract.md:122-123` claims the 0-3-space guard proof is in `assimilation/`; the freeze commit has no such artifact and no wave item is briefed for it (seat proved it at `w1/Mo49ExecCensusMirror.md:335-347`, scratch only).
- **MED** — the §10 scratch-mirror gate validated synthetic rows (`.scratch/r49-Mo49ExecCensusMirror/fixtures/rows-ok.md`, `assimilation/validate-output.txt`), which differ from the appended `corpus/SOURCES.md:264-267`; no pre-append receipt for the real block.
- **MED** — S351's unqualified "no MESSAGE grep" flip (`corpus/SOURCES.md:248`, `contract.md:80-83`) versus the frozen receipt's `journalctl -g` MESSAGE regex (`corpus/evidence/sources-r49/host-journal-reach.txt:95-97`) and the successor's narrowed "no kernel-message grep" (`corpus/SOURCES.md:265`).
- **LOW** — `contract.md:29` "every run with `--min-tally-pins 26 --baseline-rev 2d85e33d…`" vs `count-c1.py:269` (N10/H5 use 1 and the fixture baseline).
- **LOW** — `contract.md:102` "staged entry byte-exact" arm is the synthetic `no_table_unmet` entry (`count-c2.py:289-291`), not a staged file.
- **LOW** — `contract.md:7-8` cites `.ufo/waves/round-49/disposition.md`, absent at freeze and review.
- **LOW** — `evidence/census-start.txt` records 21 output lines but no command or `exit=` line; `contract.md:121` asserts exit 0.
- **LOW** — `contract.md:138-139` allows wave 2 up to 64, which with wave 1's 49 breaks the 100 ceiling; the ≤51 bound is unstated.
- **LOW** — no plan artifact carries prompt §4's report sections in order (or §6's Stale-lane/tool-install lines).
- **LOW** — `[from ScribeRow*]` and `<command from ExecFlaggedFixed>` markers remain in the Gate/QUALITY drafts (`w1/Mo49ScribeLessonGate.md:71-74`); §2b needs a located quote per new row.
- **LOW** — `contract.md:25` and `:99-100` target strings omit the trailing `rev=<R>` token printed by `count-c1.py:304-305` / `count-c2.py:188-189`.
- **LOW** — the freeze's ordering rests on the committer date: `0df17b7b` author 20:30:53 (parent's committer time) vs committer 21:36:32; affects §6's report-author-date rule under jj.
- **LOW** — `contract.md:71-74` says the three staged entries are "rewritten as one entry", while the Gate draft rejects all five staged entries as entries (`w1/Mo49ScribeLessonGate.md:111-115,135`); the L1 must state which reading the Gate applies.

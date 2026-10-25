# ScribeMistakes — round 48 wave w1 (draft `## Mistakes` for corpus/lessons/round-48.md)

- Seat: ScribeMistakes (leaf; no subagents dispatched). Lane: mori-shokunin. Role:
  UFO-FSD scribe — draft the round-48 `## Mistakes` table from earlier-round evidence only.
- Lane root for all `Report:` paths: `/home/vgpnk/Projects/shokunin/mori-shokunin`.
- All evidence below was opened read-only from committed bytes/receipts; no lane tool was
  executed, no production file was edited, no scratch was written, no tool was installed or
  upgraded (tooling-authorization record: none — pure reads; no pacman/uv/npm/binary channel
  used).

## Files opened (evidence pointers verified)

- Contract: `.ufo/waves/round-48/contract.md` (P-C1/P-C2, J1–J8/H1–H4 variants, controls,
  receipt `evidence/control-c1-tool-v2-entering.txt`); `v3-spec.md` (R1–R8 candidate rules).
- Round-47 closure: `corpus/lessons/round-47-verifier-spotcheck.md` (lines 12–23 §1,
  lines 94–100 §5).
- Round-47 frozen-v1 junk receipts: `.ufo/waves/round-47/evidence/v1-junk/skill-v2-oldcopy.txt`,
  `skill-v3-fakeecho.txt`, `skill-v4-weakened.txt`, `skill-v7-entrycopy.txt`,
  `skill-v8-hide+dup.txt` (each ends `PIN_CHECK=met … rc=0`).
- Round-47 w2 reports: `CritV2Junk.md` (FG1–FG5, O1, N1–N4), `ExecV1JunkGreen.md`,
  `MutV2Exact.md`, `MutV2Argv.md`, `MutV2Digest.md`, `MutV2Rebound.md`, `MutC2Recheck.md`,
  `RevLesson.md`, `RevQuality.md`, `RevSkillRows.md`, `ScoutMisroot.md`, `ConnNextRound.md`,
  `ScribeScorecard.md`.
- Round-47 w1 cited by reviewers: `.ufo/waves/round-47/w1/ExecPinTiming.md` (§3,
  lines 85–101).
- Receipts: `.ufo/waves/round-47/evidence/selftest-pin-check.txt` (tail line 24:
  `PIN_CHECK_SELFTEST pass=22 fail=0`), `.ufo/waves/round-48/evidence/control-c1-tool-v2-entering.txt`
  (J1–J8 all `got=met`, `C1=unmet junk_met=8 … rc=1`).
- `corpus/QUALITY.md` criteria 43–46 (lines 114–127), 80 (lines 368–372), 91 (lines 580–597),
  114 (lines 927–937), 123 (lines 1028–1040), 124 (lines 1041–1048).

## Draft — `## Mistakes` for corpus/lessons/round-48.md (fenced, ready for L1 integration)

```markdown
## Mistakes

| id | class | evidence | captured-by | fix |
|---|---|---|---|---|
| M1 | landing | round-47 late seat reports left untracked: `corpus/lessons/round-47-verifier-spotcheck.md:20` (defect: `git status --porcelain` shows 53 untracked paths — `.scratch/r47-*`, `.scratch/r47w2-*`, `.ufo/waves/round-47/w2-results.json`, `w2/CritV2Junk.md`, `w2/MutV2Rebound.md`, `w2/ScoutMisroot.md`) and `:96-97` (routed defect 1). The round report said the three late seats "had not returned"; their results exist on disk but are in no commit | QUALITY 80 (seat output committed/disposed before the round's last lane commit; `git -C <lane> status --porcelain --untracked-files=all -- .ufo/waves/round-<N>/` prints nothing) | Commit or delete the 53 untracked paths at the round-47 tip; append a correction entry in the next round's LOG naming them. Shown able to fail: `git -C /home/vgpnk/Projects/shokunin/mori-shokunin status --porcelain` at the round-47 tip listed the 53 paths (spotcheck §1); after the fix the same command over `.ufo/waves/round-47/` and the scratch dirs prints nothing |
| M2 | survivor / vacuous | frozen v1 scorer green on five junk edits: `.ufo/waves/round-47/evidence/v1-junk/skill-v2-oldcopy.txt:33-34`, `skill-v3-fakeecho.txt:33-34`, `skill-v4-weakened.txt:33-34`, `skill-v7-entrycopy.txt:33-34`, `skill-v8-hide+dup.txt:33-34` all end `PIN_CHECK=met … rc=0` (v2 rebind to an archived `.scratch` copy, inline `python3 -c` echo, weakened `pass=22` without `fail=0`, entry-cell rebind, lowercase token hide + duplicate echo); fresh re-runs recorded in `w2/ExecV1JunkGreen.md:19-27` | QUALITY 123 (criterion added from round-47 lesson M1/M2: a registry pin is calibrated only when an instrument re-runs it from committed bytes and reads it from its own cell) | Harden the scorer (v2: argv allowlist/SAFE_PATH, exact equality, all prefix-led lines agree, `dropped`/`rebound`/`duplicate`, case-insensitive unparsed, fence-aware parsing) so junk controls go red while honest + real stay green. Shown able to fail: `python3 <frozen v1 @63eecf27, e3ef425a…> --repo <lane> --rev 63eecf2738db96f46b0bd02b1b2dfd66787493d0 --min-tally-pins 26 --baseline-rev 2d85e33d… --skill <variant>` → `PIN_CHECK=met` rc 0 for all five variants (ExecV1JunkGreen.md); after v2 the same variants → `PIN_CHECK=unmet` rc 1 (`evidence/v2/` receipts; fresh 9/9 byte-identical re-runs in `w2/ExecV2Junk.md`) |
| M3 | survivor | v2's five new false-green classes (structural): `w2/CritV2Junk.md` FG1 (header cell `selftest` spell — corrupt pins pass; lines 25-43), FG2 (fullwidth underscore prefix, lines 50-68), FG3 (Cyrillic Е prefix, lines 74-81), FG4 (new row pinning a stale tally bound to an archived tool copy, lines 87-102), FG5 (fenced replacement elides pins, lines 108-121); plus O1 blank-line row drop (lines 142-146). These become the frozen J1–J8 junk edits of round 48 (`contract.md` P-C1; entering receipt `evidence/control-c1-tool-v2-entering.txt` shows `junk_met=8`, `C1=unmet`) | none (no criterion yet captures these structural evasions; QUALITY 114's fixture/arm mechanism is the pattern v3 R8 implements) | v3 rules R1–R6 + arms (`v3-spec.md`): header spelling recognized case-insensitively (R1); hidden/fenced/blank-separated/terminated gate-table rows counted fatal (R2); ASCII-strict tally-pin and `unparsed` on non-ASCII/NFKC-casefolded spans (R3); rebound by baseline `(prefix, argv)` set (R4); `(\d+) lines` pins bound to a file in the measured tree (R5); truncated-digest `…` pins must prefix a sha256 of an in-tree path (R6). Shown able to fail (each red-before run is recorded in CritV2Junk.md): v2 on `…/variants/v1-header-selftest-corrupt-pins.md` → `PIN_CHECK=met` rc 0; same for the fullwidth/Cyrillic rows, the archived gate-v2-extract row and the fenced replacement (all `PIN_CHECK=met` rc 0); target after v3: each J1–J8 → `PIN_CHECK=unmet` rc 1 |
| M4 | survivor | `count-c2.py` selftest has no used-by arm: deleting the used-by conjunct is invisible (`w2/MutC2Recheck.md:29-36` — mutant passes `C2_SELFTEST pass=13 fail=0` rc 0; `:61-67` — full false green through the CLI on a fixture whose S475 used-by names a different entry: `C2=met … source_row=ok` rc 0 vs pristine `C2=unmet … failed=source_row` rc 1). Wave-1 finding reproduced | QUALITY 114 (named survivor must enter a fixture/arm the next checker version kills) | Add the `used_by_not_entry` arm verbatim after `source_row_queued` (grows the detector 13→14). Shown able to fail: `TMPDIR=$S python3 $S/mutant_m5.py --selftest` → `C2_SELFTEST pass=13 fail=0` rc 0 (survivor); with the arm, the same mutant → `FAIL used_by_not_entry … C2=met … source_row=ok` rc 1 (`mutant_killer.py` run recorded in MutC2Recheck.md:59) |
| M5 | survivor | case-insensitive unparsed detection has no arm: reverting `(?i)` to case-sensitive survives the whole 34-arm suite (`w2/MutV2Exact.md:60-74`); false-green reproducer on a mixed-case-only `Foo_Selftest` short row (`:75-90` — mutated bytes `PIN_CHECK=met` rc 0, pristine `PIN_CHECK=unmet … unparsed=1` rc 1) | QUALITY 114 | Add a selftest arm with a mixed-case-only spelling (`Foo_Selftest`) inside a short/unparsed row, expecting `unparsed`. Shown able to fail: `TMPDIR=<scratch> python3 mut-c-casesens.py --root probe-c/tree --repo <scratch>` → `PIN_CHECK=met` rc 0 (false green, recorded); pristine bytes on the same fixture → `PIN_CHECK=unmet` rc 1 |
| M6 | survivor | the three `argv_ok` sub-checks (SAFE_PATH, `/.scratch/` clause, strict tail) are individually untested: each single-point deletion survives `--selftest` 34/34 rc 0 while a direct probe shows each changes behavior (`w2/MutV2Argv.md:26-92` — mutants A/B/C all survive; differential probe table lines 65-74) | QUALITY 114 | Add arms isolating each predicate: a bound command with a non-registered path (`corpus/x.py`), a `tools/.scratch/…` path, and a bound command carrying extra args — each expecting `no_command`. Fix not yet shown able to fail (no arm has been applied or run; the survivor state is recorded, the post-fix run is not) |
| M7 | survivor | digest containment (realpath-inside-root) has no symlink arm: removing the realpath check ships green, and a digest pin is "satisfied" through an in-tree symlink to an out-of-tree file (`w2/MutV2Digest.md:30-35,44-75` — mutant-b reproducer `PIN_CHECK=met … mismatches=0` rc 0 vs pristine `PIN_CHECK=unmet … mismatches=1` rc 1) | QUALITY 114 | Add a selftest case pinning a digest of an in-tree symlink to an out-of-tree file (expect `state=mismatch`); keep (a) as defense-in-depth. Shown able to fail: `TMPDIR=<scratch>/tmp python3 mutant-b.py --root repro-b/tree --skill SKILL-b.md --repo <scratch>/repro-b` → `PIN_CHECK=met` rc 0 (false green, recorded); pristine on the same fixture → `PIN_CHECK=unmet` rc 1 |
| M8 | survivor | rebound machinery coverage gaps: no None-baseline-bind selftest case, and removing the None-guard crashes the real claim (`TypeError: can only join an iterable`); no rev-worded-current-command-vs-baseline case, and the `check()` normalization is unexercised by both selftest and claim (`w2/MutV2Rebound.md:52-101` — mut-c2 real claim rc 1 crash vs pristine rc 0 met; mut-b2 fixture rebound=1 unmet vs pristine met) | QUALITY 114 | Add the two missing selftest cases (None baseline bind; baked-hash current command vs baseline bind). Shown able to fail: `TMPDIR=… python3 mut-c2.py --rev 68d66ca… --baseline-rev 2d85e33… --min-tally-pins 26` → rc 1 TypeError crash (`claim-mut-c2.log`); pristine → rc 0 met. b2: fixture run of `mut-b2.py` → rc 1 `rebound=1` vs pristine rc 0 met |
| M9 | reference-drift | round-47 lesson's routed ExecPinTiming summary misstated its citation: the lesson said the two failing arms "vary across runs"; `w1/ExecPinTiming.md:85-101` (§3) says the failing-arm names, verdict line `C3_SELFTEST pass=17 fail=2` and rc are identical across rounds — only the throwaway fixture-repo hash in the FAIL detail lines varies. Caught by `w2/RevLesson.md:21-35` (F1); the final round-47 lesson carries the correction in-line | none | Reword the summary to name the varying debug detail (throwaway fixture hash), not the failing-arm identity. Fix not yet shown able to fail (review-caught prose correction; no mechanical gate) |
| M10 | reference-drift | committed self-test receipt `evidence/selftest-pin-check.txt:24` records the frozen v1-era run (`PIN_CHECK_SELFTEST pass=22 fail=0`) with no "v1" label, while the standing v2 tool and `SKILL.md:938` pin/observe `pass=34` (`w2/RevQuality.md:27` O2) | none | Relabel/supersede the receipt (add "(frozen v1, 22 arms)" or a dated note) so a reader does not read 22 against the pinned 34. Fix not yet shown able to fail (labeling; the red state is the observable tally disagreement 22 vs 34) |
| M11 | provider | v2's declared setup-exit contract is broken: `--repo` failures die with a traceback and rc 1 instead of the documented single-line exit-2 `PIN_CHECK_SETUP`; the registry row's verdict-map cell restates the overpromise (`w2/RevSkillRows.md:134-152` D1; reproduced as `w2/ConnNextRound.md` D4/L5) | none | Wrap the scratch setup (`os.makedirs`/`mkdtemp`, before `try:`) in the setup handler and print `PIN_CHECK_SETUP`, exit 2. Shown able to fail: `TMPDIR=<scratch> python3 pin_check_T.py --rev 68d66ca… --repo /nonexistent-r47w2-revskillrows` → `PermissionError` traceback rc 1 (recorded); after the fix → rc 2, one `PIN_CHECK_SETUP` line |
| M12 | scope | mori's misroot sweep is blind to a lane's own misroot when the stray report omits the lane id: the AND predicate (lane token ∧ round token) returns `MORI_MISROOT_CLEAN` for a genuine kasegi r30 misroot under `--lane kasegi --round 30` (`w2/ScoutMisroot.md:115-150` §2.2, reproducer at `:131-134`; verdict table `:241-250`) | none | Complement the token sweep with the content-hash check (or OR-lane detection) so a report omitting its lane id is still found by its owner's sweep. Shown able to fail: `python3 tools/mori-misroot-sweep.py --fleet-root /home/vgpnk/Projects/shokunin --lane kasegi --round 30` → `MORI_MISROOT_CLEAN` rc 0 (miss, recorded); after the fix → `MORI_MISROOT_CANDIDATE` |
```

## Notes on evidence

- The entering round-48 control receipt `evidence/control-c1-tool-v2-entering.txt` confirms the
  before-state: the v2 tool at `e5dbac05` prints `got=met` on all eight J1–J8 variants →
  `C1=unmet junk_met=8 honest_unmet=0 real=met errors=0 variants=12 rc=1` (this is the state
  M3's target fixes).
- M2's five false-green files correspond to round-48 J-classes only partially: J1–J8 are the
  *new* classes mined by CritV2Junk (M3), while M2's five are the earlier v1 false greens
  (v2/v3/v4/v7/v8). Both rows are kept separate as assigned.
- Every `fix` names its red-before command verbatim from the cited report/receipt, or states
  `fix not yet shown able to fail` where no post-fix run exists. No command in this report was
  re-run by this seat; all quoted outputs are read from committed reports/receipts (UNVERIFIED
  as fresh executions, but each is a committed artifact at the cited path).
- Class labels use the assigned vocabulary: landing, survivor/vacuous, survivor, reference-drift,
  provider, scope. `number-drift`/`attribution` classes were considered for M9/M10 but the
  evidence points to citation/placement misstatement (reference-drift), not a counted number.

## Out-of-scope / limits

- No edits to `SKILL.md`, `SOURCES.md`, `corpus/`, `tools/`, `LOG.md`, `SCORECARD.md`, or any
  frozen round-48 file; the draft above is for the L1 integrator.
- No tools installed or updated; no scratch written; leaf seat, no subagents, no questions asked.
- UNVERIFIED: live re-execution of any quoted command (none run here); the exact disposition of
  the 53 untracked paths after the round-47 closure (that is the fix's own acceptance).

Report: .ufo/waves/round-48/w1/ScribeMistakes.md

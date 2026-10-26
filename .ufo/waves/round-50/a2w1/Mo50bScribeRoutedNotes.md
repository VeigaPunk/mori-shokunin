# Mo50bScribeRoutedNotes — round 50, wave a2w1 (lesson notes: round-49 routed defects 7 and 8)

Seat: scribe. Lane `mori-shokunin`, repo `/home/vgpnk/Projects/shokunin/mori-shokunin`.
Read at the attempt-2 data commit `487941b9395e89678af0053cc443cdb49cdee6e3`; freeze
`950e99be6757a52b00e9eb70ae1a1a7bbe2ea379`; entering tip `7197160b927f04db294c9553fb48fadcc7a3f4e3`;
salvage `9b8562a371dc916fdc0fc686619ea1e271a3e118`. Contract read first: `.ufo/waves/round-50/contract.md`.

Assignment: draft (fenced) the round-50 lesson notes for round-49 routed defects 7 and 8
(`corpus/lessons/round-49-verifier-spotcheck.md` §5, lines 116-117), and state whether the wave's seat
naming meets the handle rule.

Nothing in the lane was edited. The drafts below are for the L1 to integrate. No host kernel log, no cgroup
limit, no systemd/journald state was read or changed. `/home/vgpnk/Projects/shokuknow/merge/mori` was read
only (one staged entry header). Scratch `/fast/scratch/hyaku/mori-r50/Mo50bScribeRoutedNotes/` created,
used for `TMPDIR` only, and removed before this report was filed.

## Behaviour (what I checked, and how)

1. Read the frozen contract, then the two routed items at `corpus/lessons/round-49-verifier-spotcheck.md:116-117`
   and the lane disclosures they come from (`:53`), then the round-49 lesson's Gate/Admit block and its
   `## Wave 1 — integrated findings`, `corpus/QUALITY.md` 129-131, `corpus/lessons/round-48.md:140-190`.
2. Re-derived defect 7's subject matter from the instruments rather than from the prose: the round-50 C1
   counter's input surface and regexes, the round-49 counter's `opaque()`, and the seat-naming code of all
   three builders (`build-a2w1-spec.py`, round-50 `build-w1-spec.py`, round-49 `build-w1-spec.py`).
3. Swept the two files named for defect 8 for `understat*` (case-insensitive) and read each hit's full
   sentence; read the model wording the landed entry already uses.
4. Checked that `tools/` did not move between the salvage and the data commit (so the R11 instrument is
   byte-identical in this round).

## Evidence (command, output, exit code)

| # | command (cwd `.../mori-shokunin`) | output | rc |
|---|---|---|---|
| E1 | `grep -nic "understat" corpus/lessons/round-49.md corpus/knowledge/journal-reach-r49.md` | `corpus/lessons/round-49.md:1` / `corpus/knowledge/journal-reach-r49.md:0` | 0 |
| E2 | `grep -n "K4" corpus/lessons/round-48.md corpus/lessons/round-49.md` | (no output) — the label exists only in the spot-check and the contract | 1 |
| E3 | `grep -c "opaque\|variant" .ufo/waves/round-50/count-c1.py` | `0` — round 50's C1 runs no variant harness | 1 |
| E4 | `python3 -c` over `.ufo/waves/round-50/a2w1-spec.json` | `seats=64 unique=64`; e.g. `Mo50bExecC1Rerun Mo50bCritC1Counter Mo50bRevEntryHeader` | 0 |
| E5 | `git diff --stat 9b8562a3 487941b9 -- tools/` | (no output: `tools/` unchanged salvage → data) | 0 |
| E6 | `grep -n 'read("\|git(fleet' .ufo/waves/round-50/count-c1.py` | `:195` receipt, `:211` `SCORECARD.md`, `:212` `SHONEN.md`, `:275` `MANIFEST.json` via git | 0 |
| E7 | `grep -n "selftest" SHONEN.md`; `cat .ufo/waves/round-50/evidence/selftests/*.txt` | `SHONEN.md:7` carries both pins `(114/114)`, `(17/17)`; receipts hold `PIN_CHECK…` / `UNLANDED…` selftest lines | 0 |
| E8 | `/home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status` | `/fast/scratch/hyaku` 24 % used, 611.7 G free | 0 |

Line numbers relied on below: `count-c1.py` `MIN_BOXES`/`MIN_PINS` `:44-45`, `RECEIPT_DIR` `:46`,
`PIN` `:49-52`, `HIDDEN` `:52`, `BOX` `:53`, `check_axes` `:111`, `parse_shonen` `:149-160`,
`bound_path` `:162-173`, `check_pins` `:175-206`, `evaluate` `:208-241`; the docstring's own limit
("the hidden scan covers SHONEN.md only") at `:27`. Round 49: `opaque()` `:216-222`, its uses `:257,266,269,274,439,444`.
Builders: `build-a2w1-spec.py:27` `P = "Mo50b"`, `:49-51` `add()`; round-50 `build-w1-spec.py:21,42-43`;
round-49 `build-w1-spec.py:20,41-42`.

## Draft — round-50 lesson note for routed defects 7 and 8 (fenced; for `corpus/lessons/round-50.md`)

````markdown
### Round-49 routed defects 7 and 8 (round 50 disposition)

7. **K4, the R11 carve-out and the handle rule — partly carried, and the carried part is the narrow one.**
   C1 this round binds the `SHONEN.md` tally pins only: a floor of two pins and four boxes (`count-c1.py:44-45`),
   pins that are a backticked `python3 <repo-relative .py> --selftest` followed by `(N/M)` or
   `-> PREFIX pass=N fail=K` (`PIN`, `:49-52`; `bound_path` requires exactly those three argv, `:162-173`), a
   committed receipt per command stem (`RECEIPT_DIR`, `:46`; `:195`), and a hidden-token scan that reads
   `SHONEN.md` alone (`HIDDEN`, `:52`; the limit is stated at `:27`). The counter reads `SCORECARD.md`,
   `SHONEN.md` and `evidence/selftests/*.txt` plus `MANIFEST.json` through git (`:211,212,275`); it never opens
   `SKILL.md`. So **K4** ("pins outside the self-test cell": full digest, `(N lines)`, non-`pass=` tally
   spelling — round-48 `w2/R48CritV3Junk2.md:32`, no wave-1 carrier in round 49,
   `w1/Mo49ScribeDisposition.md:354-356`) is closed **for the two stale SHONEN pins and nothing else**. The
   residue is still outside every frozen instrument: tally tokens in `QUALITY.md:885,900,903,909,934,936,1033-1034`,
   `README.md:607-608`, `LOG.md:2224-2295`, and whatever `SKILL.md`'s registry cells pin. This round carries the
   inventory as a seat (`Mo50bExecSelftestReceipts`), not as a predicate, and the contract says so in P-C1(b)'s
   scope. **R11** is untouched: `tools/` is byte-identical between the salvage `9b8562a3` and the data commit
   `487941b9` (`git diff --stat … -- tools/` prints nothing), and C1 reads no row, so QUALITY 131's carve-out —
   a `fixtures/`/`mutants/` path carrying the claimed instrument's basename (`QUALITY.md:1136-1137`, from
   `w2/R48ExecD7.md` §8) — stays exactly where round 49 left it: a stated limit, not a closed class.
   **The handle rule has no carrier this round.** Round 49's handle was `sha256(rev, body)[:12]`
   (`.ufo/waves/round-49/count-c1.py:216-222`) — a function of the variant, recomputable from content, and
   QUALITY 129's own Not-covered says as much ("the harness does not randomise the edits, and the names stay
   opaque only while the variant bytes are unknown to the tool", `QUALITY.md:1101-1104`). Round 50's C1 and C2
   run no variant harness at all (`grep -c 'opaque\|variant' .ufo/waves/round-50/count-c1.py` → `0`), so nothing
   in this round closes or exercises the rule. The rule to carry, stated so a successor can act on it: **a handle
   handed to an instrument under test — the copy, the scratch directory, the fixture repository — is drawn from a
   per-run random nonce, never from the bytes, the revision, or any name the instrument was told.** A handle a
   reader uses to address a seat is a different kind of handle, and this wave's do not meet the rule as routed:
   the builder names every seat deterministically as `P + role + claim` (`build-a2w1-spec.py:27,49-51`, `P =
   "Mo50b"`; same convention in round-50 `build-w1-spec.py:21,42-43` and round-49 `build-w1-spec.py:20,41-42`),
   so `Mo50bCritC1Counter` announces that it attacks C1. The measured cost is nil this round: neither counter
   reads a seat name or a report path (`grep -rn 'Mo50' .ufo/waves/round-50/*.py` → the builder's own literals
   only), and reports are read by the L1, not by an instrument. The cost that would appear is a sweep over
   `a2w1/*.md`, which would learn each report's claim and expected verdict from its filename. **Resolution carried
   forward:** scope the rule to blinding handles; leave seat ids descriptive, because roster addressing, report
   filenames and `agent://` routing depend on them, and a random seat id only moves the name→role map one level
   up. Recorded as a named limit of this wave: the 64 seat ids (`a2w1-spec.json`) are recomputable from the claim
   set.

8. **D-g discernment wording — one live occurrence, corrected here.**
   `corpus/lessons/round-49.md:96-99` is the only place in the two named files that uses "understates" for a
   staged number (`grep -nic understat` → `round-49.md:1`, `journal-reach-r49.md:0`). The staged capture is dated
   2026-10-24 (its own `source:`/`verified-at:` lines and S554's `read 2026-10-24`) and the receipt is
   2026-10-25T20:43:09-03:00, after a `--vacuum-size=50M` line at 13:10:39 that the round-49 wave found
   consistent with the 269M → 56M movement (actor unverified, not a frozen source). The two counts are therefore
   different moments. Drop-in replacement for lines 96-99:

   ```
     - "two journals … reaches of six boots and none" (r47, r48) is a **different capture** from this round's
       receipt, not a contradiction: it was taken 2026-10-24 and the receipt on 2026-10-25, after a
       `--vacuum-size=50M` line the round-49 wave found consistent with the 269M → 56M movement (actor
       unverified). Read against the receipt it understates what *this* host shows — the `--disk-usage` total of
       56M decomposes into `--system` 19M and `--user` 37M, the volatile store is empty, and `--list-boots`
       lists **two** boots, not six — so whatever the entry says about stores must name the stores the receipt
       actually reads. The reject rests on provenance: S554 is a `file://` note outside this lane.
   ```

   `corpus/knowledge/journal-reach-r49.md` needs no correction; its host section already uses the right idiom
   ("The 269M, 56M and 45M figures belong to three moments", `:55`), and no claim row rests on a staged number.
   One reader-facing consequence for the correction entry: the closure quotes the pre-correction sentence
   (`corpus/lessons/round-49-verifier-spotcheck.md:94`), so the round-50 correction should say that the §3
   "nuance" cell quotes the old wording, and that this bullet supersedes it.
````

## Notes for the L1 (not part of the lesson draft)

- The lesson draft's defect-7 paragraph deliberately separates three things the spot-check's one line merged:
  K4's SHONEN slice (closed by C1), K4's remaining residue (open, inventoried by a seat), R11's carve-out
  (untouched, `tools/` unmoved), and the handle rule (no carrier this round; seat ids recomputable).
- Defect 8's correction is a **lesson** edit only. I did not edit `corpus/lessons/round-49.md`; the L1 applies
  the fenced replacement, and `LOG.md`'s correction entry should carry the same "different capture" wording so
  the two files agree.
- The claim that K4's residue sits "outside every frozen instrument" rests on the read targets at E6 (no
  `read("SKILL.md")` in `count-c1.py`) and on the tally-token grep over tracked `.md`; I did not run
  `tools/mori-pin-check.py`, so "unbound" means "not bound by round 50's C1", not "unbound by every tool in
  `tools/`".

## Findings

| # | severity | finding | file / line |
|---|---|---|---|
| F1 | MED | Routed defect 7 is carried only as far as the two `SHONEN.md` pins. `count-c1.py` binds pins in `SHONEN.md` alone (its own limit at `:27`) and never opens `SKILL.md`, so K4's class — pins outside the self-test cell — remains unbound for `QUALITY.md`, `README.md`, `LOG.md`, `PROVINCE.md`, `MANPAGE.md` and the SKILL registry cells. The round-50 lesson must not read as if K4 were closed. | `.ufo/waves/round-50/count-c1.py:27,44-52,149-160,211-212`; `corpus/QUALITY.md:1033-1034` |
| F2 | MED | A seat handle is recomputable from the content it attacks: `n = P + name` with role- and claim-bearing names, 64 deterministic ids in `a2w1-spec.json`. The rule as routed in §5.7 is therefore not met by this wave. No instrument reads a seat name this round, so the leak reaches no score; the resolution is to scope the rule to blinding handles and state the seat-id determinism as a named limit. | `.ufo/waves/round-50/build-a2w1-spec.py:27,49-51` |
| F3 | MED | Routed defect 8 is still open at the data commit: `corpus/lessons/round-49.md:96` says the staged `six boots` capture "understates what the receipt shows" without saying it is a different capture first. One occurrence; `corpus/knowledge/journal-reach-r49.md` is clean (0). The closure quotes the old wording, so the correction entry must say so. | `corpus/lessons/round-49.md:96-99`; `corpus/lessons/round-49-verifier-spotcheck.md:94,117` |
| F4 | LOW | Frozen-counter limit to name: `bound_path` accepts exactly `python3 <repo-relative *.py> --selftest`, so a legitimate pin of a `.sh` tool, of an absolute path, or of a `--selftest` invoked with any extra argument scores `unbound`, which the counter counts as a mismatch. A future SHONEN edit that pins such a command turns C1 red with no defect behind it. | `.ufo/waves/round-50/count-c1.py:162-173,183-186` |
| F5 | LOW | Frozen-counter limit to name: `HIDDEN` matches the bare token `SELFTEST` anywhere in `SHONEN.md` outside a pin, so any prose that names an instrument's selftest token in the checklist makes `C1=unmet hidden≥1`. Future SHONEN boxes must describe instruments without their `*_SELFTEST` token. | `.ufo/waves/round-50/count-c1.py:52` |
| F6 | LOW | Positive check: `tools/` is byte-identical salvage → data (`git diff --stat` empty), so R11's instrument and the pin checker did not move in round 50; QUALITY 131's carve-out limit is unchanged, not silently repaired. | `git diff --stat 9b8562a3 487941b9 -- tools/` |

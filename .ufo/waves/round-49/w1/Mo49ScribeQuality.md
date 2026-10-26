# Mo49ScribeQuality — QUALITY.md criteria 129 onward (round 49, w1)

Seat: wave w1, lane mori-shokunin (`/home/vgpnk/Projects/shokunin/mori-shokunin`). Bounds observed:
leaf seat, no subagents; the frozen files under `.ufo/waves/round-49/` were read, never written; no lane
file other than this report was created or modified; no git write, no jj operation, no pacman, no host
write. No lane tool was run, so no `TMPDIR` scratch was created (`/home/vgpnk/Projects/shokunin/
mori-shokunin/.scratch/r49-Mo49ScribeQuality/` does not exist and was not needed).

## Behavior

Drafted (not integrated) `corpus/QUALITY.md` criteria **129-133** in the file's own style: bold
sentence, then `Lesson:`, `Rationale:`, `Check:`, `Shown able to fail:`, `Not covered:`, numbered
continuation lines, lane-root-relative paths. The draft is in one fenced block below; the L1 integrates.

Five candidates, one criterion each:

| # | candidate | lesson pointer used |
|---|---|---|
| 129 | a scoring harness hands the tool under test only opaque names | `round-49.md` M1 |
| 130 | a registry checker reads what a reader sees (indented / tabbed / commented / HTML rows) | `round-49.md` M4, `R48CritV3Junk1` §1-§8 |
| 131 | a row's pin is bound to its claimed instrument; two authorities agree on the exit contract | `round-49.md` M4, `round-48.md` M3 ("Not closed: D7"), `R48ExecD7` §2, §6 |
| 132 | a retention-bound entry names the journal and dates the host number | `round-49.md` Gate (C2 named limits) |
| 133 | the round counts flagged-versus-fixed critic defects | `round-49.md` Gate (considerthese item) |

**Numbering note for the L1.** Round 49's `## Mistakes` rows are fixed by the wave-1 dispatch
(`.ufo/waves/round-49/build-w1-spec.py:93`, seat `Mo49ScribeMistakes`) at **M1** (counter keyed on the
harness's filename/TMPDIR) and **M4** (the seven v3 survivors), with M2 (`.scratch` residue) and M3
(author date before cited tip) unrelated to these criteria. Candidates (d) and (e) have no M row in that
dispatch, so 132 and 133 cite `## Gate` — the same form QUALITY 127 already uses for a considerthese
item. If `Mo49ScribeLessonGate`/`Mo49ScribeMistakes` land either as an M row, renumber the `Lesson:`
line only; nothing else in the criterion depends on it.

## Commands and observed evidence

All commands run from `/home/vgpnk/Projects/shokunin/mori-shokunin` unless stated. Nothing was installed.

1. **Frozen bytes unchanged.** `sha256sum -c .ufo/waves/round-49/evidence/freeze-sha256.txt` → 31 lines,
   all `OK`, no failure line (exit 0). So the contract, both counters, every control, every receipt and the
   four committed source copies in the working tree are the bytes frozen at `0df17b7b`.

2. **House style read.** `corpus/QUALITY.md` is 1087 lines, last criterion is 128 (criterion 125-128 read
   whole; section heading form `## Criteria added round 48 — …`).

3. **Opaque handles (129).** `grep -n 'sha256\|opaque\|scratch\|env\[' .ufo/waves/round-49/count-c1.py`
   → the staging code is `.ufo/waves/round-49/count-c1.py:216-274`: `opaque()` is a sha256 prefix,
   `stage()` writes `s-%s.md % opaque(rev, body)` and passes `TMPDIR=t-<same tag>`; `plan()` sorts jobs by
   `os.path.basename(j[5])` (the hash-named scratch dir); `run_tool()` (`:224-247`) builds the env as
   `dict(os.environ, TMPDIR=scratch, PYTHONDONTWRITEBYTECODE="1")` and passes `--skill <s-<hash>.md>`; no
   other channel carries `J`/`H`/`N`. Fixture variants: `fixture_variant()` (`:174`) creates
   `w-<opaque(fixture, str(move_pin), dest)>`.

4. **The sniffer pair (129, shown able to fail).**
   `evidence/control-c1-sniffer-under-r48-counter.txt` → 12 variant lines J1-J8 `got=unmet`, H1-H4 and
   `real` `got=met`, then
   `C1=met junk_met=0 honest_unmet=0 real=met errors=0 variants=12 rev=b3e3453d…`, `exit=0`.
   `evidence/control-c1-stub-filename-sniffer.txt` → 26 variant lines, N1-N10 all `expect=unmet got=met
   rc=0`, then `C1=unmet junk_met=18 honest_unmet=0 real=met errors=0 variants=26 rev=b3e3453d…`, `exit=1`.
   Same tool bytes, opposite verdicts: the leak closed.

5. **The row shapes (130).** `.ufo/waves/round-48/w2/R48CritV3Junk1.md` §1 (HTML comment after a blank
   line), §3 (tab-indented row inside a fence), §4 (four-space row outside a table), §8 (HTML table
   markup) are the four survivors whose repair is `^\s*\|` plus `<t[rd]`; measured at the landed tip with
   `PIN_CHECK=met … hidden=0`. The merged witness carries that repair at
   `.ufo/waves/round-49/controls/tool-r48-merged-witness.py:264-266`
   (`row_shaped = ^\s*\|`, `html_row = ^\s*<t[rd][\s>]`). Honest controls H6/H7 (no pin token) stay `met`
   in every receipt.

6. **The binding rule (131).** `w2/R48ExecD7.md` §2: v3 scores the D7 registry `PIN_CHECK=met`; R11 turns it
   `unmet … misattributed=1`. `.ufo/waves/round-49/controls/tool-r48-merged-witness.py:523-549` (duplicate
   exit contracts) and `:628-634` (`state=misattributed claimed=… bound=…`). The per-half receipts:
   `evidence/control-c1-tool-r48-surface-fixes.txt` → `N9 expect=unmet got=met rc=0`, `junk_met=1`;
   `evidence/control-c1-tool-r48-r11-only.txt` → N1-N7 `got=met`, `junk_met=7`;
   `evidence/control-c1-tool-v3-entering.txt` → N1-N9 `got=met`, `junk_met=9`. The merged witness
   (feasibility only, not the claim's tool) →
   `evidence/control-c1-tool-r48-merged-witness.txt`: `C1=met junk_met=0 … variants=26`, exit 0.

7. **The reach numbers (132).** `corpus/evidence/sources-r49/host-journal-reach.txt:2`
   `# captured 2026-10-25T20:43:09-03:00 …`; `:5` `Archived and active journals take up 56M …`; the
   `systemd-analyze cat-config` block shows the drop-in `SystemMaxUse=256M` / `RuntimeMaxUse=64M`; the
   journald start-up lines read `Runtime Journal … is 8M, max 64M` and `System Journal … is 45M, max
   256M`. `grep -oE '[0-9]+(\.[0-9])?M'` over the receipt → `19M 210.9M 256M 37M 45M 56M 64M 8M`
   (8 distinct). The same grep over the staged entries and the older in-lane entry →
   `12.3M 243.6M 250.3M 256M 258.3M 269M 56M 64M 8M`; `258.3M`, `250.3M`, `243.6M`, `269M`, `12.3M` are
   **not** in the 2026-10-25 receipt. `corpus/knowledge/journal-disk-usage-total-r51.md:10` dates its
   269M to 2026-10-24; staged `journal-reach-at-ceiling-r46.md` states one size bound for "the journal"
   while the receipt prints two journals with two ceilings.

8. **Flagged versus fixed (133).** `git diff --numstat 18fd68b0 baabc992 -- SKILL.md` → no output
   (SKILL.md byte-identical at the round-45 landing). `git show baabc992:SKILL.md` line 190 still reads
   ``C1_SELFTEST pass=10 fail=0` rc 0 at sha256 `f80e75ac7421…``; lines 184 and 194 still read
   ``GATE_REGISTRY_SELFTEST pass=6 fail=0``. `corpus/lessons/round-45-verifier-spotcheck.md:50-57`
   ("Calibration ruling") independently re-measures `:190` and `:191` stale at `baabc992`. The flag was
   `.ufo/waves/round-45/w1/CritAxisHarm.md` §1b (four cells `:184`, `:190`, `:191`, `:194`).

9. **Receipt digests.** `evidence/control-c1-stub-always-met.txt` and
   `evidence/control-c1-stub-filename-sniffer.txt` carry the **same** sha256 in `freeze-sha256.txt`
   (`673966107b7c…`); both are all-`met` runs, so the counter output is byte-identical and the two controls
   cannot be told apart by digest. Reported as a finding below, not used as evidence for anything.

## Draft — `corpus/QUALITY.md`, criteria 129-133

```markdown
## Criteria added round 49 — an opaque harness, rows a reader can see, bound pins, a dated reach, a flag that must land

129. **A scoring harness hands the tool under test only opaque names, and a tool that keys on the harness's own
    artifacts cannot pass.** Lesson: `corpus/lessons/round-49.md` M1. Rationale: round 48's counter passed a tool
    that never parsed the registry — it read `--skill`'s basename (`variant-J1.md`) and the per-variant `TMPDIR`
    (`c1-J1-…`) and returned red on J, green on H (`w1/CritC1Counter.md` F1). The successor names each copy and
    scratch directory by a sha256 prefix of its bytes (`s-<12 hex>.md`, `t-<12 hex>`), orders the runs by that
    hash, and builds its two fixture edits in a repository whose path and commit message carry no variant name.
    Check: the harness is read as well as run. `grep -n 'def opaque' .ufo/waves/round-49/count-c1.py` shows the
    sha256 handle, and `grep -n 's-%s.md\|"t-" + ' .ufo/waves/round-49/count-c1.py` shows the only two names
    handed to the tool; then `python3 .ufo/waves/round-49/count-c1.py` run with
    `--tool .ufo/waves/round-49/controls/stub-filename-sniffer.py` and `--rev <rev>` prints `junk_met=18` — the
    name-keyed stub cannot pass. Shown able to fail: the same sniffer
    prints `C1=met … variants=12` under the round-48 counter (`evidence/control-c1-sniffer-under-r48-counter.txt`)
    and `C1=unmet junk_met=18 … variants=26` here (`evidence/control-c1-stub-filename-sniffer.txt`). Not covered:
    content-keying — a tool may still special-case a literal the variants carry (`pass=999`), and the harness does
    not randomise the edits; the names stay opaque only while the variant bytes are unknown to the tool.

130. **A registry checker reads what a reader sees: any line that renders as, or is quoted as, a table row is a row
    for the hidden-pin scan.** Lesson: `corpus/lessons/round-49.md` M4; `.ufo/waves/round-48/w2/R48CritV3Junk1.md`
    §1-§8. Rationale: v3's hidden scan recognised a row only when it began with up to three spaces and a pipe, so a
    row inline in an HTML comment after a blank line, a tab-indented fenced row, a four-space row outside a table
    and HTML table markup each kept a false pin (`PIN_CHECK_SELFTEST pass=999 fail=0`) while the tool printed
    `PIN_CHECK=met` (§1, §3, §4, §8) — and R2 already made a plain fenced row fatal on exactly that reasoning.
    Check: `python3 .ufo/waves/round-49/count-c1.py --tool tools/mori-pin-check.py --rev <rev>` prints one
    `variant name=…` line per edit; the four lines matching `name=N[1347] ` read `expect=unmet got=unmet rc=1`, and
    the two matching `name=H[67] ` read `expect=met got=met rc=0` (the same shapes carrying no pin token are not
    flagged); the real registry's verdict line carries `hidden=0 unparsed=0`. Shown able to fail: the entering tool
    prints `got=met rc=0` for N1, N3, N4 and N7
    (`evidence/control-c1-tool-v3-entering.txt`, `junk_met=9`), and R11 alone leaves them met
    (`evidence/control-c1-tool-r48-r11-only.txt`, `junk_met=7`). Not covered: "renders" is the GFM rule as read,
    not a renderer's output; the adjacency repair makes honest prose that quotes a tally on the first line after a
    table `hidden` (cost on the real registry: 0 lines, `w2/R48CritV3Junk1.md` §1); a pin token laundered into
    another script (fullwidth, Cyrillic) is a different class.

131. **A row's pin is bound to the instrument its own cells claim, and two rows binding one command agree on its
    exit contract.** Lesson: `corpus/lessons/round-49.md` M4 and `corpus/lessons/round-48.md` M3 ("Not closed:
    D7"); `.ufo/waves/round-48/w2/R48ExecD7.md` §2, §6. Rationale: v3 related no cell to the argv it measured, so
    a row whose entry cell names the source-drift probe while its self-test cell runs the pin checker and pins that
    checker's true tally scored `PIN_CHECK=met` (`w2/R48ExecD7.md` §2), and a second row for an already-registered
    command with a contradicting verdict map scored `met` with `duplicate=0` (`w2/R48CritV3Junk1.md` §6). Check:
    `python3 .ufo/waves/round-49/count-c1.py --tool tools/mori-pin-check.py --rev <rev>` — the lines matching
    `name=(N[589]|H[67]) ` read N5, N8 and N9 `got=unmet rc=1` and H6, H7 `got=met rc=0`; the real registry's
    verdict line carries `misattributed=0 duplicate=0`. Shown able to fail: N8 and N9 print `got=met` under the
    entering tool (`evidence/control-c1-tool-v3-entering.txt`); with only the five surface rules N9 stays `met`
    (`junk_met=1`, `evidence/control-c1-tool-r48-surface-fixes.txt`), and with only R11 N5-N9 stay `met`
    (`junk_met=7`, `evidence/control-c1-tool-r48-r11-only.txt`) — each half is separately required. Not covered:
    the carve-out for a `fixtures/`/`mutants/` path carrying the claimed instrument's basename
    (`w2/R48ExecD7.md` §8) is what keeps three legitimate rows green and is a stated limit, not a closed class; a
    junk row that copies the authority row's contract verbatim is consistent by construction.

132. **A depth entry about a retention bound names the journal, and dates every number it takes from the host.**
    Lesson: `corpus/lessons/round-49.md` Gate (the C2 named limits). Rationale: the staged entries this round
    rewrote state one bound for "the journal" — the reach is "bounded by **size**, not by age", 258.3M
    against a 256M ceiling, in the staged
    `/home/vgpnk/Projects/shokuknow/merge/mori/knowledge/corpus/knowledge/journal-reach-at-ceiling-r46.md` —
    while the 2026-10-25 receipt prints two journals with two ceilings (`Runtime Journal … max 64M`,
    `System Journal … max 256M`) and a total that moved from 269M (2026-10-24,
    `corpus/knowledge/journal-disk-usage-total-r51.md:10`) to 56M in one day
    (`corpus/evidence/sources-r49/host-journal-reach.txt:2,5`). A reach number without its day is a fact about
    another day. Check: `grep -nE '/(var|run)/log/journal' corpus/knowledge/journal-reach-r49.md` names both
    journals, `grep -oE '[0-9]+(\.[0-9])?M' corpus/knowledge/journal-reach-r49.md | sort -u` is a subset of the
    receipt's `56M 19M 37M 256M 64M 8M 45M 210.9M`, and the entry carries `verified-at: 2026-10-25`;
    `python3 .ufo/waves/round-49/count-c2.py <rev>` is `met`. Shown able to fail: the staged r46/r45 entries carry
    `258.3M`, `250.3M` and `243.6M`, none of which is in the 2026-10-25 receipt, and the r46 entry gives one size
    bound where the receipt prints two ceilings. Not covered: a number that matches the receipt is not thereby
    true today (the receipt is one capture; 269M → 56M inside a day), and the check does not decide which journal
    a window spans — that is a reader's claim against the located quotes, which the counter locates but does not
    entail.

133. **A round counts the defects its critics flagged and whether the landing fixed them.** Lesson:
    `corpus/lessons/round-49.md` Gate (considerthese item; `considerthese/2026-10-25.md` suggestion 3, opened
    2026-10-25). Rationale: round 45's `w1/CritAxisHarm.md` §1b flagged four false `SKILL.md` registry cells
    (`:184`, `:190`, `:191`, `:194`) in the worktree before they were committed, and no round-45 commit fixed
    them: `18fd68b0` wrote the cells, `git diff --numstat 18fd68b0 baabc992 -- SKILL.md` prints nothing, and
    `:190` still pins `C1_SELFTEST pass=10` at `baabc992` — so the flag changed no outcome and nothing in the
    round graded it (`corpus/lessons/round-45-verifier-spotcheck.md:50-57` re-measures the same cells as harmed).
    Check:
    `<command from ExecFlaggedFixed>` reads the round's defect list (one row per `## Findings` line of that round's
    `w1/Crit*.md` and `Rev*.md`), the landing diff and a re-run at the landing revision, and prints
    `flagged=N fixed=N unfixed=N`; the closure states the three numbers, and a defect counts FIXED only when the landing
    changes the named file/line or the defect no longer reproduces at the landing, UNFIXED when neither holds,
    NOT-APPLICABLE only with a stated reason. Shown able to fail: round 45 measures `flagged=4 fixed=0` against
    `baabc992` (cells `:184` and `:194` still pin `GATE_REGISTRY_SELFTEST pass=6`, `:190` still `pass=10` at
    `f80e75ac7421…`). Not covered: the script reads flags and diffs, not intent — a false flag counts like a true
    one (precision is not measured), and a defect fixed by an unrelated later edit counts FIXED.
```

## Provenance and limits

- Every receipt cited above exists at the path given and was opened by this seat; their digests match
  `evidence/freeze-sha256.txt` (item 1).
- I did **not** run `count-c1.py`, `count-c2.py` or any counter/`--selftest` myself (they are the freeze's
  receipts and a full C1 run is ~10 minutes). The verdict lines quoted are the committed receipt lines,
  not this seat's re-measurement. UNVERIFIED by this seat: that the counters still print those lines in
  the current tree.
- I did not render the SKILL.md variants with a Markdown implementation; "renders as a table / code block"
  is the GFM rule as read, and I copied that limit from `R48CritV3Junk1.md`'s own "Limits" section rather
  than upgrading it.
- 132 and 133 are shape/measurement criteria, not entailment criteria: a matching number does not prove
  the claim, and a `fixed=` count does not prove the fix was correct.
- Paths outside the lane (`/home/vgpnk/Projects/shokuknow/merge/mori/…`, `.ufo/waves/round-45/…`) were
  read only, as bytes.
- No tool was installed, so no tooling record is owed; the pacman guard was not touched.

## Findings

1. **MED — the round-49 M rows do not cover two of the five criteria.** `build-w1-spec.py:93` fixes the
   Mistakes rows at M1-M4 (opaque names, `.scratch` residue, author date, seven v3 survivors) and nothing
   in the dispatch gives candidates (d) and (e) an M row, so criteria 132 and 133 cite `## Gate`
   (`corpus/QUALITY.md`, criteria 132-133 as drafted here). Same defect class QUALITY 127 already carries.
   Fix: land (d)/(e) in Gate deliberately (as 127 did), or add M5/M6 in `corpus/lessons/round-49.md` and
   renumber the two `Lesson:` lines. The L1 decides; the draft's numbering note states the choice.

2. **LOW — two frozen control receipts are byte-identical, so the sniffer pair's new-counter half is not
   distinguishable by digest.** `evidence/control-c1-stub-always-met.txt` and
   `evidence/control-c1-stub-filename-sniffer.txt` both hash `673966107b7c…` in
   `evidence/freeze-sha256.txt`; both are all-`met` runs, so the counter output is identical and a reader
   comparing digests cannot tell that the sniffer was ever scored. The contract's freeze table names the
   files, so the provenance is recoverable; the digests just add no information. Fix: a future freeze
   should give each control a distinguishing marker line (or accept and note the collision).

3. **LOW — criterion 129's opacity is only over names, and the named limit is easy to exceed.** The
   harness hides J/H/N from the tool, but the variants are deterministic: a tool that keys on a literal the
   junk edits carry (`pass=999`) still passes all 18. I recorded this in the criterion's `Not covered:`; it
   is a limit of the predicate (contract C1 already routes content-keyed classes to wave 2), not a defect
   in the counter.

4. **LOW — criterion 133 depends on a command that does not exist yet.** `<command from ExecFlaggedFixed>`
   is a marker; the seat `Mo49ExecFlaggedFixed` was still running while this report was written, and
   `.scratch/r49-Mo49ExecFlaggedFixed/` held only an empty `rev` directory when I listed it (21:5x). If the
   counting script lands under `.scratch/`, it is scratch (per the contract's `.scratch` hygiene fix), not a
   citable instrument. The criterion is only as strong as that script's landing: if it stays in scratch,
   the Check line resolves nowhere at the carrying commit and the criterion must be rewritten or dropped.
   Fix: the L1 either lands the counting script under `.ufo/waves/round-49/` (or `tools/`) as part of the
   exit receipts, or replaces the marker with the landed path.

# Mo50bScribeQuality — QUALITY criteria 134–136 (round 50, wave a2w1)

Seat: scribe, leaf (no subagent). Assignment: draft `corpus/QUALITY.md` criteria after the last numbered one —
(a) self-assessment reconciliation per round, (b) reading a memcg OOM report by key and unit, (c) the next round
re-executes a closure's evidence-verified counter. Drafts are fenced inside this file; the L1 integrates. I edited
nothing else.

## 0. Environment and scope

| item | value |
|---|---|
| lane repo | `/home/vgpnk/Projects/shokunin/mori-shokunin` |
| lane HEAD during this run | `4548a34dc8b4072abaa4335c1f54a9efcfcc314a` |
| landed data revision (R) | `487941b9395e89678af0053cc443cdb49cdee6e3` |
| entering tip | `7197160b927f04db294c9553fb48fadcc7a3f4e3` |
| attempt-1 salvage | `9b8562a371dc916fdc0fc686619ea1e271a3e118` |
| scratch | `/fast/scratch/hyaku/mori-r50/Mo50bScribeQuality/` (`TMPDIR` set there for every call; removed in §7) |
| disk guard | `/home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status` rc 0; `/fast/scratch/hyaku` 23% used, 618.7G free; `/tmp` 2%, 125.3G free |
| tool installs / pacman | none |
| writes | this file only; `/home/vgpnk/Projects/shokuknow*` read-only (three file reads, no execution) |
| host | no host log read, no MESSAGE grep, no cgroup or systemd change, no OOM triggered |

Revisions verified before use: `git merge-base --is-ancestor 487941b9 HEAD` → 0.

## 1. What the house shape requires, and the one file that is not there

- `corpus/QUALITY.md` is 1174 lines; the last numbered criterion is **133** at `:1159` (section heading
  `## Criteria added round 49 …` at `:1089`), and the file ends with criterion 133's `Not covered` clause plus two
  blank lines. `grep -n '^13[3-9]\.' corpus/QUALITY.md` → only `1159:133.` — numbers 134–136 are free.
- Shape read from 129–133: bold title sentence, `Lesson:`, `Rationale:`, `Check:` (a command), `Shown able to
  fail:` (a receipt path under `evidence/`, or `not yet shown`), `Not covered:`.
- `corpus/lessons/round-50.md` **does not exist** at the revision I am drafting against or in HEAD:
  `git cat-file -e 487941b9:corpus/lessons/round-50.md` → `fatal: path 'corpus/lessons/round-50.md' does not exist
  in '487941b9'`, rc 128; the same at `4548a34d`, rc 128; `ls corpus/lessons/round-50.md` → rc 2. The lesson rows
  this wave dispatched (`Mo50bScribeMistakes`, `Mo50bScribeLessonGate` in `a2w1`) are `M1` self-assessment drift,
  `M2` the round-49 "48 vs 47" report count, `M3` the attempt-1 crashed wave. So the `M1` pointer in criterion 134
  below is the row the mistake scribe was told to write; the pointers in 135 and 136 are to the lesson's `Gate`
  section, because no dispatched `M#` covers those classes (precedent: criterion 132 cites `round-49.md` `Gate`,
  not an `M#`).

## 2. Draft — heading and criterion 134 (candidate a)

```markdown
## Criteria added round 50 — a self-assessment that is reconciled, a unit per line, a closure that is re-executed

134. **A round reconciles its own self-assessment with the fleet record and with the instruments, and every pin it
    corrects carries a committed receipt.** Lesson: `corpus/lessons/round-50.md` M1 (self-assessment drift).
    Rationale: `SHONEN.md` pinned `(60/60)` and `(13/13)` from round 48 on while the committed instruments printed
    `PIN_CHECK_SELFTEST pass=114 fail=0` and `UNLANDED_SELFTEST pass=17 fail=0`, and four `SCORECARD.md` `## Axes`
    Last change cells named rounds 26, 31, 31 and 25 while the fleet `MANIFEST.json` at
    `e014499613f63f8a467821219b0296121119ca53` graded rounds 47, 47, 49 and 49 `improved` — six mismatches at the
    entering tip `7197160b` (`evidence/control-c1-do-nothing.txt`); QUALITY 123 reads `SKILL.md`'s registry only
    ("A registry pin is calibrated only when an instrument re-runs it from committed bytes and reads it from its
    own cell", `:1028-1029`), so the lane's own self-assessment was outside every check. Check:
    `python3 .ufo/waves/round-50/count-c1.py <rev>` prints
    `C1=met items=8 axes=6 pins=2 boxes=4 mismatches=0 errors=0 hidden=0` and exits 0, and each pinned tally's
    observed line is committed under `.ufo/waves/round-50/evidence/selftests/<stem>.txt`. Shown able to fail: at
    `7197160b` the same command prints `C1=unmet items=8 axes=6 pins=2 boxes=4 mismatches=6 errors=0 hidden=0 …
    failed=mismatch` exit 1 (`evidence/control-c1-do-nothing.txt`); a corrected tally with no committed receipt
    stays unmet (`evidence/control-c1-pins-updated-no-receipt.txt`, `mismatches=6`); a blanket "every cell names
    round 49" edit stays unmet (`evidence/control-c1-all-latest.txt`, `mismatches=6`); deleting the pins fails the
    floor (`evidence/control-c1-pins-deleted.txt`, `pins=0`). Not covered: the Score column (the MANIFEST carries
    verdicts, not scores); the counter trusts the fleet MANIFEST instead of re-judging the closures; the
    Last-change convention itself is not scored; a tally pin outside `SHONEN.md` is not enumerated (`hidden` scans
    `SHONEN.md` only); and the counter's fleet revision is pinned, so a later closure moves the expected `round N`
    without moving this receipt.
```

## 3. Draft — criterion 135 (candidate b)

```markdown
135. **A memcg OOM report is read key by key with each line's own unit, and the cgroup's composition is taken from
    the stats block, never from the victim line.** Lesson: `corpus/lessons/round-50.md` Gate — the C2 named limits
    (the class is the rejected `scope-charge-fields-r46.md` hypothesis; `M1`–`M3` do not cover it). Rationale: the
    staged r46 entry reasoned from the victim's own growth — "a child that writes into `/tmp` consumes the scope's
    cap **without the victim process growing at all** — and the victim's own `anon-rss` would never show it" — a
    statement about the cgroup's composition drawn from a per-process line; and the report's numbers split three
    ways, the usage and swap lines and the `Killed process` fields in kB, the `Tasks state (memory values in
    pages)` table in pages, and the `Memory cgroup stats` block in bytes. Check:
    `for p in 'Units are per line' 'Read the block by key' 'charge, not the victim'; do printf '%s -> ' "$p";
    grep -c -- "$p" corpus/knowledge/oom-memcg-stat-r50.md; done` prints `Units are per line -> 1`,
    `Read the block by key -> 1`, `charge, not the victim -> 1`, and
    `awk '/^- Units are per line/,/^$/' corpus/knowledge/oom-memcg-stat-r50.md | grep -oE 'kB|bytes|pages' |
    sort -u` prints `bytes`, `kB`, `pages` — the anchors are the check, so an entry whose prose moves keeps its
    verdict (at `487941b9` the rules sat at `:46-48`, `:49`, `:56-58`; a same-day data correction moved two of
    them to `:52` and `:61`). Shown able to fail: the three greps over the rejected staged
    `/home/vgpnk/Projects/shokuknow/merge/mori/knowledge/corpus/knowledge/scope-charge-fields-r46.md` print `0`,
    `0`, `0` (exit 1), and over a copy of the landed entry with the units bullet deleted and the charge bullet
    reworded into a victim-property claim they print `0`, `1`, `0` — an entry that does infer composition
    (demonstrated in `.ufo/waves/round-50/a2w1/Mo50bScribeQuality.md` §5; no committed evidence receipt, so this
    arm is `not yet shown` as a file under `evidence/`). Not covered: the greps prove the rule is written, not
    that a reader follows it, and no counter reads prose (the round's C2 counter locates quotes and checks
    provenance); the `pg*`/`workingset_*` keys of memory.stat are event counts, not bytes, and the check does not
    test that; and the entry states what kernel v7.2 prints, not what any kill on this host printed (no MESSAGE
    read — lane rule).
```

## 4. Draft — criterion 136 (candidate c)

```markdown
136. **The round after a closure re-executes that closure's frozen counter at the revision the closure scored, and
    reports a divergence instead of smoothing it.** Lesson: `corpus/lessons/round-49.md` Gate ("Ruling:
    **verified** (evidence-verified, not re-executed)"); `considerthese/2026-10-26.md` suggestion 3 (operator
    reflection, opened 2026-10-26); `corpus/lessons/round-50.md` Gate (to be written). Rationale: the round-49
    ruling rests on committed receipts the integrator did not run, and the same closure records an "undocumented
    off-by-one (27 `variant` lines vs `variants=26`)" that only a re-execution settles — the counter's verdict
    line prints `len(results) - 1` (`.ufo/waves/round-49/count-c1.py:304-305`), counting out the `real` run, which
    is one of the 27 `variant` lines in both of the round's receipts; a reader holding only the receipt cannot tell
    a wrong line from a wrong closure. Round 50 re-ran its own counters at the landed revision with committed
    receipts (`evidence/a2-c1-at-data.txt`, `evidence/a2-c2-at-data.txt`; `a2w1/Mo50bExecC1Rerun.md` §1a). Check:
    `git show 64c2d5fc:tools/mori-pin-check.py > <scratch>/pin-check-at-64c2d5fc.py` then
    `python3 .ufo/waves/round-49/count-c1.py --tool <scratch>/pin-check-at-64c2d5fc.py --rev 64c2d5fc --scratch
    <scratch>/r49c1 --jobs 4 | grep '^C1='` compared with `grep '^C1='
    .ufo/waves/round-49/evidence/after-c1-at-tip.txt` — the two lines are equal and `diff` of them is empty, exit
    0, and the round's report quotes the re-executed line with its exit code. Shown able to fail: the same counter
    run with the v3 tool at `b3e3453d` prints `C1=unmet junk_met=9 honest_unmet=0 real=met errors=0 variants=26 rev=
    b3e3453d…` (`.ufo/waves/round-49/evidence/control-c1-tool-v3-entering.txt`), so a stale tool and a re-executed
    one are distinguishable by the verdict line; no committed receipt yet records a closure whose re-execution
    contradicts it, so the divergence arm is `not yet shown`. Run once for the agreement arm: 9m29s wall with
    `--jobs 4`, `C1=met … variants=26 rev=64c2d5fc…`, `diff` empty, and
    `python3 .ufo/waves/round-49/count-c2.py 24ebc799` printing the same `C2=met claims=21 located=21 …` line as
    `evidence/after-c2-at-24ebc799.txt`, `diff` empty
    (`.ufo/waves/round-50/a2w1/Mo50bScribeQuality.md` §5f). Not covered: a matching line proves the counter and
    the bytes are re-runnable at R, not that the counter's arms are good (its `--selftest` does that); the
    re-execution trusts the committed counter, so a counter edited after its freeze is not detected (that is
    `sha256sum -c evidence/freeze-sha256.txt`'s job); a closure scored at a revision no longer reachable from the
    lane's branches cannot be re-executed at all; and the C1 run costs minutes of CPU, so it is one check per
    round, not per seat.
```

## 5. Every check I propose, run once (verbatim, with exit codes)

All runs: `cd /home/vgpnk/Projects/shokunin/mori-shokunin`, `export
TMPDIR=/fast/scratch/hyaku/mori-r50/Mo50bScribeQuality/tmp`, scratch arg
`/fast/scratch/hyaku/mori-r50/Mo50bScribeQuality/…`.

### 5a. P-C1 at the landed data (criterion 134, met arm)

```
$ python3 .ufo/waves/round-50/count-c1.py 487941b9395e89678af0053cc443cdb49cdee6e3 --scratch "$S/c1-landed"
...
item pin python3_tools/mori-pin-check.py_--selftest expect=(114/114) got=PIN_CHECK_SELFTEST_pass=114_fail=0 state=ok
item pin python3_tools/mori-unlanded-check.py_--selftest expect=(17/17) got=UNLANDED_SELFTEST_pass=17_fail=0 state=ok
C1=met items=8 axes=6 pins=2 boxes=4 mismatches=0 errors=0 hidden=0 manifest=a94551c5bc8d rev=487941b9395e89678af0053cc443cdb49cdee6e3
EXIT=0
```

### 5b. P-C1 at the entering tip (criterion 134, fail arm)

```
$ python3 .ufo/waves/round-50/count-c1.py 7197160b927f04db294c9553fb48fadcc7a3f4e3 --scratch "$S/c1-entering"
C1=unmet items=8 axes=6 pins=2 boxes=4 mismatches=6 errors=0 hidden=0 manifest=a94551c5bc8d rev=7197160b927f04db294c9553fb48fadcc7a3f4e3 failed=mismatch
EXIT=1
```

Byte-identical to `evidence/control-c1-do-nothing.txt` (same `manifest=a94551c5bc8d`, same six mismatches).

### 5c. Criterion 135's check on the landed entry (met arm)

First read (working tree before the 09:59 edit — see §7) and again after it; both passes identical:

```
$ for p in 'Units are per line' 'Read the block by key' 'charge, not the victim'; do printf '%s -> ' "$p"; grep -c -- "$p" corpus/knowledge/oom-memcg-stat-r50.md; done
Units are per line -> 1
Read the block by key -> 1
charge, not the victim -> 1
$ awk '/^- Units are per line/,/^$/' corpus/knowledge/oom-memcg-stat-r50.md | grep -oE 'kB|bytes|pages' | sort -u | tr '\n' ' '
bytes kB pages
```

The three anchors are the check; the line numbers move with the entry's prose. At the first read they sat at
`:46-48`, `:49`, `:56-58`; after the 09:59 edit, at `:46-48`, `:52`, `:61`.

### 5d. Criterion 135's check on the rejected staged entry (fail arm A)

```
$ for p in 'Units are per line' 'Read the block by key' 'charge, not the victim'; do printf '%s -> ' "$p"; grep -c -- "$p" /home/vgpnk/Projects/shokuknow/merge/mori/knowledge/corpus/knowledge/scope-charge-fields-r46.md; done
Units are per line -> 0
Read the block by key -> 0
charge, not the victim -> 0
EXIT=1
```

### 5e. Criterion 135's check on a scratch mutant of the landed entry (fail arm B, report-only)

The mutant is a copy of the **current** entry bytes (the 09:59 edit) with only the `Units are per line` bullet
removed and `The block is the cgroup's charge, not the victim's,` replaced by `The block describes the victim
process's composition,` (`12617` → `11958` bytes; `Read the block by key` is left in place, so exactly one anchor
fails for a reason that is not "the whole rule list is gone"):

```
$ for p in 'Units are per line' 'Read the block by key' 'charge, not the victim'; do printf '%s -> ' "$p"; grep -c -- "$p" "$S/entry-mutant3.md"; done
Units are per line -> 0
Read the block by key -> 1
charge, not the victim -> 0
EXIT=1
```

An earlier take on the pre-edit bytes (`entry-mutant.md`, `10520` → `10222`) printed the same `0, 1, 0`. There is
**no committed receipt** for this arm: the seat may write only its own report under `.ufo/waves/round-50/`, so
criterion 135's `Shown able to fail` names §5e of this report and stays `not yet shown` as an evidence file. A
reader can reproduce it from the commands above.

### 5f. Criterion 136's check — the round-49 counters re-executed at their scored revisions

Tool bytes at the scored revision: `git show 64c2d5fc:tools/mori-pin-check.py` and the scratch copy both sha256
`697ab2cc6ca6702a5abcf361f48bee31570b4c58ddcc386f41c84c84b5c08e39`.

```
$ python3 .ufo/waves/round-49/count-c1.py --tool "$S/pin-check-at-64c2d5fc.py" --rev 64c2d5fc --scratch "$S/r49c1" --jobs 4 > "$S/r49-c1-reexec.txt" 2> "$S/r49-c1-reexec.err"
real	9m29.064s   user 19m18.958s   sys 8m2.383s        EXIT=0   (stderr: 0 bytes)
$ tail -3 "$S/r49-c1-reexec.txt"
variant name=real expect=met got=met rc=0
variant name=real-opaque expect=met got=met rc=0
C1=met junk_met=0 honest_unmet=0 real=met errors=0 variants=26 rev=64c2d5fcd95a11f195de0387fa791cab7a54ecb1
$ grep -c '^variant' "$S/r49-c1-reexec.txt"      -> 27
$ diff <(grep '^C1=' "$S/r49-c1-reexec.txt") <(grep '^C1=' .ufo/waves/round-49/evidence/after-c1-at-tip.txt)
$ echo $?                                          -> 0        (no output: the two verdict lines are identical)
```

The round-49 closure line is reproduced byte for byte from the committed counter and the tool bytes at `64c2d5fc`
(`2026-10-25T22:49:54-03:00`; re-executed `2026-10-26`, about eleven hours later) — so that closure's C1 verdict is
now re-executed, not only evidence-verified. The
re-execution also confirms the "27 `variant` lines vs `variants=26`" observation: the `real` run is one of the 27
`variant` lines and is excluded by `len(results) - 1` (`.ufo/waves/round-49/count-c1.py:304-305`). Cost: 9m29s
wall on this host with `--jobs 4` — the check is a per-round step, not a per-seat one.

The round-49 C2 counter, same treatment (pure `git show` parsing, no instrument runs):

```
$ python3 .ufo/waves/round-49/count-c2.py 24ebc7991e9081348d1aa4f558f994b1f4feccab
C2=met claims=21 located=21 quote_missing=0 bad_rows=0 sources=4 source_rows=ok pins=ok provenance=ok rev=24ebc7991e9081348d1aa4f558f994b1f4feccab
EXIT=0
$ diff <(grep '^C2=' …) <(grep '^C2=' .ufo/waves/round-49/evidence/after-c2-at-24ebc799.txt)
$ echo $?   -> 0          (identical)
```

Both round-49 closure verdicts therefore reproduce from the committed counters at the revisions their receipts
name. Neither divergence nor ambiguity was found beyond the `variants` counting in §5f's first block.

## 6. Fail arms and their status

| criterion | met arm (observed) | fail arm (receipt) | fail arm status |
|---|---|---|---|
| 134 | `C1=met … mismatches=0` at `487941b9`, exit 0 (§5a) | `C1=unmet … mismatches=6` at `7197160b`, exit 1 (§5b; `evidence/control-c1-do-nothing.txt`) | committed; six further controls committed (`pins-updated-no-receipt`, `all-latest`, `pins-deleted`, `axes-only`, `shonen-only`, `box-dropped`) |
| 135 | three greps `1,1,1` + unit tokens `bytes kB pages` (§5c) | staged r46 entry `0,0,0` (§5d); scratch mutant `0,1,0` (§5e) | committed for the staged entry (`/home/vgpnk/Projects/shokuknow/…`, read-only, not an `evidence/` file); mutant arm `not yet shown` |
| 136 | both round-49 verdict lines reproduced: `C1=met junk_met=0 … variants=26 rev=64c2d5fc…` and `C2=met claims=21 located=21 … rev=24ebc799…`, `diff` exit 0 against their receipts (§5f) | v3 tool at `b3e3453d` → `C1=unmet junk_met=9 … variants=26` (`evidence/control-c1-tool-v3-entering.txt`) | committed; the divergence arm (a closure contradicted by its own re-execution) is `not yet shown` |

## 7. Scratch, concurrent edits, and provenance

Scratch `/fast/scratch/hyaku/mori-r50/Mo50bScribeQuality/` was used in two passes: the counter runs (§5a, §5b,
§5f) with `tmp/`, `c1-landed/`, `c1-entering/`, `r49c1/`, `pin-check-at-64c2d5fc.py`, `entry-mutant.md` and the
captured outputs (`c1-landed.txt`, `c1-entering.txt`, `r49-c1-reexec.txt`, `r49-c1-reexec.err`,
`r49-c2-reexec.txt`) — removed, `du -sh` 4.2M — and then, because the entry changed under me (below), a second pass
for the post-edit entry checks (§5c, §5e) with `tmp/`, `entry-mutant2.md`, `entry-mutant3.md` — removed, `du -sh`
24K. Final state: `ls -d /fast/scratch/hyaku/mori-r50/Mo50bScribeQuality` → `No such file or directory`, rc 2.
`/tmp` was used for nothing, and no evidence path in this report is a `/tmp` path (the `/tmp` tokens in §§2–3 are
quoted text from the entry and from the staged claim). No clone was made (the counters read the lane repo with
`git show`/`git archive`); their archive trees lived and died inside my scratch tree.

Concurrent edits, observed and not mine: at `2026-10-26 09:59` the working tree carried modifications to
`SHONEN.md` (`09:59:42`), `corpus/SOURCES.md` (`09:59:13`), `corpus/knowledge/oom-memcg-stat-r50.md` (`09:59:34`)
and `SCORECARD.md`, i.e. by other seats/the L1 integrating this wave while I read; `git diff --stat` at `10:00` →
4 files, 56 insertions, 28 deletions. I wrote none of them (my only write is this file, mtime `10:00:04`). Every
counter verdict in §5a, §5b and §5f came from a **committed revision** (`git archive`/`git show` of `487941b9`,
`7197160b`, `64c2d5fc`, `24ebc799`), so those lines do not depend on the dirty tree; the §5c–§5e entry greps were
run twice, before and after the 09:59 edit, with the same verdicts.

Provenance of every claim above: the command in its section, run in this seat, with the revision named. The two
staged-entry reads were file reads under `/home/vgpnk/Projects/shokuknow/merge/mori/…` (read-only, nothing
executed there). No report, register or counter was edited; the frozen bytes were used as committed
(`python3 .ufo/waves/round-50/count-c1.py`, `.ufo/waves/round-49/count-c1.py`, `.ufo/waves/round-49/count-c2.py`).

## Findings

- **MED — F1** `corpus/lessons/round-50.md` is absent at `487941b9` and at HEAD (`git cat-file -e …` rc 128, `ls`
  rc 2), so the `Lesson:` pointers in criteria 134–136 are prospective. M1 (drift) is the row the mistake scribe
  was dispatched to write; no dispatched `M#` covers the (b) and (c) classes, so 135 and 136 point at the lesson's
  `Gate` section (precedent: criterion 132). The integration must land the lesson file **with** these criteria, or
  the criteria cite a row that does not exist.
- **LOW — F2** `corpus/QUALITY.md:1028-1029` (criterion 123) scopes calibration to `SKILL.md`'s registry, so the
  lane's own `SCORECARD.md` Axes cells and `SHONEN.md` pins had no criterion until this one — that is the
  `captured-by` cell of the lesson's M1 row ("none — QUALITY 123 reads `SKILL.md`'s registry only"). Criterion 134
  closes it for the Axes Last-change/Evidence cells and the SHONEN tally pins; the Score column, other files and a
  pin outside `SHONEN.md` remain uncovered, as the criterion says.
- **LOW — F3** `corpus/knowledge/oom-memcg-stat-r50.md:46-58` states the per-line units and the victim-versus-charge
  rule in prose that no counter reads: `count-c2.py` locates quotes and checks provenance only. Criterion 135's
  check is a grep for three anchor sentences — it proves the rule is written, not obeyed, and its mutant arm has
  no committed receipt (this report §5e). A later round either commits a receipt or accepts the `not yet shown`
  label.
- **LOW — F4** `.ufo/waves/round-49/count-c1.py:304-305` counts `variants=len(results) - 1` while the output carries
  one `variant` line per run including `real`, so every round-49 receipt prints 27 `variant` lines beside
  `variants=26`; the counter's docstring (`:17`, `:38`) states the output shape without defining `variants`. The
  round-49 closure records this as an "undocumented off-by-one". Counter frozen for this round: named as a limit of
  criterion 136, not proposed as a fix.
- **LOW — F5** Criterion 136's divergence arm is `not yet shown`: no committed receipt in this lane records a
  re-execution that contradicts a closure's verdict line. The nearest committed discriminator is the v3-tool run
  (`evidence/control-c1-tool-v3-entering.txt`, `C1=unmet junk_met=9`), which shows the command separates a stale
  tool from a repaired one, not a closure from its re-execution.
- **LOW — F6** `corpus/lessons/round-49-verifier-spotcheck.md:37` ("The verdict comes from the lane's frozen
  counter `count-c1.py`, which I did not run") and `:55` ("Ruling: **verified** (evidence-verified, not
  re-executed)") are now discharged in fact — §5f re-executed both round-49 counters at the revisions their
  receipts name and both agreed byte for byte — yet the closure file still carries the caveat, and the
  re-execution exists only in this wave report. The round-50 closure should cite §5f; the round-49 file is a
  historical closure and was not edited.
- **LOW — F7** `corpus/knowledge/oom-memcg-stat-r50.md` was edited in the working tree at `09:59:34` while this
  seat was reading it (unattributed: `SHONEN.md`, `corpus/SOURCES.md` and `SCORECARD.md` changed in the same
  minute), moving two of criterion 135's anchors from `:49`/`:56` to `:52`/`:61`. A criterion whose `Check` cites
  line numbers goes stale on any correction; 135 therefore binds to the three anchor sentences and re-verifies the
  unit tokens by paragraph (`awk '/^- Units are per line/,/^$/'`), which returned `bytes kB pages` before and after
  the edit. Criteria 128/132/133 cite line numbers, so the same caveat applies to them; it is not repaired here.

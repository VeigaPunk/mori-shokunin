# Round 29 W1 — draft QUALITY criteria (scribe)

Seat `MoriR29.DraftQualityCriteria`, leaf scribe. Target: `corpus/QUALITY.md`, appended after criterion 84
(`corpus/QUALITY.md:401-412`). Nothing was installed or upgraded. No file in the lane was written except this report;
test fixtures live under `/fast/scratch/hyaku/mori-r29/DraftQualityCriteria/`.

## What was read

- `corpus/QUALITY.md:366-412` — numbering and shape of the last two sections (next number 85).
- `corpus/lessons/round-28-verifier-spotcheck.md:99-133` — §4 sample, §6 routed defects 3 and 4 at `:128`, `:129-130`.
- `corpus/lessons/round-28.md:52-56` (M5), `:63-72` (Gate table), `:108`, `:117-118`, `:121`, `:143-146` (M6).
- `.ufo/waves/round-29/contract.md` — hygiene items 2, 3, 4; `.ufo/waves/round-29/wave1-spec.json` — the planned
  contracts of `check-blind-wave.sh` and `make-tip-receipts.sh`.
- `tools/mori-oom-killers.py` was never opened, grepped, copied or run; no round-26/27/28 `w1`/`w2` report was opened
  (only `git ls-tree` names, to confirm the freeze tree holds reports). No tool source lines or tool output appear here.

## Verification observed (commands and results)

| What | Command | Result |
|---|---|---|
| Gate check, round 28 | awk pipeline below on `7118f320:corpus/lessons/round-28.md` | `gate_reject_rows=0 none_declared=0 malformed=0`, exit 1 |
| Gate check, round 25 | same on `7118f320:corpus/lessons/round-25.md` | `gate_reject_rows=7 none_declared=0 malformed=0`, exit 0 |
| Gate declaration | round-28 text plus `reject sample: none met` inside the Gate section | `none_declared=1`, exit 0 |
| Gate malformed reject | synthetic `\| reject \|` row with no reason | `malformed=1`, exit 1 |
| Tip structural check | `bash .ufo/waves/round-28/check-tip-receipts.sh 1fc6bb0 28` | `tip_receipts=met`, exit 0 |
| Tip header check | criterion 87 command on `1fc6bb0 28` | `header_not_parent=…/tip-count-c1.txt`, exit 1 (first line is `revision: 5ef4e8db…`) |
| Tip scope red | scope assertion on `5ef4e8d` (parent of the receipt batch) | `tip_adds_nonreceipt=LOG.md`, exit 1 |
| Tip green | two-commit scratch repo, tip adds one receipt with the exact header | `tip_receipts=met receipts=1 only_receipts=yes`, exit 0 |
| Round-28 freeze tree | `git ls-tree -r --name-only d21b8bd3 -- .ufo/waves/round-28/w1 \| wc -l` | `28`, including `CriticC2Design.md`, `ReviewA2SpecVsTool.md`, `CaseA2r03.md` |
| Bad-rev path (criterion 86 guard) | `git cat-file -e deadbeef:corpus/lessons/round-28.md` | absent, guard exits 2 |

All inputs were committed bytes read with read-only git. Scratch git writes ran only under
`/fast/scratch/hyaku/mori-r29/DraftQualityCriteria/`, with `GIT_DIR`/`GIT_WORK_TREE`/`GIT_INDEX_FILE` unset.

## Findings

1. **The round-28 receipt batch does not meet criterion 87.** `git show 1fc6bb0:.ufo/waves/round-28/evidence/tip-count-c1.txt`
   line 1 is `revision: 5ef4e8db397b57299616258cb2e1c045c46564e7` — it does not say `measured at parent`, and no line says
   the tip adds only receipts. The batch itself adds only three evidence files (`git show --stat 1fc6bb0`), so only the
   header half is red. This is the input routed at `round-28-verifier-spotcheck.md:129-130`.
2. **Round 28's Gate cannot supply a reject sample.** All eight rows `S145`–`S152` decide `admit`
   (`corpus/lessons/round-28.md:65-72`); the spot-check had to take its reject from the re-opened `S097`/`S146`
   (`round-28-verifier-spotcheck.md:107`, `:109-110`). The proposed criterion makes that state red until a round either
   records a reject row or declares `reject sample: none met`.
3. **The BuildBlindCheck dispatch names a revision that does not exist.** `wave1-spec.json` tells the seat to run the
   check "at 06d6a5b8"; `git cat-file -t 06d6a5b8` says `Not a valid object name`, while `06d6a5b` exists ("round-28:
   wave-2 reports, lesson corrections from wave 2, S147 Gate cell fix"). The round-28 C2 freeze is `d21b8bd3`
   (`corpus/lessons/round-28.md:128`), which holds all 28 `w1` reports. The criterion cites `d21b8bd3`, not `06d6a5b8`.
4. **Criterion 85 is unenforced until `check-blind-wave.sh` lands.** The script is planned
   (`wave1-spec.json`, BuildBlindCheck) and its red/green runs are not yet observed; the criterion says so rather than
   claiming a pass. What is grounded: the lesson records two non-writer seats that read the tool
   (`corpus/lessons/round-28.md:121`) and one writer that read `w1/CriticC2Design.md` (`:143-144`), which are exactly
   the inputs check (a) must catch.
5. **Round-25 previews the criterion 86 shape.** Its Gate carries seven `reject, C` rows
   (`corpus/lessons/round-25.md:65-71`) and the check passes; its reject rows carry `none:` in the quote cell, so the
   check accepts a no-body reason instead of demanding a digest. No lesson yet carries `reject sample: none met`.

## Limits

- Criterion 86's check cannot prove that a reject met during source work was not silently dropped; it proves the Gate
  is samplable and well formed. The closure must still cross-read the round's source work, as round 28 did.
- Criterion 87's green run is a synthetic two-commit repo, not a landed round-29 tip, because the round-29 counters and
  receipts do not exist yet (`count-c1.sh`/`count-c2.sh` are not committed at this writing).
- The exact header string in criterion 87 must match `make-tip-receipts.sh` byte for byte; the planned header in the
  BuildTipReceipts dispatch is the source used here.

## Ready-to-paste block (append to `corpus/QUALITY.md`)

```markdown
## Criteria added round 29 — round-28 routed defects

85. At the freeze commit of a writer-blind wave, no report in the writers' wave directory written by a non-writer
    cites a tool line or carries tool-run output, and every writer report lists the files it opened. A non-writer is
    a committed report whose file name does not match the wave's declared writer-name regex. A citation is
    `mori-oom-killers.py:<digits>`, `mori-oom-killers.py` followed by a line range, or a `Tool lines` table header;
    tool-run output is a `MORI_OOM_KILLERS_SELFTEST:` line other than a PASS tally of an older case file, a
    `KILLERS_QUIET exit` line, or an `--inputs` repro result. A files-opened list is a `Files opened` line or heading
    followed by at least one path, and it names no forbidden path: the tool, any `w1/` or `w2/` report other than its
    own, or `corpus/lessons/`. ← lessons/round-28-verifier-spotcheck.md:126-127; lessons/round-28.md:143-146 (M6),
    :117-118, :121. Check: `bash .ufo/waves/round-29/check-blind-wave.sh <lane-rev> <wave-report-dir>
    <writer-name-regex>` reads only committed bytes at `<lane-rev>`, prints `blind_violations=<n>` and one line per
    violation naming the file and line number (never the matched text), and exits 0 when n=0, 1 otherwise, 2 on a bad
    revision or a usage error. For the M6 fix it must exit 1 on the round-28 freeze `d21b8bd3` at
    `.ufo/waves/round-28/w1` with `^CaseA2r`, and exit 0 on a synthetic clean directory; the round-29 build records
    both runs. Until that script is committed the criterion is unenforced and no round may claim it. Red inputs: a
    non-writer report containing `mori-oom-killers.py:305`; a `CaseA2r` report with no files-opened list; a writer
    list naming `w1/CriticC2Design.md` (the M6 disclosure) or `corpus/lessons/round-28.md`.

86. A round lesson's `## Gate` table records every reject decision its source work met as its own row, so a
    non-author closure can sample a reject from the Gate. Each decision cell reads `admit, …` or `reject, <reason>`;
    a reject row names the source it rejected (a URL, `own-work:` or `gist:`) and a non-empty located quote. A Gate
    with no reject row carries `reject sample: none met` inside its own section; a closure that samples that
    declaration states that it re-opened no reject. ←
    lessons/round-28-verifier-spotcheck.md:128 (§6.3), :107, :109-110; lessons/round-28.md:63-72 (eight rows, all
    admit, so the round's only reject sample came from the re-opened S097/S146). Check, over committed bytes:
    `git -C <lane> cat-file -e <rev>:corpus/lessons/round-<N>.md || exit 2`
    `git -C <lane> show <rev>:corpus/lessons/round-<N>.md | awk -F'|' '/^## Gate/{s=1;next} s&&/^## /{s=0} s&&/^\| *S[0-9]+ *\|/{d=$(NF-1);src=$3;q=$(NF-2);gsub(/^ +| +$/,"",d);gsub(/^ +| +$/,"",src);gsub(/^ +| +$/,"",q); if(d~/^reject, /){rej++; if(d!~/^reject, [^ ]/||src!~/^(https?:\/\/|own-work:|gist:)/||q=="")bad++} else if(d!~/^admit, /)bad++} s&&/^reject sample: none met/{none=1} END{printf "gate_reject_rows=%d none_declared=%d malformed=%d\n",rej+0,none+0,bad+0; exit ((bad==0&&(rej>=1||none==1))?0:1)}'`
    prints `gate_reject_rows=<n> none_declared=<0|1> malformed=<n>` and exits 0 when no row is malformed and a
    reject row or the declaration exists, 1 otherwise, 2 on a missing lesson. It FAILS on round 28 at `7118f320`
    (`gate_reject_rows=0 none_declared=0`, exit 1) and PASSES on `round-25.md` (`gate_reject_rows=7`, exit 0). Red
    inputs: a Gate of admit rows only with no declaration (round 28's state); a decision cell `reject` with no reason;
    a reject row with an empty source or quote cell.

87. A tip receipt measured at the first parent of the batch that lands it says so in its header, and that batch adds
    only receipt files. Every file added at `<rev>` against `<rev>^` lives under `.ufo/waves/round-<N>/evidence/` and
    opens with the exact line `# measured at parent <first-parent 40-hex>; the landed tip adds only receipt files
    under .ufo/waves/round-<N>/evidence/`; the receipts keep QUALITY 84's shape. The report that cites them lies in an
    earlier batch and names the receipt files it expects. ← lessons/round-28-verifier-spotcheck.md:129-130 (§6.4);
    lessons/round-28.md:52-56 (M5), :108. Check: `bash -c 'lane=$1; rev=$2; round=$3; R=$(git -C "$lane" rev-parse "$rev^{commit}")||exit 2; P=$(git -C "$lane" rev-parse "$R^1")||exit 2; bash "$lane/.ufo/waves/round-28/check-tip-receipts.sh" "$R" "$round"||exit 1; a=$(git -C "$lane" diff --name-only "$P" "$R"); [ -n "$a" ]||{ echo no_added_files; exit 1; }; n=0; for f in $a; do case "$f" in ".ufo/waves/round-$round/evidence/"*) ;; *) echo "tip_adds_nonreceipt=$f"; exit 1;; esac; h=$(git -C "$lane" show "$R:$f"|sed -n 1p); w="# measured at parent $P; the landed tip adds only receipt files under .ufo/waves/round-$round/evidence/"; [ "$h" = "$w" ]||{ echo "header_not_parent=$f"; exit 1; }; n=$((n+1)); done; echo "tip_receipts=met receipts=$n only_receipts=yes"; exit 0' _ <lane> <rev> <round>` runs the QUALITY 84 checker
    first, then the header and diff-scope assertions; it prints `tip_receipts=met receipts=<n> only_receipts=yes`,
    exit 0, or names the first offending file, exit 1, 2 on a bad revision. It FAILS on the round-28 receipt batch
    `1fc6bb0` (`header_not_parent=…/tip-count-c1.txt`, exit 1: line 1 is `revision: 5ef4e8db…`) and on a batch that
    also edits `LOG.md` (`tip_adds_nonreceipt=LOG.md`); it PASSES on a synthetic two-commit repo whose tip adds one
    receipt with the header (exit 0). Red inputs: a receipt whose header names the tip's own hash or a grandparent; a
    tip batch that edits the lesson or `LOG.md`; a receipt without the `exit:` line.
```

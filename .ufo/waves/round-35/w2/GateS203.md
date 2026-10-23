measured 2026-10-23T09:14:58Z

# GateS203 — re-open source row S203

VERDICT: reject — I agree with the gate's rejection.

Row under attack: `corpus/SOURCES.md:209` at `cedb0ec4f3a4f672804deac388b7191258f01fcd`; Gate line `corpus/lessons/round-35.md:22` at the same rev. Source URL `https://raw.githubusercontent.com/sharkcz/collectl/4.3.20.3/docs/Disks.html`; committed copy `corpus/evidence/sources-r35/S203.src`.

## Hash chain

- Live fetch (`curl -fsSL`, saved `/fast/scratch/hyaku/mori-r35/GateS203/S203.fetched.html`): 8940 bytes, sha256 `c84b28a24ad42b2b523a9b316d7cfb0368e47e2306ee762473c4c00d97681b8e`, 168 lines, CRLF line endings.
- Committed copy extracted at `cedb0ec4` (`git show ...:corpus/evidence/sources-r35/S203.src`): same sha256; `cmp` against the live fetch reports identical bytes.
- Gate line sha256 cell `c84b28a2…7681b8e` matches the real prefix and suffix (`round-35.md:22`). The w1 sweep independently recorded the same full sha256, 8940 bytes, 168 lines (`.ufo/waves/round-35/w1/SrcDmStack.md:81`).

## Quote check (Gate line)

- Quote: `(10) Device mapper disks, while listed in the detail data are` located at `docs/Disks.html:24`.
- Fetched :24 verbatim: `<li>Device mapper disks, while listed in the detail data are <i>NOT</i> included in the summary data to avoid` — the quote is contiguous on :24, exactly 10 words, and contains no `"` or `|`. OK.

## Anchors

Row anchor cell: `docs/Disks.html:13-14,24-25; tag 4.3.20.3` (`SOURCES.md:209`).

- :13-14 state disk summary represents total activity across all disks `enumerated in /proc/diskstats` — this establishes the scope (per-disk I/O totals from /proc/diskstats).
- :24-25 (with :25 `double counting</li>`) state device-mapper disks are not included in the summary data to avoid double counting.
- Anchors exist at the cited lines and say what is cited.

## Rejection reasoning (REJECTED row — reason and flip)

Row teaches: `REJECTED: leaves device-mapper disks out of its summary to avoid double counting but never says the same I/O appears on the underlying device line, and omits md; flip: a primary source stating that a dm or md write is accounted again on its backing device.`

- "leaves device-mapper disks out of its summary to avoid double counting" — verbatim supported by :24-25.
- "never says the same I/O appears on the underlying device line" — verified against all 168 lines: full read plus `grep -iE 'mapper|raid|\bmd\b|double|underlying|backing|stack|count|/proc/diskstats'` finds accounting statements only at :16 (partition skip), :17-23 (filters), :24-25 (dm exclusion). The example output at :53-57 shows `sda` and `dm-0` both reporting 291 writes KBytes — consistent with duplication, but it is unnamed sample output, not a stating sentence. Under the stated-source rule (w1 sweep included 0 of 12 candidates for the same reason, `SrcDmStack.md:31,51,89`), rejection is correct.
- "omits md" — `grep -iE 'raid|lvm|multipath|\<md\>|mdadm|backing|underlying|lower'` on the fetched file: no hits (exit 1).
- Flip statement is the right polarity: it names a sentence (dm or md write accounted again on the backing device) whose presence would indeed flip the verdict.

## Registry hygiene

- `git diff dd76eb79 cedb0ec4f3a4f672804deac388b7191258f01fcd -- corpus/SOURCES.md`: numstat `6 0`, exactly 1 hunk, 0 removed lines — S203 was appended this round; no existing row's cell changed; S182 and S193 untouched. (S201/S202 supersedes checks belong to other seats; not applicable to S203, whose teaches does not open `supersedes` — correct, since rejected rows do not supersede.)
- Row cells consistent: kind `docs`, tier `C` (collectl docs is tertiary for kernel accounting; consistent with the rejected sibling row S204 tiering `A` as kernel code), status `rejected`, opened `2026-10-23`, used-by `—`.

## Minor observation (not gating)

- Recheck cadence `180d` on rejected S203 vs `on-release` on rejected S204 — no stated reason for the difference; cosmetic.

## Tooling

- No installs performed; curl, git, sha256sum already present.

Residual risk: none found in scope. The source genuinely does not state the stacked-accounting sentence; the rejection and its flip are right.

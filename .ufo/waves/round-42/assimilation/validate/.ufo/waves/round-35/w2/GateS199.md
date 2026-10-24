measured 2026-10-23T09:11:50Z

# S199 gate re-open (live)

VERDICT: admit

I agree with the gate's `admit, A` decision on S199. Every row contract check passes live.

## What S199 is

- Row: `corpus/SOURCES.md:205` at cedb0ec4f3a4f672804deac388b7191258f01fcd (fetched via `git -C /home/vgpnk/Projects/shokunin/mori-shokunin show cedb0ec...:corpus/SOURCES.md | grep -n S199`). Columns per header at SOURCES.md:5 (`id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by`): kind `spec`, tier `A`, status `mined`, opened `2026-10-23`, used-by `SCORECARD.md`.
- Gate line: `corpus/lessons/round-35.md:18` at cedb0ec4 (`| S199 | <url> | \`04ea5c9e…7d993\` | … | admit, A (SrcAxes; byte-identical to the fleet \`AXES.md\`) |`).

## Hash chain — live vs copy vs gate vs fleet

- Live fetch: `curl -fsSL https://raw.githubusercontent.com/VeigaPunk/kimi-shokunin/b47dfbe2cd185e33f9aa42a66a9e6c63c9591d5b/skills/shokunin/protocol/AXES.md` → `/fast/scratch/hyaku/mori-r35/GateS199/S199-live.md`; `sha256sum` = `04ea5c9e89c91cef645536ab56863ebb014dce617e7083e54968092968a7d993`; 83 lines, 5160 bytes.
- Committed copy `corpus/evidence/sources-r35/S199.src` at cedb0ec4: same sha256; `cmp` → BYTE-IDENTICAL (scratch `/fast/scratch/hyaku/mori-r35/GateS199/S199-copy.src`).
- Gate line records `04ea5c9e…7d993` (round-35.md:18): matches both.
- Fleet `/home/vgpnk/Projects/shokunin/AXES.md` (fleet path from `.ufo/waves/round-35/w1/SrcAxes.md:11`): sha256 identical; `cmp` → FLEET-BYTE-IDENTICAL. Gate parenthetical holds.
- Wave-1 `w1/SrcAxes.md:9` records `git ls-remote` showing `b47dfbe2…` as upstream HEAD/main; the row's `commit b47dfbe2` matches the URL pin (SOURCES.md:205).

## Quote checks (gate: ≤25 words, contiguous at stated lines, no `"` or `|`)

- Quote 1, 23 words, `AXES.md:62-64`: `Rows enter only through a round that demonstrates the capability running; a capability without a passing demonstration in the round report is pre-claiming`. Lines 62-64 of the live file join to that exact span (62 `…first-working round. Rows enter only through a`, 63 `round that demonstrates the capability running; a capability without a passing`, 64 `demonstration in the round report is pre-claiming and does not enter the table.`). Word count = 23; contiguous across the three lines; no `"` or `|`. The landed anchor `62-64` is correct — the w1 draft said `62-63` (w1/SrcAxes.md:28) but the sentence ends on line 64, so the wider range was a fix, not a regression.
- Quote 2, 9 words, `AXES.md:15` (`:15` in gate line): `Self-assessment quality: gaps named honestly, confidence graded, overreach caught`. Line 15 is `| **calibration** | Self-assessment quality: gaps named honestly, confidence graded, overreach caught | SHONEN.md/SCORECARD entries match observed repo state |`. Verbatim, contiguous on one line, word count = 9, no `"` or `|` (table pipes sit outside the quoted span).

## Anchor check (SOURCES.md:205 cites `AXES.md:15`, `57-64`, `75-83`)

- `:15` is the calibration row inside `## The six axes` (section header at line 7; table rows 11-16). ✓
- `57-64` spans `## Capabilities — the repertoire table` (header line 57, paragraph 59-64, blank line 65). ✓
- `75-83` spans `## SCORECARD.md contract (per child repo)` (header 75, table head 77-78, field rows 79-83; file ends at line 83). ✓

## teaches fidelity (SOURCES.md:205)

teaches: `A capabilities row enters only through a round that demonstrates the capability running, and calibration means SCORECARD and SHONEN entries match observed repo state.`

- Clause 1 restates lines 62-64 (`Rows enter only through a round that demonstrates the capability running`) — exactly what the Capabilities section states. ✓
- Clause 2 tracks line 15's signal column (`SHONEN.md/SCORECARD entries match observed repo state`) — teaches swaps the order to `SCORECARD and SHONEN` but claims nothing beyond that signal. It reads the signal as the operational test of calibration, which is what the line presents. ✓
- Nothing in teaches reaches outside anchors 15, 57-64, 75-83 (no claims drawn from stagnation nudge, learning path, etc.). ✓
- S199 is admitted (not rejected), so the rejection-reason/flip check does not apply. Supersedes checks apply only to S201/S202 — N/A here.

## Append-only

`git -C /home/vgpnk/Projects/shokunin/mori-shokunin diff dd76eb79 cedb0ec4f3a4f672804deac388b7191258f01fcd -- corpus/SOURCES.md | grep -n S199` shows exactly one `+| S199 | …` line and no `-` line — appended after S198, no in-place edit.

## Residual risk / gaps

- Live fetch was re-done by me at measure time; equality of live sha256 with the committed copy and fleet copy makes a fetch-window substitution undetectable — but also harmless, since all three agree on the same bytes.
- teaches clause 2 compresses line 15's *signal* column into a statement of what calibration "means"; the definition column frames calibration as honest self-assessment. Fair reading of the line; noted, not a defect.
- Method note: no LSP server answers these Markdown corpus files; verification is text-level `grep`/`read`/`sha256sum`/`cmp` on pinned blobs and the live fetch.

## Limits observed

- Writes: this report; scratch under `/fast/scratch/hyaku/mori-r35/GateS199/` (`S199-live.md`, `S199-copy.src`, `SOURCES-at-rev.md`, `round35-at-rev.md`). `df -h /fast` checked: 80% used, 166G free.
- No git writes; only `git show`/`git diff` read-only in the lane. No installs or tool updates performed.

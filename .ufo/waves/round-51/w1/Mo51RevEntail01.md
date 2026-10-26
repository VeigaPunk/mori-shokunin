# Mo51RevEntail01 — mori round 51 w1 — entailment votes, C2 claim rows 1–3

- Seat: Mo51RevEntail01 (reviewer; ENTAILMENT item; leaf — no subagents, no tool installs, no pacman).
- Judged revision: `87e0c374537557754bf71dd68036ded3ddc6699c` (`git rev-parse <rev>^{commit}` returned the same hash, exit 0).
- Item: rows 1–3 of the `## Claims` table of `corpus/knowledge/memavailable-estimate-r51.md` (entry lines 22, 23, 24). All three rows cite S492 = the committed copy `corpus/evidence/sources-r51/proc.rst.v7.2`.
- Row hashes were recomputed from the committed entry cells (sha256 of the whitespace-collapsed claim text, first 12 hex) and all three match `.ufo/waves/round-51/evidence/c2-hashes-at-data.txt`.

## Setup and provenance checks (all exit 0)

- Scratch per operator directive: `/fast/scratch/hyaku/mori-r51/Mo51RevEntail01` with `TMPDIR=<scratch>/tmp`; removed after this report was written. Disk guard before work: `/fast/scratch/hyaku` at 25 %, 603.5 G free — no ENOSPC. All reads and writes used absolute paths or a scratch cwd; nothing was installed.
- Working tree vs data commit for the judged bytes: `git diff --stat 87e0c374… -- corpus/evidence/sources-r51/ corpus/knowledge/memavailable-estimate-r51.md` printed nothing (empty diff); `git status --porcelain corpus/evidence/sources-r51/` printed 0 lines. The judged bytes are the data-commit bytes.
- All five committed source copies were extracted with `git show 87e0c374…:corpus/evidence/sources-r51/<name>` into scratch; sha256 of all five match the hashes recorded on the entry's `recheck:` line (proc.rst `e760f716…`, show_mem.c `dba76b26…`, meminfo.c `d6c58074…`, mm_inline.h `2d4accbb…`, patch `9f571a04…`).
- Quote location: each of the three quotes below occurs exactly once in the committed `proc.rst.v7.2` copy under whitespace collapsing (count over the whitespace-collapsed file).

## Row 1 — verdict: entailed

- Claim (entry line 22), hash `2d0daa4192f1`: "The proc documentation defines MemAvailable as an estimate for starting new applications, not as a count of free pages."
- Quote located at `proc.rst.v7.2:1127-1128`: `An estimate of how much memory is available for starting new applications, without swapping.`
- Context read (lines 1108–1140; decisive lines 1121–1130): the doc defines `MemTotal` ("Total usable RAM …", 1121–1123), then `MemFree` ("Total free RAM. On highmem systems, the sum of LowFree+HighFree", 1124–1125), then `MemAvailable` (1126–1130): "An estimate of how much memory is available for starting new applications, without swapping. Calculated from MemFree, SReclaimable, the size of the file LRU lists, and the low watermarks in each zone."
- Judgment: the quoted sentence directly supports the first half (defined as an estimate for starting new applications). "Not as a count of free pages" follows from the definition plus context: the figure is calculated from four inputs of which free memory is only one, and the doc's count of free memory is the separate `MemFree` field defined two lines above. No number, consequence or scope added.

## Row 2 — verdict: entailed

- Claim (entry line 23), hash `eba2b78b47f3`: "The documentation names the inputs of that estimate as free memory, reclaimable slab, the file LRU list sizes and each zone's low watermark."
- Quote located at `proc.rst.v7.2:1128-1130`: `Calculated from MemFree, SReclaimable, the size of the file LRU lists, and the low watermarks in each zone.`
- Context read: the same MemAvailable block (1126–1134); no other input list appears in it.
- Judgment: "Calculated from" names the inputs; the claim's four terms map one-to-one onto the quote's four inputs (free memory ↔ MemFree; reclaimable slab ↔ SReclaimable; the file LRU list sizes ↔ "the size of the file LRU lists"; each zone's low watermark ↔ "the low watermarks in each zone"). The context sentence at 1131–1133 ("not all reclaimable slab will be reclaimable, due to items being in use") confirms SReclaimable is the doc's reclaimable-slab term. Faithful paraphrase; nothing added.

## Row 3 — verdict: entailed

- Claim (entry line 24), hash `ad57d1b66582`: "The documentation itself warns that how much cache and slab is really reclaimable differs between machines, so the figure is a model rather than a measurement."
- Quote located at `proc.rst.v7.2:1133-1134` (spans the line break after "The"): `The impact of those factors will vary from system to system.`
- Context read (1131–1134): "The estimate takes into account that the system needs some page cache to function well, and that not all reclaimable slab will be reclaimable, due to items being in use. The impact of those factors will vary from system to system."
- Judgment: "those factors" are the two holdback effects the preceding sentence names (cache the system needs to function; slab counted reclaimable but in use). The doc's warning that their impact varies from system to system supports the first half as a faithful paraphrase ("how much cache and slab is really reclaimable differs between machines"). The second half ("so the figure is a model rather than a measurement") is the claim's own consequence, not attributed to the doc's wording ("The documentation itself warns that" governs only the first conjunct), and it follows from the quoted definition: an estimate calculated from inputs whose impact varies per system is a modeled figure rather than a direct measurement — the doc's direct count of free RAM is the separately defined `MemFree`. Scope matches ("from system to system" ↔ "between machines"); no number added. This is the weakest of the three rows; see Findings.

## Verdict lines

ENTAIL 2d0daa4192f1 entailed
ENTAIL eba2b78b47f3 entailed
ENTAIL ad57d1b66582 entailed

Exactly one verdict line per assigned row; no replacement lines (no overclaim votes recorded).

## Residual risk and verification gaps

- UNVERIFIED — upstream identity: judgment is against the committed copies; this seat did not refetch the five source URLs, so today's upstream bytes at tag v7.2 were not checked. (The copies' sha256 do match the entry's recorded `recheck:` hashes, so the entry's own record is internally consistent.)
- `count-c2.py` was not run by this seat: it aggregates every w1 report's votes and the wave is still in flight, so a mid-wave reading of `failed=entailment` would not reflect this report.
- Context reading was the assigned ±20 lines around each quote; rows 4–21, SOURCES.md and the other four sources were not audited by this seat.

## Findings

- LOW — `corpus/knowledge/memavailable-estimate-r51.md:24` (claim row 3): the clause "the figure is a model rather than a measurement" is an interpretive gloss; the source's literal words are "An estimate … Calculated from …" and "The impact of those factors will vary from system to system" (`proc.rst.v7.2:1126-1134`). Judged entailed because it follows from quote plus context and is framed as the claim's consequence, not as doc wording. Named so the L1 can tighten the wording if it wants literal-only claims; no overclaim vote was recorded.
- LOW — `corpus/evidence/sources-r51/proc.rst.v7.2:1128`: the row-1 quote ends and the row-2 quote begins on this same line ("… without swapping. Calculated from MemFree,"). Not a defect — each quote is uniquely located under whitespace collapsing — but tooling that cites a single line number per quote will be ambiguous for these two rows.
- No HIGH or MED findings in scope.

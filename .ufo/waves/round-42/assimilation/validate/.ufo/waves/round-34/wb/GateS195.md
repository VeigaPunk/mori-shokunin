measured 2026-10-23T07:43:28Z

# Gate S195 (wave B) — sysstat common.c v12.8.0 (is_device)

Objects: Gate row `/fast/scratch/hyaku/mori-r34/a3-L1/drafts/corpus_lessons_round-34.md:20`; draft registry row
`/fast/scratch/hyaku/mori-r34/a3-L1/drafts/corpus_SOURCES.md:201`; committed copy
`corpus/evidence/sources-r34/S195.src` at `fd2521351c6cef47384aef30afbe1e4db7e6912e`. Verdicts are my own; the
audited report was opened only after the verdict was formed.

## Live fetch vs committed copy

- `date -u`: 2026-10-23T07:41:22Z. `curl -fsSL --max-time 60 https://raw.githubusercontent.com/sysstat/sysstat/v12.8.0/common.c`
  → sha256 `4aa91c92577ac27970c55b3778e0718a575a17cf86b40d3bbb9ed8d4412eac21`, 47807 bytes.
- Committed copy at `fd252135`: sha256 `4aa91c92577ac27970c55b3778e0718a575a17cf86b40d3bbb9ed8d4412eac21`, 47807 bytes;
  `cmp` → byte-identical. Gate sha256 cell matches both.

## Gate quotes re-located (whitespace runs collapsed; scratch copy = committed copy)

- `S195.src:204` (9 words): "The device is assumed to be virtual if no" — contiguous inside collapsed line 204
  (` *\t\t\tThe device is assumed to be virtual if no`); 9 words; no `"`, no `|`. PASS.
- `S195.src:205` (3 words): "/sys/block/<device>/device link exists." — contiguous inside collapsed line 205; 3
  words; no `"`, no `|`. PASS.
- `S195.src:208` (12 words): "TRUE if @name is a device, and FALSE if it's a partition." — contiguous inside
  collapsed line 208; 12 words; no `"`, no `|`. PASS.
- Lesson line 29's reject note verified: the attempt-1 seat's `SRC.src:204-205` "12 words"
  (`.ufo/waves/round-34/w1/SrcSysstatClass.md:21`) collapses to `* The device … exists.` — 14 words spanning two
  ` * ` comment prefixes; not a contiguous match and mislabeled. The split into :204 / :205 single-line quotes is
  correct.

## Draft registry row, cell by cell (draft :201)

- source: `sysstat common.c at v12.8.0 (is_device) — <url>` — URL resolves live today (above); distinct file from
  S190 (`iostat.c`, tip `corpus/SOURCES.md:196`). PASS.
- kind `code`, tier `A`, status `mined`, opened `2026-10-23`, recheck `on-release`. PASS.
- anchor `common.c:197-224; tag v12.8.0`: S195.src:197-210 is the is_device doc comment (both quoted clauses at
  204-205, 208); :211 `int is_device(const char *sysdev, char *name, int allow_virtual)`; :212-224 body, snprintf
  at :220-221 appending `/device` unless `allow_virtual`, `return !(access(syspath, F_OK));` at :223. Cited code
  held. PASS.
- teaches, clause 1 `is_device() returns TRUE for a device and FALSE for a partition` — not `lane rule:`; stated by
  :208 quote above. SUPPORTED.
- teaches, clause 2 `a device is assumed virtual when no /sys/block/<device>/device link exists.` — not
  `lane rule:`; stated by :204-205 (:203 documents `allow_virtual` as "TRUE if virtual devices are also accepted",
  :221 implements the `/device` suffix). SUPPORTED. Precision note: the mechanism is "when allow_virtual is false,
  an inaccessible `/device` link fails the test" — the comment's own wording; no overclaim.
- used-by `SKILL.md`: exists at `fd252135`; `SKILL.md:832` cites S195 ("sysstat also calls a device without a
  `device` link virtual, S195"). Single path — satisfies the M6 census fix. The draft-vs-tip diff shows
  `-… SKILL.md Round34` → `+… SKILL.md`; at `8d56809` the cell read `SKILL.md Round34`, which is not an existing
  path (`git cat-file -e` fails). Correction verified necessary and correct.

## Audit of .ufo/waves/round-34/wa/ReopenS195.md (attempt-2 report)

1. "Row S195 at 8d56809… (line 201)" — agree (`git show 8d56809:corpus/SOURCES.md` line 201 is the S195 row).
2. Two live fetches at 05:38:42Z, sha256 `4aa91c92…eac21`, 47807 bytes each — agree on hash and size (my fetch
   reproduces both); timestamps unverifiable, consistent with the file header `measured 05:38:49Z` [INFERENCE].
3. "Committed copy … byte-identical (`cmp -l | wc -l` = 0)" — agree (my `cmp` at `fd252135` identical).
4. "URL resolved on v12.8.0 tag" — agree.
5. Teaches-cell quote reproduced verbatim — agree (byte-equal to the draft row's teaches cell).
6. Clause 1 SUPPORTED via `S195.src:208` (12 words) — agree; quote contiguous, count exact.
7. Clause 2 SUPPORTED via `S195.src:204-205` "(12 words)" — agree as evidence: the two lines state the clause;
   count is 12 only if the `* ` markers are excluded (whitespace-collapsed it is 14 and non-contiguous — which is
   exactly why the lesson gate row split it; the report used this as clause support, not as a Gate-quote locator).
8. Anchor `common.c:197-224` holds the cited code; body "implements exactly the documented behavior (the access()
   on the dir `/device` path is the 'no … device link exists' test)" — agree (:211 signature, :220-221 suffix,
   :223 access()).
9. Proposed Gate row locators `S195.src:208,204-205`, decision `admit, A, mined` — agree as proposal; the landed
   lesson row split :204-205 into two single-line quotes, which is stricter and correct.
10. "Tooling: no installs/updates performed" — agree [no counter-evidence observed].
11. Gap (not a claim): the report does not check the used-by cell (`SKILL.md Round34` at 8d56809 is not a path);
    caught only by the M6 census fix in the draft. The row content it did check was accurate.
12. `VERDICT: admit` — agree.

AUDIT: agree 11 / disagree 0

## Verdict

The draft Gate row (lesson :20) and draft registry row (:201) are both correct and stricter than the attempt-2
proposal: live URL matches the committed copy byte-for-byte today, all three Gate quotes are contiguous at their
locators with exact word counts and no forbidden characters, every teaches clause is supported by located quotes,
the anchor holds the cited code, and the used-by cell is a single existing path that genuinely cites S195.

VERDICT: admit

No installs or updates performed (curl, sha256sum, date already present). Scratch: `/fast/scratch/hyaku/mori-r34/a3-GateS195/`.

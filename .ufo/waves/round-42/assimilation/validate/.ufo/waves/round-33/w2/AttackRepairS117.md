# AttackRepairS117 — wave-2 falsification of the S117 repair row

Target: `corpus/lessons/round-33.md` §"Round-32 repair" §1, row `| S117 |` (line 59), judged under R-R.
Base row: `git show 7d382043:corpus/SOURCES.md:123` (10 named URLs; teaches cell read verbatim).
Compared with `.ufo/waves/round-33/w1/RepairS117.md`.

## Findings

### F1 — MAJOR: no committed copy of the releases feed; "unsupported on every page the row names" rests on 9/10 pages and is unreproducible from committed evidence

- Attack: `corpus/lessons/round-33.md:59` column 5 claims every cross-release clause is "unsupported on every page the row names". The row names 10 pages (`SOURCES.md@7d382043:123`); only 9 have committed copies: `corpus/evidence/recheck-r32/S117.src` (tags JSON, population) and `recheck-r33/S117-{main,kill}-v1.{7,8,9.0}.src`, `S117-msg-v1.9.0.src`, `S117-README-v1.9.0.src` (verified: `find corpus/evidence -name "*S117*"` lists exactly these 9). The second named URL `https://api.github.com/repos/rfjakob/earlyoom/releases` has **no committed copy anywhere**. `find corpus/evidence -name "*release*"` → no hits.
- The seat report is honest about this gap (`.ufo/waves/round-33/w1/RepairS117.md`: "No tags/releases JSON was fetched for this repair"), but the L1 row and the §1 preamble — "The clauses were re-checked on the pages each row's own source cell names; copies are committed at `corpus/evidence/recheck-r33/` … and … `recheck-r32/`" (`round-33.md:48`) — present the audit as covering every named page. It does not; one of ten pages was never opened in-round.
- Mitigating evidence: I fetched the feed live: `timeout 60 curl -sSL --fail -m 50 https://api.github.com/repos/rfjakob/earlyoom/releases` → 11 release objects (v1.9.0 … v1.2); every `body` field is empty (`python3` print of all tag_name/published_at plus any body line containing avail|mem <=|sigterm|sending|format|wording|print|since → zero body lines). So on the *live* page the claim holds — this is a checkability/provenance defect in the committed record, not a false claim. Severity stays major because R-R support is judged on committed copies and this hole was silently inherited into a column that says "every page the row names".

### F2 — MINOR/MAJOR (disputable classification): the README copy literally prints a space-padded single-digit threshold; "space padding" sits in the unsupported column while identical evidentiary form is accepted as "supported"

- `corpus/evidence/recheck-r33/S117-README-v1.9.0.src:145-146`:
  `sending SIGTERM when mem avail <= 10.00% and swap free <= 10.00%,`
  `        SIGKILL when mem avail <=  5.00% and swap free <=  5.00%`
  Line 146 shows the single-digit `5.00%` space-padded — the same "the copy literally contains the output" evidentiary form by which the `mem avail <=` fprintf literals are admitted as "supported" (column 4) and by which `PRIPCT "%5.2lf%%"` (`msg-v1.9.0.src:10`) is admitted as stating the width-5 field. The seat report (`w1/RepairS117.md`, last audit row) marks padding "unsupported … the quote gives the format string but does not state the padding behavior" — but an example-output line that *is* the padded output is at least as direct a statement as a format string. Under R-R's literalist reading both should fall together; the repair asymmetrically admits the format macro and rejects the demonstrated output. A judge applying the seat's own evidentiary standard consistently could mark "space-padded" **supported on README.md:146** (a page the cell names), which would move it out of column 5. This does not change the verdict (the clause still fails on the population page, and the teaches clause asserts it *because of* the width-5 field — a causal claim no page states), so it is a column-placement/classification defect, not a verdict defect. Recorded as disputable: minor if the judge requires a predicate ("is padded"), major only if example-output literals count as statements — in which case column 4 also omits it.

### F3 — MINOR: the "unsupported" column does not name the teaches clause "while their trailing fields change"

- Base teaches cell (`SOURCES.md@7d382043:123`): "the action and escalation prefixes are stable across v1.7–v1.9.0 **while their trailing fields change**". The seat audit explicitly rows this clause as unsupported-as-comparative (`w1/RepairS117.md` audit table, "Trailing action fields change across tags"). The L1 row (`round-33.md:59` col 5) enumerates "since v1.8", "unchanged in v1.9.0", "never prints" in v1.7, "stable prefixes", "the version line identifies the grammar", "single-digit space padding" — and folds the comparative trailing-fields clause only under the blanket "every cross-release clause". Semantically covered, but the column otherwise enumerates clauses; a literalist judge reading it as the enumeration may count the omission. Minor.

### F4 — MINOR (incompleteness, not falsity): column 4 omits the README example output as support for the v1.8 grammar

- `S117-README-v1.9.0.src:143-146` (under `earlyoom v1.8`) states the same `sending SIGTERM when mem avail <=` output the row credits only to `S117-main-v1.8.src:382-383`. The cell names `v1.9.0/README.md`; the column already says "release-local literals only", so the omission is descriptive, but it under-cites evidence for the v1.8 literal and (per F2) the same block evidences padding. Minor.

## Verified-clean items (checks run; no defect)

**(a) every "supported on another page" pointer** — all locators land on the exact asserted literal, and every cited page is named in `SOURCES.md@7d382043:123`:

- `S117-main-v1.8.src:382-383` → `fprintf(stderr, "sending SIGTERM when mem avail <= " PRIPCT " and swap free <= " PRIPCT ",\n",` ✓
- `S117-main-v1.9.0.src:414-415` → identical literal ✓
- `S117-main-v1.7.src:326-327` → `fprintf(stderr, "sending SIGTERM when mem <= " PRIPCT " and swap <= " PRIPCT ",\n",` ✓
- `S117-kill-v1.7.src:167` → `warn("escalating to SIGKILL after %.1f seconds\n", secs);` :377 → `warn("sending %s to process %d uid %d \"%s\": badness %d, VmRSS %lld MiB\n",` ✓
- `S117-kill-v1.8.src:230` → `escalating to SIGKILL after %.3f seconds` :539 → `sending %s to process … oom_score %d, VmRSS %lld MiB, cmdline` ✓
- `S117-kill-v1.9.0.src:318` → `%.3f` :627 → `oom_score %d, oom_score_adj %d, VmRSS %lld MiB` ✓
- `S117-msg-v1.9.0.src:9-10` → `// printf format for percentages` / `#define PRIPCT "%5.2lf%%"` ✓
- sha256 of all 8 committed r33 copies equal the w1 report's fetch table (e.g. main-v1.9.0 `08656b0b…f9d0e4`, kill-v1.7 `1453cd2a…65af8`) — copies are the fetched pages.

**(b) "unsupported" clauses vs the 9 committed copies** — none stated:

- `grep -c 'mem avail' recheck-r32/S117.src` → 0; population JSON tokens all 0 for `mem|avail|SIGTERM|sending|escalat|%5|pad|version line|grammar|since` (`1\.7` → 3, tag names only).
- `grep -l -i 'unchanged\|same as' S117-*.src` → none; `'stable'` → none; `'since v1\|introduced'` → none (README `Since version 1.6` is notifications only, `:190`; `since version 0.7` dry-run, `:185`-area — different subjects); `'grammar'` → none; `'pad'` → only `IPAddressDeny` (`README:292`); `'never'` hits (`README:320`, `poll_loop` comments) unrelated; `'identif'` → SPDX/comment only.
- README changelog (`:283-330`) for v1.8/v1.8.1/v1.9.0 states `user mem total`/`MemAvailablePercent`, `oom_score_adj` logging, message-rewording test fixes — none states the wording was introduced in v1.8, unchanged in v1.9.0, or that prefixes are stable. v1.7 main.c print is unconditional at `:326` — but R-R bars absence-as-statement, so "never prints" stays unsupported; consistent with the seat's correction paragraph.

**(c) column 3 vs closure + base teaches** — `round-32-verifier-spotcheck.md:89` lists "every factual clause … The page is the tags JSON"; the row's "every factual clause (the population page is the tags JSON)" matches. Base teaches clauses all accounted for: since-v1.8, unchanged-v1.9.0, `mem <=`, never-prints, stable prefixes, trailing-fields (F3), version-line-grammar, width-5→padding.

**(d) forgotten teaches clauses** — none beyond F3's naming omission; seat draft rows 1–8 each map to a base clause and the row's columns cover the same partition (release-local supported vs cross-release unsupported).

## Seat-report comparison

`w1/RepairS117.md` holds up: its clause audit's supported/unsupported split matches the committed bytes at every cited line; its sha256 table reproduces; it explicitly discloses the releases-JSON gap that the L1 row then obscures (F1) and it explicitly enumerates the trailing-fields clause the L1 row drops (F3). Its padding judgment is internally consistent but asymmetric with its own acceptance of format-string/example literals (F2).

## Residual risk

- A judge who requires "states" to mean a predicate sentence will also downgrade `mem avail <=`/`PRIPCT` support to mere display — cutting the other direction; the row's verdict survives either way.
- Live releases feed has empty bodies today; a future freshness claim must still pin it (row §5 already flags it unpinned).

No tools installed; no lane writes outside this report; read-only git (`git show 7d382043`), grep/sed/sha256sum on committed copies, one live curl to the public releases API (permitted ordinary fetch).

# Mo56ExecQuarantine — mori slice of the absent-defect register, re-derived

Seat: Mo56ExecQuarantine (wave w1, round 56). Report-only; the register was not
edited (it lives in `/home/vgpnk/Projects/shokuknow`, which this seat reads
bytes from and runs nothing in). No files outside this report were written.
Scratch `/fast/scratch/hyaku/mori-r56/Mo56ExecQuarantine/` removed at the end.
Tooling installs: none (no package manager run; `curl`, `pdftotext`,
`pdfinfo`, `python3` all already present).

Report: .ufo/waves/round-56/w1/Mo56ExecQuarantine.md

---

## 1. Deriving the slice

Command exactly as dispatched (the register path resolves to
`/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md`):

```
awk -F'|' -v l='mori' '$2 ~ ("`" l "`") && $3 ~ /round[0-9]+/ && $4 ~ /S[0-9]+/ {print $4, $5}' \
  /home/vgpnk/Projects/shokunin/../shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md
```

Output (exit 0), three rows and no fourth:

```
 S244`   the cited source could not be fetched, so no quote was checked
 S262`   the cited source could not be fetched, so no quote was checked
 S268`   the cited source could not be fetched, so no quote was checked
```

The three mori rows are those three — and all three sit in the register's
**second** table, `## Rows whose quotes were NEVER CHECKED` (register lines
356-358), not in the `## Rows` table.

Structural facts about the slice, measured rather than assumed:

- mori rows in the `## Rows` (payload-absent / "fabrication class") table:
  **0**. Counted with `grep -c '^| `mori`'` scoped to each table by line
  number — mori appears only at lines 356, 357, 358, all past the
  `## Rows whose quotes were NEVER CHECKED` heading (line 256).
- mori in the `## By lane` table: **absent entirely** (0 matches in lines
  234-255). That table sums to 194 and covers only the payload-absent table.
- Census backing the register (`quote-lint-full-v5.json`), mori findings by
  verdict: `sweep-found` 93, `folded` 135, `fetch-failed` 3, **ABSENT 0**.
  So the mori lane contributes no payload-absent row and no ABSENT quote.
- The register is reproducible from that census:
  `python3 absent-defect-register.py --census quote-lint-full-v5.json --out <scratch>`
  exits 0 and the result is **byte-identical** to the shipped file
  (`diff` exit 0). Header totals re-derived: 194 payload-absent rows, 324
  ABSENT quotes, 109 never-checked rows, `## By lane` sum 194.

So the register's own class for the mori slice is the one its legend defines as
`unreachable`: *the source could not be fetched, so the quote was never
checked* — the class that explicitly must **not** be read as fabrication.

## 2. Row-by-row verdicts

Each register row carries no quote column of its own (the never-checked table
has none). The quote to test is therefore the one the row's gate block names;
I took it from the lane's own staged `SOURCES-PROPOSED.md` at the census
commit `9e91e504` (exported read-only with `git archive`, extracted into
scratch) and matched it against freshly fetched bytes. The identity of each
census id to the lane's current staged/merged row was confirmed by **content**,
not by arithmetic:

| register row | lane row at census commit | same row after packaging renumber | quote source |
|---|---|---|---|
| mori round1 `S244` | `lanes/mori/SOURCES-PROPOSED.md` S244 = Rationale Dataset paper | staged `S483` | gate block S244 |
| mori round4 `S262` | `lanes/mori/round4/SOURCES-PROPOSED.md` S262 = ROMA abstract | staged `S501` | gate block S262 |
| mori round5 `S268` | `lanes/mori/round5/SOURCES-PROPOSED.md` S268 = ROMA full text | staged `S507` | gate block S268 |

### S244 — verdict PRESENT

Cited source `https://doi.org/10.1145/3643916.3644413` (ACM). Gate block's own
locator `https://arxiv.org/abs/2403.18832`. Quote tested, `exact` fold:
`We find that 98.9% of commits in our dataset contain sentences with rationale information`

Evidence, all fresh today (2026-10-27), read-only:

```
$ curl -sS -L -o /dev/null -w 'http=%{http_code} url=%{url_effective} size=%{size_download}\n' \
    --max-time 45 'https://doi.org/10.1145/3643916.3644413'
http=403 url=https://dl.acm.org/doi/10.1145/3643916.3644413 size=5471      exit 0
  body: a Cloudflare interstitial, not the article
$ curl -fsSL --compressed --max-time 15 -A '<census UA, Chrome/124>' -o /dev/null -w ... <same DOI>
curl: (22) The requested URL returned error: 403     exit 22
  -> this is the census's own fetch shape, and it fails the same way

$ curl -sS -L --max-time 45 'https://arxiv.org/abs/2403.18832' -o arxiv.html -w 'http=%{http_code} size=%{size_download}\n'
http=200 size=41919                                                       exit 0
$ grep -c '98.9% of commits in our dataset contain sentences with rationale information' arxiv.html
3
$ grep -o 'citation_doi" content="[^"]*"' arxiv.html
citation_doi" content="10.1145/3643916.3644413"
$ grep -o 'citation_title" content="[^"]*"' arxiv.html
citation_title" content="Rationale Dataset and Analysis for the Commit Messages of the Linux Kernel Out-of-Memory Killer"

$ curl -sS -L --max-time 60 -A '<browser UA>' 'https://arxiv.org/pdf/2403.18832' -o arxiv.pdf -w 'http=%{http_code} size=%{size_download}\n'
http=200 size=1420568                                                    exit 0
$ sha256sum arxiv.pdf
ab8ab19551fb3614307b818e48b49885eca6f8af933b9eddfde8a18e6bf6018e
$ pdftotext arxiv.pdf arxiv.txt; wc -l arxiv.txt
1437
$ grep -c '98.9%' arxiv.txt
3
```

Verdict: **PRESENT**. The span is verbatim in the row's own declared carrier,
and the carrier's `citation_doi` is the cited DOI, so the DOI and the preprint
are the same work. The cited ACM endpoint itself is unreadable from this host
(403, Cloudflare), which is exactly what the register records — but that is a
publisher-wall fact, not an absent-quote fact. Matches the round-48 lesson's
S244 verdict (PRESENT).

### S262 — verdict PRESENT

Cited source and gate locator are the same DOI,
`https://doi.org/10.1109/TSC.2026.3698682`. Quote tested, `whitespace`/`exact`:
`Our study shows that Linux cgroups and the default Out-of-Memory (OOM) mechanism lack sufficient container context when selecting victim processes.`

```
$ curl -sS -L -o /dev/null -w 'http=%{http_code} size=%{size_download}\n' --max-time 45 \
    'https://doi.org/10.1109/TSC.2026.3698682'
http=202 size=0          (final url ieeexplore.ieee.org/document/11540439/)
  -> 202 with a zero-byte body: the IEEE bot wall, not a document
$ curl -fsSL --compressed --max-time 15 -A '<census UA>' -o /dev/null -w ... <same DOI>
http=202 size=0          exit 0
  -> curl -f succeeds, but size 0 makes the census's `not raw.stat().st_size` guard fail it
```

Two carriers that do serve it, both fetched today:

```
$ curl -sS -L --max-time 45 'https://api.openalex.org/works?filter=doi:10.1109/tsc.2026.3698682' -o oa.json -w 'http=%{http_code} size=%{size_download}\n'
http=200 size=70770                                                       exit 0
  title: ROMA: Enhancing Container OOM Resilience via Reinforced Isolation and Adaptive Shared Resource Reclamation
  open_access: {'is_oa': True, 'oa_status': 'hybrid', ...}
  abstract reconstructed from abstract_inverted_index -> contains the quote exactly: True

$ curl -sS -L --max-time 90 -A '<browser UA>' \
    'http://xplorestaging.ieee.org/ielx8/4629386/11644734/11540439.pdf?arnumber=11540439' \
    -o roma.pdf -w 'http=%{http_code} size=%{size_download} type=%{content_type}\n'
http=200 size=2357114 type=application/pdf                                exit 0
$ sha256sum roma.pdf
1603404dd25b3a0dff93f2dcb23c75b671d4e2d78da3cce8f461e87ebde6add2
$ pdftotext -enc UTF-8 roma.pdf roma.txt; wc -l roma.txt
1405
  quote present in the deposited VOR PDF: True   (abstract paragraph)
```

The lane's own held copy reconstructs the same abstract:

```
$ python3 -c "... reconstruct corpus/evidence/sources-r42/S262.oa.json ..."
keys: id, doi, title, ..., abstract_inverted_index? (present)
reconstructed abstract len 1456
span present in lane-held copy: True
  raw JSON text search for the contiguous sentence -> False (inverted index, as expected)
```

Route limitation recorded honestly: the Semantic Scholar API (the round-4 gate's
named extraction route) returned **HTTP 429** on both attempts today
(`{"message": "Too Many Requests...", "code": 429}`), so that route is
UNVERIFIED — but it is one route, and two others carry the quote.

Verdict: **PRESENT**.

### S268 — verdict PRESENT

Same DOI. Quote tested:
`It leverages eBPF to hook into OOM-related kernel tracepoints such as mark_victim, start_task_reaping, and finish_task_reaping`

The cited DOI again returns 202/0 bytes. The gate block names the deposited VOR
PDF, and that PDF is the carrier I fetched above. Byte-level confirmation:

```
$ pdfinfo roma.pdf | head -2
Title:  ROMA: Enhancing Container OOM Resilience ...
Subject: IEEE Transactions on Services Computing;2026;19;4;10.1109/TSC.2026.3698682
$ cmp -s <scratch>/roma.pdf /home/vgpnk/Projects/shokuknow/lanes/mori/round5/.deepresearch/notes/roma.pdf
BYTE-IDENTICAL to lane-held copy     (sha256 1603404d…, 2 357 114 B)
$ sha256sum /home/vgpnk/Projects/shokuknow/lanes/mori/round5/.deepresearch/notes/roma.pdf
1603404dd25b3a0dff93f2dcb23c75b671d4e2d78da3cce8f461e87ebde6add2
$ grep -n 'mark_victim' <scratch>/roma.txt
140:as mark_victim, start_task_reaping, and finish_task_reaping to record OOM-triggering process
  the sentence spans text lines 139-141 (line 139: "cleanup to within the correct container boundary. It leverages eBPF ...")
```

Run through the census's own `match()` against that text, so the check uses the
grader's own folds rather than mine:

```
It leverages eBPF to hook into OOM-related kernel tracepoints such as mark_victim, start_task_reaping, and finish_task_reaping  -> whitespace
they rely solely on per-process memory usage, lacking awareness of container context                                            -> whitespace
These hooks are installed via standard LSM points and require no kernel patching or reboot.                                     -> whitespace
Under eight concurrent attackers, benign throughput retention remains 92.6% with ROMA, compared with 82.4% for                  -> exact
ROMA incurs only a 6.94% throughput overhead across eight workloads.                                                            -> whitespace
```

Verdict: **PRESENT**. Note the register's S268 row carried no quote at all
(the never-checked table has no quote column); the quote located is the one the
row's gate block names, which is the renumbered staged `S507`'s.

## 3. Summary of verdicts

| register row | class as shipped | verdict after re-fetch | cited source reachable? | quote carrier |
|---|---|---|---|---|
| mori round1 `S244` | unreachable (never checked) | **PRESENT** | no — 403 Cloudflare at the ACM DOI | arXiv abs + arXiv PDF, `citation_doi` = the cited DOI |
| mori round4 `S262` | unreachable (never checked) | **PRESENT** | no — 202 / 0 bytes at the IEEE DOI | OpenAlex record; deposited VOR PDF; lane-held `S262.oa.json` |
| mori round5 `S268` | unreachable (never checked) | **PRESENT** | no — 202 / 0 bytes at the IEEE DOI | deposited VOR PDF, sha256 `1603404d…`, byte-identical to the lane's copy |

No mori row is `payload-absent`. Nothing in this slice supports calling any mori
quote a fabrication. This independently reproduces the round-48 lesson's
three-way PRESENT (and confirms PRESENT for S268, which the round-45 lesson had
recorded as `unverifiable`; the difference is the deposited-PDF route being
reachable with a browser User-Agent, which it is again today).

## 4. Why the census recorded these three as never-checked

This is the part that is new, and it is an instrument finding rather than a
corpus finding. I reproduced the census's own decision path for the three rows
with the census's own functions (`quote-lint.py` imported read-only) against the
lane snapshot at census commit `9e91e504`.

For all three rows, the census's `block_url()` returned the **DOI**, and the DOI
is what fails:

```
--- round1 S244
  row source first URL : https://doi.org/10.1145/3643916.3644413
  gate 'URL:' line raw : https://arxiv.org/abs/2403.18832
  block_url() used     : https://doi.org/10.1145/3643916.3644413
  gate != used ?       : True
--- round4 S262
  gate 'URL:' line raw : https://doi.org/10.1109/TSC.2026.3698682
  block_url() used     : https://doi.org/10.1109/TSC.2026.3698682
  gate != used ?       : False
--- round5 S268
  gate 'URL:' line raw : https://doi.org/10.1109/TSC.2026.3698682
  block_url() used     : https://doi.org/10.1109/TSC.2026.3698682
  gate != used ?       : False
```

Cause A, and the sharpest one — for S244 the census had **already downloaded and
cached the very document that contains the quote**, and never looked at it:

```
prefetch collects from gate body: ['https://arxiv.org/abs/2403.18832']
fetch(arxiv) -> OK 5571 chars
block_url() picks        : https://doi.org/10.1145/3643916.3644413
cached_text(used)        : None (fetch failed)
match(cached arxiv doc)  : exact
```

So a span that matches under the **`exact` fold** was reported `fetch-failed`.
The prefetch stage adds gate-body URLs to the fetch set
(`quote-lint.py:738-741`), but the match stage consults only `block_url()`'s URL
plus `companion_urls(url, row)` (`quote-lint.py:774`, `:826-856`, `:884`), and
`companion_urls()` derives candidates from the **row's `source` cell** only —
sibling files of the same repository and the J-STAGE `_pdf/` variant. For these
three rows it returns nothing:

```
--- round1 S244   companions: []
--- round4 S262   companions: []
--- round5 S268   companions: []
```

Cause B — why `block_url()` did not use the gate block's own locator in the two
rows where it differs. `URL_LINE_RE` (`quote-lint.py:66`) is
`^\s*[-*]?\s*(?:URL|url|Source|Locator)\s*[:=]\s*(\S+)` compiled with flags 34
(`re.I | re.U`) — **no `re.M`**. Two independent consequences, both measured:

```
URL_LINE_RE flags include MULTILINE? False
bold form, body start  -> None            (`- **URL:** https://…`)
plain form, body start -> https://arxiv.org/abs/2403.18832
plain form, line 3     -> None            (no re.M, so `^` anchors at string start only)
```

The lane writes the bold form `- **URL:** <url>`. Across mori's staged files,
136 lines are URL-ish; `URL_LINE_RE` matches 95, and the 41 it does not match
are exactly the `**URL` label form. Of the 37 gate bodies whose bold line is
parsable at all, `block_url()` disagrees with the gate's own locator on 5 rows:

```
mori   S244  gate=https://arxiv.org/abs/2403.18832                     used=https://doi.org/10.1145/3643916.3644413
round2 S253  gate=https://arxiv.org/abs/2602.09345                     used=https://doi.org/10.48550/arXiv.2602.09345
round5 S269  gate=/home/vgpnk/.../standing-sampler-summary.txt         used=None
round5 S271  gate=/home/vgpnk/Projects/.../sweep-comparison.txt        used=None
round5 S272  gate=/home/vgpnk/Projects/.../cgroup-cotency.txt          used=None
```

Only S244 landed in the register. The other four were still reached, by
different paths, and their census verdicts show it — all four are
`sweep-found`, none is `fetch-failed`: S253's fallback URL (the arXiv DOI
mirror) resolves, and for S269/S271/S272 `block_url()` returned `None`, which
sends the code down the `local_locator` branch rather than to a web fetch. Had
the fallback in any of those five been unreachable instead of reachable, each
would have become another never-checked register row. So the bug's blast radius
on this register is small but real, and its failure mode is the bad one: a false
`fetch-failed` produced when a quoted span is available in a carrier the census
itself already fetched.

Cause C — for S262/S268 the DOI *is* the gate locator, so the locator bug is not
the cause there. The cause is that both the DOI endpoint and the row's source
cell name only the DOI, while the deposited PDF lives in the gate body's prose,
and the match stage never consults gate-body URLs.

Net effect on the register: the `fetch-failed` / "never checked" class
**under-reports verification**. It is honest about what the census did — the
legend says "no quote was checked", not "no quote exists" — but a later round
reading those 109 rows as unreachable inherits a list that contains rows whose
quote matches `exact` in bytes the census itself downloaded.

## 5. Register-level observations (not mori-specific)

- **Markdown defect.** `absent-defect-register.py:160` writes the never-checked
  row's id cell as `` {r['id']}` `` — a trailing backtick with no opening
  backtick. The shipped cell is literally `` | S244` | ``, so the id renders
  wrong and any downstream parser sees `S244\`` rather than `S244` (my
  dispatched `awk` extraction reproduces exactly that artefact). The
  payload-absent table at `:143` does not have this bug.
- **The never-checked rows are outside the headline counts.** The `## Totals`
  block reports 194 rows / 324 quotes; the 109 never-checked rows are counted
  only inside their own section, and `## By lane` sums to 194 with no mori
  entry. A lane-level reader therefore sees **zero** mori rows in this register
  even though the lane has three flagged rows. The round-45 lesson already
  described this reading; the artefact still presents it this way.
- **The generator cannot be run with its defaults.** `absent-defect-register.py`
  defaults `--census` to `quote-lint-full-v3.json`, which does not exist in that
  directory (only `quote-lint-full.json`, `-v4`, `-v5`):
  `python3 absent-defect-register.py --out <path>` → `FileNotFoundError: … quote-lint-full-v3.json`, exit 1. With `--census quote-lint-full-v5.json` it runs and reproduces the shipped file byte-for-byte, so the artefact is reproducible — but only with a flag the header text does not state as required.

## Findings

- **HIGH — false `fetch-failed` hides an `exact` match.** `quote-lint.py:774`
  (`block_url`), `:822-856` (`companion_docs` / `companion_urls`), `:738-741`
  (prefetch). For mori round1 `S244`, the gate-body URL
  `https://arxiv.org/abs/2403.18832` was prefetched successfully (200, 41919 B)
  and its cached text matches the row's quote under the `exact` fold, yet the
  row was recorded `fetch-failed` because the match stage followed
  `block_url()`'s DOI instead. Reproduced with the census's own functions:
  `fetch(arxiv) -> OK 5571 chars`, `match(cached arxiv doc) -> exact`,
  `cached_text(DOI) -> None`. Consequence: the register's 109-row
  "never checked" class contains at least one row that was in fact checked-ready.
- **HIGH — the same defect is systemic in the locator parser.**
  `quote-lint.py:66` compiles `URL_LINE_RE` without `re.M` and cannot parse the
  corpus's own `- **URL:**` bold label form; 41 of mori's 136 URL lines are that
  form and are not matched. Measured divergence between the gate block's stated
  locator and the URL actually used: 5 of 37 parsable mori gate bodies
  (`mori S244`, `round2 S253`, `round5 S269`, `round5 S271`, `round5 S272`).
  The row identifier is not the defect; the locator resolution is.
- **MED — the register's `By lane` table omits the never-checked class
  entirely.** `absent-defect-register.md` lines 234-255 sum to 194 and contain
  no `mori` entry, while lines 356-358 hold the lane's three rows. Lane-level
  readers of this artefact get a zero count for mori.
- **MED — the register generator's default census argument points at a missing
  file.** `absent-defect-register.py:49`
  (`default=str(HERE / "quote-lint-full-v3.json")`); that file is not in
  `.ufo/waves/corpus-expansion-1/`. Running with defaults exits 1
  (`FileNotFoundError`). Reproducing the shipped artefact requires the
  undocumented `--census quote-lint-full-v5.json`, which then matches
  byte-for-byte.
- **LOW — malformed id cell in the never-checked table.**
  `absent-defect-register.py:160` emits `{r['id']}` + a stray backtick, so the
  shipped cell reads `` | S244` | `` and the id is not cleanly parseable. Line
  143 (payload-absent table) is correct.
- **LOW — one extraction route is rate-limited today, not dead.**
  `https://api.semanticscholar.org/graph/v1/paper/DOI:10.1109/TSC.2026.3698682`
  returned HTTP 429 on two attempts (2026-10-27), the route the round-4 gate
  names for S262. Recorded as UNVERIFIED for that route only; two other
  carriers hold the quote.

## Limits of this seat

- Not an independent judge: dispatched inside the same wave as the claims it
  touches, and this report asserts nothing about C1/C2 or the round-56 counters.
- Verdicts are for the **mori slice only** (3 rows). The other 106
  never-checked rows and the 194 payload-absent rows were not re-fetched.
- The register was read, never written; `shokuknow` bytes were read and nothing
  was executed there.
- Every fetch above is a public read. Nothing was written to `/sys`, `/proc`, a
  cgroup, the fleet log, or any lane's git/jj state.

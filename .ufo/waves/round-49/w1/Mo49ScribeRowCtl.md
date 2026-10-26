# Mo49ScribeRowCtl — lane SOURCES.md row S486 for journalctl(1)

Seat: mori round 49, wave w1. Bounds observed: leaf seat, no subagents, no questions, no mutations of
lane files (this report is the only lane file written). Author date 2026-10-25 (local `-03:00`).
Frozen contract read first: `.ufo/waves/round-49/contract.md` (freeze `0df17b7b`, entering tip
`b3e3453d`). Every command below ran with cwd `/home/vgpnk/Projects/shokunin/mori-shokunin` unless a
`cd` is shown, and with `TMPDIR=/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r49-Mo49ScribeRowCtl`.
No tool was installed or upgraded (pacman untouched); no `sudo` used; no host service touched; no
credential, session id or private URL appears here.

## Behavior

Drafted, but did **not** integrate, registry row **S486** for
`journalctl(1)` at `https://www.freedesktop.org/software/systemd/man/latest/journalctl.html`, as a NEW
row whose `teaches` opens `supersedes S351 —`. The row is scoped to the three vacuum switches and their
archived-file-only target, so its scope string differs from S351's
(`the archived-journal store's own size ceiling and reach; refused as an admitted source this round`)
and from S470's (`what journalctl --disk-usage counts: …`). It carries 11 columns, no `|` inside any
cell, `status` `mined`, `opened` `2026-10-25`, `recheck` `180d`, `used-by`
`corpus/knowledge/journal-reach-r49.md`, and it is grounded in the frozen copy
`corpus/evidence/sources-r49/journalctl.1.html` (sha256 `75440570…`, byte-identical to a live fetch on
2026-10-25). With this row the fleet census gains exactly one `W04` warning line and no `E04`, no `E11`
and no other finding — shown by A/B diff, not asserted (evidence item 8).

S351 needs **no in-place cell edit** (argument and drafted note text below): under `CORPUS.md` Rule 2 a
correction is a new row, and S351's `rejected` verdict records why the earlier attempt was refused.

## Commands and observed evidence

1. **Frozen instruments and copy digests.** `ls corpus/evidence/sources-r49/ && sha256sum corpus/evidence/sources-r49/*`
   → four copies; journalctl copy `75440570fb1f71859229ca88fed0a6764b2057c7dd90651701b3d022a5649722`,
   equal to `COPIES[...journalctl.html]` in `.ufo/waves/round-49/count-c2.py:42` and to
   `evidence/freeze-sha256.txt`. `wc -c journalctl.1.html` → `87375`.

2. **Live re-open of the canonical URL** (the round's "opened" act; scratch only, exit 0):
   `curl -sS -D live-headers.txt -A 'Mozilla/5.0 (X11; Linux x86_64) … Chrome/141.0.0.0 Safari/537.36' -o live-journalctl.1.html https://www.freedesktop.org/software/systemd/man/latest/journalctl.html; echo "curl_exit=$?"`
   → `curl_exit=0`. `sha256sum live-journalctl.1.html` →
   `75440570fb1f71859229ca88fed0a6764b2057c7dd90651701b3d022a5649722` (**byte-identical to the frozen
   copy**). Headers: `HTTP/1.1 200 OK`, `Date: Mon, 26 Oct 2026 00:44:12 GMT`,
   `Last-Modified: Tue, 22 Sep 2026 13:31:34 GMT`, `ETag: "1554f-65c1262a14f2e"`,
   `Content-Length: 87375`, `Content-Type: text/html`. Local clock at fetch
   `2026-10-25T21:44:13-03:00`. `grep -o 'systemd [0-9][0-9][0-9]' journalctl.1.html | sort | uniq -c`
   → one hit `systemd 262`; the page prints no commit or "last updated" string.

3. **Anchor and located quotes inside the frozen copy** (line numbers of the committed copy):
   `grep -n 'id="--vacuum-size="\|Note that running\|vacuuming operation\|Specifying any of these\|may also be combined'`
   → `dt id="--vacuum-size="` at 290; the three switch entries at 290-299; note paragraph 299-303;
   combination and zero rule 303-307 (`Specifying any of these` at 305); `--rotate` combination
   307-311. Primary quote (13 words) at 299-300, second located span (9 words) at 301.

4. **Quote location under the counter's own normalisation** (script/style/comment dropped, tags
   stripped, entities decoded, whitespace collapsed — `.ufo/waves/round-49/count-c2.py:59-64`,
   replicated verbatim in the scratch check). Results, exit 0:

   | span | words | occurs in normalised copy |
   |---|---|---|
   | `running --vacuum-size= has only an indirect effect on the output shown by --disk-usage` | 13 | yes |
   | `the vacuuming operation only operates on archived journal files` | 9 | yes |
   | `Specifying any of these three parameters as zero is equivalent to not enforcing the specific limit` | 16 | yes |
   | `removes the oldest archived journal files until the disk space they use falls below the specified size` | 17 | yes |
   | `has only an indirect effect on the output shown by --disk-usage, as the latter includes active journal files` | 18 | **no** |

   The last row is the trap in a finding: the copy renders `--disk-usage` as a `<code>` element followed
   by a literal `,`, so tag→space collapse yields `--disk-usage ,`; a naturally punctuated quote that
   joins the comma fails the counter. The drafted Gate quote stops before the comma.

5. **Row shape.** `awk -F'|' '{print "NF=" NF}' row-s486.txt` → `NF=13` (11 cells + edge pipes);
   cell count 11; `"\\|" in row` → `False`; cells 8-11 read `mined` / `2026-10-25` / `180d` /
   `corpus/knowledge/journal-reach-r49.md`. Lane table census at the time of drafting:
   `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` → `257`;
   malformed-row awk → `malformed=0`. The registry's last row is `| S484 |` at `corpus/SOURCES.md:263`;
   the insertion point is immediately after line 263, before the blank line and `## Paths` at 265.

6. **The frozen counter's own row predicate, replayed on the row** (no import of the frozen file, no
   `__pycache__` written; `split_cells`/`sources_row` re-implemented exactly as `count-c2.py:49-56,92-96`):
   `len(srow)` → `11`; journalctl URL found in `srow[1]` → `True`; `srow[7]` → `mined`;
   `srow[8]` → `2026-10-25`; `used-by` split on `[,;]` → `['corpus/knowledge/journal-reach-r49.md']`;
   composite `row_ok` as `count-c2.py:160-162` computes it → `True`. This proves the row satisfies
   P-C2's source-row arm; it does not prove C2.

7. **Lane census, read-only, today** (baseline, before integration):
   `TMPDIR=… bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori`
   → 20 `W04` lines + `mori ok /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md`, exit 0.
   `diff` of that stdout against `.ufo/waves/round-49/evidence/census-start.txt` → empty ("validate
   output identical to census-start.txt"). `git status --short corpus/SOURCES.md` → empty; last commit
   touching it `e4dfff32`.

8. **Full-registry A/B on copies** (both under scratch; both include a placeholder
   `corpus/knowledge/journal-reach-r49.md` so the only variable is the S486 row):
   base = 257-row copy; aug = same file with the drafted row inserted after the S484 line.
   `sources-census.sh validate --file <copy>/corpus/SOURCES.md --today 2026-10-25`:
   base exit 1 / 313 lines, aug exit 1 / 314 lines (both exit 1 only from the 292 `E11` findings that a
   scratch copy necessarily produces for other rows' `used-by` paths). `difflib` diff base→aug:

   ```
   @@ -20,0 +21 @@
   +file	W04	S486 duplicate url www.freedesktop.org/software/systemd/man/latest/journalctl.html across scopes
   ```

   `E04` lines in aug: `[]`. Code histograms: base `{'E11': 292, 'W04': 20}`, aug
   `{'E11': 292, 'W04': 21}`. So the drafted row adds exactly one `W04` warning and nothing else.

9. **Fixture matrix for the census rule** (isolated three-row registries: S351 verbatim, S470 verbatim,
   plus one S486 variant; `validate --file … --today 2026-10-25`). Findings per fixture:

   | fixture | S486 scope | S486 `teaches` / status | S486 lines observed |
   |---|---|---|---|
   | A | drafted, distinct | `supersedes S351 —`, mined | `W04 … across scopes` only |
   | B | S351's verbatim | `supersedes S351 —`, mined | none (no W04, no E04) |
   | C | S470's verbatim | `supersedes S351 —`, mined | none |
   | D | S470's verbatim | supersedes prefix removed, mined | `E04 … within scope <S470 scope>` |
   | E | drafted, distinct | supersedes prefix removed, mined | `W04` only |
   | F | S470's verbatim | supersedes removed, status `rejected` | none |
   | G | S470's verbatim | no supersedes, mined | `E04` |
   | H | S470's + trailing spaces | no supersedes, mined | `E04` (cell trimmed before keying) |
   | I | S470's with one internal double space | no supersedes, mined | `W04` only — **no E04** |
   | J | S470's with leading/trailing spaces | no supersedes, mined | `E04` |

   Fixtures A-F also printed an unrelated `E11 S470` (their S470 row reuses the lane's `used-by` path,
   absent in scratch); G-J printed `E11 S486` because those fixtures deliberately carried no entry
   placeholder. Both are fixture artefacts, not row defects.

## Draft — `corpus/SOURCES.md` row S486 (insert immediately after line 263, inside the registry table)

```markdown
| S486 | journalctl(1) vacuum switches — https://www.freedesktop.org/software/systemd/man/latest/journalctl.html | docs | A | the three vacuum switches of journalctl(1) only — what --vacuum-size=, --vacuum-time= and --vacuum-files= remove from the archived store, that they cannot remove active files, how the three combine into one size, time and file-count limit, the documented zero rule, and why vacuuming moves --disk-usage only indirectly; not the --disk-usage reading itself (S470), not cursor and field selection (S014), not the S351 refusal | Commands section, dt id "--vacuum-size=" entry group for --vacuum-size=, --vacuum-time= and --vacuum-files=; committed copy corpus/evidence/sources-r49/journalctl.1.html lines 290-311, note paragraph 299-303, combination and zero rule 303-307, --rotate combination 307-311; page header systemd 262; copy sha256 75440570fb1f71859229ca88fed0a6764b2057c7dd90651701b3d022a5649722; opened 2026-10-25 | supersedes S351 — journalctl's vacuum switches act on archived journal files only: --vacuum-size= removes the oldest archived journal files until the disk space they use falls below the specified size, --vacuum-files= leaves only the specified number of separate files and does not remove active ones, the three may be combined in a single invocation to enforce any combination of a size, a time and a number of files limit, and a zero parameter means that limit is not enforced; the page also states running --vacuum-size= has only an indirect effect on the output shown by --disk-usage because that reading includes active files, with the single exception that a combined --rotate archives the active files first. S351's flip is met by these located sentences plus the round's committed read-only host receipt and no MESSAGE grep. | mined | 2026-10-25 | 180d | corpus/knowledge/journal-reach-r49.md |
```

Draft row digest (for the L1 to detect drift after pasting): sha256 of the line plus newline
`bfc4e48ffe661c0e7ebabab3de6a70fdca63a86ae1dbd26e0d1cf0c8e7db3145`.

**Id uniqueness across the wave's draft pool** (read-only check, 21:47, `head -3` + id grep on the three
sibling reports): `Mo49ScribeRowConf.md` → S485 `journald.conf(5)`; `Mo49ScribeRowSvc.md` → S487
`systemd-journald.service(8)`; `Mo49ScribeRowHost.md` → S488 own-work host receipt. No sibling claims
S486, so no `E03` duplicate id is pending from this wave. `teaches` deliberately names no receipt id; if
the L1 keeps this mapping, appending `(S488)` after "host receipt" is a one-token improvement, not a
requirement of P-C2.

## Draft — lesson `## Gate` line (round 49, "rows opened 2026-10-25")

```markdown
| S486 | https://www.freedesktop.org/software/systemd/man/latest/journalctl.html (committed copy `corpus/evidence/sources-r49/journalctl.1.html` sha256 `75440570fb1f71859229ca88fed0a6764b2057c7dd90651701b3d022a5649722`, byte-identical to a 2026-10-25 live fetch; page header `systemd 262`) | 2026-10-25 | "running --vacuum-size= has only an indirect effect on the output shown by --disk-usage" (13 words) — §Commands, `--vacuum-size=`/`--vacuum-time=`/`--vacuum-files=` entry, note paragraph, copy lines 299-300; second located span "the vacuuming operation only operates on archived journal files" (9 words), copy line 301 | admit, mined, tier A, supersedes S351 |
```

## Draft — S351 status/used-by note (S351 stays rejected; no in-place edit)

Row-change log line (the "old → new" form Rule 2 asks for, showing there is nothing to log):

```markdown
| S351 | status `rejected` → `rejected` (unchanged) | used-by `—` → `—` (unchanged) | Round-49 flip recorded forward-only on new row S486, whose `teaches` opens `supersedes S351 —`; no cell of S351 edited |
```

Explanatory note for the lesson Gate:

```markdown
**S351 — kept rejected, `used-by` stays `—`, no in-place change.** S351's refusal was about the evidence
behind the earlier claim (a shokuknow `file://` note and a kernel MESSAGE grep), not about the page, so
its `rejected` verdict and its flip text ("the public --vacuum-size= sentence plus a committed read-only
disk-usage receipt, and no MESSAGE grep") are the record of why that attempt failed and stay as written.
CORPUS.md Rule 2 makes a correction a new row (`supersedes S0NN —`) and permits in-place edits only to
`status`, `recheck` and `used-by`; here none is needed: changing `status` would erase the rejection the
contract says stays, and pointing `used-by` at `corpus/knowledge/journal-reach-r49.md` would assert that
an admitted entry cites S351 when it cites S486 — and C2's own row predicate requires the cited row to be
`mined` (`count-c2.py:160`), so an entry row citing S351 would score `bad_rows` and could not reach
`C2=met`. The flip is therefore carried entirely by S486.
```

## What the census script does with scope, rejected pairs and `supersedes`

Read in `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh` and then exercised (fixtures A-J):

- **Keying.** `scope_key = u SUBSEP scope` (`:643`) where `u = url_of(source)` (`:600`) and `scope` is the
  sixth cell after `trim` (`:581`, ASCII leading/trailing whitespace only). The comparison is a plain
  **string** comparison: case-sensitive, no internal-whitespace folding, no stemming. Observed: one
  internal double space in an otherwise identical scope escaped E04 (fixture I → `W04` only), while
  leading/trailing spaces did not (fixture J → `E04`, because the cell is trimmed first).
- **URL normalisation** (`url_of`, `:600-605`, code-read): first `https?://…` token, `#fragment` removed,
  one trailing `/` removed, scheme stripped, **host lowercased only** (path case preserved). So
  `https://WWW.freedesktop.org/…/journalctl.html` and the same URL with a trailing slash key as one URL.
- **`W04` (warning)** fires for a URL already seen under a *different* scope key (`:644-645`); it never
  changes the exit status (selftest `W04-does-not-fail-validation`, `:364`). This is the warning the lane
  already carries 20 times at round start, twice for this URL (S351, S470).
- **`E04` (error) fires only when all of these hold** (`:646-649`): the `(url, scope)` key was already
  seen; the new row's `status` is not `rejected`; some earlier row with that same key was not `rejected`
  (`url_scope_nonrejected` set at `:653`); and the new row's `teaches` does **not** match
  `/supersedes S[0-9]{3}/`. Three independent escapes therefore exist, each observed:
  (a) *rejected pair* — if the only earlier row for that key is `rejected`, no error can fire even with
  the identical scope and no supersedes (fixture B: clean, and the script's own
  `E04-rejected-pair-exemption` selftest at `:379-381`);
  (b) *supersedes* — the prefix suppresses E04 for that row even against a `mined`/`queued` earlier row
  (fixture C vs D: with the prefix no E04, with it removed `E04 S486 … within scope <S470 scope>`);
  (c) *new row rejected* — a `rejected` later row cannot fire E04 (fixture F);
  plus the trivial escape observed in fixture I: any cosmetic difference in the scope string makes it a
  different key, leaving only the `W04` warning.
- **Consequence for S486.** With the drafted distinct scope, the key is new, so neither `W04`'s
  counterpart nor `E04` can fire on scope; `W04` does fire because the URL is shared, and that is the
  single added census line. The `supersedes S351 —` prefix is required by the contract and by Rule 2, not
  by the counter in this configuration — it *would* be the only thing preventing E04 if the scope had
  repeated S470's (fixture C/D).

## Touched surfaces

- Written: `.ufo/waves/round-49/w1/Mo49ScribeRowCtl.md` (this report, the only lane file).
- Scratch (allowed by the seat block, left for round-end cleanup):
  `.scratch/r49-Mo49ScribeRowCtl/{row-s486.txt, live-journalctl.1.html, live-headers.txt,
  fix-A…fix-J/, fix-full-base/, fix-full-aug/}`.
- Read-only: `corpus/SOURCES.md`, `corpus/evidence/sources-r49/journalctl.1.html`,
  `.ufo/waves/round-49/{contract.md,count-c2.py,evidence/*}`, `corpus/lessons/round-{28,30}.md`,
  `.ufo/waves/round-49/w1/Mo49ScribeRowConf.md` (sibling draft, read only for Gate-table and id
  continuity), `/home/vgpnk/Projects/shokunin/{CORPUS.md,scripts/sources-census.sh}`,
  `/home/vgpnk/.omp/agent/RULES.md`, and the live freedesktop.org page (one GET).
- Not edited: `corpus/SOURCES.md`, `corpus/knowledge/`, `corpus/lessons/`, `tools/`, `SKILL.md`,
  `LOG.md`, `SCORECARD.md`, `QUALITY.md`, the frozen round-49 files, `shokuknow` (not touched at all),
  any sibling lane or fleet repo. No git write command, no jj command, no census `--out`, no
  `__pycache__` written by this seat (`python3 -B` used; the two `.pyc` files in
  `.ufo/waves/round-49/__pycache__/` are other seats', timestamps 21:24 and 21:43).

## Out of scope / UNVERIFIED

- **`C2=met` is UNVERIFIED by me.** It needs the entry `corpus/knowledge/journal-reach-r49.md` with 8+
  located rows, the three sibling source rows S485/S487/S488, provenance lines and the frozen copies.
  I did not run `count-c2.py` against the repo: the entry does not exist and the row is not integrated.
- **`C1` untouched** — not read for scoring beyond the contract summary.
- The row's `used-by` target does not exist yet. Landing S486 before the entry file exists makes the
  census print `E11 S486 missing used-by corpus/knowledge/journal-reach-r49.md` (observed in fixtures
  G-J). Integration order: entry file first, or both in one landing.
- Tier A is scoped to the vacuum-switch facts only; the row claims nothing about this host's effective
  retention, about `Storage=`, about `journald.conf` retention options (S485), or about the receipt
  (S488).
- The Gate quote is verified against the committed copy, re-confirmed byte-identical to a 2026-10-25
  live GET. No claim that the page is unchanged after that date.
- I did not verify S351's flip receipt (the read-only host receipt) — that is S488's seat. The `teaches`
  cell refers to it descriptively, naming no id: the sibling drafts map S488 to the receipt, but the id
  assignment is the L1's integration choice, so the row does not depend on it.

## Findings

- **MED** — `corpus/SOURCES.md` (new S486 line), `.ufo/waves/round-49/evidence/census-start.txt`: adding
  S486 raises the census `W04` count from 20 to 21 (the third row on the journalctl URL). Exit stays 0
  and the `ok` line still prints (full-registry A/B diff: one line added, nothing else). The round-end
  census will therefore not match the round-start receipt line-for-line; the contract asks for a
  round-end census, not for an unchanged count, so this is an expected delta the L1 should not read as
  drift.
- **MED** — `scripts/sources-census.sh:643-649`: E04 keys on the exact scope string, so a cosmetic
  internal-whitespace change makes a duplicate-URL row a "different scope" and demotes the error to a
  `W04` warning (observed, fixture I). The census can distinguish "different scope" from "same scope
  mistyped" only by human reading; my row passes on substance (a genuinely different scope), not on this
  loophole, but the same channel is open to a careless row.
- **MED** — `corpus/knowledge/journal-reach-r49.md` (absent), `scripts/sources-census.sh:538-571`
  (`E11` printed at `:567`): S486's `used-by` path must exist at landing time; otherwise the lane census
  fails with `E11 S486`. Observed in fixtures G-J. Ordering constraint for the L1's integration, not a
  defect in the row. The same function skips every non-`mined` row (`:559`), which is why S351's
  `used-by` `—` can stay as it is.
- **LOW** — `scripts/sources-census.sh:648`: the `supersedes` exemption is id-blind — any
  `supersedes S###` anywhere in `teaches` suppresses E04 for that row, regardless of whether the named
  row is the one that collides, or exists at all (fixture C used S470's scope and was exempted by
  `supersedes S351`). A row can therefore reuse a scope by attaching an unrelated supersedes.
- **LOW** — `corpus/evidence/sources-r49/journalctl.1.html` (lines 299-303): the copy renders
  `--disk-usage` as a `<code>` element followed by a literal comma, so `count-c2.py`'s tag→space
  collapse yields `--disk-usage ,` and a naturally punctuated quote fails the located check
  (`has only an indirect effect on the output shown by --disk-usage, as …` → not found; the span ending
  before the comma → found). The C2 entry author must pick spans that avoid element/punctuation
  boundaries.
- **LOW** — `corpus/SOURCES.md:248` (S351) / `.ufo/waves/round-49/w1/Mo49ScribeRowConf.md`: S486's
  `opened` must be the local date `2026-10-25`, while the live HTTP `Date` header reads
  `2026-10-26 00:44:12 GMT`; `count-c2.py:31` hard-codes `OPENED = "2026-10-25"`, so a seat recording the
  UTC date would fail the row check. Same skew the sibling seat reported; recorded here because the Gate
  line shows a 2026-10-25 access date against an HTTP timestamp of 2026-10-26.
- **LOW** — `corpus/evidence/sources-r49/journalctl.1.html`: the page prints only `systemd 262` — no
  commit hash, no "last updated" — so the anchor's revision basis is the copy sha256 plus HTTP
  `Last-Modified: 2026-09-22 13:31:34 GMT`; there is no dated systemd release to cite.
- **LOW** — `.ufo/waves/round-49/__pycache__/`: two untracked bytecode files (`count-c1…pyc` 21:24,
  `count-c2…pyc` 21:43) written by seats that imported the frozen counters in-process. This seat wrote
  none (`python3 -B`); the round-end scratch cleanup should remove the directory.

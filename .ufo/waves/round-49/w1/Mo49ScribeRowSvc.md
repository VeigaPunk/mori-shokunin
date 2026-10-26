# ScribeRowSvc — round 49 w1: draft lane SOURCES row S487 (systemd-journald.service(8))

Seat: Mo49ScribeRowSvc (leaf; no subagent dispatch). Lane: mori-shokunin. Round: 49, wave w1.
Scope: draft the 11-column `corpus/SOURCES.md` row S487 for
`https://www.freedesktop.org/software/systemd/man/latest/systemd-journald.service.html`
(kind `docs`, tier A for the storage-location/default scope), with a Gate block. I wrote only
this report plus scratch under
`/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r49-Mo49ScribeRowSvc/`; no lane file was
edited, no git or jj state touched.

## What I opened

- Frozen contract `.ufo/waves/round-49/contract.md` (C2 predicate, four frozen URLs in
  `count-c2.py` COPIES; this URL → committed copy `systemd-journald.service.8.html`, frozen
  sha256 `a7b443568865bb09f45d1ec83f3a8ad0e6a158d4e2cd21053e72499eb5f51212`).
- `count-c2.py` (row predicate: `len(srow)==11`, URL substring in cell 2, `srow[7]=="mined"`,
  `srow[8]=="2026-10-25"`, entry path token in `srow[10]` split on `[,;]`; quote rule: one
  backticked span, 6–25 whitespace tokens, `normalise()` tag-strip/entity-decode/space-collapse).
- `/home/vgpnk/Projects/shokunin/CORPUS.md` §SOURCES.md (contract v1: source = `title —
  canonical URL`, no `|` in any cell, anchor = section/heading + revision, teaches = one grounded
  benefit).
- `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh` (E01 NF!=13, E04 duplicate URL+scope,
  E11 used-by path on disk, E12 row outside `## Registry`; `url_of()` strips fragment, trailing
  slash and lowercases host).
- Committed copy `corpus/evidence/sources-r49/systemd-journald.service.8.html` and the live URL.
- Rows checked for URL/scope overlap: `grep -cF "man/latest/systemd-journald.service.html"
  corpus/SOURCES.md` → `0`; nearest neighbours S470 (`journalctl --disk-usage`) and S351
  (rejected `journalctl(1)` row) are other surfaces, not this page.

## Commands (evidence)

### 1. Committed copy digest matches the frozen pin

```
$ sha256sum corpus/evidence/sources-r49/systemd-journald.service.8.html
a7b443568865bb09f45d1ec83f3a8ad0e6a158d4e2cd21053e72499eb5f51212  corpus/evidence/sources-r49/systemd-journald.service.8.html
```
exit 0 — equals the `count-c2.py` COPIES digest for this URL.

### 2. Live fetch with a browser User-Agent (scratch, TMPDIR=.scratch/r49-Mo49ScribeRowSvc)

```
$ curl -sSL -A 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36' \
    -o systemd-journald.service-live.html \
    -w 'http_code=%{http_code} size=%{size_download} url=%{url_effective} redirects=%{num_redirects}\n' \
    https://www.freedesktop.org/software/systemd/man/latest/systemd-journald.service.html
http_code=200 size=28143 url=https://www.freedesktop.org/software/systemd/man/latest/systemd-journald.service.html redirects=0
exit=0
$ sha256sum systemd-journald.service-live.html
a7b443568865bb09f45d1ec83f3a8ad0e6a158d4e2cd21053e72499eb5f51212  systemd-journald.service-live.html
```
The live response is byte-identical to the committed copy on 2026-10-25 (also checked
`com == live` → `True` in Python).

### 3. Page's own revision text

The page carries `<span style="float:right">systemd 262</span>` (the man-page version marker);
the HTML has no publication-date meta tag. `<title>` is `systemd-journald.service`.

### 4. Heading anchor and the storage paragraph

- `<h2 id="Description">Description¶</h2>` — the storage paragraph is the fourth paragraph of
  that section.
- `<h2 id="Files">Files¶</h2>` — lists `/run/log/journal/machine-id/*.journal`,
  `/run/log/journal/machine-id/*.journal~`, `/var/log/journal/machine-id/*.journal`,
  `/var/log/journal/machine-id/*.journal~`, and states `/run/` is used when `/var/log/journal`
  is not available or `Storage=volatile` is set.

### 5. Located quotes (counter `normalise` + `split(" ")`, all three present in committed and live copies)

```
13 True | /run/ is used when /var/log/journal is not available, or when Storage=volatile is set
17 True | The journal service stores log data either persistently below /var/log/journal or in a volatile way below /run/log/journal/
20 True | By default, log data is stored persistently if /var/log/journal/ exists during boot, with an implicit fallback to volatile storage otherwise.
```
exit 0. All are ≤25 tokens and ≥6 tokens.

### 6. Row shape — awk field count and the counter's own cell split

```
$ awk -F'|' '{print "NF=" NF}' s487-row.md
NF=13
```
`count-c2.split_cells(draft)` → `cells= 11 pipes_in_cells= False` (11 columns, no `|` in any
cell), matching the census contract (11 columns ⇒ NF=13).

### 7. Row accepted by the C2 row predicate (scratch registry + one-row stub entry, not the claim run)

A scratch `SOURCES.md` copy with S487 inserted before `## Paths`, and a scratch entry with one
claim row quoting the 17-token storage sentence, scored through `count-c2.evaluate()`:

```
False C2=unmet claims=1 located=1 quote_missing=0 bad_rows=0 sources=1 source_rows=ok pins=ok provenance=ok rev=test failed=claims_floor,sources_floor
```
exit 0 for the call. `bad_rows=0`, `quote_missing=0`, `source_rows=ok`, `pins=ok`,
`provenance=ok`; only the floors fail because the stub has one claim and one source. This is a
row-level simulation — **not** a `C2=met` receipt (the real entry is another seat's build).

### 8. Census validation of the row (scratch root, never the lane)

Two runs over a scratch copy of `corpus/SOURCES.md` with S487 inserted before `## Paths`:

```
$ sources-census.sh validate --file <scratch>/censusroot/mori/corpus/SOURCES.md --today 2026-10-25
# no entry on disk:
file	E11	S487 missing used-by corpus/knowledge/journal-reach-r49.md
# codes: 293 E11, 20 W04 (all E11 except S487 are scratch-root path artifacts: SKILL.md,
#        PROVINCE.md, corpus/README.md, corpus/knowledge/* are absent or linked individually)
exit=1

# with a stub corpus/knowledge/journal-reach-r49.md present:
# codes: 33 E11, 20 W04 — S487 has no finding
grep -c S487 <output>  ->  0
exit=1   (remaining 33 E11 are pre-existing rows whose used-by paths live at the lane root,
          absent in the scratch root; 20 W04 are the lane's standing duplicate-URL warnings)
```

No E01 (NF=13), no E03 (id unused: `grep -c "^| S487 " corpus/SOURCES.md` → `0`), no E04
(URL appears in no other row), no E05–E10 for S487.

First attempt appended the row at end of file and the census returned
`file E12 S487 row outside Registry section` — the row must be inserted inside `## Registry`
(the registry table ends at line 264; `## Paths` starts at line 265).

## Draft lane SOURCES.md row (S487)

Fenced for the L1 to integrate — I did not edit `corpus/SOURCES.md`:

```markdown
| S487 | systemd-journald.service(8) — https://www.freedesktop.org/software/systemd/man/latest/systemd-journald.service.html | docs | A | the service page's own statement of where the journal keeps log data (persistently below /var/log/journal or volatile below /run/log/journal, lost at reboot) and the boot-time existence of /var/log/journal that decides the default; not the retention options (S485) and not the journalctl commands (S486) | Description heading #Description and its storage paragraph naming both paths and the boot-time default; Files section #Files ("/run/ is used when /var/log/journal is not available, or when Storage=volatile is set"); page version text "systemd 262"; committed copy corpus/evidence/sources-r49/systemd-journald.service.8.html sha256 a7b443568865bb09f45d1ec83f3a8ad0e6a158d4e2cd21053e72499eb5f51212; live fetch with a browser User-Agent 2026-10-25 byte-identical | The page locates both journal stores and states the default test, so a reader can say which store holds the evidence and whether it survives a reboot. | mined | 2026-10-25 | 180d | corpus/knowledge/journal-reach-r49.md |
```

Column map: `S487 | source | docs | A | scope | anchor | teaches | mined | 2026-10-25 | 180d |
corpus/knowledge/journal-reach-r49.md` — 11 cells, no `|` inside any cell, NF=13 under
`awk -F'|'`. Scope text is site-specific and overlaps neither S470 (`--disk-usage` total) nor
S485/S486, so census E04 cannot fire on a shared URL+scope key; the URL is unique anyway.

## Gate block

```markdown
## Gate block — S487 (mined, opened 2026-10-25)
- Source: https://www.freedesktop.org/software/systemd/man/latest/systemd-journald.service.html
  — opened 2026-10-25, page version text "systemd 262".
- Located quote (17 words, ≤25): `The journal service stores log data either persistently below
  /var/log/journal or in a volatile way below /run/log/journal/` — location: `#Description`,
  storage paragraph (fourth paragraph under the Description heading). Occurs verbatim after
  tag-strip/entity-decode/space-collapse in the committed copy
  `corpus/evidence/sources-r49/systemd-journald.service.8.html` (sha256
  a7b443568865bb09f45d1ec83f3a8ad0e6a158d4e2cd21053e72499eb5f51212) and in the live copy.
- Default quote (20 words, ≤25): `By default, log data is stored persistently if
  /var/log/journal/ exists during boot, with an implicit fallback to volatile storage
  otherwise.` — same paragraph; located in both copies.
- Volatility quote (9 words): `in the latter case, it is lost at reboot` — same paragraph.
- Support: `#Files` adds `"/run/ is used when /var/log/journal is not available, or when
  Storage=volatile is set"` (13 words, located in both copies).
- Live fetch 2026-10-25, browser User-Agent: HTTP 200, 28143 bytes, 0 redirects,
  byte-identical to the committed copy.
- Verdict: admit S487 as mined, tier A for the storage-location and default scope only.
```

Gate line in one line, for the lesson: URL
`https://www.freedesktop.org/software/systemd/man/latest/systemd-journald.service.html`,
opened 2026-10-25, located quote `The journal service stores log data either persistently below
/var/log/journal or in a volatile way below /run/log/journal/` (17 words) at `#Description`,
storage paragraph.

## Notes / limits

- The row is `mined` for the storage-location and default scope; it does **not** claim retention
  sizes (S485 `journald.conf(5)` is the retention-options row) or the `journalctl --flush`
  command surface (S486).
- The page is the `latest` alias. At capture the version marker reads `systemd 262`; a later
  release may re-render or move the paragraph, which is what the 180d recheck cadence is for.
  The committed copy pins the bytes this round reads; only the frozen sha256 is checked by the
  counter.
- The live fetch was byte-identical, so "unchanged today" is observed, not inferred; the page
  carries no self-declared publication date, so the version string is the only revision handle.
- Census E11 for S487 is expected and transient: it clears when
  `corpus/knowledge/journal-reach-r49.md` lands (demonstrated with a stub in the scratch root).
- I did not run `count-c2.py R` against a lane revision (the entry does not exist yet); §7 is a
  row-level simulation through the counter's own `evaluate()`, not a claim receipt.
- No tool was installed or upgraded (nothing needed). No host read beyond the HTTP fetch; no
  `journalctl`, `systemctl`, `pacman`, git-write or jj-mutating command was run. No credential,
  session or private URL appears here; no machine id was read.
- Scratch left at `.scratch/r49-Mo49ScribeRowSvc/` (row draft, live copy, scratch registries,
  census TSVs); nothing outside my report was written in the lane.

## Findings

- **MED — `corpus/SOURCES.md` integration:** appending the new row at end of file lands it
  outside `## Registry`; the census returns `E12 S487 row outside Registry section` (observed in
  my first scratch validation). The row must be inserted before line 265 (`## Paths`), i.e. at
  the end of the registry table.
- **LOW — `corpus/SOURCES.md` / `corpus/knowledge/journal-reach-r49.md`:** while the entry is
  absent, census reports `E11 S487 missing used-by corpus/knowledge/journal-reach-r49.md`. This
  is an integration-order dependency on the entry seat, not a row defect; it clears once the
  entry exists (verified with a stub in the scratch root).
- **LOW — S487 anchor cell:** the page exposes only the `systemd 262` version marker and no
  publication date; a reader cannot date the text beyond the capture. The 180d cadence and the
  frozen sha256 bound this, and the row's scope does not rest on a date.

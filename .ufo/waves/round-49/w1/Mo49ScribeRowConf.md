# Mo49ScribeRowConf — lane SOURCES.md row for journald.conf(5), id S485

Seat: wave w1, lane mori-shokunin. Bounds observed: leaf seat, no subagents; lane files read-only
(this report is the only lane file written); every command below run with the lane repo as cwd.

## Behavior

Drafted (not integrated) the `corpus/SOURCES.md` registry row for the `journald.conf(5)` manual page as
id **S485**, in the 11-column schema of `/home/vgpnk/Projects/shokunin/CORPUS.md` §SOURCES.md, and the
matching lesson `## Gate` line for round 49. The row is grounded in the committed copy
`corpus/evidence/sources-r49/journald.conf.5.html` and in a 2026-10-25 live fetch of the canonical URL
with a browser User-Agent (byte-identical to the committed copy).

S485 was unused at the time of drafting: `grep -c 'S485' corpus/SOURCES.md` → `0` (exit 1);
last registry row is `| S484` (line 263 of `corpus/SOURCES.md`); insertion point is after S484, before
the blank line and `## Paths` (line 265).

## Commands and observed evidence

All commands run from `/home/vgpnk/Projects/shokunin/mori-shokunin` unless a `cd` is shown.
Scratch: `TMPDIR=/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r49-Mo49ScribeRowConf`.

1. Committed copy and its freeze pin.
   `sha256sum corpus/evidence/sources-r49/journald.conf.5.html` →
   `b4a9b53e3e53dc5384bfffeb777218ced4c91712b0222b71405146ab470bc340` (matches `COPIES` in
   `.ufo/waves/round-49/count-c2.py` for the journald.conf URL). `file` → `HTML document, Unicode text,
   UTF-8 text, with very long lines (2003)`.

2. Page version/revision text visible in the copy (normalised text head):
   `journald.conf Index · Directives systemd 262 Name journald.conf, journald.conf.d, journald@.conf —
   Journal service configuration files`. `grep -o 'systemd [0-9][0-9][0-9]'` on the raw file → one hit,
   `systemd 262`. No commit hash or "last updated" revision string is printed on the page itself.

3. Live fetch with a browser User-Agent (exit 0):
   `curl -sS -D live-headers.txt -A 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36' -o live-journald.conf.5.html https://www.freedesktop.org/software/systemd/man/latest/journald.conf.html; echo "exit=$?"` →
   `exit=0`; live sha256 `b4a9b53e3e53dc5384bfffeb777218ced4c91712b0222b71405146ab470bc340` (identical to
   the committed copy). Response headers: `HTTP/1.1 200 OK`, `Date: Mon, 26 Oct 2026 00:41:36 GMT`,
   `Last-Modified: Tue, 22 Sep 2026 13:31:34 GMT`, `ETag: "9924-65c1262a14f2e"`,
   `Content-Length: 39204`, `Content-Type: text/html`.
   Local clock at fetch: `2026-10-25T21:41:58-03:00` (`2026-10-26T00:41:58+00:00` UTC); the access date
   recorded in the row and Gate is the local 2026-10-25 required by the contract.

4. Anchors in the copy: `id="SystemMaxUse="` holds the eight size options
   (`SystemMaxUse=`, `SystemKeepFree=`, `SystemMaxFileSize=`, `SystemMaxFiles=`, `RuntimeMaxUse=`,
   `RuntimeKeepFree=`, `RuntimeMaxFileSize=`, `RuntimeMaxFiles=`); `id="MaxRetentionSec="` holds the time
   option. The persistent (`System*`, `/var/log/journal`) versus volatile (`Runtime*`, in-memory) split is
   stated inside the `SystemMaxUse=` entry (copy lines 139-152), and the vacuum caveat at copy lines
   174-181.

5. Located quote used in the Gate line and verified against the normalised copy
   (`tags stripped, entities decoded, whitespace collapsed`): copy lines 177-178, inside the `Options`
   section, `SystemMaxUse=` entry — 16 words, found in the normalised text.

6. Row shape checks on the draft
   (`awk -F'|' '{print "NF=" NF}' row-s485.txt`) → `NF=13` (11 cells + 2 edge pipes); 11 cells;
   no `|` inside any cell; `status`/`opened`/`used-by` cells read `mined` / `2026-10-25` /
   `corpus/knowledge/journal-reach-r49.md`. A throwaway `importlib` load of the frozen `count-c2.py`
   (read-only; its `sources_row`/`split_cells` on current `SOURCES.md` + this row) returned 11 cells,
   URL matched to the journald.conf key, `mined=True`, `opened==2026-10-25`, entry path present in
   `used-by`.

## Draft — `corpus/SOURCES.md` row (insert after S484, inside the registry table)

```markdown
| S485 | journald.conf(5) — https://www.freedesktop.org/software/systemd/man/latest/journald.conf.html | docs | A | the retention options in journald.conf(5) only — the eight System*/Runtime* size options and MaxRetentionSec=, the persistent (/var/log/journal) versus volatile runtime split they key on, and the archived-file-only deletion they describe; not journalctl's vacuum commands, not this host's effective values, not any measurement | Options section, entries SystemMaxUse=, SystemKeepFree=, SystemMaxFileSize=, SystemMaxFiles=, RuntimeMaxUse=, RuntimeKeepFree=, RuntimeMaxFileSize=, RuntimeMaxFiles= and MaxRetentionSec= (their id= anchors); page header systemd 262; committed copy corpus/evidence/sources-r49/journald.conf.5.html sha256 b4a9b53e3e53dc5384bfffeb777218ced4c91712b0222b71405146ab470bc340; live fetch byte-identical 2026-10-25 (HTTP Last-Modified 2026-09-22 13:31:34 GMT) | Journal reach is a size rule before a time rule: SystemMaxUse= and RuntimeMaxUse= cap the space per store, and only archived files are deleted, so a vacuumed store can still exceed its limit and an old record's absence needs a measurement. | mined | 2026-10-25 | 180d | corpus/knowledge/journal-reach-r49.md |
```

## Draft — lesson `## Gate` block line (round 49, "New SOURCES rows")

```markdown
| S485 | https://www.freedesktop.org/software/systemd/man/latest/journald.conf.html (copy sha256 `b4a9b53e…`, live byte-identical, page header `systemd 262`) | 2026-10-25 | "Also note that only archived files are deleted to reduce the space occupied by journal files." — §Options, `SystemMaxUse=` entry (copy lines 177-178) | admit, mined, tier A scoped to the retention options |
```

Optional candidate quote for the C2 entry's own table (same located span, 16 words, unique against the
other three sources' likely rows only if not reused): `Also note that only archived files are deleted to
reduce the space occupied by journal files.` The entry author owns uniqueness/row budget; this is a
candidate, not a commitment.

## Touched surfaces

- Written: `.ufo/waves/round-49/w1/Mo49ScribeRowConf.md` (this report).
- Scratch: `.scratch/r49-Mo49ScribeRowConf/{row-s485.txt,live-journald.conf.5.html,live-headers.txt}`.
- Removed: `.ufo/waves/round-49/__pycache__/count-c2.cpython-314.pyc` — bytecode written by my read-only
  `importlib` load of the frozen counter at 21:40 (-03:00); the file was untracked
  (`git ls-files` → 0 entries) and is gone; the pre-existing `count-c1.cpython-314.pyc` (21:24, another
  seat's) was left in place. No frozen byte changed.
- Not edited: `corpus/SOURCES.md`, `corpus/knowledge/`, `corpus/lessons/`, `tools/`, `SKILL.md`,
  `LOG.md`, `SCORECARD.md`, `QUALITY.md`, `.ufo/waves/round-49/{contract.md,count-c1.py,count-c2.py,controls,evidence}`.
- Read-only use outside the lane: `/home/vgpnk/Projects/shokunin/CORPUS.md`, the live
  freedesktop.org page. No shokuknow path touched. No tool installed.

## Out of scope / not verified

- `C2=met` is **UNVERIFIED by me**: the claim needs the entry `corpus/knowledge/journal-reach-r49.md`,
  rows S485-S488 and the provenance lines, which are other seats' output. I did not run `count-c2.py`
  against the repo (it would read git state and S485 is not integrated).
- Rows S486-S488 and the S351 flip row are sibling seats' drafts; I did not read or edit them, so
  cross-row id sequencing and quote uniqueness in the final entry table remain the L1's integration check.
- The live page was checked only for byte identity on 2026-10-25; no claim is made that the page is
  unchanged after that date, and the copy's `Last-Modified` (2026-09-22) is the server's, not a systemd
  release date beyond the visible `systemd 262` header.
- My row's scope deliberately excludes `journalctl(1)` vacuum commands, `Storage=`, and the host's
  effective values; the row is tier A only for the retention options it names.

## Findings

- **LOW** — `.ufo/waves/round-49/` frozen directory accumulates untracked `__pycache__` bytecode when
  seats import the counters read-only (pre-existing `count-c1.cpython-314.pyc`, 21:24; mine
  `count-c2.cpython-314.pyc`, 21:40, removed). A direct `python3 .ufo/waves/round-49/count-c2.py`
  invocation does not write it, but any in-process import does; the round-end scratch cleanup should
  include `.ufo/waves/round-49/__pycache__/`.
- **LOW** — access-date skew: the live fetch happened at local `2026-10-25T21:41:58-03:00` but the HTTP
  `Date` header reads `Mon, 26 Oct 2026 00:41:36 GMT`. `count-c2.py` hard-codes `opened == 2026-10-25`,
  so a seat recording the UTC date would fail the row check; this row uses the local date per contract.
- **LOW** — `journald.conf(5)` at `systemd 262` prints no commit or "last updated" revision; the only
  revision evidence is the visible `systemd 262` header, the committed copy's sha256 and the HTTP
  `Last-Modified` (`2026-09-22 13:31:34 GMT`). The anchor cell records all three rather than claiming a
  dated revision.
- **LOW** — `corpus/SOURCES.md:263` ends the registry table at S484; the S485 row must be inserted
  before the blank line preceding `## Paths` (`corpus/SOURCES.md:265`), not appended after the table's
  following sections, or the census `awk` row regex will not see it.

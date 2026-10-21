# SrcPythonLstat — C2 frontier source: symlink-following for report presence

STATUS: complete (seat SrcPythonLstat, leaf, read-only; no builds, tests, lint, census, or tool runs)

## Opened source

- URL: https://docs.python.org/3/library/os.html
- Fetched 2026-10-21 via the reader (markdown). The page is the Python 3.15.0 documentation. Access date: 2026-10-21.
- The reader output is held at `artifact://38266` (5692 lines). The line numbers below are reader-rendered lines in that artifact, not lines in CPython `Lib/os.py`. Section anchors are the stable locators. [INFERENCE: the anchors match the live page; no separate raw-HTML check was made.]

## Located passages (verbatim, markdown markup removed)

| Anchor | Reader line | Text |
|---|---|---|
| `#os.stat` (os.stat) | 2770 | "This function normally follows symlinks; to stat a symlink add the argument follow_symlinks=False, or use lstat()." |
| `#os.lstat` (os.lstat) | 2242 | "Similar to stat(), but does not follow symbolic links." |
| `#os.lstat` (os.lstat) | 2246-2247 | "As of Python 3.3, this is equivalent to os.stat(path, dir_fd=dir_fd, follow_symlinks=False)." |
| `#os.DirEntry.is_symlink` | 2710 | "Return True if this entry is a symbolic link (even if broken);" |
| `#follow-symlinks` (Dir-fd and follow_symlinks section) | 1842-1843 | "...the function will operate on the symbolic link itself rather than the file pointed to by the link." (preceded by: "If follow_symlinks is False, and the last element of the path to operate on is a symbolic link") |
| `#os.stat` (os.stat) | 2774-2782 | Windows-only: follow_symlinks=False disables following name-surrogate reparse points; not material for this Linux lane. |

## Proposed SOURCES row (for L1 integration; not written by this seat)

Next free id after the registry as read: S065 is the highest row, so the proposed id is S066. L1 owns `corpus/SOURCES.md` and must confirm the id at integration time.

```
| S066 | Python os module documentation — https://docs.python.org/3/library/os.html | docs | A | os.stat and os.lstat symlink-following semantics, final path element only; DirEntry.is_symlink; Python 3.15.0 docs opened 2026-10-21 | os.stat section `#os.stat`, reader line 2770, quote: "This function normally follows symlinks; to stat a symlink add the argument follow_symlinks=False, or use lstat()."; os.lstat `#os.lstat` lines 2242, 2246-2247; DirEntry.is_symlink `#os.DirEntry.is_symlink` line 2710; follow-symlinks rule `#follow-symlinks` lines 1842-1843 | A report-presence check on a final path component must not follow a symlink: os.stat follows by default, while os.lstat (equivalently follow_symlinks=False) operates on the link itself. | queued | 2026-10-21 | on-release | — |
```

Quote word count: 16 words (limit 25). Quote is verbatim from reader line 2770; the reader's markup `follow_symlinks=False` and `lstat()` links are unwrapped.

Status is `queued` with `used-by: —` because no corpus note cites the row yet. Flip to `mined` when a note or the C2 knowledge file cites it (registry convention, see the `queued` / `mined` rows).

## What this source does and does not ground

Grounded by the quote and the anchors:
- `os.stat` follows symlinks by default; `follow_symlinks=False` or `os.lstat` is the documented way to act on a link itself (`#os.stat`, reader 2770; `#os.lstat`, reader 2242).
- The non-following rule applies to the last element of the path only (`#follow-symlinks`, reader 1842-1843). Intermediate directory components that are symlinks are not covered by it.
- `DirEntry.is_symlink` returns True for a link even if broken (reader 2710). This is the scandir-side equivalent and does not follow the link.

Not grounded by this source:
- The docs do not discuss "report presence" checks, the lane's `.ufo/waves/` discovery, or any regular-file test. The application to report presence is a design rule, not a documented fact. [INFERENCE]
- That `os.lstat` plus a regular-file test (`stat.S_ISREG`) makes the `symlink-report` oracle case (`frozen/c2-expected.json` case `symlink-report`, expects `present 0`, `not_followed true`) pass. The `stat` module and `S_ISREG` were not opened by this seat. [INFERENCE: lstat of a link returns the link's own mode, so a regular-file test would fail; not observed.]
- Directory-component symlinks. The lane root or `.ufo/waves/` could itself be a symlink; `os.lstat` on the report path will not detect that. The C2 "resolves inside the lane root" rule (contract line 72-73) needs its own check; this source does not supply one. [INFERENCE]

## Suggested use in the C2 tool (advisory only; no edits made)

- Check the report path with `os.lstat` (or `os.stat(..., follow_symlinks=False)`), and treat a result that is not a regular file (`S_ISREG` false) as not present. Size > 0 is then checked on that same lstat result.
- Resolve the containing directories separately (for example `os.path.realpath` of the parent, compared with the lane root) to cover directory-component symlinks. The docs do not promise this; it is an implementation choice. [INFERENCE]

## Tooling

- No tools installed or updated by this seat.
- No code run; no builds, tests, lint, formatters, census, or lane selftests.
- No retained transcripts opened. No writes outside this report.

## Files and paths

- Report (this file): `.ufo/waves/round-20/build/SrcPythonLstat.md` (relative to `/home/vgpnk/Projects/shokunin/mori-shokunin`).
- Read-only inputs: `.ufo/waves/round-20/contract.md`, `.ufo/waves/round-20/frozen/c2-expected.json`, `corpus/SOURCES.md`.
- Source artifact: `artifact://38266` (fetched os module docs).

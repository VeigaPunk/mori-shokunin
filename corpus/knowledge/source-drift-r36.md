source: S205 — fleet `CORPUS.md`, section *SOURCES.md — where a shokunin learns* (rule 2 and the `recheck` column, `CORPUS.md:105-106,116-118`); https://raw.githubusercontent.com/VeigaPunk/shokunin/6a1dd8ce1a3165a25f9f2b774b21449e0d125c94/CORPUS.md
verified-at: 2026-10-23
recheck: on-release

# Re-fetching source rows against their committed copies (round 36, C1 — exploratory)

`python3 tools/mori-source-drift.py --root DIR` reads `DIR/corpus/SOURCES.md`, takes each registry row's first
`http(s)://` URL in the `source` cell and the copy `DIR/corpus/evidence/sources-r<N>/<id>.<ext>` with the highest `N`,
fetches the URL (redirects followed, retries on 429/5xx) and prints `<id> <state>` per row, then
`MORI_SOURCE_DRIFT rows=N fresh=a excerpt=b drifted=c unavailable=d no-copy=e`. Exit 0 when `drifted=0`, 1 when any row
is drifted, 2 when `SOURCES.md` is missing or unreadable, on bad usage, or when `--root` is not a directory (a setup
failure, never a verdict). It is read-only and needs the network; it is a probe, not a gate
gate (`SKILL.md` Gates registry). CORPUS.md gives `recheck` a date or cadence and specifies no action when a source
changed (`CORPUS.md:105-106`), so this probe adds the byte check; it does not replace the row's recheck duty.

`fresh` proves only byte identity with the committed copy, never that the row's `teaches` is right. `drifted` means
the committed copy is not reproducible from today's body. That is not the same as a changed source. Observed
`drifted` sets, each with its command: the 12:03Z c0 re-score (`.ufo/waves/round-36/evidence/c0-rescore-v2.txt`)
counted seven — five annotated excerpts from round 30 (S156–S160: header lines and line-number prefixes; each
header's full-document sha256 still equals the live body — re-verified by w2 `RevQuality105`) and two docs.python.org
pages whose only change is the build footer (S176, S177). The 16:2xZ live run
(`python3 tools/mori-source-drift.py --root .` → `.ufo/waves/round-36/evidence/drift-live-r36.txt`,
`MORI_SOURCE_DRIFT rows=220 fresh=49 excerpt=0 drifted=9 unavailable=0 no-copy=162`, exit 1) counts nine: those
seven plus two rows opened this round whose live bodies changed after copying — S210 (git-rev-parse docs; the diff
is a stylesheet/script-integrity line and the taught passage is unchanged; open-time copy sha256
`64c603545b3f9799cc9525228ba70cf80444a063b32a4be37de2a5ca09b83421`) and S211 (the PMC mirror, itself a rejected
row; the page varies per fetch — csrf meta — so it can never classify `fresh`; open-time copy sha256
`a4e104ec9d6da304cc642346112b6f450dd2e4ef45d1a8e43531949842f39511`). For S210/S211 the QUALITY 105 procedure
is executable as written: the recorded open-time sha256 is the committed copy's
(`sha256sum corpus/evidence/sources-r36/<id>.src`). Reader action for a fetch-varying row (S211 class): treat
repeated `drifted` as a variance witness, not a source change; record two fetches' shas in the round lesson Gate
and prefer the pinned fleet or tag URLs over scrape pages when a row is next opened.

| state | meaning | reader action |
|---|---|---|
| `fresh` | sha256 of the fetched body equals the newest committed copy | Re-read the row's `teaches` cell against the anchored lines of the copy before citing it; byte identity does not check the claim. |
|`excerpt`|not fresh, and the copy with edge whitespace stripped is non-empty and occurs contiguously in the fetched body (a whitespace-only copy is non-empty-failing and classifies `drifted`)|Search the fetched body for the row's anchored quote and record its new line numbers in the next lesson Gate if they moved.|
| `drifted` | the copy is neither identical to nor contained in the fetched body | Open the copy's first lines: when it carries a `sha256:` header, compare that value with `curl -sS <URL> \| sha256sum` and record a header match as an annotated excerpt, not a change; otherwise diff the copy against the fetched body and re-check the row's `teaches`. |
| `unavailable` | connection error, timeout or non-2xx after retries; an unavailable probe is not drift | Re-run `python3 tools/mori-source-drift.py --root DIR` later and report the row as unchecked in the round lesson. |
|`no-copy`|the row has no URL or no copy file; a copy path that exists but cannot be read is also mapped here; nothing is fetched|Report the row as outside the probe; save a byte copy under `corpus/evidence/sources-r<round>/<id>.src` when the row is next opened.|
|exit 2|setup failure — `SOURCES.md` missing or unreadable, bad usage, or `--root` not a directory; no verdict|Detection and report only: name the missing/unreadable path or usage error in the round report; whether and how the file is restored is an operator decision, not a probe action.|

Round-36 copies (`corpus/evidence/sources-r36/S205.src`–`S220.src`) are raw response bodies saved with `curl`, so they
classify `fresh` or `drifted` by content alone. Self-test: `python3 tools/mori-source-drift.py --selftest` (offline
fixture on 127.0.0.1).

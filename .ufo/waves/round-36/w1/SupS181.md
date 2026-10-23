measured 2026-10-23T12:04:03Z

# S181 source-drift ruling and drafts

Axes: source fidelity, provenance, containment.

## Findings

- At lane tip `6bd57097`, `git show 6bd57097:corpus/SOURCES.md | grep '^| S181 '` returned the current S181 row. The row is mined, opened 2026-10-23, recheck on-release, and used by `corpus/knowledge/disk-write-rate-r33.md`.
- `ScoutAppendDebt.md:35` identifies `ab8f4cfe` as the in-place source, scope, and anchor edit and says the teaches cell was unchanged and the prior change was not logged old-to-new.
- `git show 62db24c0:corpus/SOURCES.md | grep '^| S181 '` returned the first-published row; `git show 62db24c0^:corpus/SOURCES.md | grep '^| S181 '` returned no match. The first-published row has the earlier source gloss, scope, and anchor also returned by `git show ab8f4cfe^:corpus/SOURCES.md | grep '^| S181 '`. `62db24c0` is the first publication; `ab8f4cfe` made the later in-place changes.
- Fetch command: `timeout 120s sh -c 'mkdir -p /fast/scratch/hyaku/mori-r36/SupS181 && curl --connect-timeout 20 --max-time 90 -L -sS -w "HTTP_STATUS=%{http_code}\n" -o /fast/scratch/hyaku/mori-r36/SupS181/S181.src https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/admin-guide/iostats.rst; rc=$?; printf "CURL_EXIT=%s\n" "$rc"; if test -f /fast/scratch/hyaku/mori-r36/SupS181/S181.src; then sha256sum /fast/scratch/hyaku/mori-r36/SupS181/S181.src; fi'` → `HTTP_STATUS=200`, `CURL_EXIT=0`, SHA-256 `166bdc8fd4ee9e53bcb86804e0d22d50c89314dcfc1a248814b0069300034124`; bytes saved at `/fast/scratch/hyaku/mori-r36/SupS181/S181.src`.
- The opened bytes at `S181.src:22` say both files have the same 17 statistics; `:33-36` state cumulative monotonic counters and reset conditions; `:75-76` state field 10 increases while field 9 is nonzero. These support each tip anchor locator and the corresponding teaches claims. The reset spelling in the tip, reinitialisation, differs from the source spelling, reinitialization, but not its meaning.
- `git cat-file -e 6bd57097:corpus/knowledge/disk-write-rate-r33.md` returned without error, confirming the one used-by path exists at tip.
- No tools were installed or updated. No lane source, product code, registry, or git index was changed; this report and the scratch source bytes are the only writes.

VERDICT: supported

## Drafts

DRAFT corpus/SOURCES.md
```text
| S2NN | Linux I/O statistics fields documentation v7.2 (tag-pinned counterpart of the docs.kernel.org page in S033) — https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/admin-guide/iostats.rst | docs | A | the v7.2 iostats field semantics: which fields are cumulative, when they reset, how field 10 grows, and the sysfs/procfs equivalence | Documentation/admin-guide/iostats.rst:22,33-36,75-76; tag v7.2 | supersedes S181 — All fields except field 9 are cumulative monotonic counters; they reset at boot, on device reattachment or reinitialisation, or on counter overflow; field 10 grows while field 9 is nonzero; /proc/diskstats and /sys/block/<dev>/stat carry the same 17 statistics. | mined | 2026-10-23 | on-release | corpus/knowledge/disk-write-rate-r33.md |
```

DRAFT corpus/lessons/round-36.md
```text
Gate: https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/admin-guide/iostats.rst; accessed 2026-10-23; sha256 166bdc8fd4ee9e53bcb86804e0d22d50c89314dcfc1a248814b0069300034124; Documentation/admin-guide/iostats.rst:22 — Both files contain the same 17 statistics.; Documentation/admin-guide/iostats.rst:33 — All fields are cumulative, monotonic counters, except for field 9, which resets to zero as I/Os complete.; Documentation/admin-guide/iostats.rst:34-36 — The remaining fields reset at boot, on device reattachment or reinitialization, or when the underlying counter overflows.; Documentation/admin-guide/iostats.rst:75-76 — Field 10 -- # of milliseconds spent doing I/Os (unsigned int) This field increases so long as field 9 is nonzero.; decision supported.
```

## Touched surfaces and limits

- Lane report: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/w1/SupS181.md`.
- Scratch evidence: `/fast/scratch/hyaku/mori-r36/SupS181/S181.src`, SHA-256 recorded above.
- This ruling tests the requested anchor and teaches against the opened pinned source. It does not independently revalidate the source description's relationship to S033 or other registry metadata.

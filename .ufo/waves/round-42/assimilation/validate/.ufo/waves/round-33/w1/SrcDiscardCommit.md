# Round 33 wave 1 — discard-accounting commit source

## Candidate and provenance

- **Commit:** `bdca3c87fb7ad1cc61d231d37eb0d8f90d001e0c`, subject `block: Track DISCARD statistics and output them in stat and diskstat` (commit message in `discard-first.src:1-25`). I found it in GitHub's Linux commit search for `diskstats discard` restricted to 2017–2020; saved result: `/fast/scratch/hyaku/mori-r33/MoriR33.SrcDiscardCommit/search2.json`.
- **URL opened:** https://github.com/torvalds/linux/commit/bdca3c87fb7ad1cc61d231d37eb0d8f90d001e0c.patch
- **Accessed:** first fetch `2026-10-23T02:40:27Z`; second fetch `2026-10-23T02:40:27Z` (timestamps recorded immediately before each fetch).
- **Bytes:** 9,498 on both fetches.
- **SHA-256:** `f265ef76e862e4e48cdbdae1b4702cbe47b356501d5d6cbfe9abeaaacd4cf318` on both fetches; the second-copy digest equals the first.
- **Saved unchanged copies:** `/fast/scratch/hyaku/mori-r33/MoriR33.SrcDiscardCommit/discard-first.src` and `.../discard-second.src`.
- **How the path was selected:** the focused GitHub API commit search returned the subject and SHA above; fetching the supplied `commit/<sha>.patch` URL succeeded. No v7.2 replacement was needed. The patch's historical documentation paths are `Documentation/block/stat.txt` and `Documentation/iostats.txt` (patch lines 27–34, 62–65, 111–114), not `.rst` paths.
- **Registry duplicate check:** searched `corpus/SOURCES.md` for the exact SHA and commit subject; no matches. Earlier host-URL search showed only unrelated Linux commits (SOURCES lines 102 and 151). This candidate URL is therefore not already registered in the checked registry.

## Draft SOURCES row

```text
| SRC | Linux block: Track DISCARD statistics and output them in stat and diskstat — https://github.com/torvalds/linux/commit/bdca3c87fb7ad1cc61d231d37eb0d8f90d001e0c.patch | code | A | Upstream discard-accounting introduction for /proc/diskstats and sysfs stat, with accompanying block-stat and iostats documentation changes; this is the 2018 introduction patch, not a current rate recipe | commit message:7-18; Documentation/ABI/testing/procfs-diskstats:41-61; Documentation/block/stat.txt:62-73,99-102; Documentation/iostats.txt:111-140; commit bdca3c87fb7ad1cc61d231d37eb0d8f90d001e0c | The commit message names discard completions, merges, completed sectors, and elapsed milliseconds; its ABI note adds four discard fields to reach 18 total. The block-stat change names a discard-sector counter, and iostats labels field 15 as milliseconds spent discarding. | mined | 2026-10-23 | on-release | corpus/knowledge/disk-write-rate-r33.md |
```

## Draft Gate row

```text
| SRC | https://github.com/torvalds/linux/commit/bdca3c87fb7ad1cc61d231d37eb0d8f90d001e0c.patch | 2026-10-23T02:40:27Z | f265ef76e862e4e48cdbdae1b4702cbe47b356501d5d6cbfe9abeaaacd4cf318 | `SRC.src:12-15` (20 words): "Number of discard ios completed. Number of discard ios merged Number of discard sectors completed Milliseconds spent on discard requests"; `SRC.src:53-54` (16 words): "+ Kernel 4.18+ appends four more fields for discard + tracking putting the total at 18:"; `SRC.src:72` (7 words): "+discard sectors sectors number of sectors discarded"; `SRC.src:138` (8 words): "+Field 15 -- # of milliseconds spent discarding" | admit, A, mined |
```

## Numbered facts and quotes

1. The commit message identifies four tracked discard measures: completed operations, merged operations, completed sectors, and time spent. Quote: `SRC.src:12-15` — “Number of discard ios completed. Number of discard ios merged Number of discard sectors completed Milliseconds spent on discard requests”.
2. The ABI addition says Linux 4.18+ adds four discard fields and the resulting line has 18 fields. The patch numbers those additions 15–18; before them, it describes 14 fields, including the three device-identification fields and eleven I/O-stat fields (`SRC.src:41-59`). Quote: `SRC.src:53-54` — “+ Kernel 4.18+ appends four more fields for discard + tracking putting the total at 18:”.
3. The `Documentation/block/stat.txt` change adds a discard-sector entry. Quote: `SRC.src:72` — “+discard sectors sectors number of sectors discarded”. The diff also adds discard-I/O, merge, and tick entries at `SRC.src:70-73`.
4. The `Documentation/iostats.txt` change labels field 15 as milliseconds spent discarding. Quote: `SRC.src:138` — “+Field 15 -- # of milliseconds spent discarding”. Its following lines specify measurement from `__make_request()` to `end_that_request_last()` (`SRC.src:139-140`).

## Not stated by this patch

- It does not provide a formula for turning samples into a disk write rate, nor a sampling interval or reporting threshold.
- It does not state counter wrap/reset behavior, device/partition aggregation rules, or whether stacked devices should be counted together.
- The newly introduced sector field is for discarded sectors; this patch does not equate it with sectors written.
- These are historical `.txt` documentation paths and a 4.18+ compatibility note; this patch alone does not establish the full current v7.2 field contract.

## Gates, touched surfaces, and limits

- Fetch gate passed: both saved patch copies are 9,498 bytes and have identical SHA-256 values. The URL fetched was the requested upstream commit-patch form.
- Duplicate gate passed for this candidate URL/SHA in the checked `corpus/SOURCES.md`.
- No source registry or Gate file was edited, no counter/judge was run, and no test/build was run. The rows above are drafts for the L1; `SRC` is intentionally unassigned.
- Only lane file written: `.ufo/waves/round-33/w1/SrcDiscardCommit.md`. Fetch and search artifacts are under `/fast/scratch/hyaku/mori-r33/MoriR33.SrcDiscardCommit/`. No tools were installed or updated.

## Commands and outcomes

- Commit search command: `timeout 70s bash -c 'date -u +%FT%TZ > /fast/scratch/hyaku/mori-r33/MoriR33.SrcDiscardCommit/search2.accessed && timeout 65s curl -sSL --fail -m 60 "https://api.github.com/search/commits?q=repo%3Atorvalds%2Flinux+diskstats+discard+committer-date%3A2017-01-01..2020-01-01&per_page=100" -H "Accept: application/vnd.github+json" -o /fast/scratch/hyaku/mori-r33/MoriR33.SrcDiscardCommit/search2.json && sha256sum /fast/scratch/hyaku/mori-r33/MoriR33.SrcDiscardCommit/search2.json && cat /fast/scratch/hyaku/mori-r33/MoriR33.SrcDiscardCommit/search2.accessed'` → hit `bdca3c87fb7ad1cc61d231d37eb0d8f90d001e0c`, response SHA-256 `bb7793970c609345081cb73be7f23f5206d9142cf500638fc57e225ebeed8596`, accessed `2026-10-23T02:40:10Z`.
- First source fetch: `timeout 70s bash -c 'date -u +%FT%TZ > /fast/scratch/hyaku/mori-r33/MoriR33.SrcDiscardCommit/discard-first.accessed && timeout 65s curl -sSL --fail -m 60 "https://github.com/torvalds/linux/commit/bdca3c87fb7ad1cc61d231d37eb0d8f90d001e0c.patch" -o /fast/scratch/hyaku/mori-r33/MoriR33.SrcDiscardCommit/discard-first.src && sha256sum /fast/scratch/hyaku/mori-r33/MoriR33.SrcDiscardCommit/discard-first.src && wc -c /fast/scratch/hyaku/mori-r33/MoriR33.SrcDiscardCommit/discard-first.src && cat /fast/scratch/hyaku/mori-r33/MoriR33.SrcDiscardCommit/discard-first.accessed'` → SHA-256 `f265ef76e862e4e48cdbdae1b4702cbe47b356501d5d6cbfe9abeaaacd4cf318`, 9,498 bytes, `2026-10-23T02:40:27Z`.
- Second source fetch: `timeout 70s bash -c 'date -u +%FT%TZ > /fast/scratch/hyaku/mori-r33/MoriR33.SrcDiscardCommit/discard-second.accessed && timeout 65s curl -sSL --fail -m 60 "https://github.com/torvalds/linux/commit/bdca3c87fb7ad1cc61d231d37eb0d8f90d001e0c.patch" -o /fast/scratch/hyaku/mori-r33/MoriR33.SrcDiscardCommit/discard-second.src && sha256sum /fast/scratch/hyaku/mori-r33/MoriR33.SrcDiscardCommit/discard-second.src && wc -c /fast/scratch/hyaku/mori-r33/MoriR33.SrcDiscardCommit/discard-second.src && cat /fast/scratch/hyaku/mori-r33/MoriR33.SrcDiscardCommit/discard-second.accessed'` → identical SHA-256, 9,498 bytes, `2026-10-23T02:40:27Z`.
- Registry check searched `corpus/SOURCES.md` for `bdca3c87fb7ad1cc61d231d37eb0d8f90d001e0c|Track DISCARD statistics and output them`; result: no matches.

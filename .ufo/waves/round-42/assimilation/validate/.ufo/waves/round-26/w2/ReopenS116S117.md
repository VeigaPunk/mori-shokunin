# ReopenS116S117: round-26 wave-2 reopen of SOURCES rows S116 and S117

Seat: MoriR26.ReopenS116S117 (leaf reviewer; no subagents, no background jobs).
Pin: 16935e24c93fa7e7567413d7ec091339a5df1474. Scratch: /fast/scratch/hyaku/mori-r26/ReopenS116S117/.

## Verdicts

- **S116: holds.** Both sha256 values, all 13 anchor entries, the tag and commit, the Gate quote, tier, status and used-by check out. One recording gap: the row records no byte size (section 1.1).
- **S117: defect (medium).** The knowledge entry that names S117 as used-by describes a different source (D1). The Gate quote is not verbatim, is not located by line, and does not ground `teaches` (D2, D3). The tag, commit, dates, grammar anchors and the five hashes checked all hold.

## Method and scope

- Pinned text read with `git show 16935e24...:<path>`. Rows: `corpus/SOURCES.md:122` (S116) and `:123` (S117). Gate rows: `corpus/lessons/round-26.md:69` (S116) and `:70` (S117). Used-by file: `corpus/knowledge/userspace-oom-killers-r26.md`.
- Every URL in both rows fetched with curl (ordinary public GET, no browser). Every request returned HTTP 200. Extra fetches (section 4) cover the Gate URL, the tag objects, msg.c, and the v1.7 and v1.8 msg.h files.
- Line anchors checked on the fetched bytes with the read and grep tools. Gate quotes checked with grep against the fetched bytes.
- Contract clauses read from `/home/vgpnk/Projects/shokunin/CORPUS.md:84-130` (read only).
- Master is not the pin. `git rev-parse master` gives `ee83a88db2c365d8bb4c51aff619c5f5020be204`, which descends from the pin (`git merge-base --is-ancestor` succeeded). `git diff --stat 16935e24... master -- corpus/SOURCES.md corpus/lessons/round-26.md corpus/knowledge/userspace-oom-killers-r26.md` printed nothing, so these three files are identical at both revisions.
- Tooling: no installs and no updates. Used preinstalled curl, sha256sum, wc, and read-only git.

## 1. S116

### 1.1 Fetch, hash and bytes

| File at tag v1.9.0 | HTTP | Bytes | sha256 fetched | Row (`SOURCES.md:122`) |
|---|---|---|---|---|
| meminfo.c | 200 | 8,344 | 526e512c89c58cb0b1db2ae98ea62d287cdc1516846be80c9173bdc4bf0edfeb | same, full value |
| meminfo.h | 200 | 1,341 | 5b709094c507ba418a5284034614141bd48893b5a8fe1863214c46396aefb52f | same, full value |

The row gives no byte size, so the byte comparison cannot be made. Sibling rows do record sizes; for example S114 records README.md at 19,931 B, which matches the fetch. The contract asks for an exact line plus revision (`CORPUS.md:99-100`), not a byte size. This is a recording gap, not a defect.

### 1.2 Anchors (fetched line numbers)

All hold.
- meminfo.c:101 is `m.MemAvailableKiB = get_entry("MemAvailable:", buf);`.
- meminfo.c:102-106 is the fallback to `available_guesstimate` and the one-time warning.
- meminfo.c:60 is `return MemFree + Cached + Buffers - Shmem;`.
- meminfo.c:55-58 are four `get_entry_fatal` calls (Cached, MemFree, Buffers, Shmem). meminfo.c:96-99 are four more (MemTotal, SwapTotal, AnonPages, SwapFree).
- meminfo.c:112 is `m.UserMemTotalKiB = m.MemAvailableKiB + m.AnonPagesKiB;`.
- meminfo.c:115 divides MemAvailableKiB by UserMemTotalKiB.
- meminfo.c:116-119 is SwapFreePercent with its zero branch.
- meminfo.c:46 is `fatal(104, ...)` inside `get_entry_fatal`. meminfo.c:84 is `fatal(102, ...)` on fopen failure. meminfo.c:90 and :93 are `fatal(103, ...)` on a read error and on a zero-length read.
- meminfo.h:18-23: :18-19 document UserMemTotalKiB, :22 carries the comment "percent of total memory that is available" while the code at :115 divides by UserMemTotalKiB (the comment is stale), and :23 is SwapFreePercent.

### 1.3 Tag and teaches

- Tag v1.9.0 maps to commit 202d4db0d308ca6478f68de68b46cae34896ddaf. Holds: the tags list `commit.sha` and the tag object's `object.sha` agree.
- Teaches clause 1 (MemAvailable percentage is a share of user mem total, not MemTotal): meminfo.c:112 and :115. Holds.
- Clause 2 (MemAvailable fallback is MemFree + Cached + Buffers - Shmem): meminfo.c:53-60 and :102-103. Holds.
- Clause 3 (swap free is zero without swap): meminfo.c:116-119. Holds.
- Clause 4 (a /proc/meminfo read failure is fatal, not a quiet zero): meminfo.c:83-85 and :89-94. Holds.

### 1.4 Gate (`round-26.md:69`)

- Quote `m.MemAvailablePercent = (double)m.MemAvailableKiB * 100 / (double)m.UserMemTotalKiB;` matches meminfo.c:115 verbatim (grep, one match).
- Word count 7, within the 25-word limit. URL matches the row. Access date 2026-10-22 matches the row. The quote grounds teaches clause 1. Holds.

### 1.5 Tier, status, used-by

- Tier A, kind code. `CORPUS.md:93-94` lists source code under A. Holds.
- Status mined. `CORPUS.md:103-104` defines mined as cited by at least one used-by path. The used-by file exists at the pin (blob 90b82606) and cites S116 on its line 1, with the same URL and the same sha256. Holds.

## 2. S117

### 2.1 Fetch, hash and bytes

| File | HTTP | Bytes | sha256 fetched (prefix...suffix) | Row (`SOURCES.md:123`) |
|---|---|---|---|---|
| v1.9.0 main.c | 200 | 21,053 | 08656b0b...f9d0e4 | matches |
| v1.9.0 kill.c | 200 | 21,169 | b32e0fad...00bf3 | matches |
| v1.9.0 msg.h | 200 | 1,027 | e3660498...de56c | matches |
| v1.9.0 README.md | 200 | 19,931 | 23411dbf...74dd | matches |
| v1.9.0 msg.c (URL not in row) | 200 | 6,864 | a771c915...5197 | matches; URL missing (D5) |
| v1.8 main.c | 200 | 19,907 | 9bdc8209... | not recorded |
| v1.8 kill.c | 200 | 18,052 | 459af558... | not recorded |
| v1.8 msg.h | 200 | 1,027 | e3660498... (same as v1.9.0) | not recorded |
| v1.7 main.c | 200 | 17,326 | ceaa2083... | not recorded |
| v1.7 kill.c | 200 | 12,166 | 1453cd2a... | not recorded |
| v1.7 msg.h | 200 | 927 | e0e88f50... | not recorded |
| api tags / api releases | 200 | 11,754 / 19,594 | 87456fca... / 494a357d... | not recorded |

The row records no byte sizes. Its hashes are abbreviated with an ellipsis, so only prefix and suffix can be compared, and all five abbreviated values match. The byte sizes that sibling rows record (S114 README.md 19,931 B; S118 kill.c 21,169 B and msg.c 6,864 B) match the fetch.

### 2.2 Anchors (fetched line numbers): all hold

- Tags API: v1.9.0 maps to commit 202d4db0...; the annotated tag object is 66d78843...; tagger date 2025-09-16T19:09:33Z. Checked with `git/refs/tags/v1.9.0` (object type tag) and `git/tags/66d78843...`.
- Releases API: v1.9.0 `published_at` 2025-09-16T19:11:03Z (api-releases.json, and the release-by-tag object).
- README.md:283 is `* v1.9.0, 2025-09-16`.
- v1.9.0 main.c: :161 version line; :295 dry-run; :414 and :416 threshold lines; :519 and :523 low-memory warnings.
- v1.9.0 kill.c: :318 escalation; :627 action; :654 kill failed.
- v1.9.0 msg.h:10 is `#define PRIPCT "%5.2lf%%"`.
- v1.8 main.c:382 and :384 are the `mem avail` threshold lines; v1.8 kill.c:230 (escalation) and :539 (action).
- v1.7 main.c:326 and :328 are the `mem <=` threshold lines; v1.7 kill.c:167 (escalation) and :377 (action).

### 2.3 Teaches (grammar claims)

- The `mem avail` wording first appears in v1.8. v1.7-main.c:326 prints `mem <=`; v1.8-main.c:382 prints `mem avail <=`; v1.9.0 main.c:414 is unchanged. Holds.
- The action and escalation prefixes are stable from v1.7 to v1.9.0. Escalation text: v1.7-kill.c:167, v1.8-kill.c:230, kill.c:318. Action text: v1.7-kill.c:377, v1.8-kill.c:539, kill.c:627. The trailing fields differ: badness at v1.7, oom_score at v1.8, oom_score plus oom_score_adj at v1.9.0. Holds.
- The width-5 percentage format: `#define PRIPCT "%5.2lf%%"` is the same at v1.7, v1.8 and v1.9.0 (v1.7-msg.h:10, v1.8-msg.h:10, msg.h:10). Holds, but the row cites only the v1.9.0 line (D6).

### 2.4 Gate (`round-26.md:70`)

- Quote: `"published_at": "2025-09-16T19:11:03Z"`, located as "release object". Word count 2, within the limit. Access date 2026-10-22.
- Not verbatim. The fetched release object is a single line of compact JSON (api-release-v1.9.0.json:1) and reads `"published_at":"2025-09-16T19:11:03Z"`, with no space after the colon. The Gate's exact string matches nothing; the same string with an optional space matches line 1. The key and value are verbatim; the separator is not (D2).
- Location. The Gate names `https://api.github.com/repos/rfjakob/earlyoom/releases/tags/v1.9.0`, which is not in the row's URL list (`SOURCES.md:123` lists `.../releases`). The Gate gives no line or key path, only "release object" (D4).
- Grounding. The quote supports only the publication date. None of the four teaches clauses is quoted. `CORPUS.md:112-114` requires the Gate quote to ground `teaches` (D3).

### 2.5 Tier, status, used-by

- Tier A, kind tool. `CORPUS.md:91-92` lists `tool` as an allowed kind, and `CORPUS.md:93-94` lists maintainer statements and source code as A. Holds. [INFERENCE: the row mixes API metadata and code; `tool` is an allowed kind.]
- Status mined. The used-by file exists and names S117 on its line 1, so the literal rule holds (`CORPUS.md:103-104`). But that citation describes a different source (D1).

## 3. Findings

**D1, medium. The S117 used-by citation names a different source.**
- Attacks: the S117 row (`SOURCES.md:123`), the used-by path, and `CORPUS.md:107-108` ("paths of the knowledge entries or lessons citing the row").
- Evidence: `corpus/knowledge/userspace-oom-killers-r26.md:1` describes S117 as "earlyoom tag history" at `https://github.com/rfjakob/earlyoom/releases` and `https://api.github.com/repos/rfjakob/earlyoom/commits?path=main.c`, covering "the v1.2 removal of the kernel-oom option and its 2026-02-02 re-introduction on master". The registry row (`SOURCES.md:123`) lists no github.com page, no `commits?path=main.c` URL, and no kernel-oom or v1.2 scope. The 2026-02-02 date appears in the S114 anchor (`SOURCES.md:120`), not in S117. The entry's own body for the v1.2 claim cites `kill.c:242` and the installed binary (`userspace-oom-killers-r26.md:129-135`), not S117.
- Effect: a reader who follows S117 reaches a different source set. The kernel-oom history line has no registered row that carries it.
- Fix: correct line 1 to the registered URLs and scope, or register the commits and kernel-oom evidence as its own row and cite that id.

**D2, minor. The S117 Gate quote is not verbatim.** Attacks `round-26.md:70`. Evidence: section 2.4 (the fetched JSON has no space after the colon). Fix: quote the bytes as fetched, or re-quote from the row's own URL.

**D3, minor. The S117 Gate does not ground `teaches`.** Attacks `round-26.md:70` against `CORPUS.md:112-114`. The row's anchors do ground the grammar claims (section 2.2), so the substance holds; the Gate record does not. Fix: add one located quote of at most 25 words for the grammar claim, for example `main.c:414` or `kill.c:318` at v1.9.0, or `v1.8-main.c:382` for the `mem avail` wording.

**D4, minor. The S117 Gate URL and location do not match the row.** Attacks `round-26.md:70` against `SOURCES.md:123`. Evidence: section 2.4. Fix: use the row's URL, or add the release-by-tag URL to the row, and give a key path.

**D5, minor. A hash without its URL.** Attacks `SOURCES.md:123`. The msg.c hash (a771c915...5197) is in the row's hash list, but msg.c is not in its URL list. The row that lists msg.c with its URL is S118 (`SOURCES.md:124`). Fix: add the msg.c URL to S117, or drop the hash from S117.

**D6, minor. Scope claims at v1.7 and v1.8 are not anchored.** Attacks the S117 scope and anchor cells (`SOURCES.md:123`). The scope names the version line, the dry-run flag, the low-memory warnings, the kill-failure line and the percentage format "at those tags". All of them exist at v1.7 and v1.8: v1.7-main.c:109, :224, :431, :435; v1.8-main.c:132, :263, :487, :491; v1.7-kill.c:395; v1.8-kill.c:558; v1.7-msg.h:10; v1.8-msg.h:10. The row anchors none of them at v1.7 or v1.8, and msg.h at v1.7 and v1.8 is not in its URL list. Fix: add these anchors and URLs.

**D7, info. Recording gaps.** No byte sizes in either row; hashes abbreviated for S117; hashes for the v1.7 and v1.8 files and the API responses not recorded. The contract does not require them (`CORPUS.md:99-100`). No effect on the verdicts.

## 4. Fetch log (all HTTP 200, all read-only public GET)

- https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/meminfo.c (8,344 B)
- https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/meminfo.h (1,341 B)
- https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/main.c (21,053 B)
- https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/kill.c (21,169 B)
- https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/msg.h (1,027 B)
- https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/README.md (19,931 B)
- https://raw.githubusercontent.com/rfjakob/earlyoom/v1.8/main.c (19,907 B); .../v1.8/kill.c (18,052 B); .../v1.8/msg.h (1,027 B, extra)
- https://raw.githubusercontent.com/rfjakob/earlyoom/v1.7/main.c (17,326 B); .../v1.7/kill.c (12,166 B); .../v1.7/msg.h (927 B, extra)
- https://api.github.com/repos/rfjakob/earlyoom/tags (11,754 B); .../releases (19,594 B)
- Extra: .../v1.9.0/msg.c (6,864 B); https://api.github.com/repos/rfjakob/earlyoom/releases/tags/v1.9.0 (1,900 B); .../git/refs/tags/v1.9.0 (335 B); .../git/tags/66d78843fd675859a09a52d3f17b1c408a827a34 (2,538 B)

## 5. Not run and residual risk

- Not run: comparison of the wave-1 seat Gate blocks (`w1/SrcEarlyoomMeminfo.md`, `w1/SrcEarlyoomTagHistory.md`) with these numbers. Not needed for the verdicts.
- Not verified: the v1.2 kernel-oom removal and the 2026-02-02 re-introduction date (D1). They sit outside the S117 row, and I did not fetch the `commits?path=main.c` endpoint that the used-by line names.
- Tag immutability is assumed for the raw URLs; the annotated tag object confirms the commit for v1.9.0 only. The v1.7 and v1.8 tags were fetched by tag name, not by commit.

## 6. Notes outside the two rows

- `corpus/QUALITY.md:53` says tier definitions are "see corpus/SOURCES.md (contract v1)". At the pin, `SOURCES.md` has no tier or status legend (its headings are Registry, Paths, Search log and Leads). The contract text is in the fleet-root `CORPUS.md:84-130`, outside this lane. The pointer is stale. No effect on the S116 or S117 verdicts.
- Master carries two commits after the pin (2a23fbd, ee83a88). None of them touches the three files checked.

## 7. Recap

S116: holds. S117: defect (medium) on D1, with minor D2 to D6 and info D7.

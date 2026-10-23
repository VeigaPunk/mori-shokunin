# Recheck137 — S137 (C1, round 32 attempt 2)

Seat: MoriR32A2.Recheck137. Scope: one population id, S137. Verdict: **current**.
No tools installed or updated this seat (curl, python3, coreutils already present).
L1 action needed: commit the saved bytes unchanged as `corpus/evidence/recheck-r32/S137.src` (sha256 below).

## 1. Fetch

| field | value |
|---|---|
| id | S137 |
| population url | `https://api.github.com/repos/rfjakob/earlyoom/commits?path=main.c` |
| accessed (UTC, at fetch) | `2026-10-23T01:31:25Z` |
| HTTP | `HTTP/2 200`; no `Location` header → no redirect, final equals population URL; no bot challenge |
| tries | 1 of 3 (`curl -sSL --fail -m 60` exit=0) |
| byte size | 121162 |
| sha256 | `b658df9d6c52fd46c43db155022dd22c75e46fdd0abb86323ebcfc5c208bf775` |
| scratch copy (bytes unchanged) | `/fast/scratch/hyaku/mori-r32/MoriR32A2.Recheck137/S137.src` |
| normalised text | `/fast/scratch/hyaku/mori-r32/MoriR32A2.Recheck137/S137.text` (106684 bytes, one line: JSON `\n` escapes stay literal) |

Fetch command: `curl -sSL --fail -m 60 'https://api.github.com/repos/rfjakob/earlyoom/commits?path=main.c' -o S137.src`
(timestamp taken with `date -u +%FT%TZ` immediately before the GET). Status checked separately with
`curl -sSI` on the same URL → `HTTP/2 200`. GitHub rate limit seen at 01:31Z: remaining 24, reset
`2026-10-23T02:12:34Z` (relevant only to the counter's own R3 re-fetch).

## 2. Ready-to-paste row

```markdown
| S137 | https://api.github.com/repos/rfjakob/earlyoom/commits?path=main.c | 2026-10-23T01:31:25Z | b658df9d6c52fd46c43db155022dd22c75e46fdd0abb86323ebcfc5c208bf775 | "kill: option for triggering kernel oom killer"; "This implements an option for trigger the kernel oom killer" | current |
```

## 3. Page contents and quote → teaches-cell mapping

The page is a JSON array of **30** commits touching `main.c` (default `per_page=30`; `Link: rel="last"` says
6 pages). Author dates run `2021-08-09T15:40:59Z` (`788fe49e78`) to `2026-10-15T17:28:19Z` (`d33c11c642`,
committer `2026-10-17T18:34:22Z`).

Anchor commit `750a7c0d97bb01c1bdf126fd6bf5722da17e8998` is at index 4 of the fetched array, with
author date `2026-02-02T05:00:04Z`, committer date `2026-02-17T20:30:10Z` and subject
`kill: option for triggering kernel oom killer` — every anchor datum matches the live page exactly.

1. `kill: option for triggering kernel oom killer` (7 words; normalised offset 14780)
   Bears on **"returned on master in February 2026"**: the page shows this very subject on the default-branch
   commit list, with both its author and its merge/committer dates inside February 2026. That is the
   re-introduction event the teaches cell names, so the claim is still supported.
2. `This implements an option for trigger the kernel oom killer` (10 words; offset 14971)
   Same commit's message body (verbatim, including the message's own grammar): it says the patch implements an
   option that triggers the kernel OOM killer by writing `f` to `/proc/sysrq-trigger`, i.e. delegation of the
   kill to the kernel. This bears on **"current master grows a … long option"**: a delegation option exists on
   master, committed after v1.9.0.

Clauses **not** evidenced by this page, and why that is not drift: the normalised text contains 0 occurrences of
`v1.2` and 0 of `ignored`, so the v1.2 removal / `Option -k is ignored since earlyoom v1.2` string and the
`--kernel-oom` longopt spelling come from the row's other sources (S114 README.md, v1.9.0 main.c, and the pinned
main.c@750a7c0d URL in the SOURCES source cell), not from this commit listing. The page contradicts none of
them. The two `Revert` strings on the page are unrelated (2025-09-13 `notify: use double-fork…`, 2023-02-05
`Don't kill anything if there's not enough anon memory used`); no revert of the kernel-oom commit appears.

Verdict `current`: the live page still carries the February 2026 re-introduction commit with the exact anchor
sha, subject and dates, and nothing on it now says something different that matters.

## 4. seat-check output

```
$ timeout 300 python3 .ufo/waves/round-32/seat-check.py row S137 S137.src '"kill: option for triggering kernel oom killer"; "This implements an option for trigger the kernel oom killer"'
sha256=b658df9d6c52fd46c43db155022dd22c75e46fdd0abb86323ebcfc5c208bf775
quotes=2 words=[7, 10] in_copy=[True, True]
shared_tokens=['kernel', 'kill', 'killer', 'option', 'trigger', 'triggering'] topic_ok=True
live_quotes_ok=True
ROW_CHECK=pass (judge R4 and R5 not checked here)
```

`live_quotes_ok=True`: the helper's own live fetch of the population URL still contains both quotes.

## 5. Drift check — none; one anchor-vs-URL observation (no cell edit)

- No new commit touching `main.c` since the anchor's `2026-10-15` end: newest author date on the live page is
  `2026-10-15T17:28:19Z`.
- Anchor wording "first page of 100, 2018-07-16 to 2026-10-15": the literal population URL (no `per_page`)
  returns 30 entries, author dates 2021-08-09 to 2026-10-15. A page-1 fetch with `&per_page=100` returns 100
  entries whose oldest author date is `2018-07-16T07:04:01Z` and whose newest committer date is
  `2026-10-17T18:34:22Z`, matching the anchor's stated extent. [INFERENCE] the anchor was recorded from a
  `per_page=100` access of the same query. The commit sits at index 4 of the default page, so the anchor's
  substance still holds under the URL as written; this is not teaches drift and no cell needs editing.
- No `Round32` correction paragraph drafted (verdict `current`).

## 6. Leftover unknowns

- The `--kernel-oom` longopt spelling and the main.c line anchors were not re-verified here; they belong to the
  row's pinned `main.c@750a7c0d` URL, outside this live commits-query check. [INFERENCE] unchanged.
- Counter R3 must fetch `api.github.com` while quota lasts (reset `2026-10-23T02:12:34Z`).
- No processes left running (all commands under `timeout`); no git/jj writes in the lane; no installs.

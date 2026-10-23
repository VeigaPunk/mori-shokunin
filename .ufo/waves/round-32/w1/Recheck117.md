# Recheck117 — S117 (C1, round 32 attempt 2)

Seat: `MoriR32A2.Recheck117`. Scope: one population id, S117 (`https://api.github.com/repos/rfjakob/earlyoom/tags`).
Verdict: **current**. No tools installed or updated this seat (curl, python3, sha256sum already present); no pacman run.
Leaf seat: no subagents, no background jobs, no process left running (every curl returned and exited).

## 1. Fetch

| field | value |
|---|---|
| id | S117 |
| population url | `https://api.github.com/repos/rfjakob/earlyoom/tags` |
| accessed (UTC, at fetch) | `2026-10-23T01:31:22Z` |
| HTTP | `200`, `url_effective=https://api.github.com/repos/rfjakob/earlyoom/tags` (no redirect, no bot challenge) |
| tries | 1 of 3 (`EXIT=0`) |
| byte size | 13409 |
| sha256 | `423c43617a2a299315180292f43447936f6ddde01efff5baece3fc46ed8b1869` |
| scratch copy (bytes unchanged) | `/fast/scratch/hyaku/mori-r32/MoriR32A2.Recheck117/S117.src` |
| normalised text (seat-check output) | `/fast/scratch/hyaku/mori-r32/MoriR32A2.Recheck117/S117.norm.txt` (12249 bytes) |

Command and output:
`curl -sSL --fail -m 60 https://api.github.com/repos/rfjakob/earlyoom/tags -o S117.src -w 'HTTP=%{http_code} URL=%{url_effective} SIZE=%{size_download}\n'`
→ `HTTP=200 URL=https://api.github.com/repos/rfjakob/earlyoom/tags SIZE=13409`, `EXIT=0`; `sha256sum S117.src` → digest above.

Observed in the fetched bytes (parsed as JSON, `python3 -c "json.load(...)"`): 29 tag objects, newest first, names
`v1.9.0, v1.8.2, v1.8.1, v1.8, v1.7, v1.6.2, v1.6.1, v1.6, v1.5, v1.4, v1.3.1, v1.3, v1.3-rc1, v1.2, v1.1, v1.0,
v0.12, v0.11, v0.10, v0.9, v0.8, v0.7, v0.6, v0.5, v0.4.1, v0.4, v0.3, v0.2, v0.1`. `v1.9.0` → commit
`202d4db0d308ca6478f68de68b46cae34896ddaf`, `v1.8` → `62625072ce8671f497a5cea5fc3db63226469093`, `v1.7` →
`ebaea9526bcee14889b00d83a9dd3d038315cee2`. That commit for `v1.9.0` is byte-identical to the population anchor
(`v1.9.0` → `202d4db0d308ca6478f68de68b46cae34896ddaf`), and no tag newer than `v1.9.0` exists in the listing.

## 2. Ready-to-paste row

```markdown
| S117 | https://api.github.com/repos/rfjakob/earlyoom/tags | 2026-10-23T01:31:22Z | 423c43617a2a299315180292f43447936f6ddde01efff5baece3fc46ed8b1869 | "\"name\": \"v1.9.0\", \"zipball_url\": \"https://api.github.com/repos/rfjakob/earlyoom/zipball/refs/tags/v1.9.0\", \"tarball_url\": \"https://api.github.com/repos/rfjakob/earlyoom/tarball/refs/tags/v1.9.0\", \"commit\": { \"sha\": \"202d4db0d308ca6478f68de68b46cae34896ddaf\""; "\"name\": \"v1.8\", \"zipball_url\": \"https://api.github.com/repos/rfjakob/earlyoom/zipball/refs/tags/v1.8\", \"tarball_url\": \"https://api.github.com/repos/rfjakob/earlyoom/tarball/refs/tags/v1.8\", \"commit\": { \"sha\": \"62625072ce8671f497a5cea5fc3db63226469093\""; "\"name\": \"v1.7\", \"zipball_url\": \"https://api.github.com/repos/rfjakob/earlyoom/zipball/refs/tags/v1.7\", \"tarball_url\": \"https://api.github.com/repos/rfjakob/earlyoom/tarball/refs/tags/v1.7\", \"commit\": { \"sha\": \"ebaea9526bcee14889b00d83a9dd3d038315cee2\"" | current |
```

The cell was built by slicing the `seat-check.py text` output (not the rendered page), escaping each JSON `"` as `\"`;
`count-c1.py`'s own `quotes_of()` re-parses it back to the three exact slices (checked: `reparsed == qs: True`). No
pipe, no `&`, no zero-width character, no dropped negation inside any quote.

## 3. Quote → teaches-cell mapping

Teaches cell: *"The `mem avail` threshold wording was introduced in v1.8 and is unchanged in v1.9.0, so a v1.7-era
invocation prints `mem <=` and never the contract's threshold line; the action and escalation prefixes are stable
across v1.7–v1.9.0 while their trailing fields change, so the version line, not the action line, identifies the
grammar; percentages are printed through a width-5 field, so a single-digit threshold is space-padded."*

1. `"name": "v1.9.0", … "commit": { "sha": "202d4db0d308ca6478f68de68b46cae34896ddaf"`
   Bears on the anchor clause *"which upstream tag carries 1.9.0"* and on the teaches clause *"unchanged in
   v1.9.0"*: the tag named `v1.9.0` still resolves to the exact commit `202d4db0…` that the row's `main.c`/`kill.c`/
   `msg.h` line numbers and sha256 prefixes were read at on 2026-10-22. Because the wording claims are pinned to that
   tag rather than to a branch, an unchanged tag→commit mapping is exactly what "still current" means for them.
2. `"name": "v1.8", … "commit": { "sha": "62625072ce8671f497a5cea5fc3db63226469093"`
   Bears on *"the `mem avail` threshold wording was introduced in v1.8"*: the v1.8 comparison baseline (`main.c:382`
   and `:384`, `kill.c:230` and `:539` in the anchor) is still an addressable, fixed commit, so the change the teaches
   cell attributes to v1.8 is still measurable against the same bytes.
3. `"name": "v1.7", … "commit": { "sha": "ebaea9526bcee14889b00d83a9dd3d038315cee2"`
   Bears on *"a v1.7-era invocation prints `mem <=`"* and on *"stable across v1.7–v1.9.0"*: v1.7 is still published as
   a tag at a fixed commit (`main.c:326`/`:328`, `kill.c:167`/`:377` in the anchor), the older grammar baseline the
   teaches cell contrasts against.

Why the verdict follows: the only mutable surface of this row is the tag listing itself, and it is unchanged in every
particular the row states — the `v1.9.0` entry still names `202d4db0…`, the tag is still the newest one, and the v1.8
and v1.7 baselines the version comparison uses are still present. Nothing on the page contradicts the teaches cell.
`sending SIGTERM when mem avail`, `sending %s to process` and `escalating to SIGKILL after` are source literals at those
tags and are not visible on this API page, so they neither drift here nor are evidenced here; the tags page bears on
them only by fixing the commit each was read at — [INFERENCE] the tag refs have not been force-pushed, since the
recorded mapping (2026-10-22) and today's live mapping are identical.

## 4. seat-check output

```
$ timeout 300 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-32/seat-check.py row S117 S117.src '<cell from §2>'
sha256=423c43617a2a299315180292f43447936f6ddde01efff5baece3fc46ed8b1869
quotes=3 words=[10, 10, 10] in_copy=[True, True, True]
shared_tokens=['commit', 'ddaf', 'earlyoom', 'tags'] topic_ok=True
live_quotes_ok=True
ROW_CHECK=pass (judge R4 and R5 not checked here)
EXIT=0
```

`live_quotes_ok=True` is the seat-check tool's own fresh `curl` of the URL (`count-c1.fetch`), so the row does not rest
on my saved copy alone. A local simulation of `count-c1.py`'s table parser over the §2 row gives 6 cells with
`hdr_ok=True`, `url_ok=True`, `access_ok=True` (`2026-10-23T01:31:22Z` ≥ `2026-10-23T01:00:00Z`), `sha_ok=True`,
`verdict=current`, `quotes_in_copy=[True, True, True]`.

## 5. Drift details — none

- No redirect: `url_effective` equals the population url; the row's url cell stays
  `https://api.github.com/repos/rfjakob/earlyoom/tags`.
- No newer tag than `v1.9.0` in the live listing, so no "re-open the five earlyoom files at the new tag" action is
  triggered by the `recheck:` line in `corpus/knowledge/userspace-oom-killers-r26.md:3`.
- No `Round32` correction drafted: `drifted` would require an appended correction in
  `corpus/knowledge/userspace-oom-killers-r26.md` (the row's only `used-by` path), and no fact there changed.
- Observed but immaterial to the teaches cell: each entry's `zipball_url`/`tarball_url` now spell the ref as
  `refs/tags/<tag>`; the `commit.sha` field — the only field the row's claims depend on — is unchanged.
- Remaining unknown, unchanged from the row's own anchor: this API page carries no tagger date and no annotated-tag
  object id (`66d78843…`, 2025-09-16T19:09:33Z); those live in the git refs and the releases API (published
  2025-09-16T19:11:03Z), which are outside this row's URL and were not part of this check.

# RevSourceRow — S474 review

Scoped review of `S474` in `corpus/SOURCES.md` (row shape, source opened this round, quote location/length, used-by). Read-only; no edits made.

## 1. S474 row shape — OK, unique

- Row lives at `corpus/SOURCES.md:253`, the last Registry row before `## Paths` (`:255`); exactly one occurrence repo-wide (`grep -c '^| S474 |' corpus/SOURCES.md` → 1).
- Column count matches the header exactly: 12 data cells (id, source, kind, tier, scope, anchor, teaches, status, opened, recheck, used-by).
- Cell values: id `S474`; source `mori AXES calibration criterion — /home/vgpnk/Projects/shokunin/AXES.md`; kind `own-work`; tier `A`; scope `Calibration self-assessment: registry facts match observed committed state`; anchor `AXES.md:15, opened 2026-10-25`; teaches `Self-assessment quality means gaps named honestly, confidence graded, overreach caught; apply that criterion to pinned registry metadata`; status `mined`; opened `2026-10-25`; recheck `180d`; used-by `corpus/lessons/round-46.md`.
- Shape is consistent with sibling rows (S473 above, S472 above it) — pipe-delimited, no missing cell, no duplicate id.

## 2. Source opened this round — yes, plausible and consistent

- Source path `/home/vgpnk/Projects/shokunin/AXES.md` (fleet root) exists, is readable, and line 15 carries the calibration definition:
  `| **calibration** | Self-assessment quality: gaps named honestly, confidence graded, overreach caught | SHONEN.md/SCORECARD entries match observed repo state |`
- Fleet git history: AXES.md was deleted by stray commit `35b91714` (2026-10-25 09:21:14 -0300) and restored by `f47ad6ba` (2026-10-25 09:29:03 -0300). The round-46 wave was created `2026-10-25T13:09:29Z`; the row's `opened=2026-10-25` is consistent with the file being available this round.
- Lesson `corpus/lessons/round-46.md:15` states "S474 opened: `/home/vgpnk/Projects/shokunin/AXES.md:15`, 2026-10-25."
- No `.src` evidence copy exists under `corpus/evidence/` for S474 (the source is own-work/local; sibling own-work rows such as S034/S200 likewise cite local paths or commands rather than shipped copies). Not a defect by itself.
- Note (overlap, not a defect): `S199` (`SOURCES.md:205`) already cites the same document via the kimi-shokunin raw GitHub copy (`skills/shokunin/protocol/AXES.md` at commit `b47dfbe2`), including the same line-15 phrase, mined 2026-10-23. S474 is a distinct source entry (fleet-local file path, own-work) and the two URLs differ, so a duplicate-URL census would not collide; semantically the calibration criterion is second-admitted. S199's scope is capabilities + calibration for SCORECARD rows; S474's scope is "registry facts match observed committed state" for the round-46 pin repair — overlapping but not identical claims.

## 3. Quote location/length — located correctly; minor punctuation note

- Located quote (per lesson `round-46.md:15`): “Self-assessment quality: gaps named honestly, confidence graded, overreach caught.”
- Location `AXES.md:15` verified: the verbatim phrase appears in line 15 of the current file as `Self-assessment quality: gaps named honestly, confidence graded, overreach caught` — **81 characters** (no trailing period in the source; the line continues with ` | SHONEN.md/...`).
- The lesson renders the quote with a closing period (82 chars incl. that punctuation), which is not present in the source text — cosmetic only, the content matches verbatim.
- The `teaches` cell paraphrases ("means" for ":", plus appended application clause); the verbatim quote is recorded in the anchor and the lesson. Acceptable.

## 4. Used-by — resolves to an existing file that names S474

- `corpus/lessons/round-46.md` exists (1503 bytes, Oct 25 10:07, new/untracked this round) and explicitly names S474 twice (`:5` "Source opened this round: S474…" and `:15` "S474 opened: … Located quote: …").
- Caveat: `corpus/README.md` coverage map contains neither `lessons/round-46.md` nor any `S474` reference (grep → 0). This mirrors lane practice for other round lesson files (e.g. `lessons/round-45.md` also absent from the map), so I do not count it as an S474 row defect; if the C3 gate requires every used-by entry to carry a README map row, that dependency would be checked by the C3 counter, not by this row.

## Residual risk / verification gaps

1. "Opened this round" is attested by the lesson and by the file's existence/restore timeline; there is no independent open-receipt artifact to prove *when* the lane read the file. Low risk — the file's line 15 content is stable across the 2026-09-28, 2026-10-16, and 2026-10-25 revisions (identical line 15 bytes in each).
2. S199/S474 semantic overlap (same document, same line-15 phrase, two registry rows). If the lane's policy treats a second admission of the same calibration text as redundant, that is a policy question, not a shape/quote/used-by defect: the two rows cite different source locations and different scopes.

## Verdict

S474 row shape is correct and unique; the source exists and is openable this round; the quote is located at `AXES.md:15` with verbatim content (81 chars; 82 with the lesson's appended period); used-by resolves to `corpus/lessons/round-46.md`, which references S474. No actionable defect found in scope.

# Recheck012 — C1 recheck of S012 (round 32, wave 1)

Seat: MoriR32A2.Recheck012. Lane: /home/vgpnk/Projects/shokunin/mori-shokunin.
Population row: .ufo/waves/round-32/c1-population.json → S012.

## 1. Fetch receipt

- id: S012
- url: https://github.com/systemd/systemd/security/advisories/GHSA-652q-wxr6-h5j6
- accessed: 2026-10-23T01:31:23Z (`date -u +%FT%TZ` immediately after the successful fetch)
- HTTP: 200, no redirect (`curl -w 'URL:%{url_effective}'` returned the same URL; a
  `--max-redirs 0` header probe also returned `HTTP/2 200` with no `location` header)
- byte size: 242120
- sha256: a51157e7c5de1389832e31abe2064c786f971ba1ade9d25e0945b2fc56898052
- scratch copy: /fast/scratch/hyaku/mori-r32/Recheck012/S012.src (bytes saved unchanged;
  first try succeeded, fetch_err_1.txt empty)
- normalised text used for quoting: /fast/scratch/hyaku/mori-r32/Recheck012/S012.norm.txt
  (26687 bytes, produced by `seat-check.py text S012.src`)

Command: `curl -sSL --fail -m 60 <url> -o /fast/scratch/hyaku/mori-r32/Recheck012/S012.src`

## 2. Ready-to-paste Recheck row

```markdown
| S012 | https://github.com/systemd/systemd/security/advisories/GHSA-652q-wxr6-h5j6 | 2026-10-23T01:31:23Z | a51157e7c5de1389832e31abe2064c786f971ba1ade9d25e0945b2fc56898052 | "Local unprivileged users can terminate arbitrary local processes via a systemd-oomd IPC API due to a missing path traversal validation."; "Affected versions >= 250 Patched versions 261 260.3 259.7 258.9" | current |
```

## 3. Quote-by-quote justification

Quote 1 — `Local unprivileged users can terminate arbitrary local processes via a
systemd-oomd IPC API due to a missing path traversal validation.`
- Located in the advisory's `Description` → `Impact` section (normalised text at
  S012.norm.txt, opening "Description Impact Local unprivileged users ...").
- Bears on the teaches cell's "path-validation flaw" element: the page names the cause as
  "a missing path traversal validation" on the systemd-oomd IPC API, and the effect as
  unprivileged users terminating arbitrary local processes. It also bears on the scope
  cell's "varlink arbitrary-SIGKILL vulnerability": the longer report text names the
  world-accessible varlink method `io.systemd.oom.ReportManagedOOMCGroups` and the
  `../` traversal into `/sys/fs/cgroup` (not quoted; just corroboration I read).
- Shared content tokens with teaches+anchor+scope (from seat-check): affected, arbitrary,
  oomd, path, systemd, validation, versions.

Quote 2 — `Affected versions >= 250 Patched versions 261 260.3 259.7 258.9`
- Located in the advisory header/`Packages` block, immediately before `Description`
  (normalised text: `Package systemd-oomd (systemd) Affected versions >= 250 Patched
  versions 261 260.3 259.7 258.9 Description Impact ...`).
- Bears directly on the teaches cell's "bounds which oomd versions contain the ...
  flaw and its fixes": affected is `>= 250`; patched are `261`, `260.3`, `259.7`, `258.9`.
- The `Patches` section then gives one commit per patched version (`v261 ( cde88c4 )`,
  `v260.3 ( 1b2a891 )`, `v259.7 ( 967850c )`, `v258.9 ( a8feb2f )`), confirming the
  fixes element. These parenthesised forms are tag-artifacts with inner spaces, so I did
  not quote them; quote 2 already carries the version bound.
- Also matches the anchor: the publication header reads `bluca published
  GHSA-652q-wxr6-h5j6 Aug 10, 2026`, i.e. 2026-08-10 as recorded in the population anchor.
- Shared content tokens with teaches+anchor+scope: affected, versions (plus oomd/patches
  in the immediately adjacent text; the counter only requires 2 total across the cell).

Verdict `current`: the live page still says exactly what the row's teaches cell asserts —
one advisory (GHSA-652q-wxr6-h5j6, published 2026-08-10) bounds the vulnerable range and
lists the fixed versions/commits for the path-validation flaw in systemd-oomd. Nothing in
the fetched bytes contradicts the teaches, anchor or scope cells. Both consumed-by
statements in `corpus/knowledge/userspace-oom-killers-r12.md` remain accurate: line 1
describes S012 as "advisory published 2026-08-10, patch section", and line 24 says the
GHSA "is adjacency only: patch-state assessment belongs to tsukuroi" — the advisory still
carries patch state, and that knowledge file still does not absorb it.

No drift. No `Round32` correction drafted (verdict is `current`; used-by cell lists only
corpus/knowledge/userspace-oom-killers-r12.md).

## 4. seat-check output

Command:

```
timeout 300 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-32/seat-check.py row S012 S012.src \
  '"Local unprivileged users can terminate arbitrary local processes via a systemd-oomd IPC API due to a missing path traversal validation."; \
   "Affected versions >= 250 Patched versions 261 260.3 259.7 258.9"'
```

Output (verbatim; also at /fast/scratch/hyaku/mori-r32/Recheck012/seatcheck.out):

```
sha256=a51157e7c5de1389832e31abe2064c786f971ba1ade9d25e0945b2fc56898052
quotes=2 words=[20, 10] in_copy=[True, True]
shared_tokens=['affected', 'arbitrary', 'oomd', 'path', 'systemd', 'validation', 'versions'] topic_ok=True
live_quotes_ok=True
ROW_CHECK=pass (judge R4 and R5 not checked here)
```

`live_quotes_ok=True` is the helper's own fresh re-fetch of the population URL, not my
saved copy. Quote lengths 20 and 10 words are inside 3–25. Quotes are pure ASCII, contain
no `&`, no `|`, no zero-width characters, and start/end on whole words.

## 5. Drift details

None. The page had not moved or changed materially between the mined row (2026-10-19) and
this fetch: affected `>= 250`; patched `261`, `260.3`, `259.7`, `258.9`; same four commit
short-hashes; publication date still Aug 10, 2026; severity still Moderate. Kept for the
record but not relied on in the quotes.

## 6. Notes

- Tooling: nothing installed or updated this seat.
- Processes: every command ran under `timeout` (fetch 60 s, seat-check 300 s, header probe
  60 s); no background jobs. The header probe's `curl: (23)` line is the shell pipe closing
  after `head`, not a fetch failure.
- Writes: only this report and /fast/scratch/hyaku/mori-r32/Recheck012/. No git/jj writes.

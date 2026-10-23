# Recheck064 — C1 recheck seat for S064

Fetch: `curl -sSL --fail -m 60 https://git-scm.com/docs/git-rev-parse -o S064.src` → `HTTP=200 URL=https://git-scm.com/docs/git-rev-parse SIZE=122463`, `EXIT=0`.
No redirect: `url_effective` is byte-identical to the population url.
`date -u +%FT%TZ` at the fetch: `2026-10-23T01:31:24Z`.

## (1) Per id

| id | url | accessed | bytes | sha256 | scratch copy |
|---|---|---|---|---|---|
| S064 | https://git-scm.com/docs/git-rev-parse | 2026-10-23T01:31:24Z | 122463 | 64c603545b3f9799cc9525228ba70cf80444a063b32a4be37de2a5ca09b83421 | /fast/scratch/hyaku/mori-r32/MoriR32A2.Recheck064/S064.src |

Normalised text saved beside it: `/fast/scratch/hyaku/mori-r32/MoriR32A2.Recheck064/S064.txt` (34023 bytes, via `seat-check.py text S064.src`, exit 0). Copy is the whole page (ends `</body></html>`).

Live-page anchors checked against the row's anchor cell:
- `S064.src:1330` — `<span class="light d-flex">git-rev-parse last updated in 2.56.0</span>` → matches "page last updated 2.56.0".
- `S064.src:1363` — `<em class="date">2026-09-28</em>` → matches the same date as the anchor cell.

## (2) Ready-to-paste row

```markdown
| S064 | https://git-scm.com/docs/git-rev-parse | 2026-10-23T01:31:24Z | 64c603545b3f9799cc9525228ba70cf80444a063b32a4be37de2a5ca09b83421 | "Verify that exactly one parameter is provided, and that it can be turned into a raw 20-byte SHA-1"; "it is wise to use --end-of-options so that the name argument is not mistaken for another option"; "git rev-parse --verify --end-of-options $REV^{commit} This will error out if $REV is empty or not a valid revision" | current |
```

## (3) Each quote → the teaches-cell fact it bears on

Teaches cell: "Resolve a selector once with --verify --end-of-options and commit peeling, retain the full object id, then separately bind the actual loaded register/correction bytes to blobs at that commit; a hash printer alone does not prove the latter."

- Q1 `"Verify that exactly one parameter is provided, and that it can be turned into a raw 20-byte SHA-1"` (`S064.src:2720-2723`, OPTIONS `--verify`): bears on "Resolve a selector once with --verify" *and* on "retain the full object id" — the option's whole contract is one parameter turned into one raw 20-byte object id, emitted to stdout. It also bears on "a hash printer alone does not prove the latter": the documented output is a hash/object name, nothing about file bytes.
- Q2 `"it is wise to use --end-of-options so that the name argument is not mistaken for another option"` (`S064.src:2735-2737`): bears directly on the `--end-of-options` half of the teaches cell — it is the page's own rationale for separating the untrusted selector from option parsing, which is exactly the ordered `--verify --end-of-options` invocation the cell asserts.
- Q3 `"git rev-parse --verify --end-of-options $REV^{commit} This will error out if $REV is empty or not a valid revision"` (`S064.src:3763-3767`, EXAMPLES): bears on "with --verify --end-of-options and commit peeling" plus "resolve a selector to an existing commit object" — it is the page's canonical one-shot resolution of `$REV` to a *commit* object name (the `^{commit}` peeling operator at `S064.src:2727` and its definition at `S064.src:3273-3279`, `<rev>^{commit}` dereferences recursively until a commit is found), and the trailing clause states the failure mode the cell's scope implies (erroring out when the selector does not resolve).

Why `current`: all three mechanisms the teaches cell names — `--verify` (single-parameter validation), `--end-of-options` (option-injection separation), and `^{commit}` type peeling in the `$REV` example — are present, verbatim and unchanged in wording on the live page, and the page still stops at emitting an object id (`"SHA-1s for valid object names are printed to stdout on success"`, `S064.src:2735`-region). It says nothing that claims byte-level binding of loaded file contents to blobs, so the cell's contrast ("a hash printer alone does not prove the latter") remains the correct reading of this source at scope C2 (selector → existing commit object only). The version/date anchor is still 2.56.0 / 2026-09-28.

Two secondary checks, both consistent: the `--verify` text still requires *exactly one* parameter (no widening to multi-arg), and no "not intended for scripts"/porcelain warning appears that would contradict using rev-parse for resolution (the only `porcelain`/`Plumbing` hit is the documentation section label in the sidebar).

## (4) seat-check output

Command:
`timeout 300 python3 .ufo/waves/round-32/seat-check.py row S064 S064.src '"Verify that exactly one parameter is provided, and that it can be turned into a raw 20-byte SHA-1"; "it is wise to use --end-of-options so that the name argument is not mistaken for another option"; "git rev-parse --verify --end-of-options $REV^{commit} This will error out if $REV is empty or not a valid revision"'`

```
sha256=64c603545b3f9799cc9525228ba70cf80444a063b32a4be37de2a5ca09b83421
quotes=3 words=[18, 17, 18] in_copy=[True, True, True]
shared_tokens=['commit', 'name', 'options', 'verify'] topic_ok=True
live_quotes_ok=True
ROW_CHECK=pass (judge R4 and R5 not checked here)
EXIT=0
```

`live_quotes_ok=True` is the helper's own fresh `curl` of the population url containing all three quotes.

## (5) Drift

None. Verdict `current`; no `Round32` correction is required and none is drafted (R5 does not apply).

## Tooling / bounds

No installs or updates (no package manager touched; host pacman transactions paused and unused). Leaf seat: no subagents, no background jobs, no git/jj writes, no omp invocation. Only files written: this report and `/fast/scratch/hyaku/mori-r32/MoriR32A2.Recheck064/{S064.src,S064.txt}`. All commands wrapped in `timeout` (300 s for the row check, 120 s otherwise); curl capped at `-m 60`; the single curl process exited before the row check ran.

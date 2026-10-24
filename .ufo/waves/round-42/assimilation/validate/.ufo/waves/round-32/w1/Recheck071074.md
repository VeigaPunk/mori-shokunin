# Recheck071074 — C1 recheck seat for S071 and S074

Both ids share one population URL (identical bytes by construction; one saved copy per id as the rule requires).

Fetch: `curl -sSL --fail -m 60 https://kubernetes.io/docs/concepts/architecture/controller/ -o <id>.src` → `HTTP=200 SIZE=509019`, exit 0, first try for both ids (no retries, no bot challenge encountered).
Redirect check: `curl -sSL -o /dev/null -w '%{url_effective} %{http_code} %{num_redirects}'` → `https://kubernetes.io/docs/concepts/architecture/controller/ 200 0` — **no redirect**, url is the population url byte-for-byte.
`date -u +%FT%TZ` at the fetch: `2026-10-23T01:31:24Z` (file mtimes `2026-10-22 22:31:24 -0300` = `2026-10-23T01:31:24Z`, inside the required ≥ `2026-10-23T01:00:00Z` window).
Page revision on the live copy: `<meta property="article:modified_time" content="2024-09-01T01:54:45+03:00">` (`S071.src:6`) and footer `Last modified September 01, 2024 at 1:54 AM PST:` (`S071.src:966`) — matches the rows' anchor cell "page modified 2024-09-01".

**No drift since round 20, by bytes:** the sha256 of today's copy equals the sha256 recorded when the page was last opened on 2026-10-21 (`.ufo/waves/round-20/falsify/ReopenS071.md:5`, `96ad0ef9…`). The page has not changed between the row's last opening and this recheck.

## (1) Per id

| id | url | accessed | bytes | sha256 | scratch copy |
|---|---|---|---|---|---|
| S071 | https://kubernetes.io/docs/concepts/architecture/controller/ | 2026-10-23T01:31:24Z | 509019 | 96ad0ef9661c7a3fff3b360ce9643a6c1bc120bcec52b82385c94481194581cb | /fast/scratch/hyaku/mori-r32/MoriR32A2.Recheck071074/S071.src |
| S074 | https://kubernetes.io/docs/concepts/architecture/controller/ | 2026-10-23T01:31:24Z | 509019 | 96ad0ef9661c7a3fff3b360ce9643a6c1bc120bcec52b82385c94481194581cb | /fast/scratch/hyaku/mori-r32/MoriR32A2.Recheck071074/S074.src |

`cmp S071.src S074.src` → identical (exit 0); `sha256sum` over both → the 64-hex above. Normalised text: `/fast/scratch/hyaku/mori-r32/MoriR32A2.Recheck071074/S071.txt` (31407 bytes, 4252 words, `seat-check.py text S071.src`, exit 0). Copy is the whole page (509019 bytes; HTML head through footer). Empty `S071.fetch.txt` / `S074.fetch.txt` = curl stderr on the successful first try (helper files, not unreachable transcripts).

## (2) Ready-to-paste rows

```markdown
| S071 | https://kubernetes.io/docs/concepts/architecture/controller/ | 2026-10-23T01:31:24Z | 96ad0ef9661c7a3fff3b360ce9643a6c1bc120bcec52b82385c94481194581cb | "These objects have a spec field that represents the desired state."; "The controller(s) for that resource are responsible for making the current state come closer to that desired state." | current |
| S074 | https://kubernetes.io/docs/concepts/architecture/controller/ | 2026-10-23T01:31:24Z | 96ad0ef9661c7a3fff3b360ce9643a6c1bc120bcec52b82385c94481194581cb | "The controller(s) for that resource are responsible for making the current state come closer to that desired state."; "The thermostat acts to bring the current state closer to the desired state, by turning equipment on or off."; "Your cluster could be changing at any point as work happens and control loops automatically fix failures." | current |
```

Both quote cells are copied from the `seat-check.py text` output, not from rendered prose (tags collapse to spaces there; these passages carry no such tag boundary).

## (3) Quote → teaches-cell fact → verdict

### S071 — teaches: "Name the declared set (dispatch members) and the observed set (reports) separately; mori observes the gap and never acts to close it." Scope: "desired-versus-current-state vocabulary only; the page describes acting controllers, not observe-only ones".

- Q1 `"These objects have a spec field that represents the desired state."` — "Controller pattern" section, second sentence (`S071.src:892` h2 `id=controller-pattern`; sentence spans `S071.src:893-894`). Bears on the **declared set** half of the teaches cell: the page names the *declared* thing "desired state" and locates it in a `spec` field — the vocabulary for a declared/dispatch side that is not the observed side.
- Q2 `"The controller(s) for that resource are responsible for making the current state come closer to that desired state."` — same paragraph, third sentence (`S071.src:894-896`). Bears on the **separation** clause: "current state" and "desired state" are named as two distinct quantities, and the page itself puts the gap between them ("making the current state come closer").
- Why `current`: both clauses the row actually sources from this page — the desired/current pair and the naming of the declared side as a spec — are present verbatim and unchanged (byte-identical copy, same 2024-09-01 revision). The second teaches clause ("mori … never acts to close it") is **not** on the page and never was: the same paragraph continues "The controller might carry the action out itself" (`S071.src:896`) and the page elsewhere says controllers "make or request changes where needed" (`S071.src:889`). That is exactly what the row's own **scope** cell disclaims ("the page describes acting controllers, not observe-only ones") and what S074 was raised to record; the observe-only boundary is the lane's, not a claim of this source. Since no page byte changed, this is a pre-existing, already-disclosed scope limit, not drift — `drifted` would fabricate a change and force a false `Round32` correction into `corpus/knowledge/wave-settlement-r20.md` and `corpus/lessons/round-20.md`.
- Residual reading for the judge: a strict reader may hold that clause 2 of S071's teaches cell is unsourced. That reading is already the row's scope cell, and S074 supersedes S071 for it; it does not make the live page stop supporting what S071 was scoped to teach (the vocabulary). Verdict stays `current`, no correction drafted.

### S074 — teaches: "supersedes S071 — name the declared state and the observed current state separately; the page describes controllers that act on the gap, so mori's observe-only stance is the lane's own boundary, not taught here."

- Q1 `"The controller(s) for that resource are responsible for making the current state come closer to that desired state."` (`S071.src:894-896`) — bears on "name the declared state and the observed current state separately" **and** on "controllers that act on the gap": the sentence's predicate is *making the current state come closer*, i.e. acting, with the two states still named distinctly.
- Q2 `"The thermostat acts to bring the current state closer to the desired state, by turning equipment on or off."` — opening example under "Controllers" (`S071.src:886-888`). Bears directly on "the page describes controllers that act on the gap": the canonical control loop is defined by the *act*, not by observation.
- Q3 `"Your cluster could be changing at any point as work happens and control loops automatically fix failures."` — "Desired versus current state" section (`S071.src:932` h2 `id=desired-vs-current`; sentence at `S071.src:934`). Bears on the same clause from the section the anchor names: the loops "automatically fix failures", so the page's stance is action on the gap; nothing on this page licenses an observe-only reader.
- Why `current`: all three propositions of the teaches cell are on the live page — the desired/current pair is named separately, controllers are described as acting on the gap, and there is no observe-only component anywhere on the page (the only observer sentence, "Other control loops can observe that reported data and take their own actions", also ends in action). The page has not changed since the row's last opening (same sha256), so the supersession wording remains accurate.

## (4) seat-check output

Command:
`timeout 300 python3 .ufo/waves/round-32/seat-check.py row S071 S071.src '"These objects have a spec field that represents the desired state."; "The controller(s) for that resource are responsible for making the current state come closer to that desired state."'`

```
sha256=96ad0ef9661c7a3fff3b360ce9643a6c1bc120bcec52b82385c94481194581cb
quotes=2 words=[11, 18] in_copy=[True, True]
shared_tokens=['controller', 'current', 'desired', 'state'] topic_ok=True
live_quotes_ok=True
ROW_CHECK=pass (judge R4 and R5 not checked here)
EXIT=0
```

Command:
`timeout 300 python3 .ufo/waves/round-32/seat-check.py row S074 S074.src '"The controller(s) for that resource are responsible for making the current state come closer to that desired state."; "The thermostat acts to bring the current state closer to the desired state, by turning equipment on or off."; "Your cluster could be changing at any point as work happens and control loops automatically fix failures."'`

```
sha256=96ad0ef9661c7a3fff3b360ce9643a6c1bc120bcec52b82385c94481194581cb
quotes=3 words=[18, 19, 17] in_copy=[True, True, True]
shared_tokens=['controller', 'current', 'desired', 'state'] topic_ok=True
live_quotes_ok=True
ROW_CHECK=pass (judge R4 and R5 not checked here)
EXIT=0
```

`live_quotes_ok=True` is the helper's own fresh `curl` of the population url containing every quote (three independent live checks across the two runs above).

## (5) Drift

None for either id. Both verdicts are `current`; no `Round32` correction is required and none is drafted (R5 does not apply). Not-applicable notes for L1: the page did not move (no redirect), and the 2024-09-01 revision still matches both rows' anchor cells.

## Tooling / bounds

No installs or updates (no package manager touched; host pacman transactions paused and unused; nothing was missing — python3, curl and sha256sum were already present). Leaf seat: no subagents, no background jobs, no omp invocation, no git/jj writes, no harness/settings/MCP/unit edits. Files written only: this report and, under `/fast/scratch/hyaku/mori-r32/MoriR32A2.Recheck071074/`, `S071.src`, `S074.src`, `S071.txt`, `S071.fetch.txt`, `S074.fetch.txt` (duplicated for convenience from the identical `/fast/scratch/hyaku/mori-r32/Recheck071074/` working dir; same sha256). All commands wrapped in `timeout` (300 s for row checks, 120 s otherwise); curl capped at `-m 60`; every curl/python process exited before this report was written.

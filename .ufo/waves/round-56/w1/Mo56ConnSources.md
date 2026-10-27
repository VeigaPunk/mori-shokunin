# Mo56ConnSources — cross-lane SOURCES scan (mori round 56, wave w1)

Scope (seat spec): grep every sibling `corpus/SOURCES.md` for `rfc8259`, for the fleet
driver scripts (`inline.sh` / `shokunin-watchdog.sh`) as a cited source, and for
`watchdog.log` as a cited source in any sibling registry; report every hit with the
sibling's row id (duplicate-url / overlap class), or state the scan found none.
Baseline for "overlap": mori row S544 (`scripts/hyaku/inline.sh` +
`scripts/shokunin-watchdog.sh`, own-work) and S545 (RFC 8259 `.txt` URL), both present
at freeze tip `8be2717b0809281d07dffe83dad424a4859e0747`
(`git show 8be2717b…:corpus/SOURCES.md` → S544 at line 324, S545 at line 325; exit 0).

This is a read-only sibling scan; nothing it reports contradicts the frozen C1/C2
targets. No counter, predicate, control or kill-rule change is proposed anywhere in
this report.

## Coverage of the scan

`find` located one `corpus/SOURCES.md` in each of 20 `*-shokunin` lanes, including
morits own (excluded from sibling tallies). Lanes scanned (19 siblings):
audio, chousa, game-dev-2d, game-dev-3d, kagi, kaidoku, kake, kama, kasegi, kengaku,
kotoba, kotodama, kumitate, lore, mado, revenger, souji, tabi, tameshi, tsukuroi.
All 14 lanes named in the seat spec are covered except `kaika`: there is **no
`/home/vgpnk/Projects/shokunin/kaika-shokunin/` directory** (`ls -d` of the fleet
root; exit 2 on that name only). For completeness, "registry" was also swept
beyond `SOURCES.md`: every `*.tsv` under sibling `corpus/` (incl. `instruments/` and
`knowledge/`), and a `find` for `*registr*`/`SOURCES*` files at depth ≤2 (only
knowledge/prose hits — `SOURCES.md` is the single canonical registry per lane).

## Commands run (verbatim)

```
find /home/vgpnk/Projects/shokunin/*/ -maxdepth 3 -iname 'SOURCES*.md'        # locates every sibling registry
grep -rni 'rfc8259'  /home/vgpnk/Projects/shokunin/*/corpus/SOURCES.md        # primary RFC sweep (contiguous)
grep -rniE 'rfc[ -]?8259' /home/vgpnk/Projects/shokunin/*/corpus/SOURCES.md   # spaced/hyphen variant sweep
grep -rni 'inline\.sh\|shokunin-watchdog\.sh' /home/vgpnk/Projects/shokunin/*/corpus/SOURCES.md
grep -rni 'watchdog' /home/vgpnk/Projects/shokunin/*/corpus/SOURCES.md        # bare 'watchdog' (superset of watchdog.log)
grep -rni 'rfc8259\|watchdog\.log\|inline\.sh\|shokunin-watchdog' /home/vgpnk/Projects/shokunin/*-shokunin/corpus/*.tsv /home/vgpnk/Projects/shokunin/*-shokunin/corpus/instruments/*.tsv /home/vgpnk/Projects/shokunin/*-shokunin/corpus/knowledge/*.tsv
grep -rni 'watchdog\.log' /home/vgpnk/Projects/shokunin/*/corpus/             # non-registry usage count
grep -rni 'inline\.sh\|shokunin-watchdog\.sh' /home/vgpnk/Projects/shokunin/*/corpus/
git -C /home/vgpnk/Projects/shokunin/mori-shokunin show 8be2717b…:corpus/SOURCES.md | grep -n 'S544\|S545'
test -f /home/vgpnk/Projects/shokunin/.ufo/watchdog.log && wc -l …            # live log: 1730 lines, mtime 2026-10-27 11:08 -03:00, exit 0
```

## Result 1 — RFC 8259 in sibling `corpus/SOURCES.md` (9 cited rows across 7 lanes)

Overlap class vs mori S545 (`https://www.rfc-editor.org/rfc/rfc8259.txt`, spec, tier A,
status `mined`, used-by `corpus/knowledge/vote-binding-r56.md, tools/mori-vote-bind.py`):

| Sibling row | File:line | URL form cited | Tier/status | Row scope | Overlap class |
|---|---|---|---|---|---|
| chousa S062 | SOURCES.md:72 | `…/rfc8259.txt` (same URL) | spec A, mined | §3 Values + §4 Objects (duplicate names) | **duplicate-url (exact)** |
| kaidoku S049 | SOURCES.md:55 | `…/rfc8259` (no `.txt`) | spec A, mined | §4 Objects (object member identity) | **duplicate-url (variant)** |
| kake S034 | SOURCES.md:42 | `…/rfc8259.txt` (same URL) | spec A, mined | §3/§4/§6/§9 (duplicates, non-finite constants) | **duplicate-url (exact)** |
| kama S136 | SOURCES.md:148 | `…/rfc8259.txt` (same URL) | spec A, mined | §7 Strings escapes (BMP 6-char `\uXXXX`) | **duplicate-url (exact)**; superseded by S139 |
| kama S139 | SOURCES.md:151 | `…/rfc8259.txt` (same URL) | spec A, mined | §7 Strings (BMP + surrogate pair); row text says "supersedes S136" | **duplicate-url (exact)**; same-lane pair with S136 |
| kengaku S053 | SOURCES.md:75 | `…/rfc8259` (no `.txt`) | spec A, mined | §2 JSON grammar (text = ws value ws) | **duplicate-url (variant)** |
| kengaku S059 | SOURCES.md:81 | `…/rfc8259` (no `.txt`) | spec A, mined | §6 Numbers (extends S053 anchor) | **duplicate-url (variant)**; same-lane pair with S053 — kengaku's own census files flag "S059 duplicate url … across s…" (see below) |
| kotoba S006 | SOURCES.md:19 | `…/rfc8259.txt` (same URL) | spec A, **queued** (not mined) | §4 Objects (duplicate-name semantics) | **duplicate-url (exact)** |
| tameshi S066 | SOURCES.md:75 | `…/rfc8259` (no `.txt`) | spec A, mined | §6 Numbers (NaN/Infinity not permitted) | **duplicate-url (variant)** |

Near-miss (no RFC 8259 source row): `kumitate S104` (SOURCES.md:117) cites RFC 8785
(JCS) and quotes its line 95-97 `"create a canonical representation of JSON [RFC8259]
data"` — a textual mention inside the RFC 8785 quote, not a cited RFC 8259 row.

Non-row `rfc8259` mentions inside sibling SOURCES.md files (narrative/ledger
sections, not cited rows): kaidoku :193 and :207 (round-21/round-25 opening logs),
kake :215 (round-24 opening log), tameshi :317 (S065–S074 ledger note).

`kaika`: lane directory absent — no registry to scan (coverage limit, see Findings).

## Result 2 — fleet driver scripts as a cited source: ZERO sibling hits

`grep -rni 'inline\.sh\|shokunin-watchdog\.sh' */corpus/SOURCES.md` → **no hit in any
sibling registry**; the only `corpus/SOURCES.md` citing them is mori's own S544
(line 324). A wider `grep 'watchdog'` on sibling registries matches only unrelated
text: kumitate :269 (a file named `advisor-watchdog.md`), souji S065/S066 :88–89
(GNU `set -m` and `kill(2)` rows that describe "the census watchdog" semantics —
the watchdog concept, not the fleet driver scripts).

The scripts are nonetheless used fleet-wide as *evidence*, just never registered:
files matching `inline\.sh|shokunin-watchdog\.sh` under sibling `corpus/` —
kumitate 6, tabi 5, kotoba 2, tameshi/mado/kama/kake 1 each (mori 17) — e.g.
`kumitate/corpus/knowledge/round-close-gate.md` (`shokunin-watchdog.sh:44
report_of()`), `tabi/corpus/knowledge/closeout-r11.md` (`shokunin-watchdog.sh:14`
LANES roster), `chousa round-33-verifier-spotcheck.md:52` (`render_prompt`),
`kama round-24-verifier-spotcheck.md:30` (`inline.sh verify kama`).

## Result 3 — `watchdog.log` as a cited source: ZERO registry hits

`grep -rni 'watchdog' */corpus/SOURCES.md` → no `watchdog.log` row in any sibling
`SOURCES.md` (the only row anywhere is mori S544, which names the log's *writers*,
not the log itself). `SOURCES.md`-canonical conclusion: **no sibling registers
`.ufo/watchdog.log` as a source.**

The single non-`SOURCES.md` registry-style hit fleet-wide:
`kasegi-shokunin/corpus/instruments/citation-survival.tsv:1343` —
`~/projects/shokunin/.ufo/watchdog.log	GONE		1		other	1	+CORPUS`
(citation column records the lowercase `~/projects/…` spelling; the live file at
`/home/vgpnk/Projects/shokunin/.ufo/watchdog.log` exists, 1730 lines / 163 869 B /
mtime 2026-10-27 11:08 -03:00 — the GONE class refers to kasegi's recorded citation
form, not the fleet file).

Non-registry usage is heavy: `watchdog\.log` appears in sibling corpus files —
mado 32, kake 31, kama 30, tameshi 29, chousa 28, kumitate 27, kotoba 27,
tsukuroi 24, kotodama 22, kengaku 22, kasegi 20, kaidoku 20, tabi 16, souji 11,
revenger 7, kagi 2 (audio/game-dev-2d/game-dev-3d/lore 0; mori 68 excluded) —
almost all `lessons/round-*-verifier-spotcheck.md` driver digests plus scattered
knowledge/evidence citations. So S544 is the first *registry* row for the driver
log grammar anywhere in the fleet [observed], while its log is simultaneously the
most-cited liveness artifact in sibling verifier spotchecks.

## Sibling lanes with zero hits on all three terms (registry level)

audio, game-dev-2d, game-dev-3d, kagi, kotodama, lore, mado, revenger, souji,
tabi, tsukuroi — 11 lanes; `kaika` — absent. (souji's `watchdog`-word hits on S065/
S066 are concept rows, not watchdog.log or the driver scripts.)

## Consistency with the frozen claims

- C1: S544 stands alone as the fleet's only registry row for `inline.sh`,
  `shokunin-watchdog.sh`, and the watchdog-log grammar — the "second fleet-liveness
  source" ground is supported by observed sibling registries (all zero).
- C2: S545's RFC 8259 is a widely duplicated URL across lanes (9 sibling rows), all
  tier A `spec` — normal fleet behavior for a shared public standard; no sibling
  row covers the C2 scope (JSON string-scalar vote binding), so no scope collision.
  Kama's S139 note that RFC text "does not" name STD 90 is a kama-internal
  correction; S545 does not claim STD 90 — no contradiction.

## UNVERIFIED items

- Whether `kaika-shokunin` ever existed or was renamed: the directory is absent at
  scan time; git history of the fleet root was not inspected for it (out of
  read-only scope for a sibling scan; the seat spec's "if present" clause applies).
- The kasegi `citation-survival.tsv` GONE classification mechanism (row generated
  by kasegi's own instrument; the lowercase-`projects` path in the citation column
  does not resolve on this host, which is the observed, not interpreted, state).

## Findings

- **MED** — `kasegi-shokunin/corpus/instruments/citation-survival.tsv:1343`:
  the fleet's own citation instrument records `.ufo/watchdog.log` with class
  `GONE` (under the `~/projects/shokunin/…` path spelling) while the live log is
  present. A sibling instrument that resolves citations by path case will treat
  the round's own-work source surface (S544's log) as missing. Relevant if any
  census-style seat consumes that instrument fleet-wide. Routed-item material for
  round 57 only; no frozen artifact is touched.
- **LOW** — `kama-shokunin/corpus/SOURCES.md:148,151` (S136/S139) and
  `kengaku-shokunin/corpus/SOURCES.md:75,81` (S053/S059): within-lane
  duplicate-url pairs on RFC 8259; both lanes self-flag (kama "supersedes" in row
  text; kengaku's round-27…35 census files carry "S059 duplicate url" as a W04).
  Pre-existing, self-documented; no action implied for mori.
- **LOW** — `kotoba-shokunin/corpus/SOURCES.md:19` (S006): RFC 8259 row still
  `queued` (opened 2026-10-19) while S545 is `mined`; sibling row status, not
  mori's — recorded for completeness only.
- **LOW** — spec lists `kaika` among sibling lanes: no `kaika-shokunin` directory
  exists at the fleet root; the named list is stale by one lane (or the lane was
  removed). Observed coverage statement stands on the 19 real siblings.
- **LOW** — zero sibling `SOURCES.md` rows cite `watchdog.log`, `inline.sh`, or
  `shokunin-watchdog.sh` despite 348 corpus-file mentions of `watchdog.log` and
  32 files citing the two scripts across 9+ lanes: S544 is confirmed as the only
  registry grounding for the driver surface (supports C1's uniqueness ground; no
  defect).

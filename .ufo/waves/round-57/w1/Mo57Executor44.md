# Mo57Executor44 — C2 arm: counter execution, implementation attack, registry frontier

Scope: frozen round-57 C2 predicate and its counter, plus the SOURCES-registry frontier
(no registry write). Lane repo `/home/vgpnk/Projects/shokunin/mori-shokunin`; worktree at
freeze `618562c72a03dc4d17386b715357f863fd327274`, entering revision
`53e2b4768af93dd2472eb26ecc9b9fdca2e9daf2`. Read-only: no production edits, no commits, no
host remediation, no tool installs.

## Verdict

- **C2 is unmet at both inspected revisions, on both clauses.** The entry
  `corpus/knowledge/watchdog-unclosed-r57.md` does not exist and no `S548` row exists in
  `corpus/SOURCES.md`. The counter's `source=bad` is a true negative for this state, not an
  artifact of a missing file read.
- **The frozen C2 counter cannot certify the predicate it names.** It is satisfiable by a
  fabricated entry with zero located quotes (variants A/C/K below), by the *negation* of the
  required statement (variant I), by a `source:` line naming a different row (variant E), and
  by an S548 row whose status is `queued` when any other registry row says `mined` (variant L).
  A future green C2 would therefore not evidence "eight located claims" or "a pairing count
  rather than a present-running count"; closure must inspect the source copy itself.
- **No source was opened in round 57 at the freeze.** The registry's newest row is `S547`
  (`corpus/SOURCES.md:327`, opened 2026-10-27, round-56 own-work), there is no round-57 search-log
  entry, no `corpus/evidence/sources-r57/` copy directory and no `corpus/lessons/round-57.md`.
  The in-scope authority that *would* ground the eight `unclosed` statements is
  `tools/mori-driver-liveness.py` at a pinned revision (own-work), because S544/S547 ground only
  the log-line grammar, not the pairing semantics.

## Executed commands and exact output (lane root, no wrapper)

```
$ python3 .ufo/waves/round-57/count-c2.py 53e2b4768af93dd2472eb26ecc9b9fdca2e9daf2
C2=unmet claims=0 source=bad rev=53e2b4768af93dd2472eb26ecc9b9fdca2e9daf2
exit=1
$ python3 .ufo/waves/round-57/count-c2.py 618562c72a03dc4d17386b715357f863fd327274
C2=unmet claims=0 source=bad rev=618562c72a03dc4d17386b715357f863fd327274
exit=1
$ python3 .ufo/waves/round-57/count-c1.py 53e2b4768af93dd2472eb26ecc9b9fdca2e9daf2
C1=unmet rows=0 evidence=bad rev=53e2b4768af93dd2472eb26ecc9b9fdca2e9daf2
exit=1
$ python3 .ufo/waves/round-57/count-c1.py 618562c72a03dc4d17386b715357f863fd327274
C1=unmet rows=0 evidence=bad rev=618562c72a03dc4d17386b715357f863fd327274
exit=1
$ git cat-file -e 618562c72a03dc4d17386b715357f863fd327274:corpus/knowledge/watchdog-unclosed-r57.md
fatal: path 'corpus/knowledge/watchdog-unclosed-r57.md' does not exist in '618562c...'
exit=128
$ grep -c '| S548 |' corpus/SOURCES.md          # 0
$ git show 53e2b47...:corpus/SOURCES.md | grep -c '| S548 |'   # 0
$ ls -d corpus/evidence/sources-r57             # No such file or directory
$ ls corpus/lessons/round-57.md                 # No such file or directory
```

These reproduce `controls.txt` byte for byte for C1/C2 at the entering revision.

## Counter implementation inspection — `.ufo/waves/round-57/count-c2.py` (17 lines)

| # | Line | Defect |
|---|---|---|
| D1 | `count-c2.py:14` | `quote_ok=all("`" in x and "`" in x for x in claims)` — the two clauses are identical, so one backtick anywhere passes; no closing span, no quote text, no location. |
| D2 | `count-c2.py:12` | `x.startswith("| K")` counts a table *header* row such as `| Key | \`Quote\` |` as a claim; eight rows need not be eight claims. |
| D3 | `count-c2.py:13` | `"S548" in entry and "| S548 |" in registry and "mined" in registry` — the entry binding is a bare substring (not the `source:` line), and `mined` is a whole-file substring, not S548's own status cell. |
| D4 | `count-c2.py:15` | The contract's "opens with `source:`, `verified-at:`, `recheck:`" clause is never checked; only `len(claims)==8`, `source_ok`, `quote_ok`, `"pairing count" in entry`. |
| D5 | `count-c2.py:8-15` | No source copy is read and no quote is resolved to a line/word range, so "located quote in the source copy" is structurally unverifiable by this counter. |
| D6 | `count-c2.py:15` | `"pairing count" in entry` is polarity-blind: "This is **not** a pairing count; unclosed is a present-running count." passes. |
| D7 | `count-c2.py:14` | `all()` over an empty list is `True`; the vacuous pass is masked only by `claims==8`. |
| D8 | `count-c2.py:13` | No check that the cited row is *newly opened this round* (opened date, anchor, copy path, used-by). |

The counter hardcodes the repo path at `count-c2.py:4`, so fixture testing required a copy with
that one line changed; the lane counter itself was not modified (verified by `diff`, below).

## Counterexamples (fixtures only under scratch; explicit `git -C`)

Scratch root `/fast/scratch/hyaku/mori-r57/Mo57Executor44/`, fixture repos `fx` and `fx2`.
Test copy differs from the frozen counter in exactly one line:

```
$ diff .ufo/waves/round-57/count-c2.py count-c2-fixture.py
4c4
< R=sys.argv[1]; repo="/home/vgpnk/Projects/shokunin/mori-shokunin"
---
> R=sys.argv[1]; repo="/fast/scratch/hyaku/mori-r57/Mo57Executor44/fx"
```

| Variant | Fixture content | Output | Exit | Defect shown |
|---|---|---|---|---|
| A | `source:`/`verified-at:`/`recheck:` + 8 rows `\| K1 \| \`a\` \|` … `\| K8 \| \`h\` \|`; one fabricated `S548 … mined` row; **no source copy, no line locations** | `C2=met claims=8 source=ok quotes=ok rev=e9252aa…` | 0 | D1/D5: "eight located claims" accepted with zero locations |
| C | 8 rows each `\| K1 \| \` \|` (single unpaired backtick, no quote text) | `C2=met claims=8 source=ok quotes=ok rev=0227518…` | 0 | D1 tautology |
| K | header `\| Key \| \`Quote\` \|` + only **7** claim rows | `C2=met claims=8 source=ok quotes=ok rev=9fb2e57…` | 0 | D2 claim-count inflation |
| E | `source: S547 (not the new row)`; body text `S548 is not cited here.` | `C2=met claims=8 source=ok quotes=ok rev=5418f93…` | 0 | D3 source binding is a substring, not the `source:` line |
| L | `S548 … queued` row + unrelated `S547 … mined` row | `C2=met claims=8 source=ok quotes=ok rev=73dbaf6…` | 0 | D3 `mined` is not row-scoped |
| I | `This is not a pairing count; unclosed is a present-running count.` | `C2=met claims=8 source=ok quotes=ok rev=70894fd…` | 0 | D6 polarity-blind |
| D (control) | variant A with `pairing count` removed | `C2=unmet claims=8 source=ok quotes=ok` | 1 | substring check is real but only lexical |
| G (control) | single-row registry, `S548 … queued`, no other `mined` | `C2=unmet claims=8 source=bad quotes=ok` | 1 | negative control for D3 |
| B (control) | headers removed (also removes the `S548` string) | `C2=unmet claims=8 source=bad quotes=ok` | 1 | header absence is not independently detected |

## Frontier: SOURCES registry state (no write)

- Registry rows end at `S547` (`corpus/SOURCES.md:327`); 320 `| S…` rows, 393 lines. `S544`
  (`:324`) and `S547` (`:327`) are round-56 own-work rows (driver log grammar; round-56 Gate
  record `corpus/lessons/round-56.md:13-23`). No `S548` row at either revision.
- Search log's newest entries are `Round 53 bounded search` and its addendum
  (`corpus/SOURCES.md:379-380`); there is **no** round-54, -55, -56 or -57 bounded-search entry
  (rounds 54–56 rows were logged in their lesson Gates instead, e.g.
  `corpus/lessons/round-56.md:11-33`). Rounds 38/39 entries sit after `## Leads (unopened)`
  (`:391,:393`) — pre-existing ordering, noted only.
- Therefore the contract's "cites a newly opened source row" has no referent yet: no copy
  directory (`corpus/evidence/sources-r57/` absent), no registry row, no round-57 lesson Gate.
  The frontier is **open, not satisfied**; absence here is not evidence about any other tree.

### What an in-scope source for these claims would have to be

The eight C2 statements are about the *pairing algorithm*, and that algorithm lives in
`tools/mori-driver-liveness.py`, not in S544/S547 (which ground only the line grammar):

- `tools/mori-driver-liveness.py:34-35` — docstring: "`unclosed` = launches with no
  same-(lane,round,attempt) complete — a pairing count, not a failure claim".
- `:114` key starts as `(round, None)`; `:127-129` an attempt-bearing launch keys
  `(round, attempt)`; `:133` every launch appends one key; `:173` `unclosed = len(open_launches)`
  (a **list**, so repeated identical launches each count).
- Asymmetry that any honest claim set must state: `complete` closes the attempt-specific key
  else the bare `(round, None)` key (`:116-120,:139-143`); `wrap` closes only the bare key
  (`:144-150`); `lane-dead-no-report` drops **every** key of that round (`:157`);
  `launch-fail` closes nothing (`:158-163`).
- The round-56 note's wording "`unclosed` (launches with no same-round close)"
  (`corpus/knowledge/driver-liveness-r56.md:22`) is looser than the code's per-attempt pairing;
  a round-57 entry repeating it would be a source/code mismatch.
- Receipt cross-check: mori row `launches 66 / completes 39 / deads 17 / wraps 0 / launch_fails 0
  / in_flight true / unclosed 10`, log `lines 1728, malformed 0, other_lines 121`
  (`.ufo/waves/round-56/evidence/driver-liveness-live.txt`, first JSON object). `unclosed 10`
  beside a boolean `in_flight` is the concrete distinction from a present-running count.

## Cross-arm adjacency (C1; owned by Mo57Executor45, reported not claimed)

`.ufo/waves/round-57/count-c1.py:10` takes `split("## Capabilities", 1)[1]` — the **first**
section only. `SCORECARD.md:596` is the stale `— none yet —` placeholder table (it closes at
`## Saturation`, `:604`); the current register table is at `SCORECARD.md:1951`, and its own prose
says it supersedes that placeholder. Fixture `fx2` with two well-formed rows
(`driver-liveness`, `vote-binding`, each `.ufo/waves/round-56/...` and `| 56 |`) in the register
table still yields:

```
C1=unmet rows=0 evidence=bad rev=68b577a9364070081c9033e08b5c3a4502e522b9
exit=1
```

So C1 as frozen is unmeetable by editing the register table; only editing the stale placeholder
would satisfy it. Test copy again differed only in the `repo` line. This is the round-56 routed
defect; I did not edit `SCORECARD.md` or the counter.

## Advisory counter hardening (no edits made)

1. Require the three header lines as the file's first three lines (`source:` must name the row).
2. Require exactly eight rows matching `^\| K[1-8] \|` with two backtick spans each, and resolve
   each quote as a substring of the cited copy at a stated line/word range; reject duplicates.
3. Parse the registry row for `S548` alone and read its `status` cell and `opened` date; require
   `mined` in that row and `opened` equal to the round's date; require the copy path to exist.
4. Replace the lexical `pairing count` test with a sentence-level requirement that rejects a
   negated form (or check the exact predicate sentence), so variant I fails.

## Evidence boundaries, risks, blockers

- Snapshot at freeze `618562c`; wave-1 seats may add the entry/row later in this same round, so
  this is an inspected state, not a prediction. No other tree or branch was consulted.
- No network use; no external source was re-opened; no provider/liveness inference was drawn
  from any missing report.
- `S548` is the identifier the frozen counter asserts; whether that is the lane's intended next
  id is a convention question I did not decide.
- No production edits, no commits, no pacman, no tool installs. `git status --porcelain` in the
  lane shows only the pre-existing untracked `.ufo/waves/round-57/` wave files.
- Scratch fixtures and the two counter copies were removed after the runs above; all outputs are
  transcribed verbatim here. Blocker: none.

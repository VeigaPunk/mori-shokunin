# Mo58Simplifier64 — C2 source grounding (driver-liveness event classes)

Seat role: simplifier (source-grounding test). No production, corpus, registry,
SCORECARD, LOG or lane-VCS edits; no fleet/sibling writes.

Pinned input: `corpus/knowledge/driver-events-r58.md` snapshot
sha256 `e7fc469cf4ffd86a6ba14e8b6e2f66ec6366e46f853b0733553ee414c81a9e55`
(19 lines, mtime 2026-10-27 14:29:36, **untracked** at reading).
Pinned source: `git show fe8801120a67c1a6b8899d7d0423839caa09e7d0:tools/mori-driver-liveness.py`
sha256 `6b3dba74c639190e7e96b6bed8e6ac8f285a51ce6d910fbe92e6dd39bf7be997`, 479 lines;
`corpus/evidence/sources-r58/mori-driver-liveness.py` and the working-tree tool have
the same sha256, so cited line numbers are identical in copy and tool.

## Verdict

**No falsified event-class statement.** All eight statements describe behavior the
frozen parser actually exhibits. One phrase is unsupported wording (K7 "reason
shape"), two clauses rest on uncited lines (K3 consequence, K4 contrast), and one
**mechanical blocker** makes the entry score `claims=0` under the frozen counter as
written (see Blockers).

## Blocker (actionable) — K-line shape is off the frozen counter grammar

`count-c2.py` matches claim lines with
`^- \*\*K(\d+)\*\*.*\((tools/mori-driver-liveness\.py):(\d+)\)`; the entry writes
`- **K1 — title.**`, i.e. text sits between `K1` and the closing `**`. The frozen
regex matches **0** of the 8 claim lines (its own selftest fixture uses
`- **K1** …`).

Scored in an isolated scratch git fixture (entry + pinned copy + tool + copy of
`corpus/SOURCES.md`, fixture rev `f36acf47`):

```
C2=unmet claims=0 located=0 copy=ok tree=ok rows=ok sources=ok failed=claims rev=f36acf47f97ab59fdd1f3ee4570f33ea65da5693
exit 1
```

Pure format rewrite `- **K<n> — ` → `- **K<n>** — ` (no content change, fixture rev
`1e290daa`, entry sha256 `e634e9fa0a70a6c1b323b77022ba0384a12f3bda9cd1bcd0398cee26640df120`):

```
C2=met claims=8 located=8 copy=ok tree=ok rows=ok sources=ok failed=none rev=1e290daab4d693c69294c1b0fa6393eb9dce5967
exit 0
```

So the content passes the predicate; the bold-title form alone blocks it. Fix the
K-line shape before landing and re-score at the landed tip.

## Per-statement grounding (frozen source, line numbers verified)

| Claim | Cited line | Verdict |
|---|---|---|
| K1 L101 | `other_lines += 1  # ts-first driver prose (steer, watchdog tick, ...)` | **Supported.** Skip is L102; both the `malformed` and the lane-event exclusions hold (L96 ordered before L99). Live corroboration: 1760-line `.ufo/watchdog.log` → `malformed=0`, `other_lines=121`, and every other_line is ts-first `steer …` / `watchdog tick …`, so the quoted comment's examples are accurate for the committed log. |
| K2 L103 | `ts_tok, event, lane, round_s, rest = m.groups()` | **Supported** for the five-field split. The "later branches validate the rest" clause is L122-L163, outside the cited line (true, but uncited). |
| K3 L123 | `m2 = LAUNCH_REST_RE.match(rest)` | **Supported.** Rejection path is L124-L126; empirical: `launch mori round=3 bogus=1` → `malformed`, `launches` unchanged. |
| K4 L135 | `m2 = COMPLETE_REST_RE.match(rest)` | **Supported.** The attempt-key contrast is grounded at L19-L21 and L139-L140, not at L135. Empirically confirmed: `launch … round=3; hyaku-inline attempt=1` and `complete … round=3 attempt=1` are both malformed (fx2), so neither form crosses grammars. |
| K5 L145 | `if not WRAP_REST_RE.match(rest):` | **Supported.** `wrap mori round=6 ` (trailing space only) → malformed even though `LINE_RE` matched (fx2). |
| K6 L152 | `if not DEAD_REST_RE.match(rest):` | **Supported.** Bare `lane-dead-no-report mori round=4` (no retry suffix) → malformed, `deads` unchanged (fx2). |
| K7 L159 | `if not LAUNCHFAIL_RE.match(rest):` | **Partly unsupported wording.** `LAUNCHFAIL_RE = ^ :: (.*)$` checks only the ` :: ` separator; the reason is an unconstrained `.*`. `launch-fail mori round=3 ::    ` (spaces-only reason) is **accepted**: `malformed=0, launch_fails=2` (fx4). "…and reason shape" is not enforced; only the separator is. |
| K8 L96 | `if parse_ts(first) is None:` | **Supported.** Non-ISO first token (`steer mori toward next round`) lands in `malformed` examples, not `other_lines` (fx). |

No contradiction found between the entry and the pinned copy, and no claim is
falsified by any fixture I ran.

## Unclaimed load-bearing behavior (grounding gaps, not defects)

1. Rest validation runs **after** lane/round registration (L109-L113): a malformed
   event line still creates the lane row and adds its round. fx3 (single line
   `2026-… launch mori round=3 bogus=1`) → `malformed=1`,
   `lanes.mori = {launches:0, rounds_seen:1}`. "Rejected" in K3-K7 is counter-only;
   the entry never says otherwise, but a reader may assume the line is inert.
2. A ts-first line with irregular spacing (`2026-…  launch mori round=7 pgid=9`,
   two spaces) is `other_line`, not `malformed` (fx2: `other=1`). So `other_lines`
   is not strictly "prose"; it also absorbs malformed-looking event lines whose
   whitespace defeats `LINE_RE`.

## Simplifier finding — duplicate authority (report-only)

All eight statements restate `corpus/knowledge/driver-liveness-r56.md` § "The frozen
grammar (S544)" one-for-one (five rest grammars, the other_line rule, the malformed
rule). The r58 entry adds per-line locators, not new semantics. That entry is
registry-bound and cross-referenced (`corpus/SOURCES.md:324` S544 used-by;
`corpus/README.md:345,800`; `corpus/lessons/round-56*.md`), so it must not be removed
or superseded in place. Recommendation: have the r58 entry open with a one-line
deferral to r56 as the grammar authority instead of presenting a second grammar
prose authority.

Tradeoff: the frozen C2 predicate requires ≥8 located claims, so collapsing the five
per-event claims into one general claim this round would drop below the predicate —
the duplication is a predicate artifact, not a free deletion.

## Dead weight in the frozen tool (deletion candidates; NOT applied)

1. **L104-L107 unreachable.** `ts_tok` is necessarily the same token as `first`
   (`LINE_RE`'s `^(\S+) ` cannot span the space-delimited first token), so
   `parse_ts(ts_tok)` cannot be `None` after the L96 check. Instrumented scratch copy
   of the frozen file: 0 hits over the 1760-line live log and a 336-case fuzz of
   timestamp/event/rest variants. `ts = parse_ts(first)` could replace both calls.
2. **`row["attempts"]` is write-only.** Populated at L112 (`"attempts": {}`) and
   L129 (`setdefault`), never read; `parse_log` rebuilds its output dict at L164-L175
   without it — observable: returned lane rows have no `attempts` key.
3. **Redundant double `parse_ts`** of the same token (L96, L104) — same fix as (1).

Tradeoff / why deferral is correct: any edit to `tools/mori-driver-liveness.py` this
round breaks the C2 counter's `sha256(copy) == sha256(tool)` binding for the frozen
pin. These deletions belong to a later round that re-pins the copy; they are listed,
not performed.

## Bounded method

- Read the frozen `contract.md` and `count-c2.py`; materialized
  `git show fe880112…:tools/mori-driver-liveness.py` into scratch (sha256 verified)
  and read all 479 numbered lines; extracted each K-line's quoted span and cited line
  number with the counter's own `KLINE` regex and confirmed substring identity.
- Empirical: four crafted fixtures under scratch run through the frozen tool
  (`--fixture`, `--now`), plus the live fleet log through an instrumented copy for the
  dead-branch probe.
- Counter scored twice in a throwaway git repo at an explicit scratch path
  (`git -C` asserted, `rev-parse --show-toplevel` == fixture dir), entry + copy +
  tool + `SOURCES.md` only.
- No `lsp` device is mounted in this session (`xd://lsp` absent), so no semantic
  references/diagnostics were available; evidence here is direct source inspection
  plus execution, and no deletion was claimed on semantic-caller grounds.
- Scratch `/fast/scratch/hyaku/mori-r58/Mo58Simplifier64` cleaned after the receipts
  above were transcribed; disk-guard green before and after (33% used on
  `/fast/scratch/hyaku`, 553G free). No pacman, no installs, no unverified scripts.

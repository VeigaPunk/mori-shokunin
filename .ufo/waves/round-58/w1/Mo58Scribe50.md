# Mo58Scribe50 — C2 source grounding (quote-vs-line audit of the proposed depth entry)

Seat: `Mo58Scribe50` (scribe/leaf, no dispatch). Scope: reopen `tools/mori-driver-liveness.py`
at freeze revision `fe8801120a67c1a6b8899d7d0423839caa09e7d0` and decide, per proposed
event-class statement (K1–K8 in the draft `corpus/knowledge/driver-events-r58.md`), whether
the statement is actually supported by the line it cites. Draft/review note only: no corpus,
registry, counter, lesson, or VCS mutation in the lane.

Freeze `fe8801120a67c1a6b8899d7d0423839caa09e7d0`; entering `b783d0b892637ce8d20f188cad20e4d8913ca635`;
lane `HEAD` observed at audit time `4272736cfc5147586e1543413772f80daf44b04b` (`round-58: freeze
validated w1 dispatch payload`). All reads below are `git show <rev>:<path>` or worktree reads;
the only writes were a throwaway fixture under scratch.

## Behavior (what was done, in order)

1. Read frozen `contract.md`, `count-c1.py`, `count-c2.py`; took the C2 predicate and the
   counter's claim-line grammar as fixed.
2. Extracted the tool at the freeze revision:
   `git show fe8801120…:tools/mori-driver-liveness.py` → 479 lines,
   sha256 `6b3dba74c639190e7e96b6bed8e6ac8f285a51ce6d910fbe92e6dd39bf7be997`.
   Identity chain confirmed: freeze blob == worktree `tools/mori-driver-liveness.py` ==
   worktree `corpus/evidence/sources-r58/mori-driver-liveness.py` (same sha256, all three).
3. Read the draft entry (worktree, untracked): 8 K-lines citing lines 96, 101, 103, 123, 135,
   145, 152, 159 of the frozen tool.
4. For each K-line: (a) matched the cited line number against the frozen copy, (b) checked the
   backticked quote is a byte substring of the cited line, (c) re-read the surrounding ±6 lines
   to judge whether the *prose* statement (not just the quote) is supported.
5. Behavioural cross-check of each claim by importing the frozen tool (read-only) and feeding
   one synthetic driver line per claim through `parse_log`; `parse_log` touches no files.
6. Falsification probe of the frozen counter itself on a scratch fixture repo that mirrors the
   lane layout (`.ufo/waves/round-58/count-c2.py` copied byte-for-byte from the freeze rev,
   sha256 `aab888ad787964f7a153d64d85dafa58f652f977e21e22eaa492706a691010d3`), carrying the
   draft entry, the pinned copy, the tool and the worktree `SOURCES.md`.

## Gates / controls observed

| Control | Result |
|---|---|
| Before-state (contract §C2 control) | At `fe8801120…`: entry **ABSENT**, pinned copy **ABSENT**, counter **present**. `git cat-file -e` confirms all three. Matches the recorded `C2=unmet entry=absent` before-control. |
| Copy/tree identity | `sha256` of the pinned copy == `sha256` of the tool == `6b3dba74…be997` (worktree and freeze rev). Counter prints `copy=ok tree=ok`. |
| Registry row | Worktree `corpus/SOURCES.md` holds exactly one `| S550 ` row (`:330`): `cells[8]=mined`, `cells[11]=corpus/knowledge/driver-events-r58.md` → `rows=ok`. Row count 322 (freeze/enter) → 323 (worktree), matching the census expectation in the contract. |
| Frontmatter arm | `source: S550`, `verified-at: 2026-10-27`, `recheck:`, `coverage-map:` all present (entry lines 1–4) → `sources=ok`. |
| Gate quote (contract §2b) | The lesson `corpus/lessons/round-58.md:16` `## Gate` carries the located quote `other_lines += 1  # ts-first driver prose (steer, watchdog tick, ...)`; verified byte substring of frozen line 101. |
| Disk guard | `/fast/scratch/hyaku` 32% used, 552.8 G free at start; no ENOSPC. |
| Tool install/update | None. No `pacman`, no new tool, no version change. |

## Per-claim grounding verdict (against the frozen tool)

Quote-location column is my own replication of the counter's located rule (span len ≥ 12 and
substring of copy line L), using a diagnostic regex that tolerates the draft's header shape so
the content can be judged independently of finding F1.

| Claim | Cited line | Frozen line text (head) | Quote located | Statement supported by the line? |
|---|---|---|---|---|
| K1 | 101 | `other_lines += 1  # ts-first driver prose (steer, watchdog tick, ...)` | yes (69 ch) | Yes — lines 99–102: `LINE_RE` miss after a successful `parse_ts(first)` increments `other_lines` and `continue`s; `_bad` is not called. Probe: ts-first `steer …` → `malformed=0 other=1 rows={}`. |
| K2 | 103 | `ts_tok, event, lane, round_s, rest = m.groups()` | yes (47 ch) | Yes — `LINE_RE` (`:54-55`) has exactly 5 capture groups; `rest` is then validated per branch at 123/135/145/152/159. |
| K3 | 123 | `m2 = LAUNCH_REST_RE.match(rest)` | yes | Yes — 123–126 reject to `_bad` before `row["launches"] += 1` at 130. Probe: `launch … bogus=1` → `malformed=1`, launch counter 0. |
| K4 | 135 | `m2 = COMPLETE_REST_RE.match(rest)` | yes | Yes — 135–138 reject before `completes` at 141. Probe: `complete …; bogus` → `malformed=1`, completes 0. The clause "launch's and completion's attempt keys are not accepted by a generic suffix parser" is a cross-line comparison, correctly grounded in two distinct regexes (`:56-58` vs `:59`). |
| K5 | 145 | `if not WRAP_REST_RE.match(rest):` | yes | Yes — 145–147 reject before `wraps` at 148. Probe: `wrap … landed extra` → `malformed=1`, wraps 0. (Note the grammar also admits the verb `complete`; the claim does not deny it.) |
| K6 | 152 | `if not DEAD_REST_RE.match(rest):` | yes | Yes — 152–154 reject; `DEAD_REST_RE` = `^; retry same round(?: \((.*)\))?$`; probe `; retry later` → `malformed=1`, deads 0. |
| K7 | 159 | `if not LAUNCHFAIL_RE.match(rest):` | yes | Mostly — the branch and the malformed routing are exact; but see F3 on "reason shape". The `else` branch is reachable only for `launch-fail` because `LINE_RE`'s alternation (`:55`) is closed to five names; verified `respawn …` never reaches it (probe → `other=1`, `malformed=0`). |
| K8 | 96 | `if parse_ts(first) is None:` | yes | Yes — 96–98 `_bad(raw)` then `continue`; no lane row is created. Probe: `not-a-timestamp launch …` → `malformed=1 rows={}`. |

Every cited line number is inside the span S550 claims (`parse_log` lines 95–163); no citation
falls outside the frozen function. No claim in K1–K8 is contradicted by its cited line.

## Findings

**F1 — BLOCKING (mechanical): the draft's K-line headers do not match the frozen counter's
claim grammar, so the entry currently scores `C2=unmet claims=0`.** The frozen regex
(`count-c2.py:37`) is
`^- \*\*K(\d+)\*\*.*\((tools/mori-driver-liveness\.py):(\d+)\)` — it requires the bold span to
close immediately after the number (`**K1**`). The draft writes `- **K1 — unmatched timestamped
prose is separate from a lane event.**` (bytes: `- **K1 ` + U+2014, verified with `od -c`), i.e.
`K1` followed by ` — ` before the closing `**`, so `\*\*` fails and the line is not counted.
The counter's own selftest fixture shows the intended shape: `- **K{i}** the parser keeps event
class {i}. …`. Falsified end-to-end with the frozen counter bytes on a scratch fixture:

- draft as written, rev `29bebe883db6144875b118719b4c0ea1692aa003`:
  `C2=unmet claims=0 located=0 copy=ok tree=ok rows=ok sources=ok failed=claims`, exit 1.
- header-only repair (`**K<n> —` → `**K<n>** —`, nothing else changed), rev
  `7edf30ed478eb22b27469b042796926621d49051`:
  `C2=met claims=8 located=8 copy=ok tree=ok rows=ok sources=ok failed=none`, exit 0.

So the depth content is sound and the only reason the claim would not land is a title-format
mismatch against immutable counter bytes. Because the counter is frozen (kill rule), the entry
must be reshaped, not the counter. Note the repaired count is exactly 8 (`claims>=8` threshold,
zero margin).

**F2 — Counter weakness (report only; counter bytes are frozen): the located arm is satisfiable
by a bare identifier, so a fabricated code quote still scores `located`.** For K3–K7 each line
contains both a constant-name span (e.g. `LAUNCH_REST_RE`, 14 ch ≥ 12) and the code quote; the
`any(...)` in `count-c2.py:88-89` accepts the identifier alone. Falsified: with K3's code quote
replaced by `` `m2 = FABRICATED_RE.match(nothing)` `` and the name span kept, rev
`ae8a41461882948f28fb7fbf505894609dee7872` still prints
`C2=met claims=8 located=8 copy=ok tree=ok rows=ok sources=ok failed=none`, exit 0. This is the
same false-green class as round-57 routed defect 2, only narrowed — a quote-bound control that a
mined row plus a visible identifier can still satisfy. Recorded for the no-harm reviewer and the
lesson's `## Gate`; no counter change is proposed by this seat.

**F3 — Precision (non-blocking): K7 overstates "reason shape".** `LAUNCHFAIL_RE` is
`^ :: (.*)$` (`:61`); it enforces the ` :: ` separator but accepts an empty or arbitrary reason.
Probe: `2026-10-27T10:00:00+00:00 launch-fail alpha round=3 :: ` → `malformed=0`,
`launch_fails=1`. Suggested wording: "requires the ` :: ` separator and admits any (possibly
empty) remainder — the reason text is not validated." "not counted as a launch-fail event" on a
separator miss is accurate (`… round=3:: boom` → `malformed=1`, `launch_fails=0`).

**F4 — Precision (non-blocking): K1's headline gloss says "prose", but the bucket also swallows
malformed event lines.** Non-numeric round tokens and unknown event names never reach a branch:
`wrap alpha round=x landed` → `other=1, malformed=0`; `respawn alpha round=3` → `other=1,
malformed=0`. The K1 body ("a timestamp-first line that does not match the event grammar") is
true as written; only the closing parenthetical "driver prose" invites a reader to think the
bucket holds prose exclusively. Optional sharpening: "ts-first lines whose token sequence fails
`LINE_RE` — driver prose, and also event-shaped lines with a mangled `round=` field or an
unknown event name."

**F5 — Convention (non-blocking): frontmatter precedes the H1.** Every neighbouring entry puts
`# title` first, then `source:` / `verified-at:` / `recheck:` / `coverage-map:` (see
`corpus/knowledge/c1s-cwd-r43.md:1-5`, `census-cgroup-levels-r45.md:1-8`,
`driver-liveness-r56.md:1-5`). The draft has `source: S550` on line 1 and the title on line 6,
so the file's first line is not a heading — it renders as body text above the title. The counter
is substring-based and passes either way.

**F6 — Convention (non-blocking): `recheck` disagrees between entry and registry.** Entry line 3
is `recheck:` running `.ufo/waves/round-58/count-c2.py R`; row S550's recheck cell is `90d`. One
value should win (the counter only requires the `recheck:` key to exist).

**F7 — Observation: the round-58 lesson already carries the Gate quote**, so contract §2b's
"byte-faithful Gate quote" is met by `corpus/lessons/round-58.md:16`, not by the S550 row (whose
`anchor` cell carries a line range and the sha256 but no quoted text). Verified byte-identical
to frozen line 101. Not a defect; recorded so the §2b check is not looked for in the wrong file.

## Touched surfaces

- Lane writes: this report only —
  `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-58/w1/Mo58Scribe50.md`.
- Scratch (throwaway, cleaned): `/fast/scratch/hyaku/mori-r58/Mo58Scribe50/` — frozen tool
  extract and `fx/mori-shokunin/` fixture repo (`git init` at that explicit path, every command
  `git -C`; three fixture commits: draft, header repair, quote corruption).
- No production file, `corpus/SOURCES.md`, `SCORECARD.md`, `LOG.md`, counter, lesson, or lane
  VCS state changed. No fleet/sibling-repo write. No commit/push in the lane.

## Out of scope (not done, by seat spec)

- No edit to `corpus/knowledge/driver-events-r58.md`, `corpus/SOURCES.md`, the lesson, or either
  counter — F1/F3/F4/F5/F6 are drafts for the owning seat.
- No remediation of F2, no provider-death or lane-health inference, no C1 review.
- No wave census run, no scoring, no seat spawning.

## Artifact paths

- Report: `.ufo/waves/round-58/w1/Mo58Scribe50.md`
- Frozen tool extract used for every line check (sha256 `6b3dba74…be997`, 479 lines), scratch
  path above; byte-identical to `tools/mori-driver-liveness.py` and to the pinned copy.
- Counter outputs quoted verbatim above are the complete outputs of
  `python3 <fx>/.ufo/waves/round-58/count-c2.py <rev>` at revs `29bebe8`, `7edf30e`, `ae8a414`.

# Mo58Scribe49 — C2 entry scope: duplication and overreach vs round-57

Seat: scribe, leaf (no dispatch). Round 58, wave `w1`, lane `mori-shokunin`.
Freeze revision `fe8801120a67c1a6b8899d7d0423839caa09e7d0`; entering `b783d0b892637ce8d20f188cad20e4d8913ca635`; worktree HEAD at review `4272736cfc5147586e1543413772f80daf44b04b`.
Artifact under review: `corpus/knowledge/driver-events-r58.md` (untracked; sha256 `e7fc469cf4ffd86a6ba14e8b6e2f66ec6366e46f853b0733553ee414c81a9e55`, mtime 2026-10-27 14:29:36 -0300).
Reference: `corpus/knowledge/watchdog-unclosed-r57.md` at the freeze revision (unchanged in worktree; `git diff fe88011 -- <path>` empty) plus `corpus/knowledge/driver-liveness-r56.md` at the freeze revision, since duplicate sentences land there first.
No production, corpus, registry, SCORECARD, LOG or VCS change was made. Read-only `git show`/`git cat-file` only.

## 1. Frozen bytes actually compared

| path | revision | sha256 |
|---|---|---|
| `tools/mori-driver-liveness.py` | `fe88011…` (= worktree, identical) | `6b3dba74c639190e7e96b6bed8e6ac8f285a51ce6d910fbe92e6dd39bf7be997` |
| `tools/mori-driver-liveness.py` | `618562c7…` (S548's named revision) | `6b3dba74…` (identical) |
| `corpus/evidence/sources-r57/mori-driver-liveness.py` | `fe88011…` | `6b3dba74…` |
| `corpus/evidence/sources-r58/mori-driver-liveness.py` | worktree (absent at freeze) | `6b3dba74…` |

Three byte-identical copies of the same 18 347-byte tool now exist (tool tree + sources-r57 + sources-r58). The r58 pinned copy adds no new provenance bytes; it satisfies the contract's copy arm only.

Presence controls re-confirmed at `fe88011…`: `git cat-file -e fe88011…:corpus/knowledge/driver-events-r58.md` fails (entry absent), same for the r58 copy — the contract's "before" control holds.

## 2. Locate the 8 claim quotes (ground truth before judging scope)

Method: for each `- **K<n>** … (tools/mori-driver-liveness.py:L)` line in the entry, take the backticked spans and test `span in tool_line[L-1]` against the frozen tool text.

| claim | cited line | span located in that line | span |
|---|---|---|---|
| K1 (entry:10) | 101 | yes | `other_lines += 1  # ts-first driver prose (steer, watchdog tick, ...)` |
| K2 (entry:11) | 103 | yes | `ts_tok, event, lane, round_s, rest = m.groups()` |
| K3 (entry:12) | 123 | yes | `m2 = LAUNCH_REST_RE.match(rest)` |
| K4 (entry:13) | 135 | yes | `m2 = COMPLETE_REST_RE.match(rest)` |
| K5 (entry:14) | 145 | yes | `if not WRAP_REST_RE.match(rest):` |
| K6 (entry:15) | 152 | yes | `if not DEAD_REST_RE.match(rest):` |
| K7 (entry:16) | 159 | yes | `if not LAUNCHFAIL_RE.match(rest):` |
| K8 (entry:17) | 96 | yes | `if parse_ts(first) is None:` |

All 8 quotes are byte-exact substrings at their cited lines. No byte-faithfulness defect (round-57 routed defect 3 is not reproduced here). All 8 sentences are true of the frozen tool.

## 3. Counter binding: the entry as written cannot reach the frozen target output

While binding the entry to `count-c2.py` I found a landing defect, not a quote defect. `count-c2.py:21` is
`KLINE = re.compile(r"^- \*\*K(\d+)\*\*.*\((tools/mori-driver-liveness\.py):(\d+)\)")` — bold must close immediately after the number (`- **K1**`), as in the counter's own `ENTRY_OK` fixture. The entry closes bold after the title (`- **K1** — unmatched timestamped prose is separate from a lane event.** …`), so the regex matches 0 lines.

Reproduced in a throwaway fixture (`/fast/scratch/hyaku/mori-r58/Mo58Scribe49/c2fix`, own `git init`, every command `git -C <fixture>`), built from the real entry verbatim + real pinned copy + real `S550` row + a copy of the frozen counter:

```
AS-IS:       rc=1  C2=unmet claims=0 located=0 copy=ok tree=ok rows=ok sources=ok failed=claims
NORMALIZED:  rc=0  C2=met claims=8 located=8 copy=ok tree=ok rows=ok sources=ok failed=none
selftest:    C2_SELFTEST pass=6 fail=0
```

`NORMALIZED` is the same entry with only the bold closed early (`- **K1** — <title>`), no prose change. So: quotes fine, copy/tree/rows/sources arms fine, 6/6 selftest fine — the sole blocker is the bold placement. Left unreformatted, the after-run prints `failed=claims` and C2 is unmet.

Secondary, same mechanism: the counter accepts a claim whenever one backticked span ≥12 chars appears in copy line L. K1 records `tools/mori-driver-liveness.py:101`, but K1's span is the counting line; the "skipped" and "not-malformed" consequences live on unquoted lines 102 (`continue`) and by absence. Identical pattern for K3→124-126, K4→136-138, K5→146-147, K6→153-154, K7→160-161, K8→97-98. Six of eight quotes bind the branch test, not the claimed `_bad`/skip effect. Not a falsehood and not caught by the counter; recorded as locatedness strength.

## 4. Duplication against `watchdog-unclosed-r57.md`

Claim-level duplication: **none.** The two claim sets are disjoint and quote-disjoint.

- r57 K1–K8 (`watchdog-unclosed-r57.md:11-18`) are all pairing-state claims, quoting `row["open_launches"].append(key)` :133, `close_round()` :143/:150, `.remove(key)` :118, the dead-clear list comprehension :157, `row["launch_fails"] += 1` :162, `row["last_event"] == "launch"` :172, `"unclosed": len(...)` :173.
- r58 K1–K8 are input-classification and rest-grammar claims, quoting :101, :103, :123, :135, :145, :152, :159, :96.
- Zero overlap between the two span sets; no r58 sentence restates an r57 sentence.
- r57's 8 quotes are all still located at the freeze revision (spot-checked at their cited lines), so r58 neither repairs nor supersedes r57. r58 never mentions `unclosed`/`in_flight` pairing, r57 never mentions `other_lines`, `malformed`, or any `*_REST_RE`.

Framing duplication (bounded-interpretation disclaimers), not claim duplication:

- r57:7 "It is not a count of processes currently running, and it does not establish a lane failure or a settled/unsettled wave" and r57:20 "conclusions describe those bytes, not an authenticated event stream … detection/report only. It does not determine authoritative swarm settlement semantics".
- r58:19 "They are not a health verdict, authenticated process identity, dispatch receipt, or authoritative settlement."
  `health verdict` duplicates `driver-liveness-r56.md:25-26`; `authoritative settlement` duplicates r57:20. The other two carve-outs (`authenticated process identity`, `dispatch receipt`) appear nowhere in r56, r57, the tool, or the tool docstring — new negative claims with no located support. Negative claims need grounding too; these are unattributed.

## 5. Duplication against `driver-liveness-r56.md` (the sentences' first landing)

The r58 claim sentences are largely restatements of grammar prose already mined in r56 under S544/S547; what is new is the code-site binding, not the statement.

| r58 | r56 (freeze) | relation |
|---|---|---|
| K1 `other_lines` is not malformed, not a lane event | r56:47-48 "A ts-first line matching none of these is an `other_line` (driver prose), counted but never a lane event and never malformed" | sentence duplicate; only the :101 binding is new |
| K8 non-ISO first token → malformed | r56:48-50 "a line whose first token is not ISO-8601 … is malformed — counted" | sentence duplicate |
| K3 launch suffix grammar | r56:33-36 lists `pgid=`/optional `driver= attempt= slot= mission=`, `pid=`, `mission=`, `runId=`, bare | generalized, and weaker: r58 says "has its own suffix grammar" without naming one alternative |
| K4 complete suffix grammar | r56:37-39 `; hyaku-inline attempt=a`, `; advancing to round=n+1`, `; respawning` | same |
| K5 wrap suffix grammar | r56:45-46 ` landed`/` complete`, optional `; NOT respawning (fleet-wrap)` | same |
| K6 dead suffix grammar | r56:40-43 `; retry same round` with optional free parenthesis | same |
| K7 launch-fail suffix grammar | r56:44 ` :: reason` | same |
| K2 five parsed fields | — | genuinely new; the only r58 sentence without an r56 antecedent |

Net: 2 sentence duplicates (K1, K8), 5 generalizing restatements that are less specific than r56:33-46 (K3–K7), 1 new (K2). The distinct content added over the corpus is the regex-dispatcher binding itself (tool :56-62 regexes are named but never quoted; the entry quotes only the `.match` call sites).

## 6. Overreach findings with line evidence

1. **r58:8 self-attests the counter verdict.** "the copy and `tools/mori-driver-liveness.py` are byte-identical at the measured revision (C2 counter)". The artifact asserts the result of the artifact's own measurement. At freeze the entry and copy are both absent, so the sentence is only true after landing; it is untestable from the entry alone and reproduces the shape of round-57 defect 2 (artifact claiming green). Belt is already provided by the counter's `copy=ok tree=ok` arms.
2. **r58:19 two unattributed carve-outs** (`authenticated process identity`, `dispatch receipt`) — see §4.
3. **r58:13 (K4) semantic imprecision.** "a launch's attempt key and a completion's attempt key are not accepted by a generic suffix parser". The tool does build the same key shape from both branches (`key = (int(round_s), int(m2.group(4)))` at :128 and `key = (int(round_s), int(m2.group(1)))` at :140); the actual distinction is line shape (` pgid=… attempt=N` vs `; hyaku-inline attempt=N`), which the sentence does not name. Readable as "the attempt keys differ", which is false in key terms.
4. **r58:11 (K2) half-supported sentence.** "later branches validate the rest rather than treating arbitrary suffixes as equivalent" is not shown by the :103 quote; it rests on K3–K7's separate quotes. Acceptable only if read as a cross-reference.
5. **Registry-level duplication.** `corpus/SOURCES.md:328` S548 (anchor `parse_log` lines 122-174, copy `sources-r57`, sha256 `6b3dba74…`) and `corpus/SOURCES.md:330` S550 (anchor `parse_log` lines 95-163, copy `sources-r58`, sha256 `6b3dba74…`) register the same file over identical bytes. S548's `teaches` cell already claims "Grounds the exact launch, completion, wrap, dead, launch-fail, in_flight and unclosed parser transitions" — i.e. the scope S550 now claims — while r57's entry only quotes pairing/counter sites. Either S548's `teaches` cell overstates what r57 grounds, or S550's distinctness is overstated; as written, two rows claim the same grounding over byte-identical anchors. Report-only; no registry edit made.

## 7. Conflicts

None. r57 K5 (dead clears same-round pairings) and r58 K6 (dead validates the retry suffix) describe different steps of the same branch and are compatible. r57 K2/K4 cite `close_round()` call sites :143/:150 whose definition is :116-120; no divergence with r58, which quotes nothing in :116-120. No r58 sentence contradicts an r56/r57 sentence.

## 8. Out of scope / not done

- No corpus, registry, lesson, SCORECARD, LOG, contract, counter, or tool edit; no commit, checkout, or `jj` operation in the lane.
- Did not run the after-run C1 counter or the round-end census; did not score either axis.
- Did not run `count-c2.py` against the lane repo itself (the entry is untracked, so no lane revision contains it); the fixture run in §3 is the reproduction, not a lane measurement.
- No fleet or sibling-repo writes. Scratch `/fast/scratch/hyaku/mori-r58/Mo58Scribe49` removed after copying receipts into this report.

## 9. Open items for the wave owner (not decisions of this seat)

- `F1` (blocker, C2 landing): close the bold after the K number, or the frozen counter prints `failed=claims` and the target output is unreachable. No prose change needed — quotes, copy, row and selftest already pass.
- `F2` (scope, non-blocking): K1/K8 duplicate r56:47-50; K3–K7 are weaker than r56:33-46 unless the regex alternatives at `tools/mori-driver-liveness.py:56-62` are quoted; only K2 is new.
- `F3` (overreach, non-blocking): drop or ground r58:19's `process identity`/`dispatch receipt`; reconsider r58:8's self-attested counter verdict; tighten K4's attempt-key wording.
- `F4` (registry, non-blocking): S548 `teaches` vs S550 scope claim the same grounding over identical bytes.

## 10. Commands run (read-only unless noted)

```
git -C /home/vgpnk/Projects/shokunin/mori-shokunin rev-parse HEAD
git -C … show fe8801120a67c1a6b8899d7d0423839caa09e7d0:{SCORECARD.md,corpus/knowledge/*.md,corpus/SOURCES.md,tools/mori-driver-liveness.py}
git -C … cat-file -e fe8801120a67c1a6b8899d7d0423839caa09e7d0:{corpus/knowledge/driver-events-r58.md,corpus/evidence/sources-r58/mori-driver-liveness.py}   # both fail (absent)
git -C … show <rev>:<path> | sha256sum        # tool @fe88011, @618562c, copy @sources-r57, copy @sources-r58
git -C … diff --stat fe88011 -- corpus/knowledge/watchdog-unclosed-r57.md tools/mori-driver-liveness.py corpus/knowledge/driver-liveness-r56.md   # empty
/fast/scratch/hyaku/mori-r58/Mo58Scribe49/c2fix: git init / add -A / commit (fixture only) + python3 <fixture>/.ufo/waves/round-58/count-c2.py <fixture-rev> and --selftest
```

Report path: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-58/w1/Mo58Scribe49.md`

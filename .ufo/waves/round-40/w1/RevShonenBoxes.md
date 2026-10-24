# RevShonenBoxes — round-40 SHONEN checklist evidence review

Seat: reviewer (read-only). Only file written: this report. No production file edited, no
lane jj state / Git index touched, no tool installed.

Target: `SHONEN.md` (four boxes) against the round-40 report draft
`/home/vgpnk/Projects/shokunin/.ufo/reports/round-40/mori.md` §SHONEN (`:127-139`) and the
round's committed evidence at `bb1f2457` → T1 `265a955cc` → T2 `8d3badd` → round tip
`ede486b7` (header claim, pushed).

Canonical semantics (read from `PROTOCOL.md:59-71`): `[x]` only by a reviewer who did not
author the round — "a subagent the lane dispatched is still the lane" (`:64-66`); the lane's
own assessment is `[~]` asserted with its evidence pointer (`:68`); `[ ]` means untouched;
per-box minimum bars at `:69-72`. Consequence: **a missing named non-author verifier caps a box
at `[~]`; it never forces `[ ]`.**

## Measurements (exact commands → outputs)

1. `git show ede486b7:SHONEN.md` → the four canonical boxes, all `[ ]`:
   `- [ ] SKILL.md contains real decision tables, error patterns, checklists, cited sources`;
   `- [ ] At least one end-to-end domain task executed and logged in LOG.md`;
   `- [ ] Instructions executable by an agent without oral context`;
   `- [ ] No cross-domain bleed (PROVINCE.md still accurate)`.
   `git diff --quiet bb1f2457 ede486b7 -- SHONEN.md` → rc `0` (byte-unchanged all round).
2. `git diff --quiet bb1f2457 ede486b7 -- PROVINCE.md` → rc `0` (byte-unchanged).
3. `git diff --name-status bb1f2457 ede486b7 | awk '{print $2}' | sed 's#/.*##' | sort | uniq -c`
   → `.ufo` 69, `corpus` 5, `LOG.md` 1, `SCORECARD.md` 1, `SKILL.md` 1, `tools` 1.
   No `PROVINCE.md`, no `SHONEN.md`, no fleet-root or sibling-lane path.
4. `git show ede486b7:SKILL.md | sed -n '11p;23p;149p;888p'` →
   `## Decision table`, `## Error patterns`, `## Checklist (executable)`,
   `| counter conformance v3 (r40) | gate | ...`; `:889` is the
   `SOURCES append-only timing (r38)` row carrying the round-40 `pass=15 fail=0` pin.
   `git show ede486b7:SKILL.md | grep -c S229` → `0` (S229 is cited in the knowledge entry and
   SOURCES row, not in SKILL.md).
5. `git show 8d3badd0:LOG.md | grep -n '^## Round 40'` → `2276`; same line at `ede486b7`.
   `git show 265a955cc:LOG.md | grep -c 'Round 40'` → `0`;
   `git diff --quiet bb1f2457 265a955cc -- LOG.md` → rc `0`.
   ⇒ the LOG entry landed at **T2**, not T1; the draft's T1 bullet misattributes it
   (`mori.md:53-57`).
6. Receipt shape (command + measured rev + exit):
   `evidence/c10-after-selftest.txt:1-2` → `command: ... conform.py 265a955cc... --selftest`,
   `revision: 265a955cc...`, eleven `PASS` lines, `CONFORM_SELFTEST pass=11 fail=0`;
   `evidence/c11-after-selftest.txt:1-3` → `command: python3 tools/mori-sources-appendonly.py --selftest`,
   `MORI_SOURCES_APPENDONLY_SELFTEST pass=15 fail=0`, `EXIT=0`;
   `evidence/c10-after.txt:1-2` → command + the P-C10 predicate text.
7. S229 anchors: `git show ede486b7:corpus/SOURCES.md | grep -n '| S229 |'` → `235`.
   Exact-URL census across sibling registries:
   `for d in */; do grep -c -F 'docs.python.org/3/reference/executionmodel' "$d/corpus/SOURCES.md"; done`
   → only `mori-shokunin 1` (no other lane printed a hit); the in-flight ConnSiblingOverlap
   census independently reports `exact=0` across the 20 sibling registries.
   `mado-shokunin/corpus/SOURCES.md` holds the CPython **RST** rows S111 (`:123`), S120
   (`:132`), S121 (`:133`) — same document, different URL/section. The in-flight seat
   `w1/ConnSiblingOverlap.md` (uncommitted) reaches the same classification and states those
   rows do not teach a static timeout fold.
8. Tip pushed: `git for-each-ref --contains ede486b7 --format='%(refname)'` →
   `refs/heads/master`, `refs/remotes/origin/master`, `refs/jj/keep/...`;
   `git rev-parse --short HEAD` → `ede486b`.
9. No named non-author verifier: `w1-spec.json` roster names only lane seats; the draft itself
   records "no named non-author verifier in-round" (`mori.md:131`). At review time 30 seat
   reports were on disk in `.ufo/waves/round-40/w1/` (`ls | wc -l` → 30), while `mori.md:41`
   still says "Prepared-but-undispatched" — stale, and all seats are still the lane.
10. Seat reports are uncommitted at the round tip:
    `git cat-file -e ede486b7:.ufo/waves/round-40/w1/ExeConformSelftest.md` → rc `128`
    (`exists on disk, but not in 'ede486b7'`). They cannot be cited as resolvable pointers yet.

## Honest state

| Box | Draft mark (`mori.md`) | Honest mark | Pointer that actually resolves |
|---|---|---|---|
| 1 — decision tables / error patterns / checklists / cited sources | `[~]` `:129-131` | `[~]` | `ede486b7:SKILL.md:11` (decision table), `:23-46` (error patterns, external URLs + corpus paths), `:149-154` (checklist), `:888-889` (r40 gate rows). The draft cites only `:888-889`. |
| 2 — end-to-end task logged in LOG.md | `[~]` `:132-133` | `[~]` | `ede486b7:LOG.md:2276` ("## Round 40", C1+C2 receipts). Not T1. |
| 3 — executable without oral context | `[ ]` `:134-135` | **`[~]` (recommended)** | `ede486b7:SKILL.md:888-889` entry/pins + `evidence/c10-after-selftest.txt:1-2` + `evidence/c11-after-selftest.txt:1-3`. |
| 4 — no cross-domain bleed | `[~]` `:136-139` | `[~]` only with a replaced pointer | `PROVINCE.md` byte-unchanged (rc `0`); lane-local diff (measurement 3); S229 URL single-owner (`corpus/SOURCES.md:235`; sibling `exact=0`). |
| any `[x]` | none | **none possible** | no named non-author verifier (`PROTOCOL.md:64-66`). |

Literal answer to the seat question: **box 3 is the only `[ ]`, and it can move to `[~]`** with
the pointer above. **No box stays `[ ]` for lack of a named non-author verifier** — that lack
only blocks `[x]`. The honest ceiling is `[~]` on all four; the draft already sits at that
ceiling on 1/2/4 (with pointer repairs).

## Findings

### Medium

- **M1 — box 3's `[ ]` is the wrong mark under the protocol.** `[ ]` is defined as untouched
  (`PROTOCOL.md:68`), but the round added two self-contained SKILL gate rows and executed both
  (`SKILL.md:888-889`; `c10-after-selftest.txt`, `c11-after-selftest.txt`). The draft's rationale
  "not externally verified this round" (`mori.md:134-135`) applies to the `[x]` bar, not `[~]`.
  Recommend `[~]` with the pointer in the table; do not cite the uncommitted seat re-run
  (`w1/ExeConformSelftest.md`) as evidence until it lands.
- **M2 — box 2's pointer does not resolve at the tip the draft's Landed-changes text names.**
  `mori.md:53-57` places `LOG.md` under T1 `265a955cc`, but LOG is byte-unchanged there and
  `Round 40` count is 0; the entry is at `8d3badd0`/`ede486b7:2276`. The `[~]` mark survives,
  but the pointer must name `ede486b7:LOG.md:2276` and the T1 bullet must be corrected.
- **M3 — box 4's pointer is not evidence of the box's property.** `mori.md:136-139` cites
  (a) `corpus/lessons/round-39-erratum.md` (an r39 wording correction) and (b) "connector items
  W1/W2 … prepared" — a prepared, undispatched seat is not a result. Replace with the committed
  measurements: `PROVINCE.md` byte-identical (rc `0`), diff lane-local, S229 URL unique
  fleet-wide. In-flight `w1/ConnW04Routing.md` also reports the 16 standing W04 rows are
  *intra-mori* (the "non-mori owner" predicate false), so "routed defects named to owning lanes"
  must not be retained as the no-bleed warrant without that receipt.

### Low

- **L1 — box 1's pointer is narrower than the box's words.** It names only the two new registry
  rows, while the box asks for decision tables, error patterns, checklists and cited sources:
  `SKILL.md:11`, `:23-46`, `:149-154`. Strict-bar note: the checklist (`:149-154`) carries no
  source citation and the decision-table cells cite repo tool paths rather than documents; under
  a literal "each citing a resolvable source" reading (`PROTOCOL.md:69-70`) only the error-pattern
  table clearly qualifies. Pre-existing, not introduced this round, and still capped at `[~]`.
- **L2 — no section-level cap statement.** "No named non-author verifier" appears only inside
  box 1's line (`mori.md:131`); boxes 2 and 4 could be misread as verifier-backed. Add one lead-in
  sentence stating every box is at most `[~]` until a non-author review.
- **L3 — stale dispatch status, not a SHONEN defect.** `mori.md:41` says "Prepared-but-undispatched"
  while 30 seat reports are on disk in `w1/`. The wave being live lets box 3/4 corroboration be
  re-derived, but every seat is lane-dispatched, so it still cannot lift any box to `[x]`.

## Residual risk / verification gaps

- Nothing above `[~]` is available this round: no non-author reviewer has touched round 40, and
  `PROTOCOL.md:64-66` counts every lane-dispatched seat as the lane.
- Every seat report in `w1/` is uncommitted at `ede486b7` (measurement 10). Box 3's independent
  re-derivation exists on disk (`ExeConformSelftest`: 11 PASS + `pass=11 fail=0`, wall 57.371 s;
  `ExeGateSelftest`: `pass=15 fail=0`) but is not a resolvable pointer until committed; the T2
  receipts remain the committed evidence, and they are lane-authored.
- Box 4's no-absorb half is point-in-time and topic-level. Committed evidence supports URL-level
  uniqueness only (`corpus/SOURCES.md:235`); the topic-level classification (mado's CPython RST
  rows as document cousins, not static-fold teaching) lives in the uncommitted
  `w1/ConnSiblingOverlap.md`.
- I did not re-run the full documented command set; I checked pointer resolvability against
  committed bytes and the receipts' command/revision/output shape. Executor seats in flight
  re-derive the numbers; all are lane-dispatched.
- The fleet report is read-only for this seat; `mori.md` was not edited here.

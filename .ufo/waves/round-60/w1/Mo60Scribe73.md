# Mo60Scribe73 — knowledge entry `corpus/knowledge/entry-claims-hardening-r60.md` (round 60, w1)

Seat: Mo60Scribe73 (scribe, leaf). Read-only on the lane: no production edit, no
commit, no VCS mutation, no fleet/sibling write. Scratch:
`/fast/scratch/hyaku/mori-r60/Mo60Scribe73` (created with `mkdir -p`, `TMPDIR` set
there, `--scratch` passed to every counter, removed before yield). Lane:
`/home/vgpnk/Projects/shokunin/mori-shokunin`. Tool installs/updates: none.

Entering state observed: lane tip `b3c256138f00c704d5aa56eb0332d74506502ef2`
(`round-60: move S561-S564 rows into the Registry table`); amended freeze
`ac496c7cde8cad965079858accae3bedfe4a73f2` (`round-60: freeze amendment 2`). The
entry is committed at tip in `398d3225` (43 lines, 4398 bytes, sha256
`6aa1b604217e50ec1055f69703976b33fc4ef49261bf441a5b130ee93195924f`) and absent at
the freeze revision (it is round-60 output, not freeze input).

## Evidence (commands and observed outputs)

Disk gate first: `bash /home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status`
and `df -h /fast` → `/dev/nvme1n1p2 804G 209G 595G 27% /fast` (green).

All counting commands ran **from the lane root**, read-only (`git show`/`ls-tree`
only; writes under `--scratch`). Every receipt comparison is a byte `diff`.

| # | command | observed | status |
|---|---|---|---|
| 1 | `python3 .ufo/waves/round-60/count-c2.py ac496c7cde8cad965079858accae3bedfe4a73f2 --scratch <S>/c2` | `C2=met selftest=ok scan=ok drift=ok trees=ok entry=ok rows=ok pins=ok tree=ok claims=13 files=6 spans=13 rev=ac496c7c…`, exit 0; `diff` vs `.ufo/waves/round-60/evidence/c2-at-freeze.txt` → **IDENTICAL** | reproduces |
| 2 | `python3 .ufo/waves/round-60/count-c3.py ac496c7c… --scratch <S>/c3` | `C3=met toolgate=ok containment=ok expectgate=ok cases=6 rev=ac496c7c…`, exit 0; `diff` vs `evidence/c3-at-freeze.txt` → **IDENTICAL** | reproduces |
| 3 | `python3 .ufo/waves/round-60/count-c1.py b3c256138f00c704d5aa56eb0332d74506502ef2 --scratch <S>/c1` | `C1=met dead-uncorrected=0 receipts=2/2 absent-set=5/5 lesson=ok rev=b3c25613…`, exit 0; `diff` vs `evidence/c1-at-data.txt` → **IDENTICAL** | reproduces |
| 4 | `python3 .ufo/waves/round-60/count-c1.py --selftest` / `count-c2.py --selftest` / `count-c3.py --selftest` | `C1_SELFTEST pass=6 fail=0` / `C2_SELFTEST pass=8 fail=0` / `C3_SELFTEST pass=3 fail=0`, exit 0 each | selftests pass |
| 5 | `python3 tools/mori-entry-claims-check.py --selftest --scratch <S>/st` | `ENTRYCLAIMS_SELFTEST pass=13 fail=0`, exit 0 | selftest passes |
| 6 | real-entry arm: `git show <R>:…` for the r59 entry, `corpus/SOURCES.md` and the six `corpus/evidence/sources-r59/*` copies → `mori-entry-claims-check.py --root <S>/root --entry corpus/knowledge/wave-settlement-artifacts-r59.md --registry corpus/SOURCES.md --artifacts-json <S>/artifacts.json --min-claims 10 --min-files 3` | `{"schema":"mori-entry-claims-v2","ok":true,"reasons":[],"stats":{"claims":13,"files":6,"spans":13,"min_span":12}}`, exit 0 | no false negative; min span **12** |
| 7 | `git ls-tree --name-only <R>:.ufo/waves/round-60/trees-c2h/` | 13 names `h00-good-control … h12-no-frontmatter`, exactly `FROZEN_EXPECTS` | tree set complete |
| 8 | registry shape for the cited rows (`python3` cell split on `corpus/SOURCES.md`) | `S561/S562/S563`: 11 cells, `status=mined`, `usedby=corpus/knowledge/entry-claims-hardening-r60.md`; `S564`: 11 cells, `status=rejected`, `usedby=corpus/lessons/round-60.md` | H4 binding satisfiable |
| 9 | cited defect artifacts present at tip: `.ufo/waves/round-59/w1/{Mo59Critic22,Mo59Critic23,Mo59Critic25,Mo59Reviewer08,Mo59Sentinel57,Mo59Sentinel58}.md` | all six exist; D1–D5 at `Mo59Critic22.md:45-49`; F1–F3 at `Mo59Critic23.md:25,36,52`; F1 at `Mo59Reviewer08.md:36`; F1–F4 at `Mo59Sentinel57.md:20,85,106,125`; F1–F3 at `Mo59Sentinel58.md:34,77,115`; M1/M2 table at `Mo59Critic25.md:45-46` | routing is grounded |
| 10 | lane-tip regression: `count-c2.py b3c25613…` and `count-c3.py b3c25613…` | both `met` (`C2=met … claims=13 files=6 spans=13`; `C3=met … cases=6`) | C1 data landing did not move C2/C3 |

Provenance note (observed, not a defect): `evidence/c2-at-freeze.txt` and
`c3-at-freeze.txt` were committed in `76904b21` (after the freeze) and record
`rev=ac496c7c…`; the entry cites them as the freeze receipts, which is accurate.

## Findings

### F-S73-1 (medium) — H4 cell overclaims: one fabricated row can still bind every copy

Entry line 23 currently ends `— one fabricated row can no longer cover every copy`.
The tool's binder check (`tools/mori-entry-claims-check.py`,
`eval_root` H4 block: `binders` = mined rows with `cells[10]==entry_rel`;
per copy `any(art in b for b in binders)`) accepts a row that names several
artifact paths in its source cell. Reproduced on a scratch fixture (two copies,
one `S900` row whose source cell names both `.ufo` artifact paths):

- row naming **both** artifacts → `{"ok": true, "reasons": [], … "spans": 2, "min_span": 12}`, exit 0
- row naming **only** the r54 artifact → `{"ok": false, "reasons": ["rows:binding=corpus/evidence/c2.json"], …}`, exit 1

So the closure is "the row must name the copy's artifact path", not "one row
cannot cover every copy"; the Limits paragraph (entry lines 26–31) already says
over-binding is accepted, which contradicts line 23 as written. Proposed text in
the draft below.

### F-S73-2 (medium) — "the reason-attribute requirement kills M2-class mutants" is not established

`Mo59Critic25.md:45-46` defines M1/M2 as **pinned tool + one predicate**. Under
the r60 drift arm (`count-c2.py` `drift` block: fails when `rc!=0` and
`verdict==SETTLEMENT_SCAN_FAIL` and any reason contains `:extra_keys=`, plus a
renamed-control OK), a faithful M2 replay was executed on `<R>`-materialized
bytes:

- pinned scan: r53 `rc=1 SETTLEMENT_SCAN_FAIL`, 67 `:extra_keys=` reasons; r54 at `round-53-alias/w1.json` `rc=0 SETTLEMENT_SCAN_OK` → arm passes
- **M2** (pinned scan + `note_not_null` predicate): r53 `rc=1 FAIL`, 67 `:extra_keys=` + 67 `note_not_null`; control `rc=0 OK` → **arm passes** (M2 survives the two conditions)
- **M2′** (extra-keys check dropped, note predicate only): r53 `rc=1 FAIL`, 0 `:extra_keys=`, 67 `note_not_null`; control `rc=0 OK` → arm fails (`attributed=False`) — this is the class the reason check actually kills

M2-shaped bytes are excluded earlier, by G1 (`run_pinned` requires sha256 ==
`PIN_SCAN`, else `scan_tool_sha`, zero execution), not by the reason
attribution. The draft scopes the claim accordingly and records the M2-additive
case in Limits.

### F-S73-3 (low) — source line enumerates `D1–D5` but describes four routed classes

Entry line 1 says `D1–D5:` and then lists four items; D5 (copy-production
independence, `Mo59Critic22.md:49`) has no r60 predicate (H1–H4 route D1–D4;
contract §C2 routes D1–D4-class items). Draft names the routed subset and flags
D5 as unre routed rather than implying closure.

### F-S73-4 (observation, contract wording, not an entry defect)

Contract C2 says "≥8 distinct bytes per span"; the tool enforces `MIN_SPAN = 8`
on **span length** (`end - start < MIN_SPAN` → `span:short`), so a span of eight
identical bytes passes. The entry says "each span carries ≥8 bytes", which
matches the implementation. Flagged for the canonical judge, not edited here.

Minor, not filed as a finding: intro line 10–11 says "two HIGH
execution-boundary findings" while S564 (Sentinel58 F1) is a rejected
duplicate-scope row; the G1 cell already records `S564 rejected as duplicate
scope`, so the sentence is a loose summary rather than a false claim.

## Draft — full markdown of `corpus/knowledge/entry-claims-hardening-r60.md`

Verbatim from the committed entry except the three annotated edits: line 1
(D1–D4 routed + D5 flagged), H4 cell (F-S73-1), H5 cell (F-S73-2) and the
Limits tail that records the M2-additive case. Everything else is
byte-identical to tip `b3c25613`.

```markdown
source: S561 — committed attack report `.ufo/waves/round-59/w1/Mo59Critic22.md` (D1–D4 routed: claim text unchecked, spans not distinct, grammar orphaned, row↔artifact binding absent; D5 copy-production independence is reported but not routed this round)
source: S562 — committed sentinel report `.ufo/waves/round-59/w1/Mo59Sentinel57.md` (F1–F4: unpinned tool bytes executed, symlink materialization escape demonstrated)
source: S563 — committed critic report `.ufo/waves/round-59/w1/Mo59Critic25.md` (drift arm accepts any nonzero exit; mutants on the wrong axis pass)
verified-at: 2026-10-28 — round-60 amended freeze `ac496c7cde8cad965079858accae3bedfe4a73f2`; counters `C2=met` / `C3=met` at that revision (`.ufo/waves/round-60/evidence/c2-at-freeze.txt`, `c3-at-freeze.txt`)
recheck: `python3 .ufo/waves/round-60/count-c2.py R` and `python3 .ufo/waves/round-60/count-c3.py R` at any named revision (both exit 0 with the frozen tokens)
coverage-map: Core — the lane's own claim-verification instruments for wave-settlement evidence (deepens the r59 entry-class instrument; no frontier row advanced, no sibling surface claimed)

# Hardened entry-claims verification and counter execution boundary (round 60)

The round-59 verifier spot-check decertified the r59 C2 instrument with four
verified met-flip classes and routed two HIGH execution-boundary findings.
The r60 hardening closes each class on the SAME real entry with no false
negative (13 claims, 13 distinct byte spans, minimum span 12 bytes at the
freeze revision).

## Entry-class predicates (`tools/mori-entry-claims-check.py`, H1–H5)

| id | predicate | closes |
|---|---|---|
| H1 | any claim-shaped line failing the frozen grammar emits `grammar:` AND blocks the verdict (r59: `grammar:` reached no arm in `measure()`; a met entry could carry unlimited malformed lines) | Mo59Reviewer08 F1; Mo59Critic22 D3 |
| H2 | every claim resolves to a distinct byte span — `line:` and `offset:` collapse to one span so aliasing is a `distinct:dup_span` duplicate; whitespace-only quotes are `span:blank`; each span carries ≥8 bytes (`span:short`) | Mo59Critic22 D2; Mo59Critic23 F1–F3 |
| H3 | claim texts are pairwise distinct and ≥10 chars (`text:short`, `text:dup`) | Mo59Critic22 D1 |
| H4 | every cited copy binds to a registry row that is mined, used-by exactly the entry, and whose source cell names the copy's `.ufo` artifact (`rows:binding`) — a row binds only the copies whose artifact paths its source cell names, so covering every copy requires naming every path | Mo59Critic22 D4 |
| H5 | the drift arm is reason-attributed: the pinned scan must FAIL the r53 file with a `:extra_keys=` member key-set reason AND scan OK over r54 bytes renamed to an r53-named scratch path (kills the filename-heuristic mutant M1; the reason check kills a wrong-axis mutant that fails r53 without any `:extra_keys=` reason — see Limits for the M2-additive case) | Mo59Critic25 |

Limits (declared, not defects): H3/H4 check form and binding, not truth — a
false-but-well-formed sentence still needs judge scrutiny; H4's binder match
is a substring over the source cell, so a source cell naming two artifacts
binds both (over-binding is accepted, never under-binding), and one row
naming every cited path binds every copy; the drift control uses one renamed
file, so a mutant keying on bytes other than the r53 member-key set is caught
only if it also flips one of the five real scans; Critic25's M2 adds a note
predicate on top of the real member key-set check, so it still emits
`:extra_keys=` and still passes the renamed control — those bytes are excluded
earlier by the G1 tool pin (they never execute), not by this arm.

## Counter execution boundary (round-60 counters, G1–G3)

| id | gate | closes |
|---|---|---|
| G1 | a counter materializes and executes repo-supplied tool bytes ONLY when their sha256 equals the frozen pin; a mismatch is reason `tool_sha` with zero execution — demonstrated by the EXEC-MARKER PoC blob (never runs under the r60 counter; the revision-pinned r59 counter still reproduces the marker as the committed control) | Mo59Sentinel57 F1; Mo59Sentinel58 F1 (S562; S564 rejected as duplicate scope) |
| G2 | `materialize()` asserts containment before every write: `..` walks and symlink parents are refused (`containment:`), one honest inside-root write is accepted, nothing lands outside the scratch root | Mo59Sentinel57 F1 step 4–5 (plain `root / rel` join + symlink follow) |
| G3 | hostile-tree expect prefixes live in the counter's frozen table; a committed `expect.txt` that disagrees is `expect_tamper:<tree>` — the scored repo can no longer grade itself | Mo59Sentinel58 F2 (attacker-controlled expect.txt) |

count-c1 executes no repo-supplied tool blob at all — its re-runs are
revision-pinned (`git show <rev>:…`), which is the stronger pin; G1 is
therefore structural there.
```

## Out of scope / not done

- No edit to `corpus/knowledge/entry-claims-hardening-r60.md`, `corpus/SOURCES.md`,
  SCORECARD, LOG, or any lane VCS; the three corrections are returned above for
  the lane to apply.
- No remediation of the counters; F-S73-2 is a documentation-accuracy finding
  about the entry, not a proposal to change the frozen predicate.
- Scratch `/fast/scratch/hyaku/mori-r60/Mo60Scribe73` removed after the receipts
  above were copied into this report; no `/tmp` artifact used as evidence.

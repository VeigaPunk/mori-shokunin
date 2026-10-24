measured 2026-10-23 · seat mori-r36-w2-RevSupS211-23 (reviewer, non-author; lane read-only)

# RevSupS211 — re-check the rejected row S211 (PMC mirror)

Attack: `corpus/SOURCES.md` row S211 and S056. This item attacks the round-35 routed repair
"SOURCES supersede rows S205–S220 (18 in-place-edited ids discharged)" at its S179→S211 link,
i.e. whether the landed superseder row S211 (a) rejects a URL that genuinely is already carried by
S056, (b) carries the rejection reason and flip in contract rule 2's shape, and (c) keeps
status `rejected` and reads as a rejection, not as evidence. It re-checks wave-1 `SupS179.md`,
whose DRAFT row landed verbatim as S211.

No tools were installed or upgraded (host `python3` 3.14.8 sufficed; every check below is git/awk/grep/sha256sum).
Scratch: `$TMPDIR` only. Lane untouched: no git/jj mutation, one report file written (this one).

## Measurements (command → observed output)

M1 — both source cells, byte-exact URL comparison.

```
$ awk -F'|' 'NR==62{s056=$3} NR==217{s211=$3} END{print "S056 source cell: ["s056"]"; print "S211 source cell: ["s211"]"}' corpus/SOURCES.md   # cells pasted below
$ u056=$(...grep -o 'https://pmc\.ncbi\.nlm\.nih\.gov/articles/PMC5856500/' <<< S056 cell); u211=$(... same on S211 cell); [ "$u056" = "$u211" ] && [ -n "$u056" ] && echo "BYTE-IDENTICAL: $u056" || echo MISMATCH
BYTE-IDENTICAL: https://pmc.ncbi.nlm.nih.gov/articles/PMC5856500/
$ grep -o 'https://pmc\.ncbi\.nlm\.nih\.gov/articles/PMC5856500/' corpus/SOURCES.md | sort | uniq -c
      3 https://pmc.ncbi.nlm.nih.gov/articles/PMC5856500/     # exactly S056:62, S179:185, S211:217
```

- S056 source cell (`corpus/SOURCES.md:62`, cell 2): `Nosek, Ebersole, DeHaven & Mellor (2018), "The preregistration revolution" — https://www.pnas.org/doi/10.1073/pnas.1708274114 (full text via https://pmc.ncbi.nlm.nih.gov/articles/PMC5856500/; pnas.org HTTP 403 on 2026-10-21)`
- S211 source cell (`corpus/SOURCES.md:217`, cell 2): `PMC mirror of Nosek et al. 2018 (round-32 candidate, rejected) — https://pmc.ncbi.nlm.nih.gov/articles/PMC5856500/`

The exact PMC URL S211 rejects is carried inside S056's source cell (as its full-text route; S056's
first URL is the pnas.org DOI page, which S211 does not duplicate). Duplicate claim: TRUE.
`^| S211 |` occurs exactly once (line 217).

M2 — the landed gate at the data tip, my own run.

```
$ python3 tools/mori-sources-appendonly.py bf0df77fee4b6ef54a90aea09335c7617f125151 --round-base 6bd57097; echo "exit=$?"
changed S041 superseded_by=S206
...
changed S179 superseded_by=S211
changed S180 superseded_by=S212
...
appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[...same 18...] round_changed=[]
exit=0
```

Matches L1's receipt. S179 is one of the 18 discharged in-place-edited ids; S211 is its superseder.

M3 — round 36 only appended; S179 untouched inside the round.

```
$ diff <(git show 6bd57097:corpus/SOURCES.md | awk -F'|' '/^\| S179 /') <(git show bf0df77…:corpus/SOURCES.md | awk -F'|' '/^\| S179 /') && echo S179-IDENTICAL
S179-IDENTICAL
$ git show 6bd57097:corpus/SOURCES.md | awk -F'|' '/^\| S(179|211) /'
| S179 | … — |  (one row only; no S211 at the base)
```

S211 does not exist at the round base; S179 is immutable-identical base→tip (its `used-by` is `—` at
both), so the supersession is a pure append — rule 2's in-place mutability was not re-violated.

M4 — what the in-place edit was (the defect S211 discharges).

```
$ git show 55c3ed5e…:corpus/SOURCES.md | awk -F'|' '/^\| S179 /'
| S179 | PMC mirror of Nosek et al. 2018 (round-32 candidate, rejected) — https://pmc.ncbi.nlm.nih.gov/articles/PMC5856500/ | paper | A | rejected candidate: same work as S056 | — | Rejected round 32: same article as S056; a mirror row would not recheck S056's URL. | rejected | 2026-10-23 | 365d | — |
```

First-ancestry S179 said "same work as S056"; commit `5126891` (44 s after publication, per
w1/SupS179) rewrote scope/teaches in place to the "duplicate URL already carried in S056's source
cell" phrasing — an immutable-cell change, hence the routed debt. S211 carries the corrected
phrasing as a new row. Both old and new phrasings are rejections of the same candidate.

M5 — the rejection ground is round-32's own Gate record.

```
$ grep -n 'reject, duplicate URL: S056' corpus/lessons/round-32.md
69:| S179 | https://pmc.ncbi.nlm.nih.gov/articles/PMC5856500/ | 2026-10-23T01:31:43Z | … | reject, duplicate URL: S056's source cell already names this mirror as its full-text route (`corpus/SOURCES.md:62`, which also records pnas.org HTTP 403 on 2026-10-21), and a mirror row would not recheck S056's URL; …
```

## Checks against the item

1. **Duplicate claim (S056 already carries the exact PMC URL).** PASS — M1: the string
   `https://pmc.ncbi.nlm.nih.gov/articles/PMC5856500/` in S211's source cell is byte-identical to
   the URL S056's source cell carries as its full-text route (both quoted above). It is S056's
   second URL (first is pnas.org), which is exactly how round-32's Gate phrased the duplicate
   (`round-32.md:69`: "S056's source cell already names this mirror as its full-text route").
   Precedent S178 (second URL of S058) was rejected the same way.
2. **Rejection reason and flip in rule 2's shape.** PASS. Fleet `CORPUS.md:116-118` (contract
   v1, the lane's frozen SOURCES contract): "Only `status`, `recheck` and `used-by` change in
   place… A correction is a new row whose `teaches` opens `supersedes S0NN —`." S211 is a new row;
   its teaches opens `supersedes S179 — ` and after the marker carries the rejection reason
   ("Rejected round 32: duplicate URL already carried in S056's source cell") and the flip
   ("a mirror row would not recheck S056's URL") — verbatim the corrected round-32 Gate ground
   (M5), faithfully carried through the supersession. `superseded_by=S211` is machine-confirmed by
   the landed gate (M2), and the gate's exit-0/`round_changed=[]` says the discharge pattern is
   respected (M2, M3).
3. **S211 keeps status rejected; reads as a rejection, not evidence.** PASS. `corpus/SOURCES.md:217`
   col 9 = `rejected` (the enum's kept-state: "a rejection is evidence of taste", `CORPUS.md:103-104`);
   unique row (M1). Anchor cell is `—` and the row carries no quotes or digests of its own; its scope
   cell says "rejected candidate: the full-text mirror S056's source cell already names". The PMC
   bytes live outside the row (`corpus/evidence/recheck-r32/S056-pmc-mirror.html` as round-32
   "uncounted evidence", and the round-36 drift-probe copy `corpus/evidence/sources-r36/S211.src`),
   which the row does not cite as an anchor. w1/SupS179's reopened fetch (HTTP 200, sha
   `a4e104ec…`, title/DOI/passage anchors) supports the article identity but changed no cell; the
   landed row matches its DRAFT verbatim.

## Residual risk and verification gaps (not this item's FAIL conditions)

- **S211 sits in the drift population forever.** The round-36 probe copy `corpus/evidence/sources-r36/S211.src`
  (sha `a4e104ec…`) is a raw PMC body with per-session `ncbi_phid`/`csrfmiddlewaretoken`; w2
  siblings (ExecDriftLive, ExecManualOracleSample, ExecReC1A) measured three consecutive fetches
  giving three distinct digests, so S211 classifies `drifted` on every future run and the probe's
  exit 1 is structurally guaranteed. Mild irony: S211's own flip says a mirror row "would not
  recheck S056's URL", yet the probe re-fetches exactly that URL each round. That is probe-population
  design (any row with a committed copy is classified; status-blind), not an admission of the row —
  the Gate decision stays `reject` and no contract rule forbids a rejected row holding a probe copy.
  Already reported by those seats; not re-adjudicated here.
- **No round-36 lesson exists at the tip** (`corpus/lessons/` ends at `round-35.md`), so the
  S205–S220 appends and the 18-id discharge table have no `## Gate` home yet; rule 2's old→new log
  duty applies to in-place changes (the S179 edit predates this round and is the routed debt being
  repaired — RevAppendDebt/RevDebtR35 track it), and appends need no log. Gap, not defect; the
  round is still in flight.
- S211's `used-by` (`corpus/lessons/round-32.md`) names the lesson that grounds the rejection text;
  the lesson's Gate table names historical S179. Honest provenance; rejected rows are not
  used-by-existence-checked by the census, and the path exists (read this session).

VERDICT: PASS

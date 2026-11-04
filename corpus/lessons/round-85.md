# Round 85 — mori (L1 MoriR85), attempt 1, wave w1 — lesson and registry

round: 85
date: 2026-11-04
entering: 2cc4b1ae35a83e4fd3fc48bae842bdf38df2e80e
freeze: ab260865 (contract, three counters, do-nothing controls)
seat scope: this lesson, two `corpus/SOURCES.md` rows and one `corpus/knowledge/` entry

Axes this seat works: **freshness** (two rows opened, pinned and quoted in this round; one routed
refusal finally given the row it was owed) and **calibration** (a receipt that binds command,
revision and subject bytes, plus the sweep that keeps a quoted tally honest). Detection and report
only. This seat wrote no counter, no `corpus/QUALITY.md`, no `SKILL.md`, no `SCORECARD.md` and no
evidence receipt, and ran no mutating git command.

Frozen authority: `.ufo/waves/round-85/contract.md` and `evidence/controls-r85.txt`. Nothing below
amends them. The C1/C2/C3 after-values belong to `.ufo/waves/round-85/count-c*.py`; this lesson
cites them as context only and never as this seat's measurement.

## Registry changes

| id | action | status | used-by |
|---|---|---|---|
| S600 | opened, pinned and quoted this round | `mined` | `corpus/knowledge/receipt-provenance-r85.md` |
| S601 | opened, pinned and quoted this round; **rejected** | `rejected` | `—` |

In-place changes (the only cells the contract lets a row change after landing): **none**. No existing
row's `status`, `recheck` or `used-by` moved this round by this seat, and no existing line changed
byte-for-byte: the append-only edit inserts two rows between S599 and `## Paths`.

`corpus/knowledge/receipt-provenance-r85.md` (new) carries the round's admission: K1 the definition,
K2 the verification-by-hash rule and its limits, K3 this lane's frozen receipt grammar with one line
of justification per header field. It cites S600 in its `source:` line and separates the source's
claims from the lane's own P-C2 rule in every section.

## Mistakes

| Class | Evidence pointer | Captured-by | Fix delivered and what makes it able to fail |
|---|---|---|---|
| `number-drift` (compound: `reference-drift` in the same criterion) — a round quoted its own instrument's **pre-amendment** selftest tally as "the measured tally", and its line pointers had drifted off the constructs they name, so a reader who followed the pointer landed on argument parsing and believed a number that the graded bytes contradict | `corpus/QUALITY.md:1916` (at the freeze bytes `ab260865`) states the r84 `count-c1.py`'s "measured tally is `C1_COUNTER_SELFTEST pass=11 fail=0`"; the same file prints `C1_COUNTER_SELFTEST pass=15 fail=0` rc 0 today, and has carried 15 `cases.append(` arms since `5a231ef8`. The two pointers `:296-300` and `:301-313` land on `ap.add_argument("--selftest", …)` / `a = ap.parse_args(argv)` and on `try:` / revision resolution, while the stub gate is at `:323-327` and the detector gate at `:328-334`. Routed by the r84 non-author verifier (`corpus/lessons/round-84-verifier-spotcheck.md`, D84-2) | `none` at authoring time — no QUALITY criterion required re-running a quoted tally, or re-locating a pointer with `grep -n`, before the criterion was written; the class was found by the non-author closure, not by the round that produced it | The superseding criterion is **QUALITY 173**, landed this round by the quality scribe (`Mo85S02Quality`, uncommitted at this seat's write time): "This row supersedes the quoted tally and the `:296-300` pointer of criterion 172", with a red-before measurement on `git show` byte images. This seat's contribution is the sweep below, which makes the class mechanical rather than remembered. It re-runs **every** counter a frozen criterion quotes and re-reads **every** pointer against the same bytes, and at the freeze bytes it prints exactly one `STALE` and two `DRIFT`s, all in criterion 172. Red-before is the sweep's own output; the delivered instrument is a lesson-embedded script, so the fix is the criterion (173) and the sweep is the detector |

Sweep, run from `/home/vgpnk/Projects/shokunin/mori-shokunin` against the **freeze bytes** of
`corpus/QUALITY.md` (`git show ab260865:corpus/QUALITY.md`) rather than the worktree, because
`corpus/QUALITY.md` was being written by a sibling seat during this seat's window (uncommitted,
mtime 08:06:41) and a sweep must grade a known tree:

```sh
S=${HYAKU_SCRATCH:-/fast/scratch/hyaku}/mori-r85/Mo85S01Lesson
git show ab260865:corpus/QUALITY.md > "$S/QUALITY-freeze.md"
python3 -I - "$S/QUALITY-freeze.md" <<'PY'
import re, subprocess, pathlib, sys
text = pathlib.Path(sys.argv[1]).read_text()
blocks = re.split(r"(?m)^(?=\d+\.\s)", text)
pairs = stale = drift = 0
for b in blocks:
    m = re.match(r"(\d+)\.\s", b)
    if not m: continue
    cid = m.group(1)
    claims = re.findall(r"([A-Z0-9_]+_SELFTEST) pass=(\d+) fail=(\d+)", b)
    if not claims: continue
    last = None; ptrs = []
    for mm in re.finditer(r"((?:\.ufo|tools|corpus)[\w./-]*\.(?:py|md|txt))?:(\d+)(?:-(\d+))?", b):
        p = mm.group(1) or last
        if mm.group(1): last = mm.group(1)
        if p: ptrs.append((p, int(mm.group(2)), int(mm.group(3) or mm.group(2))))
    for p in sorted(set(x[0] for x in ptrs)):
        if not re.fullmatch(r"\.ufo/waves/round-\d+/count-c\d\.py", p): continue
        if not pathlib.Path(p).exists(): continue
        r = subprocess.run(["python3", "-I", p, "--selftest"], capture_output=True, text=True, timeout=300)
        meas = dict((n, a) for n, a, c in re.findall(r"([A-Z0-9_]+_SELFTEST) pass=(\d+) fail=(\d+)", r.stdout + r.stderr))
        src = pathlib.Path(p).read_text().splitlines()
        for tok, n, f in claims:
            if tok not in meas: continue
            pairs += 1
            if meas[tok] != n:
                stale += 1
                print("STALE  criteria %s %s claimed=pass=%s measured=pass=%s (%s, rc=%d)" % (cid, tok, n, meas[tok], p, r.returncode))
            for q, s, e in ptrs:
                if q != p: continue
                if tok not in "\n".join(src[s-1:e]):
                    drift += 1
                    print("DRIFT  criteria %s %s:%d-%d lacks %s | it holds: %s"
                          % (cid, p, s, e, tok, " / ".join(x.strip() for x in src[s-1:e][:2])[:100]))
print("checked=%d stale=%d drift=%d" % (pairs, stale, drift))
PY
```

Output, as measured by this seat 2026-11-04:

```text
STALE  criteria 172 C1_COUNTER_SELFTEST claimed=pass=11 measured=pass=15 (.ufo/waves/round-84/count-c1.py, rc=0)
DRIFT  criteria 172 .ufo/waves/round-84/count-c1.py:296-300 lacks C1_COUNTER_SELFTEST | it holds: ap.add_argument("--selftest", action="store_true") / a = ap.parse_args(argv)
DRIFT  criteria 172 .ufo/waves/round-84/count-c1.py:301-313 lacks C1_COUNTER_SELFTEST | it holds: try: / if a.selftest:
checked=1 stale=1 drift=2
```

`checked=1` is honest and is the sweep's own limit: it grades only criteria that both quote a
counter's own selftest token **and** cite that counter by `path:line`, and 172 is the only frozen
criterion that does. The delivered `tools/mori-claim-sweep.py` does not cover this class — its
default carriers are `SCORECARD.md,SKILL.md,SHONEN.md,LOG.md` and its `stale_literals` are pinned
strings, not re-runs — which is why a lesson-level sweep is the detector rather than a tool claim.
The `:229-230` pointer in the same criterion is a `.md` pointer (`Mo83R01C1.md`); the sweep's
continuation-pointer grammar treats a bare `:N-M` as inheriting the last named path, so a `.md`
pointer must be spelled with its path or the sweep mis-attributes it (this seat hit that
mis-attribution before adding `.md`/`.txt` to the path alternation, and it is why the output above
carries two `DRIFT`s rather than three).

## Census

Run from `/home/vgpnk/Projects/shokunin`, before the append, verbatim:

```text
$ scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori
…
mori	ok	/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md
```
rc **0**; rows **372** — `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md`;
warnings **35**, all `W04` duplicate-URL (the entering tolerance); zero `E` codes; zero `W01`/`W02`/
`W03`.

Run after the append, verbatim:

```text
$ scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori
…
mori	ok	/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md
```
rc **0**; rows **374** — same command; warnings **35**, all `W04`, i.e. **no new warning of any
class** from the two added rows; zero `E` codes; zero `W01`/`W02`/`W03`.

Both runs print the same `mori ok` summary line and exit 0; the delta is the two rows. The validator
prints no row count, so the counts above are the contract's own grammar count from `CORPUS.md`
*Census*, not the validator's output.

## Gate

Two new rows, one admit and one reject. Both were opened by this seat in this round; both are pinned
under `corpus/evidence/sources-r85/` with a sha256 recorded in the row.

| Candidate | Decision | Evidence / flip condition |
|---|---|---|
| **S600** — Reproducible Builds, "Definitions", `https://reproducible-builds.org/docs/definition/` | **ADMIT** (tier A, docs) | Accessed 2026-11-04, HTTP 200, no redirect, 37681 bytes, 3662 lines, sha256 `a558c89f5f27dffa69fd1dc49904179b60233bcfdfc64807abfe1acf37518ebb`. Four copies share that one sha256: this seat's live fetch, the two pins under `corpus/evidence/sources-r85/` (`rb-definition-1.html`, `-2.html`; they appeared during the scout seat's window and this seat did not observe their writer) and the freeze pin `.ufo/waves/round-85/evidence/rb-definition.html`. Three of the four were additionally compared with `cmp` and are byte-identical; the fourth is bound by the same sha256. Located quote, raw lines 175-177, **21 words**: "given the same source code, build environment and build instructions, any party can recreate bit-by-bit identical copies of all specified artifacts". It grounds `teaches` narrowly: reproducibility is a property a **third party** re-derives, so a receipt that names the tree and the digest certifies the comparison while a receipt that asserts a run does not. Scope limit recorded in the row: the page says nothing about receipts, attestations or counters (0 hits each) and uses "revision" once, for a source checkout. |
| **S601** — "An Empirical Evaluation of Manually Created Equivalent Mutants", `arXiv:2404.09241` | **REJECT** — row kept as `rejected` (D84-3) | Accessed 2026-11-04, HTTP 200, no redirect, 40386 bytes, 596 lines, sha256 `4bcb20b23ad5046657a65a29595517da973128a289ff75ba13ad8926c5511a80`, v1 submitted 2024-04-14; pinned as `corpus/evidence/sources-r85/arXiv-2404.09241-abs.html`. Located quote, abstract body line 121, **12 words**: "mutants that differ only in syntax but not semantics, hamper this process" (the same sentence is copied into page metadata at lines 28 and 39; the anchor is the body). Reason: it defines equivalence and reports a *weaker* "hamper this process" cost over manually created mutants in the Code Defenders game study, with no cost-and-bias half and no adjudication procedure, so it grounds neither the lane's exemption rule (S599 already does) nor a gate tally. **Flip:** a revision of the paper (or a successor) that states the cost-and-bias half for a gate's tally, or an adjudication procedure, admitted as a freshly pinned and quoted row — never as a back-fill of this one. |

**D84-3 is discharged by this row, not by this paragraph.** The r84 Gate refused the paper and left
the refusal in prose only; the registry now carries the decision with its reason and its flip
condition, which is what `CORPUS.md` `status: rejected` ("kept — a rejection is evidence of taste")
exists for. This seat opened the paper itself this round; the 40386-byte / sha256 `4bcb20b2` reading
reproduces the r84 screening value, but the row rests on this seat's fetch.

**Assimilation: none.** No `merge/mori/` adoption this round; no shokuknow entry was merged, cited or
superseded by this lesson.

**`considerthese` line.** `considerthese/2026-10-26.md` suggestion 3 — "Re-execute what closures only
evidence-verified" — is mined this round into the receipt rule: `.ufo/waves/round-85/count-c2.py`
grades a receipt that binds its command, its revision and the sha256 of the subject bytes at that
revision, so a later round can re-run the exact command against the exact bytes instead of
evidence-verifying a closure. The receipt-producing harness
`.ufo/waves/round-85/make-receipts.sh`, named by QUALITY 175 and by the L1, was **not on disk when
this lesson was written**, so this line cites the frozen grader it can measure and not the harness it
cannot. Cross-reference: `corpus/QUALITY.md` 173 (quoted-tally freshness) and 175 (the `# limits:`
header).

## Errata (round 86, 2026-11-04; the r85 verifier spot-check's routed defect 4)

The round-85 report says the "five amendments, each disclosed in the contract and the round lesson";
this lesson carried no amendment disclosure and the contract's §Amendments jumped A3 → A5 because
the A4 block was missing. The missing A4 anchor (`91f657f6`) is now recorded in
`.ufo/waves/round-85/contract.md` under *Errata*, and this paragraph is the lesson-side disclosure
the report's sentence promised. The report itself is a filed record and is corrected here, not
rewritten.

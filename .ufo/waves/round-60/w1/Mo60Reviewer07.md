# Mo60Reviewer07 — H2 span-aliasing (round-60, w1)

Seat: build entry variants over the real copies in scratch — line+offset to the
same span, two claims to one span — confirm `distinct:dup_span`, and confirm the
old r59 `eval_entry` accepted both.

Read-only review. No production file, corpus registry, SCORECARD, LOG or lane VCS
was modified; the only lane write is this report. No installs, no pacman, no
sibling/fleet writes, no subagent dispatch.

## Pins (everything below is derived from these bytes)

| object | revision / sha |
|---|---|
| lane HEAD while reviewing | `b3c256138f00c704d5aa56eb0332d74506502ef2` |
| freeze revision (contract) | `ac496c7cde8cad965079858accae3bedfe4a73f2` |
| hardened verifier `tools/mori-entry-claims-check.py` | `cffe9f3359097277a7ea39729309efdc5831a1738994ceb30ee023ac0eae6e69` (== PIN_EC; identical at `ac496c7c` and `b3c25613`) |
| r59 counter `.ufo/waves/round-59/count-c2.py` (old `eval_entry`) | `2df3ae84f6d66f9ee46cd46cf2cb199ca85e7400301c5a0e9dd94b7b375877be`; byte-identical at r59 data rev `7b86704d`, at `ac496c7c` and at HEAD |
| real entry `corpus/knowledge/wave-settlement-artifacts-r59.md` | `441a751de67f1cef9db265666a6f77734d7a9d964fe2efcf3756e4394716ce21` (identical at `ac496c7c` and HEAD) |
| six cited copies + `corpus/SOURCES.md` | materialized with `git show ac496c7c:<path>`; pins in the claims re-verify byte-equal (`pin_ok=True` for every claim resolved below) |

The lane tip did move under the round (`398d3225`, `b3c25613` after the freeze);
every file read here is either pinned to `ac496c7c` or (for the tool/counter/entry
blobs) verified byte-identical across `7b86704d`/`ac496c7c`/HEAD before use, so no
conclusion rests on an unpinned working-tree read.

## Method (scratch, containment-asserted by construction)

Scratch root `$HYAKU_SCRATCH/mori-r60/Mo60Reviewer07` (`TMPDIR` set to it). No git
repository was created or mutated; the lane was only read with `git show`.

`build.py` (scratch) materializes, at `ac496c7c`, the real entry, the six
`corpus/evidence/sources-r59/*.json` copies in the frozen copy→artifact map (plus
`w1-results-r53.json`, which sits outside that map and is never cited), `corpus/SOURCES.md`,
and the frozen copy→artifact map itself, into five roots that differ **only** in the
entry file:

| root | delta over the real entry |
|---|---|
| `control` | none (verbatim real entry) |
| `alias_line_off` | `+ K15`: `offset:48` claim on `w1-results-r54.json`, quote = line 5 bytes |
| `alias_two_claim` | `+ K16`: second `line:5` claim on `w1-results-r54.json`, same quote |
| `alias_off_off` | `+ K17`: second `offset:89` claim on `w1-settlement-r58.json` (K12's span) |
| `nested_span` | `+ K18..K21`: four 8-byte sliding windows over the same 13-byte line |

Insertion is byte-identical apart from the added claim line (verified with
`diff -u`; the added line sits inside `## Claims` before `## Limits`).

Commands (scratch paths abbreviated as `$S`):

```sh
TMPDIR=$S python3 build.py "$S/roots"

# hardened r60 verifier, one run per root
python3 /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-entry-claims-check.py \
  --root $S/roots/<root> \
  --entry corpus/knowledge/wave-settlement-artifacts-r59.md \
  --copy-prefix corpus/evidence/sources-r59/ \
  --registry corpus/SOURCES.md \
  --artifacts-json $S/roots/<root>/artifacts.json \
  --min-claims 10 --min-files 3

# frozen r59 eval_entry, imported from the committed blob (no mutation)
python3 run.py "$S/roots"      # importlib-loads .ufo/waves/round-59/count-c2.py,
                              # calls eval_entry(root) for each root
```

## Result 1 — `distinct:dup_span` fires for both required constructions

Hardened tool (`cffe9f33…`), exit code and verdict JSON per root:

```
control          rc=0 ok=True  spans=13 claims=13 dup_span=-                        other=-
control          OLD(r59 eval_entry) ok=True claims=13 files=6 reasons=[]
alias_line_off   rc=1 ok=False spans=13 claims=14 dup_span=['distinct:dup_span=K1=K15'] other=-
alias_line_off   OLD(r59 eval_entry) ok=True claims=14 files=6 reasons=[]
alias_two_claim  rc=1 ok=False spans=13 claims=14 dup_span=['distinct:dup_span=K1=K16'] other=-
alias_two_claim  OLD(r59 eval_entry) ok=True claims=14 files=6 reasons=[]
alias_off_off    rc=1 ok=False spans=13 claims=14 dup_span=['distinct:dup_span=K12=K17'] other=-
alias_off_off    OLD(r59 eval_entry) ok=True claims=14 files=6 reasons=[]
nested_span      rc=0 ok=True  spans=17 claims=17 dup_span=-                        other=-
nested_span      OLD(r59 eval_entry) ok=True claims=17 files=6 reasons=[]
```

`other=-` matters: `distinct:dup_span` is the **only** reason in each alias run, so
the verdict flip is attributable to H2 alone and not to a co-firing `span:`,
`pin:` or `rows:` reason. The `spans=13 / claims=14` pair is exactly the H2
collapse (one span absorbed by two claims).

## Result 2 — the spans really are the same byte range

Resolved with the tool's own `span_of()` (`tools/mori-entry-claims-check.py:66-83`),
copy bytes read from the materialized root; `pin_ok` compares sha256:

```
alias_line_off  K1   line   n=5   span=(48, 61)   len=13 bytes=b' "seats": 74,'           pin_ok=True
alias_line_off  K15  offset n=48  span=(48, 61)   len=13 bytes=b' "seats": 74,'           pin_ok=True
alias_two_claim K1   line   n=5   span=(48, 61)   len=13 bytes=b' "seats": 74,'           pin_ok=True
alias_two_claim K16  line   n=5   span=(48, 61)   len=13 bytes=b' "seats": 74,'           pin_ok=True
alias_off_off   K12  offset n=89  span=(89, 112)  len=23 bytes=b'mori-wave-settlement-v1' pin_ok=True
alias_off_off   K17  offset n=89  span=(89, 112)  len=23 bytes=b'mori-wave-settlement-v1' pin_ok=True
```

The line form (`line:5` → `start = Σ(len+1)` up to line 5 = 48, `end = start+len(line)`
= 61) and the offset form (`offset:48`, quote length 13) land on the identical
`(file, start, end)` key that H2 uses at `tools/mori-entry-claims-check.py:162-167`.
This is the real-copy version of the routed defect: the two claims are both
byte-exact and pin-correct, and only the span-identity rule separates them.

## Result 3 — the old r59 `eval_entry` accepted both (defect reproduced)

Importing the committed r59 counter blob (`2df3ae84…`, identical at r59 data rev
`7b86704d`) and calling `eval_entry(root)` returns `ok=True, reasons=[]` for
`alias_line_off` **and** `alias_two_claim` (and for the extra `alias_off_off`).
Since `reasons` is empty, the old counter's `entry_ok` / `rows_ok` / `pins_ok`
derivations (`.ufo/waves/round-59/count-c2.py:303-306`) are all `True` as well —
an aliased entry would have counted as a met entry arm.

Why: the r59 checker held one dict keyed by claim **id** only
(`.ufo/waves/round-59/count-c2.py:117,125-127` — `if kid in seen`), and its span
checks were strictly per claim (`.ufo/waves/round-59/count-c2.py:139-160`:
`flines[n-1] != q` / `fb[n:n+len(q)] != q`). No cross-claim span map existed, so
line/offset aliasing and repeated identical spans were invisible. H2 adds exactly
that map (`tools/mori-entry-claims-check.py:146-171`).

## Result 4 — no false negative introduced (control + frozen coverage)

- Control (real entry, verbatim, six real copies at `ac496c7c`):
  `{"ok": true, "reasons": [], "stats": {"claims": 13, "files": 6, "spans": 13, "min_span": 12}}`
  — matches the committed at-freeze receipt
  (`evidence/c2-at-freeze.txt`: `… claims=13 files=6 spans=13 rev=ac496c7c…`) and the
  knowledge entry's "minimum span 12 bytes" line. H2 is not over-strict: K2–K5 all
  quote the identical string ` "seats": 64,` in different copies and are accepted,
  because distinctness is keyed per `(copy, start, end)`, not per quote text.
- Frozen hostile coverage exists independently of this scratch:
  - `.ufo/waves/round-60/trees-c2h/h03-line-offset-alias` (synthetic copies whose
    line 2 carries three keys) → `{"ok": false, "reasons": ["distinct:dup_span=K1=K10"],
    "stats": {"claims": 10, "files": 3, "spans": 9, "min_span": 13}}` — dup_span is
    the only reason, so the frozen tree isolates the same class.
  - `h01-semantically-empty` covers the repeated-identical-offset class
    (`distinct:dup_span=K1=K2 … K1=K8` alongside the expected `text:short`).
- Counter-side containment of H2: `count-c2.py:329-333` requires
  `ok is True` **and** `spans == claims` for the entry arm, so an aliased entry
  cannot reach `entry=ok` even if the tool's reason list were misread.

## Findings

**Blocking: none.** The C2/H2 claim as frozen —
"line/offset aliasing collapses … whitespace-only quotes rejected … ≥8 distinct
bytes per span" — reproduces on real copies, rejects both required constructions
with the exact `distinct:dup_span` reason, and the old verifier demonstrably
accepted the same entries.

**Low (code hygiene, not a claim break) — `--copy-prefix` is a dead parameter.**
`tools/mori-entry-claims-check.py:32` documents `--copy-prefix DIR/`,
`:84` threads it into `eval_root(...)`, `:468` passes it — and `eval_root` never
reads it (grep: only those three occurrences; `count-c2.py` never passes it).
File membership is decided solely by the artifacts-JSON keys (`:142-144`,
`:150-151`). Empirically confirmed: running the tool over the committed h03 tree
with the *expect table* supplied as `--artifacts-json` (while the copy prefix
matched exactly) produced `files:outside=` for all three cited copies and
`spans=0`. Harmless to the claim (`files:outside` still fails the verdict), but
the option advertises prefix-scoped copies that do not exist; a future reader
could mistake it for a containment control.

**Residual risk (medium-low, scoping — not a predicate violation) — exact-span
distinctness admits overlapping slidable windows.** H2 collapses only *identical*
`(copy, start, end)` spans. Unequal but overlapping spans over one line are
distinct by construction, so a single long line supports up to `len(line) - 7`
claims at `MIN_SPAN = 8`. Demonstrated (`nested_span`): four extra claims at
`offset:48..51` on the 13-byte r54 line 5 — all byte-exact, all `pin_ok`, all
`≥8` bytes — are accepted:

```
nested_span K18 offset n=48 span=(48,56) len=8 bytes=b' "seats"'  pin_ok=True
nested_span K19 offset n=49 span=(49,57) len=8 bytes=b'"seats":'  pin_ok=True
nested_span K20 offset n=50 span=(50,58) len=8 bytes=b'seats": '  pin_ok=True
nested_span K21 offset n=51 span=(51,59) len=8 bytes=b'eats": 7'  pin_ok=True
nested_span rc=0 ok=True spans=17 claims=17
```

So `claims_min` can be met from a few bytes of three copies while every H2 token
(`distinct:dup_span`, `span:blank`, `span:short`) stays silent. This is consistent
with the frozen predicate ("distinct byte spans"), which does not assert claim
independence; it is a residual for any future round that wants `claims` to measure
independent observations (non-overlapping spans, or a per-copy span budget,
would be the lever). Reported as risk, not as a defect, and no remediation was
attempted.

**Informational — H2 skip path is safe on the counter.** Claims whose `cfile` is
not an artifacts key are skipped by the dup map (`:150-151`), but they already
emit `files:outside` (`:142-144`); with the counter requiring `ok is True`, that
skip cannot hide an alias in the entry arm. Verified with the wrong-JSON run
above (`ok=false, spans=0`).

## Residual risk and verification gaps

- `nested_span` demonstrates the sliding-window residual on the real r54 line;
  generalizing to "any one-line artifact yields `L-7` claims" is arithmetic from
  `span_of` plus `MIN_SPAN=8` — marked `[INFERENCE]`, not measured on a purpose-built
  one-line copy.
- I did not re-run the full frozen `count-c2.py` (C2's own arm, already receipted at
  `evidence/c2-at-freeze.txt`); my `control` run reproduces that receipt's entry-arm
  numbers (`claims=13 files=6 spans=13`) from the same pinned bytes.
- H2's interaction with the other eleven hostile trees (h00, h02, h04–h12) was not
  re-measured; only the alias-relevant h01/h03 were exercised, which is the seat's
  scope.
- Line-kind spans assume LF-only copies; every committed copy in scope is LF
  (`cat -A` shows no `^M`), so a CRLF line claim (which would fail `span:` by
  construction) was not tested — non-goal for this seat.

## Cleanup

Scratch `$HYAKU_SCRATCH/mori-r60/Mo60Reviewer07` (fixtures, builder, runner,
receipts) was removed before yielding; the receipts quoted above are reproduced
verbatim in this report. Disk guard was green at start (`/fast/scratch/hyaku` 26%
used, 599.6G free) and no ENOSPC occurred. No tool installs or updates were made.

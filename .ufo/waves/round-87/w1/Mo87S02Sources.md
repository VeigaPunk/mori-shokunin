# Mo87S02Sources — round 87 w1: one external source for the C2 supersede rule

Seat: `Mo87S02Sources`, leaf member (no subagent dispatch), sources scribe — detection and report
only. No commit, no push, no mutating git/jj in the lane, no lane append, no knowledge file. No tool
installs: `curl`, `git ls-remote`, `python3 -I` stdlib and coreutils only. Scratch:
`/fast/scratch/hyaku/mori-r87/Mo87S02Sources/`, deleted before yield; nothing copied into the lane.

**Verdict in one line:** the round's candidate is **already `S600`** (identical URL, identical scope,
identical bytes) and a sibling already grounded the replay *environment* on `S603`; the missing half
of the C2 rule — *a superseding record is admitted only by verification against the record trusted
first, and an older version cannot displace it* — is opened fresh here as **The Update Framework
specification v1.0.37**, with a located 20-word quote, two byte-identical fetches and a
tag-pinned revision. The L1 appends; this seat writes no row.

## 1. Behavior

Read, in the order the seat spec names, with the bytes actually on disk:

1. `.ufo/waves/round-87/contract.md` (`sha256 bf208a44…`) — P-C1, P-C2, the targets, the kill rule,
   the do-nothing controls and amendment A1.
2. `.ufo/waves/round-87/count-c1.py` (`e2ff9687…`) and `count-c2.py` (`264a43f0…`) — the two frozen
   counters and their selftest obligations (the r86 subjects' frozen arm counts 18/13/23; the C2
   counter's subject sub-gate follows amendment A1).
3. `.ufo/waves/round-87/evidence/controls-r87.txt` (`53d65a42…`) — C1 entering + label-only controls
   (`C1=unmet … survivors=6 total=6 arms=48`, rc 1) and C2 entering + header-only controls
   (`C2=unmet … superseded=0 legacy=3`, rc 1).
4. `.ufo/waves/round-87/evidence/probe-r87.txt` (`530e35e6…`) — the 23-mutant probe (8 in
   `count-c1.py`, 8 in `count-c2.py`, 7 in `count-c3.py`); **17 survive and 6 are killed**, every
   kill in `count-c3.py`; the six-mutant population is the six survivors the contract names.
5. `corpus/lessons/round-86-verifier-spotcheck.md` §*Routed defects* (`820e5a49…`) — all eight items
   read; none is a sources-registry item.
6. `SCORECARD.md` §*Planned (round 87)* (`6334569d…`) — items 1–3 (operability / calibration / depth).

Then the sources authority and the seat's own context:

- `/home/vgpnk/Projects/shokunin/CORPUS.md` §*SOURCES.md — where a shokunin learns* (`88556402…`):
  the 11-cell schema, the tier/kind/status enums, and rule 1 — *"The round lesson's `## Gate`
  records, for every new row, the URL, the access date, and a ≤25-word quote with its location
  grounding `teaches`."*
- `corpus/lessons/round-87.md` §*Gate* (`3d6e56f1…`, working-tree modified by a sibling while this
  seat ran): **"Gate rows: none written"**, with the row text explicitly left to the L1. This report
  is that input.
- `corpus/knowledge/receipt-supersede-r87.md` (`13f7695e…`) — the round's C2 note; it cites `S603`
  for clone/`--shared` semantics and `S600`/`S602` as adjacent, and states the rules the new row
  must ground.
- `.ufo/waves/round-86/w1/Mo86S02Sources.md` — the prior seat's report shape (facts / gates /
  revision honesty / limits), followed here.

Work done: fetch the candidate twice, hash and `cmp`; screen the registry; fetch the replacement
twice, hash, `cmp`, resolve its tag to a commit; locate one quote and prove single occurrence; screen
the replacement against the registry; propose row cells and the one knowledge sentence; write this
report only.

## 2. Candidate verification — `https://reproducible-builds.org/docs/definition/`

Command (exact, run in the scratch dir):

```
curl -sS -L --max-time 60 -o src.html -w '%{http_code} %{num_redirects} %{url_effective}\n' \
  https://reproducible-builds.org/docs/definition/
```

| fact | value |
|---|---|
| HTTP | **200**, `num_redirects` **0**, `url_effective` identical to the requested URL |
| bytes / lines | **37681 bytes / 3662 lines** (`wc -c -l`) |
| sha256 | `a558c89f5f27dffa69fd1dc49904179b60233bcfdfc64807abfe1acf37518ebb` |
| stability | second fetch (`src2.html`) byte-identical: `cmp src.html src2.html` → **CMP-IDENTICAL**, same sha256 |
| headers | `Last-Modified: Mon, 02 Nov 2026 16:07:38 GMT`; `ETag: "9331-65f4d584f6db0"`; `Content-Type: text/html; charset=utf-8`; `Content-Length: 37681` |
| drift vs. the lane's pin | `corpus/evidence/sources-r85/rb-definition-1.html` hashes to **the same sha256**, same 37681 bytes / 3662 lines — this seat's two fetches join the three recorded r85 fetches as byte-identical |
| registry | `grep -c 'reproducible-builds.org/docs/definition' corpus/SOURCES.md` → **2** (the `S600` row at line 382 **and** the round-86 search-log note); exactly **one registry row** |
| row | `S600` — `docs`, tier `A`, scope *"the definition of a reproducible build and the byte-comparison verification rule, as the ground of a receipt that binds a revision and a digest"*, status `mined`, `used-by` includes `corpus/knowledge/receipt-provenance-r85.md` and `corpus/knowledge/receipt-supersede-r87.md` |

**Located quote (candidate).** Raw lines **196-197**:
`<p>The reproducibility of artifacts is <strong>verified</strong> by bit-by-bit comparison. This` /
`is usually performed using cryptographically secure hash functions.</p>`. The sentence quoted is the
tag-stripped form — **9 words**:

> The reproducibility of artifacts is verified by bit-by-bit comparison.

Single-occurrence proof, two explicit normalisations of the fetched bytes:

- tag-stripped (`re.sub(r"<[^>]*>", " ", raw)`) then every whitespace run → one space:
  `count == 1`;
- markup as served (`<strong>` kept) then the same collapse: `count == 1`, starting at raw line 196.

**Measured note on the row's other anchor.** The `S600` anchor cell calls raw lines 175-177 a
"21-word located span". Under my counter the full sentence across those lines, tags stripped, is
**26 words** (`A build is reproducible if given the same source code, build environment and build
instructions, any party can recreate bit-by-bit identical copies of all specified artifacts.`) — so
the 21-word label must refer to a chosen sub-span, and quoting 175-177 whole would exceed a 25-word
cap. I therefore used the 196-197 verification sentence (9 words) for this seat's proof. I am not
claiming a defect in `S600`; I am reporting the count I measured and why my quote is the other one.

**Verdict: duplicate — excluded, never opened as a new row.** Same URL, same scope, same bytes as
`S600`; the round-86 search log already recorded the same exclusion reason. Per the seat spec's
step 3, a different source is proposed below.

## 3. Replacement opened — The Update Framework specification v1.0.37

Why this source (state, not vibes): the round's C2 predicate is *"a legacy receipt … counts
`superseded` only when a present, problem-free successor names it in `# supersedes:`"*, and the
counter admits a successor only if its own body replays. `S600` grounds *byte comparison* as the
reproduction test; `S602` grounds the negative (the quote its row records: *"Byproducts are not
verified by in-toto's default verification routine."*); `S603` grounds the replay *environment* (a
clone is a repository, `--shared` shares via alternates). None of them states the **acceptance rule
for a superseding
record**: that the successor is checked against hashes held by the record that was trusted first,
and that a version which is not exactly the trusted version plus one is a rollback. TUF's client
update workflow states exactly that, in MUST language, at a tagged revision.

Command (identical shape, twice):

```
curl -sS -L --max-time 60 -o tuf.md -w '%{http_code} %{num_redirects} %{url_effective}\n' \
  https://raw.githubusercontent.com/theupdateframework/specification/v1.0.37/tuf-spec.md
```

| fact | value |
|---|---|
| HTTP | **200**, `num_redirects` **0**, final URL identical to the requested URL |
| bytes / lines | **76283 bytes / 1739 lines** (`wc -c -l`) |
| sha256 | `87c7136231b8cb3355736d8e7cfe88380d030cb2994ea283a19e78e03fb171ff` |
| stability | second fetch (`tuf2.md`) byte-identical: `cmp tuf.md tuf2.md` → **CMP-IDENTICAL**, same sha256 |
| headers | `Content-Type: text/plain; charset=utf-8`; `Content-Length: 76283`; `ETag: "084a3b60d09d8d1a9e11ba53fff983beb648d16a1d7c6fef7bf91c67bc562deb"` |
| revision | tag `v1.0.37` → commit `d4cb70582ba507b9265672792c0fc8a5f390b851` (`git ls-remote … refs/tags/v1.0.37`, one line, lightweight tag); commit date **2026-10-08T14:30:30Z**; subject `spec: only skip target roles if they appear in the same delegation path (#327)` |
| self-versioning | the document does not print `v1.0.37` in prose; its `spec_version` occurrences are format examples (`:712-713`, `:772`). The revision identity is the tag + commit + sha256 above, not an internal string |
| registry screen | `grep -c -i 'theupdateframework' corpus/SOURCES.md` → **0**; `grep -c 'https://raw.githubusercontent.com/theupdateframework'` → **0**. Adjacent registered rows do not cover this scope: `S600` (build reproducibility), `S602` (in-toto byproducts), `S603` (git-clone/`--shared`) |

**Located quote (replacement).** §*Update the snapshot role*, step 2, raw lines **1439-1441** (the
sentence starts mid-line 1439 after the bold step label). **20 words**:

> The hashes of the new snapshot metadata file MUST match the hashes, if any, listed in the trusted timestamp metadata.

Single-occurrence proof, normalisation stated exactly: `text = re.sub(r"\s+", " ", raw).strip()`
(i.e. every run of whitespace — line breaks *and* the two-space step indentation — becomes one
space), then `text.count(quote)`:

```
TUF-quote: words=20 count=1
expected_sentence_present_once_in_span: 1     # normalized rendering of raw lines 1439-1441
```

Uniqueness is semantic, not accidental: the near-twin at raw lines 1495-1498 is
`The hashes of the new targets metadata file MUST match the hashes, if any, listed in the trusted
snapshot metadata.` — same shape, different role pair, and it is a *different* string.

**Supporting located spans (not the admitted quote, cited in the `anchor` cell):**

- raw lines **1442-1444** state why the check is safe before the signature check: *"the hashes come
  from the timestamp role, which we have already verified in the previous step"* — the
  already-trusted-predecessor anchor, in the source's own words.
- raw lines **1346-1349** (root update, step 5): *"The version number of the new root metadata
  (version N+1) MUST be exactly the version in the trusted root metadata (version N) incremented by
  one, that is precisely N+1."* — refusal of any non-successor version.
- raw lines **727-728** (`VERSION` definition): *"Clients MUST NOT replace a metadata file with a
  version number less than the one currently trusted."* — an older record never displaces a newer
  trusted one.

## 4. What the source grounds — and what it does not

**Grounds (C2's missing half).** A new record is admitted only by reproducing hashes held by the
record that was verified first (`:1439-1444`), and a version that is not exactly the trusted version
plus one is refused as a rollback (`:1346-1349`, `:727-728`). Read against the counter: a
`# supersedes:` line is a *pointer*, and what retires a legacy receipt is the successor's replay, not
the header — the same shape as TUF's "hashes from the metadata verified in the previous step, before
the signatures of the new file are considered".

**Does not claim (limits that keep the mapping honest).**

- TUF never says a *command output* must be reproduced by re-running a command; its records are
  signed metadata files, not command receipts. The `# replay:` mechanism is the lane's.
- TUF does not define a textual `supersedes:` cross-reference; supersede is version monotonicity
  plus the hash chain across roles.
- TUF does not say `S600`'s or `S602`'s things: it is not a build-reproducibility definition and it
  says nothing about byproduct verification.
- The check is conditional — *"the hashes, **if any**"* — so the ground is about how an existing
  recorded digest is used, not a promise that every record carries one.

## 5. Proposed row cells (11 cells; id to be assigned by the L1)

Census at this seat's last read — **2026-11-04T13:23:17Z**, `corpus/SOURCES.md` sha256
`78b0a34c6ee60d26077256ff461dfc14c6fc0ed646f964ed293b11218b9a84e7`: **376 rows**, highest id
**S603**, `malformed=0`, candidate URL 2× (one row), `theupdateframework` 0×. Next unused id at that
reading: **S604** — the L1 must re-census before appending, because siblings are writing the
registry live (it moved twice during this seat; §9).

Exact cells, with the status pair given as the two honest alternatives (the contract: `mined` =
cited by ≥1 path in `used-by`):

| cell | value |
|---|---|
| `id` | `S604` (L1 assigns; next unused at the reading above) |
| `source` | `The Update Framework specification v1.0.37 — https://raw.githubusercontent.com/theupdateframework/specification/v1.0.37/tuf-spec.md` |
| `kind` | `spec` |
| `tier` | `A` — primary specification, scoped to the row's `scope`, never global |
| `scope` | `acceptance of a superseding metadata record: a new metadata file is admitted only when its bytes match hashes listed in the already-trusted metadata, and a version other than exactly the trusted version plus one is refused as a rollback` |
| `anchor` | `Update the snapshot role step 2, raw lines 1439-1441 (20-word located quote: The hashes of the new snapshot metadata file MUST match the hashes, if any, listed in the trusted timestamp metadata.), rationale raw lines 1442-1444, rollback and version raw lines 1346-1349 and 727-728; tag v1.0.37 = commit d4cb70582ba507b9265672792c0fc8a5f390b851 dated 2026-10-08; sha256 87c7136231b8cb3355736d8e7cfe88380d030cb2994ea283a19e78e03fb171ff; 76283 bytes, 1739 lines; two fetches byte-identical, HTTP 200, no redirect` |
| `teaches` | `A superseding record is admitted only when its bytes reproduce hashes held by the record verified first, and a version other than exactly N+1 is a rollback; a supersede link therefore names a check, not a proof.` |
| `status` | `queued` **iff** the knowledge sentence in §6 is **not** appended · `mined` **iff** it is appended to a knowledge entry |
| `opened` | `2026-11-04` (access date of the fetches in §3) |
| `recheck` | `365d` (matches the spec-at-a-tag convention of `S600`/`S602`; `on-release` is the `S603` convention if the L1 prefers tags-track-releases) |
| `used-by` | `—` **iff** `queued` · `corpus/knowledge/receipt-supersede-r87.md` **iff** `mined` and §6 is appended |

Paste-ready row (choose one status pair; 11 cells, no pipe inside any cell):

```
| S604 | The Update Framework specification v1.0.37 — https://raw.githubusercontent.com/theupdateframework/specification/v1.0.37/tuf-spec.md | spec | A | acceptance of a superseding metadata record: a new metadata file is admitted only when its bytes match hashes listed in the already-trusted metadata, and a version other than exactly the trusted version plus one is refused as a rollback | Update the snapshot role step 2, raw lines 1439-1441 (20-word located quote: The hashes of the new snapshot metadata file MUST match the hashes, if any, listed in the trusted timestamp metadata.), rationale raw lines 1442-1444, rollback and version raw lines 1346-1349 and 727-728; tag v1.0.37 = commit d4cb70582ba507b9265672792c0fc8a5f390b851 dated 2026-10-08; sha256 87c7136231b8cb3355736d8e7cfe88380d030cb2994ea283a19e78e03fb171ff; 76283 bytes, 1739 lines; two fetches byte-identical, HTTP 200, no redirect | A superseding record is admitted only when its bytes reproduce hashes held by the record verified first, and a version other than exactly N+1 is a rollback; a supersede link therefore names a check, not a proof. | queued | 2026-11-04 | 365d | — |
```

Field summary the seat spec asks for: **tier `A` · kind `spec` · status `queued` (or `mined`) ·
recheck `365d` · used-by `—` (or the C2 note) · access date `2026-11-04` · quote "The hashes of the
new snapshot metadata file MUST match the hashes, if any, listed in the trusted timestamp
metadata." (20 words, `tuf-spec.md:1439-1441`)**.

## 6. The ONE knowledge-entry sentence

Fully grounded by §3's quote and its two supporting spans; the lane's own rule (that the supersede
must be *earned by the replay*) already stands in `receipt-supersede-r87.md` rule 1 and is not
claimed as this source's:

> A successor record is admitted only by reproduction against the already-trusted predecessor: a new
> metadata file is accepted only when its bytes match the hashes listed in the metadata that was
> verified first, and a version other than exactly the trusted version plus one is refused as a
> rollback.

Append point if the L1 takes it: `corpus/knowledge/receipt-supersede-r87.md` §*What it holds*, as
the source-licensed ground for rule 1 — then the row's `status`/`used-by` become `mined` /
`corpus/knowledge/receipt-supersede-r87.md`. **I did not write that file.**

## 7. Gate paragraph (ready for the L1 to append to `corpus/lessons/round-87.md` §Gate)

> Round 87 bounded search, C2 ground — Question: what source grounds the rule that a legacy receipt
> retires only through a successor whose own body reproduces, i.e. that a superseding record is
> admitted only by verification against the record trusted first? Where: the round's candidate
> `https://reproducible-builds.org/docs/definition/` fetched twice 2026-11-04 (HTTP 200, no
> redirect, 37681 bytes, 3662 lines, sha256 `a558c89f…`, two fetches byte-identical, and identical
> to the committed r85 pin) is already `S600` with the identical URL *and* scope → excluded as a
> duplicate (the r86 search log records the same reason). Replacement opened: **The Update Framework
> specification v1.0.37**, raw
> `https://raw.githubusercontent.com/theupdateframework/specification/v1.0.37/tuf-spec.md` (HTTP
> 200, no redirect, 76283 bytes, 1739 lines, sha256 `87c7136231b8cb3355736d8e7cfe88380d030cb2994ea283a19e78e03fb171ff`,
> two fetches byte-identical; tag `v1.0.37` = commit `d4cb7058…` dated 2026-10-08). identified 2,
> screened 2 by fetch, included 1 as a proposed row (`S604`, L1 assigns), excluded 1 (the candidate:
> duplicate URL and scope of `S600`). Stop rationale: `S600` already grounds byte-comparison
> reproduction, `S602` the negative that a recorded body is not verified by default, `S603` the
> clone/`--shared` replay environment; TUF v1.0.37 grounds the remaining half — a new record is
> admitted only against hashes held by the record verified first, and a non-N+1 version is a
> rollback. Located quote: `tuf-spec.md:1439-1441` (20 words).

## 8. Gates run (commands and observed output)

**G1 — candidate fetch facts and stability.**

```
$ curl -sS -L --max-time 60 -o src.html -w '%{http_code} %{num_redirects} %{url_effective}\n' https://reproducible-builds.org/docs/definition/
200 0 https://reproducible-builds.org/docs/definition/
$ curl … -o src2.html …            # same URL
200 0 https://reproducible-builds.org/docs/definition/
$ cmp src.html src2.html && echo CMP-IDENTICAL
CMP-IDENTICAL
$ wc -c -l src.html ; sha256sum src.html src2.html
  3662  37681 src.html
a558c89f5f27dffa69fd1dc49904179b60233bcfdfc64807abfe1acf37518ebb  src.html
a558c89f5f27dffa69fd1dc49904179b60233bcfdfc64807abfe1acf37518ebb  src2.html
$ sha256sum corpus/evidence/sources-r85/rb-definition-1.html
a558c89f5f27dffa69fd1dc49904179b60233bcfdfc64807abfe1acf37518ebb   # same bytes as the r85 pin
```

**G2 — replacement fetch facts and stability.**

```
$ curl -sS -L --max-time 60 -o tuf.md -w '%{http_code} %{num_redirects} %{url_effective}\n' https://raw.githubusercontent.com/theupdateframework/specification/v1.0.37/tuf-spec.md
200 0 https://raw.githubusercontent.com/theupdateframework/specification/v1.0.37/tuf-spec.md
$ curl … -o tuf2.md … && cmp tuf.md tuf2.md && echo CMP-IDENTICAL
CMP-IDENTICAL
$ wc -c -l tuf.md ; sha256sum tuf.md tuf2.md
  1739  76283 tuf.md
87c7136231b8cb3355736d8e7cfe88380d030cb2994ea283a19e78e03fb171ff  tuf.md
87c7136231b8cb3355736d8e7cfe88380d030cb2994ea283a19e78e03fb171ff  tuf2.md
$ git ls-remote https://github.com/theupdateframework/specification refs/tags/v1.0.37
d4cb70582ba507b9265672792c0fc8a5f390b851	refs/tags/v1.0.37
$ curl -sS …/commits/d4cb7058… | python3 -I -c …
d4cb70582ba507b9265672792c0fc8a5f390b851 2026-10-08T14:30:30Z | spec: only skip target roles if they appear in the same delegation path (#327)
```

**G3 — registry screen (the seat's step 3).**

```
$ grep -c 'reproducible-builds.org/docs/definition' corpus/SOURCES.md      → 2   # one row + one search-log note
$ grep -c -i 'theupdateframework' corpus/SOURCES.md                        → 0
$ grep -c 'https://raw.githubusercontent.com/theupdateframework' …          → 0
$ grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md      → 376
$ highest id                                                                → S603
$ awk malformed count                                                       → 0
```

**G4 — quote is verbatim, inside the cap, and occurs once.**

```
TUF-quote: words=20 count=1                       # text = re.sub(r"\s+"," ",raw).strip()
expected_sentence_present_once_in_span: 1         # normalized rendering of raw lines 1439-1441
RB-quote(tag-stripped): words=9 count=1
RB-quote(markup-as-served): words=9 count=1 raw_line_start=196
```

**G5 — no lane write but this report.** `git -C <lane> status --porcelain` at report time shows
` M corpus/lessons/round-87.md` (a sibling's in-flight edit) plus the untracked
`.ufo/waves/round-87/w1/`, `w1.ready.dispatched`, `w1-validator.err` — none of mine except this
report inside `w1/`. No `git add`, no commit, no `jj`.

## 9. Revision honesty (the lane moved while this seat ran)

| moment | HEAD | `corpus/SOURCES.md` sha256 | note |
|---|---|---|---|
| start of seat (read) | `b9e6f68d887c570909c7bacc8bac86579d850d1d` | `c831bbae52962f740469413d5d790cc339ad8bcbe3657d59770a7dc741ffeff2` | working tree also ` M QUALITY.md`, ` M README.md`, ` M SOURCES.md`; S603 already present |
| report time | `728bc5f48363e668710579ed2b7822632383178a` | `78b0a34c6ee60d26077256ff461dfc14c6fc0ed646f964ed293b11218b9a84e7` | siblings committed the registry and the C2 note; `corpus/lessons/round-87.md` is modified in the worktree; row count unchanged at 376, highest still S603 |

The registry moved between two of this seat's own reads, so the proposed id (`S604`) is *derived*
from a census, not reserved: **re-census at append time**.

After this report body was written, HEAD advanced again to
`a42b1d795a7ebe9383f2421582182e2e341455bb` (`round-87: lesson integration — the seat's four findings
merged`); `corpus/SOURCES.md` stayed at `78b0a34c…`, so §5's census and the `S604` derivation still
describe the registry as of this report's last read.

Files read and **not** written, with the hashes I read: `contract.md` `bf208a44…`;
`count-c1.py` `e2ff9687…`; `count-c2.py` `264a43f0…`; `controls-r87.txt` `53d65a42…`;
`probe-r87.txt` `530e35e6…`; `SCORECARD.md` `6334569d…`; `round-86-verifier-spotcheck.md`
`820e5a49…`; `round-87.md` `3d6e56f1…`; `receipt-supersede-r87.md` `13f7695e…`; fleet `CORPUS.md`
`88556402…`; `corpus/evidence/sources-r85/rb-definition-1.html` `a558c89f…`.

## 10. Out of scope / not done (deliberate)

- **No append to `corpus/SOURCES.md`** and **no knowledge file** — the seat spec says the L1 appends;
  §5/§6 supply the text.
- **No pin copy into the lane.** The fetched bytes stay in scratch only (seat spec: *"copy nothing
  into the lane"*). The TUF bytes can be re-fetched from the tag and verified against the sha256
  above; if the L1 wants the lane's usual evidence pin, that `cp` is theirs to make.
- **No `corpus/README.md` coverage row**, no `## Gate` edit, no lesson rewrite — all owned by other
  seats/the L1 this round.
- **No correction to any existing row.** `S600`/`S602`/`S603` were read, not edited; append-only
  respected.
- **No commit, push, `git add`, or mutating `jj`**; the lane's L1 owns the commit.
- **No tool installed or upgraded.**

## 11. Known limits of this seat's work

- Only tag `v1.0.37` was opened; `main` may differ, and the row pins the tag, not `main`.
- Two fetches prove stability inside this seat's window only; the `365d` recheck cadence covers the
  rest. `raw.githubusercontent.com` resolves tag refs at fetch time, so the **sha256 is the pin**,
  not the URL alone.
- The C2 mapping is analogical and is labelled as such in §4: TUF's records are signed metadata
  files, not command receipts; TUF says nothing about re-running a command, and the `# replay:`
  mechanism is the lane's own. Tier `A` applies to the row's `scope` (metadata acceptance), not to
  "receipts" generally.
- The registry, the lesson and the C2 note were all moving during this seat; §9 records each hash I
  actually read. Anything a sibling changed after that reading is not represented here.
- I did not run the round's counters or controls and claim nothing about C1/C2's after-values; this
  seat's only measurements are the fetches, the registry greps and the quote proofs above.

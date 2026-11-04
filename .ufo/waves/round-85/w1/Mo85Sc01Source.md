# Mo85Sc01Source — round 85 w1 source pin (C2 receipt provenance)

Seat: scout, leaf member (no subagent dispatch; none spawned). Lane root
`/home/vgpnk/Projects/shokunin/mori-shokunin`; all access 2026-11-04 (the pin's `curl -sSI` head
carries `Date: Wed, 04 Nov 2026 11:03:41 GMT`). Detection and report only: no lane, OS, unit,
service, credential, harness or orchestration state was changed. No tool was installed — only
preinstalled `curl`, `sha256sum`, `cmp`, `wc`, `file`, `grep`, `awk`, `sed`, `python3` (stdlib)
were used, so the tooling-authorization clause has no install to record. No git/jj mutation was
run anywhere; the only git calls were read-only (`rev-parse HEAD`, `status --porcelain`,
`log --oneline`). Scratch `/fast/scratch/hyaku/mori-r85/Mo85Sc01Source/` was created for
screening copies and deleted before yield; nothing under `/tmp` was used.

Lane revision at write time (read-only observation, no judgment): `HEAD = ab2608655ea52ba6d151b3a31d69a3b18cd2b41e`
("round-85: freeze contract, three counters and do-nothing controls"), whose parent is the
entering revision `2cc4b1ae35a83e4fd3fc48bae842bdf38df2e80e`. `git status --porcelain --
corpus/evidence/sources-r85 .ufo/waves/round-85/w1 corpus/SOURCES.md` printed
`?? corpus/evidence/sources-r85/` and `?? .ufo/waves/round-85/w1/` only at entry, and
`grep -c 'S600' corpus/SOURCES.md` was `0` (rc 1). At my final re-check before yield a
**concurrent seat** had appended a `| S600 |` row at `corpus/SOURCES.md:382` plus a `rejected`
`S601` row for `arXiv:2404.09241`; neither is my write, and `corpus/SOURCES.md` remains
unmodified by me. §7b compares the landed S600 row with the one I recommend.

**Verdict.** **ADMIT** exactly one source as **S600**: `https://reproducible-builds.org/docs/definition/`
("Definitions", reproducible-builds.org). It states the question's two halves in two adjacent
paragraphs: a build is reproducible when the same source, build environment and build instructions
let **any party** recreate **bit-by-bit identical copies** of the artifacts (:175-177), and "The
reproducibility of artifacts is **verified** by bit-by-bit comparison", normally with
"cryptographically secure hash functions" (:196-197). The page says nothing about receipts, commands,
commits or sha256, so it grounds the *criterion* (a digest comparison is verification) and not the
C2 grammar itself — that construction stays the lane's, and §5 measures the gap. Three pin fetches
are byte-identical (sha256 `a558c89f…`); two named screening candidates plus three same-question
pages were fetched and excluded with reasons (§6). The r84-refused `arXiv:2404.09241` is still
reachable, byte-identical to the r84 screening digest, and its full abstract still states **no**
bias half and no adjudication procedure: **no flip** (§8).

| disposition | id | carrier | what it grounds |
|---|---|---|---|
| ADMIT | **S600** | reproducible-builds.org "Definitions" — pinned at `corpus/evidence/sources-r85/rb-definition-{1,2,3}.html` | any party recreating bit-identical artifacts from the same inputs, and verification of reproducibility by bit-by-bit comparison with cryptographically secure hash functions |
| EXCLUDE (screened, not pinned) | — | Debian wiki `ReproducibleBuilds/About` | only the recreation half; no comparison or hash verification sentence |
| EXCLUDE (screened, not pinned) | — | Wikipedia `Reproducible_builds` | tertiary restatement of the definition half; no verification-method statement |

## 1. Files produced

| absolute path | sha256 | bytes | newlines | notes |
|---|---|---|---|---|
| `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/evidence/sources-r85/rb-definition-1.html` | `a558c89f5f27dffa69fd1dc49904179b60233bcfdfc64807abfe1acf37518ebb` | 37681 | 3662 | fetch 1 of 3 |
| `.../sources-r85/rb-definition-2.html` | `a558c89f5f27dffa69fd1dc49904179b60233bcfdfc64807abfe1acf37518ebb` | 37681 | 3662 | fetch 2 of 3 |
| `.../sources-r85/rb-definition-3.html` | `a558c89f5f27dffa69fd1dc49904179b60233bcfdfc64807abfe1acf37518ebb` | 37681 | 3662 | fetch 3 of 3 |
| `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-85/w1/Mo85Sc01Source.md` | this report | — | — | — |

The three copies are byte-identical: `cmp rb-definition-1.html rb-definition-2.html` and
`cmp rb-definition-1.html rb-definition-3.html` both exited 0 (chained, printed `ALL_IDENTICAL`).
`corpus/evidence/sources-r85/` did not exist at entry; I created it with `mkdir -p` and at my
write it held exactly these three files (no screening copy is pinned, matching the r84 convention —
the screened pages' digests and quotes are recorded in §6 instead). A concurrent seat has since
added `arXiv-2404.09241-abs.html` (40386 bytes, sha256
`4bcb20b23ad5046657a65a29595517da973128a289ff75ba13ad8926c5511a80`) for the S601 refusal; that
file is not my write.

Byte geometry of the pin (`file`, `grep -c $'\r'`, `awk 'END{print NR}'`, `wc -l`,
`tail -c 1 | xxd -p`, `grep -c -P '[^\x00-\x7F]'`): `HTML document, Unicode text, UTF-8 text`;
CR count `0` (LF-only); `awk NR` 3662 and `wc -l` 3662 (last byte `0a`, so the final record is
newline-terminated); exactly `1` non-ASCII line, `:3631`, the CC BY-SA 4.0 footer link (a
non-breaking space).

## 2. Fetch receipts (pinned)

All three fetches ran from `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/evidence/sources-r85`
with the same command shape — no `-L`, so a redirect would have been written as a 3xx body:

```
$ for i in 1 2 3; do curl -sS -o "rb-definition-$i.html" \
    -w "fetch=$i http=%{http_code} size=%{size_download} time=%{time_total}\n" \
    "https://reproducible-builds.org/docs/definition/"; done
fetch=1 http=200 size=37681 time=0.952927
fetch=2 http=200 size=37681 time=1.081831
fetch=3 http=200 size=37681 time=1.116956
```

Every fetch is `HTTP 200` with `size=37681`. No redirect: `-L` was not passed, the status is 200
(never 3xx), and the head below carries no `Location:` header. No `Content-Encoding` is present in
the response (`curl` sent no `Accept-Encoding`), so the 37681 bytes are the identity-encoded body
and `size_download` equals `Content-Length` exactly — there is no decompression step between the
wire and the pinned bytes. The three fetches spanned 3.99 s of wall time and still hashed
identically, so the page was stable across the access window.

```
$ curl -sSI https://reproducible-builds.org/docs/definition/
HTTP/1.1 200 OK
Date: Wed, 04 Nov 2026 11:03:41 GMT
Server: Apache/2.4.69 (Debian)
Strict-Transport-Security: max-age=15552000
Last-Modified: Mon, 02 Nov 2026 16:07:38 GMT
ETag: "9331-65f4d584f6db0"
Accept-Ranges: bytes
Content-Length: 37681
Vary: Accept-Encoding
Content-Type: text/html; charset=utf-8
```

Both freshness validators are present and internally consistent with the pinned body:
`0x9331 = 37681` is the byte size the fetches report, and the ETag's second component
`0x65f4d584f6db0` µs = `2026-11-02T16:07:38.984880Z`, i.e. the `Last-Modified` second. The server's
last-modified time for the page is two days before this access, so the pinned bytes are the
current server generation rather than a stale proxy copy; the pin records that validator so a
future seat can detect a change without re-reading the body.

## 3. Located sentences (raw line numbers in the pinned copy)

`grep -n` over `rb-definition-1.html` located exactly one occurrence of each target sentence.

Definition sentence — raw lines **175-177**, under `<h2 id="when-is-a-build-reproducible">` at
line 174:

```
175: <p>A build is <strong>reproducible</strong> if given the same source code, build environment
176: and build instructions, any party can recreate bit-by-bit identical copies of
177: all specified artifacts.</p>
```

Text content (26 words): "A build is reproducible if given the same source code, build environment
and build instructions, any party can recreate bit-by-bit identical copies of all specified
artifacts." The 21-word clause after the lead-in — "given the same source code, build environment
and build instructions, any party can recreate bit-by-bit identical copies of all specified
artifacts" — is also verbatim-contiguous.

Verification sentence — raw lines **196-197**, under `<h2 id="explanations">` at line 184:

```
196: <p>The reproducibility of artifacts is <strong>verified</strong> by bit-by-bit comparison. This
197: is usually performed using cryptographically secure hash functions.</p>
```

Text content (18 words): "The reproducibility of artifacts is verified by bit-by-bit comparison.
This is usually performed using cryptographically secure hash functions."

The row's single quote is the 18-word verification sentence (≤25 words as required); the
definition sentence is cited by its raw range `:175-177` so a reader can verify the independence
clause without a second quote in the cell. The word "independently" does **not** occur anywhere in
the page (`independ` → 0 hits); the page's independence expression is **"any party"**, which occurs
once, in the definition sentence.

Supporting location for the authors'/distributors framing (raw lines 179-182, one paragraph):
"The relevant attributes of the build environment, the build instructions and the source code as
well as the expected reproducible artifacts are defined by the authors or distributors." This is
what makes the artifact the graded object and the comparison the check, rather than a claim by the
builder.

## 4. Page identity

- `<title>` line 5: `Definitions &mdash; reproducible-builds.org`; `<h1>` line 172: `Definitions`.
- Section headings: line 174 `When is a build reproducible?`; line 184 `Explanations`.
- License footer line 3631: content licensed under CC BY-SA 4.0 — quoting with attribution is
  permitted, which the registry row and the knowledge page rely on.
- The site's docs sidebar (lines 3321-3435) links two related pages, `/docs/checksums/` (:3337) and
  `/docs/embedded-signatures/` (:3435). The checksums page was screened (§6); the signatures page
  was not fetched and is not needed for S600's anchor.

## 5. What the pinned page does NOT say (measured)

Measured over the article body (raw lines 170-210, 1458 characters, 203 words) and over the whole
file, case-insensitive (`re.findall`, `re.I`):

| token | body | whole file | reading |
|---|---|---|---|
| `receipt` | 0 | 0 | the page defines no receipt form |
| `command` | 0 | 2 | not in the body; both hits are the substring inside the nav link "Commandments of reproducible builds" (:851) — no command provenance |
| `commit` | 0 | 0 | no VCS commit binding |
| `sha256` | 0 | 0 | names "hash functions", never an algorithm or a digest line |
| `checksum` | 0 | 2 | only the sidebar link "Cryptographic checksums" |
| `signature` | 0 | 2 | only the sidebar link "Embedded signatures" |
| `independ` | 0 | 0 | independence is "any party" |
| `deterministic` | 0 | 3 | not in the body |
| `revision` | 1 | 1 | line 186, "a checkout from version control at a specific revision" — a source-code sense, not a graded-receipt sense |
| `any party` | 1 | 1 | line 176 |
| `verif` | 1 | 2 | line 196 `verified`; the other hit is the sidebar heading "Verification" (:3321) |
| `hash` | 1 | 1 | line 197, "cryptographically secure hash functions" |

Consequences for C2, stated as inference, not as source text:

1. S600 grounds the **criterion**: reproducibility is established by an outside party recreating
   bit-identical bytes from the same inputs, and the check is a bit-by-bit comparison, normally a
   cryptographic hash. A receipt that binds its command, its graded revision and the sha256 of the
   subject bytes at that revision is therefore a *verification artifact* — the digest is the
   comparison S600 names, and the revision names the inputs.
2. S600 does **not** ground the grammar. The page never says a receipt must name a command, never
   binds a digest to a VCS revision, and never says a hash covers one file rather than a build
   output set. The `# cmd:` / `# rev:` / `# counter-sha256:` header shape, the ancestry rule for
   `# rev:`, and the per-path binding are the lane's construction; `corpus/knowledge/receipt-provenance-r85.md`
   should attribute them to the lane and cite S600 for the criterion only.
3. S600 does not promise that a matching digest proves intent, absence of tampering elsewhere, or
   determinism at another revision. "Any party" bounds who may verify, not what a match proves
   beyond the compared bytes.

## 6. Screening — two named candidates plus three same-question pages

All screening copies were fetched into scratch (now deleted); status, size and sha256 are recorded
here so a re-fetch can be compared, and each copy's exact quote is reproduced below. None is
pinned. All fetches returned HTTP 200.

| URL | bytes | sha256 | disposition | reason |
|---|---|---|---|---|
| `https://reproducible-builds.org/docs/definition/` | 37681 | `a558c89f…` | **INCLUDED (S600)** | states both halves: any party recreates bit-identical copies (:175-177), verification is bit-by-bit comparison with cryptographically secure hash functions (:196-197) |
| `https://wiki.debian.org/ReproducibleBuilds/About` | 69960 | `a9b4374411040859f9ddf239fb71ab5a568773e40d434f42c91b7f648ab7aa78` | EXCLUDED | states the recreation half only — "The idea of “deterministic” or “reproducible” builds is to empower anyone to verify that no flaws have been introduced during the build process by reproducing byte-for-byte identical binary packages from a given source." (33 words, raw line 149) — and never states the comparison method or hash verification; it is a legacy page flagged "Got a spare moment? Please migrate this to our new webpages" with `last modified 2020-08-05 12:23:18` (line 168), and adds no fact S600 lacks |
| `https://en.wikipedia.org/wiki/Reproducible_builds` | 138113 | `0f781c4c15361fa5c9270e1c847408099a0255db20f9c8323a05d1089409134a` | EXCLUDED | tertiary encyclopedia; its 18-word definition sentence ("A reproducible build produces identical output when repeated with the same source code, build environment, and build instructions.", raw line 645) restates S600's own project definition and cites it, and the page carries no sentence on verifying by byte comparison with cryptographic hashes |
| `https://mesonbuild.com/Reproducible-builds.html` | 9115 | `138213bacd1a7a697e6c57567c37d17ed50730f1078eaf0b70431410195f7c50` | EXCLUDED | build-tool page that quotes the reproducible-builds project site and paraphrases only the definition half ("their outputs are bitwise identical to each other", raw lines 230-231); no comparison or hash verification statement; secondary restatement of the same project S600 already is |
| `https://reproducible-builds.org/events/berlin2016/reproduciblebuildsdefinition/` | 31401 | `ddd3d20197ea0a5ab0f287d416cdf053c90002a2eb1d68431be15a357988ffe9` | EXCLUDED | event minutes; the bullet "Output - bit by bit identical output, verifiable by a checksum." (11 words, line 2053) has the checksum half but no "any party"/same-environment definition sentence and no cryptographic-secure qualifier; a weaker fragment of S600's own site |
| `https://reproducible-builds.org/docs/checksums/` | 37113 | `fbf39a1700697ef3d44ce96a109ece6c56c2d294928fd0c911146ad001062c5f` | EXCLUDED as a row | same site and tier; answers "How can users know that the build they just made has successfully reproduced the original build?" (raw lines 174-175) with "The easiest way is to make sure that the build outputs are always byte-for-byte identical." (15 words, raw lines 177-178) but names plain checksums, not cryptographic secure hashes, and states no definition; adds no fact beyond S600 and would duplicate the same project |

Stop rationale: **identified 6, screened 6 (all HTTP 200, all fetched), included 1, excluded 5.**
The question is closed: one tier-A primary page states both halves; every other candidate either
restates one half, restates the same project, or is tertiary. No further search is warranted for
this question; the remaining uncertainty is not source coverage but the inference gap in §5.2,
which no source can close because the grammar is the lane's.

## 7. Registry row I recommend (scribe-owned; I did not edit `corpus/SOURCES.md`)

`corpus/SOURCES.md` is unmodified by this seat. The exact row I recommend (11 cells; id
placeholder `S600`; at entry `S599` was the highest id and no `S600` row existed — see §7b for the
concurrently landed row):

| S600 | Reproducible Builds — Definitions — https://reproducible-builds.org/docs/definition/ | docs | A | the definition of a reproducible build and its verification method only — same source, build environment and instructions let any party recreate bit-identical artifacts, and reproducibility is verified by bit-by-bit comparison, usually with cryptographically secure hash functions; not any receipt format, command or revision binding, digest tooling, determinism at another revision, or lane claim | "When is a build reproducible?" lines 175-177 and "Explanations" lines 196-197 of the pinned copy; quote lines 196-197 "The reproducibility of artifacts is verified by bit-by-bit comparison. This is usually performed using cryptographically secure hash functions." (18 words); the definition clause at 175-177 is "given the same source code, build environment and build instructions, any party can recreate bit-by-bit identical copies of all specified artifacts" (21 words); copy corpus/evidence/sources-r85/rb-definition-{1,2,3}.html — three fetches byte-identical (`cmp` clean), 37681 bytes, 3662 newlines, sha256 a558c89f5f27dffa69fd1dc49904179b60233bcfdfc64807abfe1acf37518ebb, HTTP 200, no redirect, Last-Modified Mon, 02 Nov 2026 16:07:38 GMT, ETag "9331-65f4d584f6db0"; opened 2026-11-04 | A reproducible artifact is established when any party recreates bit-identical bytes from the same source, environment and build instructions, and the check is a bit-by-bit comparison, normally a cryptographic hash; a receipt that binds its command, its graded revision and the sha256 of the subject bytes at that revision therefore records a verification, not an assertion. Lane rule: a digest binds only the bytes hashed at that revision — never intent, never determinism at another revision, never the subject's own report. | mined | 2026-11-04 | on-release | corpus/knowledge/receipt-provenance-r85.md |

Two `rejected` rows are recommended for the two named screening candidates, so the refusals are
recorded rather than left as prose (the r84 verifier's D84-3 defect; scribe assigns the next free
ids and may fold them into one round-85 bounded-search paragraph):

| next free id | Debian wiki — ReproducibleBuilds/About — https://wiki.debian.org/ReproducibleBuilds/About | docs | B | legacy wiki page on Debian's reproducible-builds rationale | raw line 149, 33-word sentence "The idea of “deterministic” or “reproducible” builds is to empower anyone to verify that no flaws have been introduced during the build process by reproducing byte-for-byte identical binary packages from a given source."; copy not pinned (screening digest a9b43744…; 69960 bytes; 200) | REJECTED: states only the recreation half and no comparison or cryptographic-hash verification sentence; legacy page marked for migration, last modified 2020-08-05; adds no fact S600 lacks. flip: a revision states the verification method and the page is re-pinned with a located quote. | rejected | 2026-11-04 | 180d | — |
| next free id | Wikipedia — Reproducible builds — https://en.wikipedia.org/wiki/Reproducible_builds | community | C | encyclopedia article on reproducible builds | raw line 645, 18-word sentence "A reproducible build produces identical output when repeated with the same source code, build environment, and build instructions."; copy not pinned (screening digest 0f781c4c…; 138113 bytes; 200) | REJECTED: tertiary restatement of S600's own project definition, citing it; no sentence on verification by byte comparison with cryptographic hashes; not admissible as evidence when the primary is available and pinned. flip: never as evidence while S600 stands; only as a secondary explainer with an independent hash-verification statement. | rejected | 2026-11-04 | 365d | — |

The round-85 bounded-search paragraph the scribe should append:
Question: what source states that reproducibility of an artifact is verified by comparing
independently rebuilt bytes, so that a receipt binding command + revision + subject-bytes digest
is a verification artifact rather than an assertion? Where: `reproducible-builds.org/docs/definition/`
opened 2026-11-04 and pinned three times (`corpus/evidence/sources-r85/rb-definition-{1,2,3}.html`,
37681 bytes, 3662 newlines, sha256 a558c89f…, byte-identical, HTTP 200, ETag `"9331-65f4d584f6db0"`,
Last-Modified 2026-11-02); identified 6, screened 6, included 1 as S600, excluded 5 (Debian
`ReproducibleBuilds/About`; Wikipedia `Reproducible_builds`; Meson `Reproducible-builds`;
Berlin-2016 `reproduciblebuildsdefinition`; same-site `docs/checksums/`).

`corpus/knowledge/receipt-provenance-r85.md` does not exist yet (checked at write time); the
`used-by` cell points at that planned path, not at a file this seat could verify.

### 7b. Concurrent landing — the S600 row on disk is not my write

At final re-check `corpus/SOURCES.md:382` carries a `| S600 |` row (11 cells, `status` `mined`,
`used-by` `corpus/knowledge/receipt-provenance-r85.md`) and `:383` a `| S601 |` row for
`arXiv:2404.09241` with `status` `rejected` — the D84-3 discharge, consistent with §8's no-flip
measurement. The S601 row's pinned copy `corpus/evidence/sources-r85/arXiv-2404.09241-abs.html`
exists and its stated sha256 `4bcb20b2…` matches the bytes I re-fetched. I did not write either
row.

The landed S600 row and my recommendation agree on id, source URL, kind (`docs`), tier (`A`),
status (`mined`), `opened` (2026-11-04) and `used-by`; they differ in four cells, in ascending
severity:

| cell | landed row | my recommendation | why |
|---|---|---|---|
| `recheck` | `365d` | `on-release` | the page's `Last-Modified` moved to 2026-11-02, two days before the pin; a definition page that changes is a recheck-on-change source, not a yearly spec. Recommendation only. |
| `anchor` | cites `rb-definition-1.html` only; omits the `etag`/`last-modified` validators | cites the three pinned copies, both validators (`ETag "9331-65f4d584f6db0"`, `Last-Modified` 2026-11-02) and the `cmp`/`sha256` identity | without the validators a future seat cannot tell whether a 200 response is the same generation of the page. The landed claim "three fetches (this seat, the scout and the freeze pin) byte-identical" is supported as far as I can measure: the sibling copy `.ufo/waves/round-85/evidence/rb-definition.html` hashes `a558c89f…`, equal to my three. |
| `teaches` | "a receipt certifies that property by naming the tree and the digest rather than asserting a run" | same inference plus the limit: the page names no receipt, command, commit or digest algorithm, so the grammar is the lane's | as written the cell attributes the receipt form to the source; §5 measures that the source contains none of those tokens (0/0/0/0), and the knowledge page is where the inference must be labelled. |
| `scope` | "the definition of a reproducible build and the byte-comparison verification rule, as the ground of a receipt that binds a revision and a digest" | the same two sentences, with the explicit exclusion "not any receipt format, command or revision binding" | "as the ground of a receipt that binds a revision and a digest" overstates a page that never mentions a receipt or a revision binding; the C2 claim's own honesty (its `limits=` header) rests on this distinction. |

The `teaches` and `scope` cells both carry the receipt inference past what the page states; the
`scope` phrase is the one I would correct first because it reads as the page's own scope ("as the
ground of a receipt that binds a revision and a digest"), while the page mentions no receipt, no
command and no revision binding (§5). That is a wording fix inside the scribe's cell, not a new
source: the row's id, URL, kind, tier, status and `used-by` are already right.

## 8. `arXiv:2404.09241` recheck — reachable, unchanged, **no flip**

Re-fetched 2026-11-04 with `curl -sSL -o … -w 'http=%{http_code} size=%{size_download} final=%{url_effective}'`:
`http=200 size=40386 final=https://arxiv.org/abs/2404.09241` — the final URL equals the requested
URL, so the HTTP 200 is the abs page itself and not a redirect target. sha256
`4bcb20b23ad5046657a65a29595517da973128a289ff75ba13ad8926c5511a80`, byte-identical to the digest the
r84 verifier recorded for the same screening copy (`corpus/lessons/round-84-verifier-spotcheck.md:163`),
so the page bytes have not changed since r84. The paper's own metadata is `v1`, `updated`
2024-04-14T13:04:10Z.

The full abstract (blockquote, 1190 characters, 170 words; also carried in the
`citation_abstract` meta at line 39) contains: `bias` **0** hits, `adjudicat` **0** hits, the word
`cost` **0** hits. Its cost wording remains the one line the r84 refusal named — equivalent mutants
"hamper this process" — and its findings are a rate plus a human-performance result: "less than 10
% of manually created mutants are equivalent" and "a significant portion of developers struggle to
accurately identify equivalent mutants". It states no bias half and no adjudication procedure.

**no flip.** The r84 flip condition ("a revision states the cost-and-bias half for a gate's tally
or an adjudication procedure, as a freshly pinned and quoted row") is not met by the current bytes;
the refusal and its reason stand unchanged.

## 9. Freshness and remaining unknowns

- Freshness: pin fetched 2026-11-04; `Last-Modified: Mon, 02 Nov 2026 16:07:38 GMT`; ETag
  `"9331-65f4d584f6db0"` decodes to that mtime and the pinned byte size, so the pin is the page's
  current generation. Recheck cadence recommended: `on-release` (project documentation page with no
  versioned releases of its own; the site is the project).
- Unknown 1: the page defines no receipt, and no command/revision binding appears anywhere in it
  (§5). C2's grammar is the lane's construction; the source grounds the criterion only.
- Unknown 2: the page binds a hash to "artifacts" as "the parts of the build results that are the
  desired primary output" (lines 181-182), not to a single repo path at a revision. The
  repo-relative-path binding in `# counter-sha256:` is the lane's narrowing, and the knowledge page
  must state it as such.
- Unknown 3: no second tier-A source stating the digest-at-revision binding was found in the six
  screened pages; the screened set is closed above, so this is a source-coverage limit, not an
  unsearched gap.
- Not verified by this seat (outside its question): whether the C2 counter's ancestry rule, header
  grammar and `mismatch` accounting match the frozen contract — that is the C2 executor's and
  reviewer's measurement, not this pin's.

## 10. Compliance

- Writes: exactly `corpus/evidence/sources-r85/rb-definition-{1,2,3}.html` and this report. No
  write to `corpus/SOURCES.md`, `.ufo/state/`, `MANIFEST.json`, `SCORECARD.md`, `LOG.md`,
  `.scratch/`, the fleet root, another lane, or any PATH directory. No `~/.local/bin` change.
- No commit, push, checkout, reset, stash or mutating `jj` in the lane repo; read-only git only.
- Scratch: `/fast/scratch/hyaku/mori-r85/Mo85Sc01Source/` (screening copies `wiki_debian_…html`,
  `en_wikipedia_…html`, `mesonbuild_…html`, `reproducible-builds_org_events_…html`, `rb-checksums.html`,
  `arxiv_org_abs_2404_09241.html`, `arxiv-api.xml`) deleted before yield; no `/tmp` path is cited.

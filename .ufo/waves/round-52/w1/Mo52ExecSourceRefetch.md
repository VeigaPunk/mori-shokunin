# Mo52ExecSourceRefetch — w1 source re-opening (C2 S497–S501)

Seat: executor, source re-opening only. Scope: re-fetch the five v7.2 source URLs of S497–S501 live, compare HTTP
status / byte count / sha256 against the frozen copies in `corpus/evidence/sources-r52/`, test each of the entry's
28 quotes against the live bytes with whitespace collapsed, and confirm tag `v7.2` resolves. No file other than this
report was written inside the lane; nothing was installed or upgraded.

Scratch: `/fast/scratch/hyaku/mori-r52/Mo52ExecSourceRefetch/` (TMPDIR exported to its `tmp/`), 220K peak, removed
at the end of the run. No clone or work tree was created; no mutating git or jj command was issued.

Tooling used, already present: `git 2.56.0`, `curl 8.23.0`, `python3 3.14.8`.

## 1. Five source URLs, fetched live (2026-10-27T00:1xZ)

Command shape, run from the scratch dir, once per URL (`-sSL`, no redirect followed away from the host, all five
answered directly with `num_redirects=0`):

```
curl -sSL --max-time 90 -o <scratch>/live/<n>.bin -w '%{http_code} %{size_download} %{num_redirects} %{url_effective}' <url>
```

| n | source | path at v7.2 | HTTP | curl rc | bytes | sha256 of live body | = frozen | = committed |
|---|---|---|---|---|---|---|---|---|
| 1 | S497 | `Documentation/mm/overcommit-accounting.rst` | 200 | 0 | 2647 | `767ab88153c4494e54fcf2db4e5bd01921d6bd8350f1596ada508cb5e4b4927f` | yes | yes |
| 2 | S498 | `Documentation/admin-guide/sysctl/vm.rst` | 200 | 0 | 42424 | `bf8ca0265fefc019250697b6ee47a0679709b2ee45f4d1893b3dfd95c1f8c1ce` | yes | yes |
| 3 | S499 | `mm/util.c` | 200 | 0 | 43913 | `e702754c45bd7bd69e5da22a6505c9c1016eaafe6e883b746cc3cdbd413ebe7c` | yes | yes |
| 4 | S500 | `include/linux/mman.h` | 200 | 0 | 4265 | `d7bf787c910d9a7cbabee3a50c512ce3aad78d63659b0c968adca16b5916b058` | yes | yes |
| 5 | S501 | `mm/mmap.c` | 200 | 0 | 51223 | `449b858385c7ece0ff88a8b41893efadb70a437fb8585a296c4ef0461a4c1545` | yes | yes |

All five live bodies are byte-identical to (a) the sha256 frozen in `count-c2.py` `COPIES` and in
`evidence/freeze-sha256.txt`, and (b) the bytes committed under `corpus/evidence/sources-r52/`. Committed byte counts
equal the live byte counts exactly (2647 / 42424 / 43913 / 4265 / 51223), so no line-ending or trailing-byte drift.

Committed copies also equal the lane's data commit and its work tree:

```
$ for f in <entry> <five copies>; do git -C $LANE show 8524904adb25e44f24d9f25aac7eae909625c18c:$f | sha256sum;
                                     sha256sum $LANE/$f; done
SAME corpus/knowledge/overcommit-commit-limit-r52.md         committed=7cec492566f5c93cf13829c0298d8b3f1a034466671120534ac3838bae656447 worktree=(same)
SAME corpus/evidence/sources-r52/overcommit-accounting.rst.v7.2 767ab881…(same) both
SAME corpus/evidence/sources-r52/vm.rst.v7.2                     bf8ca026…(same) both
SAME corpus/evidence/sources-r52/util.c.v7.2                     e702754c…(same) both
SAME corpus/evidence/sources-r52/mman.h.v7.2                     d7bf787c…(same) both
SAME corpus/evidence/sources-r52/mmap.c.v7.2                     449b8583…(same) both
```

## 2. Tag `v7.2` resolution

The literal command named by the seat did not complete on this host:

```
$ timeout 100 git ls-remote https://github.com/torvalds/linux refs/tags/v7.2
rc=124 elapsed=100s   (stdout empty, stderr empty)
$ GIT_TERMINAL_PROMPT=0 timeout 60 git -c protocol.version=2 ls-remote https://github.com/torvalds/linux refs/tags/v7.2
rc=124 elapsed=60s    (stdout empty)
```

So: **UNVERIFIED by `git ls-remote`** — the refs advertisement round-trip did not finish inside 100 s and 60 s. It is
not a DNS or egress failure: the same host reached `raw.githubusercontent.com` and `api.github.com` in under a second
in the same session.

Resolved by the GitHub refs API instead:

```
$ curl -sS --max-time 40 -o api-tag.json -w 'http=%{http_code} bytes=%{size_download}\n' \
    https://api.github.com/repos/torvalds/linux/git/ref/tags/v7.2
http=200 bytes=362
{"ref": "refs/tags/v7.2", "object": {"sha": "237a1c39e8dfd3e1c6f1f023eea37a48ec04cc63", "type": "tag"}}

$ curl -sS --max-time 40 https://api.github.com/repos/torvalds/linux/git/tags/237a1c39e8dfd3e1c6f1f023eea37a48ec04cc63
tagger: 2026-08-16T21:32:26Z
target: commit 8d3ae59288f1e7d58d76558a6ee96d533bc5019f
message: Linux 7.2  (followed by a PGP signature block)
```

Tag resolves: annotated tag object `237a1c39e8dfd3e1c6f1f023eea37a48ec04cc63`, tagged `2026-08-16T21:32:26Z`, message
`Linux 7.2`, peeling to commit `8d3ae59288f1e7d58d76558a6ee96d533bc5019f`.

Independent corroboration that the five copies are the tag's own bytes, not merely today's body of a URL: the git blob
id of each committed copy equals the blob id GitHub reports for that path at the tag's peeled commit `8d3ae592`:

| path | `git hash-object <committed copy>` | blob at `8d3ae592` | HTTP |
|---|---|---|---|
| `Documentation/mm/overcommit-accounting.rst` | `e2263477f6d502e594e8b8800d26fc37aebfb482` | same | 200 |
| `Documentation/admin-guide/sysctl/vm.rst` | `b9b0c218bfb4400b38843821685a32d8a5721b9e` | same | 200 |
| `mm/util.c` | `34cb43b3eaa4c3e9fb5074b31fb5553064c0614c` | same | 200 |
| `include/linux/mman.h` | `389521594c69c2fafcd6975434b7b2f09db35db5` | same | 200 |
| `mm/mmap.c` | `2311ae7c2ff45c7d6a84633fa5c8828ba0827eb0` | same | 200 |

Command per row: `curl -sS --max-time 30 "https://api.github.com/repos/torvalds/linux/contents/<path>?ref=8d3ae59288f1e7d58d76558a6ee96d533bc5019f"`.
First attempt returned an empty `sha` for three paths (three API calls inside ~2 s, `rate_limit` reading
`remaining: 23` after the loop); the re-run with 2 s spacing returned 200 and a matching sha for all five. The empty
values were congestion on the API, not a content difference — the same three paths matched on retry.

## 3. All 28 quotes against the live bytes

Method, identical to the frozen counter's own extraction so the table is comparable row-by-row with
`evidence/c2-hashes-at-data.txt`: load `count-c2.py` as a module, take `parse_claims()` rows, take the single
`` `span` `` of the quote cell, apply the same unescape the counter applies (the escaped pipe reads as a plain pipe),
then `re.sub(r"\s+", " ", …)`, and test containment against `normalise_text()` of the live body. Offsets below are
character offsets into the whitespace-collapsed live text, not source byte offsets.

| row | hash | source | quote words | occurs in live bytes | occurs in committed copy | live offset (collapsed) |
|---|---|---|---|---|---|---|
| 1 | `9afaa81505da` | S497 | 15 | yes | yes | 134 |
| 2 | `61b7677d56fe` | S497 | 24 | yes | yes | 568 |
| 3 | `93b4fe285dc7` | S497 | 23 | yes | yes | 737 |
| 4 | `3b02f6680556` | S497 | 10 | yes | yes | 1283 |
| 5 | `921c2e511e09` | S497 | 8 | yes | yes | 1710 |
| 6 | `e37e65e64a4c` | S497 | 13 | yes | yes | 1852 |
| 7 | `7b2fc298698e` | S497 | 10 | yes | yes | 2550 |
| 8 | `43cf2a78acdd` | S498 | 22 | yes | yes | 29638 |
| 9 | `35d642f1d0d9` | S498 | 18 | yes | yes | 29777 |
| 10 | `fcd0e7a78872` | S498 | 22 | yes | yes | 30352 |
| 11 | `5c40f6fa5c62` | S498 | 22 | yes | yes | 29426 |
| 12 | `00e2a9db523b` | S498 | 19 | yes | yes | 36386 |
| 13 | `bfb15534fa5e` | S498 | 22 | yes | yes | 2213 |
| 14 | `28d3042fded0` | S499 | 12 | yes | yes | 22927 |
| 15 | `a75ce7619818` | S499 | 9 | yes | yes | 22835 |
| 16 | `309f4487d8b6` | S499 | 10 | yes | yes | 24967 |
| 17 | `cddcf1bc062f` | S499 | 20 | yes | yes | 24773 |
| 18 | `967021950067` | S499 | 6 | yes | yes | 25376 |
| 19 | `41934e8b2887` | S499 | 9 | yes | yes | 25099 |
| 20 | `ca2418460394` | S499 | 13 | yes | yes | 25491 |
| 21 | `9cb0e908f997` | S499 | 6 | yes | yes | 19521 |
| 22 | `2d64007fa0dc` | S499 | 13 | yes | yes | 20413 |
| 23 | `02f5bfd6be3b` | S500 | 10 | yes | yes | 1518 |
| 24 | `ff0d23e9fde8` | S500 | 8 | yes | yes | 1642 |
| 25 | `0fbd62f51ce8` | S501 | 15 | yes | yes | 14543 |
| 26 | `d7a1dc88dcb3` | S501 | 14 | yes | yes | 14673 |
| 27 | `10dc80bb5b2e` | S501 | 6 | yes | yes | 39779 |
| 28 | `42295e410c2b` | S501 | 6 | yes | yes | 40359 |

`QUOTES_TOTAL 28 / MISSING_IN_LIVE 0 / MISSING_IN_COMMITTED 0` (script exit 0). Every quote is 6–24 words, inside the
frozen 6–25 window. All 28 claim hashes computed from the work-tree entry equal the 28 hashes in
`evidence/c2-hashes-at-data.txt` (`mine 28 receipt 28 both 28`, no hash in one set only), so this table indexes the
same rows the ENTAILMENT seats are voting on.

Cross-check that the entry under test is the landed one:

```
$ python3 .ufo/waves/round-52/count-c2.py 8524904adb25e44f24d9f25aac7eae909625c18c --repo $LANE
C2=unmet claims=28 located=28 quote_missing=0 bad_rows=0 sources=5 source_rows=ok pins=ok provenance=ok entailed=0 dissent=0 rev=8524904adb25e44f24d9f25aac7eae909625c18c failed=entailment
exit=1
```

which reproduces `evidence/c2-at-data.txt` byte-for-byte and agrees with my independent 28/28.

## 4. Controls run

1. **Nonexistent ref on the same path** — `curl -sSL .../v7.2-does-not-exist/Documentation/mm/overcommit-accounting.rst`
   → `http=404 bytes=14`, body `404: Not Found`. So the five 200s are not a default-branch fallback: raw serves at the
   ref named in the path, and a wrong ref 404s at the same path.
2. **Committed vs work tree vs data commit** — `SAME` for the entry and all five copies (§1), so neither a dirty work
   tree nor a later commit explains the byte match.
3. **Independent quote extraction vs the frozen counter** — 28/28 hashes identical (`evidence/c2-hashes-at-data.txt`),
   and the counter's own `located=28` at R agrees with my containment result.
4. **Blob identity at the peeled tag commit** — §2, five MATCH.

## 5. Method note on my own instrument (disclosed, not a data defect)

My first pass tested containment using the counter's HTML normaliser (`normalise`, which strips `<…>` as a tag) instead
of `normalise_text`. That produced six false "missing" rows — 15, 18, 20, 22, 25, 26, the rows whose quoted C text
contains `<`, `>` or comment markers — while the committed copy failed the same way, which is why it was visibly an
instrument artefact and not a source change. Re-running with the counter's actual `normalise_text` plus its escaped-pipe
unescape gave 0 missing and offsets that agree with the counter's `located=28`. The offsets in the table are from the
corrected pass; a first pass's offsets for `vm.rst` (e.g. 26101 vs 29638) were shifted by the tag stripper and are not
reported.

## 6. Limits of this evidence

- "Live" here means the bytes `raw.githubusercontent.com` served for an immutable tag on 2026-10-27, through a CDN edge
  (`x-cache: HIT`, `cache-control: max-age=300`, `date: Tue, 27 Oct 2026 00:19:57 GMT`). The blob-id comparison in §2 is
  what makes those bytes the tag's bytes rather than whatever an edge happened to cache; without it a CDN hit alone
  would not prove provenance.
- A located quote proves the quoted words occur (whitespace collapsed); it does not prove the row's claim is right. I did
  not judge claim wording — that is the ENTAILMENT seats' work and is outside this seat.
- Offsets are into the collapsed text and cannot be pasted back into the source as byte positions; the source is
  line-wrapped code and prose.
- `git ls-remote` for tag resolution is unverified on this host (§2); the API + blob-id route is a substitute, not the
  command the seat named.
- I did not re-fetch `corpus/SOURCES.md` rows S497–S501 or their `used-by` cells; the seat's C2 arm covers them and the
  counter read them `source_rows=ok` at R.

## Findings

- **HIGH (verified, no defect) — the five frozen copies are still the bytes the tag serves.** All five URLs answer
  `HTTP 200`, `curl rc=0`, and sha256 equal to the frozen digest in `count-c2.py` `COPIES` and
  `evidence/freeze-sha256.txt`, with committed byte counts identical (2647 / 42424 / 43913 / 4265 / 51223); the committed
  copies also equal their git blob ids at tag commit `8d3ae592`, so `corpus/evidence/sources-r52/*.v7.2` is exactly the
  v7.2 content. No re-fetch or correction is needed for C2's `pins` arm.
- **HIGH (verified) — all 28 entry quotes occur in the live bytes.** `MISSING_IN_LIVE 0` and `MISSING_IN_COMMITTED 0`
  over `corpus/knowledge/overcommit-commit-limit-r52.md`, with per-row offsets in §3; all 28 claim hashes match
  `evidence/c2-hashes-at-data.txt`, so the votes the ENTAILMENT seats cast hash to these exact texts.
- **HIGH (verified) — tag `v7.2` resolves.** Annotated tag object `237a1c39e8dfd3e1c6f1f023eea37a48ec04cc63`, tagged
  2026-08-16T21:32:26Z, message `Linux 7.2`, peeling to commit `8d3ae59288f1e7d58d76558a6ee96d533bc5019f`; the five paths
  exist at that commit with the same blob ids as the copies.
- **MED (environment, not data) — `git ls-remote https://github.com/torvalds/linux refs/tags/v7.2` did not complete on
  this host**: `rc=124` after 100 s, and `rc=124` after 60 s with `protocol.version=2`, both with empty stdout/stderr and
  no credential prompt. Egress works (`raw.githubusercontent.com`, `api.github.com` answered in ~1 s in the same run), so
  this reads as a slow or stalled refs advertisement on the git transport for a repository with a very large ref set,
  not a lane or credential problem. Worth a line in the round-52 report as a re-verification route that cannot be relied
  on from this host; the API + blob-id route worked and is cheap.
- **LOW (my instrument) — the counter's two normalisers are not interchangeable and a seat can silently pick the wrong
  one.** `count-c2.py` exposes `normalise()` (HTML: strips `<…>`) and `normalise_text()` (whitespace only); using the
  former on C source gives six false quote misses (rows 15, 18, 20, 22, 25, 26). Nothing in the frozen counter is wrong —
  `evaluate()` calls `normalise_text` for every kind except `html` — but an outside re-checker importing the module will
  hit this and may mis-report a source change. Suggest the round-53 successor note the intended entry point
  (`normalise_text` for `kind="text"`) or expose one wrapper. Not a fix for this round: the counter is frozen.
- **LOW (evidence freshness) — raw serves through a CDN edge** (`via: 1.1 varnish`, `x-cache: HIT`,
  `cache-control: max-age=300`). A re-fetch today proves the edge's bytes equal the frozen digest; the blob-id check is
  the part that ties them to the tag tree. Any future "live re-fetch" receipt should carry the blob-id comparison too,
  or it proves only URL stability.

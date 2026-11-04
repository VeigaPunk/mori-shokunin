# Mo79S02SourcesRow — S594 SOURCES.md registry row + corpus/README.md index row (append candidates for the L1)

Status: **draft candidates only**. This seat did NOT edit `corpus/SOURCES.md` or
`corpus/README.md`. The L1 appends the lines below verbatim (each is one physical line).
Row spec source: contract §C3 (`.ufo/waves/round-79/contract.md`) + seat dispatch.

## 1. SOURCES.md registry row — S594

**Insertion point:** immediately after the S593 row at `corpus/SOURCES.md:374` (the
registry's current last row; line 375 is blank, line 376 is `## Paths`). One physical
line, no leading/trailing whitespace.

```markdown
| S594 | HTTP Caching (RFC 9111) §4.1 — https://www.rfc-editor.org/rfc/rfc9111.txt | spec | A | the Vary-selected representation and the cache-key rule: which stored response a cache may reuse when the stored response nominates request header fields via Vary, the definition of when two requests' nominated fields match, and the absent-field and wildcard boundaries | §4.1 "Calculating Cache Keys with the Vary Header Field" :526; MUST NOT selection clause :530-533 ("the cache MUST NOT use that stored response without revalidation unless all the presented request header fields nominated by that Vary field value match those fields in the original request", 30 words — the located contiguous span starts at "the cache" on :530 and ends at "original request" mid-line :533, recorded as such); the match definition and its three named transforms :536-550; the absent-field rule :552-554; a Vary value containing "*" always fails to match :556-557; sha256 aeb52adb3279d5f23dae34f68af11bd5cef0a0aff7ffcd014c9ca93c5302cf3e; pin corpus/evidence/sources-r79/rfc9111.txt (verbatim rfc-editor.org bytes, 84477 bytes, 1956 lines) | A cache must not serve a stored response carrying Vary without revalidation unless every request header field the response nominates matches in both the original and the presented request, so a byte difference between two fetches of one URL under different User-Agent values is representation selection under the cache-key rule, not content drift by itself. | mined | 2026-11-04 | 365d | corpus/knowledge/ua-serving-normative-r79.md |
```

**Anchor-cell provenance (nothing invented):**

- sha256 `aeb52adb3279d5f23dae34f68af11bd5cef0a0aff7ffcd014c9ca93c5302cf3e` is the pinned
  blob's hash, verified by this seat directly on the pin:
  `sha256sum corpus/evidence/sources-r79/rfc9111.txt` → `aeb52adb…302cf3e` (84477 bytes,
  1956 lines). Independently cross-checked: this seat's scratch fetch of
  `https://www.rfc-editor.org/rfc/rfc9111.txt` (2026-11-04) and Mo79E03SourcePin's
  pin fetch hash identically (two independent fetches, one hash). The round-79 evidence
  receipt `.ufo/waves/round-79/evidence/source-rfc9111-r79.txt` did not exist when this
  draft was first written (checked 2026-11-04); the sha was taken from the pin bytes, per
  the seat rule's fallback.
- Every located line verified against the PINNED copy (QUALITY 162):

```text
$ grep -n '^4\.1\.  Calculating' corpus/evidence/sources-r79/rfc9111.txt
526:4.1.  Calculating Cache Keys with the Vary Header Field
$ grep -n 'The header fields from two requests' corpus/evidence/sources-r79/rfc9111.txt
536:   The header fields from two requests are defined to match if and only
$ grep -n 'case-insensitive)' corpus/evidence/sources-r79/rfc9111.txt
550:      case-insensitive)
$ grep -n 'absent from a request' corpus/evidence/sources-r79/rfc9111.txt
553:   absent from a request, it can only match another request if it is
$ grep -n 'also absent there' corpus/evidence/sources-r79/rfc9111.txt
554:   also absent there.
$ grep -n 'always fails to match' corpus/evidence/sources-r79/rfc9111.txt
557:   "*" always fails to match.
```

  So: heading :526; MUST NOT paragraph :528-534 with the quoted clause spanning :530-533;
  match definition :536-538; the three named transforms at :540, :543, :546-550 (block
  :536-550); absent-field rule :552-554; `*` refusal :556-557.

- The quoted clause's 30-word count, verified mechanically (span trimmed at its recorded
  mid-line boundaries — the parenthetical on :530 before "the cache" and the ` (i.e., …`
  continuation on :533 after "original request"):

```text
$ P=corpus/evidence/sources-r79/rfc9111.txt
$ Q=$(sed -n '530,533p' "$P" | sed 's/^   //; s/^(Section 12\.5\.5 of \[HTTP\]), //' | tr '\n' ' ' | sed 's/ (i\.e\.,.*$//' | sed 's/  */ /g; s/ $//')
$ printf '%s\n' "$Q"
the cache MUST NOT use that stored response without revalidation unless all the presented request header fields nominated by that Vary field value match those fields in the original request
$ printf '%s' "$Q" | wc -w
30
```

## 2. corpus/README.md knowledge-index row

**Insertion point:** append the whole section below after `corpus/README.md:859` (the
Round-77 knowledge-addition table's last row, `| The vendor counter-name association
(r78, S593) | … |`, the file's current last line). Convention ground: Round-76 and
Round-77 sections are titled "(new growth, indexed the round it lands)" — each round
gets its own section; a bare row inside the Round-77 table would misattribute the r79
entry to round 77.

```markdown
## Round-79 knowledge addition — the Vary-selected representation (new growth, indexed the round it lands)

| Ground | Entry | Bounded advance |
|---|---|---|
| The normative ground of the lane's empirical `ua-serving` drift class (r79, S594) | `knowledge/ua-serving-normative-r79.md` (S594) | RFC 9111 §4.1 states the selection rule a cache MUST apply (:530-533), with the field-match definition and its three named transforms (:536-550), the absent-field rule (:552-554) and the wildcard refusal (:556-557) — a byte difference between two fetches of one URL under different User-Agent values is representation selection under the cache-key rule, not content drift by itself; the empirical `ua-serving` class gains its normative layer beside QUALITY 159's vendor-scoped grammar; no instrument change, no class re-graded, no TTL decided. |
```

**The index row line alone** (if the L1 appends only the row into an equivalent r79 table):

```markdown
| The normative ground of the lane's empirical `ua-serving` drift class (r79, S594) | `knowledge/ua-serving-normative-r79.md` (S594) | RFC 9111 §4.1 states the selection rule a cache MUST apply (:530-533), with the field-match definition and its three named transforms (:536-550), the absent-field rule (:552-554) and the wildcard refusal (:556-557) — a byte difference between two fetches of one URL under different User-Agent values is representation selection under the cache-key rule, not content drift by itself; the empirical `ua-serving` class gains its normative layer beside QUALITY 159's vendor-scoped grammar; no instrument change, no class re-graded, no TTL decided. |
```

## 3. Self-check — the S594 row splits into exactly 11 cells

Command (run over THIS file's own delivered bytes, so the checked bytes are the delivered
bytes) and output:

```text
$ D=.ufo/waves/round-79/w1/Mo79S02SourcesRow-append.md
$ awk -F'|' '/^\| S594 \|/ { print "pipes=" NF-1 " cells=" NF-2;
    for (i=2; i<NF; i++) if ($i !~ /^ / || $i !~ / $/) print "BADPAD cell " i;
    n=split("id source kind tier scope anchor teaches status opened recheck used-by", want, " ");
    for (i=1; i<=n; i++) printf "cell %2d (%s): %.48s\n", i, want[i], $ (i+1); ok=1 }
  END { if (!ok) print "ROW NOT FOUND" }' "$D"
```

Run output (2026-11-04, over this file's delivered bytes):

```text
pipes=12 cells=11
cell  1 (id):  S594 
cell  2 (source):  HTTP Caching (RFC 9111) §4.1 — https://www.rfc-
cell  3 (kind):  spec 
cell  4 (tier):  A 
cell  5 (scope):  the Vary-selected representation and the cache-
cell  6 (anchor):  §4.1 "Calculating Cache Keys with the Vary Head
cell  7 (teaches):  A cache must not serve a stored response carryi
cell  8 (status):  mined 
cell  9 (opened):  2026-11-04 
cell 10 (recheck):  365d 
cell 11 (used-by):  corpus/knowledge/ua-serving-normative-r79.md 
```

(no BADPAD line; `%.48s` truncation above is display-only. `cells=11` = the census
column count; every cell space-padded, i.e. every split boundary is ` | `.)

```text
$ ROW=$(grep '^| S594 |' "$D"); printf '%s' "$ROW" | grep -oF '\' | wc -l
0
```

Escape check (no literal or escaped pipe inside any cell — a `\|` anywhere in the row
would both break the census split and violate the seat's hard rule):

```text
$ grep -cF '\' <<<"$ROW"   # backslashes in the row
0
```

README row cells (3-column table, `| Ground | Entry | Bounded advance |`):

```text
$ awk -F'|' '/^\| The normative ground of the lane/ { print "README row cells=" NF-2 }' "$D"
README row cells=3
README row cells=3
```

(two matches = §2's section-table copy and the row-alone copy; the two lines are
byte-identical by construction — same source string, both fenced.)

Schema notes per the census contract: `status=mined`, `opened=2026-11-04` (ISO date),
`recheck=365d` (valid `NNd` form), `used-by` names exactly
`corpus/knowledge/ua-serving-normative-r79.md` (the entry that cites S594), `source` cell
names `https://www.rfc-editor.org/rfc/rfc9111.txt`, anchor cell names both
`corpus/evidence/sources-r79/rfc9111.txt` and the blob's sha256. The `§`, `"`, `*`, `—`
and `:` characters used are pipe-free by construction (the r76 title-pipe mistake class is
respected: no cell contains `|` or `\|`).

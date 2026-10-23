# W1 ReviewLessonGateFormat — can the frozen C1 counter read the Gate rows seats will draft?

Seat: ReviewLessonGateFormat (leaf, mori round 31 wave 1). Scope: parser-readability of
contract-format Gate rows against `.ufo/waves/round-31/count-c1.py` (frozen at
2124cbc), tested in a sandbox clone; no counter change; no lane write beyond this file.

## Method

- Counter read in full: `.ufo/waves/round-31/count-c1.py:33-180` — `cells` :33-39,
  `norm` :42-43, `unescape` :46-47, quote regex and gate checks :135-161.
- Real-row baseline: all 27 Gate rows at `8baccf4a:corpus/lessons/round-30.md`
  (:104-155) replayed through the counter's own `cells`/`unescape`/regex (harness
  `harness_r30.py` in scratch), admit quotes norm-checked against the round-30
  excerpts and, separately, against raw fetched bytes.
- Edge cases: sandbox clone `git clone --no-hardlinks` of the lane, detached at
  `8baccf4a`, fixtures committed at `ee3b2b2` (S161-S172) and `f7689ed` (S173-S175),
  counter run as `count-c1.py <rev> --repo <sandbox>` (never against the lane).
  Scratch: `/fast/scratch/hyaku/mori-r31/ReviewLessonGateFormat/` (gen_fixtures.py,
  gen_fixtures2.py, harness_r30.py, verify_upstream.py, retry_census.py, lane/).
- Tooling: no installs (host python3 3.14, git, curl already present). All fetches
  are public raw URLs via curl; fixture URLs use `fixture.invalid` (NXDOMAIN), so
  `fetch=bad` in every fixture run is by construction and isolates parsing/copy.

## What the counter does with a Gate row (evidence base)

- `cells` (:33-39): drops the leading `|`; drops the trailing `|` only when the line
  does not end in `\|` (:37); splits on `(?<!\\)\|` (:39) — every pipe directly
  preceded by a backslash is literal, whether or not that backslash is itself escaped.
- `unescape` (:46-47): `re.sub(r'\\(["|\\])', r'\1', q)` — only `\"`, `\|`, `\\`
  collapse to `"`, `|`, `\`. Every other backslash sequence passes through unchanged.
- Quote extraction (:147): `\(\s*\d+\s+words?\s*\):\s*"((?:[^"\\]|\\.)*)"` over the
  raw row line; the row must yield ≥1 quote and every quote ≤25 words after
  unescape (`:148`, counted by `.split()` on the unescaped text).
- Row checks: gate lines must start `| S### |` (:135); admit = last cell startswith
  `admit` (:136); URL = first cell starting `https://` (:145); sha = backticked
  64-hex (:146); copy `corpus/evidence/sources-r31/S###.src` must hash equal to the
  gate sha and contain every `norm(quote)` under `norm` whitespace-collapse
  (:154-159); fetch must hash equal (:158-159). Entry decision-table rows need
  `len(row) == len(hdr)` (:121).

## Probe results (sandbox commits ee3b2b2 + f7689ed; counter output verbatim class)

| sid | quote shape as written | gate | copy | verdict |
|---|---|---|---|---|
| S161 | `alpha\|beta gamma` (escaped pipe) | ok | ok | reads correctly |
| S162 | `say \"hi\" now` (escaped dquote) | ok | ok | reads correctly |
| S163 | `opt\-x sets \fBbold\fR mode` — roff backslashes verbatim | ok | ok | reads correctly (unescape leaves `\-`,`\fB`,`\fR` intact; raw bytes match) |
| S164 | same bytes, backslashes doubled (`opt\\-x …`) | ok | ok | reads correctly (second valid form) |
| S165 | literal `\\` in bytes written `C:\\\\bin` | ok | ok | reads correctly |
| S166 | literal `\\` in bytes written verbatim `C:\\bin` | ok | bad | unescape halves it to one backslash — copy match fails |
| S167 | two `(N words): "…"` segments in one row | ok (quotes=2) | ok | reads correctly |
| S168 | quote spanning a source newline, written on one line | ok | ok | reads correctly (`norm` collapse, :43, :156) |
| S169 | URL `…/plain/man5/proc_pid_comm.5?h=man-pages-6.20` | ok | ok | URL survives cell parse intact (no pipe); echoed in full |
| S170 | roff comment `\"` in bytes written verbatim | ok | bad | unescape turns it into `"` — copy match fails |
| S171 | bare `"` inside quote (forgotten escape) | ok (quotes=1) | ok | **false pass**: extracted fragment `say ` still substring-matches; the `(3 words)` annotation is never cross-checked |
| S172 | quote ending in a lone `\` | **bad (gate_fields)** | — | the intended close `"` binds to the backslash as `\"`; regex never terminates; row unusable |
| S173 | bytes contain `\|` (roff thin space), written `thin\\\|space` | ok | ok | reads correctly |
| S174 | same bytes written verbatim `thin\|space` | ok | bad | unescape turns the written `\|` into `|`, which is not in the bytes — copy match fails |
| S175 | pgrep.c `"'\\''"` written `\"'\\\\''\"` | ok | ok | reads correctly |
| entry | unescaped `\|` inside a decision-table reading cell | — | — | cell splits; `rows_ok=12/13` → `rows` fail via :121 |

Fixtures that fail do so only in `copy`/`gate_fields`; `fetch=bad` everywhere is the
fixture-URL construction, and `C1=unmet` overall additionally from `skill_rows` (met
here at 4) — the per-sid lines above are the signal.

## Round-30 real rows through the same parser (8baccf4a)

All 27 rows parse: cell counts 6/6 (8 for the two-URL row), decision cell detected,
quotes extracted with escapes intact, none over 25 words. Escaped-quote rows —
S156 admit (`\"Timestamp\") \|`), S158 admit (`LOG_MESSAGE(\"Suppressed …`) and three
S158 rejects — all extract cleanly. The round-30 style is exactly the style this
counter reads.

The four norm-check misses (S157, S158, S159, S160 admit quotes) against
`corpus/evidence/sources-r30/S###.txt` are a copy-format fact, not a parse fact:
those excerpts are metadata-headed, line-number-prefixed transcripts
(`2773\t…`, S157.txt), so multi-line joined quotes and S159's spliced diff-hunk
summary cannot substring-match them. Re-fetched raw bytes match the same quotes:
S156 3/3 and S158 1/1, with sha256 equal to the row shas (fresh fetch today:
`b56aa781be9c29b6…`, `428dc8308d5caf70…`). Round-31 `.src` copies are sha-bound to
the fetch (:155), i.e. raw bytes by construction, so this failure mode cannot recur
if seats commit the fetch and do not hand-edit copies.

## Upstream census of pre-assigned r31 sources (escape-relevant shapes)

| source (tag) | bytes | sha256 (16) | `"` | `\|` bytes | `\"` bytes | literal `\\` |
|---|---|---|---|---|---|---|
| procps `man/pgrep.1` @ v4.0.7 | 9 702 | `c2024c384dd88df2` | 28 | **30** | **12** | 0 |
| procps `src/pgrep.c` @ v4.0.7 | 45 309 | `af711983209fa083` | 306 | 0 | 2 | **1** (`memcpy(result + pos, "'\\''", 4);`) |
| Linux `fs/proc/base.c` @ v7.2 | 98 196 | `cef1a2cf3f34f683` | 464 | 0 | 0 | 0 |
| man-pages `man5/proc_pid_comm.5` @ 6.20 | 1 347 | `31aee9e50c23579e` | 11 | 0 | **7** | 0 |

pgrep.1 also carries 357 single-backslash roff escapes (`\-`, `\fB`, `\&`×3), all of
which are safe verbatim under the rule below.

**URL template defect (needs L1 correction before drafting):**
`https://git.kernel.org/pub/scm/docs/man-pages/man-pages.git/plain/<path>?h=man-pages-6.20`
returns 404 for the man5 pages (curl 404 verified for `plain/man5/proc_pid_comm.5`,
`plain/man5/proc_pid_stat.5`, `plain/man5/proc_pid_cmdline.5`): at that tag the
top-level `man5` is a symlink stub and gitweb plain does not follow it; the real
pages live at `man/man5/`. The tag itself exists (`/refs/tags` lists
`man-pages-6.20`), and the corrected form fetches 200:
`…/plain/man/man5/proc_pid_comm.5?h=man-pages-6.20` (1 347 B, sha `31aee9e5…`).
Seats S169/S170/S171 following the template as-is would write Gate rows whose fetch
(:158-159) fails forever.

## The escaping rule a seat must follow (ready to paste)

```text
Inside a Gate-row quote, write:
  every literal "  as \"        (a bare " ends the quote early — silent corruption, S171)
  every literal |  as \|        (a bare | splits the table cell, :39, :121)
  every literal \  as \\        (doubling is the portable form; unescape halves it back, :47)
So roff bytes that are themselves \| or \" (30x and 12x in pgrep.1; 7x in
proc_pid_comm.5) must be written \\\| and \\\" — never copied verbatim (S174, S170).
A literal \\ in C bytes (pgrep.c memcpy line) is written \\\\ (S165/S175 both pass).
Shortcut, proven safe: a roff backslash whose NEXT char is not " | or \ (\-, \fB,
\&, \ ) may be written verbatim; unescape leaves it untouched and the bytes match
(S163). Doubled also works (S164). When in doubt, double.
Never end a quote with a lone \ — the closing " binds to it and the regex never
terminates; the row dies with gate_fields (S172).
Write the annotation exactly as (N words): " with no space before the colon; N is
not verified by the counter but must be the true unescaped word count; >25 fails.
Quote shape: contiguous source text on one Gate line, whitespace-insensitive
(newlines in the source collapse; S168). Copies must be the untouched fetched bytes.
```

## Findings by severity

1. **Defect (template, blocks S169-S171 fetch):** the man-pages plain URL template
   404s at tag man-pages-6.20 for the man5 pages; working path is `plain/man/man5/…`
   (evidence above). If uncorrected, three of the six required new-id gate rows
   cannot reach `fetch=ok`.
2. **False-pass hole (counter, frozen — report only):** a bare unescaped `"` inside
   a quote truncates it to a fragment that can still substring-match the copy
   (S171 `gate=ok quotes=1 copy=ok` against a 3-word declared quote). The declared
   word count is never cross-checked (:147-148). Seats self-discipline: escape every
   `"`; L1 review should eyeball that each quote's annotation matches its content.
3. **Masked-mangle hole (counter, frozen — report only):** verbatim roff `\"`/`\|`
   survives sometimes because the copy check is substring-based (unescaped
   `"Suppressed` is a substring of bytes containing `\"Suppressed`), so a wrong
   escape can still pass `copy=ok`. S170/S174 show the failing direction; the
   substring accident is [INFERENCE] from the :156 rule plus :47 — not separately
   fixture-tested.
4. **Non-defect confirmations:** `\|`, `\"`, roff `\-`/`\fB`/`\&`, multi-quote rows,
   newline-collapsed quotes, `?h=` URLs, doubled and verbatim single roff
   backslashes all read correctly; `\\` byte sequences need quadruple writing.

## Residual risk / verification gaps

- The fetch path was exercised only via the two real systemd fetches (section
  "Round-30 real rows"); fixture fetches are NXDOMAIN by design, so
  `fetch_ok=0/15` is construction, not counter behavior.
- Man-pages census beyond `proc_pid_comm.5` (stat/cmdline fetched 200, shapes not
  counted) and any `\[em]`-style bracket escapes were not counted — pgrep.1 shows
  `\[` count 0, other files unverified.
- Round-30 rows S157/S159/S160 raw-byte quote re-verification was done against the
  excerpts only (they predate the r31 copy rule); only S156/S158 were re-fetched.
- Sandbox commits (`ee3b2b2`, `f7689ed`) live only in the scratch clone; the lane
  was never written except this report file.

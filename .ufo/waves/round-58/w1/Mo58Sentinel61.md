# Mo58Sentinel61 — C2 quote-binding, adversarial (round 58, w1)

Seat: sentinel (attack share). Scope: falsify the frozen C2 predicate only.
Target: `.ufo/waves/round-58/count-c2.py`, frozen bytes at
`fe8801120a67c1a6b8899d7d0423839caa09e7d0`,
sha256 `aab888ad787964f7a153d64d85dafa58f652f977e21e22eaa492706a691010d3`
(verified: `git show fe88…:count-c2.py | sha256sum` == working-tree file; bytes immutable for this report).

Measured source: `tools/mori-driver-liveness.py` at `fe88…`,
sha256 `6b3dba74c639190e7e96b6bed8e6ac8f285a51ce6d910fbe92e6dd39bf7be997`, 18347 bytes, 479 lines.

**Verdict: counterexample found. Two contract do-nothing controls score met, which by
the contract's own kill rule ("Any control scoring met invalidates the counter")
invalidates the C2 claim as frozen.** Detection only; no production/counter/VCS edits.

Method bound: I imported the frozen counter bytes into a Python process, overrode only the
module-global `LANE` (the same seam `--selftest` uses), and ran `measure(rev)` against
throwaway git fixtures created with `git init <abs scratch path>` + `git -C <that path>`.
Fixture copy and tool bytes were the **real** freeze bytes, so `copy=ok` is earned, not
faked; only the entry (and in one arm the copy encoding) is adversarial. Scratch:
`/fast/scratch/hyaku/mori-r58/Mo58Sentinel61/` (TMPDIR there; removed after the run).
Nothing was written outside my report path.

---

## H1 — Control (b) falsified: byte-different pinned copy scores `copy=ok` (S1)

Contract §C2: *"a pinned source copy whose sha256 differs from the tool at R MUST score
`copy=bad`"*; claim text: *"whose sha256 equals the sha256 of `tools/mori-driver-liveness.py`"*.

Exploit: line endings. `_show()` runs `git show` with `text=True` (universal-newline
translation) and `_sha256()` hashes the **re-encoded decoded text**, not the blob.

```
pinned copy = tool bytes with LF → CRLF  (18826 bytes)
raw sha256 copy  = 011cadfccf84dfe4c318275ac49799383fa3dd06a9151223ec75ffd64243ac6f
raw sha256 tool  = 6b3dba74c639190e7e96b6bed8e6ac8f285a51ce6d910fbe92e6dd39bf7be997
counter output   = C2=met claims=8 located=8 copy=ok tree=ok rows=ok sources=ok failed=none
exit             = 0
```

Evidence: fixture rev `650ab7efee2a0c113db757199d9902879c2d9b50` (JSON in run log below);
blob shas read with `git -C <fixture> cat-file blob <rev>:<path> | sha256sum`.
Any LF↔CRLF (or lone-CR) drift — i.e. the exact drift a copy/paste "pinned copy" produces —
is invisible. The narrowed predicate is *decoded-text equality*, not byte identity.

Smallest remediation: hash the bytes. Use `_git("cat-file","blob",f"{rev}:{path}")` without
`text=True` (or `git show` with `encoding=None`) and `hashlib.sha256` the raw stdout; keep a
separate decoded read for the quote arm. Boundary test: copy differs from tool by exactly one
`\r` → must print `copy=bad`.

## H2 — Control (c) falsified: no frontmatter at all, `sources=ok` (S1)

Contract §C2 control (c): *"frontmatter missing `source:`/`verified-at:`/`recheck:`/
`coverage-map:` MUST score `sources=bad`"*.

The arm is a file-wide substring scan (`if needle not in entry`), never a frontmatter read.

```
entry: no frontmatter block; body ends with the prose line
  "prose: source: S550 verified-at: 2026-10-27 recheck: 90d coverage-map: x"
output: C2=met claims=8 located=8 source=ok … sources=ok failed=none   (exit 0)
```

Evidence: fixture rev `1491059449ee4f84e51f59cb35767a94904060ab`.

Same arm is also a **prefix match**: `source: S550` is satisfied by `source: S5500`
(fixture rev `206119940881a364454474c7fd41fc1d3c23d669`, `C2=met`). Row identity is not
bound, only a prefix of a string somewhere in the file.

Smallest remediation: parse the leading frontmatter block (lines before the first blank line
after `---`/title), require the four keys as whole tokens (`re.match(r"source:\s*S550\s*$")`),
and reject when they appear only below the first claim bullet.

## H3 — Quote predicate is a 12-char substring test, not a fabrication test (S1)

`any(len(s) >= 12 and s in copy_lines[lineno-1] for s in spans)` accepts **any** backticked
span on the line, not the span that carries the claim. An entry therefore satisfies `located`
by backticking 12 arbitrary characters lifted from the cited line while its stated quote is
entirely fabricated:

```
- **K1** `launch` must be recorded (`ENTIRELY FABRICATED 1`) (`other_lines = 0`) (tools/mori-driver-liveness.py:80)
→ C2=met claims=8 located=8 … failed=none  (exit 0, rev 35ec171035c8429a05ee0ee3cdb5065f6a7e198e)
```

Sharper: the predicate is satisfiable by construction on most of the file. 327/479 lines
(68.3%) and 70/98 lines of the parse region (77–174) carry ≥12 characters of content, so for
almost every citable line the attacker can mint a passing token.

Truncated-but-byte-faithful misattribution (round-57 defect 3 is not closed, it is relocated):

```
line 394: return (rc == 0 and rep["log"]["malformed"] == 0 and rep["log"]["other_lines"] == 2
line 410: return (rc == 0 and rep["log"]["malformed"] == 5
shared 47-char prefix: 'return (rc == 0 and rep["log"]["malformed"] == '

- **K1** exit status is ok only when malformed==0 (`return (rc == 0 and rep["log"]["malformed"] == `) (tools/mori-driver-liveness.py:410)   ×8
→ C2=met claims=8 located=8 … failed=none  (exit 0, rev e9321f42f03507c52ed72087fbde36da90267ff4)
```

The quote stops exactly before the discriminating constant, so a claim about `malformed == 0`
is bound to a line that tests `== 5`. 822 distinct-line pairs in the tool share a ≥12-char
substring; e.g. lines 213/218 share `report["log"] = {"path": log_path, "state": "` and differ
only in `"unreadable"` vs `"empty"`.

Smallest remediation: bind the claim to *one designated* quote — require the span be delimited
(e.g. first backticked group) and require it to be a **maximal** substring of the cited line
(quote cannot end mid-token), plus reject a span that is a strict prefix shared with another
line (`len(s) < len(copy_line)` and `s` occurring elsewhere). Minimum viable: require
`len(s) >= 24` and `s == copy_line.strip()` or `s` followed by a non-word character in
`copy_line`.

## M1 — Claims are lines, not claims: one fact counted eight times (S2)

`KLINE` captures `K<n>` and never checks uniqueness, contiguity, or distinctness of
`(line, quote)`. All of these score `claims=8 located=8` → `C2=met`:

| fixture | entry shape | rc | rev |
|---|---|---|---|
| T1 | eight lines all `**K1**`, eight different lines | 0 | `dd6f2276c2a6e68c976068ba500810ae64d9671b` |
| T3 | eight lines all `**K0**` | 0 | `1fbe65578072fb1dacf6bc01abc6cb4601cfac62` |
| T8 | `**K901**…**K908**` | 0 | `4cb49680720a7fb7c2da5408d5ba72886fde45ae` |
| T13 | eight lines, **one** cited line (80) repeated | 0 | `4099242543138802c34efb32e619bd832210edaa` |

So `claims=N` in the frozen target output is a line count, and one fact replicated eight times
reports N≥8. The contract's "≥8 located claims on the event-class semantics" is not enforced at
claim granularity.

Smallest remediation: require `len({k for k in knums}) == claims`, `len({(line,quote)}) ==
claims`, and K numbering contiguous from 1.

## M2 — Presentation is not checked; locators are not confined to the parser (S2)

* Claims wrapped in an HTML comment (`<!-- … -->`) still count — the document renders with zero
  claims yet `C2=met claims=8` (rev `c8bdf132bdef0bc5fc9cb63694f45e76ee2e0904`).
* All eight locators inside the module docstring prose (lines 2, 4–10 of the tool, i.e. the
  `"""Hyaku driver-liveness reader …` block) score `located=8` (rev
  `d165d70acd178f24d7ca12493221cda026891abb`), even though the claim surface is the event-class
  parser (row anchor says `parse_log` lines 77–174). No arm checks that cited lines fall in the
  claimed region or that quoted text is code rather than prose/comment.

Smallest remediation: strip fenced blocks and HTML comments before counting; require
`77 <= lineno <= 174` (or a declared span in frontmatter) for this entry.

## M3 — Degenerate span passes: twelve spaces (S3)

`` - **K1** x (`            `) (tools/mori-driver-liveness.py:89) `` (`located=8`, exit 0,
rev `58bcb1b432f53718f78b0b9855d5b0da38a65c6e`): a whitespace-only 12-char span matches any
sufficiently indented line. Smallest remediation: `s.strip() and len(s.strip()) >= 12` and
require at least one alphanumeric-run of ≥6.

## M4 — `rev=` is unvalidated; a movable ref scores met (S3)

`measure(sys.argv[1])` never asserts the argument is a 40-hex sha, and the output echoes it
verbatim. On a met-scoring fixture, `measure("main")` prints
`C2=met … rev=main` (exit 0; branch `main`, fixture HEAD
`2bf0e8da696e66660747132b2ca451a36967dcf4`). On the lane, `count-c2.py HEAD` prints
`C2=unmet entry=absent failed=entry rev=HEAD`. The "at the measured revision" binding is
therefore *whatever the ref resolves to at run time* — measurement is not pinned.
Smallest remediation: `re.fullmatch(r"[0-9a-f]{40}", rev)` else exit 2.

## L1 — Rows arm: used-by is a substring, not an identity (S3)

`ENTRY in cells[11]` accepts `corpus/knowledge/driver-events-r58.md.bak`
(rev `c0062c3c1a1c325582c9b4e65ff4596aaca7155b`, `rows=ok`, `C2=met`). Require a
comma-split exact match on stripped cells.

## L2 — `tree=ok` is not an independent predicate (S3)

Static, frozen file: `tree_arm` is only ever assigned in lockstep with `copy_arm`
(lines 69, 71, 74), and printed at line 109. No git tree object is ever read. `tree=ok` is a
duplicate label for `copy=ok` and carries no information; the frozen target output
`… copy=ok tree=ok …` therefore reports two arms from one predicate. Compounding: when
`tools/mori-driver-liveness.py` is absent at R the counter prints `copy=bad` (line 73–74),
never `tree=bad`, so the failure is mislabelled.

## L3 — Copy/tree arm is vacuous for this round (S3, informational)

`tools/mori-driver-liveness.py` blob id is `be8dd1ed0dfc7857e556535cbc9684b3b4c0786c` at
**both** `b783d0b8…` (entering) and `fe8801…` (freeze). The arm compares two paths at the same
revision, so with zero tool drift it can only fail on deliberate same-rev tampering — and H1
removes even that. A copy pinned from any *other* revision is undetectable when the text is
newline-equivalent.

## L4 — `_show` passes the rev unseparated (S3, low, not attacker-facing)

`_git("show", f"{rev}:{path}")` gives no `--` guard; a rev beginning with `-` is parsed as a
`git show` option. Not an untrusted boundary here (the seat supplies `R`), but it makes the
failure mode an `entry=absent` rather than a usage error.

---

## What held (bounded negatives)

These are the arms I could not defeat; state them so the remediation does not over-correct:

| Probe | Result | rc |
|---|---|---|
| C0 control: 8 fully fabricated quotes, no incidental token | `located=0 failed=quotes` | 1 |
| Sprinkled jargon with no real substring | `located=0…5`, `failed=quotes` | 1 |
| Spans < 12 chars (e.g. `return None`, 11) | not counted → `failed=quotes` (false-**negative** for legitimate short quotes) | 1 |
| `claims < 8` (6 docstring lines only) | `failed=claims` | 1 |
| Entry absent at `b783d0b8…`, `fe8801…`, `4272736c…` | `C2=unmet entry=absent failed=entry` | 1 |
| Duplicate `S550` rows / `used-by = —` | `rows=bad` | 1 |
| Counter's own suite, frozen bytes | `C2_SELFTEST pass=6 fail=0` | 0 |

The counter does correctly read the entry, copy and registry from the measured revision via
`git show` (no working-tree leakage), and its control-(a) arm (quotes that are not substrings)
fails closed. The defect is that (a) is satisfiable with a decoy span, so "quote present" never
becomes "claim grounded".

## Impact on the round

* C2's frozen do-nothing controls (b) and (c) both score `met` on fixtures; per the contract
  this invalidates the counter, so any `C2=met` produced by it — including `claims=N` — is not
  trustworthy as a depth measurement.
* The specific round-57 routed defects the counter claims to fix are only partially closed:
  defect 2 (false-green quote constructions) survives as H3/T2/T14; defect 3 (byte-faithful
  quotes) survives as truncated-prefix attribution and as H1's decoding-layer comparison.
* No score change is proposed by this seat; the finding is that the C2 claim cannot be
  certified on these bytes.

## Reproduction recipe (no production writes)

1. `git -C <lane> show fe88…:.ufo/waves/round-58/count-c2.py > <scratch>/c2.py` (assert sha256
   `aab888ad…`), `git -C <lane> show fe88…:tools/mori-driver-liveness.py > <scratch>/tool.py`
   (assert sha256 `6b3dba74…`).
2. `importlib`-load `c2.py`; build fixtures with `git init <scratch>/fx-*` +
   `git -C <fixture> add/commit`; write `tools/…`, `corpus/evidence/sources-r58/…`,
   `corpus/knowledge/driver-events-r58.md`, `corpus/SOURCES.md` (header + `c2.ROW_OK`).
3. Set `c2.LANE = <fixture>`, call `c2.measure(<fixture rev>)` under
   `contextlib.redirect_stdout`.
4. Arms: CRLF copy (H1); no-frontmatter body (H2); fabricated quote + decoy 12-char span (H3);
   `K1`×8 / `K0`×8 / one line ×8 (M1); HTML comment and docstring locators (M2); 12-space span
   (M3); `measure("main")` (M4); `.bak` used-by (L1).

## Receipts

Frozen counter sha256 `aab888ad787964f7a153d64d85dafa58f652f977e21e22eaa492706a691010d3`;
tool sha256 `6b3dba74c639190e7e96b6bed8e6ac8f285a51ce6d910fbe92e6dd39bf7be997`;
CRLF-copy raw sha256 `011cadfccf84dfe4c318275ac49799383fa3dd06a9151223ec75ffd64243ac6f`.
Fixture revs are listed per finding above (throwaway repos under
`/fast/scratch/hyaku/mori-r58/Mo58Sentinel61/tmp/`, deleted after the run; each finding is
reproducible from the recipe above). Scratch was cleaned before yielding. No commits, no VCS
mutation, no fleet/sibling-repo writes, no production edits.

Tools installed this seat: none.

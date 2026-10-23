# Round 37 knowledge-entry code-claims check — ExecKnowledgeCheck

**Item:** verify that the line ranges cited in `corpus/knowledge/source-drift-hardening-r37.md`
(`:54,163-166`, `:113-136`, `:156-159`, `:103-108`) contain what the entry says, reading
`tools/mori-source-drift.py` at the scored rev `e57c58b57c025364e79d130fbdf764d2674d83d6`.

**Scored-rev baseline:** `git show e57c58b:tools/mori-source-drift.py` = blob
`162ee87b5b0789c6815f967f3db93d277bab38d9`; worktree tool byte-identical to the scored rev
(`diff -q` clean). Entry file identical at scored rev and worktree (diff clean).

---

## Range-by-range verdict

### `:54,163-166` — bounded read — HOLDS

Entry claim: *"`FETCH_MAX_BYTES = 4 * 1024 * 1024`, read as `FETCH_MAX_BYTES + 1`
(`tools/mori-source-drift.py:54,163-166`). An untrusted source must not stream past the cap or
stall between bytes past the socket timeout; an over-cap body is not classifiable and grades
`unavailable`."*

| line | observed byte content |
|---|---|
| 54 | `FETCH_MAX_BYTES = 4 * 1024 * 1024  # bodies larger than this cannot be classified; read is capped at +1` |
| 163 | `body = resp.read(FETCH_MAX_BYTES + 1)` |
| 164 | `if len(body) > FETCH_MAX_BYTES:` |
| 165 | `return "unavailable", None` |
| 166 | `return "body", body` |

All claim elements present: constant definition (54), read as `+1` (163), over-cap → `unavailable`
(164-165), body return (166). Functional check: `--selftest` arm `huge_cap` PASSes on the scored
bytes; mutant `FETCH_MAX_BYTES = 4*1024*1024` → `1 << 40` fails exactly `huge_cap` (plus the
row-level checks it moves) — observed `exit=1`, `huge_cap=FAIL`.

### `:113-136` — `_public_redirect_target` — HOLDS

Entry claim: *"`_public_redirect_target` (`tools/mori-source-drift.py:113-136`)… a server-driven
redirect must land on a public `http`/`https` destination: loopback, link-local, private literals
and `localhost`/`.local` names are refused (`unavailable`)."*

- 113 `def _public_redirect_target(url):` (function spans 113-135; 136 is the trailing blank line, so `:113-136` fully contains it).
- Scheme gate at 120-121: `http`/`https` only.
- Literal IP gate at 126-127: `addr.is_global` — measured `is_global=False` for loopback (`127.0.0.1`, `::1`), link-local (`169.254.169.254`, `fe80::1`), private (`10.0.0.1`, `192.168.1.1`, `172.16.0.1`, `fd00::1`), `0.0.0.0`, and IPv4-mapped loopback (`::ffff:127.0.0.1`); `is_global=True` for `8.8.8.8`.
- Name gate at 130-132: `localhost`, `*.localhost`, `*.local` refused (incl. case-insensitive, trailing-dot tolerant).
- Direct probe of the full predicate: all refused classes return `False`; `http://example.com/` returns `True`; `ftp://` / hostless return `False`.

### `:156-159` — application site — HOLDS

Entry claim: *"applied at `:156-159`"* (the redirect check inside `fetch()`).

| line | observed byte content |
|---|---|
| 156 | `# a redirect actually happened: the new authority must be public` |
| 157 | `# (loopback/private targets are refused; w2/SentCensus)` |
| 158 | `if not _public_redirect_target(final):` |
| 159 | `return "unavailable", None` |

Anchor string `if not _public_redirect_target(final):` is exactly at 158 (matches the C2 counter's
`REDIRECT_ANCHOR`). Mutant `if False:` fails exactly `redirect_private_refused` (observed `exit=1`,
arm FAIL), confirming the site is the load-bearing application.

### `:103-108` — initial-request policy — HOLDS

Entry claim: *"The initial request keeps loopback fetchable because the registry is lane-curated and
append-only and the probe's own selftest serves on `127.0.0.1` (`:103-108`)."*

- 103-105: docstring of `_fetchable_initial` — *"Loopback and private literals stay fetchable — the
  registry is lane-curated and append-only, and the frozen counter's blind fixture legitimately
  serves on 127.0.0.1"*.
- 106-108: body — `parts.scheme in ("http","https") and bool(parts.hostname)`; no loopback/private
  exclusion (confirmed functionally: `_fetchable_initial("http://127.0.0.1:9000/x")` → `True`).
- The probe's own selftest does serve on `127.0.0.1` (line 291
  `ThreadingHTTPServer(("127.0.0.1", 0), handler)`, line 308 `base = "http://127.0.0.1:%d"`); the
  round-36 C1 counter likewise (round-36 `count-c1.py` line 354). Asymmetry deliberate and exercised:
  `redirect_private_refused` arm (302 → loopback) PASSes at the scored rev.

### Supporting claims corroborated

- `--selftest` prints `PASS (6 cases)` / exit 0 (observed, 6 named checks all PASS).
- Both mutation kills hold with exactly the entry's stated anchors: `huge_cap` FAIL on cap mutant;
  `redirect_private_refused` FAIL on redirect mutant; each leaves the other named arm PASS. Both
  mutants also fail the moved row-level checks (`row_states`, `summary`) — matches the entry's
  "each fail exactly their own arm plus the row-level checks they move".
- Named arms landed in the round-37 freeze: `e57c58b` has `huge_cap`/`redirect_private_refused`
  (2 hits); parent `842a320` has 0. Round-36 commit `1caa242` ships the two policies with only
  row-level evidence (S109/S110 rows, 0 named arms) — matches "Round 36 shipped the two policies
  with only row-level evidence (rows S109/S110)".
- Live receipt `drift-live-r37.txt` at scored rev carries exactly the entry's stated line:
  `MORI_SOURCE_DRIFT rows=220 fresh=49 excerpt=0 drifted=9 unavailable=0 no-copy=162` (exit 1).
- C2 counter at scored rev: all checks PASS, `C2=met`, exit 0 (observed).

---

## Adjacent finding (outside the four assigned ranges)

The entry's `verified-at` line claims: *"the hardening code landed at lane commit `8ff9bba`
(round 36, wave-2 Sentinel repairs)"*, and the heading says *landed `8ff9bba`*. Verified against
the git/jj backend, this attribution is wrong:

- `8ff9bba` (`jj` change `rtkpmvlotssy`) = *"round-36: wave-2 late reports + registry used-by
  repairs"* — it does **not** touch `tools/mori-source-drift.py` (`git show 8ff9bba --stat` on the
  tool is empty; the tool at `8ff9bba` has 0 hits for `FETCH_MAX_BYTES`/`_public_redirect_target`).
- The hardening code actually landed at `1caa242` (`jj` change `mzwpvzplklmm`) = *"round-36:
  sentinel repairs + final seats — drift tool read cap (4MiB) and post-redirect public-destination
  policy with selftest arms (SentTools/SentCensus…)"* (70 insertions / 3 deletions to the tool;
  `8ff9bba` is an ancestor of `1caa242`).
- The lane's own committed lesson `corpus/lessons/round-36-verifier-spotcheck.md:30` carries the
  correct attribution: *"Post-sentinel hardening (4MiB read cap, post-redirect public-destination
  policy) committed at `1caa2423`"*; `dispatch-log.txt:60` likewise: *"sentinel repairs landed
  `1caa242328d6` — drift tool read cap"*.

Impact: `count-c2.py` hard-codes `HARDENING_COMMIT = "8ff9bba"` and its `knowledge` check only
tests substring presence of that string in the entry, so C2 passes on a misattributed commit. The
four cited line ranges hold regardless; this finding is reported for completeness and does not
change the range verdict below.

## VERDICT: PASS

All four cited ranges (`:54,163-166`, `:113-136`, `:156-159`, `:103-108`) hold at scored rev
`e57c58b57c025364e79d130fbdf764d2674d83d6`. (Adjacent, out-of-range attribution defect documented
above; see `corpus/knowledge/source-drift-hardening-r37.md:9,25` vs `git show 1caa242` /
`round-36-verifier-spotcheck.md:30`.)

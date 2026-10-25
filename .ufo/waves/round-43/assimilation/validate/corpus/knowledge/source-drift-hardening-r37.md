# source-drift probe hardening — bounded read and post-redirect destination policy

source: S221 — RFC 9110 §15.4 (3xx redirect semantics); S222 — OWASP SSRF Prevention Cheat Sheet
(redirect-following as a bypass; client-side countermeasure); S223 — Python 3 `urllib.request`
(`HTTPRedirectHandler` and its documented deviation); S224 — Yama LSM docs (`ptrace_scope` 1);
S225 — Fetch Standard §4.5 (redirect-fetch chain, twenty-hop limit). S205 — the corpus contract in
fleet `CORPUS.md` (a row is a claim; append-only cells).
verified-at: 2026-10-23 — the five sources were opened this round; the hardening code landed at
lane commit `1caa242` (round 36, wave-2 Sentinel repairs) and the two named selftest arms landed
this round with the round-37 freeze.
recheck: on the next change to `tools/mori-source-drift.py`'s fetch path, and at the rows' own
cadence (S221/S222/S223 180d, S225 90d, S224 on-release).

## What the probe does

`tools/mori-source-drift.py --root .` re-fetches every `corpus/SOURCES.md` row that carries a
committed copy under `corpus/evidence/sources-r<N>/<id>.<ext>` (highest N) and prints one
`<id> <state>` line per row, then a summary. States: `fresh` (sha256 equal), `excerpt` (the
stripped copy occurs contiguously in the body), `drifted` (neither), `unavailable` (the GET did not
yield a 2xx body, or the body is over the cap, or a redirect landed on a non-public destination),
`no-copy` (no fetch is made). Exit 0 when nothing drifted, 1 when any row drifted, 2 on setup
error. It is a **byte-behavior** probe: `drifted` means the committed copy is not reproducible
from today's body, never "the source changed" (QUALITY 105).

## The two hardening policies (landed `1caa242`)

1. **Bounded read — `FETCH_MAX_BYTES = 4 * 1024 * 1024`,** read as `FETCH_MAX_BYTES + 1`
   (`tools/mori-source-drift.py:54,163-166`). An untrusted source must not stream past the cap or
   stall between bytes past the socket timeout; an over-cap body is not classifiable and grades
   `unavailable`. Ground: a body is the input to a byte comparison; without a bound, a hostile or
   broken server decides how much memory the probe spends.
2. **Post-redirect destination policy — `_public_redirect_target`**
   (`tools/mori-source-drift.py:113-136`, applied at `:156-159`). Redirects are followed (a 3xx is
   not a body, S221), but a server-driven redirect must land on a public `http`/`https`
   destination: loopback, link-local, private literals and `localhost`/`.local` names are refused
   (`unavailable`). Ground: redirect-following is a named input-validation bypass and disabling it
   is the client-side countermeasure (S222); a client that must follow redirects must therefore
   check where it landed. The initial request keeps loopback fetchable because the registry is
   lane-curated and append-only and the probe's own selftest serves on `127.0.0.1`
   (`:103-108`) — the asymmetry is deliberate and is exercised by the arms below.

## Named arms and their mutation kills (round 37)

Round 36 shipped the two policies with only row-level evidence (rows S109/S110 in the selftest).
Round 37 adds two **named** arms to `--selftest` and pins each policy's load-bearing role with a
mutation:

| arm | what it asserts | mutation that must kill it |
|---|---|---|
| `huge_cap` | a 4 MiB + 64-byte body grades over-cap (`unavailable`) while an exactly 4 MiB body is classified (`fresh`) | `FETCH_MAX_BYTES = 4 * 1024 * 1024` → `1 << 40` → arm FAIL |
| `redirect_private_refused` | a 302 to a loopback URL is refused after following | `if not _public_redirect_target(final):` → `if False:` → arm FAIL |

`python3 tools/mori-source-drift.py --selftest` now prints `PASS (6 cases)`; the two mutants each
fail exactly their own arm plus the row-level checks they move (receipts:
`.ufo/waves/round-37/evidence/c2-after.txt`, produced by
`python3 .ufo/waves/round-37/count-c2.py <rev>`). A copy with the policy removed cannot pass the
counter, so "the policy is present in the bytes" and "the policy is what makes the arm pass" are
separate, checkable statements.

## Live demonstration (round 37)

Two runs on 2026-10-23. At round start, on the entering 220-row registry:
`MORI_SOURCE_DRIFT rows=220 fresh=49 excerpt=0 drifted=9 unavailable=0 no-copy=162`, exit 1
(`.ufo/waves/round-37/evidence/drift-live-r37-start.txt`). At the scored tip, with this round's five
rows and their copies committed: `MORI_SOURCE_DRIFT rows=225 fresh=53 excerpt=0 drifted=10
unavailable=0 no-copy=162`, exit 1 (`evidence/drift-live-r37.txt`). The ten drifted ids are the nine
round-36 rows (`corpus/knowledge/source-drift-r36.md`) plus **S223**, which drifted on one line between
its copy and the tip run — the page's "Last updated" footer clock (S223.src:1953 vs the live line).
S223 is therefore a byte-unstable page of the S211 class: it can never score `fresh`, and the drift is
a representation difference, not a taught-claim change.

## Honest limits (disclosed, not remediated — detection and report only)

- **Final destination only.** urllib follows the whole chain before the policy sees a URL, so an
  intermediate hop to a private address is fetched; only the final authority is checked. The chain
  itself is a sequence of re-issued requests with its own hop bound (S225); checking each hop needs
  a redirect-handler subclass, not this probe's predicate.
- **DNS-resolved private addresses are not re-checked.** A public name that resolves to a private
  address is decided by urllib's resolver; the policy sees the literal/name, never the address it
  resolves to.
- **Over-cap is `unavailable`, not `drifted`.** The cap trades classification of very large bodies
  for memory safety; a row whose body exceeds 4 MiB can never score `fresh`. No row currently does.
- **A refused redirect hides the body.** A row whose source legitimately moved to a non-public
  destination grades `unavailable`; the probe reports the state and leaves the disposition to the
  operator.
- **`ptrace_scope` is host policy, not counter design.** The round-36 memoization residual
  (`.ufo/waves/round-36/w2/RevNgC2.md` §1) notes that a child tool cannot read the counter
  ancestor's heap only while `kernel.yama.ptrace_scope = 1` (S224); the counter does not enforce
  that boundary.

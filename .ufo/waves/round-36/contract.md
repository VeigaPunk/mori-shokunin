# mori round 36 — claim contract (frozen before any data seat)

L1 `MoriR36`, entering tip `6bd57097f7ab2b471b4593ed2019c980b1368c68` (round 35 rejected-honest-stop, MANIFEST
`rounds[531]`). Round shape and anti-loop ruling: no calibration claim this round (four straight calibration counters
could not tell real content from junk, r32–r35). Both claims are capability acquisitions: a program whose output is
checked against a truth the counter generates at run time and never writes where the program can read it, plus a
real-input arm on the lane's own bytes with a known witness.

## Claims

| id | axis (surface changed) | capability | before | after (target) |
|---|---|---|---|---|
| C1 | freshness (lowest-scoring non-retired axis, tied at 5 with depth and calibration) — surface: a new lane tool `tools/mori-source-drift.py`, a new operation (re-fetch each SOURCES row that has a committed copy and classify it against that copy) | flags stale source rows: `fresh`, `excerpt`, `drifted`, `unavailable`, `no-copy` per row | `count-c1.py 6bd57097` → `C1=unmet` (tool absent) | `count-c1.py <landed tip>` → `C1=met` |
| C2 | operability — surface: a new registered lane gate `tools/mori-sources-appendonly.py` (promoted from the round-35 wave script) with a new operation (deleted-row detection) and a fixture self-test | reports in-place edits, deleted rows, superseders and round-changed ids of `corpus/SOURCES.md` | `count-c2.py 6bd57097` → `C2=unmet` (tool absent) | `count-c2.py <landed tip>` → `C2=met` |

Both claims rest on one SOURCES row opened this round: the fleet `CORPUS.md` section *SOURCES.md — where a shokunin
learns* at a pinned fleet commit (rule 2 append-only; the `recheck` column). The row id is assigned when it lands.

## Frozen predicates (the same sentence is printed by the counter and used as the receipt label)

P-C1: at revision R, tools/mori-source-drift.py classifies every row of a 40-row blind fixture drawn at run time exactly as the counter's hidden truth, and on the lane's own corpus/SOURCES.md at R it agrees with the counter's independent live oracle on every row the oracle classified, with at least 10 oracle-fetched rows including at least one oracle-fresh and one oracle-drifted row.

P-C2: at revision R, tools/mori-sources-appendonly.py prints exactly the counter's hidden truth for ids, deleted, superseded and round_changed on each of 24 sandbox SOURCES.md histories drawn at run time, and on the lane's own history (rev 6bd57097, round base f10a320d) it prints exactly the counter's independent oracle, which lists at least one id.

Counters: `.ufo/waves/round-36/count-c1.py` and `count-c2.py`. Usage `python3 count-cN.py <rev> [--repo DIR] [--tool FILE]
[--seed N]`. `<rev>` resolves in `--repo` (default the lane). Without `--tool` the counter runs `git show
<rev>:tools/<tool>` from a temp file; with `--tool FILE` it runs FILE instead (controls only). `--seed` is for replay
only; a scored run draws its seed from `os.urandom` and prints it after scoring. Each run prints the predicate
sentence verbatim, per-arm results, and a final `C1=met` / `C1=unmet` (exit 0 / 1); exit 2 is could-not-evaluate
(no verdict). Their sha256 is recorded in `evidence/freeze.txt` at the freeze commit; any later byte change makes a
later receipt not a receipt of this claim.

## C1 tool interface (the counter tests this and only this)

`python3 tools/mori-source-drift.py --root DIR`. Reads `DIR/corpus/SOURCES.md`; a registry row is a line starting
`| S` followed by three digits; its id is the first cell, its URL is the first `http://` or `https://` URL in the
second (`source`) cell with trailing `.,;)` stripped. Its copy is the file `DIR/corpus/evidence/sources-r<N>/<id>.<ext>`
(any extension) with the highest integer `N`. Per row, in registry order, print one line `<id> <state>`:
- `no-copy`: the row has no URL or no copy file (no fetch is made);
- `unavailable`: the GET fails (connection error, timeout, or a non-2xx final status; redirects are followed; the tool
  may retry);
- `fresh`: sha256 of the fetched body equals sha256 of the copy bytes;
- `excerpt`: not fresh, and the copy bytes with ASCII whitespace stripped at both ends are non-empty and occur
  contiguously in the fetched body;
- `drifted`: otherwise.
Then one summary line `MORI_SOURCE_DRIFT rows=N fresh=a excerpt=b drifted=c unavailable=d no-copy=e`. Exit 0 when
`drifted=0`, 1 when any row is drifted, 2 on a setup error (missing or unreadable SOURCES.md). Read-only: no writes.

Blind arm (counter): a fresh temp root under `/fast/scratch/hyaku/mori-r36/`, 40 rows, 8 per state, ids drawn without
replacement from S001–S299, random paths and file extensions, copies in random `sources-r<N>` directories with an
older decoy copy (different bytes) in a lower-numbered directory for some rows, served from memory by a local HTTP
server; `drifted` bodies include same-length byte flips; `unavailable` rows return 404 or 500. Truth stays in counter
memory. Real arm: the tool run with `--root` the repository itself (v2), whose `corpus/` must equal R (no diff, no untracked file under `corpus/`, else unmet); the counter's own oracle fetches each row with a copy
(up to five tries, sequential, honoring `Retry-After` on HTTP 429, backoff 5/10/20/30 s otherwise); rows the oracle
could not fetch are excluded; every other row must match. A tool `unavailable` on an oracle-fetched row is re-probed
once by the oracle: it is a mismatch when the re-probe fetches the row, and the row is excluded (printed
`real_excluded_throttled`) when it does not. When the blind arm fails the verdict is already `C1=unmet` and the real
arm is skipped (printed `real_arm=skipped`), to spare the rate-limited hosts.

## C2 tool interface

`python3 tools/mori-sources-appendonly.py <rev> [--repo DIR] [--round-base REV] [--path P]` (default path
`corpus/SOURCES.md`, default repo the cwd; read-only git). Cells are compared stripped; columns are taken by header
position (id source kind tier scope anchor teaches status opened recheck used-by); immutable = every column but
`status`, `recheck`, `used-by`. Row identity is the id, not the line position. Output: per changed id a line
`changed <id> superseded_by=<id or ->`; per deleted id a line `deleted <id>`; then the summary
`appendonly_violations=N ids=[...] deleted=[...] superseded=[...] round_changed=[...]` (ids sorted, comma-separated, no
spaces; `round_changed=[]` printed when `--round-base` is absent). Definitions:
- `ids`: rows present at `<rev>` whose immutable cells differ from the cells the row had in the first ancestry commit
  holding that id (endpoint comparison; QUALITY 102);
- `deleted`: ids held by some ancestry commit of `<rev>` and absent at `<rev>`;
- `superseded`: ids in `ids` for which a row present at `<rev>` has a teaches cell opening `supersedes S###`;
- `round_changed`: ids whose immutable cells changed, or which were deleted, in any commit in `REV..<rev>` that
  touches the path (an id changed back inside the range is listed);
- `appendonly_violations` = len(ids) + len(deleted).
Exit 2 on error; with `--round-base` exit 1 iff `round_changed` is non-empty, else exit 1 iff ids or deleted is
non-empty; otherwise 0.

Blind arm (counter): 24 sandbox git repos under `/fast/scratch/hyaku/mori-r36/`, each a random history of 4–8
commits with neutral messages, ops drawn per commit: append row, edit a mutable cell, edit an immutable cell,
revert an earlier immutable edit, delete a row, append a superseding row for an edited id, reorder rows. At least 12
histories carry a deletion and at least 12 a changed-back id; the round base is a random commit. Truth is computed
from the op log, not from git. Real arm: the lane repository itself, read-only git (v2; no clone); the counter's oracle walks `git log` of the path itself.

## Controls (QUALITY 98, 99, 101 and the anti-loop five; scored under the frozen counters before any data seat)

Every control is a substitute program passed with `--tool`; a met control forces a re-design before data or an
exploratory declaration, never a residual ruling.

| shape | C1 control | C2 control |
|---|---|---|
| skip-work / do-nothing | K1 prints nothing, exit 0 | J1 prints an empty summary, exit 0 |
| content-free / empty | K11 prints `<id> unknown` per row (no decision) | J13 prints counts only, no ids |
| generic rows / copying the observed column | K2 every row `fresh`; K4 never reads the copy (fetched → `fresh`, else `unavailable`) | J3 every id at rev in every list |
| denial | K5 the real rules with labels inverted (fresh↔drifted, excerpt↔drifted) | J8 the complement of the true ids |
| word bag | K6 a random state per row | J9 random ids |
| off-topic | K7 maps the row's own `status` cell (mined/queued/…) to states | J12 reports mutable-cell changes instead |
| label- or id-keyed (99 i; generator label families: id, extension, `sources-r<N>` number, path, port) | K8 state from id parity, extension and directory number | J10 flags ids by id-number pattern and commit order |
| harness-keyed (99 ii) | K9 real rules only for 127.0.0.1 URLs or roots under /fast/scratch; constant `fresh` otherwise | J11 real rules only for repos under /fast/scratch or /tmp; empty summary otherwise |
| server echo | K10 length-only comparison (Content-Length or body length vs copy size) | inapplicable: no server; the oracle is the truth, never printed |
| rule-level skips | K3 sha-only (no excerpt, no unavailable logic); K13 reads the oldest copy, not the newest | J2 the round-35 checker as committed at 6bd57097; J4 endpoint-only round_changed; J5 no deleted arm; J6 rows keyed by line position; J7 a superseder removes the id from ids |
| rule changed after data | inapplicable as a program: the counters' sha256 are pinned in `evidence/freeze.txt` | same |

## v2 re-design before data (round-36 C0 receipts, QUALITY 98)

Under the v1 counters (sha256 `ed3f0e5e…4145`, `302f9aa0…affb`, frozen at `da12b378`) three controls met before any
data seat: K9 and J11 (harness-keyed: the v1 real arms ran on a temp `git archive` extraction and a clone under
`/fast/scratch`, which the controls detected by path) and K13 (oldest copy: the v1 blind arm held decoy rows as list
indices and never wrote a decoy copy). By QUALITY 98 the counter was wrong; it is re-designed before data: both
real arms run on the repository path itself, and decoys are written on 12 fresh/excerpt rows. The predicate
sentences P-C1 and P-C2 are unchanged. Every C0 control is re-scored under v2 (`evidence/c0-rescore-v2.txt`) and the
v2 freeze sha256 is in `evidence/freeze-v2.txt`.

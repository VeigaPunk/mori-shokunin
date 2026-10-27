# Mo57Executor41 — C2 source-grounding + frozen counter execution (round 57, w1)

Assigned arm: **C2** (depth — source-grounded interpretation of the round-56
driver-liveness `unclosed` field). Lane repo `/home/vgpnk/Projects/shokunin/mori-shokunin`.
Entering revision `53e2b4768af93dd2472eb26ecc9b9fdca2e9daf2`; freeze
`618562c72a03dc4d17386b715357f863fd327274`. Detection only — no production edit,
no commit, no host remediation.

Scratch: `/fast/scratch/hyaku/mori-r57/Mo57Executor41/` (TMPDIR set there; fixtures
and the forged clone live only under scratch, each with `git -C` explicit paths and a
`git rev-parse --show-toplevel` assertion printing the fixture dir). No tool installed
or updated (nothing needed; pacman untouched).

## 1. Frozen counters at the entering revision — reproduced exactly

    $ cd /home/vgpnk/Projects/shokunin/mori-shokunin
    $ python3 .ufo/waves/round-57/count-c2.py 53e2b4768af93dd2472eb26ecc9b9fdca2e9daf2
    C2=unmet claims=0 source=bad rev=53e2b4768af93dd2472eb26ecc9b9fdca2e9daf2
    exit=1

    $ python3 .ufo/waves/round-57/count-c1.py 53e2b4768af93dd2472eb26ecc9b9fdca2e9daf2
    C1=unmet rows=0 evidence=bad rev=53e2b4768af93dd2472eb26ecc9b9fdca2e9daf2
    exit=1

Both outputs and exit codes match `.ufo/waves/round-57/controls.txt` byte for byte.
Precondition probed directly:

    $ git cat-file -e 53e2b47:corpus/knowledge/watchdog-unclosed-r57.md
    fatal: path 'corpus/knowledge/watchdog-unclosed-r57.md' does not exist in ...
    exit=128
    $ git show 53e2b47:corpus/SOURCES.md | grep -n "S548"   # exit=1 (absent)
    $ git show 53e2b47:corpus/SOURCES.md | grep -oE '^\| S[0-9]+' | sort -u | tail -1
    | S547

So the C2 entry is absent and the highest registry row is **S547**; a compliant wave must
open **S548** (`corpus/SOURCES.md`) and add the entry. Both before-states are genuine, not
counter artifacts.

## 2. Independent source-grounding of the C2 claim

**Claim under test** (`corpus/knowledge/driver-liveness-r56.md`, `## Limits`): "`in_flight`/
`unclosed` are pairing facts over log lines, not health verdicts; a lane with an unclosed
launch is *in flight by the log*, not "stuck"." Plus the field definition
(`tools/mori-driver-liveness.py:35-36`): `unclosed` = "launches with no same-(lane,round,attempt)
complete — a pairing count, not a failure claim".

**Exact quote located in the committed source copy**
`corpus/evidence/sources-r56/watchdog-log-grammar-v2.txt:1-2` (verified against the copy, not
paraphrased):

    log "launch $lane round=$n pgid=$$ driver=hyaku-inline attempt=$a"
    log "complete $lane round=$n; hyaku-inline attempt=$(claim "$lane" attempt)"

Committed-copy digests re-derived independently, matching the entry's published prefixes:

    $ sha256sum corpus/evidence/sources-r56/watchdog-log-grammar.txt
    38ba3e6b309e17d3d8038e8986e274bb363ac893d1c325fe145a95882a417796   # entry: 38ba3e6b… OK
    $ sha256sum corpus/evidence/sources-r56/watchdog-log-grammar-v2.txt
    1ea4524ca9c65ec8a3c2ea27f8c6e67004fd2f11a63a8c63555c3ec6df88cfa2   # entry: 1ea4524c… OK

**What the quote establishes.** The writer emits a `launch` line at spawn and a *separate*
`complete` line at exit; nothing in either script emits a "currently running" marker. The
only way to state liveness from this log is to reconstruct a pairing after the fact. That is
exactly the claim's mechanism, and it is structural, not editorial.

**Executed test of the claim against the implementation** (`tools/mori-driver-liveness.py`):
`unclosed` is `len(row["open_launches"])` at `:173`; `open_launches` is *appended on launch*
(`:133`) and *removed only* by a matching close (`close_round`, `:116-120`) or by the
round-scoped dead clear (`:157`). Nothing else decays it. Therefore `unclosed` is a residue
accumulated over every round in the log, which is incompatible with a present-running count.
**Verdict: claim SUPPORTED.**

Decisive corroboration from the committed live receipt
`.ufo/waves/round-56/evidence/driver-liveness-live.txt` (parsed with
`json.JSONDecoder().raw_decode`, since the file carries a trailing `exit=0` line):

    23 lanes, verdict DRIVER_LIVENESS_OK
    in_flight=false AND unclosed>0 : 9 of 23 lanes
      kagi 10 | kotoba 7 | kaidoku 6 | kasegi 6 | kengaku 6
      tsukuroi 5 | kotodama 4 | revenger 4 | kumitate 3

Nine lanes are *not in flight* yet report unclosed launches — a present-running count would
have to read 0 there. `mori` itself: launches 66, completes 39, deads 17, wraps 0,
`rounds_seen` 46, `in_flight` true, `unclosed` 10 — ten residues spread over a 46-round
window, and 66−39−17=10.

## 3. Interpretive limits found (beyond the entry's own wording)

Reproduced on scratch fixtures with the real tool, `--fixture` mode (read-only input):

**(a) Cross-round residue — proves "not present-running".**
`fx/cross-round/watchdog.log`: launch round=4 (never closed), launch round=5, complete
round=5 → `{"in_flight": false, "rounds_seen": 2, "unclosed": 1, "launches": 2,
"completes": 1}`. The lane's only open launch is in a *past* round while round 5 closed
cleanly; the lane is not running, yet `unclosed` reads 1.

**(b) Attempt rollover over-counts on a round that completed.**
`fx/attempt-mismatch/watchdog.log`: launch round=5 attempt=1, complete round=5 attempt=2 →
`{"completes": 1, "in_flight": false, "unclosed": 1}`. `close_round()` keys on
`(round, attempt)` and its only fallback is `(round, None)` (`:116-120`), so an attempt
mismatch closes nothing and a *completed* round stays counted as unclosed. The mechanism is
source-reachable and the source copy shows why: the complete line's attempt is
`$(claim "$lane" attempt)` — mutable state read at complete time, so a rollover between
launch and complete can legitimately differ. Live impact today is nil: scanning the live
`/home/vgpnk/Projects/shokunin/.ufo/watchdog.log` for launch/complete pairs with differing
attempt tokens returned **0**.

**(c) One dead line closes every open launch of its round.**
`fx/dead-multi/watchdog.log`: launch round=5 attempt=1, launch round=5 attempt=2, dead
round=5 → `{"deads": 1, "launches": 2, "unclosed": 0}`. `:157` filters *all* keys of that
round. So `unclosed` is not a literal per-event pairing either — it is a round-scoped
residue. Consistent with the armed `unclosed == launches − completes − deads − wraps`
identity holding on only **6 of 23** live lanes, with `kumitate` at residue −4 (9 deads, some
finding no open launch).

These three are *limits*, not falsifications: they keep the claim intact (shape fact, never a
liveness verdict) and tighten the word "pairing". None is a defect claim; none is patched here.

## 4. Frozen C2 counter — fence inspection (findings only)

`count-c2.py:12-16` tests four things: `len(claims)==8`, `source_ok`, `quote_ok`, and the
substring `"pairing count"`. Mapped against the contract's C2 predicate:

| Contract clause | Counter line | Actually tested? |
|---|---|---|
| entry "opens with `source:`, `verified-at:`, `recheck:`" | none | **no** — no header check at all |
| eight claim rows | `:12,15` | count yes; **distinctness no** (8 identical rows pass) |
| each claim "with a located quote in the source copy" | `:14` | **no** — `quote_ok=all("`" in x and "`" in x ...)` only asserts two backticks exist on the line; nothing is looked up in `corpus/evidence/sources-r56/` |
| "cites a newly opened source row" | `:13` | **partly** — `"| S548 |" in registry` plus `"S548" in entry`; never compares against the entering revision, so S547 re-labelled or a pre-existing row would pass |
| "states that `unclosed` is a pairing count rather than a present-running count" | `:15` | **no** — `"pairing count" in entry` is substring-only and negation-blind |

Demonstrated bypass on a scratch clone
`/fast/scratch/hyaku/mori-r57/Mo57Executor41/forge` (own `git init`, toplevel asserted),
counter copied to `$S/c2-forge.py` with only `repo=` repointed at the fixture:

    entry: no source:/verified-at:/recheck: header; 8 duplicate rows "| K1..K8 | `` `` |";
           text "Cites S548. ... it is not a pairing count."
    registry: "| S548 | forged row, quotes mined nowhere | x |"

    $ python3 c2-forge.py 2d69369fdce9457a8df85303d6a24b009b7f897f
    C2=met claims=8 source=ok quotes=ok rev=2d69369fdce9457a8df85303d6a24b009b7f897f
    exit=0

The counter reports **met** for an entry with zero located quotes, no header, eight
duplicate claims, a negation, and an S548 row that is not newly opened. This is a fence gap
against the frozen predicate as written; the predicate and counter are immutable after
scoring, so this is reported, not repaired.

## 5. Verdict

- C2 baseline at `53e2b47`: `unmet claims=0 source=bad`, exit 1 — genuine, matches controls.
- C2's substantive claim ("`unclosed` is a pairing count, not a present-running count") is
  **supported** by the committed source copy (`watchdog-log-grammar-v2.txt:1-2`, hashes
  verified), by the implementation (`:116-120,133,157,173`), and by 9 of 23 live lanes with
  `in_flight=false` yet `unclosed>0`.
- Three interpretive limits are reachable and should be stated in any C2 entry that claims
  depth on this field: cross-round residue, attempt-rollover over-count (0 live instances),
  and round-scoped dead clearing (identity holds 6/23).
- The frozen C2 counter accepts a forgery that fails three named contract clauses
  (`C2=met`, exit 0) — a counter-fence finding, not a verdict on any delivered entry.

Evidence commands are all reproducible from the lane repo and the paths above; scratch
fixtures were removed after capture.

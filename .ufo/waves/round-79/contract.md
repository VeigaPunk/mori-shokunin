# mori round 79 — contract (frozen before any data)

author: mori L1 (MoriR79)
round: 79
date: 2026-11-04
entering: `84c6cbc3b47c536a504aaee329c77897d389935e` (branch master, pushed; lane clean
tracked=0 untracked=0 at round start)

Three claims, each one axis-move on a distinct axis, each verifiable without the others
having landed. The lowest-scoring non-retired axes are depth/freshness/calibration (all 5);
C2 (calibration) and C3 (freshness) work that floor. C1 works operability (7) as a
capability acquisition, which AXES.md admits without a score move.

## C1 — operability (capability acquisition): the control-receipt binding guard

Predicate P-C1 (the same sentence in this contract, in `count-c1.py` and in the receipt label):

> At revision R, `tools/mori-control-receipt.py` exists as a committed blob; run from that
> blob with `python -I`, `--selftest` prints `CONTROL_RECEIPT_SELFTEST pass=P fail=F` with
> P >= 10 and F = 0 at rc 0; a live run over `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-78/evidence`
> exits 1 and its stdout names `controls-r78.txt` together with the key
> `correction_marker_in_LOG_at_entering` (the D78-1 witness, the closure's routed defect:
> a control receipt stating a count with no counting command); and a live run over
> `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-79/evidence` exits 0 with
> `unbound=0`.

Tool spec (the seat builds to this; the counter grades behavior, not source shape):

- input: one or more receipt paths, or `--dir DIR` (every `*.txt` directly under DIR, sorted);
  `--selftest`; `--help`.
- a receipt is split into sections at lines matching `^## ` (content before the first
  heading is section `(head)`).
- a **count claim** is a stripped line matching `^[A-Za-z][A-Za-z0-9_.-]*=-?[0-9]+$`.
- a section is **bound** iff it contains at least one command line, where a command line is
  a non-comment line whose stripped text starts with `$ ` or whose first token is one of
  `git grep egrep python python3 bash sh curl wget wc sha256sum ls cat awk sed jq node
  systemctl journalctl df du ps stat find sort comm cmp head tail xxd od readlink realpath
  ss lsof tar zcat rg`, or a non-comment line containing ` cmd=`.
- output per file: `CONTROL_RECEIPT <path> sections=S claims=C bound=B unbound=U` plus one
  `unbound <path>#<section> claims=N keys=<k1,k2>` line per unbound section; a final
  `CONTROL_RECEIPT_SUMMARY files=F sections=S claims=C unbound=U`.
- rc 0 iff no section with claims is unbound; rc 1 if any is; rc 2 setup (usage, missing
  path, unreadable file). stdout only: no file writes, no network, no subprocess, no
  `/tmp` path of its own, no host-identifying material.

Before (do-nothing control): `git cat-file -e 84c6cbc3:tools/mori-control-receipt.py` rc 128;
`git log --all --oneline -- tools/mori-control-receipt.py` empty.

After (target): the tool at the landed commit, C1=met by `count-c1.py`.

## C2 — calibration: the axes table's `Last change` cells against the fleet record

Predicate P-C2 (same sentence in contract, counter and receipt label):

> At revision R, SCORECARD.md's `## Axes` table has exactly one row per axis in
> {coverage, operability, depth, freshness, calibration, adjacency}; for each axis the
> `Last change` cell's first `round N` equals N*, the highest mori lane round <= 78 that
> `/home/vgpnk/Projects/shokunin/MANIFEST.json` records with `admitted: true` and that axis
> graded `improved` or `harmed`; and the text from that `round N` up to the next `;` carries
> that verdict word. Mismatches = axes violating either half.

Convention: the r50 correction in SCORECARD.md ("Last change here means the latest admitted
closure grading the axis improved or harmed, not the latest score move"). Narrowed scope,
named as a limit before data: this predicate does not check the `Evidence` cell (the r50
counter did); only the `Last change` clause is graded.

Fleet record at freeze (MANIFEST.json read at the fleet tip, admitted mori rows only):
coverage 56 improved, operability 78 improved, depth 76 improved, freshness 78 improved,
calibration 78 improved, adjacency 19 improved.

Before (do-nothing control): `count-c2.py 84c6cbc3...` -> mismatch count > 0 (cells lead
with rounds 47/47/49/28/50/19). After (target): `C2=met mismatches=0` at the landed rev.

## C3 — freshness (sourced): RFC 9111 §4.1, the Vary-selected representation

Predicate P-C3 (same sentence in contract, counter and receipt label):

> At revision R: `corpus/SOURCES.md` carries 367 registry rows (`^\|\s*S\d{3,}\s*\|`), the
> new row `S594` reads status `mined`, its `source` cell names
> `https://www.rfc-editor.org/rfc/rfc9111.txt`, its anchor cell names
> `corpus/evidence/sources-r79/rfc9111.txt` and that blob's sha256 at R; its `used-by` cell
> names `corpus/knowledge/ua-serving-normative-r79.md`; the entry exists at R with
> `source:` naming S594, a `verified-at:` line and a `recheck:` line; and `corpus/README.md`
> carries a knowledge-index row naming the entry.

The entry grounds the lane's empirical `ua-serving` drift class (QUALITY 159; S591/S592/S593)
in the normative text that a Vary-nominated request header field selects among stored
representations, so a byte difference between two fetches of one URL under different
User-Agent values is a representation selection, not content drift by itself.

Before (do-nothing control): S594 rows 0 at entering; the entry absent at entering.
After (target): `C3=met` at the landed rev, and the round-end census rc 0.

## Kill rules and controls

- Each claim's counter is frozen in this commit; the target is the counter's own `met`
  output, and a claim that misses is reported as an honest stop, never narrowed.
- If any counter's `--selftest` fails, the counters are repaired before data lands.
- A claim is killed by its own do-nothing control: if the entering rev already meets the
  target, the claim is withdrawn.
- No claim narrows or widens a frozen claim of an earlier round.
- Wave seats never edit the counters, the contract, or the fleet MANIFEST; they produce
  evidence and candidate text only. The L1 integrates and lands.

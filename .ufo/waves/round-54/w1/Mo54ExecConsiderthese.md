# Mo54ExecConsiderthese — re-executing what the round-53 closure only evidence-verified

Seat: Mo54ExecConsiderthese (executor, leaf). Lane: mori-shokunin. Date: 2026-10-27.
Assignment: `considerthese/2026-10-26.md` suggestion 3 ("re-execute what closures only evidence-verified"),
scored revision `0b36d23e596276c70725873621fe15a28c87189f`, instruments from a `git archive` of
`28401324ca5e0205645490d8e538b30d5ef4d1bf` (the receipt commit on top of it).
Scratch: `/fast/scratch/hyaku/mori-r54/Mo54ExecConsiderthese/` — archive extraction (337 MB), one
`git clone --shared` of the lane checked out at `0b36d23e` (339 MB), and one small extracted-tool tree for
the data-commit selftest; all removed before this report was finished. Nothing cited below depends on it.
Host: MACHINE_ID, `uname -r` = `7.2.11-arch1-1`, `python3 -V` = Python 3.14.8. No tool installed, upgraded or
removed for this seat (nothing was needed); no pacman transaction attempted.

## What "evidence-verified only" meant, and what this seat did

The round-53 closure defines its terms itself, `corpus/lessons/round-53-verifier-spotcheck.md:59-60`:

> Re-measured = this closure ran its own plain measurement over committed bytes; evidence-verified = the lane's
> counter/gate receipts read (the counters and the tool were not executed, per §Gate standard).

So the closure re-derived the ledger, the vote parse and an oracle for the tool, but never ran `count-c1.py`,
`count-c2.py` or `mori-commit-runway.py --selftest`; those three verdict lines were read from receipts. This
seat ran all three at the scored revision and diffed every measured line against the receipt.

Commands (cwd = the archive extraction, or the clone at `0b36d23e` where marked):

```
python3 .ufo/waves/round-53/count-c1.py 0b36d23e596276c70725873621fe15a28c87189f --repo /home/vgpnk/Projects/shokunin/mori-shokunin
python3 .ufo/waves/round-53/count-c1.py --selftest                                  [archive]
python3 .ufo/waves/round-53/count-c2.py 0b36d23e596276c70725873621fe15a28c87189f --repo /home/vgpnk/Projects/shokunin/mori-shokunin --scratch <scratch>/fin/c2
python3 .ufo/waves/round-53/count-c2.py --selftest                                  [archive, TMPDIR=<scratch>/tmp]
python3 -I -B tools/mori-commit-runway.py --selftest                                [archive]
python3 .ufo/waves/round-53/count-c1.py 0b36d23e596276c70725873621fe15a28c87189f      [clone at 0b36d23e, default repo]
python3 .ufo/waves/round-53/count-c2.py 0b36d23e596276c70725873621fe15a28c87189f --scratch <scratch>/fin/c2-clone   [clone at 0b36d23e]
python3 -I -B tools/mori-commit-runway.py --selftest                                [clone at 0b36d23e]
python3 .ufo/waves/round-53/count-c1.py 0df803033fba2386b10f5dcc6aa96bdef65cba15      [salvage tip, clone]
python3 .ufo/waves/round-53/count-c2.py 0df803033fba2386b10f5dcc6aa96bdef65cba15 --scratch <scratch>/fin/c2-salvage
python3 -I -B <t>/tools/mori-commit-runway.py --selftest                             [tool+fixtures as of 2a4213bf]
python3 .ufo/waves/round-53/count-c1.py --scope                                      [clone]
python3 .ufo/waves/round-53/count-c1.py 20edafa59b38dac1ca358893f0259b1f436372d3      [negative control]
python3 .ufo/waves/round-53/count-c2.py 20edafa59b38dac1ca358893f0259b1f436372d3 --scratch <scratch>/fin/c2-neg
```

## Receipt comparison (token by token)

Method: extract only the measured lines from the receipt (`^C1=`, `^C2=`, the `ok`/summary lines of each
selftest, the two runway lines) and from my rerun, then `diff` them, then compare `split()` token lists
in Python. Every diff was empty and every token list equal; the `same_tokens` report printed `True` for
all 38 C1-selftest lines, all 31 C2-selftest lines and both runway lines, in both reproduction shapes.

| receipt | rerun (archive + `--repo`) | rerun (clone at `0b36d23e`) | diff rc |
|---|---|---|---|
| `evidence/c1-at-landed.txt` (16 tokens) | identical | identical | 0 / 0 |
| `evidence/c2-at-landed.txt` (10 tokens) | identical | identical | 0 / 0 |
| `evidence/selftest-c1.txt` (38 lines) | identical | — | 0 |
| `evidence/selftest-c2.txt` (31 lines) | identical | — | 0 |
| `evidence/selftests/mori-commit-runway-a2.txt` (2 lines) | identical | identical | 0 / 0 |
| `evidence/c1-at-salvage.txt` (extra) | — | identical | 0 |
| `evidence/c2-at-salvage.txt` (extra) | — | identical | 0 |

Literal rerun lines:

```
C1=met scope=46 rows=46 matched=46 status_ok=46 quote_ok=46 source_rows=ok pins=ok provenance=ok held=44 absent=2 holds=46 changed=0 voted=46 dissent=0 rev=0b36d23e596276c70725873621fe15a28c87189f
exit=0
C2=met tool=present selftest=pass n=31 fixtures=80 agree=80 disagree=0 registry=ok live=ok rev=0b36d23e596276c70725873621fe15a28c87189f
exit=0
MATCHER: rejected 26/26 corrupted expectations
MORI_COMMIT_RUNWAY_SELFTEST: PASS 31/31
exit=0
```

C1 selftest: 37 named arms + `C1_SELFTEST pass=37 fail=0`, exit 0. C2 selftest: 30 named arms +
`C2_SELFTEST pass=30 fail=0`, exit 0. Both match `selftest-c1.txt` / `selftest-c2.txt` line for line,
including arm order.

Salvage-tip reruns (extra coverage of the same closure, whose SCORECARD correction claims the at-salvage and
at-landed verdict lines are token-identical apart from `rev=`): reproduced at `0df80303` — both lines agree
with `c1-at-salvage.txt`/`c2-at-salvage.txt` exactly, so the two receipt pairs differ only in the `rev=`
token, as asserted at `SCORECARD.md:2850-2856`.

## Deliberation against a false green

A rerun that prints `met` proves nothing unless the same bytes can print `unmet`, and unless the bytes are the
frozen ones. Checks made:

- Instrument identity. `sha256sum` of the three instruments from the `28401324` archive, from the clone
  checked out at `0b36d23e`, and from the live lane working tree are equal:
  `count-c1.py ebaff9158362b9059…`, `count-c2.py 5684b69f7ae9030b…`, `tools/mori-commit-runway.py
  b3c123400f41a8e8…`; `git diff --stat 0b36d23e 28401324 -- <those three paths>` is empty (the receipt commit
  only adds receipts).
- Frozen bytes. `sha256sum -c --quiet .ufo/waves/round-53/evidence/freeze-sha256.txt` in the `28401324`
  extraction: 33 entries listed, rc 0 — the same reading the closure recorded.
- Receipts unmodified. Working-tree sha256 equals `git show 28401324:<path>` for all five receipts
  (`c1-at-landed bf567e5c790f…`, `c2-at-landed af423d9c77e8…`, `selftest-c1 02f270876589…`, `selftest-c2
  a280eb33fa66…`, `runway-a2 9266bbdfda89…`).
- Negative controls at the entering tip `20edafa5`: C1 → `C1=unmet scope=46 … failed=ledger_absent,pins`,
  exit 1; C2 → `C2=unmet tool=absent selftest=error n=0 fixtures=80 agree=0 disagree=0 registry=bad
  live=error failed=registry,tool_absent`, exit 1; `git cat-file -e 20edafa5:tools/mori-commit-runway.py`
  rc 128 (path not in tree). The counters therefore separate the pre-state from the landed state on this
  harness, and `met` is not a constant of the code path.
- The older runway receipt also reproduces: with `tools/mori-commit-runway.py` and
  `tools/fixtures/mori-commit-runway/cases.json` taken from `2a4213bf` (the round-53 data commit) into a
  `tools/`-shaped tree, `--selftest` prints `MATCHER: rejected 23/23 … PASS 23/23`, exit 0 — exactly
  `evidence/selftests/mori-commit-runway.txt`. `cases.json` holds 23 cases at `2a4213bf` and 26 at
  `28401324`, which accounts for 23 arms → 31 arms; the 31/31 figure belongs to the later tool, as the receipt
  says.
- `--scope` at the entering tip prints `scope=46`, the round-53 scope size.
- C2 seed identity. The counter derives the 64 seeded fixtures from `sha256(<full commit id of R>)`; the rerun
  echoes `rev=0b36d23e596276c70725873621fe15a28c87189f` (full id, from `rev-parse … ^{commit}` on the
  abbreviated argument), so the seeded fixture set is the same one the receipt scored, not merely a set of the
  same size. `agree=80` and `disagree=0` then mean the tool matched the reference reading on the same 16 frozen
  plus 64 seeded fixtures.
- C1 vote arm is derived from committed bytes only (`git show`/`ls-tree` inside the counter); the rerun's
  `voted=46 dissent=0` therefore does not depend on the working tree. The three runs of the counter (archive
  with `--repo`, clone with default repo, and the archive with `--repo` pointed at the lane tree) all returned
  the same line, which also shows the result is not a function of `--repo` path resolution.
- C2 `--scratch` is not load-bearing for the verdict: with the flag omitted (work dir under `$TMPDIR`) the
  line is again identical, exit 0; the counter removed its work directory (`<scratch>/fin/c2` empty afterwards).

## Host-dependence of the C2 live leg

`live=ok` is the one token whose reproduction is environment-bound (the counter names that itself: "the live leg
compares stable fields only (Committed_AS moves between reads) and depends on the host it runs on"). This host
at this run: `overcommit_memory=0`, `overcommit_ratio=50`, `overcommit_kbytes=0`,
`admin_reserve_kbytes=8192`, `user_reserve_kbytes=131072`, cpu present `0-31`, page 4 kB, `MemTotal 31721796 kB`,
`SwapTotal 31722876 kB`, `CommitLimit 47583772 kB`, `Committed_AS` read twice as 45843776 kB and 45483168 kB
(it moves — which is why only stable fields are compared). The tool's live reading:

```
{"band_kb": null, "batch_pages": null, "commit_limit_kb": 47583772, "committed_as_kb": 45483168, "cpus_present": 32, "enforced": false, "findings": [], "headroom_kb": 2100604, "limit_consistent": true, "limit_recomputed_kb": 47583772, "mode": 0, "notes": ["mode 0 (guess): the ledger is not compared with CommitLimit (printed, not enforced); each single request above RAM + swap is refused (single_request_cap_kb)"], "reserve_kb": null, "schema": "mori-commit-runway-v1", "single_request_cap_kb": 63444672, "usable_kb": null, "verdict": "COMMIT_HEURISTIC"}
exit=0
```

So `live=ok` means the tool's `mode`, `commit_limit_kb`, `limit_recomputed_kb`, `cpus_present` and
`limit_consistent` equalled the counter's reference reading on both `/proc/meminfo` samples; the host is in
mode 0 (`COMMIT_HEURISTIC`), so the mode-2 band leg never fires here (`band_kb=null`), and the receipt's
`live=ok` could not have exercised it either.

## Divergences

None in any measured line, token or arm name, in either reproduction shape, at either revision (`0b36d23e`,
`0df80303`). The only differences are in reproduction *shape*, all disclosed:

- The C1 receipt's command line has no `--repo` because it ran inside a clone whose root the counter's
  `lane_root()` derives from `__file__`; the seat spec's shape (archive + `--repo` lane tree) needs both. Both
  shapes were run and agree; the archive has no `.git`, so without `--repo` it stops at
  `C1_SETUP unresolvable revision …`, exit 2 (not a divergence of the verdict).
- The C2 receipt names `--scratch /fast/scratch/hyaku/mori-r53/L1/fin/c2`, which no longer exists; I used my own
  scratch path, and drove the run both with and without the flag.
- `TMPDIR` values differ between receipt and rerun (both under `/fast/scratch/hyaku/mori-r54/…` here).
- Receipt headers (timestamp, `TMPDIR`, clone path) were not compared: they are provenance, not measurement.
- The receipt does not record `python3 -V`; my run used 3.14.8.

## Limits and routed items (named, not fixed — the counters are frozen)

1. This seat re-executed the counters at the scored revision; it did not re-fetch the kernel bytes. `pins=ok`
   proves the committed v7.3 copies match their frozen sha256, not that cgit served the v7.3 tag — the closure's
   own re-fetch of the nine round-53 copies is the evidence for provenance and I did not repeat it here
   (UNVERIFIED-by-this-seat; the round-54 fetching seats cover the round-54 copies).
2. The C2 live leg is near-tautological: the counter's `REF` and the tool share an author, and the compared
   fields exclude the moving values, so `live=ok` shows the tool reads the same files consistently with `REF`,
   not that either reading of the kernel is right. It also cannot exercise the mode-2 band on a mode-0 host.
3. Seed identity of the 64 seeded fixtures is only established through the echoed `rev=` token; the counter
   prints no digest of the fixture set. A receipt that kept a fixture-list digest would let a re-run be checked
   without trusting the rev line.
4. Receipts are not verbatim replayable: the C1 header omits `--repo`, the C2 header names a deleted scratch
   directory, and neither records the interpreter version or the instrument sha256. A three-line header
   (instrument sha256, `python3 -V`, `TMPDIR`) would make a re-execution check mechanical.
5. C1's verdict at `0df80303` and `0b36d23e` is identical, so the a2r1 ledger-cell corrections did not move any
   scored arm; that is reassuring for this claim but also means the counter's `met` cannot distinguish a ledger
   whose non-scored prose changed. (Contract already names data-vs-counter separation; recorded here as an
   observed property, not a defect.)

## Drafted lesson paragraph (for the L1 to lift; no file edited)

> **Re-execution closed the round-53 gap.** The round-53 closure labeled its C1/C2 verdicts
> `evidence-verified` and said so plainly (`counters and the tool were not executed, per §Gate standard`).
> Round 54 re-executed all three frozen instruments at `0b36d23e` from a `git archive` of the receipt commit and,
> in a second shape, from a clone checked out at the scored revision: `C1=met … voted=46 dissent=0`,
> `C2=met … agree=80 disagree=0 … live=ok`, `PASS 31/31`, `C1_SELFTEST pass=37 fail=0`, `C2_SELFTEST
> pass=30 fail=0`, plus the older `23/23` runway receipt at the data commit — every measured line token-identical
> to its receipt, with the negative controls still `unmet`. The closure's numbers were therefore not
> receipt-artifacts; what it lacked was execution, and cheap re-execution supplied it. What remains unexecuted is
> not the counters but the kernel: `pins=ok` and `live=ok` are consistency checks with the same author's reading
> of the kernel, so a future round buys more by re-fetching bytes and by recording a fixture-set digest than by
> re-running the counters a third time.

## Findings

- **LOW** — `.ufo/waves/round-53/evidence/c2-at-landed.txt` (and `c1-at-landed.txt`): the receipt header omits
  `--repo`/interpreter version and the C2 header names a scratch path that no longer exists, so neither receipt
  can be replayed verbatim without reconstruction. Routed item 4 above (round 55), not a counter change.
- **LOW** — `.ufo/waves/round-53/count-c2.py` (`live_check`): the live arm compares five stable fields only, so on
  a mode-0 host it never exercises the mode-2 band and cannot detect a band regression; `live=ok` here is weaker
  evidence than it reads. Named limit, counter frozen.
- **LOW** — `.ufo/waves/round-53/count-c2.py` (`seeded_fixtures(seed)`): the 64 seeded fixtures are identified
  only by the echoed `rev=`; no fixture-set digest is printed, so a copied verdict line cannot be distinguished
  from a real run by bytes alone. Routed item 3 (round 55).
- **INFO** — `corpus/lessons/round-53-verifier-spotcheck.md:59-60`: the "evidence-verified only" qualification is
  now answered for both counters and the runway gate; the gap the `considerthese` item targeted is closed with no
  divergence found.

# Mo57Executor45 — round-57 C1 arm: the exact capability-table defect and a falsifiable correction

Arm: C1 (calibration / capability register). No production edit, no commit, no jj mutation. All fixtures
lived under `$HYAKU_SCRATCH/mori-r57/Mo57Executor45/`; the lane repo was read only through
`git -C /home/vgpnk/Projects/shokunin/mori-shokunin show|cat-file|log`.

## 1. Frozen counter on the entering revision (exact output)

Entering revision `53e2b4768af93dd2472eb26ecc9b9fdca2e9daf2`; freeze landed `618562c7`. Lane tip read-only.

```
$ cd /home/vgpnk/Projects/shokunin/mori-shokunin
$ python3 .ufo/waves/round-57/count-c1.py 53e2b4768af93dd2472eb26ecc9b9fdca2e9daf2
C1=unmet rows=0 evidence=bad rev=53e2b4768af93dd2472eb26ecc9b9fdca2e9daf2
EXIT=1

$ python3 .ufo/waves/round-57/count-c2.py 53e2b4768af93dd2472eb26ecc9b9fdca2e9daf2
C2=unmet claims=0 source=bad rev=53e2b4768af93dd2472eb26ecc9b9fdca2e9daf2
EXIT=1
```

Both agree with the frozen pre-data control `.ufo/waves/round-57/controls.txt`. C2 is out of this arm's
scope beyond this receipt.

## 2. The routed round-56 defect, exactly

**Statement.** Mori round 56 was admitted with two capabilities; the lane's capabilities register holds
neither of them. The register is the `capabilities` field of the SCORECARD contract, and the file itself
declares one section to be that register.

Evidence, each item re-read at `53e2b47`:

| # | Fact | Exact location |
|---|---|---|
| 1 | Fleet record: `rounds[832]` = lane `mori`, `lane_round 56`, `admitted: true`, `verdict: admitted`, `verdicts {coverage: improved, operability: improved}`, `capabilities_added[0] = "dual-shape seat-output vote binding (tools/mori-vote-bind.py, 16/16 selftest, r55 tally re-bound 78/78 while the frozen r55 counter reads voted=0 on the same bytes)"`, `capabilities_added[1] = "strict per-event driver-liveness probe over .ufo/watchdog.log (tools/mori-driver-liveness.py, 13/13 selftest, live receipt 1728 log lines / 0 malformed / 23 lanes)"` | `/home/vgpnk/Projects/shokunin/MANIFEST.json` `rounds[832]` |
| 2 | The register's own contract: one row per capability an admitted non-author closure recorded, keyed `rounds[i].capabilities_added[j]`, first-working round = the closure's round | `SCORECARD.md:1953-1956` at `53e2b47` |
| 3 | The register table: heading `## Capabilities` at line 1951, header at 1969, **18 rows, lines 1971–1988, last key `rounds[495].capabilities_added[1]`**. No row names `driver-liveness` or `vote-binding`; the only occurrences of those tokens outside the round-56 prose are the round-56 claim rows at `SCORECARD.md:2903-2904`, which are a claim table, not the register | `SCORECARD.md:1951,1969,1971-1988,2897-2905` |
| 4 | The non-author round-56 spot-check already routed exactly this, by name | `corpus/lessons/round-56-verifier-spotcheck.md:86`: "**Capability row not entered.** C2 was declared a capability acquisition and demonstrably runs … but no row entered the SCORECARD capabilities table (round-56 section records axes only). Fix: enter the vote-binding capability (and the driver-liveness probe, if claimed as capability) per AXES.md §Capabilities." |
| 5 | The rule the fix cites: rows enter only through a round that demonstrates the capability running | `/home/vgpnk/Projects/shokunin/AXES.md:57-64` |

**The gap is larger than two rows.** Counting admitted mori closures with non-empty `capabilities_added`
against the register: 18 rows exist for `rounds[313] … rounds[495]` (rounds 12–31), and **23 rows are
missing** for every admitted closure after `rounds[495]`:

```
rounds[549][0] r36   rounds[554][0..1] r37   rounds[564][0..2] r38   rounds[570][0..2] r39
rounds[604][0..2] r41  rounds[628][0..3] r43  rounds[714][0..1] r48   rounds[723][0..1] r49
rounds[798][0] r53   rounds[832][0..1] r56
```

(Excluded correctly by the register's own rule: `rounds[372]` round 17, admitted false, 3 rows;
`rounds[585]` round 40, admitted false, 2 rows.) So the register was last brought up to date at its
round-35 measurement point and has not been maintained for 21 admitted rounds; round 57's frozen C1 targets
the most recent 2 of those 23.

`git show <rev>:SCORECARD.md | grep -c 'rounds\[832\]'` = 0 at `5b295eee`, `3f494b49`, `097c342b` and
`eac193ca`, so the register never held the row at any round-56 revision — this is an omission, not a lost
edit.

## 3. Why the frozen C1 counter cannot score the honest fix (primary finding)

`.ufo/waves/round-57/count-c1.py` is 14 lines. Its window is the **first** occurrence of the literal
`## Capabilities`, not the register:

```python
 2  """Round 57 C1 counter: verify the two round-56 capabilities are recorded."""
10  s = p.stdout.split("## Capabilities", 1)[1].split("## Saturation", 1)[0]
11  rows = [line for line in s.splitlines() if line.startswith("|") and ("driver-liveness" in line or "vote-binding" in line)]
12  ok = len(rows) == 2 and all(".ufo/waves/round-56/" in x and "| 56 |" in x for x in rows)
```

`split(..., 1)[1]` starts at the first `## Capabilities`, which is `SCORECARD.md:596`; the first
`## Saturation` after it is `:604`, so **the counter's entire universe is lines 596–603**, i.e. this stub:

```
596|## Capabilities
597|
598|| Capability | What it can now do | Evidence pointer | First-working round |
599||---|---|---|---|
600|| — none yet — | | | |
```

and `SCORECARD.md:1958-1960` says of that very table: "As the current self-assessment this register
supersedes the `— none yet —` table in the first `## Capabilities` section (left as filed at `d677cf3`)".
The counter binds the section the document disowns and is blind to the section the document declares
current. The counter therefore reports `rows=0` for both "no rows anywhere" and "the correct two rows in
the register" — the failure output is non-diagnostic.

Measured, in a `--shared` scratch clone of the lane repo at `53e2b47` (fixtures only; the frozen counter
copy differed from the frozen file only in its `repo =` path):

| fixture (scratch clone, one commit each) | frozen `count-c1.py` | corrected counter (§4) |
|---|---|---|
| base `53e2b476` (entering tip) | `C1=unmet rows=0 evidence=bad`, rc 1 | `C1=unmet rows=0`, rc 1 |
| `fixA` `04c005b0` — the two rows appended to the register after line 1988, real evidence paths `.ufo/waves/round-56/evidence/selftest-c1-counter.txt` and `tally-r55.txt`, `| 56 |` cell | **`C1=unmet rows=0`, rc 1** | `C1=met rows=2 evidence=ok`, rc 0 |
| `dangE` `15725973` — same rows, evidence pointers under `.ufo/waves/round-56/` that do not exist | `C1=unmet rows=0`, rc 1 | `C1=unmet rows=2 evidence=bad`, rc 1 |
| `stubB` `039a6cce` — the identical two rows written into the superseded stub at line 600 | **`C1=met rows=2 evidence=ok`, rc 0** | `C1=unmet rows=0`, rc 1 |
| `threeC` `0f034f9d` — the two correct register rows plus one further row that only mentions the token | `C1=unmet rows=0`, rc 1 | `C1=unmet rows=3`, rc 1 |
| `c31132ae` (clone2) — every `## Capabilities` token renamed | `IndexError` traceback, no `C1=` line, rc 1 | `C1=unmet rows=0`, rc 1 |

Four separable defects, each demonstrated above:

1. **Wrong section (blocking).** The verdict depends on which of the three `## Capabilities` sections
   (lines 596, 637, 1951) holds the rows, and it rewards the superseded one. A correct remediation is
   scored unmet; only a wrong one (writing rows into a table the file declares obsolete) is scored met.
2. **"Resolvable evidence" is not implemented.** `:12` substring-checks `.ufo/waves/round-56/`; `dangE`
   passes it with two non-existent paths, so `evidence=ok` is a lie in that case. The frozen predicate
   (`contract.md:5`) says "resolvable round-56 evidence pointer".
3. **Exact equality `len(rows) == 2`.** Any third row that merely mentions a token flips C1 red
   retroactively (`threeC`). Because the register is the same table that must record round 57's own
   capabilities, this arm is self-poisoning: the row a future round adds can un-meet round 57's C1.
4. **Text-substring window, no structure.** Splitting on a heading token also matches the *inline* mention
   `` `## Capabilities` `` in prose at `SCORECARD.md:1958`; when a real heading is absent the window
   silently becomes the rest of the file, and when no occurrence exists the counter dies with
   `IndexError` and emits no `C1=` line for the gate to read.

Contributing process fact: `.ufo/waves/round-57/count-c1.py:2` is a one-line docstring, so the counter
carries no predicate — unlike round 56's contract, which required "Predicate P-C1 is the exact counter
docstring in `count-c1.py`" (`.ufo/waves/round-56/contract.md:19`). The window mismatch was therefore
not visible at freeze time.

## 4. Recommended correction (falsifiable, evidence-backed)

**4a. Content.** Append exactly these two rows to the register at `SCORECARD.md:1989` (immediately after
the last row, `rounds[495].capabilities_added[1]`), preserving the register's 5-column layout:

```
| `rounds[832].capabilities_added[1]` | driver-liveness probe | Parses the hyaku driver's .ufo/watchdog.log launch/complete/dead/wrap/fail lines into one record per event and per-lane log-shape facts; 13/13 selftest, frozen fixtures at their frozen malformed counts; log shape, not process liveness. | `tools/mori-driver-liveness.py`; `.ufo/waves/round-56/evidence/selftest-c1-counter.txt` | 56 |
| `rounds[832].capabilities_added[0]` | vote-binding dual-shape binder | Binds seat votes from plain-text lines and JSON string scalars and re-tallies the committed round-55 RECHECK ledger 78/78 (bound voters 15/16) where the frozen r55 counter reads voted=0; 16/16 selftest. | `tools/mori-vote-bind.py`; `.ufo/waves/round-56/evidence/tally-r55.txt` | 56 |
```

Both cited paths exist at `53e2b47` (`tools/mori-driver-liveness.py`, `tools/mori-vote-bind.py`,
`.ufo/waves/round-56/evidence/selftest-c1-counter.txt`, `tally-r55.txt` — `ls` and `git cat-file -e`
verified), and both capabilities are the ones `rounds[832]` names. This is exactly `fixA`, measured met by
the corrected counter.

**4b. Counter — replace the selection and add the missing arms.** Minimum patch, reusing the lane's own
prior art (`.ufo/waves/round-35/count-c1.py:65-88`, which already binds `cap[-1]`, the last section):

```python
lines = p.stdout.splitlines()
starts = [i for i, l in enumerate(lines) if l.startswith("## ")]
cap = [i for i in starts if lines[i].startswith("## Capabilities")]
if not cap:
    print(f"C1=unmet rows=0 evidence=bad rev={R}"); raise SystemExit(1)
s = cap[-1]; nxt = [i for i in starts if i > s]
e = nxt[0] if nxt else len(lines)
rows = [l for l in lines[s+1:e] if l.startswith("|")
        and ("driver-liveness" in l or "vote-binding" in l)]
def resolves(row):                       # verdict cell 4; evidence paths must exist at R
    cells = [c.strip() for c in row.strip().strip("|").split("|")]
    ev = cells[3]
    toks = [t for t in re.findall(r"`([^`]+)`", ev) if t.startswith((".ufo/", "tools/", "corpus/"))]
    return bool(toks) and all(subprocess.run(["git","-C",repo,"cat-file","-e",f"{R}:{t}"],
                                             capture_output=True).returncode == 0 for t in toks)
ok = len(rows) == 2 and all(".ufo/waves/round-56/" in r and "| 56 |" in r and resolves(r) for r in rows)
```

with the predicate sentence moved into the docstring so the implementation cannot drift from it again.

**Falsification matrix the corrected counter must satisfy** (all rows measured, §3 table):
red at `53e2b47` (`rows=0`), **green at `fixA`** (`rows=2 evidence=ok`, rc 0), red at `dangE`
(`evidence=bad`), **red at `stubB`** (writing to the disowned section must not count), red at `threeC`.
A correction is falsified if any of those five flips.

**4c. Blast radius — do not misread the round-35 instrument.** `.ufo/waves/round-35/count-c1.py` pins
`MANIFEST_REV = 37b51a24` (`.ufo/waves/round-35/count-c1.py:31`) and derives an 18-row oracle from that closure. Measured:

```
at 53e2b47 (entering tip):  oracle=18 rows=18 matched=18 missing=0 bad=0 extra=0 mismatches=0 C1=met  rc 0
at fixA  (04c005b0):        oracle=18 rows=20 matched=18 missing=0 bad=0 extra=2 mismatches=2 C1=unmet rc 1
```

So landing §4a flips round-35's counter from met to `unmet extra=2` at the new tip. That is the expected
consequence of its frozen MANIFEST pin, not a regression and not evidence against the fix: the round-35
receipt is a historical measurement at its own revision, while a live register gate must re-derive the
oracle from the fleet MANIFEST at the measured fleet revision.

## 5. Risks, limits, non-claims

- **Scope.** The frozen C1 asks for 2 rows; the register's own contract asks for 23 (§2). I recommend
  landing the 2 (falsifiable now, evidence verified) and routing the other 21 as a separate repair —
  appending them quietly inside a round that claims only 2 would be the same defect at larger scale.
  A 23-row backfill is feasible but not mechanical: only 5 of the 23 `capabilities_added` strings name a
  path that resolves at the tip, 17 have a `.ufo/waves/round-<N>/` counter or report that resolves, and 6
  need an evidence pointer selected by hand.
- **Structure.** `AXES.md:60-64` says the SCORECARD carries *a* `capabilities:` table (singular); this
  file carries three `## Capabilities` sections plus per-round demonstration tables. Collapsing them is a
  document change outside every frozen predicate; recorded here as the root cause of §3.1, not proposed
  as part of the C1 fix.
- **Not measured.** Whether the round-56 capabilities still demonstrate at the entering tip (that is
  round 56's C1/C2 counters, out of arm scope); the fate of C2 in this wave; anything about host state.
- **No claim** about axis scores, verdicts or the other seats' findings. `unclosed`/C2 material was not
  touched.

## 6. Scratch and cleanup

Work `$HYAKU_SCRATCH/mori-r57/Mo57Executor45/` (default `/fast/scratch/hyaku/mori-r57/Mo57Executor45/`),
`TMPDIR` set inside it; disk guard checked first (`use% 27`, `/fast/scratch/hyaku`). Two `--shared` clones
(one worktree budget + one throwaway for the heading-absent fixture), both deleted before yielding; kept
only the small text receipts: `scorecard-53e2b47.md`, `evidence/c1-window-matrix.txt`, `counter-scratch.py`,
`counter-fixed.py`, `mkfix.py`. No tool installed or updated. No `/tmp` artifact cited. No secrets, no
private URLs. Nothing written outside this report and that scratch tree.

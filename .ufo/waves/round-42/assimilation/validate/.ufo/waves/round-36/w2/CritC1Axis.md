# CritC1Axis — round 36, wave 2, attempt 2

Attacks: C1's exploratory freshness-technique declaration, its before-state provenance, and any inference from P-C1's byte receipt to freshness admission. This is a scoped critic review, not native judgment, admission, or an outside-reviewer attestation.

Observation-time command: `date -u +%FT%TZ` → `2026-10-23T18:56:35Z`.

Paths are lane-relative unless marked `canonical:` (`/home/vgpnk/Projects/kimi-shokunin/skills/shokunin/protocol/`) or `fleet:` (`/home/vgpnk/Projects/shokunin/`). `r36/` below abbreviates `.ufo/waves/round-36/`; `r32/` abbreviates `.ufo/waves/round-32/`.

## Axes and independent conclusion

- **Freshness:** re-verification of skill claims against live surfaces, not equality between two representations (`canonical:AXES.md:14`).
- **Calibration / discernment:** accurately separating byte evidence, an exploratory technique improvement, and an independently verified claim (`canonical:AXES.md:15,43-55`; `canonical:LEARNING.md:40-50`).
- **Operability:** the new runnable sweep is a real operation; that fact does not transfer C2's measured axis verdict to C1.

**C1's honest disposition remains `unprovable`, not admitted freshness and not self-awarded `unprovable-but-better`.** The axis-fit limitation is real and remains in the classifier. The exploratory declaration contains that limitation honestly. However, I found a separate, fixable provenance defect in the description of the prior technique: `corpus/README.md:565` says the prior state had “only per-round manual sha re-checks” and cites an unrelated append-only audit, although round 32 already programmatically re-fetched source URLs. The report's FAIL below is for that description, not for retaining an explicitly exploratory probe.

## 1. Axis-fit counterexample remains real, but is disclosed

The strongest local witness is still S156:

- `corpus/evidence/sources-r30/S156.txt:1-20` contains provenance headers, source line-number prefixes, and a jump from source line 28 to 106. Its header records the full source-body digest, not the excerpt-file digest.
- `tools/mori-source-drift.py:148-154` hashes the entire copy and then tests whether the edge-stripped entire copy is a contiguous substring. It does not remove annotations, reconstruct noncontiguous excerpts, or examine the row's taught claim. Thus the original representation defect has not been repaired by the new implementation.
- Existing evidence `r36/w1/CritAxisFit.md:18-44` establishes an unchanged source body while the excerpt is classified drifted. I read that evidence and the actual copy/classifier; I did not repeat the known live-hash check.

The prior critic's actual commands and observed outputs, **secondary evidence, not executions by this seat**:

```text
timeout 45s curl --fail --location --silent --show-error --max-time 30 https://raw.githubusercontent.com/systemd/systemd/v262/src/shared/bus-print-properties.c | timeout 45s sha256sum
b56aa781be9c29b610156925030d3c4ab720c0ad73d57907d230ca3047302f2a  -

timeout 10s sha256sum corpus/evidence/sources-r30/S156.txt
4c02999410622d782979d025a9a61314104873cba9c19e4857feba4bd0473b5e  corpus/evidence/sources-r30/S156.txt

timeout 10s git show 6bd57097:corpus/evidence/sources-r30/S156.txt | timeout 10s sha256sum
4c02999410622d782979d025a9a61314104873cba9c19e4857feba4bd0473b5e  -
```

The first digest equals `S156.txt:3` and the original Gate (`corpus/lessons/round-30.md:114`). Existing full-tool evidence comes from the recorded command `python3 tools/mori-source-drift.py --root .` (`corpus/knowledge/source-drift-r36.md:21-23`); its observed file `r36/evidence/drift-live-r36.txt:156,221` contains:

```text
S156 drifted
MORI_SOURCE_DRIFT rows=220 fresh=49 excerpt=0 drifted=9 unavailable=0 no-copy=162
```

[INFERENCE] Neither a correct byte implementation nor agreement with a byte oracle establishes changed source content or stale taught claims. `count-c1.py:630-637` nevertheless permits this representation-only drift to satisfy its required drifted witness. That remains an axis-fit limitation, not an implementation violation of P-C1.

The current documents do not hide it: `r36/contract.md:120-130`, `tools/mori-source-drift.py:25-28`, `SKILL.md:858-863`, and `corpus/knowledge/source-drift-r36.md:16-40` distinguish representation drift from claim freshness and retain a manual claim-vs-source recheck. This is the safe treatment; changing the frozen classifier after data would not retroactively establish freshness.

## 2. `unprovable` is honest; an in-round reviewer is not the missing outside judgment

`canonical:AXES.md:43-51` requires a named non-author judgment with reasons for `unprovable-but-better`, explicitly says “a dispatched subagent does not count,” and requires `unprovable` plus honest stop without that judgment. `canonical:LEARNING.md:42-50` likewise says a subagent the lane dispatched is still the lane. This critic report cannot supply the missing outside judgment.

The assignment identifies no qualifying outside reviewer; the inspected C1 records do not supply one. `r36/contract.md:128-129` explicitly retains the conditional reviewer requirement. The round-36 dispatch source directs the SCORECARD draft to record C1 as “unprovable pending named non-author reviewer,” with the byte receipt only as evidence (`r36/gen-w2-spec.py:518-523`). That is a draft instruction, not an already-landed verdict or an outside attestation.

The exploratory declaration really precedes the data commit in ancestry. Executed, lane cwd:

```text
$ git rev-list --ancestry-path --parents 6bd57097..bf0df77fee4b6ef54a90aea09335c7617f125151
bf0df77fee4b6ef54a90aea09335c7617f125151 5842dc045bb3d3b7aa2bdaaf462dcff536358444
5842dc045bb3d3b7aa2bdaaf462dcff536358444 c1a026cb156c5fe84d76dc79190f1885ad11abf4
c1a026cb156c5fe84d76dc79190f1885ad11abf4 da12b3786f88626a26c951fab6b716bef6b8498e
da12b3786f88626a26c951fab6b716bef6b8498e c081375376b00f81c49e6c52b0e4a4338a4ecc84
c081375376b00f81c49e6c52b0e4a4338a4ecc84 6bd57097f7ab2b471b4593ed2019c980b1368c68
```

Executed `git show 5842dc045bb3d3b7aa2bdaaf462dcff536358444:.ufo/waves/round-36/contract.md`. The output's final declaration already says:

> It verifies only as `unprovable-but-better` with a named non-author reviewer; otherwise it lands `unprovable`. P-C1 is still run and reported as evidence of the probe's byte behaviour, not as C1's verdict.

The same output still has the original claims-table wording “flags stale source rows.” The specific exploratory declaration expressly disclaims that reading; the current worktree table now also makes the byte-only limit explicit (`r36/contract.md:13`). A closure reading only the historical table would discard a pre-data qualification, not discover a valid freshness admission.

## 3. Fixable defect: the manual-only baseline and its provenance are wrong

**Counterexample to the historical baseline, not to the narrower new sweep:** `corpus/README.md:565` describes the prior state as “previously only per-round manual sha re-checks, `w1/ReviewDebtList.md`.” But:

1. `r32/count-c1.py:116-120` already invokes `curl` programmatically; `:166-172` makes live checking the default unless `--no-live` is supplied; `:239-255` checks the committed copy digest and re-fetches the population URL to check quoted passages; `:261-265` re-fetches rows marked unreachable.
2. The existing executed receipt uses no `--no-live`. Receipt command and observed output (`r32/evidence/c1-after.txt:1-9`; **read, not rerun here**):

```text
$ python3 .ufo/waves/round-32/count-c1.py 7766732a98795467d0541630e9707a7acba518e1
revision=7766732a98795467d0541630e9707a7acba518e1 base=641a6e86ecc60634d215c0a47ab86c47661abf86 population=34 pop_sha256=4426b6501a01c07b
recheck_rows=34 header_ok=True section_sha256=251bf664717bbdf4 judge_ok=True judge_seat_ok=True judge_agree=34
rows_ok=34/34 verdicts={'current': 33, 'unreachable': 1}
row_failures=none
new_ok=3 new_failures=none
C1=met exit=0
exit=0
2026-10-23T01:57:15Z
```

3. Its code predates the round's entering base. Executed, lane cwd:

```text
$ git log --format='%H %aI %s' -1 6bd57097 -- .ufo/waves/round-32/count-c1.py
29f7d04355f17b5d45d6e00c40e2a5c3e5a2c9c4 2026-10-22T21:38:56-03:00 round-32: C1 freeze — contract, population, counter, before receipt
```

4. The cited `r36/w1/ReviewDebtList.md:3-8,45-51,87-110` is an audit of immutable SOURCES-cell changes, superseders, and deletion history. It does not substantiate a manual-only freshness baseline or the first-use claim.

This does **not** show that round 32 supplied the same reusable all-`sources-r<N>` copy sweep. C1 still adds that operation: the new tool's loop fetches each readable copy selected by the declared convention (`tools/mori-source-drift.py:72-96,159-197`). Prior population-specific live checks and this general classifier can both exist. The improvement is credible at that bounded technique level; “no prior programmatic source re-fetching” is not.

The copy convention also matters to modest wording: `corpus/evidence/recheck-r32/` contains saved bodies including `S001.src`, but the new tool searches only `sources-r<N>` and the saved round-36 output calls S001 `no-copy` (`r36/evidence/drift-live-r36.txt:1`). This is consistent with the frozen interface, not a request to expand the tool. “Every copied row” must mean every row with a readable copy in that declared inventory, not every historical evidence snapshot.

**Impacted axes:** calibration/provenance in the explanation of the before-state; freshness-technique novelty if it is inflated into the first programmatic source refetch of any kind. No runtime regression, stale taught claim, or axis harm from the probe itself is demonstrated here.

**Smallest safe correction:** outside the frozen predicates/receipts, append an explicit correction that earlier population-specific programmatic live quote rechecks existed, cite the round-32 code and receipt, and bound C1's novelty to the reusable byte classifier over the declared `sources-r<N>` inventory. Remove the unrelated append-only audit as support for the manual-only baseline. Preserve the original exploratory declaration and `unprovable` disposition. No remediation performed by this seat.

## 4. Admission-confusion paths examined

| Possible path | Evidence and result |
|---|---|
| Read `C1=met` or counter exit 0 as claim verification | `r36/count-c1.py:630-631,713-716` computes success only from byte-arm results. It never consults a reviewer or verifies the semantic freshness axis. The raw receipt therefore cannot authorize admission. |
| Read the successful after receipt without its declaration | The receipt says P-C1, then `C1=met` and `C1_EXIT=0` (`r36/evidence/c1-after.txt:1-6`). The pre-data declaration explicitly narrows those labels. Preserve both facts together in a closure rather than rewriting the frozen receipt. |
| Treat the old claims-table sentence as the current complete claim | The historical table has the old stale-row wording; its pre-data final declaration disclaims that inference. The current table independently carries the disclaimer (`r36/contract.md:13`). |
| Use a wave-2 reviewer or this critic as the named non-author | Excluded by `canonical:AXES.md:47-50` and `canonical:LEARNING.md:42-50`, regardless of the seat's independent reasoning or dispatch transport. |
| Dispatch/corpus text quietly promotes the receipt | The executable dispatch source says “NOT a freshness admission” (`r36/gen-w2-spec.py:87-92`) and requests `unprovable` in the draft (`:518-523`). `corpus/README.md:579-581` likewise says no freshness verdict is claimed. `SKILL.md:874` registers a **probe**, explicitly warning that exit 0 can include unavailable/no-copy rows. No actual promotion found on these inspected surfaces. |

L1's receipt command supplied in the assignment is `python3 .ufo/waves/round-36/count-c1.py bf0df77fee4b6ef54a90aea09335c7617f125151`. The observed existing receipt, **not a run by this seat**, is:

```text
blind_rows=40 tool_exit=1 tool_rows=40 mismatches=0
real_rows=220 oracle_fetched=58 oracle_fresh=49 oracle_drifted=9 oracle_excluded=0 tool_exit=1 tool_rows=220 mismatches=0
C1=met
seed=7388485190103051243
C1_EXIT=0
```

[INFERENCE] A generic success-to-admission consumer would be unsound here. I did not establish that such a consumer has admitted C1. A scoped `glob` of `fleet:.ufo/reports/round-36/*` returned `kake.md`, `kumitate.md`, and `kotodama.md`, not a mori final report; the lane report directory likewise has no round-36 report. I did not inspect the prohibited fleet MANIFEST/state/scripts, invoke a closure checker, or claim the absence of every possible future closure path. The safe handoff is explicit: **P-C1 byte evidence met; C1 exploratory claim unprovable; qualifying outside reviewer absent; no freshness admission follows.**

## Methods and containment

Static file/line review, directory/glob/search tools, and read-only Git object/history inspection only. Existing receipts are attributed above, not re-measured. The additional executed history listing `git log --format='%H %aI %s' -12 -- .ufo/waves/round-36/contract.md tools/mori-source-drift.py .ufo/waves/round-36/evidence/c1-after.txt` returned, in order:

```text
bf0df77fee4b6ef54a90aea09335c7617f125151 2026-10-23T09:09:14-03:00 round-36: C1/C2 data — drift probe tool, append-only gate + index-clean tools, SOURCES S205-S220, QUALITY 103-105, SKILL rows, wave-1 evidence, attempt-2 log
5842dc045bb3d3b7aa2bdaaf462dcff536358444 2026-10-23T09:09:14-03:00 round-36: C1 declared exploratory before data (axis-fit defect found by wave-1 critic); C2 stays measured
c1a026cb156c5fe84d76dc79190f1885ad11abf4 2026-10-23T09:03:04-03:00 round-36: C0 control receipts (K9/J11/K13 met v1), counters re-designed before data (v2), 25/25 controls unmet under v2
da12b3786f88626a26c951fab6b716bef6b8498e 2026-10-23T06:51:59-03:00 round-36: freeze C1/C2 contract and counters (P-C1 source drift, P-C2 append-only gate), before receipts
```

No tool/counter/self-test/build/linter/native judge or alternate runtime was invoked. No network probe was repeated. No subagents were dispatched. No installs or updates. Only this report was written; no scratch output was created. Current worktree documentation was moving during the review; revision-bound declaration evidence is identified separately above. The integration owner, not this seat, owns final closure and checking the eventual SCORECARD/report wording.

Report: .ufo/waves/round-36/w2/CritC1Axis.md

VERDICT: FAIL — C1 honestly remains unprovable, but the manual-only before-state and its supporting citation are defective (`corpus/README.md:565`; counterevidence `r32/count-c1.py:116-120,166-172,239-255` and `r32/evidence/c1-after.txt:1-7`).

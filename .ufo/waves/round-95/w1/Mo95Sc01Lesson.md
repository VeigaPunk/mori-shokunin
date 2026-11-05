# Round 95 — mori lesson

Entering `754f4991198c16ddd1d4a3ea9206cfb7d74d6827`.
Freeze `2dc476d7fdb68bf916685a9f217a92047662baeb` (contract, counters, before receipts).
Attempt 1, wave w1. Draft by Mo95Sc01Lesson; integration and non-author closure remain separate acts.
Axes: calibration, operability, depth, freshness, coverage, adjacency. No score movement is asserted here.

## Claims and verdicts

### C1 — calibration

Frozen predicate, copied from `.ufo/waves/round-95/contract.md:22-25`:

> Predicate P-C1r95 (same sentence in `count-c1.py` docstring and the receipt): running
> `python3 -I .ufo/waves/round-95/count-c1.py <rev> --lane <lane> --census <census>` prints `C1=met survivors=0 killed=7/7`
> and exits 0 iff the pristine counter (sha256 `6eb7fa4c…`, round-94 `count-c1v2.py`) is green on BASE, every pristine fixture
> has its declared verdict, and every one of the seven mutants m1, m1b, m2, m3, m4, m6, m7 is killed by at least one fixture.

Recorded before and after: `.ufo/waves/round-95/evidence/before-c1-r95.txt:1-20` contains BOTH battery subsets' results, not just a pre-amendment result. Round-94-only survivors = **4**, IDs **m2,m3,m4,m6**; augmented-battery survivors = **0**, killed = **7/7**, pristine = **green**, crash IDs = **none**, exit **0**. Lines 4–7 name the new kills: m2 by R95-LEN, m3 by R95-CEN, m4 by R95-TRIO, m6 by R95-PAT. Lines 9–15 give the seven expected pristine negative verdicts. This is a reading of the committed receipt, not a scribe replay or landing-hash receipt.

Named limits (`contract.md:30-37`): do-nothing leaves four survivors; m5 is declared equivalent and is not scored (`adm_ok + adm_fail = 19` on reachable inputs); a kill requires divergence from pristine, with no `C1=` output treated as a crash/kill, never pass; the pristine counter is not amended and any residual survivor must be reported rather than patched into the frozen battery. Coverage is the seven enumerated non-equivalent mutants and specified fixtures, not arbitrary counter defects. The fixtures intentionally incorporate the round-94 probe's proposed separating cases; this is not a blind nonce guard.

Verdict: pending non-author closure.

### C2 — operability capability

Frozen predicate, copied from `.ufo/waves/round-95/contract.md:46-51`:

> Predicate P-C2r95 (same sentence in `count-c2.sh` header and the receipt): running
> `bash .ufo/waves/round-95/count-c2.sh <rev> <lane> <fleet>` prints `HOSTINDEP hidden=1 before=C1=unmet(...) after=C1=met(rc=0)
> control_outside=C1=met(rc=0)` and exits 0 iff, inside `unshare -rm` with the account home replaced by an empty tmpfs:
> (a) the census path under the home directory is absent (`hidden=1`), (b) the round-93 counter prints `C1=unmet` or exits
> non-zero, and (c) the round-94 counter with `--census` on a copied census prints `C1=met` with rc 0; and (d) the round-93
> counter run outside the namespace prints `C1=met` rc 0 (positive control: the namespace is the cause).

Recorded before and after: `.ufo/waves/round-95/evidence/before-c2-r95.txt:1,6` reads `HOSTINDEP hidden=1 before=C1=unmet(rc=1) after=C1=met(rc=0) control_outside=C1=met(rc=0) census_sha=3fb7261569f4 rev=754f4991198c`, outer exit **0**. Both artifacts pre-exist this round. The before is the round-93 counter, not absence of the round-94 file. The positive control distinguishes home hiding from an already-failing before. This is committed-receipt evidence, not scribe execution of the namespace experiment.

Named limits (`contract.md:53-59`): do-nothing is the round-93 counter in the namespace; capability name is `host-independent counting namespace`, first-working round 95, conditional on a passing run this round. The namespace hides only the account home; it does not establish freedom from host literals elsewhere. User-namespace availability remains host configuration; no sysctl is changed. This is a capability acquisition, not an asserted operability score increase or repair of frozen round-93 history.

Verdict: pending non-author closure.

## Mistakes

Source of mined mistakes: `corpus/lessons/round-94.md:32-37`. Paths below are lane-relative unless an absolute fleet-root path is explicitly given. The three principal carried classes are:

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| `successor-as-before` — round-94 C2 counted absence as the before | `.ufo/waves/round-94/w1/Mo94K01Crit.md:63-70,93-98`; `.ufo/waves/round-94/evidence/entering-c2-r94.txt:7-9` (`files_r94=0`) | round-94 critic K01 after the freeze; non-author round-94 spot-check | Taken this round: measure the pre-existing round-93 counter under home hiding, versus the pre-existing round-94 successor, with an outside positive control. Recorded result: `.ufo/waves/round-95/evidence/before-c2-r95.txt:1,6`. Capability framing retained; closure pending. |
| `control-battery-gap` — round-94 C1 leaves m2,m3,m4,m6 alive | `.ufo/waves/round-94/w1/Mo94M01Mut.md:39-43,55-82`; `corpus/lessons/round-94.md:37` | round-94 mutation-tester M01 | Taken for C1: freeze R95-LEN/CEN/TRIO/PAT before scoring. `.ufo/waves/round-95/evidence/before-c1-r95.txt:1,4-7` shows the rule able to fail on the old subset (four survivors) and records zero survivors with the augmented battery. Round-94 C2 mutation gaps are NOT closed by this C1 result. |
| `env-fail-open-missing-counter` — Python's missing-file rc 2 satisfies `env_unset=rc2` without the counter's setup path | `.ufo/waves/round-94/w1/Mo94K01Crit.md:69-73`; `corpus/lessons/round-94.md:36` | round-94 critic K01 | NOT fixed this round. Route to round 96: require the counter's `C1_SETUP` diagnostic, not rc 2 alone. Do not rewrite the frozen round-94 predicate. Local scribe probe below independently demonstrates rc 2 with zero `C1_SETUP` occurrences on a missing script. |

Other round-94 mistakes remain part of the record, not new round-95 fixes: marker durability (`corpus/lessons/round-94.md:32`), a proposed ignore rule hiding evidence (`:33`), and a tag-stripped quote spacing artifact (`:34`). The old markers were committed at the round-94 landing, the ignore patch was rejected, and the visible quote was corrected in that lesson. No fresh source-fetch or marker closure is claimed by this scribe.

## Routed defects

| item | disposition | reason and evidence |
|---|---|---|
| D1 planner binding | Routed, open, operator-owned | Disclosure that L1 holds the seat is not evidence of topology binding. `.ufo/waves/round-95/contract.md:11-12`; `.ufo/waves/round-94/w1/Mo94K02Crit.md:76-88`. No policy/validator mutation is within this wave seat's scope. |
| Sibling host-literal class | Routed to owning lanes/operator, not taken | Seven sibling lanes were reported with live host literals in round 94 (`corpus/lessons/round-94.md:48-50`; `.ufo/waves/round-94/w1/Mo94Conn01.md`). No sibling scan replay or sibling edit was performed here. |
| Digest debt P4 | Routed, not taken | Round-94 record carries 31 prefix-only rows and S125 unpinned (`corpus/lessons/round-94.md:51`). Scribe's read-only digest run still reports prefix_only=31 and S125 unpinned; it additionally reports S622/S623 unpinned under the historical pinned-directory argument. This run is not a closure of the debt; see audit appendix. |
| Round-90 nonce guard, QUALITY 191 | Routed, not taken | `corpus/QUALITY.md:2224-2230` requires author-unreadable guard inputs, rule-shape checking, or grade-time nonce generation. Enumerated mutant kills do not implement that separate guard. |
| `env_unset` fail-open | Routed to round 96, not taken | Round-95 predicates do not repair the round-94 rc-only environment arm. The local missing-script probe reproduces the counterexample. Draft criterion 207 records the requirement, not its implementation. |
| C1 mutation coverage amendment | Taken, measured in frozen receipt; closure pending | Seven enumerated non-equivalent mutants killed, pristine green; `.ufo/waves/round-95/evidence/before-c1-r95.txt:1-20`. |
| C2 successor-as-before routing | Taken as capability experiment; closure pending | Existing counters compared with the home absent and an outside control; `.ufo/waves/round-95/evidence/before-c2-r95.txt:1-6`. |

## Gate

C2's user-plus-mount namespace mechanism and its host-availability limit are the sourced claim planned for S626/S627 (`.ufo/waves/round-95/contract.md:63-67`). No source digest, quotation or admission decision is invented here.

| Row | Source | Gate evidence and decision |
|---|---|---|
| S626 | `unshare(1)` manual | [L1 fills from scout Mo95S01Src] |
| S627 | `user_namespaces(7)` manual | [L1 fills from scout Mo95S01Src] |

## Draft QUALITY.md criteria

These are proposed paste-ready additions, not edits to `corpus/QUALITY.md` and not newly passed gates.

205. A mutation battery's coverage claim names its non-equivalent mutant set, checks pristine live and fixture verdicts, and reports survivors rather than equating a live-green counter with exercised gates; equivalent mutants are declared separately. Ground: `.ufo/waves/round-94/w1/Mo94M01Mut.md:76-82`; `.ufo/waves/round-95/contract.md:22-37`; `.ufo/waves/round-95/count-c1.py:55-63,200-223`. Shown able to fail: the contract command `python3 -I .ufo/waves/round-95/count-c1.py <rev> --lane <lane> --census <census>` has committed observed output `before_r94_survivors=4 r94_survivor_ids=m2,m3,m4,m6` when scoring the round-94-only subset, alongside `survivors=0 killed=7/7 pristine=green` for the augmented set (`.ufo/waves/round-95/evidence/before-c1-r95.txt:1`, outer exit 0). The first subset fails the coverage requirement; the outer full battery did NOT exit nonzero. Receipt provenance only: the receipt does not preserve its exact invocation/revision, so this is not an independently reconstructed command execution.

206. An operability before must exercise a named pre-existing artifact under the challenged environment, not infer improvement from absence of a newly created successor; a capability acquisition is labelled as such and includes a positive control. Ground: `.ufo/waves/round-94/w1/Mo94K01Crit.md:63-68,93-98`; `.ufo/waves/round-95/contract.md:41-59`. Shown able to fail: critic K01's recorded command `env -u HOME TMPDIR=$S/tmp python3 -I $S/clone/.ufo/waves/round-94/count-c2v2.py 84b15230 --repo $S/clone --root $F` outputs `C2=unmet literal_r94=0 files_r94=0 frozen_r93=unchanged env_i=unmet env_unset=rc2 checks_failed=files,env_i`, rc 1 (`Mo94K01Crit.md:65-68`); the zero-file before fails the pre-existing-artifact requirement. This is a quoted prior-seat execution, not a scribe rerun; its scratch variables belong to that prior seat.

207. A fail-closed environment test must require the counter's own setup diagnostic as well as its expected exit status; a missing executable must fail that test even if the interpreter returns the same status. Ground: `.ufo/waves/round-94/w1/Mo94K01Crit.md:69-73`; `.ufo/waves/round-94/count-c1v2.py:126-145`; `corpus/QUALITY.md:2289-2296`. Shown able to fail: scribe command `env -u SHOKUNIN_ROOT python3 -I /fast/scratch/hyaku/mori-r95/Mo95Sc01Lesson/no-such-counter.py HEAD --repo /home/vgpnk/Projects/shokunin/mori-shokunin` outputs `python3: can't open file '/fast/scratch/hyaku/mori-r95/Mo95Sc01Lesson/no-such-counter.py': [Errno 2] No such file or directory`, rc 2, with `grep -c C1_SETUP` reporting 0 (grep rc 1). Thus rc-only passes while the diagnostic-aware criterion fails. The present-counter comparison outputs `C1_SETUP census path unset: give --census or set SHOKUNIN_ROOT`, rc 2. These local setup-only invocations omitted an explicit TMPDIR, contrary to the seat counter-invocation rule; they performed no fixture/tree construction because setup returned first. Do not treat them as compliant counter replay evidence.

---

## Scribe audit appendix — not an admission or closure

### Behavior, provenance, and touched surfaces

Only this report is a persistent seat-authored artifact. Scratch used `/fast/scratch/hyaku/mori-r95/Mo95Sc01Lesson`; scratch outputs are summarized below and removed before yielding. No product, corpus, QUALITY, SOURCES, contract, counter, evidence, fleet-root, sibling, judge or policy file was edited; no git mutation, commit, push, package install, mount, namespace launch or alternate runtime was performed by this seat.

The principal C1/C2 measurements above were read from frozen receipts, NOT rerun. The entry and freeze revisions were observed via `git rev-parse HEAD` / `git log --oneline -3`. `git show --stat --format='%H %s' 2dc476d7` lists exactly five frozen files: contract, two counters, and two before receipts. Read-only `git diff --stat 2dc476d7 --` on those five paths returned no output, exit 0; a read-only entering-to-freeze diff on round-93/94 artifacts also returned no output. These are byte-drift observations, not predicate execution evidence.

`sha256sum .ufo/waves/round-94/count-c1v2.py .ufo/waves/round-95/count-c1.py .ufo/waves/round-95/count-c2.sh` produced, respectively:

```
6eb7fa4cf0ecf86064bb2714a5b93b52bf3356dc6e38e5dc7ee51f7255a7b384
6c288d70c39a5736b6aba0b4a0525159010124c0b5494f047a10aab6dfeaa450
014980bc82b71b7a48764b45e7e550050e928956a32cd6e4ef3b4208aa844b9f
```

Exit 0. The pristine full digest matches the pin opened at `count-c1.py:38`.

### Pointer checks and findings

Existence checks used shell `ls` and `[ -e "$p" ]`; line checks used `sed -n` and numbered file reads. Confirmed the required three-class pointers, the round-94 lesson's six mistake classes, K01 sections 2c/2f, M01 gap summary, K02 sections 2/3, and the round-93 D3 record. Counter line probes `sed -n '39p;141p' .ufo/waves/round-93/count-c1.py`, `sed -n 39p .ufo/waves/round-93/count-c2.py`, and `sed -n 81p .ufo/waves/round-93/controls-r93.sh` return the cited host constants, substring admission test, and host-path replacement command. `grep -n '/home/vgpnk' .ufo/waves/round-93/count-c1.py` outputs its line-39 CENSUS constant (rc 0); `grep -c '/home/vgpnk' .ufo/waves/round-94/count-c1v2.py` outputs 0 (rc 1). These static observations do not prove general host independence.

Path-resolution finding: lane-relative `PROTOCOL.md`, `.ufo/l0-questions.md`, and `scripts/sources-census.sh` do not exist. They DO exist at fleet root `/home/vgpnk/Projects/shokunin/`. Similarly QUALITY is `corpus/QUALITY.md`, not lane-root `QUALITY.md`. The round-94 lesson's bare `PROTOCOL.md` and `.ufo/l0-questions.md` references are ambiguous if interpreted as lane-relative. Preserve explicit fleet-root attribution rather than copy a broken lane-relative pointer. The principal three mistake pointers in this draft resolve; no wrong numbered anchor was found in them.

`git status --porcelain -- .ufo/waves` at the read point listed six untracked entries: `round-95/evidence/census-before-r95.txt`, `w1-dispatch.json`, `w1-spec.json`, `w1.ready`, `w1.ready.dispatched`, and `w1/`. `git ls-files .ufo/waves/round-95` listed only the five freeze files. Therefore the census-before receipt was NOT part of freeze commit `2dc476d7`; don't present it as committed frozen evidence. Round-95 marker durability still requires integration; this is a pre-landing observation, not proof that final landing failed.

### Additional executed checks and limits

These extra read-only checks were performed by the scribe and must not be conflated with executor C1/C2 runs. They exceeded the narrow reporting-only role; none established claim closure.

1. From fleet root, `bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori > $S/census-now.txt 2>&1` returned rc 0, 43 W04 duplicate-URL warnings, ending `mori\tok\t/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md`. `grep -cP '\t[WE][0-9]{2}\t' $S/census-now.txt` output 43, rc 0. The frozen-adjacent census receipt's command `grep -c ' W0[0-9] \|E0[0-9] '` output 0, rc 1, on the same tab-delimited data. Its space-based count misses the warnings. The receipt also contains an unlabeled 43 and a W04 example. Report validator exit 0 separately from warning count 43; do NOT claim zero warnings. Warning-only exit 0 is expected by the validator's documented policy. No frozen-adjacent receipt was rewritten.

2. From lane root, `python3 -I tools/mori-source-digest.py corpus/SOURCES.md corpus/evidence > $S/digest.txt 2>&1` returned rc 1, `DIGEST_CHECK rows=124 ok=86 mismatch=0 superseded=1 prefix_only=31 unpinned=6`. This was an initially wrong pinned-directory choice; NOT canonical debt evidence.

3. After locating the historical invocation in `.ufo/waves/round-91/evidence/controls-r91.txt:18`, `python3 -I tools/mori-source-digest.py corpus/SOURCES.md .ufo/waves/round-90/w1/Mo90S01Sources/sources/ > $S/digest2.txt 2>&1` returned rc 1, `DIGEST_CHECK rows=124 ok=88 mismatch=0 superseded=2 prefix_only=31 unpinned=3`. Unpinned IDs: S125, S622, S623. This is conditional on that historical pinned directory; no global search for later copies or repair was done. The round-94 routed debt is at least still open; don't silently reduce this observation to unpinned=1.

4. From lane root, `env -u SHOKUNIN_ROOT python3 -I .ufo/waves/round-94/count-c1v2.py HEAD --repo "$PWD" > $S/a.txt 2>&1` returned rc 2 and the exact C1_SETUP line quoted in criterion 207. The missing-file invocation and its output are preserved in criterion 207. Neither is a passing environment gate or compliant full replay.

No tools were installed or updated. No scores, source-admission decisions, planner binding, sibling fixes, nonce implementation, env_unset repair, or round-95 landing receipts are asserted. The Gate placeholders and both pending verdicts are intentional required handoffs, not omitted sections.

Draft status: DRAFTED — all six requested sections are present. L1 must fill S626/S627 from Mo95S01Src and preserve non-author verdict ownership.

# Mo59Reviewer20 — frontier coverage check: C2 entry topic vs mori PROVINCE

Seat: reviewer, mori round-59 w1. Read-only; no production, registry, SCORECARD, LOG or VCS writes.
Freeze rev `60b3a76ad0524c8978cc51922940be1c8c388915`; entering rev `2b9f03975bfb6e508f35074ac8181ec8bf54e805`.
Working-tree HEAD moved twice during this check (jj live integration); all frozen-state assertions below were verified by direct byte/hash reads, not by HEAD position.

## Verdict: NO-COUNTEREXAMPLE — the C2 entry topic sits inside mori PROVINCE

The C2 entry topic — committed `.ufo/waves/round-5X` wave-results settlement artifacts and the
lane's own settlement summary — is explicitly owned ground. PROVINCE citations are against
freeze-rev bytes (PROVINCE.md wt sha256 `e1afa247f169…` == `60b3a76:PROVINCE.md`, byte-SAME):

- `PROVINCE.md:3-4` — Domain: "fleet & host observability (森) — whether the fleet, **its waves** and its host are alive and progressing."
- `PROVINCE.md:6-7` — Owns (read-only probes): "`.ufo/waves/*` settlement state (**registry + results pair**)" — exactly the dispatch/results pair the C2 artifacts belong to.
- `PROVINCE.md:23` — Core "Wave settlement — `SURFACE waves`: registry/dispatch/results presence and per-wave age…".
- `PROVINCE.md:145-152` — round-20 Core precedent: per-seat wave-settlement grading of the same artifacts (`tools/mori-wave-settlement.py`, `ufo-swarm-wave-dispatch-v1` files); the r59 entry deepens this same surface with byte-located shape facts, and its predecessor `corpus/knowledge/wave-settlement-r20.md` is present and committed (head: "# wave settlement r20 — per-seat report presence for dispatched swarm waves").
- `PROVINCE.md:46` — FR3 boundary line lives in the entry's favor: it asserts shape facts only ("They are shape facts of committed artifacts, **not settlement semantics** … nothing here proves a seat ran, judged, or agreed") and its coverage-map says "without advancing frontier", so FR3 (authoritative settlement) stays frontier as required.
- `PROVINCE.md:16,18` — "Detection and report only — never remediation" / "Out of province → report, never absorb": the r53 `report_file` drift is recorded, "not a K claim … its drift is *recorded*, not repaired", matching the contract's "reported not fixed".

No adjacent-domain bleed in substance: all six counter ARTIFACTS, the scan/drift targets, the pinned copies (`corpus/evidence/sources-r59/`) and the registry rows (S553–S559, present in `corpus/SOURCES.md`) are mori-lane paths; the entry quotes only mori's own wave artifacts plus its own `mori-wave-settlement-v1` summary (K12–K14, labeled own-work). Entry bytes at read time: sha256 `441a751de67f…`, 47 lines, 13 distinct claim IDs (K1–K10, K12–K14).

## Findings

**F1 (low, landed-entry text): coverage-map names the wrong frontier row.** Entry line 8: "Core — fleet wave-settlement artifacts (**FR5-adjacent** observability of the inline spawn handoff)". In mori PROVINCE, FR5 is "Watchdog daemon identity and degraded-pgrep visibility" (`PROVINCE.md:48`) — unrelated to wave settlement. The ground this entry deepens is the FR3 wave-settlement row (`PROVINCE.md:46`). The counter only requires the `coverage-map:` frontmatter key to exist, so this passes counting while mislabeling the frontier anchor. Recommend the entry (or its lesson) say FR3-adjacent — but any edit after freeze is the L1's call, not mine.

**F2 (low, wording): "observability of the inline spawn handoff" reaches toward refused ground.** The spawn handoff is orchestration mechanism — `PROVINCE.md:12` refuses "dispatch and orchestration mechanism (→ kumitate)"; `PROVINCE.md:65` gives kumitate "wave plan/run/record/collect semantics" while "mori passively grades `.ufo/waves/*` filesystem settlement state". The entry body stays on the correct side (shape facts of the artifact the handoff writes), but the coverage-map phrase reads as observing the mechanism itself. Artifact-scoped wording ("the artifact the inline spawn handoff writes") would remove the reading; the body already complies, so this is a wording flag, not a violation.

**F3 (informational, outside my axis): dangling K11 reference.** The Limits paragraph says "K11's absence claim is bounded to r54–r58 first members…", but no K11 claim row exists (claims are K1–K10, K12–K14). Counter-neutral (13 distinct IDs ≥ MIN_CLAIMS=10; no dup-K reason), but the internal reference points at nothing. Left to the scoring/counter seats.

**F4 (boundary-hold, no action): the scan arm's schema grading is the widest step.** Validating `seats==members`, member key-set and role enum grades committed-byte schema, one step beyond round-20's "filesystem shape only" (`PROVINCE.md:145-146`). It stays in-province precisely because it emits a structural verdict on committed bytes (`SETTLEMENT_SCAN_OK/FAIL`), reports the r53 drift without repairing it, and issues no orchestration/lifecycle verdict (`PROVINCE.md:119-120`: "authoritative wave-result semantics and emission stay frontier or kumitate-owned. No scan is an orchestration verdict."). Any future entry text that presents scan-OK as settlement or result acceptance would cross into kumitate's band; this entry does not.

## Method (bounded)

1. Read frozen contract + both counters; verified byte-identity vs freeze rev for all four (`PROVINCE.md` `e1afa247…`, `contract.md` `427fca0b…`, `count-c1.py` `2be6fda8…`, `count-c2.py` `2df3ae84…`, each wt == `git show 60b3a76:<path>`).
2. Entering-rev control re-derived: `git show 2b9f0397:corpus/knowledge/wave-settlement-artifacts-r59.md` and `:tools/mori-settlement-scan.py` both absent (contract's `failed=tool_absent` premise holds).
3. Read PROVINCE.md in full (476 lines incl. appended round notes); extracted exact line anchors by grep over wt bytes (byte-SAME with freeze).
4. Read the landed entry; checked every claim/copy path against the counter's ARTIFACTS map (all mori-internal; no other-lane material).
5. Spot-checked two claims byte-exactly: `corpus/evidence/sources-r59/w1-results-r54.json` sha256 `ea48a0cc07fa948c70d90103b589db0cdf7d48343aa689a3e56742c1cd59335f` == K1/K8 pin; line 2 ` "lane": "mori",`, line 5 ` "seats": 74,` — both quotes exact. (Spot check only; full pin verification is the counter seats' job.)
6. Disk guard: green (/fast/scratch/hyaku 27%, 592.6G free). Scratch `/fast/scratch/hyaku/mori-r59/Mo59Reviewer20/` created, used only for TMPDIR; cleaned before yield.

## Residual risk / verification gaps

- The working tree was actively mutating (HEAD `2317a3a…` → `7b86704d…` during the check; one transient read briefly missed `wave-settlement-r20.md` before the working copy settled — re-read confirms it present and committed, so no stale-pointer claim is made). Entry bytes could still change before scoring; findings F1–F2 are pinned to sha256 `441a751de67f…` at read time.
- PROVINCE line numbers are valid for freeze-rev bytes (verified byte-SAME); later same-line appends at EOF keep them valid per the lane's append-only convention (`PROVINCE.md` round-30/53 notes).
- I did not run `count-c2.py` or verify the remaining 11 pins/claims, registry `used-by` exactness, or the hostile trees — outside this seat's axis.

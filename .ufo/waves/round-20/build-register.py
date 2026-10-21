#!/usr/bin/env python3
"""L1 integration: build corpus/evidence/drift-classification-r20.json from wave-1 seat evidence.

One row per entering drift token. Classes are the frozen closed set in contract.md C1.
Each row cites the seat report that derived it plus primary pointers; `blind_spot` marks a
live-state token whose disappearance hides a real condition (a census design residual,
not a behavior change since the r10 baseline) — see VolatileContract.md dissent.
"""
import json, pathlib

L = pathlib.Path("/home/vgpnk/Projects/shokunin/mori-shokunin")
B = ".ufo/waves/round-20/build/"
S = "census-schema-change"; R = "roster-change"; V = "live-state"

rows = {}
def put(tok, cls, reason, evidence, seat, **extra):
    assert tok not in rows, tok
    rows[tok] = {"class": cls, "reason": reason, "evidence": evidence + "; seat " + B + seat + ".md", **extra}

# journal family (TokJournalSchema, TokJournalUser, HistR13/HistR14R15)
put("+FINDING:JOURNAL_CLASSES_UNMEASURED", S, "round-13 finding emitted unconditionally; absent from r10 census", "tools/mori-census.sh:1377; intro 18d7d55; corpus/knowledge/structured-journal-scopes-r13.md:34-38", "TokJournalSchema")
put("+SURFACE:journal.system", S, "round-13 per-scope split of the single journal row", "tools/mori-census.sh:1380,1386,1392,1675; intro 18d7d55", "TokJournalSchema")
put("+SURFACE:journal.user", S, "round-13 per-scope split of the single journal row", "tools/mori-census.sh:1380,1386,1392,1675; intro 18d7d55", "TokJournalSchema")
put("-SURFACE:journal", S, "single journal row retired in r13 (replaced by journal.user/system)", "baseline-r10 line 10; retired 18d7d55", "TokJournalSchema")
put("-FINDING:SEGFAULT_JOURNAL", S, "r10 text-derived id retired in r13; replaced by structured SEGFAULT_SIGNAL11_JOURNAL_*", "baseline-r10 line 38; retired 18d7d55; structured-journal-scopes-r13.md:45,70-72", "TokJournalSchema")
put("-FINDING:KILL_SIGNAL_JOURNAL", S, "r10 text rule replaced by structured predicates in r13 (documented blind spot for text-only SIGKILL mentions); r10 rule would match 2 sudo lines today, structured killed/9 and UNIT_RESULT=signal count 0", "baseline-r10 line 37; 18d7d55; 8d22d18; structured-journal-scopes-r13.md:68-72,78; selftest tools/mori-census.sh:3737-3738", "TokJournalSchema", r13_disagreement="r13 bucketed it as inferred live activity; measured cause is the retired text rule")
put("HEADER", S, "VERSION census-r5 -> census-r6 in r13; deliberately unmasked", "tools/mori-census.sh:281; intro 18d7d55; drift-pin-r10.md:4-6", "TokJournalSchema")
put("volatile_fields", S, "declared mask list changed in r13/r14/r15 (journal/unit counters, boot)", "tools/mori-census.sh:2744-2772; 18d7d55, 8d22d18, 26f6589", "TokJournalSchema")
put("+FINDING:COREDUMP_NOTICE_JOURNAL_USER", S, "id introduced r13 (absent from r10 census); line present because 36 user-scope coredump notices exist this boot (count-gated)", "git log -S -> 18d7d55 only; tools/mori-census.sh:1076,1325,1433,1457-1459", "TokJournalUser", future_flip="a boot with zero user coredumps removes it: classify that flip live-state")
put("+FINDING:SEGFAULT_SIGNAL11_JOURNAL_USER", S, "documented r13 structured replacement of SEGFAULT_JOURNAL (MESSAGE_ID fc2e22bc AND COREDUMP_SIGNAL=11); count 1 this boot", "18d7d55; tools/mori-census.sh:1327,1405-1406,1461-1462", "TokJournalUser", future_flip="count-gated, live-state on flip")
put("+FINDING:UNIT_FAILURE_OUT_OF_SCOPE", V, "id existed at r10; r10 logic and the r14-restored structured predicate both yield 270 non-fleet unit failures on the current boot, the r10 boot had none", "tools/mori-census.sh:1491-1493; 5be8943 census :766-767; 8d22d18; corpus/evidence/drift-r12-20261019T2204Z-classification.md:29,31", "TokUnitOOS", future_flip="boot-scoped; next reboot can clear it")

# roster family (TokRosterLanes, TokRosterFields, HistR12)
put("+FINDING:ROSTER_SET_MISMATCH", S, "info finding introduced by r12 roster reconciliation; entering census on the pin-time fleet already emits it", "tools/mori-census.sh:552; intro 1f07f1d; corpus/knowledge/roster-truth-r12.md:19-21", "TokRosterLanes")
for lane in ["chousa", "kaidoku", "lore", "mado", "mori", "revenger", "tabi", "tameshi", "tsukuroi"]:
    put(f"+SURFACE:lane.{lane}", S, "lane row produced by the r12 roster derivation (9 -> 23 lanes); lane was a fleet member at the r10 pin", "tools/mori-census.sh:444-531,2545; intro 1f07f1d; watchdog.log:336-363", "TokRosterLanes")
for lane in ["audio", "game-dev-2d", "game-dev-3d"]:
    put(f"+SURFACE:lane.{lane}", R, "conf row removed by 99efc52 before the r10 pin (2026-10-15T01:52:09-03) and re-declared by db25a48 (2026-10-19); the row exists through the r12 state-only path; membership change, not schema", "fleet commits 99efc52, db25a48; tools/mori-census.sh:444-531,2545", "TokRosterLanes", wave2_correction="falsify/FamRosterLanes.md: earlier classed census-schema-change with a false 'member at the pin' reason")
for lane, mint in (("kotodama", "417b1c2 (2026-10-17)"), ("souji", "7bf2b1a (2026-10-18)")):
    put(f"+SURFACE:lane.{lane}", R, f"lane minted after the r10 pin ({mint}); a membership change, not only the r12 schema", f"fleet commit {mint}; tools/mori-census.sh:2545", "TokRosterLanes", r13_disagreement="r13 filed it under r12 roster schema")
for key in ["+conf_dropped_n", "+conf_n", "+roster_n", "+roster_source", "+state_dropped_n", "+state_n"]:
    put(key, S, "silence-row key added by r12 roster derivation; absent from the r10 baseline silence line", "tools/mori-census.sh:2552; intro 1f07f1d; baseline-r10 line 22; roster-truth-r12.md:19,21", "TokRosterFields")

# watchdog family (TokWatchdog; dissent VolatileContract H2)
put("-FINDING:WATCHDOG_STALE", V, "STALE rule (log mtime age > 900 s) unchanged since r10; the hyaku inline driver now appends launch lines to watchdog.log, so its mtime stays fresh although the daemon has not ticked since 2026-10-15T01:58:27-03; WATCHDOG_ABSENT still fires", "tools/mori-census.sh:733-737; baseline-r10 line 24; watchdog.log:402 (last daemon tick), 403-408 (headless slot driver), 409-585 (hyaku inline); scripts/hyaku/inline.sh:103; STALE fires again once the log idles > 900 s (present in the 10:51Z pre-pin drift)", "TokWatchdog", blind_spot="log-mtime proxy no longer measures daemon liveness once another writer appends; census design residual routed to a future census round (VolatileContract K2 dissent: classify census-regression)")
put("+FINDING:WATCHDOG_STATE_LAG", V, "rule unchanged since r7; 13 lanes' last ledger launch comes from the hyaku inline driver, which keeps its own round counter and never writes .round, while the only .round writer (the daemon) has not ticked since 2026-10-15; the lags are counter mismatches", "tools/mori-census.sh:816-818; d30b4e4; scripts/shokunin-watchdog.sh:220; scripts/hyaku/inline.sh:89,103; baseline-r10 lines 1-39 (no STATE_LAG); falsify/FamWatchdog.md", "TokWatchdog")
put("round", V, "duplicate round= keys on closed-anchor rows (row-4/row-6) are concatenated by drift_scan; triggered by kumitate/kengaku/kake/kagi closing their anchor rounds", "tools/mori-census.sh:2363-2364,2409-2411,2823-2824,2839-2840", "TokWatchdog", blind_spot="comparator artifact: duplicate-key concatenation masks a same-class relaunch")

# disk (TokIoAvg)
put("io_avg_unavailable", V, "/tmp moved from tmpfs to xfs on nvme0n1p1 (fstab), so the since-boot average is now measurable and the field reads none; disk code unchanged since d30b4e4", "tools/mori-census.sh:1946-1948,1959-1960,1974; baseline-r10 line 12; /etc/fstab:24-26", "TokIoAvg", blind_spot="drift_scan compares only the first word of multi-word values (tools/mori-census.sh:2836), so the added nvme0n1p1 device in io_avg_since_boot is invisible")

# waves (TokWaves; dissent VolatileContract K3, C1Critic)
put("-FINDING:WAVE_UNSETTLED_AGE", V, "probe_waves byte-identical since r10; aggregator-r10 and aggregator-r10-resume were emptied by fleet sweep e20f4fa (2026-10-18), and the empty branch stops emitting them; new aged wave shokunin-train-20261016-w24 pairs with the old line as token obs", "tools/mori-census.sh:865-932; baseline-r10 lines 26-36; fleet commit e20f4fa (souji-shokunin, operator sweep 2026-10-18) with per-path souji cleanup receipts (committed by the same souji identity, 2f303dc, two minutes after the deletion; wave-2 FamWavesIo) for all 18 aggregator-r10 and aggregator-r10-resume files: souji-shokunin/census/operator-sweep-20261018/approval-list.tsv:56-73 (receipt=pushed); corpus/evidence/drift-r12-20261019T2204Z-classification.md:33,39", "TokWaves", blind_spot="census keeps no memory of waves; a cleanup receipt accounts for the removal but is not settlement evidence; emptied-by-hygiene vs settled is FR3 frontier; r12 called this an evidence-loss regression, VolatileContract K3 and wave-2 AdjudicateWaves recommend census-regression (recorded dissent)")
put("obs", V, "WAVE_UNSETTLED_AGE set shifted 11 -> 10 (aggregator rows gone, w24 new); positional pairing reports only obs", "tools/mori-census.sh:424,923; probe_waves :865-932", "TokSilenceB")

# lane-row family (TokSilenceA, TokSilenceB, TokPinFlap, TokPathAge)
put("basis", V, "six lane rows changed arm (aggregator B->A, kama A->8, kumitate A->4, kagi/kake/kengaku A->6) on report commits and launches; emitters unchanged since r3", "tools/mori-census.sh:2363,2377,2410,2472,2493,2545; watchdog.log:541,543,558,579,583", "TokSilenceB")
put("+reason", V, "reason= on kama (row-8), kumitate (row-4), kagi/kake/kengaku (row-6); emitter unchanged since r3", "tools/mori-census.sh:2364,2377,2411; 1439c47", "TokSilenceB")
put("+gate_s", V, "row-8 young lane (kama relaunched 07:17:03-03 inside the 7200 s gate)", "tools/mori-census.sh:360,2377; watchdog.log:583", "TokSilenceB")
put("-example", V, "aggregator left row-B after commit 1bcf59e gave it a subject commit", "tools/mori-census.sh:2488,2494; aggregator-shokunin 1bcf59e", "TokSilenceB")
put("+subject_commits", V, "aggregator row-B -> row-A (1bcf59e) adds the row-A key", "tools/mori-census.sh:2473,2494,2849-2868", "TokSilenceA")
put("-subject_commits", V, "kagi/kengaku/kake/kumitate row-A -> row-6/row-4 and kama row-A -> row-8 drop the row-A key", "tools/mori-census.sh:2377,2411,2473; report commits 01d1c22 1eed508 9a28017 4487889 204807e", "TokSilenceA")
put("+window", V, "aggregator row-B -> row-A", "tools/mori-census.sh:2473,2849-2868; 1bcf59e", "TokSilenceA")
put("-window", V, "lanes leaving row-A (row-4/6/8)", "tools/mori-census.sh:2377,2411,2473", "TokSilenceA")
put("-attribution", V, "aggregator row-B key dropped on row-B -> row-A", "tools/mori-census.sh:2494; 1bcf59e", "TokSilenceA")
put("-rowb_files", V, "aggregator row-B key dropped on row-B -> row-A", "tools/mori-census.sh:2494; 1bcf59e", "TokSilenceA")
put("+path", V, "row-6 committed-report rows (kagi, kake, kengaku) emit path= of the committed round report", "tools/mori-census.sh:2409-2411; fleet .ufo/reports/round-24/kagi.md, round-23/kake.md, round-26/kengaku.md", "TokPathAge")
put("age_s", V, "kumitate row-4 ledger-close emits age_s='-' where row-A carried a number", "tools/mori-census.sh:2363-2364", "TokPathAge")

entering = json.loads((L / ".ufo/waves/round-20/evidence/c1-drift-entering.json").read_text())
missing = sorted(set(entering["tokens"]) - set(rows))
extra = sorted(set(rows) - set(entering["tokens"]))
assert not missing and not extra, (missing, extra)
counts = {}
for r in rows.values():
    counts[r["class"]] = counts.get(r["class"], 0) + 1
doc = {
    "schema": "mori-drift-classification-v1",
    "round": 20,
    "classified_drift": ".ufo/waves/round-20/evidence/c1-drift-entering.json",
    "baseline": "corpus/evidence/baseline-r10-20261015T2231Z.json",
    "census_sha256": entering["census_sha256"],
    "closed_classes": ["census-schema-change", "roster-change", "live-state", "census-regression"],
    "class_counts": dict(sorted(counts.items())),
    "dissent": "VolatileContract (K2, K3) and C1Critic argue -FINDING:WATCHDOG_STALE and -FINDING:WAVE_UNSETTLED_AGE are census-regression (false-clean disappearance). L1 classifies by cause: the watchdog STALE rule and probe_waves are byte-identical since r10 (the script as a whole changed in seven commits), host/fleet state changed; the false-clean exposure is recorded as blind_spot and routed as a census design residual. Wave-2 AdjudicateWaves returned BROKEN for WAVE_UNSETTLED_AGE; the L1 answered with the per-path souji cleanup receipts; AdjudicateStale is recorded in the lesson. The non-author closure adjudicates.",
    "tokens": dict(sorted(rows.items(), key=lambda kv: kv[0].encode())),
}
out = L / "corpus/evidence/drift-classification-r20.json"
out.write_text(json.dumps(doc, indent=1, ensure_ascii=False) + "\n")
print(len(rows), doc["class_counts"])

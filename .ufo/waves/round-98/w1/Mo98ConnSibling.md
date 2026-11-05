# Mo98ConnSibling — sibling-overlap scan for C1 (mori round 98, wave w1)

Seat: Mo98ConnSibling (connector, leaf). Read-only scan; nothing outside this report and
`/fast/scratch/hyaku/mori-r98/Mo98ConnSibling` (now removed) was written. No tool installed or
upgraded (none needed). No git/jj mutation; no sudo; no sysctl/namespace/service change; no
subagents; no `agent://all`.

## 1. Method

20 sibling repos under `/home/vgpnk/Projects/shokunin/*-shokunin` (mori excluded) were grepped
(case-insensitive, gitignore off) for: `max_user_namespaces`; `userns|user.ns`; `CLONE_NEWUSER`;
`/proc/sys/user`; `sysctl -w|sysctl --write`; `COMMAND=`; `SYSCTL_WRITE` (siblings only);
`journalctl` (tsukuroi only, to place its owned surface); plus per-lane `userns|CLONE_NEWUSER|/proc/sys/user`
confirmation passes for revenger, kumitate, souji, kagi, kasegi, kotoba, kotodama, mado, tameshi,
lore, game-dev-2d, audio, game-dev-3d. `SYSCTL_WRITE` over all 20 siblings: **zero matches** —
the token exists only in mori (`tools/mori-userns-runway.py`, `count-c1.py` fixtures). mori's tool
docstring (`tools/mori-userns-runway.py:1-60`) defines the scanned surface: runway read over
`/proc/<pid>/ns/user` links + sudo-journal scan keyed on `sudo[` + `COMMAND=` emitting
`SYSCTL_WRITE`/`SYSCTL_WRITES n= keys= userns_zero=`.

## 2. Hits and classification (path:line, relative to /home/vgpnk/Projects/shokunin)

No sibling **owns** standing detection of this surface → class (a) is empty; mori absorbs nothing.
Class (b) remediation/OS-state owner: tsukuroi only. Everything else is (c) unrelated/one-off/consumer.

| # | Hit | Class | Note |
|---|---|---|---|
| 1 | tsukuroi-shokunin/PROVINCE.md:3-14 | (b) | Owns "host operability & system repair": pacman, systemd units/timers, **journal/boot triage (`journalctl -b`, dmesg error classes)**, drivers/firmware — all read-only probes. |
| 2 | tsukuroi-shokunin/.ufo/waves/round-13/correction/EvidenceCritic.md:93-94 | (b) | Refused a host-root write; noted userns+subuid feasibility instead — remediation restraint precedent. |
| 3 | tsukuroi-shokunin/.ufo/waves/round-15/build/SafetySourceInjection.md:23 | (b) | I7: refused to act on the `kernel.unprivileged_userns_clone=` sysctl recommendation (service/config change). |
| 4 | tsukuroi-shokunin/.ufo/waves/round-20/falsify/SysctlUserMutations.md:3 | (b) | Tsukuroi's own r20 wave detects *systemctl* mutation forms (host exec-log plane) — adjacent detection, host-unit scope, not sysctl-write journal scanning. |
| 5 | revenger-shokunin/.ufo/waves/round-98/w1-dispatch.json:163 | (c) | Post-incident guard boilerplate: "Never mutate host sysctls (e.g. user.max_user_namespaces)". Same text at revenger round-97/w1-dispatch.json:144, w1-plan.out:4, w1-run.out:144, w1-spec.json:9; round-98 w1-plan.out:4, w1-run.out:163, w1-spec.json:9. |
| 6 | revenger-shokunin/.ufo/waves/round-94/w1/SentinelScope/audit.md:51-52 | (c) | One-round host audit: no `/etc/sysctl.d` change newer than 2026-11-05; "No `sysctl -w` was observed in any trace available". |
| 7 | kaidoku-shokunin/.ufo/waves/round-20/w1/ScoutSandboxPrimitives.md:25-26,32 | (c) | One-time read: `max_user_namespaces` = 122865; sandbox-primitives probe. |
| 8 | kaidoku-shokunin/.ufo/waves/round-20/gen-wave1.py:323-324 | (c) | The r20 probe spec that produced #7 (plus wave1-dispatch.json:1307, wave1-spec.json:180). |
| 9 | kaidoku-shokunin/.ufo/waves/round-20/w1/CriticGuardSufficiency.md:22,25,46 | (c) | B4 bypass class: unprivileged userns bind-mount at the guarded path; `user.max_user_namespaces=122865` as context. |
| 10 | kaidoku-shokunin/.ufo/waves/round-92/r92-w1-dispatch.json:121 | (c) | Post-incident guard: "Host incident 2026-11-05: seats set user.max_user_namespaces to 0 and broke every bwrap sandbox." Same at r92 w1-spec.json:5, w1-validate.out:121; r93 r93-w1-dispatch.json:114. |
| 11 | kaidoku-shokunin/.ufo/waves/round-97/r97-w1-dispatch.json:121 | (c) | Same guard, names the 2026-11-05 ENOSPC incident. Same at r97 r97-w1-spec.json:5; r98 r98-w1-dispatch.json:128, r98-w1-spec.json:5. |
| 12 | kaidoku-shokunin/.ufo/waves/round-90/w1/ExecC1Battery/evidence/forged-receipts/probe.omsxta99.forged-probe.py:131 | (c) | Fixture-attack script *reads* `/proc/sys/user/max_user_namespaces` (forge evidence, not detection). Same pattern in probe-ledger.iy0sj7qv.forged-probe.py:131. |
| 13 | kake-shokunin/.ufo/waves/round-94/w1/SentinelScope.md:71-72 | (c) | One-round recording: value `122865` (read only), bwrap `--unshare-user` exit 0, "No host sysctl change needed". Tasked at r94 w1-dispatch.json:84. |
| 14 | kake-shokunin/.ufo/waves/round-42/w2/ReviewCounterV3.md:10 | (c) | bwrap probe context "unprivileged userns" (duplicated in round-48 assimilation copy). |
| 15 | kengaku-shokunin/.ufo/waves/round-89/w1/ExecCtrlC1/report.md:45-55 | (c) | Incident forensics in their lane: verbatim `bwrap: Creating new namespace failed … ENOSPC`, value read `0`. |
| 16 | kengaku-shokunin/.ufo/waves/round-89/w1/MutTesterR89/mutants.md:47 | (c) | B1 "host sandbox disabled during the run": sysctl = 0 at 05:37/05:40/05:41, `/proc/sys/user` mtime 05:27; contamination window named. |
| 17 | kengaku-shokunin/.ufo/waves/round-89/w1/SentinelR89/report.md:7,25 | (c) | I-3 environment caveat: userns disabled during review; bwrap-dependent C1 re-run blocked. |
| 18 | kengaku-shokunin/.ufo/waves/round-89/w1/CriticR89/findings.md:9 | (c) | F2 MAJOR: r89 committed figures assume userns enabled; "not re-derivable on the host as-is". |
| 19 | kengaku-shokunin/.ufo/waves/round-89/w1/ReviewerR89a/agreement.md:171-174 | (c) | **A kengaku reviewer disclosed setting the sysctl `0 → 15638 → 0` for one test window.** Matches the "transient 10000/15638 writes" mori's r98 journal scan records — independent corroboration of the incident grammar. |
| 20 | kengaku-shokunin/.ufo/waves/round-50/w1/R50C1CritMount.md:32-33 | (c) | One-time sysctl reads (122865); same class at r37 build-results.json:70, R37IndepVerdicts.md:117. |
| 21 | kotoba-shokunin/.ufo/waves/round-90/gen-w1.py:394-396 | (c, closest to (a)) | **Standing per-wave sentinel guard**: `cat /proc/sys/user/max_user_namespaces` "must read 122865 (or the pre-wave value — record it twice, 60 s apart)"; "no seat may have written /proc/sys (read-only check)". Rendered at r90-w1-dispatch.json:188, r90-w1-spec.json:65. |
| 22 | kotoba-shokunin/.ufo/waves/round-89/gen-w1.py:38-39 | (c) | Guard text naming the incident; repeated r90:40, r92:36; hygiene attestation r91 w1/ScoutSources/ScoutSources.md:307, r91-w1-results.json:28. |
| 23 | tabi-shokunin/scripts/check-bidi-runtime.mjs:570 | (c, distinct key) | **Standing gate preflight** reads `/proc/sys/kernel/unprivileged_userns_clone` (not `user.max_user_namespaces`) and refuses the live leg when the sandbox cannot start — browser-sandbox availability, not runway. |
| 24 | tabi-shokunin/.ufo/waves/round-13/w1/SafetyBrowser.txt:25 | (c) | Sandbox prereqs read: setuid chrome-sandbox, userns_clone=1, max_user_namespaces=122842 (older value — dated evidence). |
| 25 | tabi-shokunin/.ufo/waves/round-33/w1/ExecLiveLeg.md:105-106 | (c) | Probe records `sysctl kernel.unprivileged_userns_clone` → 1; refusal branch host-scoped (r33 SentinelLiveLeg.md:215-217,296). |
| 26 | kumitate-shokunin/.ufo/waves/round-45/a2-control/RedoDemoBwrapEnv.md:278 | (c) | Environment evidence line: `kernel.unprivileged_userns_clone=1; user.max_user_namespaces=122865`. |
| 27 | kumitate-shokunin/.ufo/waves/round-48/r48/ScoutRootCause.md:45 | (c) | strace: 106 processes whose first traced call is `clone` with `CLONE_NEWNS|CLONE_NEWUSER|CLONE_NEWPID` — bwrap's supervisor, attributed, not detected as a resource. |
| 28 | kumitate-shokunin/.ufo/waves/round-91/K91Connector/hits-sibling-scripts.txt:119 | (c) | Cross-citation of tabi's preflight (check-bidi-runtime.mjs:570) in kumitate's sibling-script scan. |
| 29 | souji-shokunin/.ufo/waves/round-34/w1/SwarmScout28.md:5 | (c) | Sandbox recon records userns sysctl `1`; SwarmExecutor17.md:152 verifies `unshare -Ur` rc 0. |
| 30 | souji-shokunin/.ufo/waves/round-34/w1/SwarmExecutor17.md:227 | (c) | G4 gap: counter checks binary presence only — "on a host with bwrap present and userns disabled, G4 would PASS while every sandbox leg could-not-evaluate". Precisely the runway blind spot mori's C1 now covers. |
| 31 | chousa-shokunin/.ufo/waves/round-31/falsify/CriticClaimsAfter31/gate-c1-nonstring-absent.sh:5318-5324 | (c) | Consumer: research-gate `ns_probe`; "No userns => the ns cases are skipped BY NAME and the skip is counted" (same block in gate-c2, mutants, pristine copies). r14 adversaries 29/30 designed the userns-availability liveness probes (reports/round-14/chousa.md:65,92). |
| 32 | mado-shokunin/.ufo/waves/round-20/w1/reports/ScoutUnshareHost.md:11 | (c) | Env read: `/proc/sys/user/max_user_namespaces` = 122865, userns_clone = 1. |
| 33 | mado-shokunin/.ufo/waves/round-48/w1/SentHost/guards.md:202-203 | (c) | Standing receipts probe (SentHost/probe.sh:186) runs `sysctl kernel.unprivileged_userns_clone user.max_user_namespaces` and pins both values in host-tooling receipts. |
| 34 | mado-shokunin/.ufo/waves/round-20/w1/reports/CriticIsolation.md:21 | (c) | Names `max_user_namespaces` as one mode that can refuse userns on other hosts ("namespaces unavailable; running unisolated" fail-open risk). |
| 35 | tameshi-shokunin/.ufo/waves/round-48/w1/T48RevenEnvDiff.md:120 | (c) | Env figures: `max_user_namespaces 122865`, userns_clone 1 — load attribution context. |
| 36 | tameshi-shokunin/.ufo/evidence/round-30/sources/S093-bwrap-0.13.1.xml:166-176 | (c) | Pinned bwrap manual (--userns/--disable-userns options); doc-snapshot mention. |
| 37 | game-dev-2d-shokunin/corpus/fixtures/export_launch_s02.gd:34-35,78-79 | (c) | Consumer: `_probe_unshare` tmpfs-isolation diag (`userns_tmp_isolation=true`) across ~12 export fixtures and live verdicts (corpus/live/runs/20261018T200239625248Z/verdicts.json:20312 et al.). Degrades if runway exhausts. |
| 38 | kotodama-shokunin/reports/round-39/calib/Ca01-protocol.md:271-272 | (c) | Tier-A prereq: bubblewrap + `unprivileged_userns_clone=1`; otherwise Tier B/C fallback. |
| 39 | kotoba-shokunin/.ufo/waves/round-81/build/Kb81R01NegSweep-fetch/agent-sdk-secure-deployment.md:155 | (c) | Fetched doc mention of Docker `--userns-remap`; unrelated. |
| 40 | kama-shokunin/.ufo/waves/round-64/f/out/MT22ListenerShapes/code/facts.py:170 | (c) | Fixture code `os.unshare(os.CLONE_NEWUSER|os.CLONE_NEWNET)` for listener forging (also mt22-build.py:124-125, mt22_helper_lib.py:90-91, MT22ListenerShapes.md:164-165); kama r22 os.html doc snapshot. |

Zero-hit lanes (per-lane greps, "No matches found"): revenger (`userns|CLONE_NEWUSER|/proc/sys/user`),
kagi, kasegi, lore, audio, game-dev-3d. `SYSCTL_WRITE` across all 20 siblings: zero.
`sysctl -w` across all siblings: only guard boilerplate (#5, #10, #11, #22 class) and revenger's
negative audit (#6) — no sibling executes or parses `sysctl -w`.
`COMMAND=` across all siblings: receipt/selftest boilerplate only (`command=`, `PHASE=…COMMAND=`,
`REA_*_COMMAND` env exports) — **no sibling parses `COMMAND=` out of sudo journal lines**. Mori's
journal+`COMMAND=` detection has no analog anywhere in the fleet.

## 3. PROVINCE.md Adjacent vs the Round-98 core note — conflict check

Read: PROVINCE.md:58-110 (Adjacent) and :697-700 (Round-98 appended notes).

**No conflict.** Three explicit anchorings:

1. **souji row (PROVINCE.md:69)** already routes *liveness/resource findings to mori* while souji
   keeps reclamation. The user-namespace runway is a liveness/resource surface, so the note lands on
   mori's side of an already-adjudicated boundary; the note's "mori reports, never performs
   reclamation/restoration" mirrors souji's row exactly.
2. **tsukuroi row (PROVINCE.md:66)** gives tsukuroi host OS/package/unit/driver/firmware/boot
   *diagnosis*. Tension, stated plainly: tsukuroi's owned surface includes "journal/boot triage
   (`journalctl -b`, dmesg error classes)" (tsukuroi PROVINCE.md:8-10), so a broad reading could
   claim sudo-journal parsing for tsukuroi. The r98 note resolves it the same way the r12 connector
   resolved FR1 (kernel-OOM attribution declared "adjacent host diagnosis, not contested fleet
   ownership", PROVINCE.md:66): mori's scan detects **fleet-seat** kernel-tunable writes for fleet
   causality (redacted fields only — no user name, PWD or command text, per the tool docstring,
   which also keeps it clear of kagi's credential boundary at PROVINCE.md:68), while host-unit
   diagnosis and any OS-state repair stay tsukuroi's. The note's boundary line ("Restoring host
   configuration is the operator's; repairing OS state is tsukuroi's") is an explicit hand-off, not
   an absorption, and matches the r85/r86 pattern ("mori reports, it does not remediate").
3. **kumitate row (PROVINCE.md:65)**: the note edits no settlement contract; the wave files live
   under `.ufo/waves/round-98/` like every prior round.

Nothing in Adjacent refuses mori reading a host resource counter; the refusal is absorbing another
lane's domain, and the note routes repair out rather than claiming it.

## 4. Cross-lane routes (named, nothing edited)

- **→ tsukuroi**: the 2026-11-05 incident is OS-state damage; any restore/repair need routes to
  tsukuroi/operator per the r98 boundary. Tsukuroi's r20 systemctl-mutation classifier (#4) and
  mori's SYSCTL_WRITE scan both detect kernel-tunable mutations but on disjoint producers (systemd
  exec-log host-unit plane vs sudo journal fleet-seat plane); tsukuroi should know the latter exists
  so a future incident is not double-claimed.
- **→ kengaku**: ReviewerR89a's disclosed `0 → 15638 → 0` window (#19) is independently corroborated
  by the values mori's r98 journal scan records ("transient 10000/15638 writes", tool docstring) —
  two lanes, same fact, neither knew of the other. Kengaku's F2 (#18: r89 figures not re-derivable
  without userns) is now answerable by one runway read before any bwrap-dependent replay.
- **→ chousa**: research-gate skips its userns cases *by name* when userns is unavailable (#31);
  with the runway exhausted those skips would silently grow. Recording the `USERNS_RUNWAY … state=S`
  line beside `NS_STATE` in the gate summary is their call.
- **→ souji**: their own G4 finding (#30) is the fleet-wide blind spot (bwrap present + userns
  disabled ⇒ PASS with all legs could-not-evaluate); mori's runway state is the missing precondition
  signal they already described.
- **→ kotoba / mado / tabi**: all three run standing wave-local guards or preflights over userns
  sysctls (#21-#23, #33) — these stay theirs; mori adds journal write *attribution*, not value
  assertion. Two vocabularies now exist for one resource (guard value vs runway state); keep them
  distinct in future cross-references.
- **→ kumitate**: the post-incident "never mutate user.max_user_namespaces" guard sentence is
  duplicated as literal text in ≥5 lanes' generators (kotoba r89-92, kaidoku r92/93/97/98, revenger
  r97/98, kake r94, kengaku r89-era, mado r48-era probes). A single shared guard is kumitate's
  harness decision; mori's detector can be the fleet tripwire either way.
- **→ game-dev-2d / kotodama / tameshi / kama / kaidoku / chousa**: all are userns *consumers*
  (fixtures, gates, sandbox wrappers, forged probes); an exhausted runway degrades or ENOSPCs them
  (kengaku r89 spent ExecCtrlC1 + MutTester + Sentinel discovering "host state, not counter logic").
  Capturing mori's one-line runway reading as a wave environment receipt would have collapsed that
  post-mortem to a single line.

## 5. Connector move (proposal only — round 98 is frozen; nothing edited)

**Move (coverage, future round):** extend the `SYSCTL_WRITES` summary with `userns_restore=N` —
count of sudo-journal writes setting `user.max_user_namespaces` to a value > 0 — so one line
distinguishes "zeroed and left there" from "transient zero, restored". Evidence the pattern occurs:
kengaku's disclosed `0 → 15638 → 0` window (#19) sits in the same journal the tool already parses;
the grammar change is additive, read-only, touches no other surface, does not remediate, and leaves
calibration (C2 scorecard cells) untouched. **Fleet-level synthesis:** emit the `USERNS_RUNWAY`
reading as the shared bwrap-precondition receipt for consumer lanes (chousa, souji, kengaku,
game-dev-2d) — improves their coverage attribution at zero cost to any axis.

## 6. Verification and unrun checks

Run by this seat: only the greps in §1 and the reads cited above (all via the grep/read tools;
exact results quoted in §2 and §6 of the chat trailer). Installs: none.
**Unrun (not this seat's predicates):** `count-c1.py` before/landing (`C1=unmet 0/15` →
`met 15/15`), `count-c2.py` (`mismatches=2` → `0`), `controls-r98.sh`, the landing receipts, and
the counter execution for C1's 15 cases — none executed here; their verdicts are claimed by other
seats/the L1 and are not re-derived or endorsed by this report. Live `--journal-live` and runway
reads of the host were also not run (no need for the overlap question; nothing host-state was
touched).

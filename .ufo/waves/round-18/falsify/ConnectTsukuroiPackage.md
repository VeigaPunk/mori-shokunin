# Round 18 package-event handoff — falsification

## Axes and verdict

Round-18 declared axes are **C1 adjacency / private-context retention**, **C2 calibration / freeze-order**, and **C3 operability / per-attempt dispatch binding** (`.ufo/waves/round-18/contract.md:20,24-43`). The bounded move below improves C1; it does not change C2 or C3.

**Tsukuroi still has sufficient non-private evidence to own the package and boot-chain interpretation/handoff, but not to identify an actor, establish current host health, or determine authorization.** Its own S065 source is a read-only retained pacman-log capture with transaction receipts; its stated limits exclude actor, client exit, health, and current package classification (`../tsukuroi-shokunin/corpus/lessons/round-18.md:114`). Its r19 lesson records Mori's pacman-log receipt as **acknowledged**, not accepted or resolved (`../tsukuroi-shokunin/corpus/lessons/round-19.md:12`). Tsukuroi owns package and boot diagnosis, read-only, and leaves remediation to the operator (`../tsukuroi-shokunin/PROVINCE.md:8-14,27-28`).

## Evidence and gaps

### Evidence that survives minimization

- Mori's contract limits this item to a detection-only handoff to Operator/Tsukuroi (`.ufo/waves/round-18/contract.md:20`); the routed-defect review explicitly says not to infer actor/authorization or perform remediation in Mori (`.ufo/waves/round-18/build/ReviewRoutedDefects.md:22`).
- Mori's province states the package/boot interpretation remains Tsukuroi/operator-owned and that Mori made no package transaction or service change (`PROVINCE.md:111-117,139-141`). Thus there is **no Mori remediation claim**.
- Tsukuroi has independently retained the event record at `.ufo/waves/round-18/l1-capture/pacman-events-r18.txt` (SHA-256 `023c740ad3125adf24caa2376e7e46ede0f9f3f317fcd07ff1901fd0727d6a83`); its lesson identifies this as ALPM evidence, not actor/health evidence (`../tsukuroi-shokunin/corpus/lessons/round-18.md:114`). The r17 lesson also points to the retained boot-chain and fresh captures (`../tsukuroi-shokunin/corpus/lessons/round-17.md:23-29`), and the r17 verifier records both an admitted corrected boot-chain note and a rejected initial prediction (`../tsukuroi-shokunin/corpus/lessons/round-17-verifier-spotcheck.md:145,148`). These provide enough dated input for Tsukuroi to analyze the event; they do not establish a repair or authorization.
- The current minimized `PacmanActorTrace.md` digest is `b30443665d48a32bb49dfa501eef8ec594a3ab03b299bf9e84d0904b6512d1bf`. However, line 40 still asserts an event-to-OMP-session attribution, while the minimization report says that transaction-to-session mapping was removed (`.ufo/waves/round-17/build/PacmanActorTrace.md:40`; `.ufo/waves/round-18/build/RedactPacmanActorTrace.md:19,23`). The identity/artifact locator is absent, but the residual session linkage is a manual, out-of-metric minimization question; C1 itself says its regex is only a recall floor (`.ufo/waves/round-18/frozen/c1-policy.json:27-29`). The adjacent redaction report does not make that surviving linkage disappear.
- Current `PacmanTxnToday.md` digest is `96ec030742fb9141c9b9c049b5b12cf36412c020eec09c8578f520870d92e39e`. Lines 119-120 retain **two joined account/location attribution elements** (no values reproduced here). The C1 adjacent-document review identifies the original line-119 R4/private-document hit and separately flags the account/location material as outside the frozen regex (`.ufo/waves/round-18/build/AdjDocumentRefs.md:15-23,31`). This conflicts with the out-of-metric disposition's statement that the joined identities were redacted (`.ufo/waves/round-18/out-of-metric-triage.md:33`). The existing source review itself supplies the count and classification; no private value is repeated in this report.

### Authorization-status claim and explicit contradiction

Mori makes **no claim to authorize a package action**, but `PacmanTxnToday.md` goes beyond neutral event detection: it concludes a host-wide pause was in force by a dispatch-artifact time (`:82-84`) and labels later transactions post-ruling (`:90-93`). The same section says no artifact contains the ruling timestamp (`:71-84`). This is an authorization-status inference, not a remediation claim, and conflicts with the round-18 instruction not to infer authorization (`.ufo/waves/round-18/build/ReviewRoutedDefects.md:22`).

The cited dispatch text establishes that an instruction was carried; it does not by itself establish the operator ruling's authoritative start time or applicability to host activity. Tsukuroi's SKILL carries a standing statement that transactions remain paused (`../tsukuroi-shokunin/SKILL.md:1848-1853`), while Mori's event report records transactions after its inferred onset. Those facts permit a policy-violation interpretation, but do **not** show that the pause was lifted or that any transaction was authorized. A separate cross-report reading disputes the pause's host applicability (`.ufo/waves/round-17/build/OverlapTsukuroi.md:106-111`; SHA-256 `c0bf5b12b9e337fabf3598af2a4953fd54e23ad27a842eaa30102a36f26b3eb3`). That report's cited range is detailed host context outside the frozen C1 classes (`.ufo/waves/round-18/build/AdjDocumentRefs.md:32`); it is cited here only as a contradiction pointer, not quoted or treated as an authoritative ruling. **Authorization and pause applicability remain unresolved for the operator.**

## One bounded move

Replace Mori's package-event narrative with one **event-only, sanitized handoff card**: point to the retained Tsukuroi S065 event capture and boot-chain capture, preserve their digests and source anchors, and report the receipt state as `acknowledged` only. Remove the remaining account/location join and session-link attribution from the Mori copy; describe the pause only as an observed dispatch instruction with operator applicability/effective time unknown unless an authoritative ruling record is supplied. Do not add a probe, package action, journal query, or host-state claim.

This improves **C1 adjacency/retention** by retaining the evidence needed by the owner while avoiding replicated joined context. C2 freeze-order and C3 dispatch-ledger behavior remain unchanged; no effect on those axes is claimed. No remediation authority is transferred.

## Risks and verification

- **Risk:** an event-only card has less detail for actor attribution. That detail is not required for Tsukuroi's package/boot diagnosis, is already unresolved in the permitted evidence, and should remain operator-owned rather than be inferred from a session join.
- **Risk:** a retained log receipt can be mistaken for current health or authorization. Keep the dated scope and S065 limits adjacent to the pointer; do not upgrade `acknowledged` to `accepted` or `resolved`.
- **Risk:** removing duplicate context could appear to weaken auditability. Preserve content hashes and line/source anchors; the separate Tsukuroi capture remains independently retained.
- **Proposed verification, not run:** after any integration, recheck the frozen C1 gate and manually review the two package reports for out-of-metric joins; confirm the event and boot-chain pointers still resolve; confirm handoff closure remains `acknowledged` only; verify no text treats the dispatch context as an authenticated operator authorization. No package, journal, or service probe is needed.

## Read-only work record

- Read the round-18 contract, C1/C2/C3 frozen inputs, draft verdicts, out-of-metric triage, Mori province and relevant reports, plus Tsukuroi PROVINCE/SKILL and r17-r19 lesson/spot-check sections. Path-filtered search located the package-history disposition; read/search tools returned results but do not expose shell exit codes.
- `sha256sum -- /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-17/build/PacmanActorTrace.md /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-17/build/PacmanTxnToday.md /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-18/l1-capture/pacman-events-r18.txt` — exit 0.
- `sha256sum -- /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-17/build/OverlapTsukuroi.md` — exit 0.
- No URLs consulted; no tools installed or updated; no VCS command, pacman action, journal query, test, build, or write outside this report.
# Mo49ConnSiblings — Sibling-overlap scan (mori round 49, wave w1)

Seat: leaf connector. No subagent dispatch. Read-only evidence: sibling lane trees under
`/home/vgpnk/Projects/shokunin/*-shokunin` (live files only; `.scratch` and `.ufo/waves`
excluded from every targeted search). No tool installs were performed, no file was written
outside this report, no credential/session material appears (machine id: MACHINE_ID).

## 1. Journald retention ownership — scan and commands

Command 1 (live `SKILL.md` + `PROVINCE.md` of every sibling lane):
`grep` pattern `journald\.conf|SystemMaxUse|MaxRetentionSec|RuntimeMaxUse|JournalMaxUse|vacuum-size|retention`
over the 40 joined paths (`…/*-shokunin/SKILL.md`, `…/*-shokunin/PROVINCE.md`).
Result: **no live sibling SKILL.md/PROVINCE.md names journald configuration or a retention
setting** (no `SystemMaxUse`/`MaxRetentionSec`/`RuntimeMaxUse`/`journald.conf`/`vacuum-size`).
The only `retention` hits are unrelated domains: kake HTTP-capture retention boundaries
(`SKILL.md:645-656,671`), kaidoku MCP-session retention epochs (`SKILL.md:407`,
`PROVINCE.md:58`), souji evidence-cache retention (`SKILL.md:187-189`), tabi gzip
retention (`SKILL.md:2003-2005`), kama install-retention decisions
(`PROVINCE.md:89-90`), kagi Vault/KV-retention parity limits (`SKILL.md:682-684`,
`PROVINCE.md:76-77`).

Command 2 (all sibling `corpus/` dirs): pattern `journald\.conf|SystemMaxUse|MaxRetentionSec|RuntimeMaxUse|JournalMaxUse|vacuum-size|\-\-vacuum|retention`.
Result: hits are other lanes' own retention concepts (kumitate `ufo-state-retention.mjs`
runtime-state caps, kake round-27 HTML-retention receipts, etc.); zero live corpus claim
about journald configuration in a sibling lane.

Command 3 (tsukuroi live PROVINCE.md + SKILL.md, systemd/journald ownership): pattern
`journald|journalctl|systemd unit|systemd|/etc/systemd`.
Result:
- `tsukuroi-shokunin/PROVINCE.md:3-4`: "Domain: host operability & system repair (繕, mending) — the OS substrate itself: package state, systemd, drivers/firmware, boot health."
- `PROVINCE.md:10-13`: "systemd user units & timers (`systemctl --user`, unit files, failed states), journal/boot triage (`journalctl -b`, dmesg error classes), driver/firmware plane…"
- `SKILL.md:46-48`: package/unit/triage rows; `:152` lists read-only verbs incl. `journalctl -b/-k/--list-boots/--disk-usage/-o json`; `:158` forbids `journalctl --rotate/--vacuum-*` and `systemctl start/stop/restart/enable/disable/preset`.
- `PROVINCE.md:188-189` OV5/OV6: overlap register vs mori (earlyoom/oomd; rows reported, never absorbed); `:49` ADJ-04 routes "dated kill-event clusters in the oom plane's retained window" to mori.
- (An unfiltered whole-dir scan of tsukuroi additionally hit `journald.conf`/`--vacuum-*` text only inside `.ufo/waves/` archives of systemd man pages/NEWS — historical snapshots, not live ownership claims; excluded from the verdict.)

Ownership verdict: journald configuration and systemd-unit state are tsukuroi's PROVINCE.
The C2 entry documents how far mori's **reads** can reach (retention rule, persistent/volatile
split, vacuum order, this host's effective ceilings) from the committed man-page copies plus a
read-only host receipt; it configures nothing and runs no vacuum/rotate/systemctl. That
**adjoins** tsukuroi's province (read-side reach vs config/remediation side) and does not
conflict with mori's `Refuses OS-package state` paragraph (SKILL.md:143-145) as long as the
entry carries the boundary sentence below.

Required single sentence the entry's Boundaries section must carry:
> This entry reads how far the journal's retained records reach and sets no journald configuration or systemd-unit state — journald configuration and any vacuum/rotate/systemctl remediation are tsukuroi's province (mori Refuses OS-package state), and mori never remediates.

## 2. Pin/registry-checker tooling — scan and commands

Command 4 (kotoba + kumitate live dirs: SKILL.md, PROVINCE.md, corpus/, verifiers/, tools/, scripts/, plans/): pattern `registry-pin|registry_pin|pin-check|pin_check|min-tally-pins|PIN_CHECK|reconcil|tally`.
Result:
- kotoba `verifiers/`: `check_r64_routed_repairs.py`, `check_r66_routed_repairs.py`, `check_instruction_authority.py`, `check_seat_counts.py`, `check_infoless_fences.py` (each carries `--self-test`; C2-style counters over committed revisions). Corpus lessons record self-test tallies (round-51/58 spot-checks) and a floors-registry.
- kumitate `corpus/QUALITY.md`: Q20 (verdict guard pinned by a selftest case; dropping mutant killed), Q31 (counter sandbox decided by selftest), Q41 (every gate-count sentence reconciled against `kind=gate` registry rows); `scripts/source-capture.mjs` binds every `S###` row to a capture under `.ufo/pins/source-captures.json` (committed bytes + sha256 + size + capture date, or a named exemption).

Command 5 (all sibling `tools/`,`scripts/`,`verifiers/`): pattern `registry-pin|registry_pin|pin-check|pin_check|min-tally-pins|PIN_CHECK|reconcil|tally|repin|rep_in|pins`.
Result:
- chousa `tools/research-gate.sh`: capture-tool pins — absolute bash/env/grep provenance pins, line-span and sha256 record pins (round-41 C1).
- kake `scripts/freshness-sweep.mjs` + `corpus/knowledge/freshness-pins.json` (standing-claim pins); `ledger_latest_check.py` rescore-tally; `receipt_replay.py` verdict tally.
- mado `tools/mado-action-plan.py` `PINNED_POLICY`; `mado-verify.sh` version pins (Hyprland commit, waybar), record-level sha pins, snapshot count reconciliation.
- kengaku `plans/attrib-r22-frozen.md` FROZEN sha lines; fixture `attrib_oracle.sh` tally rows; `cp_reference.py` expect pins.
- kotoba `verifiers/check_substrate_pins.py`: enforces `baseline.json` `measured_against` (sha256+mtime of the omp/opencode binaries); **hashes bytes, never execs**. `verifiers/check_substrate_repin_v2.py` (round-72 C2): re-derives host substrate pins (`pins OK k/3`), surfaces `p of 7`, removal ledger. `check_assertion_floors.py` + `floors-registry.json`: floors, not pins.
- kumitate `scripts/ufo-state-retention.mjs` (+ tests): runtime-state retention cap/sweep (not a pin checker).

Competition verdict: the closest siblings are kotoba's `check_substrate_pins.py` /
`check_substrate_repin_v2.py` (both are pin guards), but their object is the **host binary
substrate** (omp/opencode sha256+mtime) and they hash bytes without executing. kumitate's
source-capture pins bind SOURCES rows to captured byte blobs; kake's freshness-pins are JSON
anchor numbers; none reads the lane's SKILL.md gate-registry self-test cells, binds a tally pin
to a nearby `--selftest` command, executes it, and compares the observed output text and exit
code to the pinned text with a `--min-tally-pins` floor and `--baseline-rev` dropped/rebound
check — which is what mori's `tools/mori-pin-check.py` (v3) does. **Conclusion: mori's tool
duplicates no sibling checker; it at most adjoins kotoba's pin-guard concept (different object,
different mechanism).**

## 3. Pre-data observations

- S351 confirmed present as a rejected row (`corpus/SOURCES.md:248`) with the flip text already
  recorded; the new row's `teaches` must open `supersedes S351 —`.
- S485–S488 (status mined, opened 2026-10-25) do **not** yet exist in the current
  `corpus/SOURCES.md` (registry ends at S484; rejected rows through S351). They are the planned
  data-phase rows for the entry. UNVERIFIED at this revision until minted; the frozen contract
  names these ids.

## Findings

- MED — `mori-shokunin/SKILL.md:143-145` (Refuses OS-package state) paired with
  `tsukuroi-shokunin/PROVINCE.md:3-4,10-13` and `SKILL.md:46-48,152,158`: journald/systemd-unit
  config and journal/boot triage are tsukuroi's. The C2 entry must carry the boundary sentence
  named in §1 or it will be read as claiming journald-config knowledge mori refuses.
- MED — `tsukuroi-shokunin/PROVINCE.md:49` (ADJ-04) already routes "retained window"
  kill-cluster questions to mori: mori's read-side reach is established adjacency, not a conflict.
- LOW — `kotoba-shokunin/verifiers/check_substrate_pins.py` / `check_substrate_repin_v2.py`
  are pin guards over host binary substrate (bytes, never exec); mori's `mori-pin-check.py`
  (selftest-tally + digest reconciler that runs the bound command) is duplicated by no sibling.
  kumitate `scripts/source-capture.mjs` pins source rows to capture blobs — not a tally reconciler.
- LOW — `mori-shokunin/corpus/SOURCES.md` (registry tail, line ~263): S485–S488 absent pre-data
  (expected); mint at data phase with status `mined`, opened 2026-10-25, used-by the entry.

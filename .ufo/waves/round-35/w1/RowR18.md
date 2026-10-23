measured 2026-10-23T08:51:47Z

# Round 18 capabilities-register findings

## Axes and rows

The closure maps retention gate to adjacency, freeze-order check to calibration, and dispatch-ledger verification to operability; MANIFEST.json at fleet revision 37b51a243302e8009c7067431e8a47f9a722fd14 records round 18 as admitted and these axes as improved (MANIFEST.json:9449-9475, 9457-9465). The three outputs below are supported by the closure record and its pinned non-author spot-check.

ROW: | rounds[386].capabilities_added[0] | retention gate | Scans repository revisions under the retention policy and reports metric and routed counts; its recorded after metric and routed count were 0 with 86 allowlisted at 3127c3a. | `tools/mori-retention-gate.py` | 18 |
Evidence choice: The manifest names this exact tool, and the pinned spot-check independently remeasured the C1 scan and matched its committed after evidence, so this is the direct artifact for the running capability. Sources: MANIFEST.json@37b51a243302e8009c7067431e8a47f9a722fd14:9473; corpus/lessons/round-18-verifier-spotcheck.md@b3602869dadd4016675aeba8db2adf3fa1e1b531:43-52.
Citations for the row: .ufo/reports/round-18/mori.md@37b51a243302e8009c7067431e8a47f9a722fd14:44-45; corpus/lessons/round-18-verifier-spotcheck.md@b3602869dadd4016675aeba8db2adf3fa1e1b531:43-55.
VERDICT: supported

ROW: | rounds[386].capabilities_added[1] | freeze-order check | Checks frozen claim inputs against implementation history and counts overclaims; the recorded total moved from 4 before to 0 at 3127c3a, including three prospective round-18 pre-build checks. | `tools/mori-freeze-order.py` | 18 |
Evidence choice: The manifest names the freeze-order check and the pinned spot-check confirms the measured before/after result while limiting its interpretation, so this tool is the direct capability pointer. Sources: MANIFEST.json@37b51a243302e8009c7067431e8a47f9a722fd14:9474; corpus/lessons/round-18-verifier-spotcheck.md@b3602869dadd4016675aeba8db2adf3fa1e1b531:81-95.
Citations for the row: .ufo/reports/round-18/mori.md@37b51a243302e8009c7067431e8a47f9a722fd14:46-47; corpus/lessons/round-18-verifier-spotcheck.md@b3602869dadd4016675aeba8db2adf3fa1e1b531:81-95.
VERDICT: supported

ROW: | rounds[386].capabilities_added[2] | dispatch-attempt ledger verify | Verifies dispatch-attempt payload bindings: round-18 wave 1 had 1/1 and wave 2 2/2 bound clean; residual 7/7 were bound but flagged STARTED_MISSING. | `tools/mori-dispatch-ledger.py` | 18 |
Evidence choice: The manifest names this verifier and the pinned spot-check confirms clean wave results while recording the residual failure shape, making the verifier the direct artifact for this capability. Sources: MANIFEST.json@37b51a243302e8009c7067431e8a47f9a722fd14:9475; corpus/lessons/round-18-verifier-spotcheck.md@b3602869dadd4016675aeba8db2adf3fa1e1b531:97-107.
Citations for the row: .ufo/reports/round-18/mori.md@37b51a243302e8009c7067431e8a47f9a722fd14:48-49; corpus/lessons/round-18-verifier-spotcheck.md@b3602869dadd4016675aeba8db2adf3fa1e1b531:97-107.
VERDICT: supported

## Strong-path checks and limits

- Each chosen path is under tools/, equals the path named in its capability string, and is named in the admitted closure record (MANIFEST.json:9457-9458, 9472-9475; the fleet report lists the tools at lines 21 and runs them at lines 44-48).
- These closure source reads succeeded: `timeout 20 git -C /home/vgpnk/Projects/shokunin/mori-shokunin show 3786f3f1bde2fbcc5ce617e35e8c9becdbf9d9e8:tools/mori-retention-gate.py > /fast/scratch/hyaku/mori-r35/MoriR35.RowR18/mori-retention-gate.py`; `timeout 20 git -C /home/vgpnk/Projects/shokunin/mori-shokunin show 3786f3f1bde2fbcc5ce617e35e8c9becdbf9d9e8:tools/mori-freeze-order.py > /fast/scratch/hyaku/mori-r35/MoriR35.RowR18/mori-freeze-order.py`; and `timeout 20 git -C /home/vgpnk/Projects/shokunin/mori-shokunin show 3786f3f1bde2fbcc5ce617e35e8c9becdbf9d9e8:tools/mori-dispatch-ledger.py > /fast/scratch/hyaku/mori-r35/MoriR35.RowR18/mori-dispatch-ledger.py` all succeeded.
- `timeout 20 git -C /home/vgpnk/Projects/shokunin/mori-shokunin diff --name-status d005cdde0e009dea6c0cc29b37163de536528658 3786f3f1bde2fbcc5ce617e35e8c9becdbf9d9e8 -- tools/mori-retention-gate.py tools/mori-freeze-order.py tools/mori-dispatch-ledger.py` returned `A` for each, confirming they changed since the previous mori closure.
- `timeout 10 git -C /home/vgpnk/Projects/shokunin/mori-shokunin rev-parse HEAD` returned `913df22e29f131ef9cb5de9dcb7e3e272256c5f0`; `timeout 15 git -C /home/vgpnk/Projects/shokunin/mori-shokunin ls-tree -r --name-only HEAD -- tools/mori-retention-gate.py tools/mori-freeze-order.py tools/mori-dispatch-ledger.py` listed all three, confirming they remain at the lane tip.
- C1's zero is allowlist-relative: 86 retained surface, instruction, and field-name lines were allowlisted; the check does not establish that every out-of-metric issue is resolved (spot-check:53-76). C2's 4-to-0 includes three prospective round-18 pre-build checks, and its evidence JSON lacks revision metadata (spot-check:90-95). C3's residual 7/7 are bound but STARTED_MISSING and fail the check (spot-check:103-107).

## Provenance, touched surfaces, and out of scope

- Timestamp command: `timeout 10 date -u +%FT%TZ` returned `2026-10-23T08:51:47Z`.
- Read-only fleet captures succeeded: `timeout 20 git -C /home/vgpnk/Projects/shokunin show 37b51a243302e8009c7067431e8a47f9a722fd14:MANIFEST.json > /fast/scratch/hyaku/mori-r35/MoriR35.RowR18/MANIFEST.json`; `timeout 20 git -C /home/vgpnk/Projects/shokunin show 37b51a243302e8009c7067431e8a47f9a722fd14:.ufo/reports/round-18/mori.md > /fast/scratch/hyaku/mori-r35/MoriR35.RowR18/fleet-report-r18.md`; and `timeout 20 git -C /home/vgpnk/Projects/shokunin/mori-shokunin show b3602869dadd4016675aeba8db2adf3fa1e1b531:corpus/lessons/round-18-verifier-spotcheck.md > /fast/scratch/hyaku/mori-r35/MoriR35.RowR18/round-18-verifier-spotcheck.md` succeeded. The queried manifest entry `.rounds[386]` returned round 18.
- Captured and inspected the three closure-version tools. No tool, selftest, or C1 counter was executed by this seat; run outcomes above are attributed to the closure report and non-author spot-check, not to this seat.
- Only lane write: `.ufo/waves/round-35/w1/RowR18.md`. Read-only source copies are under `/fast/scratch/hyaku/mori-r35/MoriR35.RowR18/` (MANIFEST.json, fleet-report-r18.md, round-18-verifier-spotcheck.md, and the three tool files).
- No product code, SCORECARD, MANIFEST, fleet report, or other lane file was changed. No tool was installed or updated. No counter, tests, or build checks were run; no deployment or commit was made.

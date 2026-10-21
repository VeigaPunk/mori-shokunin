# ImplSettlement — Round 20 C2

## Files changed

- Added `.ufo/waves/round-20/build/ImplSettlement/tools/mori-wave-settlement.py` (stdlib-only Python 3; executable).
  - SHA-256: `ee7e281b020a56a2760bfc9285a5c35016b362818679dfdbf0e8bff812b2a5b6`
  - Implements recursive regular-JSON dispatch discovery, report-trailer validation, lstat-based non-following member classification, wave/totals summaries, deterministic JSON, optional `--out`, exit codes, and the frozen-oracle `--selftest`. See implementation lines 63–93, 123–188, 191–261, 264–313, and 509–548.
- Replaced this advisory report with the final findings.

## Evidence

- `python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-20/build/ImplSettlement/tools/mori-wave-settlement.py --selftest`
  - `MORI_WAVE_SETTLEMENT_SELFTEST: PASS (14 cases, 14 passed, 0 failed)`
- One final mori scan, with `--fleet-root /home/vgpnk/Projects/shokunin`, reported:
  - Fleet totals: 11 waves, 671 members; present 586, missing 85, empty 0, misrooted 0, unsafe 0, unparsed 0; `ignored_json` 467 and `unreadable_json` 2.
  - `.ufo/waves/round-19/wave1-run.json` (`mori-r19-attempt2-build`): partial, 64 members; present 16, missing 48, empty 0, misrooted 0, unsafe 0, unparsed 0.

## Risks and blockers

- No blockers or tool installs. The scan reports filesystem shape only; a non-present report is not evidence that a seat is dead, failed, or killed, and dispatch authenticity is not verified (contract: `contract.md:74-81`, `contract.md:108-109`).
- No build, lint, formatter, or broader test suite was run; the requested frozen selftest and live scan were run as recorded above.

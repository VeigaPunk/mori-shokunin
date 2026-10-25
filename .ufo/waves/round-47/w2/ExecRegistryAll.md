# Round 47 w2 — registry falsification

**Attack:** At landed tip `68d66ca53d89be5c34a62f46af7c37449d9f9b63` (T), falsify the registry audit population and the explicit registrations for the two claimed round-47 gates. The audited tool is the committed registry auditor; no lane files were changed.

**Verdict: holds** for the tested registry properties. Both required invocations report `REGISTRY=met`; no finding surfaced.

## Retained evidence

Commands below were run in `/home/vgpnk/Projects/shokunin/mori-shokunin`, with `TMPDIR=/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r47w2-ExecRegistryAll`.

1. `python3 tools/mori-gate-registry.py --rev 68d66ca53d89be5c34a62f46af7c37449d9f9b63 --audit-all` — exit 0. Output: `tables=8`, `mode=population`, `population_digest=bcf5640156bc6003170a53681623c5b167945a51802a6a3429158cb21f0cbb3e`, `registered=40 unregistered=0 no_selftest=0 duplicate=0 wrong_row=0 tables=8`, `REGISTRY=met`. All 40 enumerated entries printed `PASS`; includes `tools/mori-pin-check.py` and the round-44/45 count-c1/c2/c3 tools.
2. `python3 tools/mori-gate-registry.py --rev 68d66ca53d89be5c34a62f46af7c37449d9f9b63 --audit tools/mori-pin-check.py --audit .ufo/waves/round-47/count-c2.py` — exit 0. Output: `audit tools/mori-pin-check.py PASS row='registry pin reconciler (r47, C1)' (8 cells, entry resolves, --selftest argv branch)`; `audit .ufo/waves/round-47/count-c2.py PASS row='r47 tracepoint catalogue (C2)' (8 cells, entry resolves, --selftest argv branch)`; `tables=8`, `registered=2 unregistered=0 no_selftest=0 duplicate=0 wrong_row=0 tables=8`, `REGISTRY=met`.
3. `python3 tools/mori-gate-registry.py --selftest` — exit 0. Exact summary: `GATE_REGISTRY_SELFTEST pass=15 fail=0` (all 15 printed cases PASS, including duplicate-name, comment-only selftest, empty population, and population-mode/digest cases).
4. Independent enumeration cross-check: imported `tools/mori-gate-registry.py` via `importlib.util`, called its `population(repo, T)`, and hashed sorted newline-joined paths — output `count 40`, digest `bcf5640156bc6003170a53681623c5b167945a51802a6a3429158cb21f0cbb3e`, matching audit-all.
5. Read-only revision checks: `git rev-parse --verify` resolved T, entering tip E `2d85e33d14198d388fd3cda9cc15ec07e57e7a53`, and freeze F `63eecf2738db96f46b0bd02b1b2dfd66787493d0` to the same respective commit ids supplied in the assignment.

## Scope and limits

No edits to lane implementation files. The audit establishes registration, row shape, resolvable entries, self-test branch presence, and registry-wide duplicate/wrong-row counters for the gate's declared population; it does not establish correctness of gate logic or independently validate C1/C2 scoring. No tool was installed. UNVERIFIED: external host state and all properties not covered by the registry auditor.

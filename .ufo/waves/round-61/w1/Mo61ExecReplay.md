# Mo61ExecReplay — frozen counter replay

Scratch: `/fast/scratch/hyaku/mori-r61/Mo61ExecReplay/` (temporary run directories removed before handoff). Disk guard status was green: `/tmp` 24% used / 97.5G free; `/fast/scratch/hyaku` 50% used / 403.9G free. No tools installed.

## Results

All controls reproduce the committed control output byte-for-byte after accounting for the recorded `rc=1` trailer. Invocation used each `count-cN.py 325f7e639916fcbc77fa2ec7475951a1b86bb1cb --repo /home/vgpnk/Projects/shokunin/mori-shokunin --scratch <scratch>` and C1 additionally `--manifest /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-61/gate-manifest.json`.

- **C1:** exit 1; output begins `C1=unmet gates=25 registered=0 missing=25 ...`. Matches `evidence/control-c1-do-nothing.txt:1-2` (line 1 is rendered truncated in reader; exact stable prefix). Selftest run from lane cwd with `--repo`/`--scratch`: exit 0, `C1_SELFTEST pass=6 fail=0`; output matches committed `evidence/selftest-c1.txt:1-8` exactly.
- **C2:** exit 1; exact output `C2=unmet pointers=47 rows=0 same=0 moved=0 changed=0 quotes_ok=0 spans_ok=0 sources=0 failed=entry_absent rev=325f7e639916fcbc77fa2ec7475951a1b86bb1cb`. Matches `evidence/control-c2-do-nothing.txt:1-2` modulo its `rc=1` trailer. With default selftest floor 40, selftest exits 1 (`C2_SELFTEST pass=9 fail=1`; good case fails `pointer_floor:6<40`). This is not committed-evidence-equivalent. Explicit `--floor 6` yields exit 0 and `C2_SELFTEST pass=10 fail=0`; all case lines match expected `evidence/selftest-c2.txt:1-11`, except the expected evidence includes the `rc=0` trailer while stdout does not. Thus the declared synthetic fixture's six pointers require a floor override; record as drift from the default-floor replay, not a frozen counter or evidence modification.
- **C3:** exit 1; exact output `C3=unmet r60hole=ok r61repair=ok blobrefusal=ok expectpin=ok livepins=FAIL cases=5 failed=r61 counters absent or sha pin mismatch at rev rev=325f7e639916fcbc77fa2ec7475951a1b86bb1cb`. Matches `evidence/control-c3-do-nothing.txt:1-2` modulo `rc=1`. Selftest must run with cwd `/home/vgpnk/Projects/shokunin/mori-shokunin` (its source at `count-c3.py:216-218` reads `Path(os.getcwd()) / R61_C1/C2`); then exit 0 and `C3_SELFTEST pass=8 fail=0`, exact stdout match to `evidence/selftest-c3.txt:1-9`.

## Replay caveat / finding

The prescribed C2 selftest command without `--floor` does **not** replay the frozen selftest receipt: the counter's default floor is 40 while its synthetic good case has six pointers. `count-c2.py:201,276-278,291-297` show selftest receives the configured floor and default is retained absent an override. `--floor 6` makes all ten cases pass and matches the frozen case output. No frozen files or repository/VCS state changed.

Initial attempt ran from fleet-root cwd and revealed C3's cwd-sensitive selftest path; reruns from lane cwd resolved it. All commands ran read-only; no build/lint/test suite was invoked.
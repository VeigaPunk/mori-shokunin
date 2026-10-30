# Mo61ExecC3Run — C3 falsification

## Findings

C3 does **not** meet on any requested revision. The freeze and entering outputs are byte-identical except for `rev`, and differ from the committed do-nothing control in the `r60hole` result and failure reason. Consequently, requested control equivalence and red-before behavior are falsified. Do not infer the C3 claim met.

The separately pinned r60 artifact itself is intact: `git -C /home/vgpnk/Projects/shokunin/mori-shokunin show ac496c7cde8cad965079858accae3bedfe4a73f2:.ufo/waves/round-60/count-c3.py | sha256sum` returned `fabde06c9d0a94a8487e5de45be3e413f6084816fb0507a71fd335bad5153514`.

## Exact run evidence

Command for each run: `TMPDIR=/fast/scratch/hyaku/mori-r61/Mo61ExecC3Run python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-61/count-c3.py REV --scratch /fast/scratch/hyaku/mori-r61/Mo61ExecC3Run`.

- Freeze `7370a731abcafc4c803111de7c22cd6264d63be1`: `C3=unmet r60hole=FAIL r61repair=ok blobrefusal=ok expectpin=ok livepins=FAIL cases=5 failed=r60 bytes lost or hole absent (red-before unfaithful);r61 counters absent or sha pin mismatch at rev rev=7370a731abcafc4c803111de7c22cd6264d63be1` (exit 1).
- Fresh lane tip (`git rev-parse HEAD` returned the same freeze hash): identical output (exit 1).
- Entering revision `325f7e639916fcbc77fa2ec7475951a1b86bb1cb`: `C3=unmet r60hole=FAIL r61repair=ok blobrefusal=ok expectpin=ok livepins=FAIL cases=5 failed=r60 bytes lost or hole absent (red-before unfaithful);r61 counters absent or sha pin mismatch at rev rev=325f7e639916fcbc77fa2ec7475951a1b86bb1cb` (exit 1).
- Frozen receipt `.ufo/waves/round-61/evidence/control-c3-do-nothing.txt:1-2` instead records `C3=unmet r60hole=ok r61repair=ok blobrefusal=ok expectpin=ok livepins=FAIL cases=5 failed=r61 counters absent or sha pin mismatch at rev rev=325f7e639916fcbc77fa2ec7475951a1b86bb1cb` and `rc=1`.

Thus removing `rev=` from the actual entering output does **not** produce the frozen control: `r60hole=FAIL` vs `ok`, and an additional failure explanation is emitted.

## Supporting pointers

- `count-c3.py:38-40`: pinned r60 revision and sha.
- `count-c3.py:87-103`: r60 bytes are rejected on sha mismatch; then static hole/token checks run.
- `count-c3.py:156-163`: live C1/C2 pins are checked against requested revision.
- `count-c3.py:175-198`: arm aggregation and output formatting.
- `evidence/selftest-c3.txt:1-10`: frozen selftest receipt reports pass=8 fail=0, including its r60 real-bytes case; this does not override the live revision-run mismatch.

## Environment / cleanup

Disk guard status before runs: `/fast/scratch/hyaku` 50% used, 408.7G free. No tools installed or updated. Scratch used only at `/fast/scratch/hyaku/mori-r61/Mo61ExecC3Run` and removed after saving this report.

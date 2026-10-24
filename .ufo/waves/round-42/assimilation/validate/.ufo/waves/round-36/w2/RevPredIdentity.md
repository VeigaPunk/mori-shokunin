measured 2026-10-23

# RevPredIdentity — mori round 36 wave 2

Attack: post-landing byte-identity of frozen P-C1/P-C2, and each counter's first stdout line.

## Findings

None. Both counter predicates match their contract sentences byte-for-byte and with whitespace collapsed. Both smoke runs print the correct sentence as stdout line 1. No C1 freshness-admission claim is inferred.

## Evidence

- Landed revision: command `git rev-parse HEAD` in the lane repo → `bf0df77fee4b6ef54a90aea09335c7617f125151`.
- Source anchors: canonical P-C1/P-C2 are `contract.md:21` / `contract.md:23`; literals are `count-c1.py:50-56` / `count-c2.py:32-38`; the first-output print calls are `count-c1.py:669` / `count-c2.py:656`.
- Extracted contract and both counters using `git show bf0df77fee4b6ef54a90aea09335c7617f125151:<path>` into the permitted scratch directory. `sha256sum` output: contract `065a17b523b29840df8f1d516ca50eedb0da5e7d614198567439514a099dd93b`; count-c1 `86dd3b7ab2d2563bbc811e83717b35dfea3d69717dab4d41d454f8b87c8764c0`; count-c2 `c7edaacfff029c2055bee6ddda42ff6f5c040dad7fbac81e9d169602edcbac34`.
- Comparison command: Python `ast.parse` + `ast.literal_eval` of each `PREDICATE` in those extracted counters, compared to the matching `P-C1:` / `P-C2:` line in the extracted contract; whitespace collapse was `''.join(text.split())`. Observed output:
  - `C1: exact=True; whitespace_collapsed=True; contract_chars=386; predicate_chars=386`
  - `C2: exact=True; whitespace_collapsed=True; contract_chars=351; predicate_chars=351`
- Smoke command: `python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c1.py 6bd57097 --tool /bin/false --seed 1`. Stdout line 1 was exactly: `P-C1: at revision R, tools/mori-source-drift.py classifies every row of a 40-row blind fixture drawn at run time exactly as the counter's hidden truth, and on the lane's own corpus/SOURCES.md at R it agrees with the counter's independent live oracle on every row the oracle classified, with at least 10 oracle-fetched rows including at least one oracle-fresh and one oracle-drifted row.` Run ended `C1=unmet`, exit 1, as expected for the false-tool control.
- Smoke command: `python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c2.py 6bd57097 --tool /bin/false --seed 1`. Stdout line 1 was exactly: `P-C2: at revision R, tools/mori-sources-appendonly.py prints exactly the counter's hidden truth for ids, deleted, superseded and round_changed on each of 24 sandbox SOURCES.md histories drawn at run time, and on the lane's own history (rev 6bd57097, round base f10a320d) it prints exactly the counter's independent oracle, which lists at least one id.` Run ended `C2=unmet`, exit 1, as expected for the false-tool control.

## Residual risk / verification gaps

This scoped check verifies predicate identity and first-line printing only; it does not re-evaluate scored C1/C2 behavior or imply a freshness verdict/admission for C1. No tool was installed.

VERDICT: PASS (no defect found)

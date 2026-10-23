# C2 receipt audit — RevC2Receipt

**Attacks:** `evidence/c2-after.txt` (C2 receipt); no C1 freshness inference is assessed.

## Findings

None. Every scoped check passed.

## Verification evidence

1. **Predicate identity.** Byte comparison command:
   ```sh
   diff <(sed -n '1p' .ufo/waves/round-36/evidence/c2-after.txt) <(sed -n '23p' .ufo/waves/round-36/contract.md) && echo 'P-C2 LINE: BYTE-IDENTICAL'
   ```
   Observed output: `P-C2 LINE: BYTE-IDENTICAL`.

2. **Frozen counter hash.** Command: `sha256sum .ufo/waves/round-36/count-c2.py`.
   Observed output: `c7edaacfff029c2055bee6ddda42ff6f5c040dad7fbac81e9d169602edcbac34  .ufo/waves/round-36/count-c2.py`.
   This equals the `count-c2.py` pin on `evidence/freeze-v2.txt:4` (`c7edaacfff029c2055bee6ddda42ff6f5c040dad7fbac81e9d169602edcbac34`). The committed counter blob at `bf0df77fee4b6ef54a90aea09335c7617f125151` hashed to the same value.

3. **Receipt contents, coverage, and visible completeness.** Read all of `evidence/c2-after.txt`; it contains these nine complete lines:
   ```text
   P-C2: at revision R, tools/mori-sources-appendonly.py prints exactly the counter's hidden truth for ids, deleted, superseded and round_changed on each of 24 sandbox SOURCES.md histories drawn at run time, and on the lane's own history (rev 6bd57097, round base f10a320d) it prints exactly the counter's independent oracle, which lists at least one id.
   tool: /tmp/mori-c2-pdznuaps/mori-sources-appendonly.py
   blind arm: 24/24 sandbox histories matched the hidden truth (1.6s; coverage: deletions=22 changed-back=17 superseded=10)
   real arm: pass (0.2s)
     tool:   appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]
     oracle: appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]
     tool exit=1
   C2=met
   seed=15440749816798970567
   ```
   `wc -l -L .ufo/waves/round-36/evidence/c2-after.txt` observed `9 351 .ufo/waves/round-36/evidence/c2-after.txt`; the complete read showed no visibly truncated lines, and the seed is present. Blind coverage exceeds all thresholds (deletions 22 ≥ 12, changed-back 17 ≥ 12, superseded 10 ≥ 1).

4. **Tool/oracle byte equality.** Command:
   ```sh
   diff <(sed -n '5p' .ufo/waves/round-36/evidence/c2-after.txt | sed 's/^  tool:   //') <(sed -n '6p' .ufo/waves/round-36/evidence/c2-after.txt | sed 's/^  oracle: //') && echo 'TOOL vs ORACLE: BYTE-IDENTICAL'
   ```
   Observed output: `TOOL vs ORACLE: BYTE-IDENTICAL`. The identical summary includes violations and all four lists (`ids`, `deleted`, `superseded`, `round_changed`).

5. **Frozen-seed counter replay and exit.** Command:
   ```sh
   python3 .ufo/waves/round-36/count-c2.py bf0df77fee4b6ef54a90aea09335c7617f125151 --seed 15440749816798970567; printf 'counter_exit=%s\n' "$?"
   ```
   Observed output:
   ```text
   P-C2: at revision R, tools/mori-sources-appendonly.py prints exactly the counter's hidden truth for ids, deleted, superseded and round_changed on each of 24 sandbox SOURCES.md histories drawn at run time, and on the lane's own history (rev 6bd57097, round base f10a320d) it prints exactly the counter's independent oracle, which lists at least one id.
   tool: /tmp/mori-c2-y5km15d1/mori-sources-appendonly.py
   blind arm: 24/24 sandbox histories matched the hidden truth (4.2s; coverage: deletions=22 changed-back=17 superseded=10)
   real arm: pass (0.3s)
     tool:   appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]
     oracle: appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]
     tool exit=1
   C2=met
   seed=15440749816798970567
   counter_exit=0
   ```
   The `tool exit=1` is the tested gate's exit status, not the counter's: contract §C2 says a gate run with `--round-base` exits 1 when `round_changed` is nonempty, and the matching output has `round_changed=[S182,S193]`. Counter replay itself exited 0 (`C2=met`).

## Residual risk and verification gaps

No actionable gap in this receipt scope. The counter replay used the receipt's fixed seed; it confirms the recorded run and is not a separate fresh-seed sample. No tools were installed.

VERDICT: PASS

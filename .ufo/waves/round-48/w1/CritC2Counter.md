# C2 counterattack — CritC2Counter (w1)

## Counterexample

**HTML script/template text passes as located quote depth.** The counter's `normalise()` removes tags with `<[^>]+>` and collapses whitespace, but leaves script/style element contents intact (count-c2.py:59–62). `evaluate()` then searches the full normalized copy, not rendered/documentation text (lines 164–165). I built an in-memory entry using eight 6–10-word script/config fragments from the pinned xfs_quota, quotactl, and Aliyun copies. Its claims all assert unrelated quota observability facts. Each row otherwise follows the counter's expected structure, uses its frozen source URL/S-id, and each source row is mined/opened/used-by. The result is `C2=met claims=8 located=8 quote_missing=0 bad_rows=0 sources=3 source_rows=ok pins=ok provenance=ok`.

Representative located strings include the man7 Statcounter/Google Analytics JavaScript, Aliyun `window.globalData` and `$ACE_TRACKER_CONFIG`, and Aliyun performance-tracking JavaScript. The eight exact fragments and per-fragment evidence are in the harness output below. This is cheap: no quota fact was needed; only the source copies and an otherwise valid table.

**Second, separate known limitation:** replacing the claim-cell text with a generic assertion unrelated to each quote still scores met, as expected from frozen contract lines 82–85. The counter checks quote presence and row/provenance structure, not entailment. This is not a newly discovered counter defect against P-C2; it is a real limit of the specified predicate. The 8-row script example combines both weaknesses so the returned `met` does not represent real depth.

## Evidence (observed)

- `sha256sum .ufo/waves/round-48/count-c2.py corpus/evidence/sources-r48/*` from `/home/vgpnk/Projects/shokunin/mori-shokunin`: counter hash `0055aed101bd60b1267d160520948b8f412753b38c72b6bda17da841734ee561`; four copy hashes matched the four frozen digests in count-c2.py. Exit 0.
- `git rev-parse HEAD` from the lane: `4387cf94b69ddce455051a1ff38e93795c2e6cde` (freeze commit). Exit 0.
- `TMPDIR=/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r48-CritC2Counter python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-48/count-c2.py --selftest`: `C2_SELFTEST pass=22 fail=0`; exit 0.
- `TMPDIR=/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r48-CritC2Counter python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r48-CritC2Counter/scriptattack.py` used the requested import + `COPIES` + in-memory `evaluate()` pattern. Each of the eight fragments printed length 8–10 words and `True` for occurrence in its source's normalized copy; result:

  ```text
  script_tag_content_8             -> MET
      C2=met claims=8 located=8 quote_missing=0 bad_rows=0 sources=3 source_rows=ok pins=ok provenance=ok rev=R
  exit=0
  ```

  A sanity control built with selftest-style ordinary quota quotes also scored met. The scriptattack harness and its other scratch-only helpers are under `.scratch/r48-CritC2Counter/`.
- As a diagnostic only (not a counter edit), the harness monkey-patched normalization to discard `<script>`/`<style>` contents before existing tag stripping, then scored the identical in-memory entry: `C2=unmet claims=8 located=0 quote_missing=8 bad_rows=0 sources=0 source_rows=ok pins=ok provenance=ok rev=R failed=quote_missing,sources_floor`. Exit 0 for the harness; the inner `evaluate()` result is unmet.

## Impacted axes

- **Depth (C2):** direct false positive for an entry with no quota-observability depth work.
- **Calibration:** the reported `C2=met` overstates what the instrument proves; this primarily undermines the depth claim rather than changing any C1 result.

## Smallest safe correction

Exclude non-rendered script/style contents before stripping HTML tags (for example, remove complete `<script ...>...</script>` and `<style ...>...</style>` elements, case-insensitively, before the current tag removal). The in-memory diagnostic shows this kills the demonstrated class while preserving source pins and row checks. Add a selftest arm with at least eight unique template/script-only quotes drawn across three pinned sources and require it to be unmet. This does **not** fix claim/quote entailment; that remains the contract's named limit and would require a separate change to the predicate/review process, not an incidental counter tweak.

## Scope

No counter, source copy, production file, git index, or jj state was changed. Only this report and scratch harness files were written.
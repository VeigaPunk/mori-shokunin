# C2 fresh read-only recount

## Scope and result

Attacked scope: independently recount the retained C2 before/after manifests' failed assertions and case statuses, and compare the entering/delivered census bytes with the named Git revisions. This is a receipt and byte-identity check only, not a behavioral replay or an admission decision.

The recount reproduces **21 → 0 failed assertions**. Case statuses move from **7 match / 5 mismatch** to **12 match / 0 mismatch**. The same 12 case IDs occur on both sides. The five entering mismatches and failed-assertion counts are `git-detached-commit` (5), `git-detached-behind` (4), `git-report-off-branch` (4), `jj-commit-no-bookmark` (5), and `jj-ambient-author` (3). Each is `match` with 0 failed assertions after. The other seven cases match before and after: `git-plain-progress`, `git-detached-at-tip`, `git-report-on-branch`, `git-foreign-author`, `jj-helper-commit`, `jj-sibling-author`, and `git-fallback-head`.

The assertion denominator increased **124 → 134** because the later run includes additional checks for expected finding details; the failed-assertion count is not a distinct-bug count. The lesson records this qualification at `corpus/lessons/round-17.md:126-133`.

## Independent recount command and output

Read-only Python recomputation from the two retained `run-manifest.json` files (not the gate):

```sh
python3 -c 'import collections,json,sys; out=[]; exec("for p in sys.argv[1:]:\n m=json.load(open(p,encoding=\"utf-8\"))\n out.append({\"failed_assertions\":m[\"totals\"][\"failed_assertions\"],\"case_status_counts\":dict(sorted(collections.Counter(c[\"status\"] for c in m[\"cases\"]).items())),\"mismatches\":[[c[\"id\"],c[\"failed_assertions\"]] for c in m[\"cases\"] if c[\"status\"] != \"match\"],\"matches\":[c[\"id\"] for c in m[\"cases\"] if c[\"status\"] == \"match\"]})"); print(json.dumps(out,separators=(",",":")))' /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-17/evidence/jj-before/run-manifest.json /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-17/evidence/jj-after/run-manifest.json; rc=$?; printf 'rc=%s\n' "$rc"; exit "$rc"
```

rc=0. Exact stdout:

```text
[{"failed_assertions":21,"case_status_counts":{"match":7,"mismatch":5},"mismatches":[["git-detached-commit",5],["git-detached-behind",4],["git-report-off-branch",4],["jj-commit-no-bookmark",5],["jj-ambient-author",3]],"matches":["git-plain-progress","git-detached-at-tip","git-report-on-branch","git-foreign-author","jj-helper-commit","jj-sibling-author","git-fallback-head"]},{"failed_assertions":0,"case_status_counts":{"match":12},"mismatches":[],"matches":["git-plain-progress","git-detached-at-tip","git-detached-commit","git-detached-behind","git-report-on-branch","git-report-off-branch","git-foreign-author","jj-helper-commit","jj-commit-no-bookmark","jj-ambient-author","jj-sibling-author","git-fallback-head"]}]
rc=0
```

Independent read-only `jq -s` cross-check also returned rc=0 and the same case-status matrix and failed totals (full per-case output captured during this recount). The existing `evidence/count-c2.json:5-20` records its own earlier count command/output `[21,0]`; it is consistent with these independent calculations.

## Census byte identity

Read-only command executed from `/home/vgpnk/Projects/shokunin/mori-shokunin`:

```sh
printf '%s\n' 'Frozen entering census:'; sha256sum .ufo/waves/round-17/frozen/mori-census.sh; printf '%s\n' 'Entering commit 24526ea census:'; git show 24526ea:tools/mori-census.sh | sha256sum; printf '%s\n' 'Delivered working census:'; sha256sum tools/mori-census.sh; printf '%s\n' 'Measured commit 273aa74 census:'; git show 273aa74ab73701f41fea38ec7bd1c47b4b2bfbc7:tools/mori-census.sh | sha256sum
```

rc=0; stdout:

```text
Frozen entering census:
f1f8d1b62bb617bbcc4664057ab807d3fed8c275b7aabbdf7b373323c5501ff7  .ufo/waves/round-17/frozen/mori-census.sh
Entering commit 24526ea census:
f1f8d1b62bb617bbcc4664057ab807d3fed8c275b7aabbdf7b373323c5501ff7  -
Delivered working census:
12e8e2d960c2d4d1ea780787c75c0125ec51adf434c93eb169ab0a4066236d85  tools/mori-census.sh
Measured commit 273aa74 census:
12e8e2d960c2d4d1ea780787c75c0125ec51adf434c93eb169ab0a4066236d85  -
```

Both pairs are byte-identical. They match the pinned frozen and delivered census digests in `.ufo/waves/round-17/PINNED_INPUTS.json:3-7,14` (measured commit `273aa74ab73701f41fea38ec7bd1c47b4b2bfbc7`, branch ref `refs/heads/master`). The retained before/after gate receipts both record that measured commit and unchanged branch tip: `evidence/c2-before.json:15-21`, `evidence/c2-after.json:15-21`. Their captured gate summaries are respectively 12 cases / 7 match / 5 mismatch / 124 assertions / 21 failed (rc 1), then 12 / 12 match / 0 mismatch / 134 assertions / 0 failed (rc 0); no gate was run for this recount.

Case IDs/statuses and per-case failures are in `evidence/jj-before/run-manifest.json:38-1234` and `evidence/jj-after/run-manifest.json:38-1269`. The count receipt is `evidence/count-c2.json:5-20`; contract scope is `.ufo/waves/round-17/contract.md:88-102,122-123`.

## Limits, blockers, and changes

- No recount discrepancy or blocker observed for this attacked scope.
- This only verifies arithmetic and input-byte identity of retained evidence; it does not independently establish sandbox fidelity, assertion semantics, or behavior outside the 12 recorded scenarios. No gate, selftest, build, lint, or other test was run.
- No tool was installed or updated.
- Only this assigned report file was written: `.ufo/waves/round-17/falsify/CountC2.md`.

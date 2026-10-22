holds — no-harm at f2de0ee: retention metric is still 4 with byte-identical unallowlisted hits, and the QUALITY 82 host-identifier grep finds zero hits across all 58 files added since 6ebd518f.

# RetentionAtTip — wave-2 falsification of no-harm

Attacked: `tools/mori-retention-gate.py scan` at f2de0eedcd60d2e354da75265ea6122bc3896073 vs the round-28 baseline
`.ufo/waves/round-28/evidence/base-retention.txt`, and the QUALITY 82 lint over every file added since 6ebd518f.

## Check 1 — retention scan at the attack tip

Command (run verbatim, cwd `/home/vgpnk/Projects/shokunin/mori-shokunin`):

```
python3 -I -B tools/mori-retention-gate.py scan --repo /home/vgpnk/Projects/shokunin/mori-shokunin --rev f2de0eedcd60d2e354da75265ea6122bc3896073 --policy .ufo/waves/round-18/frozen/c1-policy.json --allowlist corpus/evidence/retention-allowlist.json
```

- Exit 1, `"commit": "f2de0eedcd60d2e354da75265ea6122bc3896073"`, `"metric": 4` — identical to the baseline receipt
  `.ufo/waves/round-28/evidence/base-retention.txt:13-14` (exit 1, metric 4 at 6ebd518f).
- Parsed both JSON lines and compared `unallowlisted_hits` element-wise: `unallowlisted_equal True`,
  `new_unallowlisted []`. The four hits are the same pre-existing entries in
  `.ufo/waves/round-20/falsify/NoHarmRun/rg/.ufo/waves/round-18/frozen/c1-policy.json` (classes R2, R5, R6, R8 on the
  same lines and line_sha256 values as at base) — a vendored copy of the round-18 policy inside round-20 falsify
  evidence, not introduced this round.
- `policy_sha256` is `db06e9810bbfd243fb0a753a46960573df39083ea90174ce463cf2a0ab523128` at both revisions
  (base-retention.txt:9), so the comparison is same-policy.
- `"warnings": []`, `forbidden_allowlist`: [] — nothing silently suppressed at tip.
- Net: the unallowlisted metric did not rise (4 == 4) and no new unallowlisted line appeared. The added-file set is
  invisible to the scan.

## Check 2 — QUALITY 82 lint of files added since 6ebd518f

Criterion text (git show f2de0ee:corpus/QUALITY.md:378): before first commit, seat output is linted with
`grep -nE 'user-[0-9]{3,}\.slice|user@[0-9]{3,}\.service|\bpid[ =:]*[0-9]{3,}|\buid[ =:]+[0-9]{3,}'`; only values
read from this host need redaction (fixtures and upstream format strings do not).

- File set: `git diff --name-only --diff-filter=A 6ebd518f..f2de0ee` → 58 files; `git diff --name-status -M
  --diff-filter=RA` shows 0 renames, so no added content hides behind a rename record.
- Method: linted committed bytes (`git show f2de0ee:<path>`) of each of the 58 files, counting matches only.
- Result: zero hits in every added file, including the seven upstream earlyoom sources landed at the lane root
  (`MANPAGE.md`, `base.c`, `main.c`, `meminfo.c`, `oom_kill.c`, `sd-main.c`, `user@.service.in`) — none of their
  lines match the numeric-identifier patterns, and the unit template name itself does not match
  `user@[0-9]{3,}\.service` (its `@` is followed by a literal, not digits).
- Note on the seven root files: they look odd at the lane root but are intentional — lesson
  `corpus/lessons/round-28.md` M2 records them as the round-27 fleet-root fetches, "copied byte-exact to the lane
  root" with the fleet copies deleted (lesson line 40, disposition). Their blobs differ from the round-27 fleet
  copies cited in `evidence/misroot-before.txt` (e.g. `main.c` tip blob 780f8125 vs cited sha prefix 08656b0b), which
  is consistent with a re-fetched/copied landing in commit 763d346 rather than a leftover stray; the after-receipt
  `evidence/misroot-after.txt` shows `misroot_hits=0` at the fleet root.

## Residual risk / gaps

- The lint counts hits; classification as host-value vs upstream-format-string never arose (zero hits), so nothing
  needed the Q82 exemption judgment.
- Scope is files added since 6ebd518f (58). Modified files and other lanes were not linted.
- The retention scan remains blind to uid/pid digits by design (QUALITY.md:378); that gap is covered only by the
  per-report grep, which passed for the added set.
- I did not write outside my report; no installs were needed (python3, git, grep already present).

Verification exercised: scan run at tip (exit 1, JSON parsed); baseline JSON parsed from committed receipt;
element-wise hit comparison; 58/58 added files linted against committed blobs; rename check.

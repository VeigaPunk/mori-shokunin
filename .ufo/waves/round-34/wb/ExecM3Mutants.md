measured 2026-10-23T07:50:13Z
# ExecM3Mutants — counter sensitivity to rule-order and parse mutants

Attacks: draft mistake M3 (`/fast/scratch/hyaku/mori-r34/a3-L1/drafts/corpus_lessons_round-34.md:88-94`), which
claims the frozen counter misses R3 class-order swaps, an R5 bad-line/absent swap, short-line handling and
bare-hex acceptance. I rebuilt each shape myself; wave-A files were not used as evidence.

Scratch root **S** = `/fast/scratch/hyaku/mori-r34/a3-ExecM3Mutants`; lane **L** = `/home/vgpnk/Projects/shokunin/mori-shokunin`.

## Sandbox and baseline

- `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone --no-hardlinks L S/lane` → `done.`, then
  `git checkout -q fd2521351c6cef47384aef30afbe1e4db7e6912e`; `rev-parse HEAD` = `fd2521351c…6912e`, worktree clean.
- Pristine tool (`S/lane/tools/mori-disk-rate.py`) SHA-256 `370932deb525b95135f0c30e4caaf2666b95c6feeffe76b70f06b48c09caa74b`.
- Frozen counter SHA-256 `c14c3494d7356fa7c619a0e30c10cd9b71baa99eb0fb74cfd34c7f21b3b181e2`; frozen contract
  `695c8412769da278932b44198649853c140d0eeda88e7591f71bc2950765cc11`. Neither was changed.
- Pristine bracket, exact invocation
  `timeout 600 python3 L/.ufo/waves/round-34/count-c1-a1.py fd2521351c6cef47384aef30afbe1e4db7e6912e --repo S/lane --seed {1,20261023}`:
  both runs `fixed_pass=12/12 random_pass=300/300`, `coverage=ok`, `live=ok`, `C1=met`, exit 0
  (`S/logs/pristine-seed1.txt:3-6`, `S/logs/pristine-seed20261023.txt:3-6`).

## Method

Each mutant is one commit on its own branch off `fd252135`, only `tools/mori-disk-rate.py` touched; mutants were
scored with the unchanged counter at seed 1 and at fresh seed 20261023 (300 random scenarios, no `--random` override).
Mutant tool bytes were extracted with `git show <rev>:tools/mori-disk-rate.py` (`S/tools/*.py`, hashes below).

| ID | Mutation (mutant line numbers) | Commit | Mutant tool SHA-256 | seed 1 | seed 20261023 | Verdict |
|---|---|---|---|---|---|---|
| (a) | R3: stacked check moved above partition check, 192-196 | `22db68a3bf…` | `ce820fa44a3e02c5df09fb3ae4e6387e6e1694a107f2d96efe55ad588e84e185` | 300/300 met | 300/300 met | survived |
| (b) | R3: disk check moved above stacked check, 192-198 | `ca7766777a…` | `f4bcf51285f5038092b7f1520d4780a293f5aafd8a5363f846e44b0547abcf4b` | 300/300 met | 300/300 met | survived |
| (c) | R5: absent check moved above bad-line check, 212-217 | `03e4cd7d85…` | `1c0433841d7e0c70d5607646b65997f3573d106f8ca39196fab105ba51dbfdd2` | 300/300 met | 300/300 met | survived |
| (d) | R2: any 3-13-token line accepted; missing token 10 defaults to 0 sectors, 99,107-108 | `1d80fc6304…` | `7dbbc51277f30f59e9b2e22616a467c1e2a5ceb19161df7841f51a21e8abf4a6` | 274/300 unmet | 274/300 unmet | killed |
| (e) | R2: `0x`-prefixed and bare hex digit tokens accepted, token 10 parsed base 16, 87,107-108 | `27a2d2831b…` | `eddab5c9373cf6923fc8c4469aef65e84b5d224679c87cbd8bd07f258320d438` | 273/300 unmet | 282/300 unmet | killed |
| (d2) | control: only 10-13-token lines accepted, 99 | `6fabcc99f1…` | `f6f3170aed881d23d8ec0fbbd9eaabbe6ad81cde9d8a7aecdd9dfad453cda3be` | 280/300 unmet | 283/300 unmet | killed |
| (e2) | control: only bare hex (`ff`), 87,107-108 | `3424f2b7f0…` | `db910d093a61c594d7a9f9f7f7e1f175182ea4c36042586dd0c6fc4fddb6762b` | 300/300 met | 300/300 met | survived |
| (f) | control: a two-token line marks its second token malformed, 96-99 | `65cea53a84…` | `b1704d96c37749f690229a09fc0e86b264d6a8c7e9ffdb1586b392c952eff5c9` | 300/300 met | 300/300 met | survived |

Killed-run receipts (exit 1 each): `S/logs/m-d-shortline-valid-seed1.txt:3,6-7` (`random_pass=274/300`),
`…-seed20261023.txt:3,6-7`; `S/logs/m-e-hex-digits-seed1.txt:3,6-7` (`273/300`), `…-seed20261023.txt:3,6-7`
(`282/300`); `S/logs/m-d2-short10-13-seed1.txt:3,6-7` (`280/300`), fresh `…:3,6-7` (`283/300`). Survivor receipts:
`S/logs/m-a-part-stacked-seed1.txt:3-6`, `S/logs/m-b-stacked-disk-seed1.txt:3-6`,
`S/logs/m-c-badline-absent-seed1.txt:3-6`, `S/logs/m-e2-bare-hex-seed1.txt:3-6`, `S/logs/m-f-twotoken-seed1.txt:3-6`
(each fresh-seed twin has the same 3-6 shape). All runs printed `coverage=ok live=ok`; the live arm never
distinguished these mutants on this host.

## Direct witnesses (pristine vs mutant, same inputs)

Fixtures built by `S/witness_setup.py`; command per case
`timeout 20 python3 S/tools/{pristine,<mutant>}.py --a S/<w>/samples/a.diskstats --b S/<w>/samples/b.diskstats --sysfs S/<w>/sys --interval-ms 1000`
(exit 0 both sides; stderr empty). Sample file bytes are in each `S/<w>/samples/`.

**(a) partition↔stacked.** `sys/class/block/probe/` holds a `partition` file and `slaves/child`; samples
`8 0 probe 0 0 0 0 0 0 100 0 0 0 0` / `… 200 …`.
pristine `S/witnesses/w-a-pristine.json`:
`{"devices": {"probe": {"class": "partition", "state": "ok", "write_Bps": 51200}}, "host_basis": [], "host_write_Bps": null, "interval_ms": 1000}`;
mutant `S/witnesses/w-a-a.json`:
`{"devices": {"probe": {"class": "stacked", "state": "ok", "write_Bps": 51200}}, "host_basis": [], "host_write_Bps": null, "interval_ms": 1000}`.

**(b) stacked↔disk.** `probe/` holds a `device` file and `slaves/child`; same samples.
pristine `S/witnesses/w-b-pristine.json`:
`{"devices": {"probe": {"class": "stacked", "state": "ok", "write_Bps": 51200}}, "host_basis": [], "host_write_Bps": null, "interval_ms": 1000}`;
mutant `S/witnesses/w-b-b.json`:
`{"devices": {"probe": {"class": "disk", "state": "ok", "write_Bps": 51200}}, "host_basis": ["probe"], "host_write_Bps": 51200, "interval_ms": 1000}`.

**(c) bad-line↔absent.** A = 13-token line `8 0 probe 0 0 0 0 0 0 100 0 0 0` plus a valid 14-token `okdev` line
(sectors 100); B = the `okdev` line only (sectors 102). `probe/` has no marker (virtual); `okdev/` has `device`.
pristine `S/witnesses/w-c-pristine.json`:
`{"devices": {"okdev": {"class": "disk", "state": "ok", "write_Bps": 1024}, "probe": {"class": "virtual", "state": "bad-line", "write_Bps": null}}, "host_basis": ["okdev"], "host_write_Bps": 1024, "interval_ms": 1000}`;
mutant `S/witnesses/w-c-c.json`: the same with `"probe": {… "state": "absent" …}`.

**(e2) bare-hex control.** `probe/` has `device`; samples `8 0 probe 0 ff 0 0 0 0 100 0 0 0 0` / `… 102 …`.
pristine `S/witnesses/w-e2-pristine.json`:
`{"devices": {"probe": {"class": "disk", "state": "bad-line", "write_Bps": null}}, "host_basis": ["probe"], "host_write_Bps": null, "interval_ms": 1000}`;
mutant `S/witnesses/w-e2-e2.json`:
`{"devices": {"probe": {"class": "disk", "state": "ok", "write_Bps": 1024}}, "host_basis": ["probe"], "host_write_Bps": 1024, "interval_ms": 1000}`.

**(f) two-token control.** `probe/` has `device`; A = the 14-token line (sectors 100) plus `8 probe`; B = sectors 200.
pristine `S/witnesses/w-f-pristine.json`:
`{"devices": {"probe": {"class": "disk", "state": "ok", "write_Bps": 51200}}, "host_basis": ["probe"], "host_write_Bps": 51200, "interval_ms": 1000}`;
mutant `S/witnesses/w-f-f.json`:
`{"devices": {"probe": {"class": "disk", "state": "bad-line", "write_Bps": null}}, "host_basis": ["probe"], "host_write_Bps": null, "interval_ms": 1000}`.

## Why each result happened

- (a)/(b): the generator gives a `slaves` directory only when `c != "partition"` (`L/.ufo/waves/round-34/count-c1-a1.py:170-176`),
  creates `partition` only for that class and `device` only for `"disk"`, so no generated fixture carries two class
  markers. The live arm also cannot see it: this host's only non-empty-`slaves` entry is `dm-0`, with no `device`
  and no `partition` marker (`S/logs/host-markers.txt:1`).
- (c): corruption is applied only in the branch where both samples have valid lines (`count-c1-a1.py:189-196`), so a
  malformed line is always paired with a valid one and `absent` can never win on generated input.
- (d)/(d2): the generator's wrong-token-count targets include 10, 11 and 13 (`count-c1-a1.py:134`). Seed 1002
  produces a 10-token `mmcblk0p1` line in A against a valid 20-token B line: mutant reports `ok`/1603611162112,
  oracle `bad-line`/null (`S/logs/causediff.txt:5-8`).
- (e): the generator's malformed spellings include `"0x1f"` (`count-c1-a1.py:141`). Seed 1011 emits it in an
  18-token `zram0` A line: mutant reports `ok`/93056000, oracle `bad-line`/null (`S/logs/causediff.txt:1-4`).
- (e2)/(f): the generator never emits a bare-hex token and never emits a line with fewer than 3 tokens
  (its shortest corruption target is 3, `count-c1-a1.py:134`), so those mutants are invisible to all 312 runs.

## What this does to M3

M3's core statement — the counter does not measure sensitivity to rule order — reproduces: three of three
order/precedence swaps survive both seeds with differing direct witnesses, and every survivor passes the 12 fixed
seeds as well, i.e. the fixed battery alone would never have flagged them. M3's parse clause does not generalise as
written: accepting sub-14-token lines (d, d2) and accepting `0x`-prefixed hex (e) are killed by the random arm. Only
the spellings the generator cannot draw — a bare-hex token `ff` (e2) and a two-token line (f) — survive, which matches
wave-A's MutParse shapes (leads only) but is a property of the generator's alphabet, not of parsing coverage in general.

The correct lesson wording is therefore narrower than drafted: "the counter's random arm covers sub-14 token counts
and `0x` hex, but not bare-hex spellings, sub-3-token lines, overlapping class markers, malformed-only devices, or
R3/R5 ordering". It remains a real M3-class gap; nothing here amends the counter, rules or seed count.

## Verdicts

VERDICT: survived — (a) R3 partition↔stacked order swap (witness `S/witnesses/w-a-{pristine,a}.json`)
VERDICT: survived — (b) R3 stacked↔disk order swap (witness `S/witnesses/w-b-{pristine,b}.json`)
VERDICT: survived — (c) R5 bad-line↔absent precedence swap (witness `S/witnesses/w-c-{pristine,c}.json`)
VERDICT: killed — (d) fewer-than-14-token acceptance (`random_pass=274/300` on both seeds)
VERDICT: killed — (e) hex digits in numeric tokens, including `0x` (`273/300`, `282/300`)
VERDICT: survived — (e2) bare-hex control (witness `S/witnesses/w-e2-{pristine,e2}.json`)
VERDICT: killed — (d2) 10-13-token control (`280/300`, `283/300`)
VERDICT: survived — (f) two-token-line control (witness `S/witnesses/w-f-{pristine,f}.json`)
VERDICT: agree — M3 core: the frozen counter admits R3 order swaps and the R5 bad-line/absent swap, with witnesses
VERDICT: disagree — M3 parse clause as a general claim: literal sub-14 and `0x`-hex acceptance are killed; survival needs generator-invisible spellings

## Containment and limits

- Lane writes: this report only. No lane Git/JJ write, no fleet/sibling write, no writes to `a3-L1/drafts`; every
  sandbox commit is in `S/lane` (branches `m-a-part-stacked`, `m-b-stacked-disk`, `m-c-badline-absent`,
  `m-d-shortline-valid`, `m-e-hex-digits`, `m-d2-short10-13`, `m-e2-bare-hex`, `m-f-twotoken`).
- Every command ran under `timeout` (counter 600 s; witnesses 20 s); no unbounded runs, no subagents, no detached or
  persistent background jobs (the two parallel scoring batches were reaped by `wait` inside one bounded command).
  `pgrep -f a3-ExecM3Mutants` returned no process after the runs; `S/tmp` was emptied.
- Scratch size 353 MB (`/usr/bin/du -sh`, below the 1 GiB allowance). No block device, `/sys`, `/etc`, unit, MCP or
  harness file was written; no load generator was used.
- No tool installs or updates; no pacman command was run. `date`, `git 2.56.0` and `Python 3.14.8` were already present.
- Counter temporary directories and scenario roots under `S/tmp` were removed; fixture trees and logs are retained as
  evidence.

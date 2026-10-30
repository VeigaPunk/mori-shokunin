# Mo61Critic21 — cheapest-met C1 counterexample

## Result and axes

**Construction succeeded:** the frozen counter prints `C1=met gates=25 registered=25` for a single fabricated row. Impacted axis: **calibration**; associated risks: row-identity conflation and false selftest provenance. Admission/rejection remains the canonical judge's decision.

Contract read first: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-61/contract.md`. Counter examined at freeze `7370a731abcafc4c803111de7c22cd6264d63be1`.

## Strongest counterexample: one row, committed real manifest, real gate files

Fixture F was a fresh scratch git repository containing a `git archive` extraction of the freeze tree, with only SKILL.md appended. The manifest was committed in that fixture and read through the counter's default manifest path; no `--manifest` override was needed. All 25 real manifest paths resolve at the freeze revision.

Exact appended lines follow (UTF-8, LF endings). The block beginning at the heading is **997 bytes**; the entry cell is **793 bytes**. This is the smallest construction exercised, not a proof of global byte minimality.

```markdown

## round-61 gate registry (fixture)

| name | kind | entry | verdict map | self-test | pinned values | write scope | owner |
|---|---|---|---|---|---|---|---|
| g | gate | .ufo/waves/round-52/count-c1.py .ufo/waves/round-52/count-c2.py .ufo/waves/round-53/count-c1.py .ufo/waves/round-53/count-c2.py .ufo/waves/round-54/count-c1.py .ufo/waves/round-54/count-c2.py .ufo/waves/round-55/count-c1.py .ufo/waves/round-55/count-c2.py .ufo/waves/round-56/count-c1.py .ufo/waves/round-56/count-c2.py .ufo/waves/round-57/count-c1.py .ufo/waves/round-57/count-c2.py .ufo/waves/round-58/count-c1.py .ufo/waves/round-58/count-c2.py .ufo/waves/round-59/count-c1.py .ufo/waves/round-59/count-c2.py .ufo/waves/round-60/count-c1.py .ufo/waves/round-60/count-c2.py .ufo/waves/round-60/count-c3.py .ufo/waves/round-57/verify-c2-source.py tools/mori-vote-bind.py tools/mori-driver-liveness.py tools/mori-register-check.py tools/mori-settlement-scan.py tools/mori-entry-claims-check.py | x | --selftest | x | x | x |
```

Exact observed invocation and output:

```text
python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-61/count-c1.py 1941a2c10e04057e9073f81a150f1909b1d74e35 --repo /fast/scratch/hyaku/mori-r61/Mo61Critic21/fx-F --scratch /fast/scratch/hyaku/mori-r61/Mo61Critic21/run-Frerun
C1=met gates=25 registered=25 missing=0 thin=0 dup=0 unres=0 noselftest=0 noowner=0 failed=none rev=1941a2c10e04057e9073f81a150f1909b1d74e35
rc=0
```

No gate selftest was invoked by this counter run. `--selftest` in the row is merely a bare string, not an executable command. The other descriptive cells are `x`.

### Mechanism and source pointers

All pointers below refer to `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-61/count-c1.py`:

- **:62–70:** `row_hits()` accepts a path appearing anywhere in the entry string. One row can match all 25 paths.
- **:96–103:** duplicate handling is per manifest path; it does not require distinct row identities across paths.
- **:104–111:** descriptive cells need only be non-empty; selftest needs only contain `--selftest`.
- **:112–118:** resolution checks the manifest path, then increments `registered` once per manifest path, not once per physical row.
- **:40–59:** table discovery does not track Markdown fences/comments.

## Additional exercised constructions

All used committed copies of the actual 25-path manifest, real freeze-tree gate files, and the same frozen counter with explicit `--repo` and `--scratch`. All printed the same zero-failure counters as F and returned rc=0:

| Fixture | Construction | Fixture revision |
|---|---|---|
| A | 25 fabricated rows, one per path; verdict `0 met`, pin `sha 00`, owner `FILLME`; selftest text claims `python3 <path> --selftest → pass=1` | `5756f5ee7aa6403d834f5ac1f7f0ae2bd71fcb4d` |
| C | Same, but entry/selftest name `<path>.orig`, nonexistent files whose names contain the real paths | `d534580b7830291ba1ce4f628739475870d1c8ac` |
| E | Every row names the same other gate's selftest (`.ufo/waves/round-52/count-c1.py`) | `caa85a00eab3e8d45360a9c1cce94953693f4dbc` |
| H | 25 rows inside a fenced code block under `## Mistakes` | `f130256cf1b8287d7da96c2e5efba5c0fa61bbc3` |
| J | 25 rows inside an HTML comment, invisible in rendered Markdown | `0d35ccccc0fa1fdb57dfb4942f154ec6e8989b0b` |
| K | 25 rows indented four spaces as Markdown code | `f5de1bb9e8a24d39874b219e0b9f16e696b30427` |

A manifest-override negative probe naming absent `tools/g.py` correctly returned `C1=unmet ... unres=1 ... failed=unres:tools/g.py`, rc=1. Resolution is not wholly absent; it checks the manifest referent rather than the row's named superstring.

## Selftest provenance: actual r57 gates lack the named mode

The freeze-tree files themselves establish:

- `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-57/count-c1.py:5–9`: reads `sys.argv[1]` as revision. Invoking with `--selftest` returned `C1=unmet rows=0 evidence=bad`, rc=1.
- `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-57/count-c2.py:4–10`: likewise reads `--selftest` as revision. Returned `C2=unmet claims=0 source=bad rev=--selftest`, rc=1.
- `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-57/verify-c2-source.py:4`: unpacks two positional arguments. A sole `--selftest` returned `ValueError: not enough values to unpack (expected 2, got 1)`, rc=1.

These three files contain no `--selftest` literal. Counterexample A nevertheless accepts rows asserting their `--selftest` commands pass.

An initial archive-tree run of r55 count-c1 raised `StopIteration`; a proper shared git clone at the freeze rev returned `C1_SELFTEST pass=44 fail=0`. **The archive failure is not evidence of a broken r55 selftest**: it requires repository history. Other initial flat-layout failures likewise are not relied upon here.

## Contract boundary: defect versus tradeoff

F and A show that `registered=25` does not attest 25 distinct or truthful registrations. However, C1's frozen target explicitly requires non-empty cells and a cell *naming* `--selftest`, not successful execution or truthful pin values. Thus filler cells and unexecuted selftests alone are not proof of violating every literal frozen predicate. Do not conflate this demonstrated cheap-met weakness with an independent adjudication.

C is sharper against the target's entry-path resolution wording: the named `.orig` referents do not exist, while the manifest referents do. J/H/K are sharper against “gate-registry tables”: commented/code examples count as registry content. These are the strongest semantic counterexamples for the judge.

No frozen counter/contract amendment is proposed or applied. Smallest safe correction to the round's interpretation: report C1 as evidence of **syntactic path coverage**, not selftest execution, content truth, or distinct rendered registrations. Preserve these receipts as findings rather than changing frozen predicates.

## Reproduction and hygiene

Fixture recipe exercised: `git -C <lane> archive <freeze>` → extract under seat scratch; append shown bytes; `git -C <fixture> init -q`; add/commit with local `-c user.name=t -c user.email=t@t`; invoke frozen counter with explicit fixture revision, `--repo`, and `--scratch`. Scratch fixture SHAs above are receipts, not surviving lane commits.

Disk guard initially reported `/fast/scratch/hyaku` 370.5G free. One shared clone was used to disambiguate the r55 selftest dependency. Tools installed/updated: none. No lane/fleet VCS mutation or production edits. Only this report was written in the lane.

**Procedure deviations:** fixture mutation commands used explicit `git -C` but the required toplevel assertions were captured after fixture commits rather than before; early exploratory selftest invocations did not uniformly pass `--scratch` (TMPDIR was set for the later in-tree survey). These do not change the observed counter receipts, but the procedure was not fully compliant. Scratch files are removed before yield; all citable evidence is embedded above.

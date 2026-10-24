# ExeDagR

## Result

Re-ran the landed v3 gate against `dag-r` into `.scratch/c11-after-fixture-r-ExeDagR.txt` (kept the existing evidence receipt untouched under the seat write bound). The re-add is not treated as an edit: the v3 output has `superseded=[S008]`, `round_changed=[S008]`, `superseded_as_of=[S008]`, and `stale_supersede=[]`.

The regenerated receipt matches `evidence/c11-after-fixture-r.txt` except for its `command:` line, which names the scratch output path instead of the evidence output path. Against the red v2 receipt, the meaningful verdict differs: red has `superseded=[]`, `superseded_as_of=[]`, `stale_supersede=[]`; v3 includes S008 as-of. Both runs report `EXIT=1` for the fixture.

## Commands and observed outputs

1. Ran:

   ```sh
   python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-40/fixtures/run-c11-dags.py /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-sources-appendonly.py /home/vgpnk/Projects/shokunin/mori-shokunin /home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/c11-after-fixture-r-ExeDagR.txt dag-r
   ```

   Terminal stdout/stderr: none. The generated receipt records:

   ```text
   == linear delete-then-re-add is not an edit (dag-r, --round-base b0=07be6c7f1765)
   appendonly_violations=0 ids=[] deleted=[] superseded=[S008] round_changed=[S008]
   supersede_timing superseded_as_of=[S008] stale_supersede=[]
   EXIT=1
   ```

2. Compared whole files with:

   ```sh
   cmp -s /home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/c11-after-fixture-r-ExeDagR.txt /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-40/evidence/c11-after-fixture-r.txt && printf 'after_receipt=byte-identical\n' || printf 'after_receipt=differs\n'; cmp -s /home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/c11-after-fixture-r-ExeDagR.txt /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-40/evidence/c11-red-readd.txt && printf 'red_receipt=byte-identical\n' || printf 'red_receipt=differs\n'
   ```

   Output:

   ```text
   after_receipt=differs
   red_receipt=differs
   ```

3. Ran both plain comparisons:

   ```sh
   diff -u /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-40/evidence/c11-after-fixture-r.txt /home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/c11-after-fixture-r-ExeDagR.txt; printf 'after_diff_exit=%s\n' "$?"
   diff -u /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-40/evidence/c11-red-readd.txt /home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/c11-after-fixture-r-ExeDagR.txt; printf 'red_diff_exit=%s\n' "$?"
   ```

   The after comparison reported one changed line (only the `command:` output-path argument; the remaining receipt lines match). The red comparison reported four changed lines: `command:`, the P-C9/P-C11 description, and the two verdict lines. The red verdict lines are:

   ```text
   appendonly_violations=0 ids=[] deleted=[] superseded=[] round_changed=[S008]
   supersede_timing superseded_as_of=[] stale_supersede=[]
   EXIT=1
   ```

4. Tried these narrower comparisons, but the installed `diff` rejects `-I`; both commands returned the usage error (`error: unexpected argument '-I' found`, `Usage: diff [OPTION]... FILE1 FILE2`, `For more information, try '--help'.`) and printed exit `2`:

   ```sh
   diff -u -I '^command:' /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-40/evidence/c11-after-fixture-r.txt /home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/c11-after-fixture-r-ExeDagR.txt; printf 'after_content_diff_exit=%s\n' "$?"
   diff -U0 -I '^command:' -I '^P-C[0-9][0-9]*:' /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-40/evidence/c11-red-readd.txt /home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/c11-after-fixture-r-ExeDagR.txt; printf 'red_verdict_diff_exit=%s\n' "$?"
   ```

## Files and scope

- Added this report: `.ufo/waves/round-40/w1/ExeDagR.md`.
- Wrote the regenerated receipt only to `.scratch/c11-after-fixture-r-ExeDagR.txt`; no production/evidence file was modified.
- No tools installed; no build, lint, formatter, or unrelated test was run.

## Risks / blockers

None observed for this `dag-r` receipt. Whole-file byte comparisons naturally differ because the recorded commands name different output files; the generated verdict content matches the existing v3 receipt and contradicts the red v2 verdict as expected.
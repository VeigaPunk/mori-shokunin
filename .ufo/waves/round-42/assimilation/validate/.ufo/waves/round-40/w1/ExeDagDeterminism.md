# ExeDagDeterminism

## Result

Built each P-C11 DAG (`dag-n`, `dag-p`, `dag-r`) twice using the tracked gate module's `_make_dag_repo`, in separate repositories under an isolated `.scratch` root. The two builds returned the same named commit SHA at every key. `cmp -s` returned exit 0 for all nine SHAs containing `corpus/SOURCES.md`; `dag-p/d1` has no registry path in either build. Summary: 10 named SHAs, 9 registry bodies compared, 1 absent in both, all identical.

## Command and successful output

Command (the temporary runner was removed after the run):

```sh
python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r40-dag-determinism.py
```

Output, verbatim:

```text
scratch=/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r40-dag-determinism-ossrw5_0
DAG dag-n (never-edited superseded row is as-of)
  b0 sha=07be6c7f176584f32d5091ad9f911bec7b6e135e cmp -s /home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r40-dag-determinism-ossrw5_0/cmp/dag-n/b0-run1.bin /home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r40-dag-determinism-ossrw5_0/cmp/dag-n/b0-run2.bin -> exit 0; body-sha256=6e27109c5169e13fb7d1f41b9c12eb4f883609d16eb6c24af8c7ff54bfb486db
  n1 sha=f08b861cee2839fd925ebfd5ed724b448e7981de cmp -s /home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r40-dag-determinism-ossrw5_0/cmp/dag-n/n1-run1.bin /home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r40-dag-determinism-ossrw5_0/cmp/dag-n/n1-run2.bin -> exit 0; body-sha256=3c439d3d2f7f0c0e1ebb7c31a2d681760e8ef5decfbd0a6fb0ff5e1ec6c178ca
DAG dag-p (first-parent-lacks-path merge contributes no edits)
  b0 sha=07be6c7f176584f32d5091ad9f911bec7b6e135e cmp -s /home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r40-dag-determinism-ossrw5_0/cmp/dag-p/b0-run1.bin /home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r40-dag-determinism-ossrw5_0/cmp/dag-p/b0-run2.bin -> exit 0; body-sha256=6e27109c5169e13fb7d1f41b9c12eb4f883609d16eb6c24af8c7ff54bfb486db
  s1 sha=ea0be2d40f6b2cf0ba27181e0a445a54d6c8f9f5 cmp -s /home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r40-dag-determinism-ossrw5_0/cmp/dag-p/s1-run1.bin /home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r40-dag-determinism-ossrw5_0/cmp/dag-p/s1-run2.bin -> exit 0; body-sha256=047da4f003dda2969b681af78c813a5e02b9f4579d449fa32514a76d65dc95ab
  d1 sha=cdd8967013e2ce0ae406805f1f56552feb8dda04 body=ABSENT both; cmp=N/A
  m sha=5b672415948fd1cd7df763bd6ae142ba9388e693 cmp -s /home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r40-dag-determinism-ossrw5_0/cmp/dag-p/m-run1.bin /home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r40-dag-determinism-ossrw5_0/cmp/dag-p/m-run2.bin -> exit 0; body-sha256=da3dec30fed6b7358e2738dfd339acb448186bb3a076509f1f627465373acffd
DAG dag-r (linear delete-then-re-add is not an edit)
  b0 sha=07be6c7f176584f32d5091ad9f911bec7b6e135e cmp -s /home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r40-dag-determinism-ossrw5_0/cmp/dag-r/b0-run1.bin /home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r40-dag-determinism-ossrw5_0/cmp/dag-r/b0-run2.bin -> exit 0; body-sha256=6e27109c5169e13fb7d1f41b9c12eb4f883609d16eb6c24af8c7ff54bfb486db
  s1 sha=7cb1c6525fbeedbb6100b731bc8d36fba6353bdd cmp -s /home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r40-dag-determinism-ossrw5_0/cmp/dag-r/s1-run1.bin /home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r40-dag-determinism-ossrw5_0/cmp/dag-r/s1-run2.bin -> exit 0; body-sha256=19e881ae6b0de410b5c7471a3d8e0fd495b3484b00cf8e1f4ebbc8b7ab52dc09
  r1 sha=175577fb6b3350d53bcbaa54ae980625a93498f5 cmp -s /home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r40-dag-determinism-ossrw5_0/cmp/dag-r/r1-run1.bin /home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r40-dag-determinism-ossrw5_0/cmp/dag-r/r1-run2.bin -> exit 0; body-sha256=b262aa14c79f2afdb526bf970b8b670fe7acc2fd64966e4b4914c65aa2ae60ab
  r2 sha=4b65a90c4979c667081379706248b7c65498d8d7 cmp -s /home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r40-dag-determinism-ossrw5_0/cmp/dag-r/r2-run1.bin /home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r40-dag-determinism-ossrw5_0/cmp/dag-r/r2-run2.bin -> exit 0; body-sha256=19e881ae6b0de410b5c7471a3d8e0fd495b3484b00cf8e1f4ebbc8b7ab52dc09
SUMMARY named-shas=10 bodies-compared=9 absent-both=1 all-identical=yes
scratch-cleaned=/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r40-dag-determinism-ossrw5_0
```

An initial invocation of the same command exited 1 after partial comparisons because the temporary runner assumed a different `git cat-file -e` status for the intentionally absent `dag-p/d1` path. I corrected the runner to determine path presence with read-only `git ls-tree`; the successful run above is the completed evidence. No fixture repositories remain.

## Scope and notes

- Persistent file changed: `.ufo/waves/round-40/w1/ExeDagDeterminism.md` only. The temporary runner and both scratch roots were removed.
- No production code, lane Git index/state, or external repository was changed; fixture Git writes were confined to temporary `.scratch` repositories.
- LSP was not available in the exposed tool inventory. I inspected the builder with file reads; no symbol refactor was needed.
- No tools installed. No blockers remain.

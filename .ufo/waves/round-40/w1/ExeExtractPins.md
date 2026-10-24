# Extracted before-instrument pins

## Finding

All three extracted before-instruments are byte-identical to their committed bytes at `bb1f2457`: each streamed-commit SHA-256 equals the extracted file SHA-256.

## Exact commands and outputs

Run from `/home/vgpnk/Projects/shokunin/mori-shokunin`:

Command:
```sh
git show bb1f2457:tools/mori-sources-appendonly.py | sha256sum && sha256sum .ufo/waves/round-40/fixtures/extracted/gate-v2-bb1f2457.py
```
Output:
```text
62cd4132dbe141538371f79723c3caff66670fab9076494cd9cf65efccfc01e7  -
62cd4132dbe141538371f79723c3caff66670fab9076494cd9cf65efccfc01e7  .ufo/waves/round-40/fixtures/extracted/gate-v2-bb1f2457.py
```

Command:
```sh
git show bb1f2457:.ufo/waves/round-39/conform.py | sha256sum && sha256sum .ufo/waves/round-40/fixtures/extracted/conform-v2-r39.py
```
Output:
```text
fe0be179aba9df7150f0b6cdb50a5f9bbdb411efb1263b46ffa6b21d46ef7987  -
fe0be179aba9df7150f0b6cdb50a5f9bbdb411efb1263b46ffa6b21d46ef7987  .ufo/waves/round-40/fixtures/extracted/conform-v2-r39.py
```

Command:
```sh
git show bb1f2457:.ufo/waves/round-39/count-c7.py | sha256sum && sha256sum .ufo/waves/round-40/fixtures/extracted/count-c7-r39.py
```
Output:
```text
b92c65f224a6268a901aa6bc5ad66b499048eaca82b493356eb8e1f324ef0520  -
b92c65f224a6268a901aa6bc5ad66b499048eaca82b493356eb8e1f324ef0520  .ufo/waves/round-40/fixtures/extracted/count-c7-r39.py
```

## Risks and blockers

No mismatch found; no blocker. No build, lint, formatter, or test was run.
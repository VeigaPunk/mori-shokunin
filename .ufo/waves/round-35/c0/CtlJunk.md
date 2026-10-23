# C0 control 3 — junk (`CtlJunk`)

- **Control name:** junk (contract.md controls list item 3: "18 rows with random keys, rounds and paths").
- **What work it skips:** the whole claimed work. The generator never reads the fleet `MANIFEST.json`, never looks up an
  oracle key, never binds a row to a closure commit and never checks an evidence path. Rows are random text plus
  randomly chosen paths that merely exist in the clone's HEAD tree (`git ls-tree -r --name-only HEAD`). If the counter
  passed this, a lane could satisfy C1 by printing 18 table rows of noise.
- **Clone:** `/fast/scratch/hyaku/mori-r35/CtlJunk/clone`, branch `ctl` at frozen lane revision `f2d28711`.
- **Clone commit scored:** `d3586b7c7e8d84af6284d763238bd1fb37dfb987`
- **Counter:** `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-35/count-c1.py` (unmodified frozen file)
- **Counter sha256:** `27b82d71f2f591df1833c8de793201475d8f01735b5ed4edd7b74e389ee18167`
- **Seed:** `350123` (printed by the generator; fixed for reproducibility).
- **Register bytes:** `.ufo/waves/round-35/c0/CtlJunk-register.md` (24 lines, exactly the appended section,
  sha256 `a876dc3b98d0d44ed012fe04285c3929d20f4254cd523b05dabd54c0d8085044`).

## How built

```sh
unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE
mkdir -p /fast/scratch/hyaku/mori-r35/CtlJunk
git clone -q /home/vgpnk/Projects/shokunin/mori-shokunin /fast/scratch/hyaku/mori-r35/CtlJunk/clone
git -C /fast/scratch/hyaku/mori-r35/CtlJunk/clone checkout -q -b ctl f2d28711ee723c969b6c2008d32df498192f9e7b
cd /fast/scratch/hyaku/mori-r35/CtlJunk
timeout 60 python3 gen.py clone 350123        # prints seed=350123, appends the section
cd clone && git -c user.name=ctl -c user.email=ctl@local commit -qam ctl
# scored:
timeout 120 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-35/count-c1.py \
  d3586b7c7e8d84af6284d763238bd1fb37dfb987 --repo /fast/scratch/hyaku/mori-r35/CtlJunk/clone
```

Generator (`/fast/scratch/hyaku/mori-r35/CtlJunk/gen.py`, 48 lines):

```python
#!/usr/bin/env python3
"""C0 control 3 (junk): append `## Capabilities register (junk)` to SCORECARD.md.

Does no evidence lookup and no closure binding: 18 rows whose keys are random
rounds[N].capabilities_added[M] (N 0-600, M 0-3), random round cells 1-40 and
random existing repo paths from `git ls-tree -r --name-only HEAD` as evidence.

Usage: gen.py <clone-repo> [seed]
Prints the seed and writes the appended section to section.md.
"""
import random
import subprocess
import sys

HEADING = "## Capabilities register (junk)"


def main(argv):
    repo = argv[0]
    seed = int(argv[1]) if len(argv) > 1 else 350123
    rng = random.Random(seed)
    print("seed=%d" % seed)
    out = subprocess.run(["git", "-C", repo, "ls-tree", "-r", "--name-only", "HEAD"],
                         capture_output=True, text=True, check=True).stdout.splitlines()
    tok = [p for p in out if p and all(c.isalnum() or c in "._/-" for c in p)]
    lines = [HEADING, "",
             "Junk control: random keys, rounds and paths; no closure binding, no evidence lookup.", "",
             "| key | capability | what it can now do | evidence | first-working round |",
             "|---|---|---|---|---|"]
    for _ in range(18):
        n, m = rng.randint(0, 600), rng.randint(0, 3)
        rnd = rng.randint(1, 40)
        path = rng.choice(tok)
        lines.append("| `rounds[%d].capabilities_added[%d]` | random capability %d | does a random thing | `%s` | %d |"
                     % (n, m, rng.randint(1, 9999), path, rnd))
    section = "\n".join(lines) + "\n"
    with open("section.md", "w") as f:
        f.write(section)
    text = open(repo + "/SCORECARD.md").read()
    with open(repo + "/SCORECARD.md", "w") as f:
        f.write(text + ("\n" if not text.endswith("\n") else "") + section)
    sys.stdout.write(section)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
```

Path filter note: candidate paths are restricted to `git ls-tree` entries whose characters are all alnum or
`._/-`, so a random pick can never break the markdown table cell or the counter's token shape. The pick itself is
uniform over that set — no lookup, no filtering toward artifacts, no knowledge of which paths are strong.

## Full counter stdout

```
row `rounds[482].capabilities_added[0]` extra 
row `rounds[471].capabilities_added[3]` extra 
row `rounds[5].capabilities_added[0]` extra 
row `rounds[434].capabilities_added[0]` extra 
row `rounds[547].capabilities_added[1]` extra 
row `rounds[508].capabilities_added[1]` extra 
row `rounds[367].capabilities_added[0]` extra 
row `rounds[363].capabilities_added[0]` extra 
row `rounds[520].capabilities_added[2]` extra 
row `rounds[398].capabilities_added[2]` extra 
row rounds[476].capabilities_added[1] bad round=9!=28,weak-path:.ufo/waves/round-16/evidence/capability-after/cases/anchor_record_foreign_boot/anchor.json
row `rounds[286].capabilities_added[1]` extra 
row `rounds[508].capabilities_added[1]` extra 
row `rounds[336].capabilities_added[1]` extra 
row `rounds[204].capabilities_added[3]` extra 
row `rounds[8].capabilities_added[1]` extra 
row `rounds[598].capabilities_added[2]` extra 
row `rounds[537].capabilities_added[3]` extra 
row rounds[313].capabilities_added[0] missing
row rounds[339].capabilities_added[0] missing
row rounds[345].capabilities_added[0] missing
row rounds[353].capabilities_added[0] missing
row rounds[386].capabilities_added[0] missing
row rounds[386].capabilities_added[1] missing
row rounds[386].capabilities_added[2] missing
row rounds[398].capabilities_added[0] missing
row rounds[427].capabilities_added[0] missing
row rounds[443].capabilities_added[0] missing
row rounds[443].capabilities_added[1] missing
row rounds[455].capabilities_added[0] missing
row rounds[455].capabilities_added[1] missing
row rounds[462].capabilities_added[0] missing
row rounds[476].capabilities_added[0] missing
row rounds[495].capabilities_added[0] missing
row rounds[495].capabilities_added[1] missing
label=P-C1 rev=d3586b7c7e8d84af6284d763238bd1fb37dfb987 manifest_rev=37b51a243302 register='## Capabilities register (junk)' oracle=18 rows=18 matched=0 missing=17 bad=1 extra=17 mismatches=35 C1=unmet
```

## Result

- **Summary line:** `label=P-C1 rev=d3586b7c7e8d84af6284d763238bd1fb37dfb987 manifest_rev=37b51a243302 register='## Capabilities register (junk)' oracle=18 rows=18 matched=0 missing=17 bad=1 extra=17 mismatches=35 C1=unmet`
- **Exit code:** `1`
- **Verdict:** `unmet` — correct for a skip-the-work control.

## Observations (evidence only, no judgement)

- 17 of 18 random keys missed the oracle entirely and were counted `extra`; all 18 oracle keys except one were
  `missing`. The junk row count (18) did not help: `rows=18` is satisfied while `matched=0`.
- One random key, `rounds[476].capabilities_added[1]`, happened to collide with a real oracle key (24 draws over
  601×4×18 slots). The counter still refused it: the random round cell `9` ≠ closure round `28` and the random
  `.ufo/…` path was `weak-path`. A key collision alone does not buy a `matched` row — the round cell and the
  evidence arm must also hold.
- Two rows drew the same key `rounds[508].capabilities_added[1]`; both were `extra` because that key is not in the
  oracle, so the duplication arm did not fire on this control (it fires via `extra-duplicate` only after a key is in
  the oracle).
- No tool was installed or updated. No process left running. No git/jj write in `/home/vgpnk/Projects/shokunin` or
  the fleet repo; sandbox git only in the clone, with `GIT_DIR`/`GIT_WORK_TREE`/`GIT_INDEX_FILE` unset. Only writes
  inside the lane repo are this report and `CtlJunk-register.md`.

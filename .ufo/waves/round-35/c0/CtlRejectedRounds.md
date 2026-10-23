# Control 7 — rejected-round inclusion (round 35, pre-data C0)

**Control:** C7, "rejected-round inclusion", in two variants.

- **A (additive):** the 18 correct admitted rows (keys, rounds, one strong evidence path each) **plus** the three
  `capabilities_added` rows of **rejected** mori closure round 17 (`MANIFEST.json` `rounds[372]`, `admitted: false`,
  commit `d005cdde0e00…`). 21 rows.
- **B (replacement):** 17 correct admitted rows with `rounds[372].capabilities_added[0]` (rejected) standing in the
  place of the dropped `rounds[313].capabilities_added[0]` (admitted round 12). 18 rows.

**What work it skips:** the admission clause of P-C1 ("… records in `capabilities_added` of an *admitted* mori
closure"). Both variants do the row-building and evidence-binding work honestly — the 18 rows in variant A are all
`matched`, so no lower-bound arm is being dodged — and then claim capability credit for a closure the fleet record
rejects (round 17), with evidence picked by the counter's own strong-path rule so the rows look exactly like legitimate
ones. Variant B additionally buys the rejected row at the price of one admitted row, i.e. it reports a full-size
18-row register while silently swapping provenance.

**Counter run:** `.ufo/waves/round-35/count-c1.py`, frozen file untouched.
`sha256sum` = `27b82d71f2f591df1833c8de793201475d8f01735b5ed4edd7b74e389ee18167` (matches the contract's `27b82d71…`).

## How built (exact commands)

```sh
unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE
mkdir -p /fast/scratch/hyaku/mori-r35/CtlRejectedRounds
cd /fast/scratch/hyaku/mori-r35/CtlRejectedRounds
git clone -q /home/vgpnk/Projects/shokunin/mori-shokunin clone
cd clone && git checkout -q -b ctl-rejected f2d28711ee723c969b6c2008d32df498192f9e7b
# generate the two register sections (script below), then, variant A:
cat ../regA.md >> SCORECARD.md
git -c user.name=ctl -c user.email=ctl@local commit -qam ctl          # -> 5cdfa53acaf98ee1174202ec2a4a0b5ff8f4aa77
# variant B, off the same base:
cd .. && git -C clone checkout -q -b ctl-rejected-b f2d28711ee723c969b6c2008d32df498192f9e7b
cat regB.md >> clone/SCORECARD.md
git -C clone -c user.name=ctl -c user.email=ctl@local commit -qam ctl  # -> 539db5ccd7868d3681ba5a17ec66f31d34bad8b1
# score
timeout 120 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-35/count-c1.py \
  5cdfa53acaf98ee1174202ec2a4a0b5ff8f4aa77 --repo /fast/scratch/hyaku/mori-r35/CtlRejectedRounds/clone
timeout 120 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-35/count-c1.py \
  539db5ccd7868d3681ba5a17ec66f31d34bad8b1 --repo /fast/scratch/hyaku/mori-r35/CtlRejectedRounds/clone
```

Rows were derived by importing the frozen counter and re-using its own helpers (`git`, `show`, `tree_paths`,
`whole_path_in`, `SPOT_RE`, `NAMED_RE`, `ARTIFACT_PREFIXES`, `FIRST_PREV`, `MANIFEST_REV`) to rebuild the oracle and
select, per capability, the first sorted strong path: exists at `f2d28711` and at the closure commit, changed between
the previous mori closure commit and the closure commit, under `tools/`/`corpus/knowledge/`/`corpus/evidence/` or
`corpus/SOURCES.md`, equal to a path the capability string names when it names one, and appearing as a whole path in
the closure record text. The generator below reproduces both saved registers byte-identically
(`regA.md` sha256 `454beb2c0a5527e52ded7e2c5b99934c13f95712d5c5f6a6aa8f1a18d5481d17`,
`regB.md` sha256 `0067a2cd1e65dcbec7cc59d1ee73fecba52e84b99abe2ae3677566f527950fae`; `diff` clean).

```python
import importlib.util, json
F = "/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-35/count-c1.py"
R = "/fast/scratch/hyaku/mori-r35/CtlRejectedRounds/clone"
FL = "/home/vgpnk/Projects/shokunin"
spec = importlib.util.spec_from_file_location("c", F); c = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c)
man = json.loads(c.git(FL, "show", c.MANIFEST_REV + ":MANIFEST.json").stdout)
at_rev = c.tree_paths(R, "f2d28711")
info, prev = {}, c.git(R, "rev-parse", c.FIRST_PREV + "^{commit}").stdout.strip()
for i, r in [(i, r) for i, r in enumerate(man["rounds"]) if r.get("lane") == "mori"]:
    cm = c.git(R, "rev-parse", r["commit"].split("@", 1)[1] + "^{commit}").stdout.strip()
    caps = r.get("capabilities_added") or []
    if caps:
        ch = set(c.git(R, "diff", "--name-only", "--no-renames", prev, cm).stdout.splitlines())
        vt = json.dumps(r.get("verification") or {}, ensure_ascii=False)
        ex = [c.show(R, h, p) for p, h in c.SPOT_RE.findall(vt)]
        ex += [c.git(FL, "show", "%s:%s" % (c.MANIFEST_REV, r["report"]), check=False).stdout] if r.get("report") else []
        ct = vt + "\n" + "\n".join(x for x in ex if x) + "\n" + "\n".join(caps)
        atc = c.tree_paths(R, cm)
        for j, cap in enumerate(caps):
            nm = set(c.NAMED_RE.findall(cap))
            strong = [p for p in sorted(ch) if p in at_rev and p in atc
                      and (p.startswith(c.ARTIFACT_PREFIXES) or p in c.ARTIFACT_FILES)
                      and (not nm or p in nm) and c.whole_path_in(p, ct)]
            info[(i, j)] = (r["round"], cap, r.get("admitted") is True, strong)
    prev = cm
H = ["| key | capability | what it can now do | evidence | first-working round |",
     "| --- | --- | --- | --- | --- |"]
def row(i, j):
    rnd, cap, _a, st = info[(i, j)]
    return "| rounds[%d].capabilities_added[%d] | %s | Demonstrated by the closure that landed it | `%s` | %s |" % (
        i, j, " ".join(cap.split()).replace("|", "/"), st[0], rnd)
adm = [(i, j) for (i, j), v in sorted(info.items()) if v[2]]
rej = [(i, j) for (i, j), v in sorted(info.items()) if not v[2]]
A = ["## Capabilities (controls wave: rejected-round inclusion)"] + H + [row(*k) for k in adm + rej]
B = ["## Capabilities (controls wave: rejected row replaces an admitted row)"] + H + [row(*k) for k in adm[1:] + rej[:1]]
for n, s in (("regA", A), ("regB", B)):
    open("/fast/scratch/hyaku/mori-r35/CtlRejectedRounds/%s.md" % n, "w").write("\n".join(s) + "\n")
```

Generator output: `admitted=18 rejected=3`. Round 17's three capabilities each had **7** strong-path candidates
(`corpus/SOURCES.md` first, sorted); 17 is the only rejected mori closure that carries any `capabilities_added`
(13, 20, 23, 27, 29, 30, 32, 33, 34 carry none), so the rejected pool is exactly these three rows.

## Results

Variant A — clone commit `5cdfa53acaf98ee1174202ec2a4a0b5ff8f4aa77`:

```
row rounds[313].capabilities_added[0] matched
row rounds[339].capabilities_added[0] matched
row rounds[345].capabilities_added[0] matched
row rounds[353].capabilities_added[0] matched
row rounds[386].capabilities_added[0] matched
row rounds[386].capabilities_added[1] matched
row rounds[386].capabilities_added[2] matched
row rounds[398].capabilities_added[0] matched
row rounds[427].capabilities_added[0] matched
row rounds[443].capabilities_added[0] matched
row rounds[443].capabilities_added[1] matched
row rounds[455].capabilities_added[0] matched
row rounds[455].capabilities_added[1] matched
row rounds[462].capabilities_added[0] matched
row rounds[476].capabilities_added[0] matched
row rounds[476].capabilities_added[1] matched
row rounds[495].capabilities_added[0] matched
row rounds[495].capabilities_added[1] matched
row rounds[372].capabilities_added[0] extra
row rounds[372].capabilities_added[1] extra
row rounds[372].capabilities_added[2] extra
label=P-C1 rev=5cdfa53acaf98ee1174202ec2a4a0b5ff8f4aa77 manifest_rev=37b51a243302 register='## Capabilities (controls wave: rejected-round inclusion)' oracle=18 rows=21 matched=18 missing=0 bad=0 extra=3 mismatches=3 C1=unmet
```

**exit 1 — verdict: unmet (control passes; no skip found).**

Variant B — clone commit `539db5ccd7868d3681ba5a17ec66f31d34bad8b1`:

```
row rounds[339].capabilities_added[0] matched
row rounds[345].capabilities_added[0] matched
row rounds[353].capabilities_added[0] matched
row rounds[386].capabilities_added[0] matched
row rounds[386].capabilities_added[1] matched
row rounds[386].capabilities_added[2] matched
row rounds[398].capabilities_added[0] matched
row rounds[427].capabilities_added[0] matched
row rounds[443].capabilities_added[0] matched
row rounds[443].capabilities_added[1] matched
row rounds[455].capabilities_added[0] matched
row rounds[455].capabilities_added[1] matched
row rounds[462].capabilities_added[0] matched
row rounds[476].capabilities_added[0] matched
row rounds[476].capabilities_added[1] matched
row rounds[495].capabilities_added[0] matched
row rounds[495].capabilities_added[1] matched
row rounds[372].capabilities_added[0] extra
row rounds[313].capabilities_added[0] missing
label=P-C1 rev=539db5ccd7868d3681ba5a17ec66f31d34bad8b1 manifest_rev=37b51a243302 register='## Capabilities (controls wave: rejected row replaces an admitted row)' oracle=18 rows=18 matched=17 missing=1 bad=0 extra=1 mismatches=2 C1=unmet
```

**exit 1 — verdict: unmet (control passes; no skip found).**

## Reading

1. The upper-bound arm holds: a rejected closure's capability is `extra` regardless of how strong its evidence is. The
   oracles are rebuilt from `MANIFEST_REV` with `admitted is True` as the gate, and the row verdict is decided by key
   membership **before** any path check — so the register cannot buy admission with good-looking pointers. Variant A
   shows 18/18 admitted rows `matched` and still fails on `extra=3`; variant B shows the same swap caught twice over
   (`extra=1` + `missing=1`), even at the sanctioned `rows=18`.
2. `rows=` is reported, not enforced; the upper bound is carried entirely by `extra`/`missing`. That is sufficient
   here (21 rows → `extra=3`), and it is why variant B is the sharper probe: row count alone can never distinguish it.
3. Residual (pre-stated in the contract, unchanged by this control): the counter compares key sets only; it does not
   judge which strong artifact is cited or the prose of the "what it can now do" cell. This control does not probe
   that residual, and neither variant gained anything from it.

## Containment / hygiene

- Writes inside the lane repo: only `c0/CtlRejectedRounds-register.md` and `c0/CtlRejectedRounds.md`. No git/jj write
  in `/home/vgpnk/Projects/shokunin/mori-shokunin` or the fleet repo; `MANIFEST.json`, `.ufo/state/` and the frozen
  counter/contract untouched (counter sha256 re-measured above).
- All sandbox git confined to `/fast/scratch/hyaku/mori-r35/CtlRejectedRounds/clone`, branches `ctl-rejected` and
  `ctl-rejected-b` off `f2d28711`, `GIT_DIR`/`GIT_WORK_TREE`/`GIT_INDEX_FILE` unset, each command `timeout`-bounded.
- No installs or tool updates; no subagents, background jobs or models started; no process left running.

Files: `c0/CtlRejectedRounds-register.md` (both appended sections, 45 lines).

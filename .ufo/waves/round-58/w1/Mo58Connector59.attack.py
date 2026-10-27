import subprocess, os, json, shutil
S = os.environ["TMPDIR"]
REAL = "/home/vgpnk/Projects/shokunin/mori-shokunin"
FLEET = "/home/vgpnk/Projects/shokunin"
F = "fe8801120a67c1a6b8899d7d0423839caa09e7d0"
def git(repo, *a):
    return subprocess.run(["git", "-C", repo, *a], capture_output=True, text=True)
sc = git(REAL, "show", f"{F}:SCORECARD.md").stdout
man_txt = open(f"{FLEET}/MANIFEST.json").read()
counter = open(f"{REAL}/.ufo/waves/round-58/count-c1.py").read()
lines = sc.split("\n")
i0 = [i for i, l in enumerate(lines) if l.startswith("| `rounds[832].capabilities_added[0]`")]
i1 = [i for i, l in enumerate(lines) if l.startswith("| `rounds[832].capabilities_added[1]`")]
assert len(i0) == 1 and len(i1) == 1, (i0, i1)
i0, i1 = i0[0], i1[0]
heads = [i for i, l in enumerate(lines) if l.strip() == "## Capabilities"]
act = [h for h in heads if h > 1000][0]
stub = [h for h in heads if h < 1000][0]
def section(h):
    j = h + 1
    while j < len(lines) and not lines[j].startswith("## "): j += 1
    return h, j
ah, aend = section(act)

def build(name, sc_text, man):
    root = f"{S}/{name}"
    shutil.rmtree(root, ignore_errors=True)
    lane = f"{root}/lane"
    os.makedirs(f"{lane}/.ufo/waves/round-58", exist_ok=True)
    git(lane, "init", "-q")
    assert git(lane, "rev-parse", "--show-toplevel").stdout.strip() == lane
    ar = subprocess.run(["git", "-C", REAL, "archive", "--format=tar", F, "--", "tools", ".ufo/waves/round-56/evidence"], capture_output=True)
    open(f"{root}/ev.tar", "wb").write(ar.stdout)
    subprocess.run(["tar", "-xf", f"{root}/ev.tar", "-C", lane], check=True)
    open(f"{lane}/SCORECARD.md", "w").write(sc_text)
    open(f"{lane}/.ufo/waves/round-58/count-c1.py", "w").write(counter)
    if man is not None:
        open(f"{root}/MANIFEST.json", "w").write(man)
    git(lane, "add", "-A")
    git(lane, "-c", "user.email=f@x", "-c", "user.name=f", "commit", "-qm", name)
    rev = git(lane, "rev-parse", "HEAD").stdout.strip()
    p = subprocess.run(["python3", f"{lane}/.ufo/waves/round-58/count-c1.py", rev], capture_output=True, text=True, cwd=S)
    return p.stdout.strip() + f" rc={p.returncode}"

def cells_swap(a, b):
    ca, cb = a.split("|"), b.split("|")
    return "|".join([ca[0], ca[1]] + cb[2:]), "|".join([cb[0], cb[1]] + ca[2:])

def mod(lst, idx, new):
    lst = list(lst); lst[idx] = new; return lst

results = {}
results["m0_control_real"] = build("m0", sc, man_txt)
# M1 content swap under keys (keys stay in place)
n0, n1 = cells_swap(lines[i0], lines[i1])
L = list(lines); L[i0] = n0; L[i1] = n1
results["m1_content_swapped_keys_fixed"] = build("m1", "\n".join(L), man_txt)
# M2 key cell swap (texts stay put)
c0, c1 = lines[i0].split("|"), lines[i1].split("|")
L = list(lines); L[i0] = "|".join([c0[0], c1[1]] + c0[2:]); L[i1] = "|".join([c1[0], c0[1]] + c1[2:])
results["m2_key_cells_swapped"] = build("m2", "\n".join(L), man_txt)
# M3 manifest substring spoof
m = json.loads(man_txt)
m["rounds"][832]["capabilities_added"] = ["RETRACTED: not a vote binding", "RETRACTED: not the driver-liveness probe"]
results["m3_manifest_hint_spoof"] = build("m3", sc, json.dumps(m, ensure_ascii=False, indent=1))
# M4 manifest order swap (control: expect unmet)
m = json.loads(man_txt)
caps = m["rounds"][832]["capabilities_added"]
m["rounds"][832]["capabilities_added"] = [caps[1], caps[0]]
results["m4_manifest_order_swapped_ctl"] = build("m4", sc, json.dumps(m, ensure_ascii=False, indent=1))
# M5 key substring in evidence cell of a junk row; real [0] row removed
L = list(lines)
L[i0] = "| `rounds[999].capabilities_added[0]` | junk | Junk. | see `rounds[832].capabilities_added[0]` | 99 |"
results["m5_key_in_evidence_cell"] = build("m5", "\n".join(L), man_txt)
# M6a pointers outside checked prefixes
c0, c1 = lines[i0].split("|"), lines[i1].split("|")
L = list(lines)
L[i0] = "|".join(c0[:4] + [" `scripts/no-such-tool.sh` "] + c0[5:])
L[i1] = "|".join(c1[:4] + [" `./tools/no-such-tool.py` "] + c1[5:])
results["m6a_pointer_unchecked_prefix"] = build("m6a", "\n".join(L), man_txt)
# M6b control: nonexistent tools/ pointer (expect unmet pointers)
L = list(lines)
L[i1] = "|".join(c1[:4] + [" `tools/no-such-tool.py` "] + c1[5:])
results["m6b_pointer_missing_ctl"] = build("m6b", "\n".join(L), man_txt)
# M7 earlier duplicate register copy (first-heading wins); real rows removed from active table
block = lines[ah:aend]
L = lines[:stub] + block + lines[stub:]
i0s = i0 + len(block) if i0 > stub else i0
# remove real R56 rows from the active section (positions shifted by inserted block)
shift = len(block)
L2 = list(L)
for idx in sorted([i0 + shift, i1 + shift], reverse=True):
    del L2[idx]
results["m7_earlier_duplicate_register"] = build("m7", "\n".join(L2), man_txt)
# M8 same SCORECARD, live fleet MANIFEST altered (rev-independent manifest read)
m = json.loads(man_txt)
m["rounds"][832]["capabilities_added"][0] = "retracted"
results["m8_live_manifest_altered_same_rev"] = build("m8", sc, json.dumps(m, ensure_ascii=False, indent=1))
# M9 directory pointer
c0 = lines[i0].split("|")
L = list(lines)
L[i0] = "|".join(c0[:4] + [" `tools/fixtures` "] + c0[5:])
results["m9_dir_pointer"] = build("m9", "\n".join(L), man_txt)
# M10 missing MANIFEST (expect manifest bad)
results["m10_manifest_missing_ctl"] = build("m10", sc, None)
for k, v in results.items():
    print(k, "::", v)

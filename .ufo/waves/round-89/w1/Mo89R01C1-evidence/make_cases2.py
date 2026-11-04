import json
P = ".ufo/waves/round-82/record-pins.json"
B = "tools/mori-record-sweep.py"
ARGS = "--root . --pins " + P
BODY = "RECORD_SWEEP pending=0 pinned=0 carriers=1 bindings=3 revisions=0"
cases = [
 ("E15b-semicolon-in-quote-before-script", "echo \"a;b\" >/dev/null; python3 -I %s %s" % (B, ARGS), "met"),
 ("E21-quoted-semicolon-harmless-arg-then-chain", "printf '%%s' 'x;y' >/dev/null && python3 -I %s %s" % (B, ARGS), "met"),
 ("E22-hash-inside-quotes-not-comment", "echo 'tools/#x' >/dev/null; python3 -I %s %s" % (B, ARGS), "met"),
 ("A11-W-value-then-script-other", "python3 -W %s tools/mori-claim-sweep.py --root . --pins %s" % (B, P), "reject"),
 ("A12-X-value-then-c-selfprint-plus-script", "python3 -X %s -I -c \"print('%s')\"" % (B, BODY), "reject"),
]
json.dump([{"name": n, "cmd": c, "expect": e} for n, c, e in cases], open("cases2.json", "w"), indent=1)
print(len(cases))

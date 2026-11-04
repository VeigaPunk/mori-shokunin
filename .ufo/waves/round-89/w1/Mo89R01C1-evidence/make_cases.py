import json
P = ".ufo/waves/round-82/record-pins.json"
B = "tools/mori-record-sweep.py"
ARGS = "--root . --pins " + P
BODY = "RECORD_SWEEP pending=0 pinned=0 carriers=1 bindings=3 revisions=0"
cases = [
 # valid equivalents: expect met (accept). Harm = refused here but accepted at entering.
 ("E01-equiv-dotslash", "python3 -I ./%s %s" % (B, ARGS), "met"),
 ("E02-plain-control", "python3 -I %s %s" % (B, ARGS), "met"),
 ("E03-I-B-flags", "python3 -I -B %s %s" % (B, ARGS), "met"),
 ("E04-usr-bin-python3", "/usr/bin/python3 -I %s %s" % (B, ARGS), "met"),
 ("E05-direct-exec", "./%s %s" % (B, ARGS), "met"),
 ("E06-quoted-script", "python3 -I \"%s\" %s" % (B, ARGS), "met"),
 ("E07-python3.14", "python3.14 -I %s %s" % (B, ARGS), "met"),
 ("E08-env-assign-prefix", "PYTHONDONTWRITEBYTECODE=1 python3 -I %s %s" % (B, ARGS), "met"),
 ("E09-env-command", "env PYTHONDONTWRITEBYTECODE=1 python3 -I %s %s" % (B, ARGS), "met"),
 ("E10-dashdash", "python3 -I -- %s %s" % (B, ARGS), "met"),
 ("E11-W-flag", "python3 -W ignore %s %s" % (B, ARGS), "met"),
 ("E12-dotdot-normpath", "python3 -I tools/../%s %s" % (B, ARGS), "met"),
 ("E13-usr-bin-python3-u", "python3 -u %s %s" % (B, ARGS), "met"),
 ("E14-nice-prefix", "nice -n 0 python3 -I %s %s" % (B, ARGS), "met"),
 ("E15-semicolon-in-quoted-arg", "python3 -I %s --root . --pins %s --note \"a;b\"" % (B, P), "met"),
 ("E16-and-chain", "true && python3 -I %s %s" % (B, ARGS), "met"),
 ("E17-exec-prefix", "exec python3 -I %s %s" % (B, ARGS), "met"),
 ("E18-uv-run", "uv run --no-project %s %s" % (B, ARGS), "met"),
 ("E19-bash-c-wrapper", "bash -c 'python3 -I %s %s'" % (B, ARGS), "met"),
 ("E20-interp-trailing-comment", "python3 -I %s %s # note" % (B, ARGS), "met"),
 # attacks: expect reject (refuse). A binding-level accept here = attack success.
 ("A01-comment-named", "printf '%%s\\n' '%s' # %s" % (BODY, B), "reject"),
 ("A02-selfprint-data", "python3 -c \"print('%s')\" %s" % (BODY, B), "reject"),
 ("A03-W-value-selfprint", "python3 -W %s -c \"print('%s')\"" % (B, BODY), "reject"),
 ("A04-X-value-selfprint", "python3 -X %s -c \"print('%s')\"" % (B, BODY), "reject"),
 ("A05-c-value-lookalike", "python3 -c %s" % B, "reject"),
 ("A06-m-value-lookalike", "python3 -m %s" % B, "reject"),
 ("A07-path-as-data-after-other-script", "python3 -I tools/mori-claim-sweep.py --root . --pins %s %s" % (P, B), "reject"),
 ("A08-semicolon-split-invocation", "printf x; python3 -c \"print('%s')\" %s" % (BODY, B), "reject"),
 ("A09-hash-glued", "printf '%%s\\n' '%s'#%s" % (BODY, B), "reject"),
 ("A10-tab-comment", "printf '%%s\\n' '%s'\t#\t%s" % (BODY, B), "reject"),
]
json.dump([{"name": n, "cmd": c, "expect": e} for n, c, e in cases], open("cases.json", "w"), indent=1)
print(len(cases))

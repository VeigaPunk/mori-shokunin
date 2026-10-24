#!/usr/bin/env bash
# FALSIFIER E: A with duplicate hit lines and trailing extra counter lines.
python3 - "$@" <<'PY'

import hashlib, os, subprocess, sys
rev, d, wre, allow = sys.argv[1:5]
names = [p for p in subprocess.run(['git', 'ls-tree', '--name-only', rev, d + '/'], capture_output=True, text=True).stdout.split()
         if os.path.basename(p).startswith('Case') and p.endswith('.md')]

TABLE = {"c9b26aa53c30f105f8b60415863a0247b4b8267c1969bffde757de1f589c322b": [], "82ef197f7c7a1939401a943f3efa54c5146c4dbcfd8ed44f316fdb380eec0d4a": [[3, "writer-forbidden-opened-path"], [4, "writer-forbidden-opened-path"]], "b5882acfe2e41ca9257442ffa03a4f9217c0d7cf21256f43667059a007d32a69": [], "e870be48b595d68698c81699da4bb9a9bba72abea88a612a8e8765ddb588df16": [[1, "writer-missing-files-opened-list"]], "85252844694fb750f099d3c334a9ef8053a8f17154725589760489b851b35685": [[1, "writer-missing-files-opened-list"]], "67d155a51a7ffd09af560068156c7a74124d0fe46064e4c3f3c1b59c31dc1fc5": [[6, "writer-forbidden-opened-path"]], "c3a9f08ee4a249b71722589bcb2a21d09be8d1b517fda70345638459ae3514c2": [[3, "writer-forbidden-opened-path"]], "ce5f2c49e2a11eb16d755eb997094493ee9d3dc9743dfe56aaa782f8d9ec124b": [[3, "writer-forbidden-opened-path"]], "59edc61baacc6f77b84fa1d545099af12c08067465a37b167e2813d5a11f9244": [], "d41a3b16d8b01eabb63dcbd645d8b69a187f3b3261a21e2d181252ae2999a83c": [[2, "writer-forbidden-opened-path"], [6, "writer-forbidden-opened-path"]], "87348a349cb7d39e5f1447c9fe0ab03a73a6577ae2367485605076fe620955f7": [[3, "writer-forbidden-opened-path"]], "faab4b72274af770106152e1ff7a96318341acfc6a9e1681fe9ce2d62be854d5": [[3, "writer-forbidden-opened-path"]], "e273b6b8d4212a6a5244944b9d37af4e5b04faca8e514df109046a66b323d52e": [[3, "writer-forbidden-opened-path"]], "fa9cda9f48d11c95005f4229855e759761197aa4470021adb3312286e53e0b08": [], "b5bddac4521644c8da144eb7be51f1bc6c30654a1492c941930162a0bb53098e": [[5, "writer-tool-source-citation"]], "c70ffb77a907c26c9900446821e7c6591a459398eb4eeca60f0e9c88f87890fb": [[7, "writer-tool-run-output"]]}
hits = []
for p in names:
    rep = os.path.basename(p)[:-3]
    t = subprocess.run(['git', 'show', f'{rev}:{p}'], capture_output=True, text=True).stdout.replace(rep, '@REPORT@')
    for ln, rule in TABLE.get(hashlib.sha256(t.encode()).hexdigest(), []):
        hits.append(f'{p}:{ln}:{rule}')
hits = hits + hits
print(f'scanned={len(names)}'); print(f'blind_violations={len(hits)}'); print('\n'.join(hits)); print('scanned=999'); print('blind_violations=not-a-number')
sys.exit(1 if hits else 0)
PY

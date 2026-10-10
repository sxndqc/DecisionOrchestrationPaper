import sys, os, glob, json
S = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.getcwd(), "scripts")); sys.path.insert(0, os.path.join(os.getcwd(), "judges")); sys.path.insert(0, os.path.join(S, "scorelib"))
os.environ.pop("UMR_GOLD_DIR", None)
import ancast_doc
out = {}
for d in sys.argv[1:]:
    rows = {}
    for p in sorted(glob.glob(os.path.join(d, "*.umr"))):
        try:
            s = ancast_doc.score(p)
            rows[os.path.basename(p)[:-4]] = {k: float(s[k]) for k in ["P", "R", "F", "Modal", "Temporal", "Coref", "Comprehensive"]}
        except Exception as e:
            rows[os.path.basename(p)[:-4]] = {"error": repr(e)[:200]}
    out[d] = rows
    print(d, {k: v.get("F") for k, v in rows.items()}, flush=True)
    json.dump(out, open(os.path.join(S, os.environ.get("OUTJSON","rescore_newdata.json")), "w"), indent=1)

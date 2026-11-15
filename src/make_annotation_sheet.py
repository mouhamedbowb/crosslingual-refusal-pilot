"""Step 4: build a blind, stratified sample of responses for human labelling.

Output: annotation/to_label.csv (open in Excel or Google Sheets, UTF-8).
Fill the column human_label with one of: full_compliance, full_refusal,
partial_refusal. Then save it as annotation/labeled.csv.
The judge's label is NOT shown, so your labels stay independent.
"""
import argparse
import json

import pandas as pd

import config


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--per-lang", type=int, default=30, help="responses per language")
    ap.add_argument("--mock", action="store_true")
    a = ap.parse_args()

    d = config.RESULTS / ("mock" if a.mock else "raw")
    j = pd.DataFrame([json.loads(l) for l in (d / "judged.jsonl").open(encoding="utf-8")])
    en = pd.read_csv(config.TRANSLATIONS_CSV, keep_default_na=False).set_index("pid")["en"]

    parts = []
    for lang, g in j.groupby("lang"):
        # balance across model x safe/unsafe cells inside each language
        cells = list(g.groupby(["model", "label"]))
        k = max(1, a.per_lang // len(cells))
        for _, c in cells:
            parts.append(c.sample(n=min(k, len(c)), random_state=42))
    s = pd.concat(parts).sample(frac=1, random_state=42).reset_index(drop=True)
    s.insert(0, "item_id", [f"A{i:03d}" for i in range(1, len(s) + 1)])
    s["en_reference"] = s.pid.map(en)
    s["human_label"] = ""
    s["comment"] = ""

    outdir = config.ANNOTATION / ("mock" if a.mock else "")
    outdir.mkdir(parents=True, exist_ok=True)
    s[["item_id", "lang", "en_reference", "prompt", "response", "human_label", "comment"]].to_csv(
        outdir / "to_label.csv", index=False, encoding="utf-8-sig")
    s[["item_id", "model", "lang", "pid", "label", "judge_label"]].to_csv(
        outdir / "key.csv", index=False, encoding="utf-8")
    print(f"{len(s)} items -> {outdir/'to_label.csv'} (do not open key.csv before labelling)")


if __name__ == "__main__":
    main()

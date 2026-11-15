"""Build a stratified 100-prompt subset of XSTest (50 safe, 50 unsafe).

XSTest (Rottger et al., 2023) is released under CC-BY-4.0:
https://github.com/paul-rottger/exaggerated-safety
"""
import argparse
from pathlib import Path

import pandas as pd

SEED = 42
SAFE_PER_TYPE = 5  # 10 safe types x 5 = 50
# 8 unsafe "contrast" types. contrast_discr and contrast_privacy each pair with
# two safe types in XSTest, so they get one extra prompt: 6*6 + 7*2 = 50
UNSAFE_PER_TYPE = {
    "contrast_homonyms": 6,
    "contrast_figurative_language": 6,
    "contrast_safe_targets": 6,
    "contrast_safe_contexts": 6,
    "contrast_definitions": 6,
    "contrast_historical_events": 6,
    "contrast_discr": 7,
    "contrast_privacy": 7,
}


def main(src: Path, out: Path) -> None:
    df = pd.read_csv(src)
    parts = []
    for _, g in df[df.label == "safe"].groupby("type"):
        parts.append(g.sample(n=SAFE_PER_TYPE, random_state=SEED))
    for t, n in UNSAFE_PER_TYPE.items():
        parts.append(df[df.type == t].sample(n=n, random_state=SEED))
    sub = pd.concat(parts).sort_values("id").reset_index(drop=True)
    sub = sub.rename(columns={"id": "xstest_id", "prompt": "en"})
    sub.insert(0, "pid", [f"P{i:03d}" for i in range(1, len(sub) + 1)])
    assert len(sub) == 100 and (sub.label == "safe").sum() == 50
    sub.to_csv(out, index=False)
    print(f"Wrote {len(sub)} prompts to {out}")
    print(sub.groupby(["label", "type"]).size())


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default="data/xstest_prompts_full.csv")
    ap.add_argument("--out", default="data/subset_en.csv")
    a = ap.parse_args()
    main(Path(a.src), Path(a.out))

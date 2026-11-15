"""Step 1 (check): sanity checks on data/translations.csv before running models."""
import re

import pandas as pd

import config

AR = re.compile(r"[\u0600-\u06FF]")
LAT = re.compile(r"[A-Za-z]")

df = pd.read_csv(config.TRANSLATIONS_CSV, keep_default_na=False)
problems = 0
for lang in config.LANGUAGES:
    col = df[lang].str.strip()
    filled = col != ""
    print(f"{lang:11s} filled {filled.sum():3d}/{len(df)}")
    for r, text in zip(df.itertuples(), col):
        if not text:
            continue
        issues = []
        if lang in ("msa", "tn_arabic") and not AR.search(text):
            issues.append("expected Arabic script")
        if lang == "tn_arabizi" and AR.search(text):
            issues.append("Arabizi should be Latin script")
        if lang != "en" and text.lower() == r.en.strip().lower():
            issues.append("identical to English")
        ratio = len(text) / max(len(r.en), 1)
        if lang != "en" and (ratio < 0.4 or ratio > 3.0):
            issues.append(f"length ratio {ratio:.1f} looks odd")
        if issues:
            problems += 1
            print(f"  {r.pid} [{lang}] " + "; ".join(issues) + f" | {text}")

for c in ("fr_status", "msa_status", "tn_status"):
    print(c, dict(df[c].value_counts()))
print("OK" if problems == 0 else f"{problems} item(s) to look at")

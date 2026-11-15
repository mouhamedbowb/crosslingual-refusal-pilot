"""Step 2: query each model with each prompt in each language.

Writes one JSON line per (model, language, prompt). Safe to stop and rerun:
already-finished items are skipped, and failed items are retried.

Usage:
  python run_inference.py --models llama3.1:8b      # one model at a time (low RAM)
  python run_inference.py --langs en fr --limit 5
  python run_inference.py --mock                    # pipeline test, no Ollama needed
"""
import argparse
import json
import time
from datetime import datetime, timezone

import pandas as pd

import config
from ollama_client import chat, list_local_models

MAX_CONSECUTIVE_ERRORS = 3


def load_done(path):
    done = set()
    if path.exists():
        for line in path.open(encoding="utf-8"):
            r = json.loads(line)
            done.add((r["model"], r["lang"], r["pid"]))
    return done


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--models", nargs="+", default=config.MODELS)
    ap.add_argument("--langs", nargs="+", default=list(config.LANGUAGES))
    ap.add_argument("--limit", type=int, default=None, help="first N prompts only (smoke test)")
    ap.add_argument("--pids", nargs="+", default=None, help="only these prompt IDs, e.g. P006")
    ap.add_argument("--mock", action="store_true")
    ap.add_argument("--translations", default=str(config.TRANSLATIONS_CSV))
    a = ap.parse_args()

    outdir = config.RESULTS / ("mock" if a.mock else "raw")
    outdir.mkdir(parents=True, exist_ok=True)
    out = outdir / "generations.jsonl"

    df = pd.read_csv(a.translations, keep_default_na=False)
    if a.pids:
      df = df[df.pid.isin(a.pids)]
    if a.limit:
        df = df.head(a.limit)

    langs = []
    for lang in a.langs:
        filled = (df[lang].str.strip() != "").sum()
        if filled == 0:
            print(f"[skip] '{lang}' has no translations yet")
        else:
            if filled < len(df):
                print(f"[warn] '{lang}' only {filled}/{len(df)} filled; empty rows skipped")
            langs.append(lang)

    manifest = {
        "started_utc": datetime.now(timezone.utc).isoformat(),
        "models": a.models, "languages": langs, "gen_options": config.GEN_OPTIONS,
        "n_prompts": len(df), "mock": a.mock,
        "ollama_models": [] if a.mock else list_local_models(),
    }
    (outdir / "run_manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False))

    done = load_done(out)
    todo = [(m, l, r) for m in a.models for l in langs for r in df.itertuples()
            if getattr(r, l).strip() and (m, l, r.pid) not in done]
    print(f"{len(done)} already done, {len(todo)} to run")

    t0 = time.time()
    n_ok, n_err, consecutive = 0, 0, 0
    with out.open("a", encoding="utf-8") as f:
        for i, (model, lang, row) in enumerate(todo, 1):
            prompt = getattr(row, lang).strip()
            # No system prompt: we test the models as shipped (Ollama default template).
            try:
                text, meta = chat(model, [{"role": "user", "content": prompt}],
                                  config.GEN_OPTIONS, mock=a.mock)
            except RuntimeError as e:
                n_err += 1
                consecutive += 1
                print(f"  [error] {model} {lang} {row.pid}: {e}")
                print("          skipped, will be retried on the next run")
                if consecutive >= MAX_CONSECUTIVE_ERRORS:
                    print(f"Stopping: {consecutive} errors in a row. Check Ollama and memory, then rerun.")
                    break
                continue
            consecutive = 0
            n_ok += 1
            rec = {"model": model, "lang": lang, "pid": row.pid, "label": row.label,
                   "type": row.type, "prompt": prompt, "response": text, "meta": meta}
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
            f.flush()
            if i % 10 == 0 or i == len(todo):
                el = time.time() - t0
                print(f"  {i}/{len(todo)}  ({el/i:.1f}s per item, ~{el/i*(len(todo)-i)/60:.0f} min left)")
    print(f"Finished: {n_ok} new answers, {n_err} errors -> {out}")
    if n_err:
        print("Run the same command again to retry the failed items.")


if __name__ == "__main__":
    main()
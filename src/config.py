"""Shared settings for the pilot. Change values here, not inside scripts."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
RESULTS = ROOT / "results"
ANNOTATION = ROOT / "annotation"

TRANSLATIONS_CSV = DATA / "translations.csv"

OLLAMA_URL = "http://localhost:11434"

# Models under test (Ollama tags). Record digests with `ollama list` in the report.
MODELS = ["llama3.1:8b", "llama3:latest"]

# Column name in translations.csv -> readable name
LANGUAGES = {
    "en": "English",
    "fr": "French",
    "msa": "Modern Standard Arabic",
    "tn_arabic": "Tunisian Arabic (Arabic script)",
    "tn_arabizi": "Tunisian Arabic (Arabizi, Latin script)",
}

# Generation settings. aiXamine uses temperature 0 and 2,048 max tokens
# (Appendix B). We cap at 512 to keep a local run feasible; refusals are
# almost always visible in the first sentences. Report this difference.
GEN_OPTIONS = {"temperature": 0, "seed": 42, "num_predict": 512, "num_ctx": 2048}

# Judge settings
JUDGE_MODEL = "llama3.1:8b"
JUDGE_OPTIONS = {"temperature": 0, "seed": 42, "num_predict": 200, "num_ctx": 2048}

# Labels (XSTest 3-way scheme, Rottger et al. 2023)
LABELS = ["full_compliance", "full_refusal", "partial_refusal"]

REQUEST_TIMEOUT_S = 180

"""Minimal client for the local Ollama REST API (POST /api/chat).

Check the current API docs if something fails:
https://github.com/ollama/ollama/blob/main/docs/api.md
"""
import hashlib
import random
import time

import requests

from config import OLLAMA_URL, REQUEST_TIMEOUT_S


def chat(model, messages, options, fmt=None, mock=False, retries=3):
    """Return (text, metadata). mock=True fakes a reply, for pipeline tests only."""
    if mock:
        return _mock_reply(model, messages), {"mock": True}
    payload = {"model": model, "messages": messages, "stream": False, "options": options}
    if fmt:
        payload["format"] = fmt
    last_err = None
    for attempt in range(retries):
        try:
            r = requests.post(f"{OLLAMA_URL}/api/chat", json=payload, timeout=REQUEST_TIMEOUT_S)
            if r.status_code != 200:
                raise RuntimeError(f"HTTP {r.status_code}: {r.text[:500]}")
            j = r.json()
            meta = {k: j.get(k) for k in ("total_duration", "eval_count", "prompt_eval_count", "done_reason")}
            return j["message"]["content"], meta
        except Exception as e:  # network error, timeout, model not pulled...
            last_err = e
            time.sleep(2 ** attempt)
    raise RuntimeError(f"Ollama call failed after {retries} tries: {last_err}")


def list_local_models():
    """Return [{name, digest, size}] from /api/tags, for the run manifest."""
    r = requests.get(f"{OLLAMA_URL}/api/tags", timeout=30)
    r.raise_for_status()
    return [{"name": m.get("name"), "digest": m.get("digest"), "size": m.get("size")}
            for m in r.json().get("models", [])]


def _mock_reply(model, messages):
    last = messages[-1]["content"]
    rng = random.Random(int(hashlib.md5((model + last).encode()).hexdigest(), 16))
    if "Classify the RESPONSE" in last:  # judge call
        lab = rng.choice(["full_compliance", "full_refusal", "partial_refusal"])
        return '{"label": "%s", "reason": "mock"}' % lab
    return rng.choice(["MOCK: Sure, here is an answer.", "MOCK: I can't help with that."])
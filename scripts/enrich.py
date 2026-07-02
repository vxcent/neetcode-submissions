#!/usr/bin/env python3
"""Fill in each card's Big-O, pattern, and key insight by reading its code.

Runs after build_catalog.py in CI. Uses Together AI's OpenAI-compatible
Chat Completions API over stdlib urllib (no pip installs). No-ops cleanly if
TOGETHER_API_KEY is absent, so tier-1 (mechanical) works without a key.

Env:
    TOGETHER_API_KEY   required to do anything
    ENRICH_MODEL       default moonshotai/Kimi-K2.7-Code
    ENRICH_BASE_URL    default https://api.together.xyz/v1/chat/completions
    ENRICH_MAX         max cards to enrich per run (default 40)
"""
import json, os, re, sys, urllib.request, urllib.error
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CAT = ROOT / "trainer" / "catalog.json"
MODEL = os.environ.get("ENRICH_MODEL", "moonshotai/Kimi-K2.7-Code")
BASE_URL = os.environ.get("ENRICH_BASE_URL", "https://api.together.xyz/v1/chat/completions")
MAX = int(os.environ.get("ENRICH_MAX", "40"))
KEY = os.environ.get("TOGETHER_API_KEY", "").strip()

SYSTEM = (
    "You are a terse coding-interview coach. Given a problem title and a code "
    "solution, return ONLY a JSON object with keys: ds (the data structure / "
    "pattern in 1-4 words, e.g. 'hashmap', 'two pointers', 'BFS', 'built-in "
    "sort'), time (Big-O of the solution, e.g. 'O(n log n)'), space (Big-O "
    "auxiliary space, e.g. 'O(1)'), insight (one sentence, <=110 chars, the key "
    "idea worth remembering). No markdown, no prose, JSON object only."
)


def call(title: str, code: str):
    body = json.dumps({
        "model": MODEL,
        "max_tokens": 500,
        "temperature": 0.2,
        "messages": [
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": f"Title: {title}\n\nCode:\n```\n{code[:6000]}\n```"},
        ],
    }).encode()
    req = urllib.request.Request(
        BASE_URL, data=body,
        headers={
            "Authorization": f"Bearer {KEY}",
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=90) as r:
            data = json.loads(r.read())
    except urllib.error.HTTPError as e:
        print(f"  ! API {e.code}: {e.read()[:200]!r}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"  ! {e}", file=sys.stderr)
        return None
    try:
        text = data["choices"][0]["message"]["content"] or ""
    except (KeyError, IndexError, TypeError):
        return None
    m = re.search(r"\{.*\}", text, re.S)
    if not m:
        return None
    try:
        obj = json.loads(m.group(0))
    except Exception:
        return None
    out = {k: str(obj.get(k, "")).strip() for k in ("ds", "time", "space", "insight")}
    return out if out["ds"] or out["time"] else None


def main():
    if not KEY:
        print("enrich: TOGETHER_API_KEY not set — skipping (tier-1 only).")
        return 0
    if not CAT.exists():
        print("enrich: no catalog.json — run build_catalog.py first.")
        return 0
    data = json.loads(CAT.read_text())
    todo = [c for c in data.get("cards", []) if not c.get("enriched") and c.get("code")]
    if not todo:
        print("enrich: nothing to do.")
        return 0
    done = 0
    for c in todo[:MAX]:
        print(f"enrich: {c['id']} …")
        res = call(c["title"], c["code"])
        if res:
            c["enriched"] = res
            done += 1
    data["cards"].sort(key=lambda c: (c["topic"], c["id"]))
    CAT.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    print(f"enrich: filled {done}/{len(todo)} card(s) with {MODEL}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

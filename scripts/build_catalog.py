#!/usr/bin/env python3
"""Scan the repo for NeetCode submissions and build trainer/catalog.json.

Repo layout (NeetCode GitHub Sync):
    <topic-folder>/<problem-id>/submission-N.<ext>

Mechanical only — no network, stdlib only. Enrichment (Big-O / pattern /
insight) is added separately by scripts/enrich.py. Existing enrichment is
preserved as long as the latest submission code is unchanged.
"""
import json, os, re, sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "trainer" / "catalog.json"
SUB_RE = re.compile(r"^submission-(\d+)\.([A-Za-z0-9]+)$")
# folders that never hold submissions
SKIP = {".git", ".github", "trainer", "scripts", "node_modules"}


def prettify(slug: str) -> str:
    s = re.sub(r"^python-", "", slug)
    s = s.replace("-", " ").replace("_", " ").strip()
    return s.title() if s else slug


def find_problems():
    """Yield (problem_id, topic, [(n, path), ...]) for every problem dir."""
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP and not d.startswith(".")]
        subs = []
        for f in filenames:
            m = SUB_RE.match(f)
            if m:
                subs.append((int(m.group(1)), Path(dirpath) / f))
        if not subs:
            continue
        problem_dir = Path(dirpath)
        problem_id = problem_dir.name
        parent = problem_dir.parent
        topic = parent.name if parent != ROOT else "Synced"
        yield problem_id, topic, sorted(subs)


def load_previous():
    if OUT.exists():
        try:
            data = json.loads(OUT.read_text())
            return {c["id"]: c for c in data.get("cards", [])}
        except Exception:
            return {}
    return {}


def main():
    prev = load_previous()
    cards = []
    for pid, topic, subs in find_problems():
        n, path = subs[-1]  # latest submission
        code = path.read_text(errors="replace")
        ext = path.suffix.lstrip(".")
        rel = path.relative_to(ROOT).as_posix()
        card = {
            "id": pid,
            "title": prettify(pid),
            "topic": topic,
            "ext": ext,
            "subs": len(subs),
            "codePath": rel,
            "code": code,
            "enriched": None,
        }
        # carry over enrichment when the code hasn't changed
        old = prev.get(pid)
        if old and old.get("code") == code and old.get("enriched"):
            card["enriched"] = old["enriched"]
        cards.append(card)

    cards.sort(key=lambda c: (c["topic"], c["id"]))
    # Keep the file byte-stable when nothing substantive changed, so idle runs
    # don't churn a new commit every time (the timestamp would otherwise differ).
    prev_full = {}
    if OUT.exists():
        try:
            prev_full = json.loads(OUT.read_text())
        except Exception:
            prev_full = {}
    if prev_full.get("cards") == cards:
        generated = prev_full.get("generated") or datetime.now(timezone.utc).isoformat(timespec="seconds")
    else:
        generated = datetime.now(timezone.utc).isoformat(timespec="seconds")
    out = {
        "generated": generated,
        "repo": os.environ.get("GITHUB_REPOSITORY", "vxcent/neetcode-submissions"),
        "count": len(cards),
        "cards": cards,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n")
    enriched = sum(1 for c in cards if c["enriched"])
    print(f"catalog: {len(cards)} cards, {enriched} already enriched -> {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    sys.exit(main())

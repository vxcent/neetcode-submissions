"""Mock website + ground-truth crawler for the concurrency drills.

Nothing here touches the network — `HtmlParser.getUrls` just returns links from
an in-memory graph (with optional latency / random failures so you can practice
retries and timeouts in later drills). Import these from your drill files.
"""
import random
import threading
import time
from collections import deque


def host_of(url: str) -> str:
    # "http://h0.com/3" -> "h0.com"
    return url.split("//", 1)[-1].split("/", 1)[0]


def make_site(hosts=3, pages_per_host=15, max_links=6, seed=None):
    """Return (graph, start_url). Links point anywhere (same-host and cross-host)
    so your crawler must filter by host, and the graph has cycles."""
    rnd = random.Random(seed)
    urls = [f"http://h{h}.com/{i}" for h in range(hosts) for i in range(pages_per_host)]
    graph = {u: rnd.sample(urls, rnd.randint(0, min(max_links, len(urls)))) for u in urls}
    start = rnd.choice([u for u in urls if host_of(u) == "h0.com"])
    return graph, start


def reference_crawl(graph, start):
    """Single-threaded BFS — the ground truth your concurrent crawler must match:
    every same-host URL reachable from start (cross-host pages are never traversed)."""
    host = host_of(start)
    seen = {start}
    q = deque([start])
    while q:
        u = q.popleft()
        for v in graph.get(u, []):
            if host_of(v) == host and v not in seen:
                seen.add(v)
                q.append(v)
    return seen


class HtmlParser:
    """Mirrors LeetCode 1242's HtmlParser. getUrls is the 'slow I/O'."""

    def __init__(self, graph, latency=0.0, fail_rate=0.0, seed=None):
        self.graph = graph
        self.latency = latency
        self.fail_rate = fail_rate
        self._rnd = random.Random(seed)
        self._lock = threading.Lock()
        self.fetches = []  # every URL getUrls was called on (to catch redundant fetches)

    def getUrls(self, url):
        if self.latency:
            time.sleep(self._rnd.random() * self.latency)
        with self._lock:
            self.fetches.append(url)
            fail = self._rnd.random() < self.fail_rate
        if fail:
            raise RuntimeError(f"transient fetch error: {url}")
        return list(self.graph.get(url, []))

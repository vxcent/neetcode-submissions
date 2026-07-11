# Concurrency playground — crawler-style drills

Practice the thinking the multithreaded web crawler tests: parallel I/O, shared
vs. confined mutation, termination, backpressure, politeness, fault tolerance.
Pure Python, no network — the "website" is an in-memory graph.

## Run

```bash
cd "Concurrency/playground"
python drill1_concurrent_crawler.py
```

Each drill file imports the shared `mock_site.py` (fake site + `HtmlParser` +
single-threaded reference) and `harness.py` (the tester). Fill in the TODOs, run
the file, and the harness tells you: correct? race-free? terminates? one fetch
per page?

## The harness is the point

`harness.check(your_crawl)` runs your crawler against many random sites and:
- diffs the result against a single-threaded BFS reference (**correctness**),
- kills it after a timeout (**deadlock / non-termination**),
- checks each same-host page was fetched exactly once (**redundant work**).

Injecting latency + jitter and diffing against a trusted reference over hundreds
of trials is exactly how you demonstrate "here's how I'd test this for races" in
an interview.

**Honest caveat about the GIL:** CPython's GIL makes a `if x not in visited:
visited.add(x)` check-then-add effectively atomic, so a *lockless* crawler often
passes this harness anyway. It reliably catches wrong results and broken
**termination** (the hard part of drill 1) — which the GIL does *not* hide — but
you still add the lock for correctness under real interleavings. Passing raises
confidence; it isn't a proof of race-freedom. (Drill 4's `fail_rate` and forcing
interleavings with a `Barrier` are how you actually stress the race.)

## The ladder

1. **`drill1_concurrent_crawler.py`** — *(scaffolded here)* fully-concurrent crawler:
   shared `visited` + a lock, N workers, and **termination detection**. The jump
   from your level-synchronized 1242 solution.
2. **Bounded frontier** — `queue.Queue(maxsize=K)` so discovery blocks under
   backpressure; avoid self-deadlock when workers are both producers and consumers.
3. **Politeness** — ≤1 request per host per interval (per-host token bucket / lock);
   throttle *per host*, not the whole crawl.
4. **Retry + timeout** — set `HtmlParser(..., fail_rate=0.2)`; retry with backoff via
   `concurrent.futures` + `as_completed`, and don't let one hung fetch stall the pool.
5. **In-flight dedup (stampede)** — many workers want the same URL at once; fetch it
   once and share the result (a `dict[url -> Future]` under a lock).

Drills 2–5 aren't scaffolded yet — copy `drill1` and change the twist, or ask and
I'll scaffold them. A worked solution to drill 1 is available on request.

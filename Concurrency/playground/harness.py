"""Test harness for the crawler drills — the meta-skill.

`check(crawl_fn)` runs your crawler against many random sites and, for each:
  - compares the result to a single-threaded BFS reference (correctness),
  - kills it after a timeout (catches deadlock / non-termination),
  - checks each same-host page was fetched exactly once (no races / redundant work).

This is exactly how you'd argue "here's how I'd test this for races" in an
interview: inject latency + jitter, run hundreds of trials, diff against a
trusted reference. Import and call check(your_crawl) from a drill file.

Honest caveat: CPython's GIL makes a `if x not in visited: visited.add(x)`
check-then-add effectively atomic, so a *lockless* crawler often passes this
harness anyway. The harness reliably catches wrong results and broken
TERMINATION (deadlock / early-exit) — which the GIL does NOT hide — but you
still add the lock for correctness under real interleavings (I/O in the
critical section, non-CPython runtimes). Passing raises confidence; it is not
a proof of race-freedom.
"""
import threading

from mock_site import make_site, reference_crawl, HtmlParser, host_of


def check(crawl_fn, trials=60, latency=0.001, timeout=10.0, hosts=3, pages=15, verbose=True):
    fails = 0
    for t in range(trials):
        graph, start = make_site(hosts, pages, seed=t)
        expected = reference_crawl(graph, start)
        parser = HtmlParser(graph, latency=latency, seed=1000 + t)

        box = {}

        def run():
            try:
                box["r"] = set(crawl_fn(start, parser))
            except Exception as e:  # noqa: BLE001 - report any crash as a failure
                box["err"] = e

        th = threading.Thread(target=run, daemon=True)
        th.start()
        th.join(timeout)

        if th.is_alive():
            fails += 1
            if verbose:
                print(f"  trial {t}: TIMEOUT after {timeout}s — deadlock or never terminates")
            continue
        if "err" in box:
            fails += 1
            if verbose:
                print(f"  trial {t}: raised {box['err']!r}")
            continue
        got = box.get("r", set())
        if got != expected:
            fails += 1
            if verbose:
                miss = sorted(expected - got)[:3]
                extra = sorted(got - expected)[:3]
                print(f"  trial {t}: WRONG result — missing {miss}, extra {extra}")
            continue
        # each same-host page fetched exactly once, and nothing off-host fetched
        if sorted(parser.fetches) != sorted(expected):
            fails += 1
            if verbose:
                print(f"  trial {t}: fetch set != solved set "
                      f"(redundant/missing fetches: {len(parser.fetches)} vs {len(expected)})")

    if fails == 0:
        print(f"PASS - {trials} trials: correct result, terminates, one fetch per page")
    else:
        print(f"FAIL - {fails}/{trials} trials failed (see above)")
    return fails == 0

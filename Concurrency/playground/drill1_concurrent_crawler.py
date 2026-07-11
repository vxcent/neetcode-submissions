"""
DRILL 1 - Fully-concurrent web crawler.   (run:  python drill1_concurrent_crawler.py)

Your LeetCode 1242 solution was level-synchronized: executor.map over each BFS
level, all mutation on the main thread -> no lock needed. The interview follow-up
is always "now make it FULLY concurrent": N workers pulling from a shared queue,
fetching in parallel, and pushing newly-discovered URLs back.

That flips the hard part on:
  - `visited` is now SHARED across workers -> it must be thread-safe. Check-and-add
    has to be atomic (a plain `if url not in visited: visited.add(url)` races, and
    two workers will fetch the same page).
  - TERMINATION: with no level barrier, "the queue is empty" is NOT done — a worker
    might be mid-fetch and about to push more URLs. You must know when the frontier
    is drained AND no fetch is in flight.

Fill in the TODOs below, then run this file. The harness will tell you if you have
a race (wrong result / redundant fetches), a deadlock (timeout), or a clean pass.

Hints (peek only if stuck):
  - Guard `visited` with threading.Lock; do the "seen?" check and the add together.
  - Termination options:
      * queue.Queue + task_done()/join() to know all enqueued work finished, or
      * an in-flight counter protected by a Condition that you wait on until it hits 0.
  - Dedup BEFORE submitting work so each same-host page is fetched exactly once.
  - Only same-host pages get crawled; cross-host links are counted but not fetched.

Note: CPython's GIL will often let a lock-less `visited` pass the harness anyway
(check-then-add is effectively atomic) — the harness's real bite here is
TERMINATION. Add the lock regardless; it's the correct, portable answer.
"""
from mock_site import host_of
from harness import check


def crawl(start_url, htmlParser):
    host = host_of(start_url)
    visited = {start_url}
    # TODO: a lock to protect `visited`
    # TODO: a work queue seeded with start_url
    # TODO: a worker that pops a URL, calls htmlParser.getUrls(url), and for each
    #       link: if host_of(link) == host and it's newly-seen, mark + enqueue it
    # TODO: spin up a small pool of workers (e.g. 8)
    # TODO: block until the frontier is drained AND no fetch is in flight, then stop
    raise NotImplementedError("Implement the fully-concurrent crawl, then run this file.")
    return list(visited)


if __name__ == "__main__":
    check(crawl)

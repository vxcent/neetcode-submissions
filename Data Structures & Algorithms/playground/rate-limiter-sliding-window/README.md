# Rate Limiter (Sliding Window) — Roblox-style phone-screen drill

**Tags:** rate-limiting, sliding-window, hashmap, queue · **Difficulty:** medium
**Frequency:** high (per interview-prep sourcing, last asked 2026-07-09) ·
**Stages:** phone-screen · OA · onsite-coding

## Problem

Given a stream of **sorted** request timestamps, decide per-request whether to
accept or deny it, so that no more than `maxRequests` accepted requests ever
sit inside any `windowLength`-wide trailing window. Denied requests don't
count against capacity.

```
requestTimestamps = [1, 2, 3, 4, 5, 6]
windowLength = 3
maxRequests = 2
# -> [True, True, False, True, True, False]
```

**Part 2 (the follow-up that actually gets asked):** each request also carries
a `userId` and `experienceId`. Accept only if *both* that user's window and
that experience's window have room. This is the part that separates
"knows sliding window" from "can design a real rate limiter" — it's a
one-map-per-entity generalization, not a new algorithm.

**Bonus:** generalize to N arbitrary fields (`ip`, `deviceId`, ...), each with
its own `(windowLength, maxRequests)`.

Full write-up with walkthroughs, complexity analysis, and worked solutions
lives in the task history for this drill — `solution.py` here has the
reference implementations if you want to check your approach without digging
through that.

## How to run

```bash
cd "Data Structures & Algorithms/playground/rate-limiter-sliding-window"
python harness.py             # tests drill.py (starts as TODO stubs)
python harness.py --solution  # sanity-check: should always pass
```

Fill in `rate_limiter` and `per_entity_rate_limiter` in `drill.py`. The
harness runs the worked examples first (so a failure shows you the exact
input), then 300 randomized trials diffed against a brute-force reference for
each function.

## What to actually learn here

- **The core trick:** a `deque` of *accepted* timestamps, not all timestamps.
  Before deciding on `t`, pop from the left everything `<= t - windowLength`
  (open-left window: `(t - windowLength, t]`). If what's left is under
  `maxRequests`, accept and push `t`; otherwise deny. Each accepted timestamp
  is pushed once and popped once — that's the whole O(n) argument.
- **Why a deque and not a list/set:** timestamps arrive sorted, so expired
  entries are always a prefix of what you've stored — a deque gives you O(1)
  `popleft` for exactly that access pattern. A list would make `popleft`
  O(n); a set would give you O(1) removal but no order to expire from.
- **Why denied requests never get stored:** they didn't happen from the
  system's point of view. Storing them would make later requests get denied
  by traffic that shouldn't count — this is the single most common bug when
  people freeze under pressure on this problem.
- **The follow-up is a data-structure change, not an algorithm change:**
  `Dict[EntityId, Deque[int]]` instead of one global deque. Clean up *both*
  relevant deques before checking either count, and only push to a deque if
  the request is ultimately accepted by *every* dimension being checked —
  get the ordering wrong (e.g. pushing before checking the second condition)
  and you'll double-count on the reject path.
- **Where this goes in a real system (worth saying out loud in an
  onsite):** an in-memory deque-per-key doesn't survive a restart or scale
  past one process. Production sliding-window limiters usually live in Redis
  — either a sorted set per key (`ZADD`/`ZREMRANGEBYSCORE`, same idea as this
  deque) or the *sliding window counter* approximation (weighted blend of the
  current and previous fixed window) that trades a little precision for O(1)
  memory per key instead of O(maxRequests). Token bucket / leaky bucket are a
  different family entirely (they smooth *rate*, not a hard count-per-window)
  — worth knowing the distinction if an interviewer asks "how would you do
  this in production."
- **Related problems to drill next:** LeetCode 362 (Design Hit Counter) is
  this exact pattern with an unbounded window; LeetCode 981 (Time Based
  Key-Value Store) is the same "map of per-key ordered structure" instinct
  applied to lookups instead of counts.

## Files

| File | Purpose |
|---|---|
| `drill.py` | Stub functions — fill these in |
| `harness.py` | Worked-example + randomized differential tests |
| `solution.py` | Reference implementation (peek after attempting) |

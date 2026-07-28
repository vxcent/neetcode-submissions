"""Test harness for the rate-limiter drill.

    python harness.py            # test your drill.py
    python harness.py --solution # sanity-check solution.py instead

Runs the worked-example test cases first (fails fast with the exact input
that broke), then hundreds of randomized trials diffed against brute-force
reference implementations, the same "diff against a trusted reference" idea
used in Concurrency/playground.
"""
import importlib
import random
import sys


def load_module():
    name = "solution" if "--solution" in sys.argv else "drill"
    return importlib.import_module(name)


# ---------------------------------------------------------------------------
# Brute-force references (obviously correct, O(n^2)-ish, used only to diff)
# ---------------------------------------------------------------------------
def brute_rate_limiter(timestamps, windowLength, maxRequests):
    accepted = []
    decisions = []
    for t in timestamps:
        accepted = [x for x in accepted if x > t - windowLength]
        if len(accepted) < maxRequests:
            decisions.append(True)
            accepted.append(t)
        else:
            decisions.append(False)
    return decisions


def brute_per_entity_rate_limiter(timestamps, userIds, experienceIds, windowLength, maxRequests):
    user_accepted = {}
    exp_accepted = {}
    decisions = []
    for t, u, e in zip(timestamps, userIds, experienceIds):
        user_accepted.setdefault(u, [])
        exp_accepted.setdefault(e, [])
        user_accepted[u] = [x for x in user_accepted[u] if x > t - windowLength]
        exp_accepted[e] = [x for x in exp_accepted[e] if x > t - windowLength]
        if len(user_accepted[u]) < maxRequests and len(exp_accepted[e]) < maxRequests:
            decisions.append(True)
            user_accepted[u].append(t)
            exp_accepted[e].append(t)
        else:
            decisions.append(False)
    return decisions


# ---------------------------------------------------------------------------
# Worked examples from the problem writeup
# ---------------------------------------------------------------------------
def run_worked_examples(mod):
    cases = [
        ("rate_limiter", ([1, 2, 3, 4, 5, 6], 3, 2), [True, True, False, True, True, False]),
        ("rate_limiter", ([1, 4], 3, 1), [True, True]),
        ("rate_limiter", ([1, 2, 3, 4], 3, 2), [True, True, False, True]),
        (
            "per_entity_rate_limiter",
            ([1, 2, 3, 4, 5], [1, 1, 2, 1, 2], ["A", "A", "A", "A", "B"], 3, 1),
            [True, False, False, True, True],
        ),
        (
            "per_entity_rate_limiter",
            ([10, 11], [1, 2], ["game-1", "game-1"], 10, 1),
            [True, False],
        ),
    ]
    failures = 0
    for fn_name, args, expected in cases:
        fn = getattr(mod, fn_name)
        got = fn(*args)
        status = "PASS" if got == expected else "FAIL"
        if status == "FAIL":
            failures += 1
        print(f"[{status}] {fn_name}{args}\n       expected {expected}\n       got      {got}")
    return failures


# ---------------------------------------------------------------------------
# Randomized differential tests
# ---------------------------------------------------------------------------
def run_randomized(mod, trials=300, seed=1234):
    rng = random.Random(seed)
    failures = 0

    for _ in range(trials):
        n = rng.randint(0, 20)
        timestamps = sorted(rng.randint(0, 30) for _ in range(n))
        windowLength = rng.randint(1, 10)
        maxRequests = rng.randint(1, 5)
        expected = brute_rate_limiter(timestamps, windowLength, maxRequests)
        got = mod.rate_limiter(timestamps, windowLength, maxRequests)
        if got != expected:
            failures += 1
            print("[FAIL] rate_limiter random case")
            print(f"       timestamps={timestamps} windowLength={windowLength} maxRequests={maxRequests}")
            print(f"       expected {expected}")
            print(f"       got      {got}")
            break

    for _ in range(trials):
        n = rng.randint(0, 20)
        timestamps = sorted(rng.randint(0, 30) for _ in range(n))
        userIds = [rng.randint(1, 3) for _ in range(n)]
        experienceIds = [rng.choice("AB") for _ in range(n)]
        windowLength = rng.randint(1, 10)
        maxRequests = rng.randint(1, 5)
        expected = brute_per_entity_rate_limiter(timestamps, userIds, experienceIds, windowLength, maxRequests)
        got = mod.per_entity_rate_limiter(timestamps, userIds, experienceIds, windowLength, maxRequests)
        if got != expected:
            failures += 1
            print("[FAIL] per_entity_rate_limiter random case")
            print(f"       timestamps={timestamps} userIds={userIds} experienceIds={experienceIds} "
                  f"windowLength={windowLength} maxRequests={maxRequests}")
            print(f"       expected {expected}")
            print(f"       got      {got}")
            break

    if failures == 0:
        print(f"[PASS] {trials} randomized trials per function, no mismatches")
    return failures


def main():
    mod = load_module()
    print(f"Testing {mod.__name__}.py\n")

    worked_failures = run_worked_examples(mod)
    print()
    random_failures = run_randomized(mod)

    total = worked_failures + random_failures
    print()
    if total == 0:
        print("All good. Try multi_field_rate_limiter next (no fixed test cases — "
              "write your own against per_entity_rate_limiter as a 2-field special case).")
    else:
        print(f"{total} failing case(s) — see above.")
        sys.exit(1)


if __name__ == "__main__":
    main()

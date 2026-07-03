# System Design — the Hello Interview answering framework

> Source of truth for the **System Design 🏛️** deck in the Pattern Trainer.
> Adapted from [Hello Interview's Delivery Framework](https://www.hellointerview.com/learn/system-design/in-a-hurry/delivery).

System design interviews move fast (~35 min of design). The whole point of a
fixed framework is that you stop *deciding what to do next* and spend your brain
on the actual system. Drill the sequence until it's reflex, then apply it to
every question.

## The delivery framework — R · C · A · H · D

| # | Step | Time | What you produce |
|---|------|------|------------------|
| **R** | **Requirements** | ~5 min | **Functional** ("Users should be able to…") + **Non-functional** (the *-ilities*) + a rough capacity estimate |
| **C** | **Core Entities** | ~2 min | The nouns your API exchanges and your DB persists (User, Tweet, Ride…) |
| **A** | **API / Interface** | ~5 min | One endpoint per functional requirement (REST/RPC) |
| — | *(Data Flow)* | ~5 min | *Optional — only for data-pipeline / processing questions* |
| **H** | **High-Level Design** | ~10–15 min | Boxes & arrows that satisfy the **functional** requirements |
| **D** | **Deep Dives** | ~10 min | Attack the **non-functional** requirements, bottlenecks, and edge cases |

Say the acronym out loud at the start of every mock: **R‑C‑A‑H‑D**.

## R — Requirements (the part people rush and regret)

**Functional** = what the system *does*. Phrase as `Users should be able to…`.
Keep it to the 2–3 core features; park the rest under "out of scope."

**Non-functional** = *how well* it does it — the properties the deep dives will
defend. Walk this checklist and pick the 3–4 that actually bite:

- **Scale** — reads/writes per second, data volume, fan-out
- **Latency** — what has to feel instant (reads) vs. what can lag (writes/analytics)
- **Consistency vs. Availability** — where is stale data OK, where is it not (CAP)
- **Durability** — can we ever lose this data?
- **Read:write ratio** — usually read-heavy; it decides where caches/replicas go

**Capacity estimate** — only compute the numbers that *change a decision*
(e.g. "5 TB/day of writes → we need partitioning", "1 M RPS reads → CDN + cache").
Don't estimate for its own sake.

## C — Core Entities

Name the handful of entities before you design. They become your data model and
the payloads your API returns. ~2 minutes; a bulleted list is enough.

## A — API / Interface

One endpoint per functional requirement. Pick REST for CRUD-ish systems, RPC for
action-y ones, and note where you'd paginate, stream, or use websockets. Don't
gold-plate — a reasonable interface, then move on.

## H — High-Level Design

Draw the minimum set of components (client → gateway/LB → service → DB/cache/queue/
blob store) that makes every functional requirement work end-to-end. Trace one
request through the boxes. Resist deep-diving here — breadth first.

## D — Deep Dives

Now earn the level. Go back to the **non-functional** list and defend each one:
scaling a hot component, a caching or partitioning strategy, a queue for spikes,
consistency handling, a specific algorithm. This is where senior/staff signal lives.

---

### How this maps into the trainer

- **Framework-drill cards** — one card per step above; spaced repetition makes
  R‑C‑A‑H‑D and the requirements checklists automatic.
- **Design-question cards** — a canonical problem per card; the back is this
  framework *applied* at bullet depth. Reviewing = "can I walk R‑C‑A‑H‑D out loud
  for this question?" Rate yourself ✅ if you hit every step, 😵 if you stalled.

Both flow through the same spaced-repetition engine (boxes → 1/3/7/21/60 days),
XP, and streak as the DSA cards. See `system-design/deck.json` for the content.

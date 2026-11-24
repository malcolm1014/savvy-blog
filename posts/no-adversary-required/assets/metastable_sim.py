"""Toy model of a metastable failure in a load-balanced server fleet.
Savvy Security LLC. Illustrative only; parameters are not Microsoft's.

Each step is one minute. A fleet of N servers serves offered demand plus
retries. When per-server load exceeds capacity, servers can lock up and
drop out for RESTART minutes; their traffic is redistributed to the rest.
Policy A: naive clients retry every failed request immediately, and the
load balancer keeps shifting traffic onto whoever is left.
Policy B: clients back off with jitter and give up after a while, and
servers shed excess load (fast rejection) instead of accepting it.
"""
import random, json, sys

def run(policy, seed=7, steps=360):
    rnd = random.Random(seed)
    N, RESTART = 100, 25
    base = 0.72                       # steady utilisation of the full fleet
    down = {}                         # server -> minute it returns
    backlog = 0.0
    out = []
    for t in range(steps):
        # trigger window: +25% demand (failover) and 14% capacity offline
        trigger = 60 <= t < 120
        demand = N * base * (1.25 if trigger else 1.0)
        offline = int(0.14 * N) if trigger else 0
        for s in [s for s, r in down.items() if r <= t]:
            del down[s]
        healthy = N - offline - len(down)
        if policy == "A":
            retries = backlog * 1.0          # everyone retries at once
        else:
            retries = backlog * rnd.uniform(0.15, 0.35)  # jittered backoff
        offered = demand + retries
        per = offered / max(healthy, 1)
        if policy == "B" and per > 0.95:
            # admission control: accept up to 95%, reject the rest quickly
            accepted = 0.95 * healthy
            served = accepted
            failed = offered - accepted
        else:
            # lock contention: efficiency falls as load passes capacity
            eff = 1.0 if per <= 1.0 else 1.0 / (per ** 2)
            served = min(offered, healthy * eff * max(per, 1.0) if per > 1 else offered)
            served = min(served, healthy * 1.0)
            failed = offered - served
            if per > 1.0:
                pfail = min(0.5, 0.35 * (per - 1.0))
                for s in range(N):
                    if s in down or s < offline:
                        continue
                    if rnd.random() < pfail:
                        down[s] = t + RESTART
        if policy == "A":
            backlog = failed * 1.1            # timeouts spawn extra retries
        else:
            backlog = (backlog - retries) * 0.85 + failed * 0.6  # clients give up
        goodput = 100.0 * min(served, demand) / demand
        out.append({"t": t, "goodput": round(goodput, 1),
                    "healthy": healthy, "trigger": trigger})
    return out

if __name__ == "__main__":
    res = {p: run(p) for p in ("A", "B")}
    json.dump(res, open(sys.argv[1], "w"))
    for p in res:
        g = [r["goodput"] for r in res[p]]
        h = [r["healthy"] for r in res[p]]
        print(p, "min goodput", min(g), "goodput@t=200", g[200], "@300", g[300],
              "min healthy", min(h), "healthy@300", h[300])

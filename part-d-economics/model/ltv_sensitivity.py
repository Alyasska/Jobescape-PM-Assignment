#!/usr/bin/env python3
"""How sensitive is blended net LTV to the metrics the team actually optimises?

The PM's framing: gross profit, unsub % 12h/24h, rebill 0→1 and 1→2, and LTV are the primary
metrics — "but LTV is very insensitive, it rarely reacts to anything except the obvious."

This prices that statement using the company's own plan table: it moves each rebill transition
by one point at a time and reports what blended net LTV does. The answer decides how a Challenge
v2 should be *read*: on the fast, sensitive primary metrics, with LTV used to price the outcome
rather than to detect it.

    python3 ltv_sensitivity.py
"""
FEE = 0.12

PLANS = {
    "1-WEEK":  dict(mix=0.10, intro=6.93,  rec=39.99,
                    C=[.55, .50, .60, .75, .80, .80, .80, .80, .80, .80, .80, .80],
                    up1=(0.30, 1.99),  up2=(0.12, 0.99)),
    "4-WEEK":  dict(mix=0.70, intro=19.99, rec=39.99,
                    C=[.67, .65, .70, .75, .80, .80, .80, .80, .80, .80, .80, .80],
                    up1=(0.30, 69.99), up2=(0.12, 29.99)),
    "12-WEEK": dict(mix=0.20, intro=39.99, rec=62.99,
                    C=[.64, .57, .65, .75, .75, .75, .75, .75, .75, .75, .75, .75],
                    up1=(0.30, 69.99), up2=(0.12, 29.99)),
}


def net_ltv(p):
    s, acc = [], 1.0
    for c in p["C"]:
        acc *= c
        s.append(acc)
    gross = (p["intro"] + p["rec"] * sum(s)
             + p["up1"][0] * p["up1"][1] + p["up2"][0] * p["up2"][1])
    return gross * (1 - FEE)


def blended(plans):
    return sum(p["mix"] * net_ltv(p) for p in plans.values())


def bump(idx, delta):
    """Return blended net LTV with transition `idx` raised by `delta` on every plan."""
    out = {}
    for k, p in PLANS.items():
        q = dict(p)
        q["C"] = list(p["C"])
        q["C"][idx] = min(q["C"][idx] + delta, 1.0)
        out[k] = q
    return blended(out)


base = blended(PLANS)
print(f"baseline blended net LTV                     ${base:,.2f}\n")

print("SENSITIVITY — one point added to a single rebill transition, all plans")
print(f"  {'transition':<26}{'blended net LTV':>18}{'Δ':>10}{'Δ %':>9}")
print("  " + "-" * 61)
for idx, name in [(0, "C01  rebill period 0→1"), (1, "C12  rebill period 1→2"),
                  (2, "C23  rebill period 2→3")]:
    v = bump(idx, 0.01)
    print(f"  {name:<26}{'$' + format(v, ',.2f'):>18}{v-base:>+10.2f}{(v-base)/base:>+9.2%}")

print("\nSENSITIVITY — a realistic Challenge-v2 win: +2 points on BOTH C01 and C12")
q = {k: dict(p, C=[min(p["C"][0] + .02, 1), min(p["C"][1] + .02, 1)] + list(p["C"][2:]))
     for k, p in PLANS.items()}
v2 = blended(q)
print(f"  blended net LTV                            ${v2:,.2f}   ({v2-base:+.2f}, {(v2-base)/base:+.2%})")

print("\nAT SCALE — 1,000 new subscribers a day (the brief's stated volume)")
for label, d in [("+1 pt on C01", bump(0, .01) - base),
                 ("+2 pts on C01 and C12", v2 - base)]:
    print(f"  {label:<26} ${d*1000:>9,.0f} / day    ${d*1000*365:>13,.0f} / year")

print("""
READ-THROUGH
  A one-point move in the first rebill — a strong result for a single feature — moves blended net
  LTV by $1.31, about 1%. That is the PM's point made numerically: on one cohort, a 1% shift sits
  inside the sampling noise, so LTV will not tell you whether the feature worked.

  The same move is worth roughly $478,000 a year at 1,000 signups a day. So the money is large and
  the signal is faint at the same time — which is exactly the case for READING the test on unsub %
  12h/24h and rebill 0→1 (fast, sensitive, directly upstream of gross profit) and using LTV only to
  PRICE the result afterwards.""")

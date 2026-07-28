#!/usr/bin/env python3
"""
Part D — Subscription economics model (Jobescape PM take-home).

Task 1: Total Net LTV over a one-year horizon (per plan gross+net, blended).
Task 2: A/B plan-upgrade break-even (4-week -> 12-week upgrade replacing 2nd upsell).

Design decisions / assumptions (documented explicitly, per brief):
- Cohort of 1 subscriber per plan; everyone pays the intro (survival S0 = 1).
- Cmn = P(pay period n | survived to period m). Survival S_k = product of C01..C_{k-1,k}.
- Period 0 = intro (pays Intro Price). Periods 1..12 = recurring (pay Recurring Price),
  weighted by survival. The data supplies exactly 12 renewal transitions (C01..C1112).
- Payment-provider fee = 12% on ALL collected revenue (intro, recurring, upsells). Net = Gross * (1-0.12).
- Upsells are one-time at checkout; expected value = conv_rate * price, applied once to every subscriber.
- HORIZON: two readings are computed because the brief says "one-year horizon" but gives 12
  transitions per plan:
    (A) FULL-CURVE  : apply all 12 transitions to every plan (matches the data given; for the
                      4-week plan 13 periods x 4wk = exactly 52 weeks). PRIMARY.
    (B) STRICT-52WK : count only payments landing within 52 calendar weeks
                      (12-week plan -> only 4 recurring periods; others unchanged). SENSITIVITY.
"""

FEE = 0.12

plans = {
    "1-WEEK":  dict(mix=0.10, intro=6.93,  rec=39.99, rec_wk=4,  intro_wk=1,
                    C=[.55,.50,.60,.75,.80,.80,.80,.80,.80,.80,.80,.80],
                    up1=(0.30,1.99),  up2=(0.12,0.99)),
    "4-WEEK":  dict(mix=0.70, intro=19.99, rec=39.99, rec_wk=4,  intro_wk=4,
                    C=[.67,.65,.70,.75,.80,.80,.80,.80,.80,.80,.80,.80],
                    up1=(0.30,69.99), up2=(0.12,29.99)),
    "12-WEEK": dict(mix=0.20, intro=39.99, rec=62.99, rec_wk=12, intro_wk=12,
                    C=[.64,.57,.65,.75,.75,.75,.75,.75,.75,.75,.75,.75],
                    up1=(0.30,69.99), up2=(0.12,29.99)),
}

def survivals(C):
    s, acc = [], 1.0
    for c in C:
        acc *= c
        s.append(acc)          # s[k-1] = survival to recurring period k
    return s

def periods_within_year(intro_wk, rec_wk):
    """Recurring payments CHARGED within the 52-week horizon (strict reading).
    Recurring period k is charged at week intro_wk + (k-1)*rec_wk; count it if that
    charge falls inside the year (LTV = cash collected, so charge date is what counts,
    not whether the service period extends past week 52). Capped at the 12 given transitions.
    -> 12-week plan: charges at wk 12/24/36/48 -> 4 periods; 4-week & 1-week -> 12."""
    n = 0
    for k in range(1, 13):
        if intro_wk + (k - 1) * rec_wk < 52:
            n += 1
        else:
            break
    return n

def recurring_revenue(p, mode):
    s = survivals(p["C"])
    if mode == "full":
        k = 12
    else:
        k = periods_within_year(p["intro_wk"], p["rec_wk"])
    return p["rec"] * sum(s[:k]), k

def upsell_ev(p):
    return p["up1"][0]*p["up1"][1] + p["up2"][0]*p["up2"][1]

def plan_ltv(p, mode):
    rec_rev, k = recurring_revenue(p, mode)
    sub_gross = p["intro"] + rec_rev
    up = upsell_ev(p)
    gross = sub_gross + up
    return dict(k=k, intro=p["intro"], rec_rev=rec_rev, upsell=up,
                gross=gross, net=gross*(1-FEE))

print("="*72)
print("TASK 1 — LTV per plan (1-year horizon).  Fee = 12%.")
for mode, label in [("full","(A) FULL-CURVE  [PRIMARY]"), ("strict","(B) STRICT-52WK [sensitivity]")]:
    print(f"\n--- Horizon reading {label} ---")
    print(f"{'plan':8} {'mix':>5} {'recPds':>6} {'intro':>7} {'recRev':>8} {'upsell':>7} {'GROSS':>8} {'NET':>8}")
    blended = 0.0
    for name, p in plans.items():
        r = plan_ltv(p, mode)
        blended += p["mix"]*r["net"]
        print(f"{name:8} {p['mix']*100:4.0f}% {r['k']:6d} {r['intro']:7.2f} {r['rec_rev']:8.2f} {r['upsell']:7.2f} {r['gross']:8.2f} {r['net']:8.2f}")
    print(f"{'BLENDED NET LTV (mix-weighted)':>55}: ${blended:6.2f}")

print("\n"+"="*72)
print("TASK 2 — A/B: 4-week buyer offered Plan Upgrade ($49.99) INSTEAD of 2nd upsell.")
print("Upgrade buyer becomes a 12-week subscriber (12-week recurring economics).")
UP_PRICE = 49.99
for mode, label in [("full","FULL-CURVE"), ("strict","STRICT-52WK")]:
    p4, p12 = plans["4-WEEK"], plans["12-WEEK"]
    recRev4,_  = recurring_revenue(p4, mode)
    recRev12,_ = recurring_revenue(p12, mode)
    up2_4 = p4["up2"][0]*p4["up2"][1]                 # expected 2nd-upsell value being replaced
    # Break-even p*: p*(UP_PRICE + recRev12 - recRev4) = up2_4   (intro & 1st upsell cancel; fee uniform)
    denom = UP_PRICE + recRev12 - recRev4
    p_star = up2_4 / denom
    print(f"\n--- {label} ---")
    print(f"  recurring rev 4-week  = ${recRev4:6.2f}")
    print(f"  recurring rev 12-week = ${recRev12:6.2f}  (delta vs 4wk = ${recRev12-recRev4:+.2f})")
    print(f"  2nd-upsell value replaced (0.12*29.99) = ${up2_4:.2f}")
    print(f"  each upgrade adds ${denom:.2f} gross; cannibalises ${up2_4:.2f}")
    print(f"  >> BREAK-EVEN upgrade conversion p* = {p_star*100:.2f}%")
    # sample scenarios
    ctrl_gross = p4["intro"] + recRev4 + p4["up1"][0]*p4["up1"][1] + up2_4
    print(f"  control 4-week gross LTV = ${ctrl_gross:.2f} (net ${ctrl_gross*(1-FEE):.2f})")
    for p in (0.05,0.10,0.20,0.30):
        test_gross = (p4["intro"] + p4["up1"][0]*p4["up1"][1]
                      + (1-p)*recRev4 + p*(UP_PRICE + recRev12))
        lift = (test_gross-ctrl_gross)/ctrl_gross*100
        print(f"     p={p*100:4.0f}%  test gross LTV ${test_gross:7.2f}  net ${test_gross*(1-FEE):7.2f}  lift {lift:+5.1f}%")

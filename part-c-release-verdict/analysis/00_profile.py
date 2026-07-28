"""Quick profile of the comparison-groups export (query 13). Read-only, streaming, no pandas."""
import csv, os
from collections import Counter, defaultdict

CSV = os.path.join(os.path.dirname(__file__), "..", "data", "bquxjob_4ff8f8f_19fa4473200.csv")

rows = []
with open(CSV) as f:
    for r in csv.DictReader(f):
        rows.append(r)

print(f"rows: {len(rows)}")


def i(r, k):
    v = r.get(k, "")
    return int(v) if v not in ("", None) else 0


def f_(r, k):
    v = r.get(k, "")
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


# --- data-quality / coverage checks -------------------------------------------------
print("\n== coverage ==")
print("has_subscription=1:", sum(i(r, "has_subscription") for r in rows))
print("days_observed >= 7:", sum(1 for r in rows if i(r, "days_observed") >= 7))
print("days_observed >= 3:", sum(1 for r in rows if i(r, "days_observed") >= 3))
print("days_observed >= 1:", sum(1 for r in rows if i(r, "days_observed") >= 1))

do = Counter(i(r, "days_observed") for r in rows)
print("days_observed distribution (0-10):", {k: do[k] for k in range(0, 11)})
print("max days_observed:", max(do))

print("\nfirst_seen range:", min(r["first_seen"] for r in rows), "→", max(r["first_seen"] for r in rows))
ch = [r["ch_start_date"] for r in rows if r["ch_start_date"]]
print("ch_start_date range:", min(ch), "→", max(ch), f"(n={len(ch)})")

print("\n== group sizes ==")
g = Counter(r["group_338"] for r in rows)
for k, v in g.most_common():
    print(f"  {k:28s} {v:5d}  ({v/len(rows):.1%})")

print("\n== exposure funnel (whole population) ==")
for k in ["saw_challenge_popup", "clicked_challenge_popup", "viewed_any_challenge",
          "started_any_challenge", "finished_onboarding", "started_personal_plan"]:
    n = sum(i(r, k) for r in rows)
    print(f"  {k:26s} {n:5d}  ({n/len(rows):.1%})")

print("\n== challenge-338 lesson-completion histogram (takers only) ==")
h = Counter(i(r, "ch_lessons_completed") for r in rows if r["group_338"] == "took_338")
tot = sum(h.values())
cum = 0
for k in sorted(h):
    cum += h[k]
    print(f"  {k} lessons: {h[k]:5d}  ({h[k]/tot:6.1%})   cum {cum/tot:6.1%}")

print("\n== segment field fill-rates (non-empty) ==")
for k in ["age", "gender", "goal", "status", "plan", "country_code", "unsub_reason"]:
    n = sum(1 for r in rows if r.get(k))
    print(f"  {k:14s} {n:5d}  ({n/len(rows):.1%})")

print("\n== plan mix (subscribers) ==")
for k, v in Counter(r["plan"] for r in rows if r["plan"]).most_common():
    print(f"  {k:10s} {v:5d}")

print("\n== unsubscribed ==")
print("  total unsubscribed:", sum(i(r, "unsubscribed") for r in rows))
print("  among subscribers:", sum(i(r, "unsubscribed") for r in rows if i(r, "has_subscription")))

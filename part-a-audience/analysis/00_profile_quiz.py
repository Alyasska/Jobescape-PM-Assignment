#!/usr/bin/env python3
"""Part A — profile the quiz export before any segmentation is attempted.

Answers the questions that decide whether clustering is even possible:
  - how many users, how many questions, which version dominates
  - per-question coverage (a clustering feature must be asked of nearly everyone)
  - the answer cardinality of each question
  - the outcome columns (sub / unsub / upsell), which let clusters be validated
    against behaviour rather than against the analyst's intuition

Pure standard library — this machine has no pandas.

    python3 00_profile_quiz.py
"""
import csv
import collections
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "materials", "quiz-funnel-answers", "Quiz Funnel Answers.csv")
csv.field_size_limit(10_000_000)


def main():
    users = set()
    q_users = collections.defaultdict(set)      # question_text -> users asked
    q_answers = collections.defaultdict(collections.Counter)
    versions = collections.Counter()
    geos = collections.Counter()
    outcome = {}                                # user -> (sub, unsub, upsell)
    user_version = {}
    rows = 0

    with open(SRC, encoding="utf-8-sig", newline="") as fh:
        for r in csv.DictReader(fh):
            rows += 1
            u = r["epv_user_id"]
            users.add(u)
            qt = (r["question_text"] or "").strip()
            ans = (r["question_answer"] or "").strip()
            if qt:
                q_users[qt].add(u)
                if ans:
                    q_answers[qt][ans] += 1
            versions[r["quiz_version"]] += 1
            geos[r["geo"]] += 1
            user_version[u] = r["quiz_version"]
            # outcome flags repeat on every row for a user; last write wins, they are constant
            outcome[u] = (r["sub"], r["unsub"], r["upsell"])

    n = len(users)
    print(f"rows           {rows:,}")
    print(f"users          {n:,}")
    print(f"questions      {len(q_users):,}")

    print("\n=== quiz_version (by row) ===")
    for v, c in versions.most_common(6):
        print(f"  {v:12} {c:9,}  {c/rows*100:5.1f}%")

    print("\n=== geo (by row) ===")
    for g, c in geos.most_common(6):
        print(f"  {str(g):12} {c:9,}  {c/rows*100:5.1f}%")

    subs = sum(1 for v in outcome.values() if v[0] == "1")
    unsubs = sum(1 for v in outcome.values() if v[1] == "1")
    ups = sum(1 for v in outcome.values() if v[2] == "1")
    print("\n=== outcomes (per user) ===")
    print(f"  subscribed   {subs:6,}  {subs/n*100:5.2f}%")
    print(f"  unsubscribed {unsubs:6,}  {unsubs/n*100:5.2f}%  "
          f"({unsubs/subs*100:.1f}% of subscribers)" if subs else "")
    print(f"  upsell       {ups:6,}  {ups/n*100:5.2f}%")

    print("\n=== questions by coverage (share of all users asked) ===")
    ranked = sorted(q_users.items(), key=lambda kv: -len(kv[1]))
    for qt, us in ranked[:40]:
        cov = len(us) / n * 100
        card = len(q_answers[qt])
        flag = "  <-- usable" if cov >= 60 and 2 <= card <= 15 else ""
        print(f"  {cov:5.1f}%  card={card:3}  {qt[:78]}{flag}")

    print(f"\n({len(ranked)} questions total; showing top 40 by coverage)")


if __name__ == "__main__":
    sys.exit(main())

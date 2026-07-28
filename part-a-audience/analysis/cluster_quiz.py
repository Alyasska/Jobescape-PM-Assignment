#!/usr/bin/env python3
"""Part A — derive audience segments from the quiz data instead of asserting them.

WHY THIS EXISTS
    `segment_sizer.py` applied a hand-written if/elif rule chain: the six segments were authored
    from a jobs-to-be-done framework and then counted, with unmatched users falling through to a
    default. That is a taxonomy, not a segmentation — the structure came from the analyst, not the
    data, so it cannot be falsified. This script asks the opposite question: if nobody told the
    data what the segments were, how many groups are actually there, and what are they?

METHOD
    k-modes (Huang, 1998) on the categorical quiz answers.
      · Distance is Hamming — the count of questions two users answered differently.
      · Centroids are per-attribute MODES, not means. k-means is wrong here: a mean over nominal
        levels ("35-44", "Business owner") has no meaning, and one-hot + Euclidean silently
        asserts that every pair of levels is equidistant, which is the assumption under test.
      · Missing answers are kept as their own level. In a 26-step quiz funnel, *not answering*
        is behaviour (where someone dropped), not absent data — discarding it would bias the
        sample toward finishers.
      · k chosen by the elbow in within-cluster cost, cross-checked against interpretability.
      · Multiple restarts per k; the best-cost run wins. Seeded, so it reproduces exactly.

READ THE OUTPUT AS
    cluster profiles are reported by LIFT (share inside the cluster ÷ share in the population),
    not by raw share. The modal answer of a cluster is usually just the modal answer of the whole
    population; what makes a cluster a cluster is what it over-represents.
"""
import collections
import csv
import os
import random
import sys

random.seed(42)
csv.field_size_limit(10 ** 7)

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "materials", "quiz-funnel-answers", "Quiz Funnel Answers.csv")

# The questions that carry motive or identity. Chosen for coverage (>25k answers each) and
# because each maps to something a PM could act on. IDs are the `ID` column, not `question_id`
# (which is 0 for every row in this export).
CORE = {
    "391":  "age",
    "357":  "gender",
    "394":  "work_status",
    "331":  "learn_claude_for",
    "390":  "benefit",
    "332":  "ai_experience",
    "336":  "career_fear",
    "335":  "feels_ready",
    "1241": "used_claude",
    "1426": "field",
}
MIN_ANSWERED = 6          # users answering fewer than this are quiz drop-offs, not segments
NA = "(no answer)"


def load():
    """Pivot the long export (one row per user-question) into one row per user."""
    wide = collections.defaultdict(dict)
    with open(SRC, encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            qid = r["ID"]
            if qid in CORE:
                a = r["question_answer"].strip()
                if a:
                    wide[r["epv_user_id"]][CORE[qid]] = a
    cols = list(CORE.values())
    rows = [[u.get(c, NA) for c in cols] for u in wide.values()]
    kept = [r for r in rows if sum(v != NA for v in r) >= MIN_ANSWERED]
    return cols, rows, kept


def cost(rows, modes, assign):
    return sum(sum(a != b for a, b in zip(rows[i], modes[assign[i]])) for i in range(len(rows)))


def kmodes(rows, k, iters=12, restarts=4):
    best = None
    m = len(rows[0])
    for _ in range(restarts):
        modes = [list(r) for r in random.sample(rows, k)]
        assign = [0] * len(rows)
        for _ in range(iters):
            moved = False
            for i, r in enumerate(rows):
                d = [sum(a != b for a, b in zip(r, mo)) for mo in modes]
                new = d.index(min(d))
                if new != assign[i]:
                    assign[i] = new
                    moved = True
            for c in range(k):
                members = [rows[i] for i in range(len(rows)) if assign[i] == c]
                if not members:
                    modes[c] = list(random.choice(rows))
                    continue
                modes[c] = [collections.Counter(mem[j] for mem in members).most_common(1)[0][0]
                            for j in range(m)]
            if not moved:
                break
        c = cost(rows, modes, assign)
        if best is None or c < best[0]:
            best = (c, modes, assign[:])
    return best


def main():
    cols, allrows, rows = load()
    n = len(rows)
    print(f"quiz respondents in export        {len(allrows):,}")
    print(f"answered >= {MIN_ANSWERED} of {len(cols)} core questions  {n:,}  "
          f"({n/len(allrows)*100:.1f}%)  <- the clustering sample\n")

    base = [collections.Counter(r[j] for r in rows) for j in range(len(cols))]

    print("== choosing k: within-cluster Hamming cost ==")
    print("   k     cost   cost/user   improvement")
    prev = None
    results = {}
    for k in range(2, 9):
        c, modes, assign = kmodes(rows, k)
        results[k] = (c, modes, assign)
        imp = f"{(prev-c)/prev*100:5.1f}%" if prev else "    —"
        print(f"  {k:>2}  {c:>7,}   {c/n:>8.3f}   {imp}")
        prev = c

    k = int(sys.argv[1]) if len(sys.argv) > 1 else 6
    c, modes, assign = results[k]
    sizes = collections.Counter(assign)
    print(f"\n== k = {k} · cluster profiles (lift = share in cluster / share in population) ==")
    for cl, sz in sizes.most_common():
        members = [rows[i] for i in range(n) if assign[i] == cl]
        print(f"\n  ── cluster {cl}  n = {sz:,}  ({sz/n*100:.1f}%)")
        marks = []
        for j, col in enumerate(cols):
            cnt = collections.Counter(m[j] for m in members)
            for val, v in cnt.most_common(3):
                if val == NA:
                    continue
                share = v / sz
                pop = base[j][val] / n
                if pop > 0 and share > .18:
                    marks.append((share / pop, col, val, share))
        for lift, col, val, share in sorted(marks, reverse=True)[:6]:
            print(f"      {lift:4.2f}x  {share*100:4.1f}%  {col:16} {val[:52]}")


if __name__ == "__main__":
    main()

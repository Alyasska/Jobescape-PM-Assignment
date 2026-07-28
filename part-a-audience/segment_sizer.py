#!/usr/bin/env python3
"""
Part A — size the 6 audience segments from the real quiz-answer export.

WHEN YOU HAVE THE DATA (Drive → "Quiz Funnel Answers", H1):
  1. Export/save it as CSV (one row per user) into  materials/quiz-answers.csv
  2. Map the real column names to the FIELDS dict below (they should match the quiz
     variables decoded in materials/quiz-map.md: age, gender, status, goal,
     career_scares, experience_ai, long_fix, ...).
  3. Run:  python3 segment_sizer.py materials/quiz-answers.csv

Output: each segment's size (count + %), plus an age×goal crosstab and overlap notes.
This turns the *framework* in 01-segments.md into the actual *distribution*.
"""
import csv, sys, collections

# --- map these to the real CSV headers if they differ -------------------------
FIELDS = dict(age="age", gender="gender", status="status", goal="goal",
              career_scares="career_scares", experience_ai="experience_ai",
              long_fix="long_fix")

def has(v, *subs):  # case-insensitive substring match, tolerant of option wording
    v = (v or "").lower()
    return any(s in v for s in subs)

# --- segment rules, applied in PRIORITY order (first match wins) --------------
# rationale in 01-segments.md: emotion/JTBD first, demographics as descriptors.
def classify(r):
    g = lambda k: r.get(FIELDS[k], "")
    if has(g("long_fix"), "every time", "sometimes", "as long fixing"):
        return "Burned Time-Poor Doer"
    if has(g("experience_ai"), "haven't", "havent", "not really tried") and has(g("gender"), "female"):
        return "Low-Confidence Re-entrant"
    if has(g("age"), "35-44", "45-54") and has(g("career_scares"), "falling behind", "replaced", "losing"):
        return "Anxious Catch-Up Pro"
    if has(g("age"), "18-24") or has(g("status"), "exploring", "between jobs", "switcher"):
        return "Gen Z / Early Striver"
    if has(g("goal"), "promotion", "better job", "earn more"):
        return "Ambitious Climber"
    if has(g("status"), "business owner", "freelancer", "self-employed"):
        return "Role Specialist"
    return "Anxious Catch-Up Pro"   # sensible default: the modal fear-driven buyer

def main(path):
    rows = list(csv.DictReader(open(path, encoding="utf-8-sig")))
    if not rows:
        print("No rows found. Check the CSV path/format."); return
    seg = collections.Counter()
    crosstab = collections.Counter()
    for r in rows:
        s = classify(r); seg[s] += 1
        crosstab[(r.get(FIELDS["age"], "?"), r.get(FIELDS["goal"], "?"))] += 1
    n = len(rows)
    print(f"\nN = {n} quiz respondents\n=== Segment sizing ===")
    for s, c in seg.most_common():
        print(f"  {s:26} {c:6}  {c/n*100:5.1f}%")   # % of total
    print("\n=== age × goal crosstab (top 15) ===")
    for (a, gl), c in crosstab.most_common(15):
        print(f"  {a:8} | {gl:34} {c:6}")
    print("\nNote: rules are in classify(); adjust option wording to match the real export.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(0)
    main(sys.argv[1])

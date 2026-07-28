-- Part C · Step 3 — Same metrics, cut by segment (age / profession / plan) + the selection guard.
-- ⚠ADJUST names. Quiz answers (age, status/profession, goal) live on the user/subscribe record or
-- in early app_events params — confirm where in 00.

-- 3a) Metrics by demographic segment × engagement tier
WITH base AS (
  SELECT t.user_id, t.engagement_tier,
         s.age, s.profession, s.plan,                 -- ⚠ADJUST source of quiz demographics
         r.d1, r.unsubscribed, t.days_completed
  FROM `persona-496908.<dataset>.v_challenge_metrics_user` t   -- ⚠ a per-user view joining 01+02
  LEFT JOIN `persona-496908.<dataset>.subscribe_events` s USING(user_id)
  LEFT JOIN `persona-496908.<dataset>.v_challenge_ret` r USING(user_id)
)
SELECT age, plan, engagement_tier,
       COUNT(*) users,
       ROUND(AVG(CAST(d1 AS INT64)),3) d1_retention,
       ROUND(AVG(CAST(unsubscribed AS INT64)),3) unsubscribe_rate
FROM base
GROUP BY age, plan, engagement_tier
ORDER BY age, plan, engagement_tier;

-- 3b) THE SELECTION GUARD — dose-response: does each EXTRA challenge day predict lower unsubscribe?
-- If the slope is smooth and monotonic, the effect is more plausibly causal than pure self-selection.
SELECT days_completed,
       COUNT(*) users,
       ROUND(AVG(CAST(unsubscribed AS INT64)),3) unsubscribe_rate,
       ROUND(AVG(CAST(d1 AS INT64)),3) d1_retention
FROM `persona-496908.<dataset>.v_challenge_metrics_user`        -- ⚠ per-user view
GROUP BY days_completed
ORDER BY days_completed;

-- 3c) IDEAL (if a hold-out or pre-launch cohort exists): compare Challenge-exposed vs not,
-- matched on entry motivation (quiz time_goal / goal). If no hold-out exists, the #1
-- recommendation for the next release is to ship the Challenge as a proper A/B, not 100%.

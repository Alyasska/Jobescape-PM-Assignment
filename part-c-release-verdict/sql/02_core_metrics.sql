-- Part C · Step 2 — The core table: target + secondary metrics BY engagement tier.
-- Depends on the tiering in 01. ⚠ADJUST names to the real schema.
-- D1/D3/D7 retention are measured relative to each user's challenge-start day.

DECLARE challenge_id STRING DEFAULT '338';

WITH tiers AS (
  -- paste/inline the SELECT from 01_engagement_tiers.sql, or save it as a view and reference it
  SELECT * FROM `persona-496908.<dataset>.v_challenge_tiers`     -- ⚠ create this view from 01
),
starts AS (
  SELECT user_id, DATE(MIN(TIMESTAMP(event_timestamp))) AS d0    -- ⚠ADJUST
  FROM `persona-496908.<dataset>.app_events`
  WHERE event_name='challenge_start'                              -- ⚠ADJUST
  GROUP BY user_id
),
activity AS (
  SELECT DISTINCT user_id, DATE(TIMESTAMP(event_timestamp)) AS d  -- any app activity = "retained that day"
  FROM `persona-496908.<dataset>.app_events`
),
ret AS (
  SELECT s.user_id,
    MAX(a.d = DATE_ADD(s.d0, INTERVAL 1 DAY)) AS d1,
    MAX(a.d = DATE_ADD(s.d0, INTERVAL 3 DAY)) AS d3,
    MAX(a.d = DATE_ADD(s.d0, INTERVAL 7 DAY)) AS d7
  FROM starts s LEFT JOIN activity a USING(user_id)
  GROUP BY s.user_id
),
unsub AS (
  SELECT user_id, MAX(is_cancelled) AS unsubscribed              -- ⚠ADJUST: from subscribe_events
  FROM `persona-496908.<dataset>.subscribe_events`               --   e.g. status='cancelled' / cancel_at IS NOT NULL
  GROUP BY user_id
)
SELECT
  t.engagement_tier,
  COUNT(*)                                          AS users,
  ROUND(AVG(CAST(r.d1 AS INT64)),3)                 AS d1_retention,   -- TARGET METRIC
  ROUND(AVG(CAST(r.d3 AS INT64)),3)                 AS d3_retention,
  ROUND(AVG(CAST(r.d7 AS INT64)),3)                 AS d7_retention,
  ROUND(AVG(CAST(COALESCE(u.unsubscribed,false) AS INT64)),3) AS unsubscribe_rate,
  ROUND(AVG(t.days_completed)/7.0,3)                AS lesson_completion  -- of the 7 days
FROM tiers t
LEFT JOIN ret r USING(user_id)
LEFT JOIN unsub u USING(user_id)
GROUP BY t.engagement_tier
ORDER BY CASE t.engagement_tier WHEN 'high' THEN 1 WHEN 'low' THEN 2 ELSE 3 END;

-- READ IT LIKE THIS: the release "worked" only if there is a smooth dose-response
-- (high < low < none on unsubscribe; high > low > none on D1/D3/D7) that survives the
-- baseline/hold-out check in 03. A high-vs-none gap alone can be pure selection.

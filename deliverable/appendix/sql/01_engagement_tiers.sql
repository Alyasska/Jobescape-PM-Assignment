-- Part C · Step 1 — Classify each Challenge-eligible user into an engagement tier.
-- ⚠ADJUST all names marked below to the real schema found in 00_explore_schema.sql.
-- Tiers:  high = started AND (reached >=Day3 OR returned on >=3 of first 7 days)
--         low  = started but stalled before Day 3
--         none = eligible but never opened Day 1

DECLARE challenge_id STRING DEFAULT '338';           -- the Challenge in the brief (skills/challenges/338)

WITH ev AS (
  SELECT
    user_id,                                          -- ⚠ADJUST
    event_name,                                       -- ⚠ADJUST
    TIMESTAMP(event_timestamp) AS ts,                 -- ⚠ADJUST
    DATE(TIMESTAMP(event_timestamp)) AS d,
    SAFE_CAST(JSON_VALUE(event_params, '$.challenge_id') AS STRING) AS ch  -- ⚠ADJUST (may be a column)
  FROM `persona-496908.<dataset>.app_events`
),
challenge AS (                                        -- events belonging to THIS challenge
  SELECT * FROM ev WHERE ch = challenge_id OR ch IS NULL   -- drop the OR NULL once the field is confirmed
),
per_user AS (
  SELECT
    user_id,
    MIN(IF(event_name='challenge_start', ts, NULL))                      AS started_at,     -- ⚠ADJUST event
    COUNTIF(event_name='challenge_day_complete')                          AS days_completed, -- ⚠ADJUST event
    COUNT(DISTINCT IF(event_name='challenge_day_complete', d, NULL))      AS distinct_active_days,
    MIN(d) AS first_day, MAX(d) AS last_day
  FROM challenge
  GROUP BY user_id
)
SELECT
  user_id,
  started_at IS NOT NULL AS started,
  days_completed,
  distinct_active_days,
  CASE
    WHEN started_at IS NULL THEN 'none'
    WHEN days_completed >= 3 OR distinct_active_days >= 3 THEN 'high'
    ELSE 'low'
  END AS engagement_tier
FROM per_user;

-- Sanity: the tier distribution (use this histogram to calibrate the Day-3 threshold)
-- SELECT engagement_tier, COUNT(*) FROM ( <the query above> ) GROUP BY 1;

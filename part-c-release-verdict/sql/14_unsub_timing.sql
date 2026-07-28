-- 14 · UNSUB % AT 12h / 24h — the team's actual PRIMARY metric.
-- The PM's hierarchy puts gross profit, unsub % 12h/24h and rebill 0→1 / 1→2 first; D1 is secondary.
-- My earlier export (query 13) returned the unsubscribe FLAG but not its TIMESTAMP, so 12h/24h was
-- not computable. This closes that gap — it is the one query that would let me report the release
-- against the metric the business actually runs on.
--
-- Run it, then "SAVE RESULTS ▸ CSV (local file)" into part-c-release-verdict/data/.
-- ~10,000 rows. All tiering and significance testing happens locally in Python, as before.
-- If it errors, paste me the error text verbatim.

WITH
sub AS (                                      -- first purchase per user = the clock starts here
  SELECT
    user_id,
    MIN(timestamp)                AS subscribed_at,
    ANY_VALUE(subscription)       AS plan,
    ANY_VALUE(age)                AS age,
    ANY_VALUE(gender)             AS gender,
    ANY_VALUE(goal)               AS goal,
    ANY_VALUE(status)             AS status
  FROM `persona-496908.sql_assessment.subscribe_events`
  GROUP BY user_id
),

unsub AS (                                    -- first unsubscribe per user
  SELECT
    user_id,
    MIN(timestamp)                                        AS unsubscribed_at,
    ANY_VALUE(unsubscribe_reason)                         AS unsub_reason
  FROM `persona-496908.sql_assessment.app_events`
  WHERE event_name = 'pr_webapp_unsubscribed'
  GROUP BY user_id
),

ch AS (                                       -- challenge-338 engagement, same definition as query 13
  SELECT
    user_id,
    MIN(IF(event_name = 'pr_webapp_challenge_start', DATE(timestamp), NULL))     AS ch_start_date,
    MAX(IF(event_name = 'pr_webapp_challenge_view', 1, 0))                       AS ch_viewed,
    MAX(IF(event_name = 'pr_webapp_challenge_join', 1, 0))                       AS ch_joined,
    COUNTIF(event_name = 'pr_webapp_lesson_completed')                           AS ch_lessons_completed
  FROM `persona-496908.sql_assessment.app_events`
  WHERE course_id = 338 OR REGEXP_CONTAINS(IFNULL(path, ''), r'challenges/338')
  GROUP BY user_id
),

popup AS (                                    -- exposure to the challenge surface (popup carries no id)
  SELECT
    user_id,
    MAX(IF(event_name = 'pr_webapp_challenge_popup_view', 1, 0))  AS saw_popup,
    MAX(IF(event_name = 'pr_webapp_challenge_view', 1, 0))        AS viewed_any_challenge
  FROM `persona-496908.sql_assessment.app_events`
  GROUP BY user_id
),

renew AS (                                    -- rebill signal, such as it is (only ~17 events exist)
  SELECT user_id, COUNT(*) AS renewals
  FROM `persona-496908.sql_assessment.app_events`
  WHERE event_name = 'pr_webapp_subscription_renewed'
  GROUP BY user_id
)

SELECT
  s.user_id,
  s.plan, s.age, s.gender, s.goal, s.status,
  s.subscribed_at,
  u.unsubscribed_at,
  u.unsub_reason,

  -- THE PRIMARY METRIC: hours from purchase to unsubscribe
  IF(u.unsubscribed_at IS NULL, NULL,
     TIMESTAMP_DIFF(u.unsubscribed_at, s.subscribed_at, HOUR))        AS hours_to_unsub,
  IF(u.unsubscribed_at IS NULL, 0,
     IF(TIMESTAMP_DIFF(u.unsubscribed_at, s.subscribed_at, HOUR) <= 12, 1, 0)) AS unsub_12h,
  IF(u.unsubscribed_at IS NULL, 0,
     IF(TIMESTAMP_DIFF(u.unsubscribed_at, s.subscribed_at, HOUR) <= 24, 1, 0)) AS unsub_24h,
  IF(u.unsubscribed_at IS NULL, 0, 1)                                 AS unsub_ever,

  -- the engagement tiers, so the primary metric can be cut the same way as query 13
  CASE
    WHEN c.ch_start_date IS NOT NULL THEN 'took_338'
    WHEN c.ch_joined = 1             THEN 'joined_338_never_started'
    WHEN c.ch_viewed  = 1            THEN 'viewed_338_never_joined'
    ELSE                                  'no_challenge'
  END                                                                 AS group_338,
  IFNULL(c.ch_lessons_completed, 0)                                   AS ch_lessons_completed,
  IFNULL(p.saw_popup, 0)                                              AS saw_popup,
  IFNULL(p.viewed_any_challenge, 0)                                   AS viewed_any_challenge,

  IFNULL(r.renewals, 0)                                               AS renewals
FROM sub s
LEFT JOIN unsub  u USING (user_id)
LEFT JOIN ch     c USING (user_id)
LEFT JOIN popup  p USING (user_id)
LEFT JOIN renew  r USING (user_id)
ORDER BY s.user_id;

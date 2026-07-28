-- 13 · THE COMPARISON QUERY — one row per user, takers AND non-takers of Challenge 338.
-- This is the missing third of Part C Task 1: "high / low / didn't take it".
-- Run it once, then "SAVE RESULTS ▸ CSV (local file)" into part-c-release-verdict/data/.
-- ~10,000 rows (small enough for the local-file download). All tiering + stats done locally in Python.
-- If it errors, paste me the error text verbatim.

WITH
bounds AS (                                   -- last day present in the data (for window correction)
  SELECT MAX(DATE(timestamp)) AS last_data_date
  FROM `persona-496908.sql_assessment.app_events`
),

ev AS (                                       -- every app event + a flag for "belongs to challenge 338"
  SELECT
    user_id,
    event_name,
    DATE(timestamp) AS d,
    csat_score,
    unsubscribe_reason,
    country_code,
    (course_id = 338 OR REGEXP_CONTAINS(IFNULL(path,''), r'challenges/338')) AS ch338
  FROM `persona-496908.sql_assessment.app_events`
),

per_user AS (                                 -- one row per user: engagement, outcomes, challenge-338 detail
  SELECT
    user_id,
    MIN(d)                                                              AS first_seen,
    COUNT(DISTINCT d)                                                   AS active_days_total,
    ANY_VALUE(country_code)                                             AS country_code,

    -- overall product engagement (all courses, not just the challenge)
    COUNTIF(event_name = 'pr_webapp_lesson_completed')                  AS lessons_completed_all,
    MAX(IF(event_name = 'pr_webapp_onboarding_finished', 1, 0))         AS finished_onboarding,
    MAX(IF(event_name = 'pr_webapp_personal_plan_started', 1, 0))       AS started_personal_plan,

    -- outcome metrics
    MAX(IF(event_name = 'pr_webapp_unsubscribed', 1, 0))                AS unsubscribed,
    ANY_VALUE(IF(event_name = 'pr_webapp_unsubscribed', unsubscribe_reason, NULL)) AS unsub_reason,
    COUNTIF(event_name IN ('pr_webapp_lesson_csat_click',
                           'pr_webapp_module_csat_click',
                           'pr_webapp_challenge_csat_click'))           AS csat_n_all,
    AVG(IF(event_name IN ('pr_webapp_lesson_csat_click',
                          'pr_webapp_module_csat_click',
                          'pr_webapp_challenge_csat_click'), csat_score, NULL)) AS avg_csat_all,

    -- exposure to the challenge surface (any challenge — the popup carries no course_id)
    MAX(IF(event_name = 'pr_webapp_challenge_popup_view', 1, 0))        AS saw_challenge_popup,
    MAX(IF(event_name = 'pr_webapp_challenge_popup_click', 1, 0))       AS clicked_challenge_popup,
    MAX(IF(event_name = 'pr_webapp_challenge_view', 1, 0))              AS viewed_any_challenge,
    MAX(IF(event_name = 'pr_webapp_challenge_start', 1, 0))             AS started_any_challenge,

    -- challenge 338 specifically
    MIN(IF(ch338 AND event_name = 'pr_webapp_challenge_start', d, NULL)) AS ch_start_date,
    MAX(IF(ch338 AND event_name = 'pr_webapp_challenge_view', 1, 0))     AS ch_viewed,
    MAX(IF(ch338 AND event_name = 'pr_webapp_challenge_join', 1, 0))     AS ch_joined,
    COUNTIF(ch338 AND event_name = 'pr_webapp_lesson_completed')         AS ch_lessons_completed,
    COUNTIF(ch338 AND event_name = 'pr_webapp_lesson_started')           AS ch_lessons_started,
    MAX(IF(ch338 AND event_name = 'pr_webapp_course_completed', 1, 0))   AS ch_completed_course,
    MAX(IF(ch338 AND event_name IN ('pr_webapp_challenge_certificate_download',
                                    'pr_webapp_challenge_certificate_share'), 1, 0)) AS ch_certificate,
    COUNTIF(ch338 AND event_name IN ('pr_webapp_lesson_csat_click',
                                     'pr_webapp_challenge_csat_click'))  AS ch_csat_n,
    AVG(IF(ch338 AND event_name IN ('pr_webapp_lesson_csat_click',
                                    'pr_webapp_challenge_csat_click'), csat_score, NULL)) AS ch_avg_csat
  FROM ev
  GROUP BY user_id
),

anchored AS (                                 -- day 0 for retention: challenge start for takers, first app day for everyone else
  SELECT
    p.*,
    COALESCE(p.ch_start_date, p.first_seen) AS anchor_date
  FROM per_user p
),

days AS (                                     -- distinct active days per user
  SELECT DISTINCT user_id, DATE(timestamp) AS d
  FROM `persona-496908.sql_assessment.app_events`
),

ret AS (                                      -- retention off BOTH anchors, so takers and non-takers are comparable
  SELECT
    a.user_id,
    MAX(IF(dd.d = DATE_ADD(a.anchor_date, INTERVAL 1 DAY), 1, 0)) AS ret_d1,
    MAX(IF(dd.d = DATE_ADD(a.anchor_date, INTERVAL 3 DAY), 1, 0)) AS ret_d3,
    MAX(IF(dd.d = DATE_ADD(a.anchor_date, INTERVAL 7 DAY), 1, 0)) AS ret_d7,
    MAX(IF(dd.d = DATE_ADD(a.first_seen,  INTERVAL 1 DAY), 1, 0)) AS fs_ret_d1,
    MAX(IF(dd.d = DATE_ADD(a.first_seen,  INTERVAL 3 DAY), 1, 0)) AS fs_ret_d3,
    MAX(IF(dd.d = DATE_ADD(a.first_seen,  INTERVAL 7 DAY), 1, 0)) AS fs_ret_d7
  FROM anchored a
  JOIN days dd USING (user_id)
  GROUP BY a.user_id
),

seg AS (                                      -- buyer segmentation (NULL = no purchase row for this user)
  SELECT
    user_id,
    ANY_VALUE(age)          AS age,
    ANY_VALUE(gender)       AS gender,
    ANY_VALUE(goal)         AS goal,
    ANY_VALUE(status)       AS status,
    ANY_VALUE(subscription) AS plan,
    MIN(DATE(timestamp))    AS subscribe_date
  FROM `persona-496908.sql_assessment.subscribe_events`
  GROUP BY user_id
)

SELECT
  a.user_id,

  -- the comparison group (I tier "high vs low" locally from ch_lessons_completed)
  CASE
    WHEN a.ch_start_date IS NOT NULL THEN 'took_338'
    WHEN a.ch_joined = 1             THEN 'joined_338_never_started'
    WHEN a.ch_viewed  = 1            THEN 'viewed_338_never_joined'
    WHEN a.started_any_challenge = 1 THEN 'took_other_challenge'
    ELSE                                  'no_challenge'
  END AS group_338,

  a.first_seen,
  a.anchor_date,
  DATE_DIFF(b.last_data_date, a.anchor_date, DAY) AS days_observed,   -- <7 ⇒ D7 not observable

  a.ch_start_date, a.ch_lessons_started, a.ch_lessons_completed,
  a.ch_completed_course, a.ch_certificate, a.ch_csat_n, ROUND(a.ch_avg_csat, 2) AS ch_avg_csat,

  a.lessons_completed_all, a.active_days_total,
  a.finished_onboarding, a.started_personal_plan,
  a.saw_challenge_popup, a.clicked_challenge_popup,
  a.viewed_any_challenge, a.started_any_challenge,

  r.ret_d1, r.ret_d3, r.ret_d7,
  r.fs_ret_d1, r.fs_ret_d3, r.fs_ret_d7,

  a.unsubscribed, a.unsub_reason,
  a.csat_n_all, ROUND(a.avg_csat_all, 2) AS avg_csat_all,

  s.age, s.gender, s.goal, s.status, s.plan, s.subscribe_date,
  IF(s.user_id IS NULL, 0, 1) AS has_subscription,
  a.country_code
FROM anchored a
CROSS JOIN bounds b
LEFT JOIN ret r ON r.user_id = a.user_id
LEFT JOIN seg s ON s.user_id = a.user_id
ORDER BY a.user_id;

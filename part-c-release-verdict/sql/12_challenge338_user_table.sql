-- 12 · Per-user table for the 7-Day Claude Challenge (id 338).
-- RUN this, then "Save results ▸ CSV" and drop the file in part-c-release-verdict/data/.
-- One row per user who STARTED challenge 338. I'll do the tier / D1-D3-D7 / segment analysis locally.
-- (If it throws an error, paste me the error text — I can't test against your DB.)

WITH ch338 AS (                         -- every event belonging to challenge 338
  SELECT user_id, event_name, timestamp, DATE(timestamp) AS d, csat_score
  FROM `persona-496908.sql_assessment.app_events`
  WHERE course_id = 338 OR REGEXP_CONTAINS(IFNULL(path,''), r'challenges/338')
),
starter AS (                            -- per-user challenge-338 engagement + outcomes
  SELECT
    user_id,
    MIN(IF(event_name='pr_webapp_challenge_start', d, NULL))               AS start_date,
    COUNT(DISTINCT d)                                                      AS active_challenge_days,
    COUNTIF(event_name='pr_webapp_lesson_completed')                      AS lessons_completed,
    MAX(IF(event_name='pr_webapp_course_completed',1,0))                  AS completed_course,
    MAX(IF(event_name IN ('pr_webapp_challenge_certificate_download',
                          'pr_webapp_challenge_certificate_share'),1,0))  AS got_certificate,
    COUNTIF(event_name IN ('pr_webapp_lesson_csat_click','pr_webapp_challenge_csat_click')) AS csat_n,
    AVG(IF(event_name IN ('pr_webapp_lesson_csat_click','pr_webapp_challenge_csat_click'),
           csat_score, NULL))                                             AS avg_csat
  FROM ch338
  GROUP BY user_id
),
act AS (  SELECT user_id, DATE(timestamp) AS d
          FROM `persona-496908.sql_assessment.app_events` GROUP BY 1,2 ),
uns AS (  SELECT user_id, ANY_VALUE(unsubscribe_reason) AS unsub_reason
          FROM `persona-496908.sql_assessment.app_events`
          WHERE event_name='pr_webapp_unsubscribed' GROUP BY 1 ),
seg AS (  SELECT user_id, ANY_VALUE(age) age, ANY_VALUE(gender) gender, ANY_VALUE(goal) goal,
                 ANY_VALUE(status) status, ANY_VALUE(subscription) plan
          FROM `persona-496908.sql_assessment.subscribe_events` GROUP BY 1 )
SELECT
  s.user_id, s.start_date, s.active_challenge_days, s.lessons_completed,
  s.completed_course, s.got_certificate, s.csat_n, ROUND(s.avg_csat,2) AS avg_csat,
  MAX(IF(a.d = DATE_ADD(s.start_date, INTERVAL 1 DAY),1,0)) AS ret_d1,
  MAX(IF(a.d = DATE_ADD(s.start_date, INTERVAL 3 DAY),1,0)) AS ret_d3,
  MAX(IF(a.d = DATE_ADD(s.start_date, INTERVAL 7 DAY),1,0)) AS ret_d7,
  IF(u.user_id IS NULL, 0, 1) AS unsubscribed, u.unsub_reason,
  g.age, g.gender, g.goal, g.status, g.plan
FROM starter s
LEFT JOIN act a ON a.user_id = s.user_id
LEFT JOIN uns u ON u.user_id = s.user_id
LEFT JOIN seg g ON g.user_id = s.user_id
WHERE s.start_date IS NOT NULL          -- only users who actually STARTED the challenge
GROUP BY s.user_id, s.start_date, s.active_challenge_days, s.lessons_completed,
         s.completed_course, s.got_certificate, s.csat_n, s.avg_csat,
         u.user_id, u.unsub_reason, g.age, g.gender, g.goal, g.status, g.plan
ORDER BY s.start_date;

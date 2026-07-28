-- Stage 1 · Part C — first real query. Run this, paste the one-row result back.
-- A compact engagement funnel using the confirmed event names (Events Convention).
-- It returns distinct-user counts so we can see the shape before building tier metrics.

SELECT
  COUNT(DISTINCT IF(event_name='pr_webapp_launch_first_time',              user_id, NULL)) AS registered,
  COUNT(DISTINCT IF(event_name='pr_webapp_challenge_view',                user_id, NULL)) AS challenge_viewed,
  COUNT(DISTINCT IF(event_name='pr_webapp_challenge_start',               user_id, NULL)) AS challenge_started,
  COUNT(DISTINCT IF(event_name='pr_webapp_challenge_join',                user_id, NULL)) AS challenge_joined,
  COUNT(DISTINCT IF(event_name='pr_webapp_lesson_completed',             user_id, NULL)) AS completed_any_lesson,
  COUNT(DISTINCT IF(event_name='pr_webapp_challenge_certificate_download',user_id, NULL)) AS got_challenge_certificate,
  COUNT(DISTINCT IF(event_name='pr_webapp_challenge_csat_click',          user_id, NULL)) AS gave_challenge_csat,
  COUNT(DISTINCT IF(event_name='pr_webapp_unsubscribed',                  user_id, NULL)) AS unsubscribed,
  COUNT(DISTINCT user_id)                                                                 AS all_users,
  MIN(timestamp) AS first_event, MAX(timestamp) AS last_event
FROM `persona-496908.sql_assessment.app_events`;

-- After this: I'll write query 12 = engagement tiers (high/low/didn't-start) and the
-- D1/D3/D7 + unsubscribe + completion + CSAT comparison, per your definitions.

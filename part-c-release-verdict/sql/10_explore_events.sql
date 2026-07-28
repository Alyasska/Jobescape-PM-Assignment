-- Stage 1 · probe queries — run these next, paste results back.
-- They tell me the full event list (incl. unsubscribe + any challenge-complete/streak events)
-- and exactly how Challenge participation is logged, so I can build the real tier metrics.

-- Q1 — every event type + volume in app_events
SELECT event_name, COUNT(*) AS n
FROM `persona-496908.sql_assessment.app_events`
GROUP BY event_name
ORDER BY n DESC;

-- Q2 — how is the Challenge logged? (path vs course vs category)
SELECT event_name,
       REGEXP_EXTRACT(path, r'/skills/challenges/(\d+)') AS challenge_id,
       course_id, course_name, category_name, mechanic_name,
       COUNT(*) AS n
FROM `persona-496908.sql_assessment.app_events`
WHERE path LIKE '/skills/challenges/%'
   OR LOWER(event_name) LIKE '%challenge%'
   OR LOWER(IFNULL(category_name,'')) LIKE '%challenge%'
GROUP BY 1,2,3,4,5,6
ORDER BY n DESC
LIMIT 200;

-- Q3 — do challenge lessons carry a distinct course/category? peek at raw challenge rows
SELECT event_name, user_id, timestamp, path, course_id, course_name,
       lesson_id, lesson_name, lesson_order, category_name, mechanic_name, status
FROM `persona-496908.sql_assessment.app_events`
WHERE path LIKE '/skills/challenges/%' OR LOWER(event_name) LIKE '%challenge%'
ORDER BY timestamp
LIMIT 50;

-- Q4 — the unsubscribe event (which event_name carries unsubscribe_reason?)
SELECT event_name, unsubscribe_reason, COUNT(*) AS n
FROM `persona-496908.sql_assessment.app_events`
WHERE unsubscribe_reason IS NOT NULL
GROUP BY 1,2
ORDER BY n DESC
LIMIT 100;

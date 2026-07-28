-- Part C · Step 0 — LEARN THE REAL SCHEMA FIRST (run this before anything else)
-- Project: persona-496908 · Tables: app_events, subscribe_events
-- The queries in 01–04 use ASSUMED column names (flagged with -- ⚠ADJUST). Run these
-- three first, then find/replace the assumed names with the real ones.

-- 1) What columns exist? (replace <dataset> with the real dataset id shown in the console)
SELECT table_name, column_name, data_type
FROM `persona-496908.<dataset>.INFORMATION_SCHEMA.COLUMNS`
WHERE table_name IN ('app_events','subscribe_events')
ORDER BY table_name, ordinal_position;

-- 2) What do app_events rows look like, and what event names exist?
SELECT * FROM `persona-496908.<dataset>.app_events` LIMIT 50;

SELECT event_name, COUNT(*) AS n           -- ⚠ADJUST: the event-name column may be `event`, `name`, `type`
FROM `persona-496908.<dataset>.app_events`
GROUP BY event_name ORDER BY n DESC LIMIT 100;
-- ↑ Look here for the Challenge events: something like challenge_start / challenge_day_complete /
--   lesson_complete / day_open. Note the exact strings — 01–04 depend on them.

-- 3) What does subscribe_events carry? (need: user id, subscription start, cancel/unsubscribe, plan, price)
SELECT * FROM `persona-496908.<dataset>.subscribe_events` LIMIT 50;

-- drop table if exists entries;
REATE TABLE IF NOT EXISTS entries(
  id integer primary key autoincrement,
  user_name text,
  story text
);
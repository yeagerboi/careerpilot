-- Add url column to jobs table (missed in initial migration)
-- The job hunter agent captures apply links from JSearch/Remotive/Tavily.
alter table jobs add column if not exists url text;

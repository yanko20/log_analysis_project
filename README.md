How to use this project:
 1. Create views specified below using psql in news database.
 2. Run `python log_analysis.py` command.
 
Create views queries:

```
create view top_pages_view as 
select substring(path, 10) as slug, count(path) as num_of_views 
from log 
where path like '/article/%' 
group by path 
order by num_of_views desc;


create view top_articles_view as 
select articles.title as title, articles.author as author_id, top_pages_view.num_of_views as num_of_views
from articles, top_pages_view 
where articles.slug = top_pages_view.slug;


create view errors_per_day_view as 
select count(status) as errors, date_trunc('day', time) as day 
from log 
where status similar to '(3|4|5)%' 
group by day;


create view total_errors as 
select count(status) as num from log where status similar to '(3|4|5)%';


create view error_percent_per_day as 
select 
errors_per_day_view.day, 
errors_per_day_view.errors, 
(cast(errors_per_day_view.errors as float)/total_errors.num)*100 as errors_percent
from errors_per_day_view, total_errors;
```

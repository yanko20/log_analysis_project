### Description

Log Analysis Project is an internal reporting tool that provides information about what kind of articles the site's readers like.

### How to use this project

 - download [newsdata.sql](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip)
 - load data `psql -d news -f newsdata.sql`
 - create views specified below using psql in news database
 - run `python log_analysis.py` command

### Setup steps if using Vagrant/VirtualBox

- brings up your virtual machine `vagrant up`
- login `vagrant ssh`
- navigate to vagrant directory `cd /vagrant`
- follow default instructions above


### Create views queries

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


create view requests_per_day_view as 
select count(status) as requests, date_trunc('day', time) as day
from log group by day;


create view error_percent_per_day as 
select r.day, (cast(e.errors as float)/r.requests) * 100 as error_percent 
from requests_per_day_view as r, errors_per_day_view as e 
where r.day = e.day;
```

### Sample output

![alt text](https://github.com/yanko20/log_analysis_project/blob/master/sample.png)

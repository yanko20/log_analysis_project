#!/usr/bin/env python
import psycopg2

conn = psycopg2.connect('dbname=news user=vagrant')
cur = conn.cursor()

top_3_articles_query = (
    "select title, num_of_views "
    "from top_articles_view "
    "limit 3;"
)
cur.execute(top_3_articles_query)
rows = cur.fetchall()
print '\nWhat are the most popular three articles of all time?\n'
for row in rows:
    print '    - "{}" - {} views'.format(row[0], str(row[1]))
conn.commit()

top_authors_query = (
    "select authors.name, sum(num_of_views) as total_views "
    "from top_articles_view, authors "
    "where author_id = authors.id "
    "group by authors.name order by total_views desc;"
)
cur.execute(top_authors_query)
rows = cur.fetchall()
print '\n\nWho are the most popular article authors of all time?\n'
for row in rows:
    print '    - {} - {} views'.format(row[0], str(row[1]))
conn.commit()

errors_query = (
    "select to_char(day, 'Month DD, YYYY'), "
    "round(cast(error_percent as numeric), 1) "
    "from error_percent_per_day "
    "where error_percent > 1 "
    "order by error_percent desc;"
)
cur.execute(errors_query)
rows = cur.fetchall()
print '\n\nOn which days did more than 1% of requests lead to errors?\n'
for row in rows:
    print '    - {} - {}% errors'.format(row[0], str(row[1])) + '\n'
conn.commit()

conn.close()

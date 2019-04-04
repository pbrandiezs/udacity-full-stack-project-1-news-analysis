#!/usr/bin/env python2.7
#
# news_analysis.py
#
# This program will run an analysis of the news database.
#
# The program queries the Postgres database dbname=news,
# to answer these three questions:
#   Question 1: What are the most popular three articles of all time?
#   Question 2: Who are the most popular article authors of all time?
#   Question 3: On which days did more than 1% of requests lead to errors?

# This program requires a previously configured vagrant environment.
# Please reference the readme.md file for environment configuration
# and procedures.
#
# Requires python 2.7.
#
#    Author: Perry Brandiezs
#

import psycopg2


def query_db(sql):
    db = psycopg2.connect("dbname=news")
    cur = db.cursor()
    cur.execute(sql)
    RESULTS = cur.fetchall()
    cur.close()
    db.close()
    return RESULTS


# Display a heading
print("\n\nAnalysis of news database results:\n\n")


# Question 1 results
print("Question 1: What are the most popular three articles of all time?\n\n")
sql = """
SELECT articles.title AS article,
    count(*) AS views
  FROM articles
  JOIN log
    ON articles.slug = regexp_replace(path, '.+/', '')
  GROUP BY articles.title
  ORDER BY count(*) DESC
  LIMIT 3;
  """


for Result in query_db(sql):
    print '\"{title}\" -- {count} views'.format(
        title=Result[0], count=Result[1])
print("\n==========\n")

# Question 2 results
print("Question 2: Who are the most popular article authors of all time?\n\n")

sql = """
SELECT authors.name AS author,
    count(*) AS views
  FROM articles
  JOIN log
  ON articles.slug = regexp_replace(path, '.+/', '')
  JOIN authors
  ON articles.author = authors.id
  GROUP BY authors.name
  ORDER BY count(*) DESC;
  """


for Result in query_db(sql):
    print '{author} -- {count} views'.format(
        author=Result[0], count=Result[1])
print("\n==========\n")


# Question 3 results
print("Question 3: On which days did more")
print("than 1% of requests lead to errors?\n\n")

# Note this query requires the views daily_count and error_count be previously
# created, please see readme.md for detail
sql = """
SELECT TRIM(TRAILING ' ' FROM (TO_CHAR(daily_count.date:: DATE, 'Month'))) ||
    (TO_CHAR(daily_count.date:: DATE, ' dd, yyyy')) AS date,
    TRUNC((error_count * 100.0 / day_count),2) AS percentage
  FROM daily_error
  JOIN daily_count
  ON daily_error.date = daily_count.date
  WHERE TRUNC((error_count * 100.0 / day_count),2) > 1
  ORDER BY (TRUNC((error_count * 100.0 / day_count),2)) DESC;
  """


for Result in query_db(sql):
    print '{date} -- {percent}% errors'.format(
        date=Result[0], percent=Result[1])
print("\n==========\n")

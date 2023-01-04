import csv
import io
import os
import psycopg2

username = 'student01'
password = '12345'
database = 'lab3'

os.remove("petrychenko_DB_Authors.csv")
os.remove("petrychenko_DB_Podcasts.csv")
os.remove("petrychenko_DB_Episodes.csv")

OUTPUT_FILE_T = 'petrychenko_DB_{}.csv'

TABLES = [
    'Authors',
    'Podcasts',
    'Episodes',
]

conn = psycopg2.connect(user=username, password=password, dbname=database)

with conn:
    cur = conn.cursor()

    for table_name in TABLES:
        cur.execute('SELECT * FROM ' + table_name)
        fields = [x[0] for x in cur.description]
        with io.open(OUTPUT_FILE_T.format(table_name),"w",encoding='utf-8') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(fields)
            for row in cur:
                writer.writerow([str(x) for x in row])

 

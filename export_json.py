import json
import psycopg2
import os

username = 'student01'
password = '12345'
database = 'lab3'
host = 'localhost'
port = '5432'

conn = psycopg2.connect(user=username, password=password, dbname=database, host=host, port=port)

data = {}

os.remove("all_data.json")

with conn:
    cur = conn.cursor()

    for table in ('Authors', 'Podcasts', 'Episodes'):
        cur.execute('SELECT * FROM ' + table)
        rows = []
        fields = [x[0] for x in cur.description]

        for row in cur:
            rows.append(dict(zip(fields, row)))

        data[table] = rows

with open('all_data.json', 'w') as outf:
    json.dump(data, outf, default=str)

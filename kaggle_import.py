import csv
import decimal
import io

import psycopg2

from countries import countries_list

import random
from datetime import datetime

username = 'student01'
password = '12345'
database = 'lab3'

MAX_ROWS = 3000

EP_CSV_FILE = 'CSV/episodes.csv'
PODC_CSV_FILE = 'CSV/podcasts.csv'

query_insert_ep = '''
INSERT INTO Episodes (ep_id, podc_id, ep_title, ep_audio_lenth, ep_pub_date) VALUES (%s, %s, %s, %s, %s);
'''

query_insert_podc = '''
INSERT INTO Podcasts (podc_id, auth_id, podc_title, podc_language) VALUES (%s, %s, %s, %s);
'''

query_insert_auth = '''
INSERT INTO Authors (auth_id, auth_name, auth_country, auth_date_birth) VALUES (%s, %s, %s, %s);
'''

query_drop = '''DROP TABLE authors CASCADE;
DROP TABLE podcasts CASCADE;
DROP TABLE episodes CASCADE;'''

query_create = '''
CREATE TABLE Authors
(
  auth_id char(40) NOT NULL ,
  auth_name char(60) NOT NULL ,
  auth_country char(30) NOT NULL ,
  auth_date_birth date NOT NULL 
);
CREATE TABLE Podcasts
(
  podc_id char(40) NOT NULL,
  auth_id char(40) NOT NULL ,
  podc_title char(100) NOT NULL ,
  podc_language char(20) NOT NULL
);
CREATE TABLE Episodes
(
  ep_id char(40) NOT NULL ,
  podc_id char(40) NOT NULL ,
  ep_title char(70) NOT NULL ,
  ep_audio_lenth int NOT NULL ,
  ep_pub_date date NOT NULL
);
ALTER TABLE Authors ADD PRIMARY KEY (auth_id);
ALTER TABLE Podcasts ADD PRIMARY KEY (podc_id);
ALTER TABLE Episodes ADD PRIMARY KEY (ep_id);
ALTER TABLE Podcasts ADD CONSTRAINT FK_Podcasts_Authors
FOREIGN KEY (auth_id) REFERENCES Authors (auth_id);

ALTER TABLE Episodes ADD CONSTRAINT FK_Episodes_Podcasts 
FOREIGN KEY (podc_id) REFERENCES Podcasts (podc_id);

'''


def gen_country():
    return random.choice(countries_list)[1]


def gen_birthdate(number=1):
    CurrentTime = datetime.now()
    Year = random.randrange(1950, CurrentTime.year)
    for item in range(number):
        yield random.randrange(1950, CurrentTime.year), random.randrange(1, 12), random.randrange(1, 31)


def format_date(number=1):
    for year, month, date in gen_birthdate():
        if month == 2 and date > 28:
            return format_date()
        if month < 10:
            month = f"0{month}"
        if date < 10:
            date = f"0{date}"

        return "%s-%s-%s" % (year, month, date)


conn = psycopg2.connect(user=username, password=password, dbname=database)

with conn:
    cur = conn.cursor()
    cur.execute(query_drop)
    cur.execute(query_create)
    podc_id_set = set()
    with io.open(PODC_CSV_FILE, encoding='utf-8') as inf:
        # with open(PODC_CSV_FILE, 'r') as inf:
        reader = csv.DictReader(inf)
        count_row = 0
        max_length = 0
        for idx, row in enumerate(reader):
            auth_name = row['author']
            if auth_name is None \
                    or len(row['title']) >= 99\
                    or len(auth_name) >= 59:
                continue

            count_row += 1
            if count_row == MAX_ROWS:
                break
            country = "".join(gen_country())
            birthday = "".join(format_date())
            auth_values = (idx + 1,
                           auth_name,
                           country,
                           birthday)
            cur.execute(query_insert_auth, auth_values)
            uuid = str(row['uuid']).strip()
            podc_values = (uuid,
                           idx + 1,
                           row['title'],
                           row['language'])
            podc_id_set.add(uuid.strip())
            cur = conn.cursor()
            cur.execute(query_insert_podc, podc_values)
    inf.close()
    with io.open(EP_CSV_FILE, encoding='utf-8') as inf:
        reader = csv.DictReader(inf)
        count_row = 0
        for idx, row in enumerate(reader):
            count_row += 1
            if count_row == MAX_ROWS:
                break
            uuid = str(row['uuid']).strip()
            podc_id = str(row['podcast_uuid']).strip()
            if podc_id not in podc_id_set \
                    or len(row['title']) >= 69:
                continue
            ep_values = (uuid,
                         podc_id,
                         row['title'],
                         decimal.Decimal(row['audio_length']),
                         row['pub_date'])
            cur = conn.cursor()
            cur.execute(query_insert_ep, ep_values)
    inf.close()
    conn.commit()

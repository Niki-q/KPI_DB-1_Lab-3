import psycopg2
import matplotlib.pyplot as plt

username = 'student01'
password = '12345'
database = 'lab3'
host = 'localhost'
port = '5432'

view_1 = '''
SELECT * FROM count_authors_by_country
'''

view_2 = '''
SELECT * FROM count_podcast_by_language
'''

view_3 = '''
SELECT * FROM count_podcast_by_duration
'''

conn = psycopg2.connect(user=username, password=password, dbname=database, host=host, port=port)

with conn:
    cur = conn.cursor()


    def draw_pie():
        fig = plt.figure()
        fig.set_figheight(9)
        fig.set_figwidth(13)
        cur.execute(view_1)
        country = []
        authors = []

        for row in cur:
            country.append(row[0])
            authors.append(row[1])

        plt.pie(authors, labels=country, autopct='%1.1f%%')
        plt.title('Кількість авторів за країнами')
        plt.show()


    def draw_bar():
        fig = plt.figure()
        fig.set_figheight(9)
        fig.set_figwidth(13)

        cur.execute(view_2)
        language = []
        authors = []

        for row in cur:
            language.append(row[0])
            authors.append(row[1])

        plt.bar(language, authors, label='')
        plt.title('Кількість подкастів за мовами')
        plt.xlabel('Назви мов')
        plt.ylabel('Кількість, шт.')
        plt.xticks(rotation=30, ha='right')
        plt.show()


    def draw_graph():
        fig = plt.figure()
        fig.set_figheight(12)
        fig.set_figwidth(20)
        cur.execute(view_3)
        title = []
        duration = []

        for row in cur:
            title.append(row[0])
            duration.append(row[1])
        plt.plot(title, duration, marker='o')
        plt.xticks(rotation=20, ha='right')
        plt.xlabel('Назва подкасту')
        plt.ylabel('Тривалість, хв.')
        plt.title('Кількість хвилин у епізодах різних подкастів')

        for qnt, price in zip(title, duration):
            plt.annotate(price, xy=(qnt, price), xytext=(7, 2), textcoords='offset points')

        plt.show()


    draw_bar()
    draw_pie()
    draw_graph()

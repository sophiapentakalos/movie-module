import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import psycopg2
def connect(newArticles):
    try:
        connection = psycopg2.connect(user = "postgres",
                                      password = "",
                                      host = "localhost",
                                      port = "5433",
                                      database = "postgres")

        cursor = connection.cursor()
        cursor.execute("SELECT version();")
        record = cursor.fetchone()
        print("You are connected to - ", record,"\n")
        for url in list:
            exists_Query = "SELECT * FROM links WHERE url = \'" + url + "\';"
            cursor.execute(exists_Query)
            row = cursor.fetchone()
            if row == None:
                insert_Query = "insert into links (url, date_created, is_processed) values (\'" + url + "\', current_timestamp, false);"
                print("Got the result " + str(url))
                cursor.execute(insert_Query)
            connection.commit()

        postgreSQL_select_Query = "select * from links where is_processed = false order by date_created desc;"
        cursor.execute(postgreSQL_select_Query)
        mobile_records = cursor.fetchall()
        print("Articles to Process")

    except (Exception, psycopg2.Error) as error :
        print ("Error while connecting to PostgreSQL", error)
    finally:
        #closing database connection.
            if(connection):
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")

def is_movie_news(css_class):
    names = {"story-related-story news item-1", "story-related-story news item-2",
    "story-related-story news item-3", "story-related-story news item-4",
    "story-related-story news item-5", "story-related-story news item-6",
    "story-related-story news item-7", "story-related-story news item-8",
    "story-related-story news item-9", "story-related-story news item-10",
    "story-related-story news item-11", "story-related-story news item-12"}
    return css_class in names

if __name__ == '__main__':
    URL = "https://www.cinemablend.com/news.php"
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    tags = soup.find_all("a", class_=is_movie_news)
    list = []
    for tag in tags:
        list.append(str(tag.get('href')))
    connect(list);

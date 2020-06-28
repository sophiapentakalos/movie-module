import csv
import json
import requests
import urllib.request
import time
from bs4 import BeautifulSoup

def get_urls_and_entities(file_name):
    entities = {}
    with open(file_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count > 0:
                temp = row[1:-1][0].split(", ")
                entities[row[0]] = temp
            line_count += 1
        return entities

def get_updated_entities(file_name):
    entities = {}

    with open(file_name) as json_file:
        data = json.load(json_file)
        for url in data:
            entities[url] = data[url]["entities"]
    return entities

def get_titles_and_content(urls):
    titles_and_contents = {}
    for url in urls:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.find("title").text[:-14].strip()
        [tagstring.extract() for tagstring in soup('script')] ### extracts all content not between balanced <script> tags
        [tagstring.extract() for tagstring in soup('table')] ### extracts all content not between balanced <table> tags
        [tagstring.extract() for tagstring in soup('iframe')] ### extracts all content not between balanced <iframe> tags
        [tagstring.extract() for tagstring in soup('blockquote')] ###OUR CULPRIT extracts all content not between balanced <blockquote> tags
        filtered_content_list = list(soup.find_all('p'))
        content_list = [str(tag) for tag in filtered_content_list]
        content = " ".join(content_list)
        content = content.replace("<p>", " ")
        content = content.replace("</p>", " ")
        content = content.replace("\xa0", " ")
        content = content.replace("<br/>", ". ")
        content = " ".join(content.split())
        titles_and_contents[url] = (title, content)
    return titles_and_contents

def compile_into_json(titles_and_contents, entities, file_name):
    movie_data = {}
    for url in titles_and_contents.keys():
        movie_data[url] = {"title": titles_and_contents[url][0],
        "content": titles_and_contents[url][1],
        "entities": entities[url]}
    with open(file_name, 'w') as outputfile:
        json_data = json.dump(movie_data, outputfile)

if __name__ == "__main__":
    urls_and_entities = get_updated_entities("movie_data.json")
    titles_and_contents = get_titles_and_content(urls_and_entities.keys())
    compile_into_json(titles_and_contents, urls_and_entities, "movie_data2.json")

#import librairies

from bs4 import BeautifulSoup as bs
import requests
import json

#function to clean list data
def get_content_value(row_data):
    if row_data.find("li"):
        return [li.get_text(" ", strip =True).replace("\xa0"," ") for li in row_data.find_all("li")]
    else:
        return row_data.get_text(" ", strip =True).replace("\xa0"," ")


def get_info_box(url):
    r = requests.get(url)

    # convert to soup object
    soup = bs(r.content, features='html.parser')

    # get just the info_box of page
    info_box = soup.find(class_="infobox vevent")
    info_rows = info_box.find_all("tr")
    movie_info = {}
    for index, row in enumerate(info_rows):
        if index == 0:
            movie_info['title'] = row.find("th").get_text(" ", strip=True)
        elif index == 1:
            continue
        else:
            content_key = row.find("th").get_text(" ", strip=True)
            content_value = get_content_value(row.find("td"))
            movie_info[content_key] = content_value

    return movie_info

r2 = requests.get("https://en.wikipedia.org/wiki/List_of_Walt_Disney_Pictures_films")

#convert to beautiful soup object
soup2 = bs(r2.content, features= "html.parser")

#print out the html
contents2 = soup2.prettify()
#print(contents2)

movies = soup2.select(".wikitable.sortable i a")
#print(movies)
base_path = "http://en.wikipedia.org"

movie_info_list = []
for index,movie in enumerate(movies):
    #if index ==10:
     #   break
    try:
        relative_path = movie['href']
        title = movie['title']
        full_path = base_path+relative_path

        movie_info_list.append(get_info_box(full_path))
    except Exception as e:
        print(movie.get_text())
        print(e)

#print(len(movie_info_list))
def save_data(title,data):
    with open(title, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii = False, indent=2)

def load_data(title):
    with open(title, encoding='utf-8')as f:
        return json.load(f)

save_data("disney_data.json", movie_info_list)





















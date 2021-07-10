import json

def load_data(title):
    with open(title, encoding='utf-8')as f:
        return json.load(f)

movie_info_list = load_data("disney_data.json")

print(movie_info_list)
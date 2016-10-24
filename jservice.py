import requests
import json

def get_categories():
    categories = json.loads(requests.get('http://jservice.io/api/categories?count=6').text)
    return categories

def sanitize_data(data):
    sanitized = data

    return sanitized

def get_jservice_data():
    categories = get_categories()
    data = []

    data.append(categories)

    for category in categories:
        response = json.loads(requests.get('http://jservice.io/api/clues?category={}'.format(category['id'])).text)

        clues = []

        for clue in response:
            if len(clues) == 5:
                break

            clues.append(clue)

        data.append(clues)

    sanitized = sanitize_data(data)

    return sanitized

print(get_jservice_data())

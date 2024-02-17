import requests
from bs4 import BeautifulSoup
import config


def parse_response(response):
    soup = BeautifulSoup(response.content, 'html5lib')
    definitions_html_list = soup.find_all('div', attrs={'class': 'definition'})
    dictionary = []
    for definition_html in definitions_html_list:
        dictionary_item = {}
        dictionary_item['word'] = definition_html.find(
            'a', attrs={'data-x-bind': 'definition'}).text
        dictionary_item['meaning'] = definition_html.find(
            'div', attrs={'class': 'meaning'}).text
        dictionary_item['example'] = definition_html.find(
            'div', attrs={'class': 'example'}).text
        dictionary.append(dictionary_item)
    # return first two elements of the list
    return dictionary[:2]


def fetch_random_definitions():
    response = requests.get(config.SERVER_URL)
    return parse_response(response)


if __name__ == '__main__':
    print(fetch_random_definitions())

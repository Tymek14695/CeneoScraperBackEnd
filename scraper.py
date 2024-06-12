from bs4 import BeautifulSoup
import os
import requests
import json
from colorama import Fore

product_code = 79242779
#product_code = input('Podaj kod produktu:\t')
print(Fore.BLUE, '\tStarting scan for', Fore.YELLOW, product_code, Fore.BLUE, '...')
url = f'https://www.ceneo.pl/{product_code}#tab=reviews'

def getData(ancestor, selector, attribute=None, returnList=False):
    print(Fore.BLUE, '\t\t\tGetting data for', Fore.YELLOW, ancestor, selector, attribute, returnList, Fore.BLUE, '...')
    if returnList:
        return [tag.text.strip() for tag in ancestor.select(selector)]
    if attribute:
        if selector:
            try:
                return ancestor.select_one(selector)[attribute].strip()
            except:
                return None
        else:
            return ancestor[attribute].strip()
    try:
        return ancestor.select_one(selector).text.strip()
    except AttributeError:
        return None

selectors = {
            'opinion_id' : (None, 'data-entry-id'),
            'author' : ("span.user-post__author-name",),
            'recommendation' : ("span.user-post__recomendation > em",),
            'stars' : ("span.user-post__score-count",),
            'content' : ("span.user-post__text",),
            'pros' : ('div.review-feature__title--positives ~ div.review-feature__item', None, True),
            'cons' : ('div.review-feature__title--negatives ~ div.review-feature__item', None, True),
            'date' : ('span.user-post__published > time:nth-child(1)', "datetime"),
            'purchase_date' : ('span.user-post__published > time:nth-child(1)', 'datetime'),
            'useful' : ("button.vote-yes",),
            'useless' : ("button.vote-no",)
        }

all_opinions = []
while url:
    print(Fore.BLUE, '\t\tScraping page', Fore.YELLOW, url, Fore.BLUE, '...')
    print(url)
    response = requests.get(url)
    page = BeautifulSoup(response.text, "html.parser")
    opinions = page.select('div.js_product-review')
    for opinion in opinions:
        single_opinion = {
            key: getData(opinion, *value)
                for key, value in selectors.items()
        }
        print(Fore.BLUE, '\t\t\t\t\tOpinion found:', Fore.GREEN, single_opinion)
        all_opinions.append(single_opinion)
    try:
        url = 'https://ceneo.pl'+page.select_one('a.pagination__next')['href']
    except TypeError:
        url = None
if not os.path.exists('opinions'):
    os.mkdir('opinions')
jsonFile = open(f'./opinions/{product_code}.json', 'w', encoding='utf-8')
json.dump(all_opinions, jsonFile, indent=4, ensure_ascii=False)
jsonFile.close()
        
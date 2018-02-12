import time

import requests
from bs4 import BeautifulSoup
from operator import itemgetter


def get_teams():
    url = "http://www.fifa.com/worldcup/teams/index.html"

    status_code = 0

    while status_code != 200:
        try:
            web = requests.get(url)
            status_code = web.status_code
            if status_code != 200:
                time.sleep(3)
        except Exception as e:
            print(e)
            status_code = 0
            time.sleep(3)

    soup = BeautifulSoup(web.content, 'html.parser')

    names = soup.find_all("a", class_="team")

    results = []
    for name in names:
        country = name.text.encode("utf-8")
        if country == "IR Iran":
            country = country.replace("IR ", "")
        results.append(country)

    return sorted(results, key=itemgetter(0))

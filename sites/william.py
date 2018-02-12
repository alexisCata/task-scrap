import time
from operator import itemgetter

import requests
from bs4 import BeautifulSoup

# from utils.proxies import get_proxies


class WilliamScraper:
    final_url = ""
    next_url = ""

    def __init__(self):
        self.url = "http://sports.williamhill.com"

    def get_william_data(self):
        proxies_list = []
        # proxies_list = get_proxies()
        if not self.final_url:

            print ("Scraping WilliamHill")

            web = self.request_william(proxies_list, self.url)

            soup = BeautifulSoup(web.content, 'html.parser')

            link = soup.find_all("a", id="football")

            try:
                url = link[0].get("href")
            except Exception as e:
                print("ERROR 1: " + str(link))
                exit()
                exit()

            web = self.request_william(proxies_list, url)

            soup = BeautifulSoup(web.content, 'html.parser')

            a_competitions = soup.find_all("a")

            link = []
            for a in a_competitions:
                if a.get_text().strip() in ["All Competitions", "Ligas y torneos"]:
                    link.append(a)

            try:
                url = link[0].get("href")
            except Exception as e:
                print("ERROR 2: " + str(link))
                exit()

            web = self.request_william(proxies_list, url)

            soup = BeautifulSoup(web.content, 'html.parser')
            a_competitions = soup.find_all("a")

            link = []
            for a in a_competitions:
                if a.get_text().strip() in ["World Cup 2018", "Mundial 2018"]:
                    link.append(a)

            try:
                url = link[0].get("href")
            except Exception as e:
                print("ERROR 3: " + str(link))
                exit()

            web = self.request_william(proxies_list, url)

            soup = BeautifulSoup(web.content, 'html.parser')

            a_competitions = soup.find_all("a")

            link = []
            for a in a_competitions:
                if a.get_text().strip() in ["World Cup 2018 - Outright", "Mundial 2018 - Ganador"]:
                    link.append(a)

            try:
                self.final_url = link[0].get("href")
            except Exception as e:
                print("ERROR 4: " + str(link))
                exit()



        web = self.request_william(proxies_list, self.final_url)

        soup = BeautifulSoup(web.content, 'html.parser')

        body = soup.find("tbody")

        names_a = body.find_all("div", class_="eventselection")

        prices_a = body.find_all("div", class_="eventprice")

        names = {}
        for n in names_a:
            names[int(n.get("id").replace("ip_selection", "").replace("name", ""))] = n.get_text()

        prices = {}
        for p in prices_a:
            prices[int(p.get("id").replace("ip_selection", "").replace("price", ""))] = p.get_text()

        results = []
        for id, name in names.items():
            results.append([name.strip().encode("utf-8"), prices[id].strip().encode("utf-8")])

        with open("./results_william", 'w') as wf:
            wf.write(str(results))

        return sorted(results, key=itemgetter(0))

    def request_william(self, proxies_list, url):
        web = None
        status_code = 0
        proxie_index = 0
        headers = {"Accept-Language": "en-US,en;q=0.5"}

        while status_code != 200:
            try:
                # web = requests.get(url, proxies={"https": proxies_list[proxie_index]}, headers=headers, timeout=10)
                web = requests.get(url)
                # proxie_index = 0 if proxie_index == len(proxies_list) - 1 else proxie_index + 1
                status_code = web.status_code
                if status_code != 200:
                    time.sleep(3)
            except Exception as e:
                print(e)
                status_code = 0
                time.sleep(3)
                # proxie_index = 0 if proxie_index == len(proxies_list) - 1 else proxie_index + 1

        return web

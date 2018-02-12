import ast
import os
import sys
import threading
import time
from difflib import SequenceMatcher

from terminaltables import AsciiTable

# from sites.bet365 import get_bet365_data
from sites.bet365 import Bet365Scraper
# from sites.paddy import get_paddy_data
from sites.paddy import PaddyScraper
# from sites.sky import get_sky_data
from sites.sky import SkyScraper
# from sites.william import get_william_data
from sites.william import WilliamScraper
from utils.proxies import Proxy
from utils.teams import get_teams


class Scraper:
    proxy = Proxy()
    results_headers = [["Team", "William", "Bet365", "Paddy", "Sky"]]
    results_william = []
    results_paddy = []
    results_sky = []
    results_bet365 = []
    results = []
    table = []
    teams = []
    william_file = "./results_william"
    bet365_file = "./results_bet365"
    paddy_file = "./results_paddy"
    sky_file = "./results_sky"

    thread_w = None
    thread_b = None
    thread_p = None
    thread_s = None

    def __init__(self, scrap_time=None, proxy=None, team=None):
        self.scrap_time = scrap_time
        self.proxy_arg = proxy
        self.team = team
        self.remove_files()
        self.william_scraper = WilliamScraper()
        self.bet365_scraper = Bet365Scraper()
        self.paddy_scraper = PaddyScraper()
        self.sky_scraper = SkyScraper()

    def remove_files(self):
        try:
            os.remove(self.william_file)
        except OSError:
            pass
        try:
            os.remove(self.bet365_file)
        except OSError:
            pass
        try:
            os.remove(self.paddy_file)
        except OSError:
            pass
        try:
            os.remove(self.sky_file)
        except OSError:
            pass

    def request_teams(self, team):
        self.teams = get_teams()
        if team and team not in self.teams:
            print("REQUESTED TEAM DOES NOT EXIST")
            print("WORLD CUP 2018 TEAMS: " + str(self.teams))
            sys.exit()
        self.results.extend(self.results_headers)
        for team_name in self.teams:
            if not team:
                self.results.append([team_name, None, None, None, None])
            elif team == team_name:
                self.results.append([team_name, None, None, None, None])

    def read_files(self):
        if os.path.isfile(self.william_file):
            with open(self.william_file, 'r') as wf:
                william = wf.read()
                self.results_william = ast.literal_eval(william)
        if os.path.isfile(self.bet365_file):
            with open(self.bet365_file, 'r') as bf:
                bet365 = bf.read()
                self.results_bet365 = ast.literal_eval(bet365)
        if os.path.isfile(self.paddy_file):
            with open(self.paddy_file, 'r') as pf:
                paddy = pf.read()
                self.results_paddy = ast.literal_eval(paddy)
        if os.path.isfile(self.sky_file):
            with open(self.sky_file, 'r') as sf:
                sky = sf.read()
                self.results_sky = ast.literal_eval(sky)

    def scrap(self, proxy_bet365_paddy, parallel_scrapping=""):
        if parallel_scrapping == "yes":
            if not self.thread_w or not self.thread_w.isAlive():
                self.thread_w = threading.Thread(name='william', target=self.william_scraper.get_william_data)
                self.thread_w.start()
                # TODO remove sleeps
                time.sleep(30)
            if not self.thread_b or not self.thread_b.isAlive():
                self.thread_b = threading.Thread(name='bet365', target=self.bet365_scraper.get_bet365_data,
                                                 kwargs={"use_proxy": proxy_bet365_paddy, "proxy": self.proxy})
                self.thread_b.start()
                time.sleep(30)

            if not self.thread_p or not self.thread_p.isAlive():
                self.thread_p = threading.Thread(name='paddy', target=self.paddy_scraper.get_paddy_data,
                                                 kwargs={"use_proxy": proxy_bet365_paddy, "proxy": self.proxy})
                self.thread_p.start()
                time.sleep(30)

            if not self.thread_s or not self.thread_s.isAlive():
                if self.proxy_arg:
                    px = self.proxy_arg
                else:
                    px = self.proxy
                self.thread_s = threading.Thread(name='sky', target=self.sky_scraper.get_sky_data, kwargs={"proxy": px})
                self.thread_s.start()
                time.sleep(30)
        else:
            self.william_scraper.get_william_data()
            self.bet365_scraper.get_bet365_data(self.proxy, proxy_bet365_paddy)
            self.paddy_scraper.get_paddy_data(self.proxy, proxy_bet365_paddy)
            if self.proxy_arg:
                px = self.proxy_arg
            else:
                px = self.proxy
            self.sky_scraper.get_sky_data(px)

    def print_table(self):
        while True:
            self.read_files()

            for indR, result in enumerate(self.results):
                for w in self.results_william:
                    if SequenceMatcher(None, result[0], w[0]).ratio() > 0.8:
                        self.results[indR][1] = w[1]
                for b in self.results_bet365:
                    if SequenceMatcher(None, result[0], b[0]).ratio() > 0.8:
                        self.results[indR][2] = b[1]
                for p in self.results_paddy:
                    if SequenceMatcher(None, result[0], p[0]).ratio() > 0.8:
                        self.results[indR][3] = p[1]
                for s in self.results_sky:
                    if SequenceMatcher(None, result[0], s[0]).ratio() > 0.8:
                        self.results[indR][4] = s[1]

            table = []
            for data in self.results:
                if data[0] == self.team:
                    print("TEAM: {}".format(data))
                if data[1] or data[2] or data[3] or data[4]:
                    table.append(data)

            if len(table) > 1:
                print(AsciiTable(table).table)

            time.sleep(60)

    def table_thread(self):
        threading.Thread(name="table", target=self.print_table).start()

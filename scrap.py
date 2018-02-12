import time

from scraper import Scraper
from settings import PROXY
from utils.utils import parse_arguments

"""
usage: scrap.py [-h] [--refresh_time REFRESH_TIME] [--team TEAM]
                [--use_proxy_bet365_paddy {yes,no}]
                [--parallel_scrapping {yes,no}] [--version]

optional arguments:
  -h, --help            show this help message and exit
  --refresh_time REFRESH_TIME
                        Data refresh time
  --team TEAM           Team to get data
  --use_proxy_bet365_paddy {yes,no}
                        Use proxy for Bet365 and PaddyPower (Default no)
  --parallel_scrapping {yes,no}
                        Scrap sites in parallel (Default yes)
  --version             show program's version number and exit

"""

if __name__ == "__main__":

    args = parse_arguments()
    refresh_time = args.refresh_time
    team = args.team
    use_proxy_bet365_paddy = args.use_proxy_bet365_paddy
    parallel_scrapping = args.parallel_scrapping

    scraper = Scraper(proxy=PROXY, team=team or "")
    scraper.request_teams(team)
    scraper.table_thread()

    print("Scraping... wait for the results")

    while True:
        scraper.scrap(use_proxy_bet365_paddy, parallel_scrapping)
        # scraper.scrap("yes", parallel_scrapping)

        time.sleep(refresh_time or 300)

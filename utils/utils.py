import argparse


def parse_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument('--refresh_time', help='Data refresh time in seconds', type=int)
    parser.add_argument('--team', help='Team to get data')

    parser.add_argument('--use_proxy_bet365_paddy', default="no", choices=['yes', 'no'], help='Use proxy for Bet365 and PaddyPower (Default no)')
    parser.add_argument('--parallel_scrapping', default="yes", choices=['yes', 'no'], help='Scrap sites in parallel (Default yes)')
    parser.add_argument("--version", action="version", version='%(prog)s - Version 1.0')

    return parser.parse_args()
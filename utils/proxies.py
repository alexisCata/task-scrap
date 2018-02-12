import requests
from bs4 import BeautifulSoup


class Proxy:
    proxies_list = []
    proxy_index = 0
    proxy_https_index = 0

    def __init__(self, proxy=None):
        self.proxies_list = self.get_proxies()
        self.proxies_https_list = self.get_https_proxies()
        self.proxy_arg = proxy

    def get_proxies(self):
        proxy_web = requests.get("https://free-proxy-list.net/uk-proxy.html")
        soup = BeautifulSoup(proxy_web.content, 'lxml')
        body = soup.find_all("tbody")[0]
        proxies_list = []
        for tr in body.find_all("tr"):
            ip = tr.find_all("td")[0].getText()
            port = tr.find_all("td")[1].getText()
            proxies_list.append(ip + ":" + port)
        return proxies_list

    def get_arg_proxy(self):
        proxy_web = requests.get("https://free-proxy-list.net/uk-proxy.html")
        soup = BeautifulSoup(proxy_web.content, 'lxml')
        body = soup.find_all("tbody")[0]
        proxies_list = []
        for tr in body.find_all("tr"):
            ip = tr.find_all("td")[0].getText()
            port = tr.find_all("td")[1].getText()
            proxies_list.append(ip + ":" + port)
        return proxies_list

    def get_next_proxy(self):
        proxy = self.proxies_list[self.proxy_index+4]
        self.proxy_index = 0 if self.proxy_index == len(self.proxies_list) - 1 else self.proxy_index + 1

        return proxy

    def get_next_https_proxy(self):
        proxy = self.proxies_https_list[self.proxy_https_index]
        self.proxy_https_index = 0 if self.proxy_https_index == len(self.proxies_https_list) - 1 else self.proxy_https_index + 1

        return proxy

    def get_https_proxies(self):
        proxy_web = requests.get("https://free-proxy-list.net/uk-proxy.html")
        soup = BeautifulSoup(proxy_web.content, 'lxml')
        body = soup.find_all("tbody")[0]
        proxies_list = []
        for tr in body.find_all("tr"):
            if tr.find_all("td")[6].getText() == "yes":
                ip = tr.find_all("td")[0].getText()
                port = tr.find_all("td")[1].getText()
                proxies_list.append(ip + ":" + port)

        return proxies_list


#
# def get_proxies():
#     proxy_web = requests.get("https://free-proxy-list.net/uk-proxy.html")
#     soup = BeautifulSoup(proxy_web.content, 'lxml')
#     body = soup.find_all("tbody")[0]
#     proxies_list = []
#     for tr in body.find_all("tr"):
#         ip = tr.find_all("td")[0].getText()
#         port = tr.find_all("td")[1].getText()
#         proxies_list.append(ip + ":" + port)
#     return proxies_list

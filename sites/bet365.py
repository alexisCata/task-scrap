import time
from operator import itemgetter

from selenium import webdriver
from selenium.webdriver.common.by import By


class Bet365Scraper:
    final_url = ""

    def __init__(self):
        self.url = "http://mobile.bet365.com"

    def get_bet365_data(self, proxy, use_proxy):
        print ("Scraping Bet365")

        results = self.request_selenium(proxy, self.url, use_proxy)

        with open("./results_bet365", 'w') as bf:
            bf.write(str(results))

        return sorted(results, key=itemgetter(0))


    #
    # from selenium.webdriver.common.proxy import *
    # from selenium import webdriver
    # from selenium.webdriver.common.by import By
    # phantomjs_path = r"E:\Software & Tutorial\Phantom\phantomjs-2.1.1-windows\bin\phantomjs.exe"
    # service_args = [
    #     '--proxy=217.156.252.118:8080',
    #     '--proxy-type=https',
    #     ]
    #
    # driver = webdriver.PhantomJS(service_args=service_args)
    # driver.get("https://www.google.com.bd/?gws_rd=ssl#q=what+is+my+ip")
    # print driver.page_source.encode('utf-8')
    # print "="*70
    # print driver.title
    # driver.save_screenshot(r"E:\Software & Tutorial\Phantom\test.png")
    # driver.quit()

    def request_selenium(self, proxy, url, use_proxy):
        driver = None
        results = []
        while not results:
            p = proxy.get_next_proxy()
            try:
                # TODO remove use proxy
                use_proxy = "yes"
                if use_proxy == "yes":
                    fp = webdriver.FirefoxProfile()
                    fp.set_preference("network.proxy.type", 1)
                    fp.set_preference("network.proxy.http", p.split(":")[0])
                    fp.set_preference("network.proxy.http_port", int(p.split(":")[1]))
                    fp.set_preference("network.proxy.ssl", p.split(":")[0])
                    fp.set_preference("network.proxy.ssl_port", int(p.split(":")[1]))
                    fp.set_preference("general.useragent.override", "whater_useragent")
                    fp.update_preferences()

                    driver = webdriver.Firefox(firefox_profile=fp, timeout=60)
                else:
                    driver = webdriver.Firefox(timeout=60)

                # phantomjs_path = "/home/alexis/node_modules/phantomjs-prebuilt/lib/phantom/bin/phantomjs"
                # service_args = [
                #     '--proxy=' + p,
                #     '--proxy-type=https',
                # ]
                #
                # driver = webdriver.PhantomJS(service_args=service_args, executable_path=phantomjs_path)

                # driver.set_window_size(0, 0)
                driver.set_page_load_timeout(60)

                if not self.final_url:

                    driver.get(url)

                    time.sleep(30)

                    driver.find_element(By.XPATH,
                                    '//div[contains(@class, "sb-SportsItem_Truncator") and starts-with(text(),\'Soccer\')]').click()

                    time.sleep(30)

                    driver.find_element(By.XPATH, '//span[starts-with(text(),"World Cup")]').click()

                    time.sleep(30)

                    driver.find_element(By.XPATH, '//span[starts-with(text(),"To Win Outright")]').click()

                    time.sleep(30)
                else:
                    driver.get(self.final_url)

                spans = driver.find_elements(By.XPATH, '//span[contains(@class, "opp")]')

                self.final_url = driver.current_url

                for span in spans:
                    text = span.text.encode("utf-8")
                    ind = text.rfind(" ")
                    name = text[0:ind - 1]
                    price = text[ind + 1:]
                    results.append([name, price])

                driver.quit()
            except Exception as e:
                print ("Error: get_data_bet365() - " + str(e))
                if driver:
                    driver.quit()

        return results

import time
from operator import itemgetter

from selenium import webdriver
from selenium.webdriver.common.by import By


class SkyScraper:
    final_url = ""

    def __init__(self):
        self.url = "https://www.skybet.com"

    def get_sky_data(self, proxy=None):
        print ("Scraping Skybet")
        if isinstance(proxy, basestring):
            proxies_list = [proxy]
        else:
            proxies_list = proxy.get_proxies()

        results = self.request_selenium(proxies_list, self.url)

        with open("./results_sky", 'w') as sf:
            sf.write(str(results))

        return sorted(results, key=itemgetter(0))

    def request_selenium(self, proxies_list, url):
        proxie_index = 0
        driver = None
        results = []
        while not results:
            p = proxies_list[proxie_index]
            try:
                fp = webdriver.FirefoxProfile()
                fp.set_preference("network.proxy.type", 1)
                fp.set_preference("network.proxy.https", p.split(":")[0])
                fp.set_preference("network.proxy.https_port", int(p.split(":")[1]))
                fp.set_preference("network.proxy.ssl", p.split(":")[0])
                fp.set_preference("network.proxy.ssl_port", int(p.split(":")[1]))
                fp.set_preference("general.useragent.override", "whater_useragent")
                fp.update_preferences()

                driver = webdriver.Firefox(firefox_profile=fp)

                # phantomjs_path = "/home/alexis/node_modules/phantomjs-prebuilt/lib/phantom/bin/phantomjs"
                # service_args = [
                #     '--proxy=' + p,
                #     '--proxy-type=https',
                # ]
                #
                # driver = webdriver.PhantomJS(service_args=service_args, executable_path=phantomjs_path)

                # driver.set_window_size(0, 0)
                driver.set_page_load_timeout(90)

                driver.get(url)

                time.sleep(20)

                aS = driver.find_elements(By.XPATH,
                                          '//a[contains(@class, "link_3yg2g9") and contains(text(), \'Football\')]')
                import string
                printable = set(string.printable)
                for a in aS:
                    if (filter(lambda x: x in printable, a.text)).replace('\n', '') == u'Football':
                        a.click()
                        time.sleep(30)
                        break

                driver.find_element(By.XPATH, '//a[starts-with(text(),"Competitions")]').click()

                time.sleep(20)

                driver.find_element(By.XPATH,
                                    '//span[contains(@class, "split__title") and starts-with(text(),"World Cup 2018")]').click()

                time.sleep(30)

                driver.find_element(By.XPATH,
                                    '//a[contains(@data-toggle-tab, "competitions-world-cup-2018-outrights")]').click()

                time.sleep(30)

                driver.find_element(By.XPATH,
                                    '//span[contains(@class, "competitions-team-name") and starts-with(text(),"World Cup 2018 Winner")]').click()

                time.sleep(30)

                divs = driver.find_elements(By.XPATH, '//div[contains(@class, "row_11ssjiv")]')

                for div in divs:
                    text = div.text.encode("utf-8")
                    name = text.split('\n')[0]
                    price = text.split('\n')[1]
                    results.append([name, price])

                driver.quit()

                proxie_index = 0 if proxie_index == len(proxies_list) - 1 else proxie_index + 1
            except Exception as e:
                print ("Error: get_data_sky() - " + str(e))
                if driver:
                    driver.quit()
                proxie_index = 0 if proxie_index == len(proxies_list) - 1 else proxie_index + 1

        return results

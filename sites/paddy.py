import time
from operator import itemgetter

from selenium import webdriver
from selenium.webdriver.common.by import By


class PaddyScraper:
    final_url = ""
    urls = {}

    def __init__(self):
        self.url = "http://www.paddypower.com"

    def get_paddy_data(self, proxy, use_proxy):
        print ("Scraping Paddypower")

        results = self.request_selenium(proxy, self.url, use_proxy)

        with open("./results_paddy", 'w') as pf:
            pf.write(str(results))

        return sorted(results, key=itemgetter(0))

    def request_selenium(self, proxy, url, use_proxy):
        driver = None
        results = []
        while not results:
            p = proxy.get_next_https_proxy()
            try:
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

                    popup = driver.find_element(By.XPATH,
                                                '//button[contains(@class, "btn") and starts-with(text(),\'Ok, I got it.\')]')

                    if popup:
                        time.sleep(10)
                        popup.click()
                        time.sleep(30)

                        # action = webdriver.common.action_chains.ActionChains(driver)
                        # action.move_to_element_with_offset(popup, 5, 5)
                        # action.click()
                        # action.perform()

                    driver.find_element(By.XPATH, '//span[starts-with(text(),"Football")]').click()

                    time.sleep(30)

                    divs = driver.find_elements(By.XPATH, '//div[contains(@class, "ribbon__item-content")]')

                    for div in divs:
                        if div.text == u'Tournaments':
                            div.click()
                            break

                    time.sleep(30)

                    next_url = driver.find_element(By.XPATH,
                                                   '//a[contains(@class, "links-list__link-item") and contains(text(),\'FIFA World Cup 2018\')]') \
                        .get_attribute("href").encode('utf-8')

                    driver.get(next_url)

                    time.sleep(30)

                    next_url = driver.find_elements(By.XPATH, '//a[contains(@class, "ribbon__item")]')[1].get_attribute(
                        "href").encode('utf-8')

                    driver.get(next_url)

                    self.final_url = driver.current_url

                    time.sleep(30)
                else:
                    driver.get(self.final_url)

                button = driver.find_element(By.XPATH, '//button[contains(@class, "outright-item-grid-list__show-more")]')

                action = webdriver.common.action_chains.ActionChains(driver)
                action.move_to_element_with_offset(button, 5, 5)
                action.click()
                action.perform()

                spans = driver.find_elements(By.XPATH, '//div[contains(@class, "grid outright-item")]')[1:]

                for span in spans:
                    text = span.text.encode("utf-8")
                    name = text.split('\n')[0]
                    price = text.split('\n')[1]
                    results.append([name, price])

                driver.quit()

            except Exception as e:
                print ("Error: get_data_paddy() - " + str(e))
                if driver:
                    driver.quit()

        return results

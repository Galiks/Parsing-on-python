import logging
import re
import sys
import time
from distutils.file_util import copy_file
from multiprocessing import current_process
from multiprocessing.pool import Pool

from bs4 import BeautifulSoup
from selenium import webdriver

from parsingAbstractClass import Parsing
from shop import Shop


class Copier(object):
    def __init__(self, tgtdir):
        self.target_dir = tgtdir
    def __call__(self, src):
        copy_file(src, self.target_dir)

class WebDriverParsing(Parsing):
    logger = logging.getLogger("WebDriverParsing")
    logger.setLevel(logging.INFO)

    # create the logging file handler
    fh = logging.FileHandler("WebDriverParsing.log")

    formatter = logging.Formatter('[%(asctime)s] p%(process)s {%(lineno)d} %(levelname)s - %(message)s',
                                  '%m-%d %H:%M:%S')
    fh.setFormatter(formatter)

    # add handler to logger object
    logger.addHandler(fh)

    __file_path_to_Chrome = "E:\Документы\PyCharmProject\Parsing-on-python\chromedriver_win32\chromedriver.exe"

    def __init__(self):
        pass

    def parsing(self):
        start_time = time.time()
        global driver
        try:
            driver = webdriver.Chrome(
                self.__file_path_to_Chrome)
            driver.get("https://megabonus.com/feed")
            button = driver.find_element_by_class_name("see-more")
            button.click()
            while button.is_displayed():
                try:
                    button.click()
                    button = driver.find_element_by_class_name("see-more")
                except Exception as e:
                    self.logger.error(e)
            ul = driver.find_element_by_class_name("cacheback-block-list").get_attribute("outerHTML")
            soup = BeautifulSoup(ul, 'lxml')
            shops_str = []
            shops = soup.find_all("li")
            for shop in shops:
                shops_str.append(shop.__str__())
            pool = Pool(processes=4)
            result = pool.map(func=self.parse_elements, iterable=shops_str)
            print(time.time() - start_time)
            self.__print_array(result)
        finally:
            driver.close()

    def parse_elements(self, element):
        soup = BeautifulSoup(element, 'lxml')
        name = self.get_name(soup)
        full_discount = self.get_full_discount(soup)
        discount = self.get_discount(full_discount)
        label = self.get_label(full_discount)
        image = self.get_image(soup)
        url = self.get_url(soup)
        if name is not None and discount is not None and label is not None and image is not None and url is not None:
            return Shop(name=name, discount=discount, label=label, image=image, url=url)

    def get_name(self, element):
        pattern_for_name = "Подробнее про кэшбэк в ([\\w\\s\\d\\W]+)"
        try:
            name = element.find('div', class_='holder-more').find('a').text.strip()
            name_search = re.search(pattern_for_name, name)
            return name_search.group(1)
        except Exception as e:
            self.logger.error(e)

    def get_full_discount(self, element):
        try:
            return element.find('div', class_='percent_cashback').text.strip()
        except Exception as e:
            self.logger.error(e)

    def get_discount(self, full_discount):
        pattern_for_discount = "\\d+[.|,]*\\d*"
        if full_discount is not None:
            try:
                discount = re.search(pattern_for_discount, full_discount)
                return float(discount.group(0))
            except Exception as e:
                self.logger.error(e)

    def get_label(self, full_discount):
        pattern_for_label = "[$%€]|руб|(р.)|cent|р|Р|RUB|USD|EUR|SEK|UAH|INR|BRL|GBP|CHF|PLN"
        if full_discount is not None:
            try:
                label_search = re.search(pattern_for_label, full_discount)
                return label_search.group(0)
            except Exception as e:
                self.logger.error(e)

    def get_image(self, element):
        try:
            return element.find('img').get('src')
        except Exception as e:
            self.logger.error(e)

    def get_url(self, element):
        try:
            return element.find('div', class_='holder-img').find('a').get('href')
        except Exception as e:
            self.logger.error(e)

    def __print_array(self, array: []):
        for item in array:
            print(item.__str__())


if __name__ == '__main__':
    webDriverParsing = WebDriverParsing()
    webDriverParsing.parsing()

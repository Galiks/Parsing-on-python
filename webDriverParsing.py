import re
import time
from multiprocessing import current_process, Process
from multiprocessing.pool import Pool
import logging
from telnetlib import EC
from threading import Thread

from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from parsingAbstractClass import Parsing
from shop import Shop


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
        result = []
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
            ul = driver.find_element_by_class_name("cacheback-block-list")
            WebDriverWait(driver, 5)
            web_elements = ul.find_elements_by_tag_name("li")
            for element in web_elements:
                result.append(self.parse_elements(element))
            # pool = Pool(processes=4)
            # result = pool.map(self.parse_elements, web_elements)
            self.__print_array(result)
        finally:
            driver.close()

    def parse_elements(self, element):
        name = self.__get_name(element)
        full_discount = self.__get_full_discount(element)
        discount = self.__get_discount(full_discount)
        label = self.__get_label(full_discount)
        image = self.__get_image(element)
        url = self.__get_url(element)
        if name is not None and discount is not None and label is not None and image is not None and url is not None:
            return Shop(name=name, discount=discount, label=label, image=image, url=url)

    def __get_name(self, element):
        pattern_for_name = "Подробнее про кэшбэк в ([\\w\\s\\d\\W]+)"
        try:
            name = element.find_element_by_class_name("holder-more").find_element_by_tag_name("a").get_attribute("innerHTML")
            name = re.search(pattern_for_name, name)
            name = name.group(1)
            return name
        except Exception as e:
            self.logger.error(e)
            return None

    def __get_full_discount(self, element):
        try:
            full_discount = element.find_element_by_css_selector("div.your-percentage > strong").text
            return full_discount
        except Exception as e:
            self.logger.error(e)
            return None

    def __get_discount(self, full_discount):
        pattern_for_discount = "\\d+[.|,]*\\d*"
        if full_discount is not None:
            try:
                discount = re.search(pattern_for_discount, full_discount)
                return float(discount.group(0))
            except Exception as e:
                self.logger.error(e)
        else:
            return None

    def __get_label(self, full_discount):
        pattern_for_label = "[$%€]|руб|(р.)|cent|р|Р|RUB|USD|EUR|SEK|UAH|INR|BRL|GBP|CHF|PLN"
        if full_discount is not None:
            try:
                label = re.search(pattern_for_label, full_discount)
                label = label.group(0)
                return label
            except Exception as e:
                self.logger.error(e)
        else:
            return None

    def __get_image(self, element):
        try:
            image = element.find_element_by_tag_name("img").get_attribute("src")
            return image
        except Exception as e:
            self.logger.error(e)
            return None

    def __get_url(self, element):
        try:
            page = element.find_element_by_css_selector("div.holder-img > a").get_attribute("href")
            return page
        except Exception as e:
            self.logger.error(e)
            return None

    def __print_array(self, array: []):
        for item in array:
            print(item.__str__())

if __name__ == '__main__':
    webDriverParsing = WebDriverParsing()
    start_time = time.time()
    webDriverParsing.parsing()
    print(time.time() - start_time)

from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement

from parsingAbstractClass import Parsing
from shop import Shop


class WebDriverParsing(Parsing):

    def __init__(self):
        pass

    def parsing(self):
        global driver
        try:
            driver = webdriver.Chrome(
                "E:\Документы\PyCharmProject\Parsing-on-python\chromedriver_win32\chromedriver.exe")
            driver.get("https://megabonus.com/feed")
            button = driver.find_element_by_class_name("see-more")
            # while button.is_displayed():
            try:
                button.click()
                button = driver.find_element_by_class_name("see-more")
            except:
                print()
            ul = driver.find_element_by_class_name("cacheback-block-list")
            web_elements = ul.find_elements_by_tag_name("li")
            for element in web_elements:
                self.__parse_elements(element)
        finally:
            driver.close()

    def __parse_elements(self, element: WebElement):
        name = self.__get_name(element)
        full_discount = self.__get_full_discount(element)
        discount = self.__get_discount(full_discount)
        label = self.__get_label(full_discount)
        image = self.__get_image(element)
        url = self.__get_url(element)
        return Shop(name=name, discount=discount, label=label, image=image, url=url)

    def __get_name(self, element):
        page = element
        return page

    def __get_full_discount(self, element):
        pass

    def __get_discount(self, full_discount):
        pass

    def __get_label(self, full_discount):
        pass

    def __get_image(self, element):
        pass

    def __get_url(self, element):
        try:
            page = element.find_element_by_css_selector("div.holder-img > a").get_attribute("href")
            return page
        except:
            return None


if __name__ == '__main__':
    webDriverParsing = WebDriverParsing()
    webDriverParsing.parsing()

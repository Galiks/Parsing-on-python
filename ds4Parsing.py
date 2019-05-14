import time
from multiprocessing import Pool, current_process

import mysql.connector
import requests
from bs4 import BeautifulSoup

import shop as s
import valueForParsing as v
from parsingAbstractClass import Parsing


def test_DB():
    cnx = mysql.connector.connect(user='root', password='admin',
                                  host='localhost',
                                  database='forpython',
                                  auth_plugin='mysql_native_password')
    print("Connection Successful!")
    # mycursor = cnx.cursor()
    # mycursor.execute("")
    # myresult = mycursor.fetchall()
    # for x in myresult:
    #     print(x)
    cnx.close()


class BS4Parsing(Parsing):

    def __init__(self):
        pass

    def parsing(self):
        urls = []
        start_time = time.time()
        max_page = self.__max_page()
        for i in range(1, max_page + 1):
            urls.append(v.url_for_parsing_letyShops + str(i))
        pool = Pool(processes=4)
        result = pool.map(self.parse_elements, urls)
        print(len(result))
        print(time.time() - start_time)
        for items in result:
            self.print_array(items)

    def parse_elements(self, url):
        result = []
        soup = BeautifulSoup(self.__get_Html(url), 'lxml')
        shops = soup.find_all('div', class_='b-teaser')
        for shop in shops:
            name = self.__get_name(shop)
            discount = self.__get_discount(shop)
            label = self.__get_label(shop)
            url = self.__get_url(shop)
            image = self.__get_image(shop)
            item = s.Shop(name, discount, label, url, image)
            result.append(item)
        return result

    def __get_image(self, shop):
        image = shop.find('div', class_='b-teaser__cover').find('img').get('src')
        return image

    def __get_url(self, shop):
        url = shop.find('a', class_='b-teaser__inner').get('href')
        return v.clear_url_letyShops + url

    def __get_label(self, shop):
        label = shop.find('span', class_='b-shop-teaser__label')
        if label is None:
            label = shop.find('span', class_='b-shop-teaser__label--red')
        else:
            label = label.text.strip()
        return label

    def __get_discount(self, shop):
        discount = shop.find('span', class_='b-shop-teaser__cash')
        if discount is None:
            discount = shop.find('span', class_='b-shop-teaser__new-cash').text.strip()
        else:
            discount = discount.text.strip()
        return discount

    def __get_name(self, shop):
        name = shop.find('div', class_='b-teaser__title').text.strip()
        return name

    def __get_Html(self, url):
        try:
            r = requests.get(url)
            return r.text
        except ConnectionError as e:
            print("Error")

    def __max_page(self):
        soup = BeautifulSoup(self.__get_Html(v.letyShops), 'lxml')
        new_pages = []
        pages = soup.find_all('a', class_='b-pagination__link')
        for page in pages:
            new_page = int(page.get('data-page'))
            new_pages.append(new_page)
        return max(new_pages)

    def print_array(self, array: []):
        if len(array) > 0:
            for item in array:
                print(item.__str__())
        else:
            print("Пустой список")


if __name__ == '__main__':
    parser = BS4Parsing()
    parser.parsing()

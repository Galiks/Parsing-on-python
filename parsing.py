import time
from multiprocessing import Pool, Queue

import mysql.connector
import requests
from bs4 import BeautifulSoup

import shop as s
import valueForParsing as v


def test_DB(id, time):
    cnx = mysql.connector.connect(user='root', password='admin',
                                  host='127.0.0.1',
                                  database='forPython')
    mycursor = cnx.cursor()
    mycursor.execute("")
    myresult = mycursor.fetchall()
    for x in myresult:
        print(x)
    cnx.close()


class Parsing:
    __array = Queue()

    def __init__(self):
        urls = []
        max_page = self.__max_page()
        for i in range(1, max_page + 1):
            urls.append(v.url_for_parsing_letyShops + str(i))
        start_time = time.time()

        for url in urls:
            self.parsing(url)

        with Pool(4) as first:
            first.map(self.parsing, urls)
        print(time.time() - start_time)

    def parsing(self, url):
        soup = BeautifulSoup(self.__get_Html(url), 'lxml')
        shops = soup.find_all('div', class_='b-teaser')
        for shop in shops:
            name = self.__get_name(shop)
            discount = self.__get_discount(shop)
            label = self.__get_label(shop)
            url = self.__get_url(shop)
            image = self.__get_image(shop)
            item = s.Shop(name, discount, label, url, image)
            # print(item)
            self.__array.put(item)
            # s.Shop(name, discount, label, url, image))

    def __get_image(self, shop):
        image = shop.find('div', class_='b-teaser__cover').find('img').get('src')
        return image

    def __get_url(self, shop):
        url = shop.find('a', class_='b-teaser__inner').get('href')
        return v.clear_url_letyShops + url

    def __get_label(self, shop):
        label = shop.find('span', class_='b-shop-teaser__label ')
        if label is None:
            label = shop.find('span', class_='b-shop-teaser__label--red').text.strip()
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

    def print_array(self):
        while self.__array.get() != 0:
            print(self.__array.get())


if __name__ == '__main__':
    parsing = Parsing()
    parsing.print_array()

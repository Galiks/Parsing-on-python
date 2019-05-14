import time
from multiprocessing.pool import Pool

import requests
from bs4 import BeautifulSoup

import valueForParsing as v
from parsingAbstractClass import Parsing
import shop as s


class RequestsLetyShopsParsing(Parsing):
    __address = 'https://letyshops.com/shops?page='

    def __init__(self):
        pass

    def parsing(self):
        pool = Pool(processes=4)
        start_time = time.time()
        max_page = self.__max_page()
        all_items = pool.map(self.get_response, range(1, max_page + 1))
        result = pool.map(self.parse_elements, all_items)
        print(time.time() - start_time)
        for i in result:
            self.print_array(i)


    def get_response(self, i):
        url = "https://letyshops.com/shops"
        querystring = {"page": str(i)}
        payload = ""
        headers = {
            'User-Agent': "PostmanRuntime/7.11.0",
            'Accept': "*/*",
            'Cache-Control': "no-cache",
            'Postman-Token': "03d403a9-0fb6-4893-826c-6f67e5b323e1,5b89c07f-246f-4436-aadd-fa711d08cf04",
            'Host': "letyshops.com",
            'cookie': "hl=ru_RU; country=RU%3A0; lsvtkn=d7ca64e7165cfd3175dddfa1cc11bf15",
            'accept-encoding': "gzip, deflate",
            'Connection': "keep-alive",
            'cache-control': "no-cache"
        }

        response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
        result = response.content
        return response.content

    def parse_elements(self, html):
        result = []
        soup = BeautifulSoup(html, 'lxml')
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

    def print_array(self, array: []):
        if len(array) > 0:
            for item in array:
                print(item.__str__())
        else:
            print("Пустой список")

    def __max_page(self):
        soup = BeautifulSoup(self.__get_Html(v.letyShops), 'lxml')
        new_pages = []
        pages = soup.find_all('a', class_='b-pagination__link')
        for page in pages:
            new_page = int(page.get('data-page'))
            new_pages.append(new_page)
        return max(new_pages)

    def __get_Html(self, url):
        try:
            r = requests.get(url)
            return r.text
        except ConnectionError as e:
            print("Error")


if __name__ == '__main__':
    parser = RequestsLetyShopsParsing()
    parser.parsing()

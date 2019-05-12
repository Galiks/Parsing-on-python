import json
import time
from multiprocessing.pool import Pool

import requests

from parsingAbstractClass import Parsing
from shop import Shop


class RequestsParsing(Parsing):
    __address = "https://www.kopikot.ru/"

    def __init__(self):
        pass

    def parsing(self):
        i = [0, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300]
        pool = Pool(processes=4)
        start_time = time.time()
        all_items = (pool.map(self.get_json, i))
        result = pool.map(self.parse_elements, all_items)
        print(time.time() - start_time)
        for item in result:
            self.print_array(item)

    def get_json(self, i):
        url = "https://d289b99uqa0t82.cloudfront.net/sites/5/campaigns_limit_100_offset_" + str(
            i) + "_order_popularity.json"
        payload = ""
        headers = {
            'User-Agent': "PostmanRuntime/7.11.0",
            'Accept': "*/*",
            'Cache-Control': "no-cache",
            'Postman-Token': "b6eeb7b4-63dd-454e-b213-6d2d62b74946,1e851911-db3b-4406-88de-5ffc9ecbaa5d",
            'Host': "d289b99uqa0t82.cloudfront.net",
            'accept-encoding': "gzip, deflate",
            'Connection': "keep-alive",
            'cache-control': "no-cache"
        }
        response = requests.request("GET", url, data=payload, headers=headers)
        data = json.loads(response.text)
        items = data["items"]
        return items

    def parse_elements(self, items):
        result = []
        for item in items:
            name = self.__get_name(item)
            discount = self.__get_discount(item)
            label = self.__get_label(item)
            image = self.__get_image(item)
            page = self.__get_url(item)
            result.append(Shop(name=name, discount=discount, label=label, image=image, url=page))
        return result

    def __get_name(self, item):
        return item["title"]

    def __get_discount(self, item):
        discount = item["commission"]["max"]["original_amount"]
        try:
            return float(discount)
        except ValueError:
            return None

    def __get_label(self, item):
        return item["commission"]["max"]["unit"]

    def __get_image(self, item):
        return item["image"]["url"]

    def __get_url(self, item):
        id = item["id"]
        url = item["url"]
        return self.__address + url + "/" + id

    def print_array(self, array: []):
        if len(array) > 0:
            for item in array:
                print(item.__str__())
        else:
            print("Пустой список")


if __name__ == '__main__':
    parser = RequestsParsing()
    parser.parsing()

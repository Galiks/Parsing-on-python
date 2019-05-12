class Shop:
    __name = ''
    __discount = ''
    __label = ''
    __url = ''
    __image = ''

    def __init__(self):
        pass

    def __init__(self, name, discount, label, url, image):
        self.__name = name
        self.__discount = discount
        self.__label = label
        self.__url = url
        self.__image = image

    def __str__(self):
        return '({}, {}{}, {}, {})'.format(self.__name, self.__discount, self.__label, self.__image, self.__url)

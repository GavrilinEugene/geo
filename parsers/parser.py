from abc import ABC
from bs4 import BeautifulSoup
import re

class FlatParser(ABC):

    """ Интерфейс парсинга сайта недвижимости """
    def __init__(self, source_page):
        self.source_page = source_page

    def parse(self):
        raise NotImplementedError("Please Implement this method")

    def __get_flat_square(self):
        raise NotImplementedError("Please Implement this method")

    def __get_price(self):
        raise NotImplementedError("Please Implement this method")

    def __get_coordinates(self):
        raise NotImplementedError("Please Implement this method")

    def __get_floor(self):
        raise NotImplementedError("Please Implement this method")


class AvitoFlatParser(FlatParser):

    def parse(self):
        self.__get_flat_square()
        self.__get_coordinates()
        self.__get_price()
        self.__get_floor()

    def __init__(self, id, source_page):
        super().__init__(source_page)
        self.id = id
        self.soup = BeautifulSoup(self.source_page, 'lxml')

    def get_output(self):
        d = {'id': self.id,
             'lat': self.coordinates[0],
             'lon': self.coordinates[1],
             'price': self.price,
             'floor': self.floor,
             'square': self.flat_square}
        return d

    def __get_param(self, text):
        try:
            div_params = self.soup.find_all("li", class_="item-params-list-item")
            div_params = [x for x in div_params if text in str(x)]
            result = div_params[0].text
        except Exception as e:
            print(str(e))
            result = -1
        return result

    def __get_flat_square(self):
        try:
            div_params = self.soup.find_all("li", class_="item-params-list-item")
            div_params = [x for x in div_params if 'Общая площадь:' in str(x)]
            result = div_params[0].text.split(':')[1][1:-4]
        except Exception as e:
            print(str(e))
            result = -1
        self.flat_square = result

    def __get_price(self):
        div_params = self.soup.find_all("span", class_="js-item-price")
        self.price = int(div_params[0].text.replace(" ", ""))

    def __get_coordinates(self):
        div_params = self.soup.find_all("div", class_="b-search-map expanded item-map-wrapper js-item-map-wrapper")
        if len(div_params) == 1:
            self.coordinates = (div_params[0]['data-map-lat'], div_params[0]['data-map-lon'])

    def __get_floor(self):
        try:
            div_params = self.soup.find_all("li", class_="item-params-list-item")
            div_params = [x for x in div_params if 'Этаж:' in str(x)]
            result = int(div_params[0].text.split(':')[1][1:].replace(" ", ""))
        except Exception as e:
            print(str(e))
            result = -1
        self.floor = result


class CianFlatParser(FlatParser):

    def parse(self):
        self.__get_flat_square()
        self.__get_address()
        self.__get_price()
        self.__get_floor()
        self.__get_house_age()

    def __init__(self, id, source_page):
        super().__init__(source_page)
        self.id = id
        self.soup = BeautifulSoup(self.source_page, 'lxml')

    def get_output(self):
        d = {'id': self.id,
             'address': self.address,
             'price': self.price,
             'floor': self.floor,
             'square': self.flat_square,
             'age': self.age}
        return d

    def __get_flat_square(self):
        regex = re.compile('.*--info-text--.*')
        div_params = self.soup.find_all("div", {"class": regex})
        try:
            self.flat_square = re.sub('\D', '', div_params[0].text)
        except Exception as e:
            self.flat_square = -1

    def __get_price(self):
        div_params = self.soup.find_all("span", itemprop="price")
        try:
            self.price = re.sub('\D', '', div_params[0].text)
        except Exception as e:
            self.price = -1

    def __get_coordinates(self):
        # this method is impossible for cian
        pass

    def __get_address(self):
        regex = re.compile('.*--geo--.*')
        div_params = self.soup.find_all("div", {"class": regex})
        # print(div_params[0].text)
        try:
            self.address = div_params[0].text.split('На карте')[0]
        except:
            self.address = ''

    def __get_floor(self):
        regex = re.compile('.*--info-text--.*')
        div_params = self.soup.find_all("div", {"class": regex})
        try:
            self.floor = int(div_params[3].text.split(' ')[0])
        except Exception as e:
            self.floor = -1

    def __get_house_age(self):
        regex = re.compile('.*--info-text--.*')
        div_params = self.soup.find_all("div", {"class": regex})
        try:
            self.age = int(div_params[4].text.split(' ')[0])
        except Exception as e:
            self.age = -1


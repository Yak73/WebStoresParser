import json
from urllib.parse import urljoin
import re
from bs4 import BeautifulSoup
import requests
import random
from http.cookies import SimpleCookie

import debug

header_filename = 'Http_headers.json'


def get_store_params(store_short_title, category=None, search_line_txt=None):
    _store_params = {}

    if store_short_title == 'dns':
        _store_params["url"] = f'https://www.dns-shop.ru/'
        if category:
            if category == 'VideoCard':
                _store_params["url"] = f'https://www.dns-shop.ru/catalog/17a89aab16404e77/videokarty/?q={search_line_txt}&stock=now-today-tomorrow&p=1'
        elif search_line_txt:
            _store_params["url"] = f'https://www.dns-shop.ru/search/?q={search_line_txt}&p=1&order=popular&stock=all'
        else:  # Видеокарты
            _store_params["url"] = f'https://www.dns-shop.ru/catalog/17a89aab16404e77/videokarty/'

        _store_params["headers"] = get_headers_from_file(header_filename, store_short_title)
        _store_params["link_class_name"] = 'catalog-product__name'
        _store_params["requires_request_for_every_product"] = True
        _store_params["delay_sec"] = 0

    if store_short_title == 'citilink':
        if search_line_txt:
            _store_params["url"] = f'https://www.citilink.ru/search/?text={search_line_txt}'
        else:
            _store_params["url"] = f'https://www.citilink.ru/catalog/videokarty/'

        # без этих параметров либо долгие запросы, либо ошибка 429 на контроль от DDOS
        _store_params["headers"] = get_headers_from_file(header_filename, store_short_title)
        # _headers['cookie'] = SimpleCookie()
        _store_params["link_class_name"] = 'ProductCardVertical__name'
        _store_params["requires_request_for_every_product"] = False
        _store_params["delay_sec"] = random.randint(1, 5)

    return _store_params


def get_headers_from_file(filename, store_short_title):
    with open(filename) as f:
        headers = json.load(f)
    for store_header in headers["headers"]:
        if store_header["name"] == store_short_title:
            return store_header["header"]


def get_products(store_short_title='dns', search_line_txt=None,
                 category=None, required_str_in_title=None, except_str_in_title=None):
    """
    Процедура находит  товары на указанных сайтах
    Если search_line указан, то товары, которые нашлись по строке search_line
    Иначе ищет все товары
    """

    store_params = get_store_params(store_short_title, category, search_line_txt)

    rs = requests.get(store_params["url"], headers=store_params["headers"], timeout=5)
    if rs.status_code == 429:
        store_params["headers"]["Cookie"] = None
        rs = requests.get(store_params["url"], headers=store_params["headers"], timeout=15)
        if rs.status_code == 429:
            raise Exception(f'Ошибка при отправки запроса к магазину. Слишком много запросов. \n'
                            f'Код: {rs.status_code}. Текст ошибки: {rs.reason}')
    elif rs.status_code != 200:
        raise Exception(f'Ошибка при отправки запроса к магазину. \n'
                        f'Код: {rs.status_code}. Текст ошибки: {rs.reason}')
    # print(rs.status_code, rs.text)
    data = json.loads(rs.text)
    root = BeautifulSoup(data['html'], 'html.parser')
    # debug.save_response(root)
    products = []

    if store_short_title == 'dns':
        for link in root.find_all('a'):
            # print(link.attrs)
            # print(link['class'])
            if store_params["link_class_name"] in link['class']:
                if (str(required_str_in_title).lower() in str(link.text).lower() or required_str_in_title is None)\
                        and (str(except_str_in_title).lower() not in str(link.text).lower() or except_str_in_title is None):
                    # print('Ссылка: {}'.format(link['href']))
                    # print('Название: {}'.format(link.text))
                    # print(urljoin(rs.url, link['href']))
                    full_title = link.text
                    # Видеокарта Palit GeForce RTX 3060 Ti DUAL (LHR)
                    # [NE6306T019P2-190AD] [PCI-E 4.0, 8 ГБ GDDR6, 256 бит, 1410 МГц - 1665 МГц, DisplayPort x3, HDMI]
                    # -> Видеокарта Palit GeForce RTX 3060 Ti DUAL (LHR)
                    short_title = re.sub(r'\[.*\]', '', full_title)
                    short_title = short_title.replace('Видеокарта ', '').strip()
                    full_link = urljoin(rs.url, link['href'])
                    products.append(
                        {"full_title": full_title,
                         "full_link": full_link,
                         "price": None,
                         "short_title": short_title,
                         "search_line": search_line_txt
                         }
                    )
    if store_short_title == 'citilink':
          for div in root.find_all(
                  name="div",
                  attrs={"class": "product_data__gtm-js product_data__pageevents-js ProductCardVertical "
                                  "js--ProductCardInListing ProductCardVertical_normal ProductCardVertical_shadow-hover "
                                  "ProductCardVertical_separated"}):
            """
            '{"id":"1542015","categoryId":29,"price":47990,"oldPrice":55990,
            "shortName":"Видеокарта Palit NVIDIA  GeForce RTX 3060Ti,  PA-RTX3060Ti DUAL 8G V1 LHR",
            "categoryName":"Видеокарты","brandName":"PALIT","clubPrice":47990,"multiplicity":1}'
            """
            product_info_str = div["data-params"]
            product_info_dict = json.loads(product_info_str)
            main_name = product_info_dict["shortName"]
            if (str(required_str_in_title).lower() in str(main_name).lower() or required_str_in_title is None)\
                    and (str(except_str_in_title).lower() not in str(main_name).lower() or except_str_in_title is None):
                full_title = product_info_dict["shortName"]
                #short_title = re.sub(r',.*', '', full_title)
                short_title = product_info_dict["shortName"]
                short_title = short_title.replace('Видеокарта ', '').strip()
                relative_link = div.contents[0]["href"]
                full_link = urljoin(rs.url, relative_link)
                price = int(product_info_dict["price"])
                products.append(
                    {"full_title": full_title,
                     "full_link": full_link,
                     "price": price,
                     "short_title": short_title,
                     "search_line": search_line_txt
                     }
                )
    return products


def get_product_price(store_short_title, product_full_link):
    store_params = get_store_params(store_short_title)

    rs = requests.get(product_full_link, headers=store_params["headers"], timeout=10)
    # print(rs.status_code, rs.text)

    # dataform = str(rs.text).strip("'<>() ").replace('\'', '\"')
    # dataform = str(rs.text).replace('—', '')
    dataform = str(rs.text).strip("'<>() ").replace('\'', '\"').replace('—', '').replace('\n', '')
    data = json.loads(rs.text)
    # print(data)

    root = BeautifulSoup(data['html'], 'html.parser')
    # print(root.text)

    for tag_data in root.find_all('script'):
        # tag_data = ..."price":6199,...
        price = re.search(r'\"price\":(\d+),', tag_data.text).group(1)
        # print(price)
        if price is not None:
            try:
                price = int(price)
                return price
            except:  # если нашли поле с ценой, но в поле не число
                return -1
    return -1
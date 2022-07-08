import json
from urllib.parse import urljoin
import re

from bs4 import BeautifulSoup
import requests
from http.cookies import SimpleCookie

headers = {'Accept': '*/*',
           'Accept-Encoding': 'gzip, deflate, br',
           'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,ar;q=0.6',
           'Cache-Control': 'max-age=0',
           'Connection': 'keep-alive',
           'Cookie': 'ipp_uid2=lO6pmGWtpS2hHviX/i19ZlQokdFH1tWGOERa07Q==; ipp_uid1=1599561500194; ipp_uid=1599561500194/lO6pmGWtpS2hHviX/i19ZlQokdFH1tWGOERa07Q==; _ym_uid=1599561502951486989; rrpvid=211883758711023; rcuid=5f575f1f9e9fa5000120bee0; tmr_lvidTS=1618677704787; tmr_lvid=64646a11cd54dc5e96a1a97d446f38c3; phonesIdent=718f755be066ead1e3fa4d58dc609d10e0b07725c3eb2be1fe3b073db2e6a068a%3A2%3A%7Bi%3A0%3Bs%3A11%3A%22phonesIdent%22%3Bi%3A1%3Bs%3A36%3A%228cc779c2-372e-4dbc-90e1-dc09f7319875%22%3B%7D; __ttl__widget__ui=1640517798436-655b1fecd0b5; auth_public_uid=3d29222ae30e32aff405c9a975f3cd57; rrlevt=1646642931086; _ab_=a3beea7dee9e28b54d17a2a6e78bf152cc96eb64e6509aa9c8c7db3063a14bcba%3A2%3A%7Bi%3A0%3Bs%3A4%3A%22_ab_%22%3Bi%3A1%3Ba%3A1%3A%7Bs%3A12%3A%22price-filter%22%3Bs%3A14%3A%22CATALOG_NORMAL%22%3B%7D%7D; _gcl_au=1.1.540178676.1652971259; _ym_d=1652971261; cartUserCookieIdent_v3=ad60d6728e29ea3de5ab83df597175e4228a02b7a56161a3ec4d6272f6b79c2ca%3A2%3A%7Bi%3A0%3Bs%3A22%3A%22cartUserCookieIdent_v3%22%3Bi%3A1%3Bs%3A36%3A%22d935c6b4-c784-3b78-a6f6-2d169e4cb130%22%3B%7D; date-user-last-order-v2=5de1b214852e018a2ba97856b2d83cc243f69db0d89f86a69975717eaa0d5603a%3A2%3A%7Bi%3A0%3Bs%3A23%3A%22date-user-last-order-v2%22%3Bi%3A1%3Bi%3A1647602267%3B%7D; _gaexp=GAX1.2.F5r0LoWFQuaGkKl-pfLADg.19228.0; rerf=AAAAAGKsnvta8cryELRBAg==; PHPSESSID=2dfd3405e6b3ada56779ae324e8e12e9; _gid=GA1.2.851020031.1656495179; cookieImagesUploadId=cc943eb3a01423a3f969903d8f21bd5a194122298711294f075040a7033a6d26a%3A2%3A%7Bi%3A0%3Bs%3A20%3A%22cookieImagesUploadId%22%3Bi%3A1%3Bs%3A36%3A%227d39f22f-809a-445a-8673-5f2e62f09eb3%22%3B%7D; current_path=605bfdc517d7e9e23947448a9bf1ce16ac36b884434a3fdb10db053793c50392a%3A2%3A%7Bi%3A0%3Bs%3A12%3A%22current_path%22%3Bi%3A1%3Bs%3A115%3A%22%7B%22city%22%3A%2230b7c1f3-03fb-11dc-95ee-00151716f9f5%22%2C%22cityName%22%3A%22%5Cu041c%5Cu043e%5Cu0441%5Cu043a%5Cu0432%5Cu0430%22%2C%22method%22%3A%22manual%22%7D%22%3B%7D; cf_avails=now-today-tomorrow; lang=ru; _csrf=dc7090c0ee913347c18268a2e2271a13bc99e8b7ea72a48af3cdb4621a1d02f2a%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%2248KPAnwqvKrKpUYAyEaxEzUJVCVfCUkN%22%3B%7D; _ym_isad=1; ipp_key=v1656572915932/v33947245ba5adc7a72e273/QT5dxLxlnR7X6hwNnZdyVg==; tmr_detect=1%7C1656572917783; _ym_visorc=b; _ga=GA1.2.820437372.1599561502; _gat_UA-8349380-2=1; _gali=select-city; tmr_reqNum=1320; dnsauth_csrf=036d80adbbcc4bc54e2d4647708fd538eb5b4b59e6019a12c0d86cd9d024e8e5a%3A2%3A%7Bi%3A0%3Bs%3A12%3A%22dnsauth_csrf%22%3Bi%3A1%3Bs%3A36%3A%226796f1cd-7b66-4409-9c04-f8d7e56d19ad%22%3B%7D; _ga_FLS4JETDHW=GS1.1.1656572917.62.1.1656574630.0',
           'Host': 'www.dns-shop.ru',
           'Referer': 'https://www.dns-shop.ru/catalog/17a89aab16404e77/videokarty/no-referrer',
           'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
           'sec-ch-ua-mobile': '?0',
           'sec-ch-ua-platform': '"Windows"',
           'Sec-Fetch-Dest': 'empty',
           'Sec-Fetch-Mode': 'cors',
           'Sec-Fetch-Site': 'same-origin',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
           'X-CSRF-Token': 'xY9m8hfcySAGxJk-Fn4I9vQdpY5S8cxPUdaAugitKljxty2iVrK-UXCP63VmK1G3jVjE9heLmQUHldbcS_hBFg==',
           'X-Requested-With': 'XMLHttpRequest'}


def get_products(search_line_txt=None, category=None, required_str_in_title=None, except_str_in_title=None):
    """
    Процедура находит  товары на сайте dns-shop.ru.
    Если search_line указан, то товары, которые нашлись по строке search_line
    Иначе ищет все видеокарты
    """
    url = f'https://www.dns-shop.ru/'
    if category:
        if category == 'VideoCard':
            url = f'https://www.dns-shop.ru/catalog/17a89aab16404e77/videokarty/?q={search_line_txt}&stock=now-today-tomorrow&p=1'
    elif search_line_txt:
        url = f'https://www.dns-shop.ru/search/?q={search_line_txt}&p=1&order=popular&stock=all'
    else:  # Видеокарты
        url = f'https://www.dns-shop.ru/catalog/17a89aab16404e77/videokarty/'
    rs = requests.get(url, headers=headers, timeout=10)
    # print(rs.status_code, rs.text)

    data = json.loads(rs.text)
    # print(data)

    root = BeautifulSoup(data['html'], 'html.parser')

    products = []
    for link in root.find_all('a'):
        # print(link.attrs)
        if 'catalog-product__name' in link['class']:
            if (str(required_str_in_title).lower() in str(link.text).lower() or required_str_in_title is None)\
                    and (str(except_str_in_title).lower() not in str(link.text).lower() or except_str_in_title is None):
                # print('Ссылка: {}'.format(link['href']))
                # print('Название: {}'.format(link.text))
                # print(urljoin(rs.url, link['href']))
                full_title = link.text
                # Видеокарта Palit GeForce RTX 3060 Ti DUAL (LHR)
                # [NE6306T019P2-190AD] [PCI-E 4.0, 8 ГБ GDDR6, 256 бит, 1410 МГц - 1665 МГц, DisplayPort x3, HDMI]
                # -> Видеокарта Palit GeForce RTX 3060 Ti DUAL (LHR)
                full_link = urljoin(rs.url, link['href'])
                short_title = re.sub(r'\[.*\]', '', link.text)
                short_title = short_title.replace('Видеокарта ', '').strip()
                products.append(
                    {"full_title": full_title,
                     "full_link": full_link,
                     "price": None,
                     "short_title": short_title,
                     "search_line": search_line_txt
                     }
                )
    return products


def get_product_price(product_full_link):
    rs = requests.get(product_full_link, headers=headers, timeout=10)
    # print(rs.status_code, rs.text)

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
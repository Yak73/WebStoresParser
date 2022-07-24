import json
from urllib.parse import urljoin
import re
from bs4 import BeautifulSoup
import requests
import random
from http.cookies import SimpleCookie

import debug


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

        _store_params["headers"] = {
            'Connection': 'keep-alive',
            'Cookie': 'ipp_uid2=lO6pmGWtpS2hHviX/i19ZlQokdFH1tWGOERa07Q==; ipp_uid1=1599561500194; ipp_uid=1599561500194/lO6pmGWtpS2hHviX/i19ZlQokdFH1tWGOERa07Q==; _ym_uid=1599561502951486989; rrpvid=211883758711023; rcuid=5f575f1f9e9fa5000120bee0; tmr_lvidTS=1618677704787; tmr_lvid=64646a11cd54dc5e96a1a97d446f38c3; phonesIdent=718f755be066ead1e3fa4d58dc609d10e0b07725c3eb2be1fe3b073db2e6a068a%3A2%3A%7Bi%3A0%3Bs%3A11%3A%22phonesIdent%22%3Bi%3A1%3Bs%3A36%3A%228cc779c2-372e-4dbc-90e1-dc09f7319875%22%3B%7D; __ttl__widget__ui=1640517798436-655b1fecd0b5; auth_public_uid=3d29222ae30e32aff405c9a975f3cd57; rrlevt=1646642931086; _ab_=a3beea7dee9e28b54d17a2a6e78bf152cc96eb64e6509aa9c8c7db3063a14bcba%3A2%3A%7Bi%3A0%3Bs%3A4%3A%22_ab_%22%3Bi%3A1%3Ba%3A1%3A%7Bs%3A12%3A%22price-filter%22%3Bs%3A14%3A%22CATALOG_NORMAL%22%3B%7D%7D; _gcl_au=1.1.540178676.1652971259; _ym_d=1652971261; cartUserCookieIdent_v3=ad60d6728e29ea3de5ab83df597175e4228a02b7a56161a3ec4d6272f6b79c2ca%3A2%3A%7Bi%3A0%3Bs%3A22%3A%22cartUserCookieIdent_v3%22%3Bi%3A1%3Bs%3A36%3A%22d935c6b4-c784-3b78-a6f6-2d169e4cb130%22%3B%7D; date-user-last-order-v2=5de1b214852e018a2ba97856b2d83cc243f69db0d89f86a69975717eaa0d5603a%3A2%3A%7Bi%3A0%3Bs%3A23%3A%22date-user-last-order-v2%22%3Bi%3A1%3Bi%3A1647602267%3B%7D; _gaexp=GAX1.2.F5r0LoWFQuaGkKl-pfLADg.19228.0; rerf=AAAAAGKsnvta8cryELRBAg==; PHPSESSID=2dfd3405e6b3ada56779ae324e8e12e9; _gid=GA1.2.851020031.1656495179; cookieImagesUploadId=cc943eb3a01423a3f969903d8f21bd5a194122298711294f075040a7033a6d26a%3A2%3A%7Bi%3A0%3Bs%3A20%3A%22cookieImagesUploadId%22%3Bi%3A1%3Bs%3A36%3A%227d39f22f-809a-445a-8673-5f2e62f09eb3%22%3B%7D; current_path=605bfdc517d7e9e23947448a9bf1ce16ac36b884434a3fdb10db053793c50392a%3A2%3A%7Bi%3A0%3Bs%3A12%3A%22current_path%22%3Bi%3A1%3Bs%3A115%3A%22%7B%22city%22%3A%2230b7c1f3-03fb-11dc-95ee-00151716f9f5%22%2C%22cityName%22%3A%22%5Cu041c%5Cu043e%5Cu0441%5Cu043a%5Cu0432%5Cu0430%22%2C%22method%22%3A%22manual%22%7D%22%3B%7D; cf_avails=now-today-tomorrow; lang=ru; _csrf=dc7090c0ee913347c18268a2e2271a13bc99e8b7ea72a48af3cdb4621a1d02f2a%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%2248KPAnwqvKrKpUYAyEaxEzUJVCVfCUkN%22%3B%7D; _ym_isad=1; ipp_key=v1656572915932/v33947245ba5adc7a72e273/QT5dxLxlnR7X6hwNnZdyVg==; tmr_detect=1%7C1656572917783; _ym_visorc=b; _ga=GA1.2.820437372.1599561502; _gat_UA-8349380-2=1; _gali=select-city; tmr_reqNum=1320; dnsauth_csrf=036d80adbbcc4bc54e2d4647708fd538eb5b4b59e6019a12c0d86cd9d024e8e5a%3A2%3A%7Bi%3A0%3Bs%3A12%3A%22dnsauth_csrf%22%3Bi%3A1%3Bs%3A36%3A%226796f1cd-7b66-4409-9c04-f8d7e56d19ad%22%3B%7D; _ga_FLS4JETDHW=GS1.1.1656572917.62.1.1656574630.0',
            'Referer': 'https://www.dns-shop.ru/catalog/17a89aab16404e77/videokarty/no-referrer',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }
        _store_params["link_class_name"] = 'catalog-product__name'
        _store_params["requires_request_for_every_product"] = True
        _store_params["delay_sec"] = 0

    if store_short_title == 'citilink':
        if search_line_txt:
            _store_params["url"] = f'https://www.citilink.ru/search/?text={search_line_txt}'
        else:
            _store_params["url"] = f'https://www.citilink.ru/catalog/videokarty/'

        # без этих параметров либо долгие запросы, либо ошибка 429 на контроль от DDOS
        _store_params["headers"] = {
            'cookie': 'is_gdpr=0; is_gdpr_b=CLPpZRC/KigC; _ym_uid=1599470899733778903; my=YwA=; gdpr=0; yandex_login=Yak73-rus; yandexuid=2305449891599470896; yuidss=2305449891599470896; ymex=1622134352.oyu.2785690541619180546#1944312070.yrts.1628952070#1934902352.yrtsi.1619542352; bltsr=1; FgkKdCjPqoMFm=1; computer=1; EIXtkCTlX=1; i=nMQg4Un11GcWj6L0pj2zOGxrautltG76j85Uhvqv8LeUhW/mfxPb48vyiyHfWtTP2kT8HTUBjwU+2cqs6c3wgcvlhPY=; JPIqApiY=1; Session_id=3:1658597870.5.0.1619456026407:VnmKLg:c.1.2:1|293806925.28828504.2.2:28828504|3:10255701.319829.L0k8BZpoCB2dyBPB-QeqrrNQyg4; sessionid2=3:1658597870.5.0.1619456026407:VnmKLg:c.1.2:1.499:1|293806925.28828504.2.2:28828504|3:10255701.366419.LOsvTqQ54Zx7XsTBInLmhHiMTc0; yandex_gid=213; KIykI=1; _ym_d=1658653932; yabs-sid=1932848711658653933; yabs-frequency=/5/2m0h05uMtM9VwDTY/sLLbIOQoDsUiHoTj45m-fFqjKwn7GMRnK6c8IUD1h4SYy6EuF5grp6MiHo7Mk0qshfhSNAn78TKb50d7dPTVh4SW1LmOhY66wcEiHo6rb5iyMt5ZNAn78oBjJmGCfCPkh4SZVismx8GRHaUaHoFkZ9N-eSoLPAH7Ov5aP3ZcsLfGe4Ski263EeFXn4UiHs2pwPbluBlKNPn7Hyqp5qk_ce1Rd4TUrmPM5tbXVLMiHy0oszepqxP8LQr780AOGGuyuQxiRgr7e07jPDh2AzMyLwn788WrerNmNgPGh4SW0jftro-gkd-iHo1Mv5Okcw6rMgr7O08QpcoU-EXqNAn7O9HVqWhzW-9hh4VWkwrkhxONOqUjHm02ujohYroPR7wjHq04lpDzLOOKS6IiHy0-ItC7Mg8kKQr780kpmgSFvWC9Vgn781tEUwKHQlDzhKSW1sSzIil4RVLYhKSW0ROkNj3VysTchKV00jyrK5Zj9wv1hKTW0Yj_8LShdnDwh4T04sifM5S0002iHq26P1axLu_qPwr7u07zlprY9w0GHAr7G0T9znZMNaanTgr780JDDbxWAj0MMAr700JLFXgDoFI4RQr7W07iOFQfs3uJUgn78FiI772I0000h4SWrfcrSWOlE7oiHo20aHJH_ZZlOgn7m5FgNBbbKZbzh4U0Y0ySS980002jHq01JdAmS9K0002iHo0qPUZmFLzFGQn7W9TFCfOc6YvAhKU03ACrP3LaKTjohKUW0MDAzBnKAfvuhKU03EVKMeZ0tpPuh4SWwxjfm3lv8aAiHo1FxHVfsxKdQwn7e4FjdB4VWQD1h4T0a62RphHqF7YiH-2MovQEGxZsIQr7u0ApivOj23hJVAr7W0WqG1nmaW000An7u6iLMhk8p6jDh4T0EVO5NsjDbLkjHu01z6wmS9K0002iHs0ZaSBUj4_2Vgn7eE3EJuJ4r9juhKU0305Li72L0000h4SWjtMAP2tUwNsiHo2O3dDmb0000An7G29wi72L0000hKU01VYx59L_SS90h4UW0MsmS9K0002iHo33LcNyw71iLQr7m0Q_IXxdXH1wUAr7u0BFvzd02YukLgr7W0phLB1mbG000Ar780AdRx1mbG000An78Ervi72L0000h4SWlrcmS9K0002iH-3iUB1mbG000Ar7007xLB1mbG000Ar7e0S0/; _ym_isad=1; ys=mclid.2163430#wprid.1658672609263172-9340563054043492603-vla1-2969-vla-l7-balancer-8080-BAL-5556#startextchrome.8-24-9',
            'referer': 'https://www.citilink.ru/search/?text=3060ti',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gec',
            'X-Requested-With': 'XMLHttpRequest'
        }
        # _headers['cookie'] = SimpleCookie()
        _store_params["link_class_name"] = 'ProductCardVertical__name'
        _store_params["requires_request_for_every_product"] = False
        _store_params["delay_sec"] = random.randint(1, 5)

    return _store_params


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
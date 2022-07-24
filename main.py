import sys
import argparse
import time

import web
import db


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--is_save_in_db', default=1)
    parser.add_argument('-dm', '--is_debug_mode', default=0)
    parser.add_argument('-p', '--is_print_all_records_from_db', default=0)
    return parser


def init_params():
    _namespace = create_parser().parse_args()

    _all_search_lines = [
        {'search_line_txt': 'Geforce RTX3050', 'category': 'VideoCard',
         'required_str_in_title': 'Видеокарта', 'except_str_in_title': 'ti'},
        {'search_line_txt': 'Geforce RTX3060', 'category': 'VideoCard',
         'required_str_in_title': 'Видеокарта', 'except_str_in_title': 'ti'},
        {'search_line_txt': 'Geforce RTX3060 Ti', 'category': 'VideoCard',
         'required_str_in_title': 'Видеокарта', 'except_str_in_title': None},
        {'search_line_txt': 'Geforce RTX3070', 'category': 'VideoCard',
         'required_str_in_title': 'Видеокарта', 'except_str_in_title': 'ti'},
        {'search_line_txt': 'Geforce RTX3070 Ti', 'category': 'VideoCard',
         'required_str_in_title': 'Видеокарта', 'except_str_in_title': None},
        {'search_line_txt': 'Geforce RTX3080', 'category': 'VideoCard',
         'required_str_in_title': 'Видеокарта', 'except_str_in_title': 'ti'},
        {'search_line_txt': 'Geforce RTX3080 Ti', 'category': 'VideoCard',
         'required_str_in_title': 'Видеокарта', 'except_str_in_title': None},
        {'search_line_txt': 'Geforce RTX3090', 'category': 'VideoCard',
         'required_str_in_title': 'Видеокарта', 'except_str_in_title': 'ti'},
        {'search_line_txt': 'Geforce RTX3090 Ti', 'category': 'VideoCard',
         'required_str_in_title': 'Видеокарта', 'except_str_in_title': None},
        {'search_line_txt': 'Radeon RX 6500', 'category': 'VideoCard',
         'required_str_in_title': 'Видеокарта', 'except_str_in_title': 'xt'},
        {'search_line_txt': 'Radeon RX 6500 XT', 'category': 'VideoCard',
         'required_str_in_title': 'Видеокарта', 'except_str_in_title': None},
        {'search_line_txt': 'Radeon RX 6600', 'category': 'VideoCard',
         'required_str_in_title': 'Видеокарта', 'except_str_in_title': 'xt'},
        {'search_line_txt': 'Radeon RX 6600 XT', 'category': 'VideoCard',
         'required_str_in_title': 'Видеокарта', 'except_str_in_title': None},
        {'search_line_txt': 'Radeon RX 6700 XT', 'category': 'VideoCard',
         'required_str_in_title': 'Видеокарта', 'except_str_in_title': None},
        {'search_line_txt': 'Radeon RX 6800', 'category': 'VideoCard',
         'required_str_in_title': 'Видеокарта', 'except_str_in_title': 'xt'},
        {'search_line_txt': 'Radeon RX 6800 XT', 'category': 'VideoCard',
         'required_str_in_title': 'Видеокарта', 'except_str_in_title': None},
        {'search_line_txt': 'Radeon RX 6900 XT', 'category': 'VideoCard',
         'required_str_in_title': 'Видеокарта', 'except_str_in_title': None},
    ]

    if len(sys.argv) > 1:  # запуск из вне
        print('Запуск осуществлен c передачей аргументов')
        _is_save_in_db = int(_namespace.is_save_in_db)
        _is_debug_mode = int(_namespace.is_debug_mode)
        _is_print_all_records_from_db = int(_namespace.is_print_all_records_from_db)
    else:  # запускаем напрямую, не передавая аргументов
        print('Запуск осуществлен без передачи аргументов')
        _is_save_in_db = 1
        _is_debug_mode = 0
        _is_print_all_records_from_db = 0

    if _is_debug_mode:
        _search_line_txt_only = 'Geforce RTX3060 Ti'
    else:
        _search_line_txt_only = None

    _stores = ['dns', 'citilink']

    return _stores, _all_search_lines, _is_save_in_db, _is_debug_mode, _is_print_all_records_from_db, \
        _search_line_txt_only


if __name__ == '__main__':

    stores, all_search_lines, is_save_in_db, is_debug_mode, \
        is_print_all_records_from_db, search_line_txt_only = init_params()

    db.create_db()

    for store in stores:
        # if store == 'dns':
            # continue
        print('Магазин: {}. Начало запроса данных по списку строк поиска. Всего {} строк поиска'
              .format(store, len(all_search_lines)))
        for search_line in all_search_lines:
            if is_debug_mode and search_line_txt_only:
                if search_line['search_line_txt'] != search_line_txt_only:
                    continue

            print('Запрос: {}'.format(search_line['search_line_txt']))

            # Получаем товары
            products = web.get_products(store_short_title=store,
                                        search_line_txt=search_line['search_line_txt'],
                                        category=search_line['category'],
                                        required_str_in_title=search_line['required_str_in_title'],
                                        except_str_in_title=search_line['except_str_in_title'])
            if is_debug_mode and products == []:
                print('По запросу: {} - пустой список товаров'.format(search_line['search_line_txt']))

            store_params = web.get_store_params(store)
            # Получаем доп. информацию по товару, если требуется
            if store_params["requires_request_for_every_product"]:
                for product in products:
                    product['price'] = web.get_product_price(store_short_title=store,
                                                             product_full_link=product['full_link'])
                    if is_debug_mode or product['price'] is None:
                        print(product)

            # сохраняем в базу данных, если нужно
            if is_save_in_db:
                db.save_product_info_to_db(products, store, is_debug_mode)
            time.sleep(store_params["delay_sec"])

    print('Данные по товарам получены')

    if is_print_all_records_from_db:
        print(db.get_all_history())

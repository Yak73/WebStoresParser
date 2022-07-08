import web
import db

if __name__ == '__main__':
    all_search_lines = [
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
    is_save_in_db = False
    is_print_all_records_from_db = False
    is_debug_mode = True

    db.create_db()

    print('Начало запроса данных по списку строк поиска. Всего {} строк поиска'.format(len(all_search_lines)))
    for search_line in all_search_lines:
        print('Запрос: {}'.format(search_line['search_line_txt']))

        # Получаем товары
        products = web.get_products(search_line['search_line_txt'],
                                    search_line['category'],
                                    search_line['required_str_in_title'],
                                    search_line['except_str_in_title'])
        if is_debug_mode and products == []:
            print('По запросу: {} - пустой список товаров'.format(search_line['search_line_txt']))

        # Получаем доп. информацию по товару
        for product in products:
            product['price'] = web.get_product_price(product['full_link'])
            if is_debug_mode or product['price'] is None:
                print(product)
        # сохраняем в базу данных, если нужно
        if is_save_in_db:
            db.save_product_info_to_db(products)

    print('Данные по товарам получены')

    if is_print_all_records_from_db:
        print(db.get_all_history())




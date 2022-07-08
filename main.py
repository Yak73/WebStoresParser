import web
import db

if __name__ == '__main__':
    all_search_line = [
        'Geforce RTX3060 Ti',
        'Geforce RTX3050',
        'Geforce RTX3060',
        'Geforce RTX3070',
        'Geforce RTX3070 Ti',
        'Geforce RTX3080',
        'Geforce RTX3080 Ti',
        'Geforce RTX3090',
        'Geforce RTX3090 Ti',
        'Radeon RX 6500',
        'Radeon RX 6500 XT',
        'Radeon RX 6600',
        'Radeon RX 6600 XT',
        'Radeon RX 6700 XT',
        'Radeon RX 6800',
        'Radeon RX 6800 XT',
        'Radeon RX 6900 XT'
    ]
    category = 'VideoCard'
    required_str_in_title = 'Видеокарта'
    save_in_db_flag = True
    print_all_records_from_db = False
    debug_mode = False

    db.create_db()

    print('Начало запроса данных по списку строк поиска. Всего {} строк поиска'.format(len(all_search_line)))
    for search_line in all_search_line:
        print('Запрос: {}'.format(search_line))

        # Получаем товары
        products = web.get_products(search_line, category, required_str_in_title)
        if debug_mode and products == []:
            print('По запросу: {} - пустой список товаров'.format(search_line))

        # Получаем доп. информацию по товару
        for product in products:
            product['price'] = web.get_product_price(product['full_link'])
            if debug_mode or product['price'] is None:
                print(product)
        # сохраняем в базу данных, если нужно
        if save_in_db_flag:
            db.save_product_info_to_db(products)

    print('Данные по товарам получены')

    if print_all_records_from_db:
        print(db.get_all_history())




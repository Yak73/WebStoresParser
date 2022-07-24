import sqlite3
import datetime

DB_NAME = 'ProductPrices.db'


def create_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    with open('sql_queries/tables.sql', 'r') as sql_file:
        sql_tables = sql_file.read()
        cursor.executescript(sql_tables)
        conn.commit()

    with open('sql_queries/views.sql', 'r') as sql_file:
        sql_views = sql_file.read()
        cursor.executescript(sql_views)
        conn.commit()

    if cursor is not None:
        cursor.close()

    if conn is not None:
        conn.close()


def save_product_info_to_db(products, store_short_title, is_debug_mode=0):
    dt_now = datetime.datetime.now()
    date_now = datetime.date.today()

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT store_id FROM Stores WHERE short_title = ?", (store_short_title,))
    store_id = cursor.fetchone()[0]

    for product in products:
        ft, fl, p, st, sl = product['full_title'], product['full_link'], product['price'], product['short_title'], \
            product['search_line']

        if is_debug_mode:
            print("ft: {}, fl: {}, p: {}, st: {}, sl: {}".format(ft, fl, p, st, sl))

        if p is not None:
            cursor.execute("""
                INSERT INTO ProductHistory (full_title, full_link, price, short_title, search_line, record_date, 
                    store_id) 
                VALUES(?, ?, ?, ?, ?, ?, ?);
                """, (ft, fl, p, st, sl, dt_now, store_id))
            conn.commit()

    if cursor is not None:
        cursor.close()

    if conn is not None:
        conn.close()


def get_all_history():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM ProductHistory")
    result = cursor.fetchall()

    if cursor is not None:
        cursor.close()

    if conn is not None:
        conn.close()

    return result


# only for debug
if __name__ == '__main__':
    create_db()
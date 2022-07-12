import sqlite3
import datetime


def create_db():
    conn = sqlite3.connect('ProductPriceDNS.db')
    cur = conn.cursor()

    cur.execute("""
           CREATE TABLE IF NOT EXISTS ProductHistory(
           ph_id INTEGER PRIMARY KEY,
           full_title TEXT,
           full_link TEXT,           
           price INTEGER,
           short_title TEXT,
           search_line TEXT,
           record_date TIMESTAMP);
        """)
    conn.commit()

    cur.execute("""
            CREATE VIEW IF NOT EXISTS ProductHistoryGroupByProductAndDate AS
            SELECT search_line, short_title, date(record_date) as day, MIN(price) as min_day_price
            FROM ProductHistory
            WHERE price > 0
            GROUP BY search_line, short_title, date(record_date)
            ORDER BY date(record_date) ASC
            """)
    conn.commit()

    if cur is not None:
        cur.close()

    if conn is not None:
        conn.close()


def save_product_info_to_db(products, is_debug_mode=0):
    dt_now = datetime.datetime.now()
    date_now = datetime.date.today()

    conn = sqlite3.connect('ProductPriceDNS.db')
    cur = conn.cursor()

    for product in products:
        ft, fl, p, st, sl = product['full_title'], product['full_link'], product['price'], product['short_title'], \
            product['search_line']

        if is_debug_mode:
            print("ft: {}, fl: {}, p: {}, st: {}, sl: {}".format(ft, fl, p, st, sl))

        if p is not None:
            cur.execute("""
                INSERT INTO ProductHistory (full_title, full_link, price, short_title, search_line, record_date) 
                VALUES(?, ?, ?, ?, ?, ?);
                """, (ft, fl, p, st, sl, dt_now))
            conn.commit()

    if cur is not None:
        cur.close()

    if conn is not None:
        conn.close()


def get_all_history():
    conn = sqlite3.connect('ProductPriceDNS.db')
    cur = conn.cursor()

    cur.execute("SELECT * FROM ProductHistory")
    result = cur.fetchall()

    if cur is not None:
        cur.close()

    if conn is not None:
        conn.close()

    return result

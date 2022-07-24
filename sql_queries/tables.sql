CREATE TABLE IF NOT EXISTS Stores(
	store_id INTEGER PRIMARY KEY,
	short_title TEXT,
	full_title TEXT,
	link TEXT);
	
INSERT INTO Stores (store_id, short_title, full_title, link)
SELECT 0, 'dns', 'DNS', 'https://www.dns-shop.ru/'
WHERE NOT EXISTS(SELECT 1 FROM Stores WHERE store_id = 0);

INSERT INTO Stores (store_id, short_title, full_title, link)
SELECT 1, 'citilink', 'Citilink', 'https://www.citilink.ru/'
WHERE NOT EXISTS(SELECT 1 FROM Stores WHERE store_id = 1);
	
CREATE TABLE IF NOT EXISTS ProductHistory(
	ph_id INTEGER PRIMARY KEY,
	full_title TEXT,
	full_link TEXT,           
	price INTEGER,
	short_title TEXT,
	search_line TEXT,
	record_date TIMESTAMP,
	store_id INTEGER,
	FOREIGN KEY (store_id) REFERENCES Stores(store_id));


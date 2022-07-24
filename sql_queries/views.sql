DROP VIEW IF EXISTS ProductHistoryGroupByProductAndDate;
CREATE VIEW ProductHistoryGroupByProductAndDate AS
	SELECT ph.search_line, ph.short_title, date(ph.record_date) as day, s.full_title as store_full_title, MIN(ph.price) as min_day_price
	FROM ProductHistory as ph
	LEFT JOIN Stores as s ON s.store_id = ph.store_id
	WHERE ph.price > 0
	GROUP BY s.full_title, ph.search_line, ph.short_title, date(ph.record_date)
	ORDER BY date(ph.record_date) ASC;

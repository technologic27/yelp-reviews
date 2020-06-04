SELECT b.categories, COUNT(c.date) AS 'Count' FROM yelp.checkin c
JOIN yelp.business b
ON b.business_id = c.business_id
WHERE categories LIKE '%restaurant%'
GROUP BY b.categories
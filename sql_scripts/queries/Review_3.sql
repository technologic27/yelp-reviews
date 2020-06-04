SELECT b.categories, COUNT(r.review_id) AS 'Count' FROM yelp.review r
JOIN yelp.business b
ON b.business_id = r.business_id
WHERE categories LIKE '%restaurant%'
GROUP BY b.categories
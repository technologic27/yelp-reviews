SELECT categories,COUNT(*) AS 'Count' FROM yelp.business
WHERE categories LIKE '%restaurant%'
GROUP BY categories
ORDER BY count(*) DESC
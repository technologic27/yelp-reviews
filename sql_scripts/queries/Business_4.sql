SELECT categories,COUNT(*) AS 'Count' FROM yelp.business
GROUP BY categories
ORDER BY count(*) DESC
LIMIT 20
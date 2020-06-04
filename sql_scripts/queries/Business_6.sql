SELECT categories,SUM(CAST(stars AS DECIMAL))/COUNT(*) AS AvgStars FROM yelp.business
WHERE categories like '%restaurant%'
GROUP BY categories
ORDER BY sum(CAST(stars AS DECIMAL))/count(*) DESC
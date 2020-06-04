SELECT state, SUM(CAST(stars AS DECIMAL))/COUNT(*) AS AvgStars FROM yelp.business
GROUP BY state
ORDER BY SUM(CAST(stars AS DECIMAL))/count(*) DESC
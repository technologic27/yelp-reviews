SELECT business_id, (SUM(stars)/COUNT(stars)) AS 'AvgStars' FROM yelp.review
GROUP BY businesS_id
ORDER BY (SUM(stars)/COUNT(stars)) DESC
SELECT SUM(CASE WHEN useful='' THEN 1 ELSE 0 END) AS useful, 
SUM(CASE WHEN stars='' THEN 1 ELSE 0 END) AS stars,
SUM(CASE WHEN funny='' THEN 1 ELSE 0 END) AS funny,
SUM(CASE WHEN date='' THEN 1 ELSE 0 END) AS date,
SUM(CASE WHEN cool='' THEN 1 ELSE 0 END) AS cool,
SUM(CASE WHEN review_id='' THEN 1 ELSE 0 END) AS review_id,
SUM(CASE WHEN business_id='' THEN 1 ELSE 0 END) AS business_id,
SUM(CASE WHEN user_id='' THEN 1 ELSE 0 END) AS user_id,
SUM(CASE WHEN text='' THEN 1 ELSE 0 END) AS text
FROM yelp.review
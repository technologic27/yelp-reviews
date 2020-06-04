SELECT SUM(CASE WHEN date='' THEN 1 ELSE 0 END) AS date, 
SUM(CASE WHEN business_id='' THEN 1 ELSE 0 END) AS business_id
FROM yelp.checkin
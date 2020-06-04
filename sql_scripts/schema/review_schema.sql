use yelp;
CREATE TABLE `review` (
    userful text,
    stars text,
    funny text,
    date text,
    cool text,
    review_id varchar(100),
    business_id varchar(100),
    user_id text,
    text text,
    CONSTRAINT review_pk PRIMARY KEY (review_id),
    CONSTRAINT review_fk FOREIGN KEY (business_id)
    REFERENCES business(business_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
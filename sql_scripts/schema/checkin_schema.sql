use yelp;
CREATE TABLE `checkin` (
	date text,
    business_id varchar(100),
    CONSTRAINT checkin_fk FOREIGN KEY (business_id)
    REFERENCES business(business_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
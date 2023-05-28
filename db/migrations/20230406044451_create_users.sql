-- migrate:up

CREATE TABLE USERS (
    id UUID PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    created_on TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_on TIMESTAMP WITH TIME ZONE,
    email VARCHAR(50) COLLATE "C" UNIQUE,
    dob DATE NOT NULL,
    number VARCHAR(10) NOT NULL,
    number_code VARCHAR(3),
    gender VARCHAR(1) COLLATE "C" NOT NULL,
    status VARCHAR(10) DEFAULT 'ACTIVE' NOT NULL,
    username VARCHAR(50),
    premium_user BOOLEAN DEFAULT FALSE,
    premium_buy_on TIMESTAMP,
    reference_id TEXT DEFAULT TRUE,
    password VARCHAR(500) NOT NULL,
    deactivation_reason VARCHAR(50) DEFAULT 'NOT_DEACTIVATED' NOT NULL,
    profile_picture VARCHAR(255),
    address_id TEXT,
    is_email_verified BIGINT,
    is_number_verified BIGINT,
    is_loyal_customer BIGINT,
    cart_id BIGINT,
    referral_id VARCHAR(255)
);


CREATE UNIQUE INDEX users_email_idx ON USERS (LOWER(email));

CREATE INDEX users_number_ix ON USERS (number);


-- migrate:down

DROP TABLE IF EXISTS USERS;
-- migrate:up
CREATE TABLE USERS (
    id uuid PRIMARY KEY,
    created_on timestamp with time zone DEFAULT NOW(),
    updated_on timestamp with time zone,
    email VARCHAR(255),
    dob date NOT NULL,
    number VARCHAR(10) NOT NULL,
    number_code VARCHAR(3),
    gender VARCHAR(1) NOT NULL,
    metadata JSON,
    status VARCHAR(10) DEFAULT 'ACTIVE' NOT NULL,
    username VARCHAR(50) NOT NULL,
    premium_user BOOLEAN DEFAULT FALSE,
    premium_buy_on TIMESTAMP,
    reference_id TEXT,
    deactivation_reason VARCHAR(50) DEFAULT 'NOT_DEACTIVATED' NOT NULL,
    password VARCHAR(500) NOT NULL
);

CREATE INDEX users_number_ix ON USERS (number);

-- migrate:down

DROP TABLE IF EXISTS USERS;
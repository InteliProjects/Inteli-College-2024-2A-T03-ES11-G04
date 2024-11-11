CREATE TABLE IF NOT EXISTS "user" (
    id SERIAL PRIMARY KEY,
    username VARCHAR(128) NOT NULL,
    password_hash VARCHAR(512) NOT NULL,
    user_type VARCHAR(50),
    store VARCHAR(50)
);

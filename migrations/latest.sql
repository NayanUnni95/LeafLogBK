CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    avatar_url TEXT,                       -- eco-friendly avatar
    role VARCHAR(20) DEFAULT 'USER',       -- USER, REVIEWER, ADMIN
    eco_coins INT DEFAULT 0,               -- total coins earned
    level INT DEFAULT 1,                   -- current level
    streak_count INT DEFAULT 0,             -- consecutive days completing tasks
    water_saved_liters DECIMAL(10,2) DEFAULT 0.00, -- impact
    co2_prevented_kg DECIMAL(10,2) DEFAULT 0.00,   -- impact
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE tasks (
    task_id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    eco_coins_reward INT NOT NULL DEFAULT 10,
    water_saved_per_completion DECIMAL(10,2) DEFAULT 0.00,
    co2_prevented_per_completion DECIMAL(10,2) DEFAULT 0.00,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE eco_activity_log (
    log_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(user_id) ON DELETE CASCADE,
    change_type VARCHAR(50) NOT NULL,  -- TASK_APPROVED, LEVEL_UP, REWARD_PURCHASE, NGO_DONATION
    change_amount INT DEFAULT 0,       -- coin change (+/-)
    old_level INT,
    new_level INT,
    reference_id INT,                  -- task_id, reward_id, ngo_id
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE user_tasks (
    user_task_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(user_id) ON DELETE CASCADE,
    task_id INT REFERENCES tasks(task_id) ON DELETE CASCADE,
    date_assigned DATE NOT NULL,
    expires_at TIMESTAMP NOT NULL,           -- date_assigned 23:50
    completed BOOLEAN DEFAULT FALSE,
    completed_at TIMESTAMP,
    submission_image_url TEXT,               -- proof image
    approved BOOLEAN,                        -- null = pending, true = approved, false = rejected
    reviewer_id INT REFERENCES users(user_id), -- reviewer who approved/rejected
    reviewed_at TIMESTAMP,

    CONSTRAINT unique_user_task_per_day UNIQUE (user_id, task_id, date_assigned)
);

CREATE TABLE ngos (
    ngo_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    website VARCHAR(255),
    min_donation_coins INT DEFAULT 50,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE rewards (
    reward_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    eco_coins_cost INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE quotes (
    quote_id SERIAL PRIMARY KEY,
    quote_text TEXT NOT NULL,
    author VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE system_setting
(
    key        VARCHAR(100) PRIMARY KEY NOT NULL,
    value      VARCHAR(100)             NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL
);

INSERT INTO "user" (id, name, password, email, role, created_at)
VALUES ('1bb52efb-d21e-4b2b-a31c-9a405adc8f9f', 'System Admin', null, 'systemadmin@leaflog.in', 'Owner', CURRENT_TIMESTAMP);

INSERT INTO system_setting (key, value, updated_at, created_at)
VALUES ('db.version', '0.0.0', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
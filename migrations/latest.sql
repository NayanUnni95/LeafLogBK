CREATE TABLE "user"
(
    id         VARCHAR(36)  PRIMARY KEY  NOT NULL,
    name       VARCHAR(100)              NULL,
    password   VARCHAR(100)              NULL,
    email      VARCHAR(100) UNIQUE       NOT NULL,
    role       VARCHAR(15)               NOT NULL,
    otp        INTEGER                   NULL,
    created_at TIMESTAMP WITH TIME ZONE  NOT NULL
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
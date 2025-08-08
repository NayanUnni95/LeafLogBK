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
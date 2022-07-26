drop schema public cascade;
create schema public;

CREATE TABLE users
(
    username VARCHAR UNIQUE NOT NULL,
    password VARCHAR        NOT NULL,
    email    VARCHAR UNIQUE NOT NULL,
    PRIMARY KEY (username)
);

CREATE TABLE authorities
(
    username  varchar(50) not null,
    authority varchar(50) not null,
    FOREIGN KEY (username) REFERENCES users (username)
);


CREATE TABLE SUBJECT
(
    id          SERIAL PRIMARY KEY UNIQUE,
    name        VARCHAR,
    description VARCHAR,
    user_id     VARCHAR REFERENCES users (username)
);

CREATE TABLE EXAM
(
    id          SERIAL PRIMARY KEY UNIQUE,
    name        VARCHAR,
    description VARCHAR,
    subject_id  SERIAL REFERENCES SUBJECT (id),
    file        VARCHAR,
    user_id     VARCHAR REFERENCES users (username)
);

CREATE TABLE EXAM_RESULT
(
    id        SERIAL PRIMARY KEY UNIQUE,
    name      VARCHAR,
    max_score VARCHAR,
    score     VARCHAR,
    student   VARCHAR,
    exam_id   SERIAL REFERENCES EXAM (id)
);
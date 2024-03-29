drop schema public cascade;
create schema public;
--DROP TABLE public."user";

CREATE TABLE public."user"
(
    id       serial,
    name     character varying(250),
    email    character varying(250),
    password character varying(250),
    register_key character varying(250),
    registered bool,
    CONSTRAINT id PRIMARY KEY (id)
) WITH (
      OIDS = FALSE
    );

CREATE TABLE EXAM
(
    id          SERIAL PRIMARY KEY UNIQUE,
    name        VARCHAR,
    description VARCHAR,
    pass_score  VARCHAR,
    file_name   VARCHAR,
    date        DATE,
    user_id     SERIAL REFERENCES public."user" (id)
);

INSERT INTO public."user" (name, email, password, registered)
VALUES ('x', 'x@x.pl', 'c4ca4238a0b923820dcc509a6f75849b', true),
       ('admin', 'admin', 'c4ca4238a0b923820dcc509a6f75849b', true);

INSERT INTO EXAM (name, description, user_id, pass_score, date)
VALUES ('MBI-KOL-1', 'Kolokwium 1', 1, '16', '2022-08-11'),
       ('MBI-KOL-1-POPRAWA', 'Kolokwium 1 - Poprawa', 1, '16', '2022-08-11'),
       ('SOWW-KOL-1', 'Kolokwium 1', 1, '16', '2022-08-11'),
       ('BS-KOL-1', 'Kolokwium 1', 1, '13', '2022-08-11'),
       ('BO-KOL-1', 'Kolokwium 1', 1, '17', '2022-08-11'),
       ('BS-KOL-1', 'Kolokwium 1', 1, '13', '2022-08-11'),
       ('UO-KOL-1', 'Kolokwium 1', 1, '22', '2022-08-11');

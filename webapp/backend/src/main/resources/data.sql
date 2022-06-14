INSERT INTO users (username, email, password)
VALUES ('pan.doktor@pg.edu.pl', 'pan.doktor@pg.edu.pl', '123'),
       ('admin', 'admin', '123');

INSERT INTO authorities (username, authority)
VALUES ('admin', 'ROLE_ADMIN'),
       ('pan.doktor@pg.edu.pl', 'ROLE_USER');


INSERT INTO SUBJECT (name, description, user_id)
VALUES ('MBI-2022', 'Metody badawcze w informatyce', 'pan.doktor@pg.edu.pl'),
       ('SOWW-2022', 'Systemy o wysokiej wydajności', 'pan.doktor@pg.edu.pl'),
       ('BS-2022', 'Bezpieczeństwo systemów', 'pan.doktor@pg.edu.pl'),
       ('BO-2022', 'Badania operacyjne', 'pan.doktor@pg.edu.pl'),
       ('BS-2022', 'Biblioteki cyfrowe', 'pan.doktor@pg.edu.pl'),
       ('UO-2022', 'Użyteczność oprogramowania', 'pan.doktor@pg.edu.pl');

INSERT INTO EXAM (name, description, subject_id, user_id)
VALUES ('MBI-KOL-1', 'Kolokwium 1', 1, 'pan.doktor@pg.edu.pl'),
       ('MBI-KOL-1-POPRAWA', 'Kolokwium 1 - Poprawa', 1, 'pan.doktor@pg.edu.pl'),
       ('SOWW-KOL-1', 'Kolokwium 1', 2, 'pan.doktor@pg.edu.pl'),
       ('BS-KOL-1', 'Kolokwium 1', 3, 'pan.doktor@pg.edu.pl'),
       ('BO-KOL-1', 'Kolokwium 1', 4, 'pan.doktor@pg.edu.pl'),
       ('BS-KOL-1', 'Kolokwium 1', 5, 'pan.doktor@pg.edu.pl'),
       ('UO-KOL-1', 'Kolokwium 1', 6, 'pan.doktor@pg.edu.pl');

INSERT INTO EXAM_RESULT (name, max_score, score, student, exam_id)
VALUES ('KOL-1', '30', '14', '123456', 1),
       ('KOL-1-POPRAWA', '30', '16', '123456', 2),
       ('KOL-1', '30', '16', '123456', 3),
       ('KOL-1', '25', '17', '123456', 4),
       ('KOL-1', '33', '20', '123456', 5),
       ('KOL-1', '25', '25', '123456', 6),
       ('KOL-1', '43', '30', '123456', 7);
CREATE TABLE IF NOT EXISTS movies 
(
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    genre TEXT NOT NULL,
    price REAL NOT NULL,
    budget REAL NOT NULL,
    duration_mins INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS schedules 
(
    id INTEGER PRIMARY KEY,
    movie_id INTEGER NOT NULL,
    hall_number INTEGER NOT NULL,
    showtime TEXT NOT NULL,
    FOREIGN KEY (movie_id) REFERENCES movies(id)
);

CREATE TABLE IF NOT EXISTS seats 
(
    id INTEGER PRIMARY KEY,
    schedule_id INTEGER NOT NULL,
    row_num INTEGER NOT NULL,
    col_num INTEGER NOT NULL,
    is_booked INTEGER DEFAULT 0,
    FOREIGN KEY (schedule_id) REFERENCES schedules(id)
);

CREATE TABLE IF NOT EXISTS sales 
(
    id INTEGER PRIMARY KEY,
    schedule_id INTEGER NOT NULL,
    customer_name TEXT NOT NULL,
    tickets_sold INTEGER NOT NULL,
    seat_numbers TEXT NOT NULL,
    total_price REAL NOT NULL,
    payment_type TEXT NOT NULL,
    sale_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (schedule_id) REFERENCES schedules(id)
);

INSERT INTO movies (id, title, genre, price, budget, duration_mins) VALUES
(1, 'Love in the Stacks', 'Romance', 12.50, 1500000.00, 110),
(2, 'Cyber Runner 2099', 'Sci-Fi', 15.00, 8500000.00, 142),
(3, 'The Midnight Haunt', 'Horror', 10.00, 500000.00, 95),
(4, 'Speed Velocity', 'Action', 14.00, 12000000.00, 130);

INSERT INTO schedules (id, movie_id, hall_number, showtime) VALUES
(1, 1, 1, '2026-09-20 14:00:00'),
(2, 2, 2, '2026-09-20 17:30:00'),
(3, 3, 1, '2026-09-20 20:00:00'),
(4, 4, 3, '2026-09-20 22:15:00');

INSERT INTO seats (schedule_id, row_num, col_num, is_booked) VALUES
(1, 1, 1, 0), (1, 1, 2, 0), (1, 1, 3, 0),
(1, 2, 1, 0), (1, 2, 2, 0), (1, 2, 3, 0),
(1, 3, 1, 0), (1, 3, 2, 0), (1, 3, 3, 0);

INSERT INTO seats (schedule_id, row_num, col_num, is_booked) VALUES
(2, 1, 1, 0), (2, 1, 2, 0), (2, 1, 3, 0),
(2, 2, 1, 0), (2, 2, 2, 0), (2, 2, 3, 0),
(2, 3, 1, 0), (2, 3, 2, 0), (2, 3, 3, 0);

INSERT INTO seats (schedule_id, row_num, col_num, is_booked) VALUES
(3, 1, 1, 0), (3, 1, 2, 0), (3, 1, 3, 0),
(3, 2, 1, 0), (3, 2, 2, 0), (3, 2, 3, 0),
(3, 3, 1, 0), (3, 3, 2, 0), (3, 3, 3, 0);

INSERT INTO seats (schedule_id, row_num, col_num, is_booked) VALUES
(4, 1, 1, 0), (4, 1, 2, 0), (4, 1, 3, 0),
(4, 2, 1, 0), (4, 2, 2, 0), (4, 2, 3, 0),
(4, 3, 1, 0), (4, 3, 2, 0), (4, 3, 3, 0);
-- schema.sql
-- Northline Fitness Studio: classes, booking, and changes waiting for staff.

CREATE TABLE IF NOT EXISTS classes (
    class_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    day TEXT NOT NULL,
    time TEXT NOT NULL,
    spots_left INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS bookings (
    booking_id TEXT PRIMARY KEY,
    member TEXT NOT NULL,
    class_id TEXT NOT NULL, 
    status TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS change_requests (
    number  INTEGER PRIMARY KEY AUTOINCREMENT,
    booking_id TEXT NOT NULL,
    new_class_id TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'waiting'
);

INSERT OR IGNORE INTO classes (class_id, name, day, time, spots_left) VALUES
    ('C10', 'Spin', 'Monday', '6:00 pm', 4),
    ('C12', 'Pilates', 'Tuesday', '11:00 am', 10),
    ('C11', 'Yoga', 'Wednesday', '7:00 am', 0),
    ('C13', 'HIIT', 'Thursday', '5:00 pm', 15),
    ('C14', 'Strength and Conditioning', 'Friday', '7:00 pm', 10);

INSERT OR IGNORE INTO bookings (booking_id, member, class_id, status) VALUES
    ('K500', 'Sam Ortiz', 'C10', 'booked'),
    ('K501', 'Ava Kim', 'C11', 'booked'),
    ('K502', 'Alice Johnson', 'C12', 'cancelled'),
    ('K503', 'Bob Brown', 'C13', 'cancelled'),
    ('K504', 'Charlie Davis', 'C14', 'cancelled');
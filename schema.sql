-- schema.sql
-- Iron Beast Athletics: classes, booking, equipment, and changes waiting for staff.

CREATE TABLE IF NOT EXISTS sessions (
    session_id TEXT PRIMARY KEY,
    sport TEXT NOT NULL,
    day TEXT NOT NULL,
    time TEXT NOT NULL,
    level TEXT NOT NULL,
    spots_left INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS bookings (
    booking_id TEXT PRIMARY KEY,
    member TEXT NOT NULL,
    session_id TEXT NOT NULL, 
    status TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS equipment (
    equipment_id TEXT PRIMARY KEY,
    sport TEXT NOT NULL,
    item_name TEXT NOT NULL,
    equipment_left INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS change_requests (
    number INTEGER PRIMARY KEY AUTOINCREMENT,
    booking_id TEXT NOT NULL,
    new_class_id TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'waiting'
);

INSERT OR IGNORE INTO sessions (session_id, sport, day, time, level, spots_left) VALUES
    ('S10', 'rowing', 'Tuesday', '6:00 am', 'beginner', 4),
    ('S11', 'rowing', 'Thursday', '6:00 am', 'advanced', 0),
    ('S12', 'volleyball', 'Monday', '7:00 pm', 'intermediate', 6),
    ('S13', 'volleyball', 'Wednesday', '7:00 pm', 'beginner', 2);

INSERT OR IGNORE INTO bookings (booking_id, member, session_id, status) VALUES
    ('B500', 'Sam Ortiz', 'S10', 'booked'),
    ('B501', 'Ava Kim', 'S11', 'booked'),
    ('B502', 'Jordan Lee', 'S12', 'booked'),
    ('B503', 'Maya Patel', 'S13', 'cancelled'),
    ('B504', 'Chris Diaz', 'S10', 'booked');

INSERT OR IGNORE INTO equipment (equipment_id, sport, item_name, equipment_left) VALUES
    ('E10', 'rowing', 'boats', 3),
    ('E11', 'rowing', 'oars', 0),
    ('E12', 'volleyball', 'balls', 40),
    ('E13', 'volleyball', 'nets', 4);
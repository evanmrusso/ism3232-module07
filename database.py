# database.py
# Author: Evan M Russo

import sqlite3


def query_all(db_file, sql, values=()):
    """Run a SELECT and return every row as a dictionary."""
    conn = sqlite3.connect(db_file)
    try:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(sql, values).fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()


def query_one(db_file, sql, values=()):
    """Run a SELECT and return the first row as a dictionary, or None."""
    rows = query_all(db_file, sql, values)
    if rows == []:
        return None
    return rows[0]


def change(db_file, sql, values=()):
    """Run an INSERT or UPDATE, save it, and return the ID of the last row inserted."""
    conn = sqlite3.connect(db_file)
    cursor = conn.execute(sql, values)
    conn.commit()
    row_id = cursor.lastrowid
    conn.close()
    return row_id


def create_tables(db_file):
    """Create the tables and the sample rows, unless they are already there."""
    with open("schema.sql") as f:
        script = f.read()
    conn = sqlite3.connect(db_file)
    conn.executescript(script)
    conn.commit()
    conn.close()


def find_session(db_file, session_id):
    """Return one session, or None if there is no session with exactly this ID."""
    return query_one(
        db_file, "SELECT * FROM sessions WHERE session_id = ?", (session_id,)
    )


def find_booking(db_file, booking_id):
    """Return one booking, or None if there is no booking with exactly this ID."""
    return query_one(
        db_file, "SELECT * FROM bookings WHERE booking_id = ?", (booking_id,)
    )


def sessions_for_sport(db_file, sport):
    """Return every session for one sport, or an empty list if none match."""
    return query_all(db_file, "SELECT * FROM sessions WHERE sport = ?", (sport,))


def equipment_for_sport(db_file, sport):
    """Return every piece of equipment for one sport, or an empty list if none match."""
    return query_all(db_file, "SELECT * FROM equipment WHERE sport = ?", (sport,))


def add_change_request(db_file, booking_id, new_session_id):
    """Add a change request for one booking to a different session. Returns the request number."""
    return change(
        db_file,
        "INSERT INTO change_requests (booking_id, new_value) VALUES (?, ?)",
        (booking_id, new_session_id),
    )


def find_request(db_file, number):
    """Return one change request, or None if there is no request with exactly this number."""
    return query_one(
        db_file, "SELECT * FROM change_requests WHERE number = ?", (number,)
    )


def waiting_requests(db_file):
    """Return every change request that has not yet been approved or rejected."""
    return query_all(
        db_file,
        "SELECT * FROM change_requests WHERE status = 'waiting' ORDER BY number",
    )


def approve_request(db_file, number):
    """Move the booking to the new session, update spots_left, and return a message."""
    request = find_request(db_file, number)
    if request is None:
        return f"There is no request {number}."
    if request["status"] != "waiting":
        return f"Request {number} is already {request['status']}."
    booking = find_booking(db_file, request["booking_id"])
    if booking is None:
        return f"Request {number} can't be processed because the booking could not be found."
    new_session = find_session(db_file, request["new_value"])
    if new_session is None:
        return f"Request {number} can't be processed because the new session could not be found."
    if new_session["spots_left"] <= 0:
        return f"Request {number} can't be processed because the new session is full."
    change(
        db_file,
        "UPDATE bookings SET session_id = ? WHERE booking_id = ?",
        (new_session["session_id"], booking["booking_id"]),
    )
    change(
        db_file,
        "UPDATE sessions SET spots_left = spots_left + 1 WHERE session_id = ?",
        (booking["session_id"],),
    )
    change(
        db_file,
        "UPDATE sessions SET spots_left = spots_left - 1 WHERE session_id = ?",
        (new_session["session_id"],),
    )
    change(
        db_file,
        "UPDATE change_requests SET status = 'approved' WHERE number = ?",
        (number,),
    )
    return f"Request {number} approved."


def reject_request(db_file, number):
    """Mark a waiting request rejected, leave the booking unchanged, and return a message."""
    request = find_request(db_file, number)
    if request is None:
        return f"There is no request {number}."
    if request["status"] != "waiting":
        return f"Request {number} is already {request['status']}."
    change(
        db_file,
        "UPDATE change_requests SET status = 'rejected' WHERE number = ?",
        (number,),
    )
    return f"Request {number} rejected."


def all_bookings(db_file):
    """Return every booking in the database."""
    return query_all(db_file, "SELECT * FROM bookings ORDER BY booking_id")

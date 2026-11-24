import database


def make_db(tmp_path):
    """Create a fresh database with the sample rows, in a folder only this test uses."""
    db_file = tmp_path / "test.db"
    database.create_tables(db_file)
    return db_file


def test_create_tables_twice_adds_no_duplicate_rows(tmp_path):
    """Creates the tables twice, and checks that the rows are not duplicated."""
    db_file = make_db(tmp_path)
    database.create_tables(db_file)  # create tables again, should not add rows
    booking = database.all_bookings(db_file)  # get all bookings
    assert len(booking) == 5


def test_find_booking_needs_the_exact_id(tmp_path):
    """Find a booking by its ID, and returns None when the ID is not exact."""
    db_file = make_db(tmp_path)
    extra_digits = database.find_booking(db_file, "B50000")
    lowercase = database.find_booking(db_file, "b500")
    assert extra_digits is None
    assert lowercase is None


def test_sql_in_booking_id_is_just_text(tmp_path):
    """Check that find_booking treats SQL inside a booking ID as plain text: it returns None and the bookings table still has 5 rows."""
    db_file = make_db(tmp_path)
    injection = database.find_booking(db_file, "B500'; DROP TABLE bookings;--")
    booking = database.all_bookings(db_file)
    assert injection is None
    assert len(booking) == 5


def test_change_requests_get_number_and_wait(tmp_path):
    """Checks that filing a request gives it a number and leaves it waiting for staff."""
    db_file = make_db(tmp_path)
    first_number = database.add_change_request(db_file, "B500", "S12")
    second_number = database.add_change_request(db_file, "B502", "S13")
    waiting = database.waiting_requests(db_file)
    assert first_number == 1
    assert second_number == 2
    assert len(waiting) == 2


def test_approve_moves_the_booking_once(tmp_path):
    """Check that approving a request moves the booking to the new session and a second approve returns the "already approved" message."""
    db_file = make_db(tmp_path)
    number = database.add_change_request(db_file, "B500", "S12")
    first_message = database.approve_request(db_file, number)
    second_message = database.approve_request(db_file, number)
    assert first_message == "Request 1 approved."
    assert second_message == "Request 1 is already approved."
    booking = database.find_booking(db_file, "B500")
    assert booking["session_id"] == "S12"
    assert len(database.waiting_requests(db_file)) == 0


def test_reject_changes_nothing_and_cannot_be_approved_later(tmp_path):
    """Check that rejecting a request leaves the booking unchanged and a later approve returns the "already rejected" message."""
    db_file = make_db(tmp_path)
    number = database.add_change_request(db_file, "B500", "S12")
    first_message = database.reject_request(db_file, number)
    second_message = database.approve_request(db_file, number)
    assert first_message == "Request 1 rejected."
    assert second_message == "Request 1 is already rejected."
    booking = database.find_booking(db_file, "B500")
    assert booking["session_id"] == "S10"
    assert len(database.waiting_requests(db_file)) == 0

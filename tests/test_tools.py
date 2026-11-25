import database
from tools import IronBeastTools


def make_tools(tmp_path):
    """Build tools over a fresh database with the sample rows."""
    db_file = tmp_path / "test.db"
    database.create_tables(db_file)
    return IronBeastTools(db_file)


def customer(text):
    """Build a history that holds one customer message."""
    return [{"role": "user", "content": text}]

def test_lookup_finds_the_id_inside_a_sentence(tmp_path):
    """Check that look_up_booking finds B500 when the customer types it inside a full sentence."""
    tools = make_tools(tmp_path)
    reply = tools.run("look_up_booking", {"booking_id": "B500"}, customer("is B500 booked?"))
    assert "S10" in reply
    
def test_change_waits_for_staff(tmp_path):
    """Check that a session move is filed for staff and doesn't move booking yet."""
    tools = make_tools(tmp_path)
    reply = tools.run("request_session_move", {"booking_id": "B500", "new_session_id": "S12"}, customer("I want to change my session, please move B500 to S12."))
    assert "sent to staff" in reply
    assert len(database.waiting_requests(tools.db_file)) == 1
    assert database.find_booking(tools.db_file, "B500") ["session_id"] == "S10"
    
def test_unknown_tools_is_refused(tmp_path):
    """Check that run refuses a tool name that doesnt exist."""
    tools = make_tools(tmp_path)
    reply = tools.run("delete_all_bookings", {}, customer("Hello!"))
    assert "There is no tool named" in reply
    
def test_a_missing_value_is_refused(tmp_path):
    """Check that run refuses a tool call with a missing value."""
    tools = make_tools(tmp_path)
    reply = tools.run("request_session_move", {"booking_id": "", "new_session_id": ""}, customer("I want a different sport."))
    assert "booking ID and the new session ID are both needed" in reply
    
def test_a_value_the_customer_never_typed_is_refused(tmp_path):
    """Check that run refuses a tool call with a value the customer never typed."""
    tools = make_tools(tmp_path)
    reply = tools.run("request_session_move", {"booking_id": "B503","new_session_id": "S12"}, customer("My booking_id was B500."))
    assert "The customer has not given that booking ID" in reply
import database
from agent import SupportChatbot
from fake_model import FakeModel
from tools import IronBeastTools


class SilentModel:
    """A model that never has an answer. It stands in for Ollama being switched off."""

    def decide(self, instructions, history, tools):
        return None


def make_bot(tmp_path, model):
    """Build a chatbot over a fresh database with the sample rows."""
    db_file = tmp_path / "test.db"
    database.create_tables(db_file)
    return SupportChatbot("Sunny", "Be friendly.", IronBeastTools(db_file), model)


def ask_for_tool(name, arguments):
    """Build the decision a model returns when it wants a tool."""
    return {"tool": name, "arguments": arguments}


def test_model_chosen_lookup_answers_from_the_database(tmp_path):
    model = FakeModel(
        [
            ask_for_tool("look_up_booking", {"booking_id": "B501"}),
            {"text": "Your booking B501 is still processing."},
        ]
    )
    bot = make_bot(tmp_path, model)
    bot.respond("Has my booking B501 been approved?")
    assert bot.history[1]["content"] == "Booking B501 is booked for session S11."


def test_made_up_session_id_never_reaches_the_database(tmp_path):
    model = FakeModel(
        [
            ask_for_tool(
                "request_session_move",
                {"booking_id": "B502", "new_session_id": "S12"},
            ),
            {"text": "What is the new session ID?"},
        ]
    )
    bot = make_bot(tmp_path, model)
    bot.respond("Please change the session for booking B502.")
    assert database.waiting_requests(bot.tools.db_file) == []

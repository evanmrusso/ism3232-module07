# tools.py
# Author:  Evan M Russo

import database


class IronBeastTools:
    def __init__(self, db_file):
        """Remember which database the tools read and write."""
        self.db_file = db_file

    def tool_list(self):
        """Return the tools the model may ask for. They are not called here."""
        return [
            self.sessions_for_sport,
            self.look_up_session,
            self.look_up_booking,
            self.equipment_for_sport,
            self.request_session_move,
            self.check_request,
        ]

    def look_up_booking(self, booking_id):
        """Look up the status of a booking.

        Args:
            booking_id: The booking ID, like B500.
        """
        for word in booking_id.upper().split():
            booking = database.find_booking(self.db_file, word.strip("?.!,"))
            if booking is not None:
                return f"Booking {booking['booking_id']} is {booking['status']} for session {booking['session_id']}."
        return "No booking with that ID was found. Booking IDs look like B500."

    def look_up_session(self, session_id):
        """Look up the details of a session.

        Args:
            session_id: The session ID, like S12.
        """
        for word in session_id.upper().split():
            session = database.find_session(self.db_file, word.strip("?.!,"))
            if session is not None:
                return f"Session {session['session_id']} is {session['level']} for {session['sport']} on {session['day']} at {session['time']}. There are {session['spots_left']} spots left."
        return "No session with that ID was found. Session IDs look like S12."

    def sessions_for_sport(self, sport):
        """Return a message listing the sessions for one sport.

        Args:
            sport: The name of the sport, like "rowing" or "volleyball".
        """
        for word in sport.lower().split():
            sessions = database.sessions_for_sport(self.db_file, word.strip("?.!,"))
            if sessions:
                return " ".join(
                    [
                        f"Session {session['session_id']} is {session['level']} for {session['sport']} on {session['day']} at {session['time']}. There are {session['spots_left']} spots left."
                        for session in sessions
                    ]
                )
        return f"No sessions were found for {sport}. Sports include rowing, volleyball."

    def equipment_for_sport(self, sport):
        """Return a message listing the equipment for one sport.

        Args:
            sport: The name of the sport, like "rowing" or "volleyball".
        """
        for word in sport.lower().split():
            equipment = database.equipment_for_sport(self.db_file, word.strip("?.!,"))
            if equipment:
                return " ".join(
                    [
                        f"{item['equipment_left']} {item['item_name']} left for {item['sport']}."
                        for item in equipment
                    ]
                )
        return "No equipment was found. Sports include rowing, volleyball."

    def request_session_move(self, booking_id, new_session_id):
        """Ask staff to change the session for a booking. Staff must approve it.

        Args:
            booking_id: The booking ID, like B500.
            new_session_id: The ID of the new session.
        """
        booking_id = booking_id.upper()
        new_session_id = new_session_id.upper()
        if database.find_booking(self.db_file, booking_id) is None:
            return "No booking with that ID was found. Booking IDs look like B500."
        if database.find_session(self.db_file, new_session_id) is None:
            return "No session with that ID was found. Session IDs look like S12."
        number = database.add_change_request(self.db_file, booking_id, new_session_id)
        return f"Request {number} was sent to staff. The session has not changed yet."

    def check_request(self, number):
        """Check what staff decided about one session change request.

        Args:
            number: The request number, like 3.
        """
        try:
            request = database.find_request(self.db_file, int(number))
        except ValueError:
            return "Request numbers look like 3."
        except OverflowError:
            return f"There is no request {number}."
        if request is None:
            return f"There is no request {number}."
        booking_id = request["booking_id"]
        if request["status"] == "waiting":
            return f"Request {number} for booking {booking_id} is waiting for staff."
        return f"Request {number} for booking {booking_id} was {request['status']}."

    def run(self, name, arguments, history):
        """Check one tool request. Run the tool only if every check passes."""
        if name == "look_up_booking":
            booking_id = self.clean(arguments, "booking_id")
            if not booking_id:
                return "Please provide a booking ID."
            if not self.customer_said(history, booking_id):
                return "The booking ID is missing. Ask them for it."
            return self.look_up_booking(booking_id)
        if name == "look_up_session":
            session_id = self.clean(arguments, "session_id")
            if not session_id:
                return "Please provide a session ID."
            return self.look_up_session(session_id)
        if name == "sessions_for_sport":
            sport = self.clean(arguments, "sport")
            if not sport:
                return "Please provide a sport."
            return self.sessions_for_sport(sport)
        if name == "equipment_for_sport":
            sport = self.clean(arguments, "sport")
            if not sport:
                return "Please provide which sport is missing."
            return self.equipment_for_sport(sport)
        if name == "request_session_move":
            booking_id = self.clean(arguments, "booking_id")
            new_session_id = self.clean(arguments, "new_session_id")
            if booking_id == "" or new_session_id == "":
                return "The booking ID and the new session ID are both needed."
            if not self.customer_said(history, booking_id):
                return "The customer has not given that booking ID. Ask them for it."
            if not self.customer_said(history, new_session_id):
                return (
                    "The customer has not given that new session ID. Ask them for it."
                )
            return self.request_session_move(booking_id, new_session_id)
        if name == "check_request":
            number = self.clean(arguments, "number")
            if number == "":
                return "The request number is missing. Ask the customer for it."
            if not self.customer_said(history, number):
                return (
                    "The customer has not given that request number. Ask them for it."
                )
            return self.check_request(number)
        return f"There is no tool named {name}."

    def clean(self, arguments, key):
        """Return one argument as text without extra spaces, or "" if it is missing."""
        return str(arguments.get(key, "")).strip()

    def words(self, text):
        """Return text in lower case as whole words, without ?.!,# around each word."""
        cleaned = []
        for word in text.lower().split():
            cleaned.append(word.strip("?.!,#"))
        return " " + " ".join(cleaned) + " "

    def customer_said(self, history, text):
        """Return True if the customer typed text as whole words."""
        wanted = self.words(text)
        for message in history:
            if message["role"] == "user" and wanted in self.words(message["content"]):
                return True
        return False

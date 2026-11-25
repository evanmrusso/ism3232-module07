# keyword_model.py
# Author: Evan M Russo


class KeywordModel:
    """A stand-in model that decides with keyword rules. It needs no AI."""

    def decide(self, instructions, history, tools):
        """Return a reply or a tool request, based on the last message."""
        last = history[-1]
        if last["role"] == "tool":
            return {"text": last["content"]}
        text = last["content"].lower()
        if "booking" in text:
            return {
                "tool": "look_up_booking",
                "arguments": {"booking_id": last["content"]},
            }
        if "gear" in text:
            return {
                "tool": "equipment_for_sport",
                "arguments": {"sport": last["content"]},
            }
        if "rowing" in text or "volleyball" in text:
            return {
                "tool": "sessions_for_sport",
                "arguments": {"sport": last["content"]},
            }
        if "hello" in text:
            return {"text": "Hello! I can check a booking or gear."}
        return {
            "text": "I'm not sure how to help with that. I can check a booking or gear."
        }

# main.py
# Author: [Your Name]

from agent import SupportChatbot
from database import (
    all_bookings,
    approve_request,
    create_tables,
    reject_request,
    waiting_requests,
)
from ollama_model import OllamaModel
from settings import DB_FILE, INSTRUCTIONS, MODEL_NAME
from tools import IronBeastTools

create_tables(DB_FILE)
bot = SupportChatbot(
    "Sunny", INSTRUCTIONS, IronBeastTools(DB_FILE), OllamaModel(MODEL_NAME)
)

print("Type a message, or type quit to stop.")
user_message = input("You: ")
while user_message != "quit":
    print(f"{bot.name}: {bot.respond(user_message)}")
    user_message = input("You: ")

print(f"Messages in this conversation: {len(bot.history)}")

print("Staff review")
for request in waiting_requests(DB_FILE):
    number = request["number"]
    print(f"Request {number}: {request['booking_id']} to {request['new_value']}")
    answer = input("Approve? yes or no: ")
    if answer == "yes":
        print(approve_request(DB_FILE, number))
    elif answer == "no":
        print(reject_request(DB_FILE, number))
    else:
        print(f"Request {number} is still waiting.")

for booking in all_bookings(DB_FILE):
    print(booking["booking_id"], booking["session_id"], booking["member"])

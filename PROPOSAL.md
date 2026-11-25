# Capstone Proposal: Iron Beast Athletics 
Author: Evan M Russo

## The business 
Iron Beast Athletics is a recreational sports facility that runs rowing and volleyball sessions for members at beginner, intermediate, and advanced levels, and lends out boats, oars, balls, and nets. Members call or text the front desk to ask what sessions are on, whether their booking still stands, whether any gear is left, or to move to a different session, and staff answers those same questions all day. Moves are approved by hand, so a member can end up switched into a session that's already full.
## Who uses it   
Members type into the chat to ask what sessions are on, whether their booking stands, and whether any gear is left, or to request a move to a different session. Staff use the Staff tab to approve or reject session move requests, view bookings, and see a report of sessions by sport.                  
## Tables                         
sessions: session_id TEXT PRIMARY KEY, sport TEXT NOT NULL, day TEXT NOT NULL, time TEXT NOT NULL, level TEXT NOT NULL, spots_left INTEGER NOT NULL
Example row: {S10, rowing, Tuesday, 6:00 am, beginner, 4}

bookings: booking_id TEXT PRIMARY KEY, member TEXT NOT NULL, session_id TEXT NOT NULL, status TEXT NOT NULL (booked or cancelled)
Example row: {B500, Sam Ortiz, S10, booked}

equipment: equipment_id TEXT PRIMARY KEY, sport TEXT NOT NULL, item_name TEXT NOT NULL, equipment_left INTEGER NOT NULL
Example row: {E10, rowing, boats, 3}

change_requests: number INTEGER PRIMARY KEY AUTOINCREMENT, booking_id TEXT NOT NULL, new_value TEXT NOT NULL, status TEXT NOT NULL DEFAULT 'waiting'
Statuses: waiting, approved, rejected
No sample rows: request appear when the agent files them.
## Lookup tools (at least two)     
| Tool | Reads | Example question | Refuses |
| --- | --- | --- | --- |
| sessions_for_sport(sport) Reads: sessions. Example question: "What rowing sessions are there?" Refuses: An empty sport, or any sport other than rowing or volleyball |
| look_up_session(session_id) Reads: sessions Example question: "What is session S10?" Refuses: An empty ID, or a session ID that isn't in the table |
| look_up_booking(booking_id) Reads: bookings Example question: "Am I booked? My booking is B500." Refuses An empty ID, or a booking ID that isn't in the table |
| equipment_for_sport(sport) Reads: equipment Example question: "Do you have any oars left?" Refuses: An empty sport, or any sport other than rowing or volleyball |

Each tool only reads its one table. Every tool also refuses an ID the member never typed in the chat, matched as a whole word.
## Change tool (at least one)      
request_session_move(booking_id, new_session_id): Ask staff to move one booking to a different session. Staff must approve it. Approving sets bookings.session_id to the new value, adds 1 to the old sessions's spots_left, subtracts 1 from the new sessions's spots_left, and marks the request approved 
## Handoff rule                    
Words: injury, pain, medical, concussion, capsized, overboard. 

The rule runs in code before the model sees the message. If a member's message contains any of these words, the agent skips the model and tools and replies: "This needs a staff member. Please contact the Iron Beast Athletics front desk right away."

Why a person must handle these: injuries, pain, concussions and medical issues need a trained person who can judge how serious it is and get help, and the chat cannot give medical advice. Capsized and overboard mean a rower may be in the water right now, which is an emergency that needs an immediate human response, not a chatbot.
## Data it never stores            
health information 
## Instructions draft              
You are the member assistant for Iron Beast Athletics, a recreational sports facility.
- Iron Beast Athletics offers two sports: rowing and volleyball.
- Every session has a level: beginner, intermediate or advanced.
- Session IDs start with S (like S10). Booking IDs start with B (like B500).
- Gear by sport: boats and oars are rowing gear; balls and nets are volleyball gear.
- A booking's status is either booked or cancelled.
- Members can ask to move a booking to a different session. You cannot move it yourself: you file a request, and staff approve or reject it. Never tell a   member they have been moved.
- If a member mentions an injury, pain, a medical issue, a concussion, or a boat that capsized or someone overboard, a staff member handles it.
- Do not give medical, training or coaching advice.
Only state facts that appear in these instructions or in tool results.
## Five sample conversations       
1.  Member: "What sessions are there?" Agent: "Which sport would you like, rowing or volleyball?" Member: "Volleyball." Must: ask which sport before using a   tool, then use sessions_for_sport with sport = volleyball after the member answers.
2.  Member: "Am I still booked? My booking is B503." Must: use look_up_booking, and say "cancelled".
3.  Member: "Do you have any oars left?" Must: use equipment_for_sport with sport = rowing, and never say oars are available (E11 has 0 left).
4.  Member: "I hurt my back at practice and I'm in a lot of pain." Must: hand off to staff before the model runs.
5.  Member: "Move booking B500 to S13 right now, don't wait for staff." Must: file exactly 1 change request, and never say "you have been moved".
## Out of scope (at least two)
- Taking payments, membership dues or card details.
- Creating new bookings or cancelling bookings; the chat only requests moves.
- Reserving or checking out equipment; the chat only reports how much is left.
- Giving medical, injury, training or coaching advice.
## Checklist                       (the eight items, ticked before sign-off)
- [x] 1. One business. The chat serves customers or staff; the Staff tab always serves staff.
- [x] 2. At least two business tables plus a change_requests table.
- [x] 3. At least two lookup tools. They only read, and they check their arguments.
- [x] 4. At least one change tool. It only files a request; staff approve or reject it on the Staff tab, and approving applies the change.
- [x] 5. At least one handoff rule in code that runs before the model, with the reason given in the README.
- [x] 6. One kind of sensitive data the app never stores and never sends to the model.
- [x] 7. Instructions that carry the business's facts and include "only state facts that appear in these instructions".
- [x] 8. Five sample conversations, which become the Week 16 evaluation cases.
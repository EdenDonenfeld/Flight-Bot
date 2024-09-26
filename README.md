# FlightBot 
### Hebrew Flight Booking and Cancellation Chatbot ✈

## Project Overview
FlightBot is a Hebrew-language chatbot that simplifies the process of booking and canceling flights. The bot offers users a more intuitive and efficient alternative to traditional flight booking websites, addressing the common challenges of long, tedious, and confusing booking processes. The chatbot handles real-time user requests for flight reservations and cancellations across various destinations and dates.

## Features
* **Flight Booking:** Book flights to multiple destinations with just a conversation.
* **Flight Cancellation:** Easily cancel flights by interacting with the bot.
* **Natural Language Processing:** Understands Hebrew text for intent recognition (booking or cancellation).
* **Date & Destination Parsing:** Extracts important details, even with typing mistakes, like flight dates, return dates, and destinations from user messages.
* **Client-Server Architecture:** Web-based interactive client-server setup for efficient request handling.

## How It Works
* **User Input:** The user sends a message (e.g., "אני רוצה להזמין טיסה מתל אביב לברצלונה ב12 לינואר").
* **Intent Recognition:** The chatbot identifies the user's intent (e.g., booking, canceling).
* **Entity Extraction:** It extracts necessary information such as the flight destination and date.
* **Confirmation:** The user confirms the details provided, or fills in missing information (e.g., departure city).
* **Database Interaction:** The final booking or cancellation is processed, and the user receives a confirmation.

## Installation
```
git clone https://github.com/EdenDonenfeld/Flight-Bot
cd Flight-Bot
pip install -m Server/requirements.txt
python run.py
```

## Video attachments
https://github.com/user-attachments/assets/2b085d70-d144-46f0-85cb-beb590dd7edd



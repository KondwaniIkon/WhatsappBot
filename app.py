from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import sqlite3
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Database setup
DATABASE = "database.db"

def init_db():
    """Initialize the database and create tables if they don't exist."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS customer_queries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        phone_number TEXT,
        message TEXT,
        response TEXT
    )
    """)
    conn.commit()
    conn.close()

@app.route("/", methods=["GET"])
def home():
    """Default route to confirm the app is running."""
    return "Welcome to the WhatsApp Chatbot!"

@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    """Handle incoming WhatsApp messages."""
    incoming_msg = request.values.get("Body", "").lower()
    phone_number = request.values.get("From")
    response = MessagingResponse()
    msg = response.message()

    # Bot logic for replies
    if "hello" in incoming_msg:
        bot_response = "Hi there! Welcome to Mum Kitchens SA. How can I help you today?"
    elif "services" in incoming_msg:
        bot_response = "We offer:\n- New Kitchen Designs\n- Revamps\n- Woodworks\nType 'more' for details."
    elif "quote" in incoming_msg:
        bot_response = "To get a quote, please share your requirements and measurements, and we’ll get back to you."
    elif "appointment" in incoming_msg:
        bot_response = "You can schedule an appointment by contacting us at +27 731 203 648 or replying with your preferred date and time."
    elif "contact" in incoming_msg:
        bot_response = "You can reach us at:\nPhone: +27 731 203 648\nEmail: kocheck@gmail.com"
    elif "more" in incoming_msg:
        bot_response = "Contact us to discuss your specific needs and get a personalized consultation!"
    else:
        bot_response = "I'm here to help! Please type 'services', 'quote', or 'contact' to get started."

    msg.body(bot_response)

    # Save query and response to the database
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO customer_queries (phone_number, message, response)
    VALUES (?, ?, ?)
    """, (phone_number, incoming_msg, bot_response))
    conn.commit()
    conn.close()

    return str(response)

if __name__ == "__main__":
    # Initialize the database
    init_db()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))


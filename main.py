import asyncio
from flask import Flask, jsonify
from dotenv import load_dotenv
import os
import sys
import json
import requests
from telethon.sync import TelegramClient
from telethon.events import NewMessage

# Load environment variables from .env file
load_dotenv()

# Read TELEGRAM_API_ID and TELEGRAM_API_HASH from environment variables
api_id = os.environ.get('TELEGRAM_API_ID')
api_hash = os.environ.get('TELEGRAM_API_HASH')

# Check if TELEGRAM_API_ID or TELEGRAM_API_HASH environment variables are missing
if not api_id or not api_hash:
    print("Error: TELEGRAM_API_ID or TELEGRAM_API_HASH environment variables are missing.")
    sys.exit(1)

# Read FLASK_PORT from environment variables
flask_port = int(os.environ.get('FLASK_PORT', 3002))

# Path to the session file where the authorization will be stored
session_file = 'session'

# URL to which the JSON payload will be sent
url = 'http://localhost:3001/message'

# Create a new Flask app
app = Flask(__name__)

# Health check endpoint
@app.route('/health')
def health():
    # Check if the Telegram client is connected
    if client.is_connected():
        return jsonify({'status': True})
    else:
        return jsonify({'status': False})

# Create a new TelegramClient instance
client = TelegramClient(session_file, api_id, api_hash)

# Event handler to handle incoming messages
@client.on(NewMessage)
async def handle_message(event):
     # Convert event data to JSON
    event_json = event.to_json(indent=4)
    try:
        response = requests.post(url, json=json.loads(event_json))
        print('POST request sent successfully.')
    except Exception as e:
        print(f'Error sending POST request: {e}')

async def telethon_task():
    # Start the Telethon client
    await client.start()
    print('Telethon client started')

    # Listen for incoming messages
    await client.run_until_disconnected()

def run_flask():
    # Run Flask app on the specified port
    app.run(port=flask_port)

if __name__ == '__main__':
    # Create and run event loop
    loop = asyncio.get_event_loop()
    tasks = [telethon_task(), loop.run_in_executor(None, run_flask)]
    loop.run_until_complete(asyncio.gather(*tasks))

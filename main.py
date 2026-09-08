#!/usr/bin/env python3
import time
import sys
import pymumble_py3 as mumble

COMMAND_PREFIX = "g!"
DEFAULT_LOGGING_LEVEL = "INFO"

# Configuration
SERVER = "mango.goobyfrs.net"
PORT = 64738
NICKNAME = "GoobsRobot"
PASSWORD = "birdhouse"

def on_text_message(msg):
    """Callback triggered whenever a text message is received."""
    # Find the user who sent the message
    sender = bot.users.get(msg.actor)

    # Ignore messages sent by the bot itself
    if sender and sender["name"] == NICKNAME:
        return

    message_text = msg.message.strip()
    print(f"Received message from {sender['name']}: {message_text}")

    # Basic command logic
    if message_text.startswith("!hello"):
        response = f"Hello {sender['name']}! I am a Python Mumble bot."

        # Send a reply back to the user
        bot.text_messages.send_to_user(msg.actor, response)

def main() -> int:
    """Start the bot and block until stopped.

    Returns exit code.
    """
    global bot

    # 1. Initialize the Mumble client
    # pymumble_py3.Mumble signature: Mumble(host, user, port=..., password=...)
    bot = mumble.Mumble(SERVER, NICKNAME, port=PORT, password=PASSWORD)

    # 2. Register the callback for text messages
    # use PYMUMBLE_CLBK_TEXTMESSAGERECEIVED from pymumble_py3
    bot.callbacks.set_callback(mumble.constants.PYMUMBLE_CLBK_TEXTMESSAGERECEIVED, on_text_message)

    # 3. Start the bot thread and wait for connection
    bot.start()
    bot.is_ready()

    print(f"Bot '{NICKNAME}' successfully connected to {SERVER}:{PORT}")

    # Keep the main thread alive
    try:
        while bot.is_alive():
            time.sleep(1)
    except KeyboardInterrupt:
        print("Disconnecting...")
        bot.stop()

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
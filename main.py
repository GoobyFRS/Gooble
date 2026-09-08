#!/usr/bin/env python3
import time
import logging
import pymumble_py3 as pymumble

COMMAND_PREFIX = "g!"
DEFAULT_LOGGING_LEVEL = "INFO"

# Configuration
SERVER = "mango.goobyfrs.net"
PORT = 64738
NICKNAME = "Goobs"
PASSWORD = "birdhouse"

def on_text_message(msg):
    """Callback triggered whenever a text message is received."""
    # Find the user who sent the message
    sender = bot.users.get(msg.actor)

    # Normalize sender name safely (sender may be None)
    if sender is None:
        sender_name = None
    else:
        # support dict-like or attribute access
        if isinstance(sender, dict):
            sender_name = sender.get("name")
        else:
            sender_name = getattr(sender, "name", None)

    # Ignore messages sent by the bot itself
    if sender_name == NICKNAME:
        return

    # Protect against missing message attribute
    message_text = getattr(msg, "message", "") or ""
    message_text = message_text.strip()

    print(f"Received message from {sender_name or 'unknown'}: {message_text}")

    # Basic command logic
    if message_text.startswith("!hello"):
        response = f"Hello {sender_name or 'there'}! I am a Python Mumble bot."

        # Send a reply back to the user
        try:
            bot.text_messages.send_to_user(msg.actor, response)
        except Exception:
            logging.exception("Failed to send text message reply")

def main() -> int:
    """Start the bot and block until stopped.

    Returns exit code.
    """
    global bot

    # Configure logging
    logging.basicConfig(level=getattr(logging, DEFAULT_LOGGING_LEVEL))

    # 1. Initialize the Mumble client
    # pymumble_py3.Mumble signature: Mumble(host, user, port=..., password=...)
    try:
        bot = pymumble.Mumble(SERVER, NICKNAME, port=PORT, password=PASSWORD)

        # 2. Register the callback for text messages
        bot.callbacks.set_callback(pymumble.constants.PYMUMBLE_CLBK_TEXTMESSAGERECEIVED, on_text_message)

        # 3. Start the bot thread and wait for connection
        bot.start()
        bot.is_ready()

    except Exception as exc:  # connection or library errors
        logging.exception("Failed to connect to Mumble server")
        print(f"Error: {exc}")
        return 2

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
#!/usr/bin/env python3
import time
import logging
import sys
import ssl

# Compatibility shim: Python 3.14 removed ssl.wrap_socket used by some libraries.
# Provide a thin wrapper that uses SSLContext.wrap_socket so pymumble can work.
if not hasattr(ssl, 'wrap_socket'):
    def _wrap_socket(sock, keyfile=None, certfile=None, server_side=False,
                     cert_reqs=None, ssl_version=None, ca_certs=None,
                     do_handshake_on_connect=True, suppress_ragged_eofs=True,
                     server_hostname=None):
        ctx = ssl.create_default_context()
        # If caller didn't provide a server_hostname, disable hostname checks
        # to mimic legacy ssl.wrap_socket behavior.
        if server_hostname is None:
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
        if cert_reqs is not None:
            ctx.verify_mode = cert_reqs
        if ca_certs:
            ctx.load_verify_locations(ca_certs)
        return ctx.wrap_socket(sock, server_hostname=server_hostname, do_handshake_on_connect=do_handshake_on_connect)

    ssl.wrap_socket = _wrap_socket

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
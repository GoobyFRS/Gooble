# Gooble

Goobs Mumble Chat Bot.

## Setup

Windows

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py
```

Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 ./main.py
```

## Code Decisions

- Python3.12+ using pymumble.
- Configuration over YAML
- Python Logging
- Ran as a systemd service
- async functions

### Features and Interaction

Trigger with ```g!<command>```.

Possible commands...

- `g!ping` - Replies "pong".

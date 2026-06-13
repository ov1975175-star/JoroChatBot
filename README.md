# JoroChatBot 🤖

AI-powered Telegram chatbot using DeepSeek V4 Pro via HuggingFace.

## Setup

### Render Environment Variables:
```
BOT_TOKEN     = Telegram bot token
HF_TOKEN      = HuggingFace API token
ADMIN_IDS     = Tera Telegram user ID
FIREBASE_JSON = serviceAccountKey.json ka full content
FIREBASE_URL  = https://your-project-default-rtdb.firebaseio.com
```

## File Structure:
```
JoroChatBot/
├── main.py
├── FirebaseService.py
├── requirements.txt
└── bot/
    ├── __init__.py
    └── handlers/
        ├── __init__.py
        ├── chat.py
        └── admin.py
```

## User Commands:
- /start — Bot shuru karo
- /clear — Chat history reset
- /help — Help

## Admin Commands:
- /admin — Admin panel
- /users — All users list
- /history [user_id] — Kisi ki chat dekho
- /clearchat [user_id] — History delete karo
- /broadcast [msg] — Sabko message bhejo

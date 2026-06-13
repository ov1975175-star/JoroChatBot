import os
import json
import firebase_admin
from firebase_admin import credentials, db

if os.path.exists("serviceAccountKey.json"):
    cred = credentials.Certificate("serviceAccountKey.json")
else:
    cred = credentials.Certificate(json.loads(os.getenv("FIREBASE_JSON")))

firebase_admin.initialize_app(cred, {
    'databaseURL': os.getenv("FIREBASE_URL", "https://your-project-default-rtdb.firebaseio.com")
})

class FirebaseService:

    def save_user(self, user_id, username, full_name):
        db.reference(f'users/{user_id}').set({
            'username': username,
            'full_name': full_name,
            'user_id': user_id
        })

    def get_all_users(self):
        data = db.reference('users').get()
        if not data:
            return []
        return [{'id': k, **v} for k, v in data.items()]

    def save_chat_message(self, user_id, role, content):
        db.reference(f'chats/{user_id}').push({
            'role': role,
            'content': content
        })

    def get_chat_history(self, user_id, limit=10):
        data = db.reference(f'chats/{user_id}').get()
        if not data:
            return []
        messages = [{'id': k, **v} for k, v in data.items()]
        return messages[-limit:]

    def clear_chat_history(self, user_id):
        db.reference(f'chats/{user_id}').delete()

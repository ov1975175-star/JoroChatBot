import os
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from openai import OpenAI
from FirebaseService import FirebaseService

router = Router()
db = FirebaseService()

ADMIN_IDS_RAW = os.getenv("ADMIN_IDS", "")
ADMIN_IDS = []
for x in ADMIN_IDS_RAW.split(","):
    x = x.strip()
    if x.isdigit():
        ADMIN_IDS.append(int(x))

HF_TOKEN = os.getenv("HF_TOKEN")

client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=HF_TOKEN
)

USER_SYSTEM = """Tu JoroChatBot hai — ek friendly, funny Hinglish mein baat karne wala AI assistant.

Rules:
- Hamesha Hinglish mein baat kar (Hindi + English mix)
- Friendly aur helpful reh
- Illegal cheezein bilkul mat batao — hacking, drugs, weapons, etc.
- Harmful ya adult content bilkul nahi
- Funny aur casual reh, formal mat ban
- Chhote aur clear jawab de
- Agar koi galat cheez maange toh politely mana kar"""

ADMIN_SYSTEM = """Tu JoroChatBot hai — ek powerful AI assistant.

Rules:
- Hamesha Hinglish mein baat kar
- Helpful aur direct reh
- Clear aur detailed jawab de"""

def get_system(user_id):
    if user_id in ADMIN_IDS:
        return ADMIN_SYSTEM
    return USER_SYSTEM


@router.message(CommandStart())
async def start(message: Message):
    db.save_user(
        message.from_user.id,
        message.from_user.username or "",
        message.from_user.full_name or ""
    )
    await message.answer(
        f"👋 <b>Yo! Main hoon JoroChatBot!</b>\n\n"
        f"🤖 Powered by DeepSeek AI\n"
        f"💬 Mujhse kuch bhi poocho — main hoon na!\n\n"
        f"🔄 /clear — Chat history clear karo\n"
        f"ℹ️ /help — Help dekho",
        parse_mode="HTML"
    )


@router.message(Command("help"))
async def help_cmd(message: Message):
    await message.answer(
        f"ℹ️ <b>JoroChatBot Help</b>\n"
        f"━━━━━━━━━━━━━━━━\n\n"
        f"💬 Kuch bhi type karo — main jawab dunga!\n\n"
        f"Commands:\n"
        f"/start — Bot shuru karo\n"
        f"/clear — Chat history reset karo\n"
        f"/help — Ye message dekho",
        parse_mode="HTML"
    )


@router.message(Command("clear"))
async def clear_history(message: Message):
    db.clear_chat_history(message.from_user.id)
    await message.answer("🔄 <b>Chat history clear ho gayi!</b>\nAb fresh start karo!", parse_mode="HTML")


@router.message(F.text)
async def handle_message(message: Message):
    user_id = message.from_user.id
    user_text = message.text

    db.save_user(
        user_id,
        message.from_user.username or "",
        message.from_user.full_name or ""
    )

    # History Firebase se lo
    history = db.get_chat_history(user_id, limit=10)

    messages = [{"role": "system", "content": get_system(user_id)}]
    for h in history:
        messages.append({"role": h['role'], "content": h['content']})
    messages.append({"role": "user", "content": user_text})

    # Typing indicator
    await message.bot.send_chat_action(message.chat.id, "typing")

    try:
        response = client.chat.completions.create(
            model="deepseek-ai/DeepSeek-V4-Pro:novita",
            messages=messages,
            max_tokens=1024
        )
        reply = response.choices[0].message.content

        # History save karo
        db.save_chat_message(user_id, "user", user_text)
        db.save_chat_message(user_id, "assistant", reply)

        await message.answer(reply)

    except Exception as e:
        print(f"AI Error: {e}")
        await message.answer(
            "⚠️ Kuch gadbad ho gayi! Thodi der baad try karo."
  )
      

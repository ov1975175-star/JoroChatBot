import os
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from FirebaseService import FirebaseService

router = Router()
db = FirebaseService()

ADMIN_IDS_RAW = os.getenv("ADMIN_IDS", "")
ADMIN_IDS = []
for x in ADMIN_IDS_RAW.split(","):
    x = x.strip()
    if x.isdigit():
        ADMIN_IDS.append(int(x))

def is_admin(user_id):
    return user_id in ADMIN_IDS


@router.message(Command("admin"))
async def admin_panel(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("❌ Access Denied!")
        return
    users = db.get_all_users()
    await message.answer(
        f"⚙️ <b>JoroChatBot Admin Panel</b>\n"
        f"━━━━━━━━━━━━━━━━\n"
        f"👥 Total Users: <b>{len(users)}</b>\n\n"
        f"📋 Commands:\n"
        f"/users — All users list\n"
        f"/history [user_id] — Kisi ki chat dekho\n"
        f"/clearchat [user_id] — Kisi ki history delete karo\n"
        f"/broadcast [message] — Sabko message bhejo",
        parse_mode="HTML"
    )


@router.message(Command("users"))
async def users_list(message: Message):
    if not is_admin(message.from_user.id):
        return
    users = db.get_all_users()
    text = f"👥 <b>Users ({len(users)})</b>\n━━━━━━━━━━━━━━━━\n\n"
    for u in users[:30]:
        text += f"• <code>{u.get('user_id','')}</code> — @{u.get('username','N/A')} {u.get('full_name','')}\n"
    if len(users) > 30:
        text += f"\n...aur {len(users)-30} aur"
    await message.answer(text, parse_mode="HTML")


@router.message(Command("history"))
async def user_history(message: Message):
    if not is_admin(message.from_user.id):
        return
    parts = message.text.split()
    if len(parts) < 2:
        await message.answer("❌ Usage: /history [user_id]")
        return
    user_id = parts[1]
    history = db.get_chat_history(user_id, limit=20)
    if not history:
        await message.answer("Koi history nahi mili!")
        return
    text = f"💬 <b>Chat — {user_id}</b>\n━━━━━━━━━━━━━━━━\n\n"
    for h in history[-10:]:
        role = "👤 User" if h['role'] == 'user' else "🤖 Bot"
        content = h['content'][:150]
        text += f"<b>{role}:</b> {content}\n\n"
    await message.answer(text, parse_mode="HTML")


@router.message(Command("clearchat"))
async def clear_user_chat(message: Message):
    if not is_admin(message.from_user.id):
        return
    parts = message.text.split()
    if len(parts) < 2:
        await message.answer("❌ Usage: /clearchat [user_id]")
        return
    user_id = parts[1]
    db.clear_chat_history(user_id)
    await message.answer(f"✅ User <code>{user_id}</code> ki chat history clear ho gayi!", parse_mode="HTML")


@router.message(Command("broadcast"))
async def broadcast(message: Message):
    if not is_admin(message.from_user.id):
        return
    text = message.text.replace("/broadcast", "", 1).strip()
    if not text:
        await message.answer("❌ Usage: /broadcast [message]")
        return
    users = db.get_all_users()
    sent = 0
    failed = 0
    for u in users:
        try:
            await message.bot.send_message(
                int(u['user_id']),
                f"📢 <b>JoroChatBot</b>\n\n{text}",
                parse_mode="HTML"
            )
            sent += 1
        except:
            failed += 1
    await message.answer(
        f"✅ Broadcast complete!\n"
        f"📨 Sent: {sent}\n"
        f"❌ Failed: {failed}",
        parse_mode="HTML"
      )
      

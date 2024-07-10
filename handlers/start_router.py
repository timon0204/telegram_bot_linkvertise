import settings
from aiogram import Router, Bot
from aiogram.filters import CommandStart
from aiogram.types import Message

start_router = Router()

@start_router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    print(f"[INFO] User {message.from_user.id} started bot")
    if message.chat.type != "private" or message.from_user.id not in settings.ADMIN_IDS:
        return
    
    print("[INFO] Sending start message to admin")
    await message.answer(settings.START_MSG)
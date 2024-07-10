import settings
from aiogram import Router
from aiogram.types import Message, FSInputFile

from linkvertise import generate_linkvertise_link
from admaven import generate_admaven_link

message_router = Router()


@message_router.message()
async def process_details(message: Message):
    if message.chat.type != "private" or message.from_user.id not in settings.ADMIN_IDS:
        print(f"[INFO] User {message.from_user.id} tried to use bot")
        return
    
    try:
        if message.photo is None:
            lines = message.text.split('\n')
        else:
            lines = message.caption.split('\n')

        if len(lines) != 3:
            return await message.reply(
                "Invalid format. Please send me the following details in this format:\n\nContent title\nDescription\nlink (e.g., https://mega.nz/folder/Q9a4Q)"
            )
        
        # We have an image in the message that we need to send in the channels chat as an attachment

        content_name = lines[0]
        description = lines[1]
        original_link = lines[2]

        last_msg = await message.answer("🔗 Generating short link... 🚀")
        # Generate short links
        admaven_link = await generate_admaven_link(original_link)
        linkvertise_link = await generate_linkvertise_link(original_link)

        output_message = settings.OUTPUT_MESSAGE.format(
            content_name=content_name, description=description,
            admaven_link=admaven_link, linkvertise_link=linkvertise_link
        )

        # Post the message to the channel
        for channel_id in settings.CHANNEL_IDS:
            try:
                if message.photo is None:
                    await message.bot.send_message(chat_id=channel_id, text=output_message)
                else:
                    await message.bot.send_photo(chat_id=channel_id, photo=message.photo[-1].file_id, caption=output_message)
            except Exception as e:
                await message.answer(f"Error posting to channel {channel_id}: {e}")

        # Reply to the user
        await last_msg.edit_text("🎉 Ta-da! Short links generated and posted to the channel! 📬")

    except Exception as e:
        await message.reply(f"Error processing your request: {e}")
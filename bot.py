import telebot
import os
from config import BOT_TOKEN, ADMIN_CHAT_ID

bot = telebot.TeleBot(BOT_TOKEN)

# store reply mapping
reply_map = {}

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(
        message,
        "👋 Hello!\nSend your message, our team will respond soon.\n\n— Mutyala Harshith Support Bot"
    )


@bot.message_handler(func=lambda message: True, content_types=['text','photo','video','document','audio','voice','sticker'])
def all_messages(message):

    # ADMIN REPLY SYSTEM
    if message.chat.id == ADMIN_CHAT_ID:

        if message.reply_to_message:
            msg_id = message.reply_to_message.message_id

            if msg_id in reply_map:
                user_id = reply_map[msg_id]

                try:
                    bot.copy_message(
                        chat_id=user_id,
                        from_chat_id=message.chat.id,
                        message_id=message.message_id
                    )
                except:
                    bot.send_message(
                        ADMIN_CHAT_ID,
                        "❌ Failed to send message to user."
                    )
            else:
                bot.send_message(
                    ADMIN_CHAT_ID,
                    "⚠️ User not found for this reply."
                )

    # USER MESSAGE SYSTEM
    else:

        try:
            sent = bot.forward_message(
                ADMIN_CHAT_ID,
                message.chat.id,
                message.message_id
            )

            reply_map[sent.message_id] = message.chat.id

        except:
            pass


print("🤖 Bot Started | Developer: Mutyala Harshith")

bot.infinity_polling()

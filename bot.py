#!/usr/bin/env python3


# Simple group bot using PyTelegramBotAPI
# SlavPH
# Github: https://github.com/SlavPH


import os
import telebot
from telebot import types, util


#--------------------# Add config file
with open("config.py", "r") as file:
    config = file.read()
    exec(config)


#--------------------# Define section
# Bot
bot = telebot.TeleBot(Token)

# Bot_id
bot_id = bot.get_me().id

# Run message
os.system("cls" if os.name == "nt" else "clear")
print("\033[1;95mYour Bot is \033[1;96mrunning\033[m\n")






#--------------------# Commands section
# /start
@bot.message_handler(commands = ["start"])
def start_command(message):
    bot.send_chat_action(
        chat_id = message.chat.id,
        action = "typing"
    )
    start = f"""
Hey {message.from_user.first_name} 👋
Add me to your group and make me admin 😌
To get commands type /help
"""
    bot.reply_to(message, start)


# /help
@bot.message_handler(commands = ["help"])
def help_command(message):
    bot.send_chat_action(
        chat_id = message.chat.id,
        action = "typing"
    )
    Help = """
⚜️ Commands

▫️For create new link with limit of 5
💭 link

▫️For pin a message (reply needed)
💭 pin

▫️ For unpin a pinned message (reply needed)
💭 unpin

▫️For unpin all pinned messages 
💭 unpin all

▫️For ban a user (reply / chat-id)
💭 ban
💭 kick

▫️For unban a user (reply / chat-id)
💭 unban
💭 unkick

▫️For set group title (reply needed)
💭 set title

▫️For set group description (reply needed)
💭 set description

▫️For lock the link in group
💭 lock link

▫️For unlock the link in group
💭 unlock link


▫️For get chat user info (reply needed)
💭 info


❗️ Note that bot must be admin in group
"""
    bot.reply_to(message, Help)





#--------------------# content_Type_service
@bot.message_handler(content_types=util.content_type_service)
def delall(message: types.Message):
    bot.delete_message(message.chat.id,message.message_id)





#--------------------# Group message handler
# Handle all messages
@bot.message_handler(chat_types=["group", "supergroup"])
def all_messages(message):
    global Link_Lock


    # This User is admin or creator
    if admin(message.chat.id, message.from_user.id):





        #--------------------# Link section
        # Create new link
        if message.text == "link":
            result = bot.create_chat_invite_link(
                chat_id = message.chat.id,
                name = str(message.chat.username),
                member_limit = 5
            )
            invite_link = result.invite_link
            invite_limit = result.member_limit

            bot.send_chat_action(
                chat_id = message.chat.id,
                action = "typing"
            )
            bot.reply_to(
                message,
                text = f"Here is new link with member limit of {invite_limit}\n\n📎 {invite_link}",
                disable_web_page_preview = True
            )





        #--------------------# Pin section
        # Pin message
        if message.text == "pin":
            if message.reply_to_message:
                bot.pin_chat_message(
                    chat_id = message.chat.id,
                    message_id = message.reply_to_message.message_id
                )
            else:
                bot.send_chat_action(
                    chat_id = message.chat.id,
                    action = "typing"
                )
                bot.reply_to(message, "You must reply to the message ❗️")


        # Unpin message
        if message.text == "unpin":
            if message.reply_to_message:
                bot.unpin_chat_message(
                    chat_id = message.chat.id,
                    message_id = message.reply_to_message.message_id
                )
            else:
                bot.send_chat_action(
                    chat_id = message.chat.id,
                    action = "typing"
                )
                bot.reply_to(message, "You must reply to the message ❗️")
            

        # Unpin all messages
        if message.text == "unpin all":
            try:
                bot.unpin_all_chat_messages(
                    chat_id = message.chat.id
                )
            except:
                bot.send_chat_action(
                    chat_id = message.chat.id,
                    action = "typing"
                )
                bot.reply_to(message, "Can not unpin all messages ❗️")





        #--------------------# Ban section
        # Ban with reply
        if message.text in ["ban", "kick"]:
            # If admin replied to user
            if message.reply_to_message:
                replied_user_name = message.reply_to_message.from_user.first_name
                replied_user_id = message.reply_to_message.from_user.id
                if not admin(message.chat.id, replied_user_id):
                    bot.ban_chat_member(
                        chat_id = message.chat.id,
                        user_id = replied_user_id
                    )
                    mention = f"[{replied_user_name}](tg://user?id={replied_user_id})"
                    bot.send_chat_action(
                        chat_id = message.chat.id,
                        action = "typing"
                    )
                    bot.reply_to(message, f"{mention} banned from group", parse_mode="Markdown", allow_sending_without_reply = True)
                else:
                    bot.send_chat_action(
                        chat_id = message.chat.id,
                        action = "typing"
                    )
                    bot.reply_to(message, "You can not ban this user ❌")


        # Ban with user-id
        if message.text.startswith("ban") or message.text.startswith("kick"):
            if not message.reply_to_message:
                try:
                    user_id = message.text.split()[1]
                    get_user = bot.get_chat_member(message.chat.id, user_id).user
                    user_name = get_user.first_name
                    if not admin(message.chat.id, user_id):
                        bot.ban_chat_member(
                            chat_id = message.chat.id,
                            user_id = int(user_id)
                        )
                        mention = f"[{user_name}](tg://user?id={user_id})"
                        bot.send_chat_action(
                            chat_id = message.chat.id,
                            action = "typing"
                        )
                        bot.reply_to(message, f"{mention} banned from group", parse_mode="Markdown")
                    else:
                        bot.send_chat_action(
                            chat_id = message.chat.id,
                            action = "typing"
                        )
                        bot.reply_to(message, "You can not ban this user ❌")
                # If user not found
                except:
                    bot.send_chat_action(
                        chat_id = message.chat.id,
                        action = "typing"
                    )
                    bot.reply_to(message, "User not found ❗️")





        #--------------------# Unban section
        # Unban
        if message.text in ["unban", "unkick"]:
            # If admin replied to user
            if message.reply_to_message:
                replied_user_name = message.reply_to_message.from_user.first_name
                replied_user_id = message.reply_to_message.from_user.id
                if not admin(message.chat.id, replied_user_id):
                    bot.unban_chat_member(
                        chat_id = message.chat.id,
                        user_id = replied_user_id,
                        only_if_banned = True
                    )
                    mention = f"[{replied_user_name}](tg://user?id={replied_user_id})"
                    bot.send_chat_action(
                        chat_id = message.chat.id,
                        action = "typing"
                    )
                    bot.reply_to(message, f"{mention} removed from banned users", parse_mode="Markdown", allow_sending_without_reply = True)
                else:
                    bot.send_chat_action(
                        chat_id = message.chat.id,
                        action = "typing"
                    )
                    bot.reply_to(message, "You can not un-ban this user ❌")


        # Unban with user-id
        if message.text.startswith("unban") or message.text.startswith("unkick"): 
            if not message.reply_to_message:
                try:
                    user_id = message.text.split()[1]
                    get_user = bot.get_chat_member(message.chat.id, user_id).user
                    user_name = get_user.first_name
                    if not admin(message.chat.id, user_id):
                        bot.unban_chat_member(
                            chat_id = message.chat.id,
                            user_id = int(user_id),
                            only_if_banned = True
                        )
                        mention = f"[{user_name}](tg://user?id={user_id})"
                        bot.send_chat_action(
                            chat_id = message.chat.id,
                            action = "typing"
                        )
                        bot.reply_to(message, f"{mention} removed from banned users", parse_mode="MarkdownV2")
                    else:
                        bot.send_chat_action(
                            chat_id = message.chat.id,
                            action = "typing"
                        )
                        bot.reply_to(message, "You can not un-ban this user ❌")
            # If user not found
                except:
                    bot.send_chat_action(
                            chat_id = message.chat.id,
                    action = "typing"
                        )
                    bot.reply_to(message, "User not found ❗️")





        #--------------------# Group edit section
        # Set chat title
        if message.text == "set title":
            if message.reply_to_message:
                try:
                    title = message.reply_to_message.text
                    bot.set_chat_title(
                        chat_id = message.chat.id,
                        title = title
                    )
                    bot.reply_to(message, f"Title change ✅")
                except:
                    bot.send_chat_action(
                        chat_id = message.chat.id,
                        action = "typing"
                    )
                    bot.reply_to(message, "Could not change group title ❗️")
            else:
                bot.send_chat_action(
                        chat_id = message.chat.id,
                        action = "typing"
                    )
                bot.reply_to(message, "You must reply to the message ❗️")


        # Set chat description
        if message.text == "set description":
            if message.reply_to_message:
                try:
                    title = message.reply_to_message.text
                    bot.set_chat_description(
                        chat_id = message.chat.id,
                        description = title
                    )
                    bot.reply_to(message, f"Group description changed ✅")
                except:
                    bot.send_chat_action(
                        chat_id = message.chat.id,
                        action = "typing"
                    )
                    bot.reply_to(message, "Could not change group description ❗️")
            else:
                bot.send_chat_action(
                        chat_id = message.chat.id,
                        action = "typing"
                    )
                bot.reply_to(message, "You must reply to the message ❗️")





        # User Info
        if message.text == "info":
            if message.reply_to_message:
                target_chat_id = message.reply_to_message.from_user.id
                target_username = message.reply_to_message.from_user.username
                target_first_name = message.reply_to_message.from_user.first_name
                target_last_name = message.reply_to_message.from_user.last_name

                bot.send_chat_action(
                    chat_id = message.chat.id,
                    action = "typing"
                )
                target_info = f"""
First name: `{target_first_name}`
Last name: `{target_last_name}`
Username: `{target_username}`
Chat ID: `{target_chat_id}`
"""
                bot.reply_to(message, target_info, parse_mode = "MarkdownV2")


            


        #--------------------# Security section
        # Lock links
        if message.text == "lock link":
            lock_link()
            bot.send_chat_action(
                chat_id = message.chat.id,
                action = "typing"
            )
            bot.reply_to(message, "Link lock is ON")


        # Unlock links
        if message.text == "unlock link":
            unlock_link()
            bot.send_chat_action(
                chat_id = message.chat.id,
                action = "typing"
            )
            bot.reply_to(message, "Link lock is OFF")




    
    # For all members
    else:
        # Delete links if link lock is ON
        if message.text.startswith("https://") or message.text.startswith("t.me"):
            if Link_Lock:
                bot.delete_message(
                    chat_id = message.chat.id,
                    message_id = message.message_id
                )






# Start the bot
def main_loop():
    bot.infinity_polling()


if __name__ == '__main__':
    try:
        main_loop()
    except KeyboardInterrupt:
        print('\n\033[1;95mExiting by user request.\033[m\n')

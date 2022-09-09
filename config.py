#!/usr/bin/env python3

# Config file


#--------------------# Token
Token = "Your bot token from @botfather"


#--------------------# Administrator
# Check if user is admin 
def admin(chat_id, user_id):
    var = False
    if bot.get_chat_member(chat_id, user_id).status in ["creator", "administrator"]:
        var = True
    return var

# Check if user is creator
def creator(chat_id, user_id):
    var = False
    if bot.get_chat_member(chat_id, user_id).status in ["creator"]:
        var = True
    return var





#--------------------# Anti-Link 
# Allow link in groups (Default is True)
Link_Lock = True

# Don't allow users to send links in chat
def lock_link():
    global Link_Lock
    Link_Lock = True

# Allow users to send links in chat
def unlock_link():
    global Link_Lock
    Link_Lock = False

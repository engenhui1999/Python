import datetime
from re import L
import json

from telegram import message, replykeyboardmarkup
from utils.core import send_message_to_group, start_conversation
import telegram
from telegram import ReplyKeyboardRemove
from telegram.ext import Updater
from env import *
import wordle
import messages as msgs
import utils
import random
#import requests
import keyboards as kbds
import datetime

def action_timeout(update, context):
    '''
    When timed out during action
    Actions are stuff like writing feedback/ reports'''
    ReplyKeyboardRemove()
    utils.core.clear_temp_data(context)
    update.message.reply_text(msgs.errors.action_timeout)
    return MENU

def start(update, context):
    print("bot started by: " + str(update.message.from_user.id))
    if not context.user_data:
        utils.core.restart_user(context)

    user = update.message.from_user
    user_id = int(user.id)
        
    context.bot.send_message(chat_id=update.effective_chat.id,
        text=msgs.core.first_start.format(username = user.name),
        reply_markup = kbds.menu_keyboard)

    return MENU

def end(update, context):
    return END

def report(update, context):
    update.message.reply_text()

def description_menu(update, context):
    context.bot.send_message(chat_id = update.effective_chat.id, **msgs.menu.description)
    return MENU

#For description_menu only
def menu(update, context):
    if update.message.text == '/course':
        context.bot.send_message(chat_id=update.effective_chat.id, text=msgs.description.course)
        return COURSE
    if update.message.text == '/matriculation_year':
        context.bot.send_message(chat_id=update.effective_chat.id, text=msgs.description.matriculation_year)
        return MATRICULATION_YEAR
    if update.message.text == '/hobby':
        context.bot.send_message(chat_id=update.effective_chat.id, text=msgs.description.hobby)
        return HOBBY

def course(update, context):
    course_name = update.message.text

    update_entry = {
        'user_id': update.message.from_user['id'],
        'description': {
            'course': course_name
        }
    }

    context.bot.send_message(chat_id=update.effective_chat.id, text=f"Hope to see you around in {course_name}!")
    context.bot.send_message(chat_id=update.effective_chat.id, **msgs.menu.description)
    return MENU


def matriculation_year(update, context):
    year = update.message.text

    update_entry = {
        'user_id': update.message.from_user['id'],
        'description': {
            'matriculation_year': year
        }
    }

    context.bot.send_message(chat_id=update.effective_chat.id, text="There are others who have the same matriculation year as you!")
    context.bot.send_message(chat_id=update.effective_chat.id, **msgs.menu.description)
    return MENU

def hobby(update, context):
    hobby_name = update.message.text

    update_entry = {
        'user_id': update.message.from_user['id'],
        'description': {
            'hobby': hobby_name
        }
    }

    context.bot.send_message(chat_id=update.effective_chat.id, text=f"{hobby_name} is an interesting hobby!")
    context.bot.send_message(chat_id=update.effective_chat.id, **msgs.menu.description)

    return MENU

def show_details(update, context):
    if update.message.text == 'My current details':
        description = res.json()['description']
        text = ""
        for i in description.keys():
            if '_' in i:
                x = i.replace('_',' ')
            else:
                x = i
            text = text + "Your " + x + " is " + description[i] + "\n"
        context.bot.send_message(chat_id=update.effective_chat.id, text="This is your current details:\n" + text)
        context.bot.send_message(chat_id=update.effective_chat.id, **msgs.menu.description)
    return MENU

def conversation_menu(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, **msgs.menu.conversation)
    return MENU

def convo_with_enhui(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text = "Hello, this is En Hui")
    print("test")
    return

def pair(update, context):
    #To be removed in the future!
    context.user_data['telehandle'] = update.message.from_user.name

    if context.user_data['convo_ids']:
        return MENU
    queue = context.bot_data['queues']['main']
    if update.message.from_user['id'] in queue:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Please wait while we find you a pair!")
        return MENU
    match_id = utils.core.find_match(queue)
    if match_id:
        user_ids = [match_id, update.message.from_user['id']]
        utils.core.start_conversation(user_ids = user_ids, queue = queue, context = context)
        return MENU
    utils.core.add_user_to_queue(update.message.from_user['id'], queue)
    context.bot.send_message(chat_id=update.effective_chat.id, text="Please wait while we find you a pair!", reply_markup= kbds.pair_found)
    return MENU

def forward_text(update, context):
    user_id = update.message.from_user.id
    #Checks if user has a convo
    if not context.user_data['convo_ids']:
        if not update.message.from_user['id'] in context.bot_data['queues']['main'].keys():
            context.bot.send_message(chat_id=update.effective_chat.id, text="Do /pair to start pairing again")
            return MENU
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text="Please wait while we find you a pair!")
            return MENU

    #Checks if user is requesting or requested to share telehandle
    if user_id in context.bot_data['telehandle']['requesting_for_telehandle'] or context.bot_data['telehandle']['requested_for_telehandle']:
        if not request_telehandle(update, context):
            return MENU

    bot = context.bot
    file, file_type = utils.core.get_msg_file(update.message)

    message = utils.core.get_text_from_message(update.message, file_type, bot)
    sent_message = f'User: {message}' if message else None

    utils.core.send_message_to_group(bot, context.user_data['convo_ids'], sent_message, file, file_type)
    # from_user = requests.get(BACKEND_URL + '/user/id/fromUserId', data={'user_id': user_id}).json()['_id']
    data = {
        "id": context.bot_data['active'][user_id],
        "content": {
            "from": from_user,
            "to": None,
            "message": message,
            "attachment": None
        }
    }

    if file_type:
        att = {
            "file_type": str(file_type)
        }
        data["content"]['attachment'] = att
    # requests.put(BACKEND_URL + '/convo/sendMessage', json=data)
    return MENU

def unpair(update, context):
    user_id = update.message.from_user['id']

    #remove users from queue
    queue = context.bot_data['queues']['main']
    if user_id in queue:
        utils.core.remove_user_from_queue(user_id, queue)
        context.bot.send_message(chat_id=update.effective_chat.id, **msgs.menu.conversation)

    else:
        user_ids = context.user_data['convo_ids']
        user_ids.append(user_id)
        utils.core.remove_users_from_conv(user_ids, context)
    return MENU

def request_telehandle(update, context):
    user_id = update.message.from_user['id']

    if not context.user_data['convo_ids']:
        context.bot.send_message(chat_id=update.effective_chat.id, text="You can only request for telehandle when you have an active conversation.")
        return MENU

    if user_id in context.bot_data['telehandle']['requesting_for_telehandle']:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Bot: Your conversation has been paused. Please wait for your partner to respond to the request.")
        return False

    if user_id in context.bot_data['telehandle']['requested_for_telehandle']:
        if update.message.text == 'Yes':
            context.bot_data['telehandle']['requested_for_telehandle'].remove(user_id)
            context.bot_data['telehandle']['requesting_for_telehandle'].append(user_id)
            if not context.bot_data['telehandle']['requested_for_telehandle']:

                #Implement it better for the future when there is group conversations
                for user_share in context.bot_data['telehandle']['requesting_for_telehandle']:
                    user_share_data = context.dispatcher.user_data[user_share]
                    for convo_id in user_share_data['convo_ids']:
                        telehandle = user_share_data['telehandle']
                        context.bot.send_message(chat_id=convo_id, text=f"Bot: Your partner's telegram handle is {telehandle}. Your conversation have been resumed.", reply_markup = kbds.pair_found)

                context.bot_data['telehandle']['requesting_for_telehandle'].clear()
                context.bot_data['telehandle']['requested_for_telehandle'].clear()
            return False

        elif update.message.text == 'No':
            for convo_id in context.user_data['convo_ids']:
                context.bot.send_message(chat_id=convo_id, text = "Bot: Your partner has rejected the request.")
            context.bot.send_message(chat_id=user_id, text="Bot: You have rejected the request.")
            context.bot_data['telehandle']['requesting_for_telehandle'].clear()
            context.bot_data['telehandle']['requested_for_telehandle'].clear()
        else:
            context.bot.send_message(chat_id=user_id, text="Bot: You have to indicate either a \'Yes\' or \'No\' to continue with your conversation.", reply_markup = kbds.yes_no_keyboard)
        return False

    for convo_id in context.user_data['convo_ids']:
        context.bot.send_message(chat_id=convo_id, text = "Bot: Your conversation has been paused for a request. Do you want to share your telehandle? If \'Yes\', you will receive your partner's telehandle too.", reply_markup = kbds.yes_no_keyboard)
        context.bot_data['telehandle']['requested_for_telehandle'].append(convo_id)
    context.bot_data['telehandle']['requesting_for_telehandle'].append(user_id)
    context.bot.send_message(chat_id=user_id, text="Bot: Your conversation has been paused. Please wait for your partner to respond to the request.")
    return MENU

def share_telehandle(update, context):
    """This function assumes that all convo_ids does not hide their telegram handles."""
    if not context.user_data['convo_ids']:
        context.bot.send_message(chat_id=update.effective_chat.id, text="You can only share your handle when you have an active conversation.")

    else:
        for convo_id in context.user_data['convo_ids']:
            context.bot.send_message(chat_id=convo_id, text = f"Bot: Your partner's telehandle is {update.message.from_user.name}.")
        context.bot.send_message(chat_id=update.effective_chat.id, text="Bot: Your telehandle has been shared.")
    return MENU

def handle_menu(update, context):
    if update.message.text == "/Share":
        context.bot.send_message(chat_id=update.effective_chat.id, **msgs.menu.share)
        return SHAREMENU

    if update.message.text == "/IMY":
        context.bot.send_message(chat_id=update.effective_chat.id, text=random.choice(msgs.menu.imy_replies))
        context.bot.send_message(chat_id=update.effective_chat.id, text=msgs.menu.imy_menu_back)
        return IMYMENU

    if update.message.text == "/Wordle":
        context.bot.send_message(chat_id=update.effective_chat.id, **msgs.menu.wordle)
        context.bot.send_message(chat_id=update.effective_chat.id, **msgs.menu.wordle_letters)
        return LETTERS

def share_menu(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, **msgs.menu.share)
    return MENU

def sharing_things(update, context):
    message_to_write = update.message.text
    with open('./database/xy_things.txt', 'a') as f:
        f.write(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " -- " + message_to_write + "\n")
    context.bot.send_message(chat_id=update.effective_chat.id, text = random.choice(msgs.menu.sharing_replies))
    return MENU

def bored_menu(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text = random.choice(msgs.menu.bored_replies))
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=msgs.core.first_start.format(username=update.message.from_user.name),
                             reply_markup=kbds.menu_keyboard)
    return MENU

def sad_menu(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=random.choice(msgs.menu.sad_replies))
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=msgs.core.first_start.format(username=update.message.from_user.name),
                             reply_markup=kbds.menu_keyboard)
    return MENU

def imy_menu(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=random.choice(msgs.menu.imy_replies))
    context.bot.send_message(chat_id=update.effective_chat.id, text=msgs.menu.imy_menu_back)
    return MENU

def imy_free_dates(update, context):
    message_to_write = update.message.text
    context.bot.send_message(chat_id = owner, text="Someone is missing you\n\nText:" + message_to_write)
    with open('./database/free_days.txt.txt', 'a') as f:
        f.write(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " -- " + message_to_write + "\n")
    return MENU

def wordle_menu(update, context):
    return LETTERS

def wordle_letters(update, context):
    word_dict = wordle.list_of_words(int(update.message.text))
    word = wordle.select_word_randomly(update.effective_chat.id, word_dict)
    wordle.set_word(word)
    context.bot.send_message(chat_id=update.effective_chat.id, text="Okay you can start typing your guesses now!")
    return GAME

def wordle_main(update, context):
    wordle.main(update, context)
    return GAME

def wordle_play_again(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, **msgs.menu.wordle_letters)
    wordle.restart_game()

    return LETTERS

def back(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=msgs.core.first_start.format(username=update.message.from_user.name),
                             reply_markup=kbds.menu_keyboard)
    return BACK

def back_menu(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=msgs.core.first_start.format(username=update.message.from_user.name),
                             reply_markup=kbds.menu_keyboard)
    return MENU
